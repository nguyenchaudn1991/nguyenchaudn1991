"""
Agent loop demo — Claude Platform 101 (section 7)
Chạy đúng ví dụ 'get_weather' trong bài học, có thêm print ở mỗi bước
để THẤY vòng lặp agent chạy thật: stop_reason -> tool_use -> tool_result -> end_turn.

KHÔNG cần sửa gì. Chỉ cần đặt biến môi trường ANTHROPIC_API_KEY rồi chạy.
"""
import os
import sys
import anthropic

# Nạp file .env nếu có (tìm từ thư mục hiện tại đi ngược lên thư mục cha).
# anthropic.Anthropic() chỉ đọc BIẾN MÔI TRƯỜNG, không tự mở .env như bên Node.
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(usecwd=True))
except ImportError:
    pass  # chưa cài python-dotenv cũng ok, miễn là đã set biến môi trường

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("Chua thay ANTHROPIC_API_KEY. Sua 1 trong 2 cach:")
    print("  Cach 1 (.env): them dong  ANTHROPIC_API_KEY=sk-ant-...  vao file .env,")
    print("                 roi cai:   pip install python-dotenv")
    print("  Cach 2 (cmd):  set ANTHROPIC_API_KEY=sk-ant-...   roi chay lai trong CUNG cua so.")
    sys.exit(1)

client = anthropic.Anthropic()  # tự đọc ANTHROPIC_API_KEY từ môi trường / .env vừa nạp

# Bài 'chọn model': demo đơn giản -> dùng Haiku (rẻ + nhanh nhất).
# Đổi sang "claude-opus-4-8" khi tác vụ thực sự khó.
MODEL = "claude-haiku-4-5"

# --- 1) Khai báo tool = name + description + input_schema (JSON Schema) ---
# Claude ĐỌC 'description' để quyết định có gọi tool hay không.
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city to get weather for"}
            },
            "required": ["city"],
        },
    }
]

# --- 2) Hàm thật: CODE CỦA ANH chạy tool này, KHÔNG phải Claude ---
def run_tool(name, tool_input):
    if name == "get_weather":
        # Đời thật: gọi API thời tiết. Ở đây hardcode cho dễ thấy luồng.
        return f"Weather in {tool_input['city']}: 95F, sunny"
    raise ValueError(f"Unknown tool: {name}")


messages = [
    {"role": "user", "content": "What should I wear in Austin today?"}
]

turn = 0
while True:
    turn += 1
    print(f"\n================ TURN {turn}: gọi API (client.messages.create) ================")
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
    print(f"stop_reason = {response.stop_reason}")
    print(f"usage: input={response.usage.input_tokens} tokens, "
          f"output={response.usage.output_tokens} tokens   (đây là chỗ tính tiền)")

    # --- Claude XONG: in câu trả lời cuối rồi thoát vòng lặp ---
    if response.stop_reason == "end_turn":
        print("\n----- Claude XONG (end_turn) -> câu trả lời cuối -----")
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    # --- Claude XIN gọi tool: code của anh chạy rồi trả kết quả về ---
    if response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"[Claude nói]: {block.text}")
            if block.type == "tool_use":
                print(f"[Claude XIN gọi tool] name={block.name}  input={block.input}  id={block.id}")
                result = run_tool(block.name, block.input)     # <-- CODE CỦA ANH chạy
                print(f"[Code CỦA ANH trả kết quả] {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,     # ghép đúng yêu cầu tool_use
                    "content": result,
                })
        # Mỗi vòng append ĐỦ 2 message, ĐÚNG thứ tự:
        messages.append({"role": "assistant", "content": response.content})  # (1) nguyên response Claude
        messages.append({"role": "user", "content": tool_results})           # (2) tool_result, role = user
