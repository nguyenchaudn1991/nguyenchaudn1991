# Bài thực hành 16 — RAG với class VectorIndex (vector store tự viết)
# Chạy:  python practice/16_vector_store.py
# Bám notebook Anthropic 003_vectordb.ipynb: class VectorIndex + 5 bước RAG.
#
# ⚠️ Gọi VoyageAI (KHÔNG phải Anthropic). Cần: pip install voyageai + VOYAGE_API_KEY trong .env.
#    Chỉ tốn 2 request (batch embed chunks + embed query) -> né giới hạn 3 RPM free.

import math
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

load_dotenv()

REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.md")

if not os.getenv("VOYAGE_API_KEY"):
    print("❌ Chưa thấy VOYAGE_API_KEY trong .env. Đăng ký https://www.voyageai.com rồi thêm key.")
    sys.exit(1)
try:
    import voyageai
except ImportError:
    print("❌ Chưa cài voyageai.  pip install voyageai")
    sys.exit(1)

client = voyageai.Client()


# ==========================================================================
# Hàm của notebook (giữ nguyên)
# ==========================================================================
def chunk_by_section(document_text):
    return re.split(r"\n## ", document_text)


def generate_embedding(chunks, model="voyage-3-large", input_type="query"):
    # ⭐ Nâng cấp: nhận CẢ string lẫn list. List -> trả list embedding (batch);
    #             string -> trả 1 embedding.
    is_list = isinstance(chunks, list)
    inp = chunks if is_list else [chunks]
    result = client.embed(inp, model=model, input_type=input_type)
    return result.embeddings if is_list else result.embeddings[0]


# ==========================================================================
# VectorIndex — "vector database" thu nhỏ (rút gọn từ notebook, giữ đúng logic)
# ==========================================================================
class VectorIndex:
    def __init__(self, distance_metric: str = "cosine", embedding_fn=None):
        self.vectors: List[List[float]] = []
        self.documents: List[Dict[str, Any]] = []
        self._vector_dim: Optional[int] = None
        if distance_metric not in ["cosine", "euclidean"]:
            raise ValueError("distance_metric must be 'cosine' or 'euclidean'")
        self._distance_metric = distance_metric
        self._embedding_fn = embedding_fn

    def add_vector(self, vector, document: Dict[str, Any]):
        if not isinstance(vector, list) or not all(isinstance(x, (int, float)) for x in vector):
            raise TypeError("Vector must be a list of numbers.")
        if not isinstance(document, dict) or "content" not in document:
            raise ValueError("Document must be a dict containing a 'content' key.")
        # kiểm tra CÙNG số chiều
        if not self.vectors:
            self._vector_dim = len(vector)
        elif len(vector) != self._vector_dim:
            raise ValueError(f"Inconsistent vector dimension. Expected {self._vector_dim}, got {len(vector)}")
        self.vectors.append(list(vector))
        self.documents.append(document)

    def add_document(self, document: Dict[str, Any]):
        if not self._embedding_fn:
            raise ValueError("Embedding function not provided during initialization.")
        vector = self._embedding_fn(document["content"])
        self.add_vector(vector, document)

    def search(self, query: Any, k: int = 1) -> List[Tuple[Dict[str, Any], float]]:
        if not self.vectors:
            return []
        # query có thể là string (tự embed) hoặc list số (dùng thẳng)
        if isinstance(query, str):
            if not self._embedding_fn:
                raise ValueError("Embedding function not provided for string query.")
            query_vector = self._embedding_fn(query)
        elif isinstance(query, list) and all(isinstance(x, (int, float)) for x in query):
            query_vector = query
        else:
            raise TypeError("Query must be a string or a list of numbers.")
        if len(query_vector) != self._vector_dim:
            raise ValueError(f"Query dim mismatch. Expected {self._vector_dim}, got {len(query_vector)}")
        if k <= 0:
            raise ValueError("k must be a positive integer.")

        dist_func = self._cosine_distance if self._distance_metric == "cosine" else self._euclidean_distance
        distances = [(dist_func(query_vector, v), self.documents[i]) for i, v in enumerate(self.vectors)]
        distances.sort(key=lambda item: item[0])            # distance THẤP lên đầu = giống nhất
        return [(doc, dist) for dist, doc in distances[:k]]

    def _euclidean_distance(self, v1, v2):
        return math.sqrt(sum((p - q) ** 2 for p, q in zip(v1, v2)))

    def _cosine_distance(self, v1, v2):
        mag1 = math.sqrt(sum(x * x for x in v1))
        mag2 = math.sqrt(sum(x * x for x in v2))
        if mag1 == 0 and mag2 == 0:
            return 0.0
        if mag1 == 0 or mag2 == 0:
            return 1.0
        dot = sum(p * q for p, q in zip(v1, v2))
        cos = max(-1.0, min(1.0, dot / (mag1 * mag2)))      # clamp tránh lỗi làm tròn
        return 1.0 - cos                                    # cosine DISTANCE = 1 - similarity

    def __len__(self):
        return len(self.vectors)

    def __repr__(self):
        return f"VectorIndex(count={len(self)}, dim={self._vector_dim}, metric='{self._distance_metric}')"


def _guard(call):
    try:
        return call()
    except voyageai.error.RateLimitError:
        print("\n⏳ Dính RATE LIMIT VoyageAI (free = 3 request/phút). Đợi ~60s rồi chạy lại.")
        sys.exit(1)


# ==========================================================================
# 5 BƯỚC RAG
# ==========================================================================
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Chunk
chunks = chunk_by_section(text)
print(f"1. Chunk: {len(chunks)} section.")

# 2. Embed tất cả chunk trong 1 request (batch — generate_embedding nhận list)
embeddings = _guard(lambda: generate_embedding(chunks, input_type="document"))
print(f"2. Embed: {len(embeddings)} vector, mỗi vector {len(embeddings[0])} chiều.")

# 3. Tạo store & nạp (embedding + TEXT GỐC) — lưu text để search xong lấy lại được
store = VectorIndex()
for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})
print(f"3. Store: {store}")

# 4. Embed câu hỏi user (cùng model)
question = "What did the software engineering dept do last year?"
user_embedding = _guard(lambda: generate_embedding(question, input_type="query"))
print(f"4. Query embedded: {question!r}")

# 5. Search — 2 chunk gần nhất (distance thấp = giống hơn)
print("\n5. Search — 2 chunk liên quan nhất (cosine distance, thấp = giống):\n")
results = store.search(user_embedding, 2)
for doc, distance in results:
    title = doc["content"].strip().splitlines()[0][:60]
    print(f"   distance={distance:.3f} | {title}")
    print(f"      {doc['content'].strip()[:160].replace(chr(10), ' ')}…\n")

best = results[0]
print(f"🏆 Trúng nhất: {best[0]['content'].strip().splitlines()[0][:60]} (distance {best[1]:.3f})")
print("\n💡 Để ý: nếu Methodology lọt top-2 sát nút -> retrieval CHƯA hoàn hảo.")
print("   'Chạy ra kết quả' ≠ 'đúng' — bài sau sẽ cải thiện độ chính xác.")
