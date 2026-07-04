# Bài thực hành 17 — BM25 (lexical search) vá điểm yếu của semantic search
# Chạy:  python practice/17_bm25.py
# Bám notebook Anthropic: class BM25Index + tìm mã sự cố "INC-2023-Q4-011".
#
# ⚡ BM25 THUẦN PYTHON — KHÔNG gọi API, KHÔNG tốn tiền. Chạy thoải mái.

import math
import os
import re
import sys
from collections import Counter
from typing import Any, Callable, Dict, List, Optional, Tuple

sys.stdout.reconfigure(encoding="utf-8")

REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.md")


def chunk_by_section(document_text):
    return re.split(r"\n## ", document_text)


# ==========================================================================
# BM25Index — lexical search (đúng logic notebook Anthropic)
# ==========================================================================
class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75,
                 tokenizer: Optional[Callable[[str], List[str]]] = None):
        self.documents: List[Dict[str, Any]] = []
        self._corpus_tokens: List[List[str]] = []
        self._doc_len: List[int] = []
        self._doc_freqs: Dict[str, int] = {}       # mỗi term có mặt trong bao nhiêu DOC
        self._avg_doc_len: float = 0.0
        self._idf: Dict[str, float] = {}
        self._index_built: bool = False
        self.k1 = k1
        self.b = b
        self._tokenizer = tokenizer if tokenizer else self._default_tokenizer

    def _default_tokenizer(self, text: str) -> List[str]:
        text = text.lower()                        # lowercase
        tokens = re.split(r"\W+", text)            # tách theo ký tự KHÔNG-chữ
        return [t for t in tokens if t]            # bỏ token rỗng

    def _update_stats_add(self, doc_tokens: List[str]):
        self._doc_len.append(len(doc_tokens))
        seen = set()
        for token in doc_tokens:                   # đếm document-frequency (mỗi doc tính 1 lần/term)
            if token not in seen:
                self._doc_freqs[token] = self._doc_freqs.get(token, 0) + 1
                seen.add(token)
        self._index_built = False                  # thêm doc -> phải build lại index

    def _calculate_idf(self):
        N = len(self.documents)
        self._idf = {}
        for term, freq in self._doc_freqs.items():
            # freq (số doc chứa term) THẤP -> idf CAO
            self._idf[term] = math.log(((N - freq + 0.5) / (freq + 0.5)) + 1)

    def _build_index(self):
        if not self.documents:
            self._avg_doc_len = 0.0; self._idf = {}; self._index_built = True
            return
        self._avg_doc_len = sum(self._doc_len) / len(self.documents)
        self._calculate_idf()
        self._index_built = True

    def add_document(self, document: Dict[str, Any]):
        if not isinstance(document, dict) or "content" not in document:
            raise ValueError("Document must be a dict containing a 'content' key.")
        doc_tokens = self._tokenizer(document["content"])
        self.documents.append(document)
        self._corpus_tokens.append(doc_tokens)
        self._update_stats_add(doc_tokens)

    def _compute_bm25_score(self, query_tokens: List[str], doc_index: int) -> float:
        score = 0.0
        doc_term_counts = Counter(self._corpus_tokens[doc_index])
        doc_length = self._doc_len[doc_index]
        for token in query_tokens:
            if token not in self._idf:
                continue
            idf = self._idf[token]
            tf = doc_term_counts.get(token, 0)     # term frequency trong DOC này
            numerator = idf * tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self._avg_doc_len))
            score += numerator / (denominator + 1e-9)
        return score

    def search(self, query_text: str, k: int = 1,
               score_normalization_factor: float = 0.1) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents:
            return []
        if not self._index_built:
            self._build_index()
        if self._avg_doc_len == 0:
            return []
        query_tokens = self._tokenizer(query_text)
        if not query_tokens:
            return []

        raw_scores = []
        for i in range(len(self.documents)):
            raw = self._compute_bm25_score(query_tokens, i)
            if raw > 1e-9:
                raw_scores.append((raw, self.documents[i]))
        raw_scores.sort(key=lambda item: item[0], reverse=True)   # raw CAO = liên quan

        # chuẩn hoá về dạng GIỐNG DISTANCE (thấp = tốt) để lát merge với cosine
        normalized = []
        for raw, doc in raw_scores[:k]:
            normalized.append((doc, math.exp(-score_normalization_factor * raw)))
        normalized.sort(key=lambda item: item[1])
        return normalized

    def __len__(self):
        return len(self.documents)

    def __repr__(self):
        return f"BM25Index(count={len(self)}, k1={self.k1}, b={self.b}, index_built={self._index_built})"


# ==========================================================================
# CHẠY: tìm mã sự cố "INC-2023-Q4-011"
# ==========================================================================
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Chunk
chunks = chunk_by_section(text)
print(f"1. Chunk: {len(chunks)} section.")

# 2. BM25 store
store = BM25Index()
for chunk in chunks:
    store.add_document({"content": chunk})
print(f"2. Store: {store}")

# 3. Search
query = "What happened with INC-2023-Q4-011?"
print(f"3. Search: {query!r}\n")
results = store.search(query, 3)
print("Top 3 (normalized score — THẤP = liên quan hơn):\n")
for doc, distance in results:
    title = doc["content"].strip().splitlines()[0][:55]
    print(f"   score={distance:.4f} | {title}")

# --- Đối chiếu: section nào THẬT SỰ chứa mã? (chứng minh BM25 tìm đúng) ---
print("\n🔎 Đối chiếu — section thật sự chứa 'INC-2023-Q4-011':")
for i, ch in enumerate(chunks):
    if "INC-2023-Q4-011" in ch:
        title = ch.strip().splitlines()[0][:55]
        print(f"   ✓ chunks[{i}] {title}")

print("\n💡 BM25 ưu tiên đúng các section chứa mã (Software Engineering + Cybersecurity)")
print("   nhờ mã hiếm -> IDF cao. Semantic search dễ lôi nhầm section chỉ liên quan")
print("   khái niệm. Bài sau MERGE 2 kết quả -> hybrid search.")
