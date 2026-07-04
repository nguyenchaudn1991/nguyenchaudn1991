# Bài thực hành 14 — Text Embeddings với VoyageAI (bước "tìm chunk liên quan" của RAG)
# Chạy:  python practice/14_embeddings.py
# Bám theo notebook gốc Anthropic: đọc report.md -> chunk_by_section -> embed chunks[0].
# (Thêm phần "soi vector" để học được nhiều hơn là chỉ in ra một cục số.)
#
# ⚠️ Bài này GỌI API VoyageAI (KHÔNG phải Anthropic). Cần chuẩn bị:
#   1) Đăng ký tài khoản VoyageAI: https://www.voyageai.com  (key free để bắt đầu)
#   2) pip install voyageai
#   3) Thêm vào file .env (cùng chỗ ANTHROPIC_API_KEY):
#        VOYAGE_API_KEY="voyage-..."

import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

load_dotenv()

# report.md nằm CÙNG thư mục với script này -> chạy ở đâu cũng tìm ra
REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.md")

# --- Kiểm tra điều kiện trước khi gọi API (để lỗi rõ ràng, không mập mờ) ---
if not os.getenv("VOYAGE_API_KEY"):
    print("❌ Chưa thấy VOYAGE_API_KEY trong môi trường.")
    print("   → Đăng ký https://www.voyageai.com lấy key, rồi thêm vào .env:")
    print('     VOYAGE_API_KEY="voyage-..."')
    sys.exit(1)

try:
    import voyageai
except ImportError:
    print("❌ Chưa cài thư viện voyageai.  Chạy:  pip install voyageai")
    sys.exit(1)

client = voyageai.Client()  # tự đọc VOYAGE_API_KEY từ env (giống Anthropic())


def _guard(call):
    """Chạy 1 lệnh gọi API, nếu dính rate limit thì báo tiếng Việt dễ hiểu rồi dừng."""
    try:
        return call()
    except voyageai.error.RateLimitError:
        print("\n⏳ Dính RATE LIMIT của VoyageAI (free = 3 request/phút, 10K token/phút).")
        print("   → Đợi ~60 giây rồi chạy lại, HOẶC gắn payment method ở")
        print("     https://dashboard.voyageai.com/ (vẫn được 200M token free cho series 3).")
        sys.exit(1)


# ==========================================================================
# Hàm của notebook gốc (giữ nguyên)
# ==========================================================================
def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)


def generate_embedding(text, model="voyage-3-large", input_type="query"):
    # client.embed nhận MỘT LIST text (embed nhiều đoạn cùng lúc)
    # -> truyền [text] cho 1 đoạn rồi lấy .embeddings[0]
    result = client.embed([text], model=model, input_type=input_type)
    return result.embeddings[0]


def generate_embeddings(texts, model="voyage-3-large", input_type="document"):
    # ⭐ BATCH: embed NHIỀU đoạn trong MỘT request -> ít request hơn (né rate limit)
    #    + nhanh hơn. Trả về list embedding, CÙNG THỨ TỰ với texts.
    result = client.embed(texts, model=model, input_type=input_type)
    return result.embeddings


# ==========================================================================
# 1) ĐÚNG FLOW NOTEBOOK: đọc report.md -> cắt section -> embed các chunk đầu
#    (Gộp 4 chunk vào 1 request để tránh giới hạn 3 RPM của VoyageAI free.)
# ==========================================================================
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_by_section(text)
print(f"📄 report.md -> chunk_by_section cắt ra {len(chunks)} section.")
print(f"   Section đầu (chunks[0]) — 60 ký tự đầu: {chunks[0][:60]!r}\n")

# 1 REQUEST duy nhất cho 4 chunk đầu (thay vì 4 request lẻ)
sample = chunks[:4]
embs = _guard(lambda: generate_embeddings(sample, input_type="document"))
emb0 = embs[0]   # embedding của chunks[0] — đúng cái notebook gốc lấy

# --- SOI cái vector (notebook chỉ in cả cục số; ta phân tích cho dễ hiểu) ---
print("🔢 Embedding của chunks[0]:")
print(f"   → là list {len(emb0)} số thực (dimensions của voyage-3-large).")
print(f"   → 8 số đầu: {[round(x, 4) for x in emb0[:8]]}")
print(f"   → nhỏ nhất {min(emb0):.4f} | lớn nhất {max(emb0):.4f}  (đều trong [-1, +1])")
print("   ⭐ Không biết mỗi số nghĩa là gì — model tự học lúc training.\n")

# ==========================================================================
# 2) Mọi chunk -> vector CÙNG ĐỘ DÀI (điều kiện để so sánh được ở bài sau)
#    -> lấy luôn từ batch trên, KHÔNG tốn thêm request.
# ==========================================================================
print("Các section vừa embed (cùng batch) đều CÙNG số chiều:")
for i, e in enumerate(embs):
    title = chunks[i].strip().splitlines()[0][:55]
    print(f"  • chunks[{i}] len={len(e)} | {title}")
print("→ Cùng số chiều -> mới đo khoảng cách (so sánh) được ở bài sau.\n")


# ==========================================================================
# 3) TEASER bài sau: query vs document (1 request nữa)
# ==========================================================================
# Bài sau ĐO ĐỘ GIỐNG NHAU giữa query và từng chunk để chọn chunk liên quan.
# Câu hỏi dùng input_type="query", chunk tài liệu dùng input_type="document".
query = "How did the company perform financially?"
q_emb = _guard(lambda: generate_embedding(query, input_type="query"))
print("🔎 Query:", query)
print(f"   → cũng thành 1 vector {len(q_emb)} chiều (input_type='query').")
print("   Bài SAU: so q_emb với embedding từng section -> section 'Financial Analysis'")
print("   sẽ GẦN nhất -> đó chính là semantic search.")
