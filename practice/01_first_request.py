# Bài thực hành 1 — Request đầu tiên tới Claude API
# Chạy từ thư mục gốc repo:  python practice/01_first_request.py
# (load_dotenv() đọc ./.env ở gốc — nơi chứa ANTHROPIC_API_KEY)

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in được tiếng Việt trên console Windows (tránh lỗi cp1252)

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()                  # nạp ANTHROPIC_API_KEY từ .env vào biến môi trường

client = Anthropic()           # tự đọc key từ env — KHÔNG dán key vào code
model = "claude-haiku-4-5"     # model hiện hành, rẻ nhất để luyện tập
                               # (đổi sang "claude-sonnet-4-6" hoặc "claude-opus-4-8" khi cần mạnh hơn)

message = client.messages.create(
    model=model,
    max_tokens=10,           # van an toàn, KHÔNG phải mục tiêu
    messages=[
        {"role": "user", "content": "bạn training data tới ngày bao nhiêu"}
    ],
)

# --- Đọc kết quả ---
print("TEXT:")
print(message.content[0].text)   # content là LIST block -> lấy block đầu rồi .text

print("\n--- metadata ---")
print("stop_reason:", message.stop_reason)   # vì sao dừng
print("usage      :", message.usage)         # token input/output
