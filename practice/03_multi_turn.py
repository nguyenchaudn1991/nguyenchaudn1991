# Bài thực hành 3 — Hội thoại nhiều lượt (multi-turn)
# Chạy:  python practice/03_multi_turn.py
# Mục tiêu: thấy Claude STATELESS, và cách tự giữ lịch sử để nó "nhớ" ngữ cảnh.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"


# --- 3 helper functions (đúng như bài học) ---
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text


# ========== ❌ CÁCH SAI: không gửi lịch sử ==========
# Hỏi follow-up trong một request MỚI, không kèm ngữ cảnh -> Claude ngơ ngác.
print("========== ❌ KHÔNG có lịch sử ==========")
broken = []
add_user_message(broken, "Write another sentence")   # "thêm câu" về cái gì??
print(chat(broken))


# ========== ✅ CÁCH ĐÚNG: tự giữ & gửi toàn bộ lịch sử ==========
print("\n========== ✅ CÓ lịch sử (multi-turn) ==========")
messages = []                                                  # sổ rỗng

add_user_message(messages, "Define quantum computing in one sentence")
answer = chat(messages)                                        # lượt 1
print("Lượt 1 (user):  Define quantum computing in one sentence")
print("Claude:        ", answer)

add_assistant_message(messages, answer)                        # ghi câu trả lời vào sổ (bước hay quên!)
add_user_message(messages, "Write another sentence")           # follow-up
final_answer = chat(messages)                                  # lượt 2 — CÓ ngữ cảnh
print("\nLượt 2 (user):  Write another sentence")
print("Claude:        ", final_answer)

print(f"\n--- Sổ 'messages' giờ có {len(messages)} dòng (user/assistant xen kẽ) ---")
for m in messages:
    print(f"  [{m['role']}] {m['content'][:60]}...")
