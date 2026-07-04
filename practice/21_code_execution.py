# Bài thực hành 21 — CODE EXECUTION + FILES API (Claude tự viết & chạy code)
# Chạy:  python practice/21_code_execution.py   (KHI NÀO BẠN MUỐN — file này để ĐỌC HIỂU)
#
# Mục tiêu THẤY TẬN MẮT:
#   1) Upload file dữ liệu lên Anthropic (Files API) -> lấy file_id.
#   2) Gửi file vào hội thoại bằng block "container_upload" (KHÔNG nhét cả CSV vào prompt).
#   3) Bật tool "code_execution" -> Claude TỰ viết Python, TỰ chạy trong sandbox,
#      rồi trả kết quả (phân tích + biểu đồ) mà app KHÔNG cần cài pandas/matplotlib.
#   4) Duyệt các block trả về: text / server_tool_use / code_execution_tool_result.
#   5) (Tuỳ chọn) Tải file kết quả (biểu đồ .png) mà Claude tạo ra về máy.
#
# ⚠️ ĐÂY LÀ SERVER-SIDE TOOL: code CHẠY TRÊN HẠ TẦNG CỦA ANTHROPIC, không phải máy bạn.
#    -> Bạn không tự thực thi tool này; API tự lo vòng chạy code và trả kết quả.
#
# ⚠️ TÍNH NĂNG BETA: cần bật beta header. Tên phiên bản header/tool có thể ĐỔI theo thời gian
#    -> nếu chạy lỗi, hãy đối chiếu lại docs chính thức Anthropic (Code Execution & Files API).

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

# ⭐ Bật 2 tính năng BETA qua header:
#    - code-execution: cho phép Claude chạy code trong sandbox.
#    - files-api:       cho phép upload/download file.
client = Anthropic(
    default_headers={
        "anthropic-beta": "code-execution-2025-08-25, files-api-2025-04-14"
    }
)

# ⭐ Dùng model HAIKU (theo yêu cầu).
model = "claude-haiku-4-5"

# Dùng đường dẫn TUYỆT ĐỐI theo vị trí file .py này -> chạy từ thư mục nào cũng đúng.
# (Nếu để "streaming.csv" trần, chạy `python practice/21_...` sẽ tìm sai thư mục.)
CSV_PATH = Path(__file__).parent / "streaming.csv"


# =====================================================================
# HELPERS — FILES API
# =====================================================================
# Bảng ánh xạ đuôi file -> mime type (để upload đúng loại).
MIME_BY_EXT = {
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".md": "text/plain",
    ".py": "text/plain",
    ".csv": "text/csv",
    ".json": "application/json",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def upload(file_path):
    """Tải 1 file lên Files API -> trả về metadata (có .id để dùng làm file_id)."""
    path = Path(file_path)
    mime = MIME_BY_EXT.get(path.suffix.lower())
    if not mime:
        raise ValueError(f"Chưa biết mime type cho đuôi: {path.suffix}")
    with open(path, "rb") as f:
        return client.beta.files.upload(file=(path.name, f, mime))


def list_files():
    """Liệt kê các file đã upload (dọn dẹp hoặc kiểm tra)."""
    return client.beta.files.list()


def delete_file(file_id):
    """Xoá 1 file trên server theo id."""
    return client.beta.files.delete(file_id)


def get_metadata(file_id):
    """Lấy metadata (tên file, kích thước, ...) theo id."""
    return client.beta.files.retrieve_metadata(file_id)


def download_file(file_id, filename=None):
    """Tải file (vd: biểu đồ Claude tạo ra) về máy.

    Không truyền filename -> lấy tên gốc từ metadata.
    """
    content = client.beta.files.download(file_id)
    if not filename:
        filename = get_metadata(file_id).filename
    content.write_to_file(filename)
    print(f"   -> Đã tải về: {filename}")


# =====================================================================
# HELPER — duyệt & in các block trả về (nhiều LOẠI block khác nhau)
# =====================================================================
def show_response(message):
    """In gọn từng block trong response để HIỂU Claude đã làm gì.

    Các loại block hay gặp khi dùng code execution:
      - text:                       lời giải thích / kết luận cho người dùng.
      - server_tool_use:            Claude YÊU CẦU chạy 1 đoạn code (input là code Python).
      - code_execution_tool_result: KẾT QUẢ chạy code (stdout, lỗi, và file output nếu có).
    """
    for block in message.content:
        btype = block.type
        if btype == "text":
            print("\n[TEXT]")
            print("  ", block.text[:500])
        elif btype == "server_tool_use":
            print("\n[SERVER_TOOL_USE] Claude muốn chạy code:")
            code = getattr(block, "input", {}) or {}
            # input thường chứa key 'code' là đoạn Python Claude tự viết
            snippet = code.get("code", "") if isinstance(code, dict) else str(code)
            print("  ", snippet[:500])
        elif btype == "code_execution_tool_result":
            print("\n[CODE_EXECUTION_TOOL_RESULT] Kết quả chạy:")
            print("  ", str(getattr(block, "content", ""))[:500])
        else:
            print(f"\n[{btype.upper()}] (block loại khác)")


# =====================================================================
# LUỒNG CHÍNH — phân tích churn từ streaming.csv, xuất biểu đồ
# =====================================================================
print("=" * 68)
print("BƯỚC 1 — Upload streaming.csv lên Files API")
print("=" * 68)
file_meta = upload(CSV_PATH)
print(f"   file_id = {file_meta.id}")
print(f"   tên     = {getattr(file_meta, 'filename', '(không rõ)')}")


print("\n" + "=" * 68)
print("BƯỚC 2 — Yêu cầu Claude phân tích churn + tạo biểu đồ (tự viết & chạy code)")
print("=" * 68)

# ⚠️ LƯU Ý QUAN TRỌNG (nhắc trong prompt):
#    Mỗi lần Claude chạy code là 1 "phiên sạch" (clean slate) — KHÔNG giữ biến/import
#    từ lần chạy trước. Vì vậy phải import lại thư viện & đọc lại file mỗi lần.
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": (
                    "Hãy phân tích chi tiết để tìm các YẾU TỐ CHÍNH gây churn "
                    "(khách rời bỏ dịch vụ) trong file dữ liệu đính kèm. "
                    "Cột 'Churned' = 1 nghĩa là đã rời bỏ, = 0 là ở lại. "
                    "Kết quả cuối cùng cần có ÍT NHẤT 1 biểu đồ tóm tắt phát hiện. "
                    "Lưu ý: mỗi lần chạy code là phiên sạch, hãy import lại thư viện "
                    "và đọc lại file mỗi lần chạy."
                ),
            },
            # ⭐ Gắn file đã upload vào hội thoại bằng container_upload
            {"type": "container_upload", "file_id": file_meta.id},
        ],
    }
]

response = client.messages.create(
    model=model,
    max_tokens=4096,
    messages=messages,
    # ⭐ Bật tool code_execution -> Claude tự viết & chạy Python trong sandbox
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

show_response(response)


print("\n" + "=" * 68)
print("BƯỚC 3 (TUỲ CHỌN) — Tải biểu đồ Claude tạo ra về máy")
print("=" * 68)
print("""\
# Claude thường tạo file output (vd biểu đồ .png) trong sandbox. file_id của output
# nằm trong block 'code_execution_tool_result' của response. Sau khi lấy được id đó,
# tải về bằng:
#
#     download_file("file_xxxxxxxxxxxxxxxx")     # id lấy từ response ở BƯỚC 2
#
# (Để trống ở đây vì file này để ĐỌC HIỂU — chưa chạy. Khi chạy thật, copy id vào.)
""")


# =====================================================================
# GHI CHÚ (chỉ để đọc)
# =====================================================================
print("=" * 68)
print("GHI CHÚ")
print("=" * 68)
print("""\
- container_upload: cách "đưa file cho Claude" mà KHÔNG dán nội dung file vào prompt
  -> tiết kiệm token, và Claude đọc file trực tiếp trong sandbox.
- code_execution là SERVER-SIDE tool: bạn KHÔNG cần tự thực thi, API tự chạy vòng lặp code.
- "Clean slate": mỗi lần chạy code không giữ trạng thái -> luôn import & đọc file lại.
- Dọn dẹp: dùng list_files() để xem, delete_file(id) để xoá file đã upload khi không cần.
- Kết hợp với bài 20 (caching): nếu system prompt/định nghĩa tool dài & lặp lại,
  có thể cache để giảm chi phí input cho các request phân tích liên tiếp.
""")
print("--- Xong. Đây là bản .py để đọc hiểu; chạy khi bạn đã sẵn sàng. ---")
