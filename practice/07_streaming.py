# Bài thực hành 7 — Response Streaming
# Chạy:  python practice/07_streaming.py
# Mục tiêu: thấy tận mắt 3 tầng streaming đã học:
#   DEMO 1: stream=True  -> in RA TỪNG EVENT (thấy MessageStart...Delta...Stop)
#   DEMO 2: client.messages.stream() + text_stream -> hiệu ứng gõ chữ realtime
#   DEMO 3: get_final_message() -> ráp lại message đầy đủ (text + usage + stop_reason)

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


# =====================================================================
# DEMO 1 — RAW: stream=True, in ra TỪNG event để thấy luồng
# =====================================================================
print("=" * 64)
print("DEMO 1 — RAW EVENTS (stream=True)")
print("Quan sát thứ tự: message_start -> content_block_start ->")
print("content_block_delta (nhiều) -> content_block_stop -> message_delta -> message_stop")
print("=" * 64)

messages = []
add_user_message(messages, "Write a 1 sentence description of a fake database.")

stream = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    stream=True,
)

for event in stream:
    if event.type == "message_start":
        # input_tokens biết NGAY TỪ ĐẦU
        print(f"[message_start]  input_tokens={event.message.usage.input_tokens}")
    elif event.type == "content_block_delta":
        # text thật nằm ở đây (rất nhiều event loại này)
        print(f"[content_block_delta]  -> text: {event.delta.text!r}")
    elif event.type == "message_delta":
        # "chốt sổ": stop_reason + output_tokens chỉ biết Ở CUỐI
        print(f"[message_delta]  stop_reason={event.delta.stop_reason}  "
              f"output_tokens={event.usage.output_tokens}")
    else:
        print(f"[{event.type}]")


# =====================================================================
# DEMO 2 — GỌN: text_stream, hiệu ứng gõ chữ realtime
# =====================================================================
print("\n" + "=" * 64)
print("DEMO 2 — TEXT STREAM (client.messages.stream + text_stream)")
print("Chữ phải HIỆN DẦN, không đợi xong cả câu:")
print("=" * 64)

messages = []
add_user_message(messages, "Cho 1 câu mô tả ngắn về một thành phố tưởng tượng.")

with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)   # end="" để nối liền; flush để hiện ngay
    print()  # xuống dòng sau khi xong


# =====================================================================
# DEMO 3 — RÁP LẠI: get_final_message()
# =====================================================================
print("\n" + "=" * 64)
print("DEMO 3 — FINAL MESSAGE (get_final_message)")
print("Vừa stream cho user, vừa có message đầy đủ để lưu/nối lịch sử:")
print("=" * 64)

messages = []
add_user_message(messages, "Một câu slogan cho quán cà phê AI.")

with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final_message = stream.get_final_message()

print("\n\n--- final_message (object đầy đủ) ---")
print("text       :", final_message.content[0].text)
print("stop_reason:", final_message.stop_reason)
print("usage      :", final_message.usage)
