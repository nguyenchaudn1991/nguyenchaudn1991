# Bài thực hành 4 — Chat Bot Exercise
# Chạy:  python practice/04_chatbot.py
# Mục tiêu: ghép input() + while True quanh 3 helper của bài 3
#           -> chatbot chạy LIÊN TỤC trong terminal và NHỚ được ngữ cảnh.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"


# --- 3 helper functions (y hệt bài 3) ---
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


# ========== Vòng lặp chatbot ==========
# QUAN TRỌNG: 'messages' nằm NGOÀI vòng lặp -> lớn dần qua mỗi lượt
# -> mỗi lần chat() gửi TOÀN BỘ lịch sử lên API -> bot "nhớ" được.
print("🤖 Chatbot sẵn sàng. Gõ 'quit' hoặc 'exit' để thoát.\n")

messages = []  # sổ lịch sử rỗng, khai báo MỘT LẦN ở đây

while True:
    # Bước 1: nhận input từ người dùng (gõ thẳng trong terminal)
    user_input = input("Bạn: ")

    # Đường thoát (slide ghi "repeat" vô tận, nhưng nên có cách dừng)
    if user_input.strip().lower() in ("quit", "exit"):
        print("👋 Tạm biệt!")
        break

    # Bước 2: thêm câu của user vào sổ
    add_user_message(messages, user_input)

    # Bước 3: gọi API (gửi cả lịch sử)
    answer = chat(messages)

    # Bước 4: ghi câu trả lời của Claude vào sổ (bước hay quên!)
    add_assistant_message(messages, answer)

    # Bước 5: in câu trả lời
    print("Claude:", answer, "\n")

    # Bước 6: while True tự quay lại Bước 1
