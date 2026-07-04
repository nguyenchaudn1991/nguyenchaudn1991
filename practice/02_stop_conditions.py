# Bài thực hành 2 — 3 điều kiện dừng (stop conditions)
# Chạy:  python practice/02_stop_conditions.py
# Mục tiêu: thấy stop_reason đổi giá trị theo từng tình huống.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows (tránh lỗi cp1252)

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"


def show(title, message):
    """In gọn text + lý do dừng để đối chiếu."""
    text = message.content[0].text if message.content else "(rỗng)"
    print(f"\n========== {title} ==========")
    print("TEXT       :", repr(text))               # repr() để thấy rõ chỗ bị cắt
    print("stop_reason:", message.stop_reason)       # ← thứ cần quan sát
    print("stop_seq   :", message.stop_sequence)     # cụm dừng đã trúng (nếu có)
    print("output_tok :", message.usage.output_tokens)


# ① end_turn — Claude tự thấy đủ và dừng (trần đủ rộng)
m1 = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[{"role": "user", "content": "Say hello in exactly one short sentence."}],
)
show("① end_turn (tự nhiên)", m1)

# ② max_tokens — ANH chặn độ dài; output bị cắt giữa chừng
m2 = client.messages.create(
    model=model,
    max_tokens=10,
    messages=[{"role": "user", "content": "Explain quantum computing in detail."}],
)
show("② max_tokens (chạm trần)", m2)

# ③ stop_sequence — ANH đặt cụm cấm vượt; gặp "5" là dừng phắt
m3 = client.messages.create(
    model=model,
    max_tokens=1000,
    stop_sequences=["5"],                            # ← định nghĩa cụm dừng
    messages=[{"role": "user", "content": "Count from 1 to 10, separated by commas."}],
)
show("③ stop_sequence (gặp cụm dừng)", m3)

print("\n--- Tóm tắt: ai cầm phanh? ---")
print("① end_turn     -> Claude tự phanh (nói xong)")
print("② max_tokens   -> ANH phanh (giới hạn độ dài)")
print("③ stop_sequence-> ANH phanh (cụm cấm vượt)")
