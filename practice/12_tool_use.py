# Bài thực hành 12 — TOOL USE (form chuẩn giáo trình: tách hàm)
# Chạy:  python practice/12_tool_use.py
# Cấu trúc 3 tầng đúng như khoá dạy:
#   run_conversation  -> VÒNG LẶP (gọi Claude, xem stop_reason, lặp)
#   run_tools(message)-> GOM: lọc tool_use block, chạy từng cái, bắt lỗi, trả LIST tool_result
#   run_tool(name,in) -> ROUTER: "tool này chạy hàm nào" (ở đây dùng dict TOOL_FUNCTIONS)
# Quan sát 4 kịch bản: 1 tool · 2 tool song song · lỗi is_error · chaining phụ thuộc.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

import json
from dotenv import load_dotenv
from anthropic import Anthropic

# import "kho tool" từ file bên cạnh (cùng thư mục practice/)
from exchange_tools import TOOL_SCHEMAS, TOOL_FUNCTIONS

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"


# =====================================================================
# HELPER — chat() trả FULL message; text_from_message() rút chữ khi cần
# =====================================================================
def chat(messages, tools=None):
    params = {"model": model, "max_tokens": 1000, "messages": messages}
    if tools:
        params["tools"] = tools
    return client.messages.create(**params)   # trả nguyên message (giữ cả tool_use block)


def text_from_message(message):
    # gom MỌI text block (một message có thể có nhiều), khác content[0].text
    return "\n".join(b.text for b in message.content if b.type == "text")


# =====================================================================
# ROUTER — tên tool -> hàm thật. (Khoá dùng if/elif; ở đây dùng dict cho gọn.)
# =====================================================================
def run_tool(tool_name, tool_input):
    return TOOL_FUNCTIONS[tool_name](**tool_input)   # bung dict thành keyword args


# =====================================================================
# GOM KẾT QUẢ — lọc tool_use block, chạy từng cái, trả LIST tool_result block
# =====================================================================
def run_tools(message):
    tool_requests = [b for b in message.content if b.type == "tool_use"]  # bỏ text block
    tool_result_blocks = []
    for req in tool_requests:
        print(f"   → Claude xin tool: {req.name}({req.input})")
        try:
            output = run_tool(req.name, req.input)
            block = {
                "type": "tool_result",
                "tool_use_id": req.id,               # PHẢI khớp id của tool_use block
                "content": json.dumps(output),       # serialize chuẩn (dict/số/list)
                "is_error": False,
            }
        except Exception as e:
            print(f"      ⚠️ tool lỗi: {e}")
            block = {
                "type": "tool_result",
                "tool_use_id": req.id,
                "content": f"Error: {e}",
                "is_error": True,                    # lỗi VẪN phải trả block, không Claude treo
            }
        tool_result_blocks.append(block)
    return tool_result_blocks


# =====================================================================
# AGENT LOOP — lặp tới khi Claude thôi xin tool
# =====================================================================
def run_conversation(messages):
    while True:
        response = chat(messages, tools=TOOL_SCHEMAS)   # ⭐ LUÔN kèm tools, kể cả vòng cuối

        # lưu NGUYÊN response.content (cả text lẫn tool_use block) vào lịch sử
        messages.append({"role": "assistant", "content": response.content})

        intermediate = text_from_message(response)
        if intermediate:
            print(f"   💬 Claude: {intermediate}")     # text trung gian (nếu có)

        # stop_reason quyết định: còn "tool_use" thì chạy tool; ngược lại thì xong
        if response.stop_reason != "tool_use":
            return response

        tool_results = run_tools(response)              # gom kết quả HẾT các tool
        messages.append({"role": "user", "content": tool_results})  # trả về trong 1 user message


# =====================================================================
# CHẠY THỬ 4 KỊCH BẢN
# =====================================================================
questions = [
    "1 đô la Mỹ đổi được bao nhiêu tiền Việt?",                          # 1 tool
    "So sánh giúp tôi: 100 USD ra bao nhiêu VND, và 100 USD ra bao nhiêu JPY?",  # 2 tool 1 lượt
    "1 Euro đổi được bao nhiêu VND?",                                    # EUR không có -> is_error
    "Tôi có 430.000 VND, đổi ra được bao nhiêu Yên Nhật?",               # CHAINING: rate -> convert
    "Hệ thống này hỗ trợ những đồng tiền nào?",                          # ZERO-ARG: list_supported_currencies
    "Cho tôi xem bảng tỉ giá của đồng USD.",                             # DICT trả về: rate_table -> json.dumps
]

for q in questions:
    print("\n" + "=" * 64)
    print(f"HỎI: {q}")
    print("=" * 64)
    messages = [{"role": "user", "content": q}]
    final = run_conversation(messages)
    print("ĐÁP:", text_from_message(final))
