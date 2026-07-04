# Bài thực hành 6 — Temperature
# Chạy:  python practice/06_temperature.py
# Mục tiêu: THẤY TẬN MẮT khác biệt giữa
#   - temperature = 0.0  -> deterministic  -> 3 lần gần như Y HỆT nhau
#   - temperature = 1.0  -> random/creative -> 3 lần mỗi lần một KHÁC

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"  # Haiku cho rẻ — bài này gọi API 6 lần


# --- helpers (thêm temperature so với bài trước) ---
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system=None, temperature=1.0):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,   # <-- núm mới của bài này
    }
    if system:                        # API không nhận system=None -> thêm có điều kiện
        params["system"] = system
    message = client.messages.create(**params)
    return message.content[0].text


def generate_idea(temperature):
    # messages MỚI mỗi lần -> biến số duy nhất giữa các lần là temperature
    messages = []
    add_user_message(
        messages,
        "Cho a ý tưởng visualize agent làm việc trong claude code/ cli. Ngắn gọn 1 dòng",
    )
    return chat(messages, temperature=temperature)


print("=" * 64)
print("TEMPERATURE = 0.0  (deterministic -> kỳ vọng: 3 lần gần như y hệt)")
print("=" * 64)
for i in range(1, 4):
    print(f"\n[Lần {i}] {generate_idea(0.0)}")

print("\n" + "=" * 64)
print("TEMPERATURE = 1.0  (random -> kỳ vọng: 3 lần mỗi lần một khác)")
print("=" * 64)
for i in range(1, 4):
    print(f"\n[Lần {i}] {generate_idea(1.0)}")

print("\n--- Xong. Quan sát: khối 0.0 lặp lại? khối 1.0 đa dạng? ---")
