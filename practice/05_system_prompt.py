# Bài thực hành 5 — System Prompt
# Chạy:  python practice/05_system_prompt.py
# Mục tiêu: thấy system prompt đổi CÁCH Claude trả lời (vai trò/phong cách),
#           CHỨ KHÔNG đổi nội dung; và cách viết chat() linh hoạt nhận system.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"


# --- helpers ---
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system=None):
    params = {"model": model, "max_tokens": 1000, "messages": messages}
    if system:                       # API KHÔNG nhận system=None -> chỉ thêm khi có
        params["system"] = system
    message = client.messages.create(**params)
    return message.content[0].text


# System prompt: gán vai "gia sư Toán" + luật hành xử (điều khiển CÁCH trả lời)
TUTOR_SYSTEM = """
Bạn là một gia sư Toán kiên nhẫn.
Tuyệt đối KHÔNG trả lời thẳng đáp án.
Hãy đặt câu hỏi gợi mở và dẫn dắt học sinh từng bước để tự tìm ra lời giải.
"""

QUESTION = "Giải 5x + 2 = 3 để tìm x"


# ========== So sánh: cùng câu hỏi, khác system prompt ==========
print("========== ❌ KHÔNG system prompt (trả lời thẳng) ==========")
m1 = []
add_user_message(m1, QUESTION)
print(chat(m1))

print("\n========== ✅ CÓ system prompt (gia sư dẫn dắt) ==========")
m2 = []
add_user_message(m2, QUESTION)
print(chat(m2, system=TUTOR_SYSTEM))   # truyền system qua tham số riêng


# ========== Chatbot gia sư (tương tác) ==========
print("\n========== 🧮 Chatbot Gia sư Toán (gõ 'quit' để thoát) ==========")
messages = []                 # sổ lịch sử, khai báo MỘT LẦN ngoài vòng lặp
# Lưu ý: KHÔNG append system vào messages. Nó đi đường system= riêng mỗi lượt.
while True:
    user_input = input("\nHọc sinh: ")
    if user_input.strip().lower() in ("quit", "exit"):
        print("👋 Tạm biệt!")
        break
    add_user_message(messages, user_input)
    answer = chat(messages, system=TUTOR_SYSTEM)   # vai bot cố định -> truyền lại mỗi lượt
    add_assistant_message(messages, answer)
    print("Gia sư:", answer)
