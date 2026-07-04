# Bài thực hành 11 — EVAL THẬT: chấm chất lượng "AI reply Google review" (case MEO)
# Chạy:  python practice/11_eval_google_review_reply.py
#
# Vì sao có file này: MEO có feature lấy review Google của khách -> AI tự soạn
# reply. Đã đổi model 3 lần (4o-mini -> 4.1-mini -> 5-nano) mà KHÔNG đo -> "ổn"
# chỉ là cảm giác. File này là CÁI THƯỚC: chấm chất lượng reply bằng số, để:
#   (1) biết prompt hiện tại thật sự tốt tới đâu,
#   (2) A/B 2 model (cũ vs mới) trên cùng bộ ca -> biết đổi model là nâng hay tụt.
#
# Task "reply review" là TASK MỞ (vô số reply đúng) -> dùng MODEL GRADER
# (LLM-as-judge), KHÔNG dùng code grader. Chạy tuần tự, in rõ từng bước.

import sys
sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt/Nhật trên Windows

import json
import re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# ── 2 VAI MODEL KHÁC NHAU ──────────────────────────────────────────────
TASK_MODEL = "claude-haiku-4-5"     # MODEL ĐANG BỊ CHẤM (đóng vai feature MEO)
JUDGE_MODEL = "claude-sonnet-4-6"   # GIÁM KHẢO (mạnh >= task; khác model -> bớt thiên vị)
# ⮕ Để A/B: đổi TASK_MODEL rồi chạy lại, so điểm trung bình. Muốn cắm GPT thật
#   của MEO thì sửa hàm generate_reply() (xem khối comment trong hàm đó).


# ===== Helpers =====
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat(model, messages, system=None, temperature=1.0, stop_sequences=[], output_config=None):
    params = {
        "model": model,
        "max_tokens": 600,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if system:
        params["system"] = system
    if output_config:                      # ép JSON bằng schema (cho model mới, thay prefill)
        params["output_config"] = output_config
    return client.messages.create(**params).content[0].text


# Schema ép giám khảo trả JSON đúng cấu trúc (thay cho prefill ```json mà model
# mới chặn). reasoning đứng TRƯỚC score trong required cũng nhắc model lý luận trước.
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "strengths": {"type": "array", "items": {"type": "string"}},
        "weaknesses": {"type": "array", "items": {"type": "string"}},
        "reasoning": {"type": "string"},
        "score": {"type": "integer"},
    },
    "required": ["strengths", "weaknesses", "reasoning", "score"],
    "additionalProperties": False,
}


def parse_json_loose(text):
    """Parse JSON từ LLM an toàn (LLM hay trả JSON hơi lỗi)."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        repaired = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            return None


# ===== PROMPT ĐANG BỊ ĐÁNH GIÁ (baseline — sau này anh cải tiến chính chỗ này) =====
REPLY_SYSTEM = """\
Bạn là trợ lý CSKH, soạn câu trả lời công khai cho review Google của khách.
Yêu cầu:
- Trả lời ĐÚNG NGÔN NGỮ của review (review tiếng Nhật -> trả lời tiếng Nhật).
- Lịch sự, chân thành, đúng giọng thương hiệu; KHÔNG máy móc sáo rỗng.
- Bám đúng nội dung khách nói; nếu khách chê, ghi nhận và xin lỗi đúng điểm đó.
- TUYỆT ĐỐI không bịa thông tin/khuyến mãi/cam kết không có thật.
- Ngắn gọn 2-4 câu.
"""


# ===== BƯỚC 3 · TASK MODEL soạn reply (đây là "feature MEO") =====
def generate_reply(review_inputs):
    user_text = f"""\
Thông tin doanh nghiệp: {review_inputs["business"]}
Số sao: {review_inputs["rating"]}/5
Nội dung review của khách:
\"\"\"{review_inputs["review"]}\"\"\"

Hãy soạn câu trả lời công khai cho review trên.
"""
    messages = []
    add_user_message(messages, user_text)
    return chat(TASK_MODEL, messages, system=REPLY_SYSTEM, temperature=0.7)

    # ── MUỐN CẮM GPT THẬT CỦA MEO: thay nguyên thân hàm trên bằng đoạn dạng ──
    # from openai import OpenAI
    # oai = OpenAI()
    # res = oai.chat.completions.create(
    #     model="gpt-5-nano",
    #     messages=[{"role":"system","content":REPLY_SYSTEM},
    #               {"role":"user","content":user_text}],
    # )
    # return res.choices[0].message.content
    # ⮕ Phần còn lại (grader, vòng lặp) GIỮ NGUYÊN — eval không phụ thuộc nhà cung cấp.


# ===== BƯỚC 4 · MODEL GRADER (LLM-as-judge) chấm reply =====
def grade_reply(test_case, reply):
    inp = test_case["prompt_inputs"]
    criteria = "\n".join(f"- {c}" for c in test_case["solution_criteria"])

    eval_prompt = f"""\
Bạn là giám khảo chấm CHẤT LƯỢNG câu trả lời review của một trợ lý CSKH. Chấm KHÁCH QUAN.

Review gốc của khách (số sao {inp["rating"]}/5):
<review>{inp["review"]}</review>

Câu trả lời cần chấm:
<reply>{reply}</reply>

Tiêu chí RIÊNG cho ca này:
<criteria>
{criteria}
</criteria>

Tiêu chí BẮT BUỘC (vi phạm bất kỳ -> điểm <= 3):
- Trả lời ĐÚNG ngôn ngữ của review.
- KHÔNG bịa thông tin/khuyến mãi/cam kết không có trong review.
- Bám đúng nội dung khách nói (không generic, không lạc đề).

Trả về JSON đúng thứ tự field:
- "strengths": mảng 1-3 điểm mạnh
- "weaknesses": mảng 1-3 điểm cần cải thiện
- "reasoning": giải thích ngắn (tiếng Việt)
- "score": số nguyên 1-10
Chỉ trả JSON, ngắn gọn.
"""
    messages = []
    add_user_message(messages, eval_prompt)
    # Model mới (Sonnet 4.6) CHẶN prefill -> dùng structured outputs ép JSON bằng schema.
    eval_text = chat(
        JUDGE_MODEL,
        messages,
        temperature=0.0,
        output_config={"format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
    )

    data = parse_json_loose(eval_text)
    if data is None:
        return {"strengths": [], "weaknesses": ["(grader trả JSON lỗi)"],
                "reasoning": "Raw: " + eval_text.strip()[:200], "score": 0}
    return data


# ===== GOLDEN DATASET — review thật điển hình (thay bằng review MEO sau) =====
DATASET = [
    {
        "prompt_inputs": {
            "business": "Quán cà phê Mộc, Đà Nẵng",
            "rating": 5,
            "review": "Không gian đẹp, cà phê ngon, nhân viên tên Linh tư vấn rất nhiệt tình. Sẽ quay lại!",
        },
        "solution_criteria": [
            "Cảm ơn chân thành",
            "Nhắc lại điểm khách khen (không gian/nhân viên Linh)",
            "Mời quay lại tự nhiên",
        ],
    },
    {
        "prompt_inputs": {
            "business": "Nhà hàng Hải Sản Biển Xanh",
            "rating": 2,
            "review": "Đợi món 45 phút, tôm không tươi. Thất vọng dù nhân viên thái độ ok.",
        },
        "solution_criteria": [
            "Xin lỗi đúng vấn đề (chờ lâu + tôm không tươi)",
            "Không phòng thủ/đổ lỗi",
            "Đề nghị bù đắp/khắc phục mà KHÔNG bịa khuyến mãi cụ thể",
        ],
    },
    {
        "prompt_inputs": {
            "business": "Spa An Nhiên",
            "rating": 3,
            "review": "Dịch vụ ổn nhưng giá hơi cao. Có giảm giá cho khách quen không?",
        },
        "solution_criteria": [
            "Cảm ơn + ghi nhận góp ý về giá",
            "Trả lời câu hỏi giảm giá mà KHÔNG bịa chương trình không có thật",
            "Mời liên hệ để được tư vấn cụ thể",
        ],
    },
    {
        "prompt_inputs": {
            "business": "Khách sạn Sakura Hotel",
            "rating": 5,
            "review": "とても清潔で、スタッフの対応も素晴らしかったです。また泊まりたいです。",
        },
        "solution_criteria": [
            "PHẢI trả lời bằng tiếng Nhật",
            "Lịch sự đúng văn hoá (kính ngữ)",
            "Cảm ơn + mong được đón tiếp lần sau",
        ],
    },
    {
        "prompt_inputs": {
            "business": "Tiệm bánh Ngọt Lành",
            "rating": 1,
            "review": "Đặt bánh sinh nhật mà giao trễ 2 tiếng, hỏng cả buổi tiệc của con tôi.",
        },
        "solution_criteria": [
            "Xin lỗi nghiêm túc, đồng cảm (hỏng tiệc của con)",
            "Nhận trách nhiệm giao trễ, không bao biện",
            "Mời liên hệ trực tiếp để xử lý, không bịa đền bù cụ thể",
        ],
    },
]


# ===== Chạy 1 ca, IN RÕ TỪNG BƯỚC =====
def run_test_case(i, total, test_case):
    inp = test_case["prompt_inputs"]
    print("\n" + "=" * 72)
    print(f"CASE {i}/{total}  ·  {inp['business']}  ·  {inp['rating']}/5 sao")
    print("=" * 72)
    print(f"REVIEW   : {inp['review']}")
    print(f"TIÊU CHÍ : {test_case['solution_criteria']}")

    print(f"\n--- BƯỚC 3 · {TASK_MODEL} soạn reply (generate_reply) ---")
    reply = generate_reply(inp)
    print(reply.strip())

    print(f"\n--- BƯỚC 4 · {JUDGE_MODEL} làm giám khảo chấm (grade_reply) ---")
    g = grade_reply(test_case, reply)
    print(f"strengths : {g['strengths']}")
    print(f"weaknesses: {g['weaknesses']}")
    print(f"reasoning : {g['reasoning']}")
    print(f"==> SCORE = {g['score']}/10")

    return {"score": g["score"]}


# ===== Vòng lặp toàn dataset (TUẦN TỰ) =====
if __name__ == "__main__":
    results = []
    total = len(DATASET)
    for idx, tc in enumerate(DATASET, 1):
        results.append(run_test_case(idx, total, tc))

    scores = [r["score"] for r in results]
    avg = sum(scores) / len(scores)
    passed = len([s for s in scores if s >= 7])
    print("\n" + "#" * 72)
    print(f"# TASK_MODEL = {TASK_MODEL}")
    print(f"# ĐIỂM TRUNG BÌNH = {avg:.2f}/10   ·   PASS RATE (>=7) = {passed}/{total}")
    print("#" * 72)
    print("\n>> A/B model: đổi TASK_MODEL ở đầu file -> chạy lại -> so điểm trung bình.")
    print(">> Cải tiến prompt: sửa REPLY_SYSTEM (1 thay đổi) -> chạy lại -> so điểm.")
    print(">> Trước khi tin số: cho người chấm vài ca, đối chiếu điểm judge (calibrate).")
