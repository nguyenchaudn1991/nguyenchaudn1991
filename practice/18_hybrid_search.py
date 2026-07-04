# Bài thực hành 18 — Hybrid Search (kết thúc phần RAG)
# Chạy:  python practice/18_hybrid_search.py
# Bám notebook Anthropic: class Retriever (Reciprocal Rank Fusion) gộp
# VectorIndex (semantic) + BM25Index (lexical) → tìm đúng hơn cả hai dùng riêng.
#
# ⚠️ Gọi VoyageAI (KHÔNG phải Anthropic). Cần: pip install voyageai + VOYAGE_API_KEY trong .env.
#    Chỉ tốn 2 request VoyageAI (batch embed chunks + embed query) → né giới hạn 3 RPM free.

import math
import os
import re
import sys
from collections import Counter
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

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
# Hàm dùng chung
# ==========================================================================
def chunk_by_section(document_text):
    return re.split(r"\n## ", document_text)


def generate_embedding(chunks, model="voyage-3-large", input_type="query"):
    is_list = isinstance(chunks, list)
    inp = chunks if is_list else [chunks]
    result = client.embed(inp, model=model, input_type=input_type)
    return result.embeddings if is_list else result.embeddings[0]


def _guard(call):
    try:
        return call()
    except voyageai.error.RateLimitError:
        print("\n⏳ Dính RATE LIMIT VoyageAI (free = 3 request/phút). Đợi ~60s rồi chạy lại.")
        sys.exit(1)


# ==========================================================================
# SearchIndex Protocol — interface chung để Retriever dùng
# ==========================================================================
class SearchIndex(Protocol):
    def add_document(self, document: Dict[str, Any]) -> None: ...
    def search(self, query: Any, k: int = 1) -> List[Tuple[Dict[str, Any], float]]: ...


# ==========================================================================
# VectorIndex (copy rút gọn từ bài 16)
# ==========================================================================
class VectorIndex:
    def __init__(self, distance_metric: str = "cosine", embedding_fn=None):
        self.vectors: List[List[float]] = []
        self.documents: List[Dict[str, Any]] = []
        self._vector_dim: Optional[int] = None
        self._distance_metric = distance_metric
        self._embedding_fn = embedding_fn

    def add_vector(self, vector, document: Dict[str, Any]):
        if not self.vectors:
            self._vector_dim = len(vector)
        elif len(vector) != self._vector_dim:
            raise ValueError(f"Dim mismatch. Expected {self._vector_dim}, got {len(vector)}")
        self.vectors.append(list(vector))
        self.documents.append(document)

    def add_document(self, document: Dict[str, Any]):
        if not self._embedding_fn:
            raise ValueError("Embedding function not provided.")
        vector = self._embedding_fn(document["content"])
        self.add_vector(vector, document)

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Batch embed — 1 request thay vì N request (né rate limit)."""
        if not self._embedding_fn:
            raise ValueError("Embedding function not provided.")
        contents = [d["content"] for d in documents]
        vectors = self._embedding_fn(contents)
        for vector, doc in zip(vectors, documents):
            self.add_vector(vector, doc)

    def search(self, query: Any, k: int = 1) -> List[Tuple[Dict[str, Any], float]]:
        if not self.vectors:
            return []
        if isinstance(query, str):
            if not self._embedding_fn:
                raise ValueError("Embedding function not provided for string query.")
            query_vector = self._embedding_fn(query)
        else:
            query_vector = query
        dist_func = self._cosine_distance
        distances = [(dist_func(query_vector, v), self.documents[i]) for i, v in enumerate(self.vectors)]
        distances.sort(key=lambda item: item[0])
        return [(doc, dist) for dist, doc in distances[:k]]

    def _cosine_distance(self, v1, v2):
        mag1 = math.sqrt(sum(x * x for x in v1))
        mag2 = math.sqrt(sum(x * x for x in v2))
        if mag1 == 0 or mag2 == 0:
            return 1.0
        dot = sum(p * q for p, q in zip(v1, v2))
        cos = max(-1.0, min(1.0, dot / (mag1 * mag2)))
        return 1.0 - cos

    def __len__(self):
        return len(self.vectors)

    def __repr__(self):
        return f"VectorIndex(count={len(self)}, dim={self._vector_dim})"


# ==========================================================================
# BM25Index (copy rút gọn từ bài 17)
# ==========================================================================
class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75,
                 tokenizer: Optional[Callable[[str], List[str]]] = None):
        self.documents: List[Dict[str, Any]] = []
        self._corpus_tokens: List[List[str]] = []
        self._doc_len: List[int] = []
        self._doc_freqs: Dict[str, int] = {}
        self._avg_doc_len: float = 0.0
        self._idf: Dict[str, float] = {}
        self._index_built: bool = False
        self.k1 = k1
        self.b = b
        self._tokenizer = tokenizer if tokenizer else self._default_tokenizer

    def _default_tokenizer(self, text: str) -> List[str]:
        return [t for t in re.split(r"\W+", text.lower()) if t]

    def _update_stats_add(self, doc_tokens: List[str]):
        self._doc_len.append(len(doc_tokens))
        seen = set()
        for token in doc_tokens:
            if token not in seen:
                self._doc_freqs[token] = self._doc_freqs.get(token, 0) + 1
                seen.add(token)
        self._index_built = False

    def _build_index(self):
        if not self.documents:
            self._avg_doc_len = 0.0; self._idf = {}; self._index_built = True
            return
        self._avg_doc_len = sum(self._doc_len) / len(self.documents)
        N = len(self.documents)
        self._idf = {
            term: math.log(((N - freq + 0.5) / (freq + 0.5)) + 1)
            for term, freq in self._doc_freqs.items()
        }
        self._index_built = True

    def add_document(self, document: Dict[str, Any]):
        doc_tokens = self._tokenizer(document["content"])
        self.documents.append(document)
        self._corpus_tokens.append(doc_tokens)
        self._update_stats_add(doc_tokens)

    def add_documents(self, documents: List[Dict[str, Any]]):
        for doc in documents:
            self.add_document(doc)

    def search(self, query: Any, k: int = 1,
               score_normalization_factor: float = 0.1) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents:
            return []
        if not self._index_built:
            self._build_index()
        if self._avg_doc_len == 0:
            return []
        query_tokens = self._tokenizer(query if isinstance(query, str) else "")
        if not query_tokens:
            return []

        raw_scores = []
        for i in range(len(self.documents)):
            doc_term_counts = Counter(self._corpus_tokens[i])
            doc_length = self._doc_len[i]
            score = 0.0
            for token in query_tokens:
                if token not in self._idf:
                    continue
                idf = self._idf[token]
                tf = doc_term_counts.get(token, 0)
                numerator = idf * tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self._avg_doc_len))
                score += numerator / (denominator + 1e-9)
            if score > 1e-9:
                raw_scores.append((score, self.documents[i]))
        raw_scores.sort(key=lambda item: item[0], reverse=True)

        normalized = []
        for raw, doc in raw_scores[:k]:
            normalized.append((doc, math.exp(-score_normalization_factor * raw)))
        normalized.sort(key=lambda item: item[1])
        return normalized

    def __len__(self):
        return len(self.documents)

    def __repr__(self):
        return f"BM25Index(count={len(self)}, k1={self.k1}, b={self.b})"


# ==========================================================================
# Retriever — gộp nhiều index, merge bằng Reciprocal Rank Fusion (RRF)
# ==========================================================================
class Retriever:
    """Wraps multiple SearchIndex, forwards add_document to all,
    and merges search results via Reciprocal Rank Fusion."""

    def __init__(self, *indexes: SearchIndex):
        if len(indexes) == 0:
            raise ValueError("At least one index must be provided")
        self._indexes = list(indexes)

    def add_document(self, document: Dict[str, Any]):
        for index in self._indexes:
            index.add_document(document)

    def add_documents(self, documents: List[Dict[str, Any]]):
        for index in self._indexes:
            index.add_documents(documents)

    def search(self, query_text: str, k: int = 1, k_rrf: int = 60) -> List[Tuple[Dict[str, Any], float]]:
        """
        1) Chạy query qua TẤT CẢ index (lấy k*5 mỗi index để có đủ ứng cử viên)
        2) Gom rank của mỗi doc qua từng index
        3) Tính RRF score = Σ 1/(k_rrf + rank_i)
        4) Sort giảm, trả top-k (doc, rrf_score)
        """
        # Bước 1: lấy kết quả từ tất cả index
        all_results = [index.search(query_text, k=k * 5) for index in self._indexes]

        # Bước 2: gom rank
        doc_ranks: Dict[int, Dict] = {}
        for idx, results in enumerate(all_results):
            for rank, (doc, _score) in enumerate(results):
                doc_id = id(doc)
                if doc_id not in doc_ranks:
                    doc_ranks[doc_id] = {
                        "doc_obj": doc,
                        "ranks": [float("inf")] * len(self._indexes),
                    }
                doc_ranks[doc_id]["ranks"][idx] = rank + 1  # rank bắt đầu từ 1

        # Bước 3: tính RRF
        def calc_rrf(ranks: List[float]) -> float:
            return sum(1.0 / (k_rrf + r) for r in ranks if r != float("inf"))

        scored = [(info["doc_obj"], calc_rrf(info["ranks"])) for info in doc_ranks.values()]

        # Bước 4: sort giảm (RRF CAO = liên quan hơn), trả top-k
        scored = [(doc, score) for doc, score in scored if score > 0]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    def __repr__(self):
        return f"Retriever(indexes={len(self._indexes)})"


# ==========================================================================
# CHẠY: hybrid search trên report.md
# ==========================================================================
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Chunk
chunks = chunk_by_section(text)
print(f"1. Chunk: {len(chunks)} section.\n")

# 2. Tạo index + Retriever
vector_index = VectorIndex(embedding_fn=generate_embedding)
bm25_index = BM25Index()
retriever = Retriever(bm25_index, vector_index)
print(f"2. Tạo Retriever: {retriever}")
print(f"   ├── {bm25_index}")
print(f"   └── {vector_index}\n")

# 3. Nạp tất cả chunk vào Retriever (tự forward sang cả 2 index)
#    ⭐ Dùng add_documents (batch) để VectorIndex chỉ gọi 1 request VoyageAI
docs = [{"content": chunk} for chunk in chunks]
_guard(lambda: retriever.add_documents(docs))
print(f"3. Nạp {len(docs)} chunk vào cả 2 index:")
print(f"   ├── {bm25_index}")
print(f"   └── {vector_index}\n")

# 4. Search — câu hỏi mà semantic search đơn ĐÚNG nhưng sai thứ tự
query = "What happened with INC-2023-Q4-011?"
print(f"4. Hybrid search: {query!r}\n")

results = _guard(lambda: retriever.search(query, k=5, k_rrf=60))
print("   Top 5 (RRF score — CAO = liên quan hơn):\n")
for i, (doc, rrf_score) in enumerate(results, 1):
    title = doc["content"].strip().splitlines()[0][:60]
    print(f"   {i}. rrf={rrf_score:.4f} | {title}")

# 5. So sánh: chỉ semantic vs chỉ BM25 vs hybrid
print("\n" + "=" * 70)
print("  SO SÁNH: Semantic only vs BM25 only vs Hybrid (top 3)")
print("=" * 70)

sem_results = _guard(lambda: vector_index.search(query, k=3))
bm25_results = bm25_index.search(query, k=3)
hybrid_results = results[:3]

def _title(doc):
    return doc["content"].strip().splitlines()[0][:50]

print("\n📐 Semantic (cosine distance — THẤP = giống):")
for doc, dist in sem_results:
    print(f"   dist={dist:.4f} | {_title(doc)}")

print("\n📝 BM25 (normalized — THẤP = liên quan):")
for doc, score in bm25_results:
    print(f"   score={score:.4f} | {_title(doc)}")

print("\n🔀 Hybrid (RRF — CAO = liên quan):")
for doc, rrf in hybrid_results:
    print(f"   rrf={rrf:.4f} | {_title(doc)}")

# 6. Đối chiếu: section nào THẬT SỰ chứa mã?
print("\n🔎 Đối chiếu — section thật sự chứa 'INC-2023-Q4-011':")
for i, ch in enumerate(chunks):
    if "INC-2023-Q4-011" in ch:
        title = ch.strip().splitlines()[0][:55]
        print(f"   ✓ chunks[{i}] {title}")

print("\n💡 Hybrid search lấy ĐIỂM MẠNH cả hai:")
print("   • BM25 tìm CHÍNH XÁC mã (INC-2023-Q4-011 → IDF cao)")
print("   • Semantic hiểu NGHĨA câu hỏi (\"what happened\" → incident analysis)")
print("   • RRF merge: section nào CÙNG xuất hiện ở cả hai → rank cao hơn hẳn")
print("   → Kết quả cuối chính xác hơn dùng riêng lẻ từng phương pháp.")
print("\n🏁 Đây là bước cuối của phần RAG trong khoá Building with Claude API.")
