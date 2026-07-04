# Bài thực hành 20 — PROMPT CACHING (cache tiền tố để tiết kiệm token)
# Chạy:  python practice/20_prompt_caching.py    (KHI NÀO BẠN MUỐN — mặc định file này để ĐỌC HIỂU)
#
# Mục tiêu THẤY TẬN MẮT:
#   1) KHÔNG cache -> mỗi request trả FULL giá input cho phần prompt lặp lại.
#   2) CÓ cache    -> lần 1 GHI cache (cache_creation_input_tokens cao, đắt hơn ~1.25x),
#                     lần 2 ĐỌC cache (cache_read_input_tokens cao, chỉ ~10% giá input).
#   3) Đọc usage để CHỨNG MINH cache có "ăn" hay không (cache_creation vs cache_read).
#   4) Ràng buộc dễ vấp với Haiku: phần cache phải ĐỦ DÀI (Haiku cần ~2048 token),
#      nếu ngắn hơn -> API LẶNG LẼ bỏ qua cache (không báo lỗi).
#
# ⚠️ CƠ CHẾ CỐT LÕI: cache khớp TIỀN TỐ chính xác từng byte.
#    - Cache toàn bộ nội dung TỪ ĐẦU prompt -> tới điểm đặt "cache_control".
#    - Đổi 1 ký tự trong phần tiền tố -> HỎNG toàn bộ cache phía sau (cache miss).
#    - Thiết kế: nội dung ỔN ĐỊNH để lên đầu, nội dung THAY ĐỔI để xuống cuối.
#    - Thứ tự Anthropic xử lý: tools -> system -> messages.
#
# 💡 Giá (mức Anthropic công bố, có thể đổi -> nên kiểm tra docs chính thức):
#    - Ghi cache (write): ~1.25x giá input thường (TTL 5 phút).
#    - Đọc cache (read):  ~0.10x (10%) giá input thường.
#    => Trả phụ phí GHI một lần, đổi lấy giảm ~90% cho mọi lần ĐỌC sau đó.
#       Chỉ LỜI khi phần tiền tố ổn định được tái dùng ĐỦ NHIỀU trong vòng TTL.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# ⭐ Dùng model HAIKU (theo yêu cầu). Haiku nhanh + rẻ, hợp để minh hoạ caching.
#    LƯU Ý: ngưỡng token tối thiểu để cache của Haiku CAO hơn Sonnet/Opus
#    (Haiku ~2048 token, Sonnet/Opus ~1024). Vì vậy phần cache bên dưới phải DÀI.
model = "claude-haiku-4-5"


# =====================================================================
# HELPERS
# =====================================================================
def chat(messages, system=None, tools=None, temperature=1.0,
         cache_system=False, cache_tools=False):
    """Gọi API, có TÙY CHỌN bật cache cho system prompt và/hoặc tools.

    - cache_system=True -> gắn 'cache_control' vào block system cuối cùng.
    - cache_tools=True  -> gắn 'cache_control' vào tool cuối cùng (cache CẢ khối tools).
    Đặt mốc cache ở PHẦN TỬ CUỐI của khối vì cache tính TỪ ĐẦU -> tới điểm mốc.
    """
    params = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages,
        "temperature": temperature,
    }

    if tools:
        if cache_tools:
            # sao chép để không sửa list gốc; gắn mốc vào tool CUỐI
            tools = [dict(t) for t in tools]
            tools[-1]["cache_control"] = {"type": "ephemeral"}
        params["tools"] = tools

    if system is not None:
        if cache_system:
            # system dạng LIST BLOCK -> mới gắn được cache_control
            params["system"] = [
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},  # ⭐ mốc cache
                }
            ]
        else:
            params["system"] = system  # dạng string thường -> KHÔNG cache

    return client.messages.create(**params)


def print_usage(tag, message):
    """In bảng usage để so sánh có/không cache.

    - input_tokens:                token input THƯỜNG (không cache).
    - cache_creation_input_tokens: token GHI vào cache (lần đầu, đắt hơn ~1.25x).
    - cache_read_input_tokens:     token ĐỌC từ cache (các lần sau, chỉ ~10% giá).
    - output_tokens:               token model sinh ra.
    """
    u = message.usage
    # một số field chỉ xuất hiện khi có cache -> dùng getattr cho an toàn
    creation = getattr(u, "cache_creation_input_tokens", 0) or 0
    read = getattr(u, "cache_read_input_tokens", 0) or 0
    print(f"[{tag}]")
    print(f"   input_tokens (thường)      = {u.input_tokens}")
    print(f"   cache_creation (GHI cache) = {creation}")
    print(f"   cache_read     (ĐỌC cache) = {read}")
    print(f"   output_tokens              = {u.output_tokens}")


def text_from_message(message):
    return "\n".join(b.text for b in message.content if b.type == "text")


# =====================================================================
# NỘI DUNG ỔN ĐỊNH, DÀI -> ứng viên cache lý tưởng
# =====================================================================
# ⚠️ Đây là "tài liệu tham chiếu" giả lập. Trong thực tế nó có thể là:
#    - system prompt dài, định nghĩa tool, few-shot examples, hoặc 1 tài liệu lớn.
# Phải ĐỦ DÀI để vượt ngưỡng cache của Haiku (~2048 token). Nếu bạn thấy
# cache_creation = 0 ở KỊCH BẢN 2 -> nội dung còn NGẮN, hãy nối thêm cho dài ra.
KB_BASE = """\
Bạn là trợ lý chăm sóc khách hàng của công ty "Runsystem VN" — một dịch vụ xem phim trực tuyến.
Hãy trả lời NGẮN GỌN, lịch sự, đúng chính sách bên dưới. Nếu câu hỏi ngoài phạm vi
tài liệu, hãy nói rõ là bạn sẽ chuyển cho nhân viên phụ trách.

# 1. CÁC GÓI DỊCH VỤ
- Gói Basic (7.99$/tháng): xem 1 thiết bị cùng lúc, độ phân giải tối đa 720p.
- Gói Standard (12.99$/tháng): xem 2 thiết bị cùng lúc, độ phân giải tối đa 1080p.
- Gói Premium (17.99$/tháng): xem 4 thiết bị cùng lúc, độ phân giải tối đa 4K, có tải offline.

# 2. CHÍNH SÁCH THANH TOÁN
- Chu kỳ thanh toán tính theo tháng, tự động gia hạn vào đúng ngày đăng ký.
- Hỗ trợ thẻ nội địa, thẻ quốc tế, và ví điện tử phổ biến tại Việt Nam.
- Nếu thanh toán thất bại, hệ thống thử lại tối đa 3 lần trong 5 ngày trước khi tạm khoá.

# 3. CHÍNH SÁCH HOÀN TIỀN
- Khách mới được dùng thử 7 ngày; huỷ trong thời gian này KHÔNG bị tính phí.
- Sau khi đã bị tính phí, công ty KHÔNG hoàn tiền cho phần thời gian chưa dùng,
  trừ trường hợp lỗi kỹ thuật kéo dài trên 24 giờ được xác nhận từ đội kỹ thuật.

# 4. NÂNG/HẠ CẤP GÓI
- Nâng cấp có hiệu lực NGAY, phần chênh lệch được tính theo tỉ lệ ngày còn lại.
- Hạ cấp có hiệu lực từ CHU KỲ KẾ TIẾP, không hoàn phần chênh lệch của chu kỳ hiện tại.

# 5. SỰ CỐ THƯỜNG GẶP
- Không phát được video: kiểm tra mạng, đăng xuất rồi đăng nhập lại, xoá cache ứng dụng.
- Bị đăng xuất liên tục: thường do vượt số thiết bị cho phép của gói đang dùng.
- Chất lượng hình thấp: phụ thuộc tốc độ mạng và giới hạn độ phân giải của gói.

# 6. QUY TẮC ỨNG XỬ
- Luôn xưng "Runsystem VN" và gọi khách bằng "Quý khách".
- Không hứa hẹn hoàn tiền nếu chưa đúng chính sách mục 3.
- Không tiết lộ thông tin nội bộ, giá vốn, hay dữ liệu người dùng khác.
"""

# Nhân bản tài liệu vài lần cho ĐỦ DÀI vượt ngưỡng cache của Haiku (mẹo minh hoạ).
# Trong thực tế bạn KHÔNG cần nhân bản — tài liệu thật đã đủ dài.
SYSTEM_PROMPT = (KB_BASE + "\n") * 6

QUESTION = "Tôi mới đăng ký hôm qua và muốn huỷ ngay, tôi có bị tính phí không?"


# =====================================================================
# KỊCH BẢN 1 — KHÔNG cache: gọi 2 lần, cả 2 lần đều trả FULL giá input
# =====================================================================
print("=" * 68)
print("KỊCH BẢN 1 — KHÔNG bật cache (baseline)")
print("=" * 68)

messages = [{"role": "user", "content": QUESTION}]

resp1 = chat(messages, system=SYSTEM_PROMPT, cache_system=False)
print_usage("Lần 1 - không cache", resp1)

resp2 = chat(messages, system=SYSTEM_PROMPT, cache_system=False)
print_usage("Lần 2 - không cache", resp2)

print("Quan sát: cả 2 lần cache_creation = cache_read = 0 -> luôn trả full giá input.")


# =====================================================================
# KỊCH BẢN 2 — CÓ cache system: lần 1 GHI cache, lần 2 ĐỌC cache
# =====================================================================
print("\n" + "=" * 68)
print("KỊCH BẢN 2 — BẬT cache cho system prompt")
print("=" * 68)

# ⚠️ 2 lần gọi phải:
#    - Cùng phần tiền tố (system) GIỐNG HỆT nhau từng byte.
#    - Gọi trong vòng TTL (mặc định 5 phút; mỗi lần ĐỌC trúng cache lại reset 5 phút).
resp3 = chat(messages, system=SYSTEM_PROMPT, cache_system=True)
print_usage("Lần 1 - GHI cache", resp3)
print("   -> Kỳ vọng: cache_creation CAO (đang ghi cache lần đầu).")

resp4 = chat(messages, system=SYSTEM_PROMPT, cache_system=True)
print_usage("Lần 2 - ĐỌC cache", resp4)
print("   -> Kỳ vọng: cache_read CAO, cache_creation = 0 (đọc lại cache -> rẻ ~10%).")

print("\nĐÁP (nội dung không đổi giữa các lần):")
print("  ", text_from_message(resp4)[:300])

print("""
Nếu cache_creation = 0 ngay từ lần 1 -> nội dung cache CÒN NGẮN so với ngưỡng Haiku (~2048 token).
   Cách xử lý: tăng số lần nhân bản SYSTEM_PROMPT, hoặc dùng tài liệu thật dài hơn.
""")


# =====================================================================
# GHI CHÚ THÊM (chỉ để đọc)
# =====================================================================
print("=" * 68)
print("GHI CHÚ")
print("=" * 68)
print("""\
- Tối đa 4 MỐC cache trong 1 request (ví dụ: 1 cho tools, 1 cho system, 1-2 cho tài liệu).
- Cache là khớp TIỀN TỐ: đặt phần ổn định lên đầu, phần biến động xuống cuối.
- TTL mặc định 5 phút; có tuỳ chọn 1 giờ (phí ghi cao hơn, ~2x).
- Muốn cache TOOLS: gọi chat(..., tools=[...], cache_tools=True) -> mốc gắn vào tool cuối.
- Đo hiệu quả bằng cache_creation_input_tokens vs cache_read_input_tokens trong response.usage.
- Cảnh báo "hỏng âm thầm": nếu cache_creation cứ TĂNG mỗi lượt còn cache_read đứng yên,
  nghĩa là bạn đang GHI lại cache liên tục mà không ĐỌC được -> kiểm tra lại tiền tố có bị đổi không.
""")
print("--- Xong. So sánh usage KỊCH BẢN 1 (full giá) vs KỊCH BẢN 2 (ghi 1 lần, đọc rẻ). ---")
