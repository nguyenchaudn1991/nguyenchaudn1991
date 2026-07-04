# Bài thực hành 15 — Semantic Search chạy thật (RAG pipeline hoàn chỉnh)
# Chạy:  python practice/15_semantic_search.py
#
# 2 phần:
#   PHẦN A — Toán cosine similarity trên ví dụ 2 chiều (KHÔNG gọi API, miễn phí).
#   PHẦN B — Pipeline THẬT: embed các section của report.md + 1 câu hỏi,
#            tính cosine similarity, xếp hạng, in ra section trúng nhất.
#            (Gọi VoyageAI: gộp còn 2 request để né giới hạn 3 RPM free.)

import math
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")


# ==========================================================================
# Hàm toán: cosine similarity giữa 2 vector (thuần Python, không cần numpy)
# ==========================================================================
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))         # tích vô hướng
    na = math.sqrt(sum(x * x for x in a))          # độ dài vector a
    nb = math.sqrt(sum(y * y for y in b))          # độ dài vector b
    return dot / (na * nb)                         # cosine của GÓC giữa a và b


# ==========================================================================
# PHẦN A — Ví dụ 2 chiều trong bài (model tưởng tượng: [mức y-khoa, mức phần-mềm])
# ==========================================================================
print("=" * 70)
print("  PHẦN A — Cosine similarity trên ví dụ 2 chiều (không gọi API)")
print("=" * 70)

# Vector đã normalize (magnitude = 1.0) như trong bài
medical = [0.944, 0.331]    # chunk y khoa (có chữ "bug")
software = [0.295, 0.955]   # chunk phần mềm (có "infection vectors")
query = [0.112, 0.993]      # câu hỏi: hỏi về phần mềm

sim_sw = cosine_similarity(query, software)
sim_med = cosine_similarity(query, medical)

print(f"Query {query}  (hỏi về software engineering)")
print(f"  ↔ Software {software} : cosine = {sim_sw:.3f}")
print(f"  ↔ Medical  {medical} : cosine = {sim_med:.3f}")
print(f"→ Software cao hơn hẳn ({sim_sw:.3f} > {sim_med:.3f}) -> CHỌN software chunk.")
print("  (Bài quote 0.983 vs 0.398 — số minh hoạ, làm tròn; điều quan trọng là")
print("   software THẮNG rõ rệt.)")
print(f"\nCosine DISTANCE = 1 - similarity:  software={1 - sim_sw:.3f} | medical={1 - sim_med:.3f}")
print("  → distance nhỏ = giống (NGƯỢC với similarity: cao = giống). Đừng lẫn 2 thang.\n")


# ==========================================================================
# PHẦN B — Pipeline THẬT trên report.md (cần VoyageAI key)
# ==========================================================================
print("=" * 70)
print("  PHẦN B — Semantic search THẬT trên report.md")
print("=" * 70)

from dotenv import load_dotenv

load_dotenv()

if not os.getenv("VOYAGE_API_KEY"):
    print("⏭  Bỏ qua phần B: chưa có VOYAGE_API_KEY (phần A ở trên đã chạy xong).")
    print("   Thêm key vào .env rồi chạy lại để xem pipeline thật.")
    sys.exit(0)

try:
    import voyageai
except ImportError:
    print("⏭  Bỏ qua phần B: chưa cài voyageai (pip install voyageai).")
    sys.exit(0)

client = voyageai.Client()
REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.md")


def chunk_by_section(document_text):
    return re.split(r"\n## ", document_text)


def _guard(call):
    try:
        return call()
    except voyageai.error.RateLimitError:
        print("\n⏳ Dính RATE LIMIT VoyageAI (free = 3 request/phút). Đợi ~60s rồi chạy lại.")
        sys.exit(1)


# --- BƯỚC 1: Chunk ---
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    text = f.read()
chunks = chunk_by_section(text)
print(f"Bước 1 (Chunk): report.md -> {len(chunks)} section.")

# --- BƯỚC 2+3: Embed tất cả section (1 request) rồi 'store' vào list trong RAM ---
# (Ở production 'store' là vector database; ở đây list là đủ cho demo.)
doc_embs = _guard(lambda: client.embed(
    chunks, model="voyage-3-large", input_type="document"
).embeddings)
print(f"Bước 2+3 (Embed + Store): {len(doc_embs)} vector, mỗi vector {len(doc_embs[0])} chiều.")

# --- BƯỚC 4: Embed câu hỏi user (CÙNG model, input_type='query') ---
question = "What did the software engineering department do this year?"
q_emb = _guard(lambda: client.embed(
    [question], model="voyage-3-large", input_type="query"
).embeddings[0])
print(f"Bước 4 (Process query): đã embed câu hỏi -> vector {len(q_emb)} chiều.")
print(f"   Câu hỏi: {question!r}")

# --- BƯỚC 5: Tính cosine similarity query ↔ từng section, xếp hạng ---
scored = []
for i, emb in enumerate(doc_embs):
    title = chunks[i].strip().splitlines()[0][:55]
    scored.append((cosine_similarity(q_emb, emb), i, title))
scored.sort(reverse=True)   # cao nhất lên đầu

print("\nBước 5 (Find similar): top 5 section giống câu hỏi nhất:")
for sim, i, title in scored[:5]:
    print(f"   {sim:.3f} | chunks[{i}] {title}")

best_sim, best_i, best_title = scored[0]
print(f"\n🏆 Trúng nhất: chunks[{best_i}] — {best_title}  (cosine {best_sim:.3f})")

# --- BƯỚC 6: Ghép final prompt (chưa gửi Claude — chỉ in ra để anh thấy) ---
final_prompt = f"""Answer the user's question about the report.

<user_question>
{question}
</user_question>

<report>
## {chunks[best_i].strip()[:400]}...
</report>"""

print("\nBước 6 (Final prompt) — sẽ gửi cho Claude (in ra để xem):")
print("-" * 70)
print(final_prompt)
print("-" * 70)
print("\n✅ Đó là RAG trọn vẹn: chunk → embed → store → (query) embed → cosine → prompt.")
print("   (Bước gửi prompt cho Claude để trả lời là phần ghép nốt — dùng lại")
print("    client.messages.create() đã học ở các bài đầu khoá.)")
