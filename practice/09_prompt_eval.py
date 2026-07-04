# Bài thực hành 9 — Prompt Evaluation (evaluation pipeline tối giản)
# Chạy:  python practice/09_prompt_eval.py
# Mục tiêu: THẤY TẬN MẮT cách "chấm điểm" prompt thay vì test bằng cảm tính.
#   Pipeline 4 mảnh:  Dataset -> Run -> Grade -> Score & Iterate
#   - PHẦN A: code-based grader (extraction)  -> so khớp tuyệt đối, rẻ, tất định
#   - PHẦN B: LLM-as-judge (task mở)          -> một model chấm 1-5 theo rubric
#
# Móc nối bài trước:
#   - temperature=0 cho task cần kiểm chứng (bài 6) -> eval mới đáng tin
#   - giám khảo ép JSON bằng output_config/structured outputs (thay cho
#     prefill + stop_sequences ở bài structured data, vì model mới chặn prefill)

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt trên Windows

import json
import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# 2 model khác VAI (id tiến hoá theo thời gian — tra id hiện hành khi chạy):
TASK_MODEL = "claude-haiku-4-5"      # model ĐANG BỊ CHẤM (rẻ/nhanh, eval gọi nhiều lần)
JUDGE_MODEL = "claude-sonnet-4-6"    # GIÁM KHẢO (mạnh >= task model)
# Muốn judge mạnh hơn -> đổi sang "claude-opus-4-8" NHƯNG phải BỎ temperature
# trong judge() (các model mới nhất không nhận temperature -> lỗi 400).


# ===== KHUNG CHUNG: chạy 1 dataset qua run_fn rồi chấm bằng grade_fn =====
# grade_fn trả về (score_0_đến_1, ghi_chú)
def evaluate(title, dataset, run_fn, grade_fn, pass_threshold):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)
    scores = []
    for i, case in enumerate(dataset, 1):
        out = run_fn(case["input"])           # Mảnh 2: gọi Claude
        score, note = grade_fn(case, out)     # Mảnh 3: chấm điểm
        scores.append(score)
        flag = "PASS" if score >= pass_threshold else "FAIL"
        print(f"\n[{i}] {flag}  score={score:.2f}  in={case['input']!r}")
        print(f"     out= {out!r}")
        print(f"     {note}")
    avg = sum(scores) / len(scores)
    pr = sum(1 for s in scores if s >= pass_threshold) / len(scores)
    print(f"\n--> TRUNG BÌNH = {avg:.2f}   PASS RATE = {pr:.0%}")   # Mảnh 4
    return avg


# ========== PHẦN A — EXTRACTION + CODE-BASED GRADER ==========
EXTRACT_SYSTEM = (
    "Bạn trích số tiền VND từ câu của khách. Trả về DUY NHẤT con số nguyên "
    "(đồng), không chữ, không dấu phẩy. 1 triệu=1000000, 500k=500000, "
    "1tr5=1500000. Nếu câu KHÔNG có số tiền, trả về đúng chữ: null"
)


def run_extractor(text):
    msg = client.messages.create(
        model=TASK_MODEL,
        max_tokens=30,
        temperature=0,                 # task cần kiểm chứng -> temp 0 (bài 6)
        system=EXTRACT_SYSTEM,
        messages=[{"role": "user", "content": text or "(trống)"}],
    )
    return msg.content[0].text.strip()


def parse_amount(t):
    t = t.strip().lower()
    if t == "" or "null" in t:
        return None
    d = re.sub(r"[^\d-]", "", t)
    return int(d) if d not in ("", "-") else None


def grade_amount(case, out):
    got, exp = parse_amount(out), case["expected"]
    return (1.0 if got == exp else 0.0), f"parsed={got}  expected={exp}"


AMOUNT_DATASET = [
    {"input": "Chuyển giúp anh 2 triệu nhé",    "expected": 2000000},
    {"input": "cho mình rút 500k",              "expected": 500000},
    {"input": "thanh toán 1tr5 dùm",            "expected": 1500000},
    {"input": "",                               "expected": None},      # rỗng
    {"input": "shop ơi áo này đẹp quá",         "expected": None},      # không có tiền
    {"input": "hoàn lại âm 200 ngàn cho khách", "expected": -200000},   # ca khó
]


# ========== PHẦN B — OPEN-ENDED + LLM-AS-JUDGE ==========
REMINDER_SYSTEM = (
    "Bạn là CSKH. Nhận một tình huống, viết DUY NHẤT MỘT câu tiếng Việt nhắc "
    "khách thanh toán: lịch sự, thân thiện, không gắt, không dài dòng."
)


def run_reminder(sit):
    msg = client.messages.create(
        model=TASK_MODEL,
        max_tokens=120,
        temperature=0.7,               # task sáng tạo -> temp cao hơn (tương phản Phần A)
        system=REMINDER_SYSTEM,
        messages=[{"role": "user", "content": sit or "(trống)"}],
    )
    return msg.content[0].text.strip()


# Giám khảo phải trả ĐIỂM máy đọc được -> ép JSON bằng STRUCTURED OUTPUTS.
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string"},   # lý do TRƯỚC
        "score": {"type": "integer"},      # điểm SAU (1..5, ràng buộc bằng prompt)
    },
    "required": ["reasoning", "score"],
    "additionalProperties": False,
}

JUDGE_TEMPLATE = """Bạn là giám khảo chấm tin nhắn CSKH. Chấm KHÁCH QUAN theo rubric.

[Tình huống] {input}
[Tiêu chí ĐẠT] {reference}
Luôn yêu cầu thêm: đúng MỘT câu, tiếng Việt, lịch sự, KHÔNG bịa số tiền không có.
[Tin nhắn cần chấm] {output}

Cho điểm 1-5 (5 = đạt mọi tiêu chí). Giải thích NGẮN trước, rồi mới cho điểm."""


def judge(case, out):
    prompt = JUDGE_TEMPLATE.format(
        input=case["input"] or "(trống)",
        reference=case["reference"],
        output=out,
    )
    msg = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=400,
        temperature=0,                 # giám khảo phải ổn định -> temp 0
        output_config={"format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
        messages=[{"role": "user", "content": prompt}],
    )
    data = json.loads(msg.content[0].text)   # schema bảo đảm JSON hợp lệ
    return data["score"], data["reasoning"]


def grade_reminder(case, out):
    raw, reason = judge(case, out)
    return raw / 5.0, f"judge={raw}/5 — {reason}"


REMINDER_DATASET = [
    {"input": "Khách mua áo 350k, đã 3 ngày chưa chuyển khoản.",
     "reference": "Nhắc chuyển 350k, nhẹ nhàng, không trách móc."},
    {"input": "Khách hẹn thanh toán hôm nay nhưng chưa thấy.",
     "reference": "Nhắc khéo theo lời hẹn hôm nay, giữ thiện cảm."},
    {"input": "",
     "reference": "Thiếu thông tin -> hỏi lại lịch sự, TUYỆT ĐỐI không bịa số tiền."},
]


if __name__ == "__main__":
    evaluate("PHẦN A · EXTRACTION (code-based grader)", AMOUNT_DATASET,
             run_extractor, grade_amount, pass_threshold=1.0)
    evaluate("PHẦN B · REMINDER (LLM-as-judge)", REMINDER_DATASET,
             run_reminder, grade_reminder, pass_threshold=0.8)

    print("\n--- Xong. Vòng iterate: xem ca FAIL -> sửa prompt (vd thêm ví dụ")
    print("    '1tr5=1500000' vào EXTRACT_SYSTEM) -> chạy lại -> so điểm mới vs cũ. ---")
    print("--- LLM-judge là THƯỚC cần nghiệm thu: nên cho người chấm ~10-20 ca")
    print("    rồi so với điểm judge (calibrate) trước khi tin cho production. ---")
