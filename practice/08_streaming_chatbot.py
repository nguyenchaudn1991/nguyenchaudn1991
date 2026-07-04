# Bài thực hành 8 — Streaming Chatbot (gộp bài 04 + bài 07)
# Chạy:  python practice/08_streaming_chatbot.py
# Mục tiêu: chatbot terminal NHỚ ngữ cảnh + chữ HIỆN DẦN realtime.
#
# Điểm mấu chốt: vẫn stream cho user xem, NHƯNG dùng get_final_message()
# để lấy text ĐẦY ĐỦ rồi add_assistant_message -> không vỡ multi-turn.

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


def stream_chat(messages, system=None, temperature=1.0):
    """Stream chữ ra terminal realtime, đồng thời trả về message ĐẦY ĐỦ."""
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system

    with client.messages.stream(**params) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)   # (A) user thấy chữ hiện dần
        print()                                # xuống dòng khi xong
        return stream.get_final_message()      # (B) message đầy đủ để lưu/nối sổ


# ========== Vòng lặp chatbot ==========
print("🤖 Streaming chatbot sẵn sàng. Gõ 'quit' hoặc 'exit' để thoát.\n")

# (tuỳ chọn) đặt vai cho bot — đổi/bỏ tuỳ thích
system_prompt = "Bạn là trợ lý thân thiện, trả lời ngắn gọn bằng tiếng Việt."

messages = []   # sổ lịch sử — NGOÀI loop để bot nhớ

while True:
    user_input = input("Bạn: ")
    if user_input.strip().lower() in ("quit", "exit"):
        print("👋 Tạm biệt!")
        break

    add_user_message(messages, user_input)

    print("Claude: ", end="", flush=True)
    final_message = stream_chat(messages, system=system_prompt)   # stream realtime

    # ⭐ mấu chốt: ghi text ĐẦY ĐỦ vào sổ -> lượt sau Claude vẫn nhớ
    add_assistant_message(messages, final_message.content[0].text)

    # (xem cho biết) tốn bao nhiêu token lượt này
    u = final_message.usage
    print(f"   [usage: in={u.input_tokens} out={u.output_tokens} | stop={final_message.stop_reason}]\n")
