# Bài thực hành 19 — EXTENDED THINKING ("giấy nháp" của Claude)
# Chạy:  python practice/19_extended_thinking.py
# Mục tiêu THẤY TẬN MẮT:
#   1) Cùng 1 câu hỏi: KHÔNG thinking -> response 1 text block
#                       CÓ  thinking  -> response = thinking block + text block
#   2) thinking block có 'signature' (token mã hoá chống sửa)
#   3) redacted_thinking: ép bằng magic string -> app PHẢI xử lý không crash
#   4) Ràng buộc: budget_tokens >= 1024 và max_tokens PHẢI > thinking_budget
#   5) KHÔNG tương thích: bật thinking thì không set temperature (bài minh hoạ luôn)
#
# ⚠️ Model: dùng "claude-sonnet-4-5" — ĐÚNG như notebook của khoá và là model
#    còn nhận cú pháp CŨ thinking={"type":"enabled","budget_tokens": N}.
#    Trên model mới (Opus 4.6+/Sonnet 5/Fable 5) cú pháp này trả LỖI 400 ->
#    phải dùng adaptive thinking (xem phần cuối file). Đề THI vẫn hỏi kiểu cũ.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message

load_dotenv()
client = Anthropic()
model = "claude-sonnet-4-5"  # model của khoá; nhận budget_tokens (bài này KHÔNG dùng Haiku)

# Magic string ÉP Claude trả về redacted_thinking (để test app xử lý ca này)
THINKING_TEST_STR = (
    "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_"
    "46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"
)


# =====================================================================
# HELPERS
# =====================================================================
def add_user_message(messages, message):
    # nhận cả Message object (để lưu nguyên content) lẫn string
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})


def chat(messages, system=None, temperature=1.0, thinking=False, thinking_budget=1024):
    # max_tokens PHẢI > thinking_budget -> lấy dư ra 2000 token cho câu trả lời
    params = {
        "model": model,
        "max_tokens": thinking_budget + 2000,
        "messages": messages,
    }
    if thinking:
        # ⭐ bật extended thinking = thêm cấu hình thinking
        params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
        # ⚠️ KHÔNG set temperature khi thinking (2 tính năng KHÔNG tương thích).
        #    Nếu bạn thêm temperature ở đây, API sẽ báo lỗi.
    else:
        params["temperature"] = temperature
    if system:
        params["system"] = system
    return client.messages.create(**params)


def split_blocks(message):
    # duyệt block THEO type (không theo index) — 1 message nhiều loại block
    thinking = [b for b in message.content if b.type == "thinking"]
    redacted = [b for b in message.content if b.type == "redacted_thinking"]
    text = [b for b in message.content if b.type == "text"]
    return thinking, redacted, text


def text_from_message(message):
    return "\n".join(b.text for b in message.content if b.type == "text")


def clip(s, n=280):
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[:n] + " …[cắt bớt]"


# câu hỏi cần suy luận nhiều bước -> thinking phát huy tác dụng
HARD_Q = (
    "Một cửa hàng bán combo: 3 áo + 2 quần = 1.190.000đ, và 2 áo + 3 quần = "
    "1.210.000đ. Hỏi giá 1 áo và 1 quần? Trả lời gọn kèm đáp số cuối."
)


# =====================================================================
# KỊCH BẢN 1 — KHÔNG thinking: response chỉ là 1 text block
# =====================================================================
print("=" * 68)
print("KỊCH BẢN 1 — KHÔNG bật thinking")
print("=" * 68)
messages = []
add_user_message(messages, HARD_Q)
resp = chat(messages, thinking=False, temperature=0.0)
th, red, txt = split_blocks(resp)
print(f"Số block: thinking={len(th)}  redacted={len(red)}  text={len(txt)}")
print("ĐÁP:", clip(text_from_message(resp), 400))
print(f"(output_tokens = {resp.usage.output_tokens})")


# =====================================================================
# KỊCH BẢN 2 — CÓ thinking: response = thinking block + text block
# =====================================================================
print("\n" + "=" * 68)
print("KỊCH BẢN 2 — BẬT thinking (budget_tokens=1500)")
print("=" * 68)
messages = []
add_user_message(messages, HARD_Q)
resp = chat(messages, thinking=True, thinking_budget=1500)
th, red, txt = split_blocks(resp)
print(f"Số block: thinking={len(th)}  redacted={len(red)}  text={len(txt)}")
if th:
    # phần 'giấy nháp' — đọc được, KÈM signature (token mã hoá chống sửa)
    print("\n[THINKING BLOCK] (giấy nháp Claude):")
    print("  ", clip(th[0].thinking, 400))
    has_sig = getattr(th[0], "signature", None) is not None
    print(f"   -> có signature? {has_sig}  (token mã hoá đảm bảo bạn KHÔNG sửa thinking)")
print("\n[FINAL ANSWER]:", clip(text_from_message(resp), 400))
print(f"\n(output_tokens = {resp.usage.output_tokens}  <- gồm CẢ thinking tokens -> tốn hơn KB1)")
print("Quan sát: KB2 có thêm thinking block; token nhiều hơn -> đánh đổi tiền/độ trễ lấy reasoning.")


# =====================================================================
# KỊCH BẢN 3 — REDACTED THINKING: ép bằng magic string, app không được crash
# =====================================================================
print("\n" + "=" * 68)
print("KỊCH BẢN 3 — redacted_thinking (magic string) + gửi lại giữ ngữ cảnh")
print("=" * 68)
messages = []
add_user_message(messages, THINKING_TEST_STR)  # magic string -> ép redacted
resp = chat(messages, thinking=True, thinking_budget=1500)
th, red, txt = split_blocks(resp)
print(f"Số block: thinking={len(th)}  redacted={len(red)}  text={len(txt)}")
if red:
    # redacted = nội dung suy luận bị hệ thống an toàn CỜ -> mã hoá, KHÔNG đọc được
    print("   -> Nhận redacted_thinking block: nội dung MÃ HOÁ, không đọc được (đúng như kỳ vọng).")
    print("   -> App xử lý mượt, KHÔNG crash. ✅")
print("[FINAL ANSWER]:", clip(text_from_message(resp), 300))

# ⭐ Lưu NGUYÊN message (kèm block redacted) rồi hỏi tiếp -> không mất ngữ cảnh
add_assistant_message(messages, resp)                 # giữ nguyên content (cả redacted block)
add_user_message(messages, "Tóm tắt trong 1 câu bạn vừa làm gì.")
resp2 = chat(messages, thinking=True, thinking_budget=1500)
print("HỎI TIẾP:", clip(text_from_message(resp2), 300))
print("Quan sát: phải gửi lại NGUYÊN message (kèm redacted) thì lượt sau mới còn ngữ cảnh.")


# =====================================================================
# KỊCH BẢN 4 — RÀNG BUỘC token (minh hoạ lỗi có kiểm soát)
# =====================================================================
print("\n" + "=" * 68)
print("KỊCH BẢN 4 — thử phá ràng buộc: max_tokens <= thinking_budget -> LỖI")
print("=" * 68)
try:
    # cố tình: budget 1500 nhưng max_tokens 1000 (nhỏ hơn) -> API từ chối
    client.messages.create(
        model=model,
        max_tokens=1000,
        thinking={"type": "enabled", "budget_tokens": 1500},
        messages=[{"role": "user", "content": "hi"}],
    )
    print("(Không lỗi? — kiểm tra lại phiên bản API)")
except Exception as e:
    print("Đúng như kỳ vọng, API báo lỗi:")
    print("  ", clip(str(e), 300))
print("Rút ra: budget_tokens >= 1024 VÀ max_tokens PHẢI > thinking_budget.")


# =====================================================================
# GHI CHÚ PRODUCTION 2026 — adaptive thinking (KHÔNG chạy, chỉ để đọc)
# =====================================================================
print("\n" + "=" * 68)
print("GHI CHÚ: trên model mới (Opus 4.6+/Sonnet 5/Fable 5) dùng adaptive thinking")
print("=" * 68)
print("""\
# Cú pháp CŨ (bài này, để THI):        thinking={"type":"enabled","budget_tokens": 1500}
# Cú pháp MỚI (production, model mới):  thinking={"type":"adaptive"}  + output_config={"effort":"high"}
#   -> Claude TỰ quyết cần suy nghĩ bao nhiêu; budget_tokens gửi vào model mới -> LỖI 400.
#   -> Giống hệt tình huống prefill -> structured outputs đã gặp: đề hỏi kiểu cũ, code thật dùng kiểu mới.
""")
print("--- Xong. So sánh KB1 vs KB2 (cấu trúc + token), và KB3 (redacted không crash). ---")
