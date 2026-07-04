# Bài thực hành 10 — Eval pipeline CHẠY TỪNG BƯỚC (bản .py dễ theo dõi)
# Chạy:  python practice/10_eval_step_by_step.py
#
# Vì sao có file này: notebook giấu hết xử lý trong vòng lặp run_eval() (còn
# chạy đa luồng) -> chỉ thấy điểm trung bình ở cuối. File này LÀM CHẬM LẠI,
# TUẦN TỰ, in rõ từng bước cho từng ca để THẤY tận mắt pipeline làm gì.
#
# Ví dụ dùng đúng ngành của anh (CSKH / bán hàng), tiếng Việt cho dễ hiểu:
#   - Ca 1: trích số tiền VND -> JSON
#   - Ca 2: phân loại cảm xúc review -> JSON
# Vẫn đủ 2 grader: model grader (chấm nội dung 1-10) + code grader (JSON hợp lệ?).

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

import json
import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
model = "claude-haiku-4-5"


# ===== Helpers =====
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if system:
        params["system"] = system
    return client.messages.create(**params).content[0].text


# ===== Parse JSON AN TOÀN (bài học production: LLM hay trả JSON hơi lỗi) =====
def parse_json_loose(text):
    text = text.strip()
    try:
        return json.loads(text)                       # thử bình thường
    except json.JSONDecodeError:
        # vá các dấu '\' không hợp lệ (vd \- \d) thành '\\' rồi thử lại
        repaired = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            return None                                # chịu thua -> trả None


# ===== Dataset gắn cứng — tiếng Việt, ngành CSKH/bán hàng =====
DATASET = [
    {
        "task": "Trích số tiền VND từ câu của khách: 'chuyển giúp em 2 triệu 5 nhé'. "
                "Trả JSON đúng dạng {\"so_tien\": <số nguyên, đơn vị đồng>}",
        "format": "json",
        "solution_criteria": "so_tien = 2500000; JSON hợp lệ; không chữ thừa",
    },
    {
        "task": "Phân loại cảm xúc review của khách: 'Áo đẹp, giao nhanh, shop tư vấn dễ thương'. "
                "Trả JSON đúng dạng {\"cam_xuc\": \"tích cực\" | \"tiêu cực\" | \"trung tính\"}",
        "format": "json",
        "solution_criteria": "cam_xuc = tích cực; JSON hợp lệ",
    },
]


# ===== BƯỚC 3 · chạy prompt đang được đánh giá =====
def run_prompt(test_case):
    prompt = f"""
Nhiệm vụ: {test_case["task"]}

* CHỈ trả về JSON đúng yêu cầu
* KHÔNG giải thích, KHÔNG thêm chữ nào ngoài JSON
"""
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")          # prefill mở code block JSON
    return chat(messages, stop_sequences=["```"], temperature=0.0)


# ===== BƯỚC 4a · Model grader (một AI khác chấm nội dung) =====
def grade_by_model(test_case, output):
    eval_prompt = f"""
Bạn là giám khảo chấm lời giải do AI tạo ra. Chấm KHÁCH QUAN theo tiêu chí.

Nhiệm vụ gốc:
<task>{test_case["task"]}</task>

Lời giải cần chấm:
<solution>{output}</solution>

Tiêu chí đánh giá:
<criteria>{test_case["solution_criteria"]}</criteria>

Trả về JSON đúng thứ tự các field:
- "strengths": mảng 1-3 điểm mạnh
- "weaknesses": mảng 1-3 điểm cần cải thiện
- "reasoning": giải thích ngắn gọn (tiếng Việt)
- "score": số nguyên 1-10
Chỉ trả JSON, ngắn gọn.
"""
    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"], temperature=0.0)  # giám khảo ổn định

    data = parse_json_loose(eval_text)
    if data is None:                                    # grader trả JSON hỏng -> không crash
        return {
            "strengths": [],
            "weaknesses": ["(không parse được JSON từ grader)"],
            "reasoning": "Grader trả JSON lỗi. Raw: " + eval_text.strip()[:200],
            "score": 0,
        }
    return data


# ===== BƯỚC 4b · Code grader (kiểm JSON hợp lệ, trả 10/0) =====
def validate_json(text):
    try:
        json.loads(text.strip()); return 10
    except json.JSONDecodeError:
        return 0


def grade_syntax(output, test_case):
    if test_case["format"] == "json":
        return validate_json(output)
    return 10  # các format khác bỏ qua trong demo này


# ===== Chạy 1 ca, IN RÕ TỪNG BƯỚC =====
def run_test_case(i, total, test_case):
    print("\n" + "=" * 70)
    print(f"CASE {i}/{total}")
    print("=" * 70)
    print(f"NHIỆM VỤ : {test_case['task']}")
    print(f"FORMAT   : {test_case['format']}")
    print(f"TIÊU CHÍ : {test_case['solution_criteria']}")

    print("\n--- BƯỚC 3 · Gửi prompt cho Claude (run_prompt) → nhận output ---")
    output = run_prompt(test_case)
    print(output.strip())

    print("\n--- BƯỚC 4a · Model grader chấm nội dung (grade_by_model) ---")
    g = grade_by_model(test_case, output)
    print(f"strengths : {g['strengths']}")
    print(f"weaknesses: {g['weaknesses']}")
    print(f"reasoning : {g['reasoning']}")
    print(f"==> model_score = {g['score']}")

    print("\n--- BƯỚC 4b · Code grader chấm JSON hợp lệ (grade_syntax) ---")
    syntax = grade_syntax(output, test_case)
    ok = "JSON hợp lệ → 10" if syntax == 10 else "JSON LỖI → 0"
    print(f"==> syntax_score = {syntax}  ({ok})")

    print("\n--- BƯỚC 5 · Trộn điểm: (model + syntax) / 2 ---")
    score = (g["score"] + syntax) / 2
    print(f"==> ({g['score']} + {syntax}) / 2 = {score}")

    return {"score": score}


# ===== Vòng lặp toàn dataset (TUẦN TỰ) =====
if __name__ == "__main__":
    results = []
    total = len(DATASET)
    for idx, tc in enumerate(DATASET, 1):
        results.append(run_test_case(idx, total, tc))

    avg = sum(r["score"] for r in results) / len(results)
    print("\n" + "#" * 70)
    print(f"# ĐIỂM TRUNG BÌNH = {avg:.2f} / 10   ({total} ca)")
    print("#" * 70)
    print("\nMỗi ca tốn 2 lời gọi API (1 run_prompt + 1 grade_by_model).")
    print("Đổi MỘT thứ trong run_prompt → chạy lại → so điểm. Đó là vòng iterate.")
