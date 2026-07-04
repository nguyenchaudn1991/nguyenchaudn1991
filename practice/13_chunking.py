# Bài thực hành 13 — Text Chunking (cắt tài liệu cho RAG)
# Chạy:  python practice/13_chunking.py
# Mục tiêu: xem TẬN MẮT 3 chiến lược cắt cùng một tài liệu (report.md) khác nhau ra sao,
#           và vì sao "chunk dở -> lấy nhầm ngữ cảnh -> AI trả lời sai".
#
# ⭐ Bài này KHÔNG gọi Claude API -> KHÔNG tốn tiền. Cứ chạy đi chạy lại thoải mái,
#    đổi tham số (chunk_size, overlap...) để cảm nhận.

import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")  # in tiếng Việt/ký tự lạ trên Windows

# report.md nằm CÙNG thư mục với script này -> chạy ở đâu cũng tìm ra
REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.md")


# ==========================================================================
# 3 HÀM CHUNKING (đúng bản Anthropic đưa, chỉ thêm chú thích tiếng Việt)
# ==========================================================================

# --- Chiến lược 1: Size-based (cắt theo SỐ KÝ TỰ, có overlap) ---
def chunk_by_char(text, chunk_size=150, chunk_overlap=20):
    chunks = []
    start_idx = 0
    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))   # không vượt quá cuối text
        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)
        # ⭐ MẤU CHỐT: nhảy tới = cuối chunk LÙI LẠI overlap ký tự
        #    -> chunk sau lấn vào chunk trước (giữ context). Chạm cuối thì dừng hẳn.
        start_idx = end_idx - chunk_overlap if end_idx < len(text) else len(text)
    return chunks


# --- Chiến lược 2: Sentence-based (gom N CÂU một chunk, overlap tính theo câu) ---
def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    # (?<=[.!?]) = lookbehind: cắt tại khoảng trắng ĐỨNG NGAY SAU . ! ?
    # -> tách thành câu mà VẪN GIỮ dấu câu dính vào câu.
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    start_idx = 0
    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))
        start_idx += max_sentences_per_chunk - overlap_sentences  # tiến bước, chừa overlap câu
        if start_idx < 0:
            start_idx = 0
    return chunks


# --- Chiến lược 3: Structure-based (cắt theo HEADING "## " của Markdown) ---
def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)


# ==========================================================================
# HELPER: in danh sách chunk cho gọn (preview đầu mỗi chunk + số ký tự)
# ==========================================================================
def preview(chunks, n_preview=150, show=None):
    """In tóm tắt các chunk. show=None in hết; show=3 chỉ in 3 chunk đầu."""
    total = len(chunks)
    to_show = total if show is None else min(show, total)
    for i in range(to_show):
        head = chunks[i].replace("\n", " ").strip()
        if len(head) > n_preview:
            head = head[:n_preview] + "…"
        print(f"  [chunk {i:>2}] {len(chunks[i]):>4} ký tự | {head}")
    if to_show < total:
        print(f"  … còn {total - to_show} chunk nữa (ẩn bớt cho gọn)")
    print()


def banner(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def show_full(chunks, indices):
    """In TRỌN VẸN (không cắt) các chunk theo chỉ số trong indices — để thấy hết nội dung."""
    for i in indices:
        print(f"\n┌── chunk {i} ({len(chunks[i])} ký tự) " + "─" * 30)
        print(chunks[i])
        print("└" + "─" * 48)


# ==========================================================================
# CHẠY THỬ trên report.md
# ==========================================================================
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

print(f"📄 Đã đọc report.md — tổng {len(text)} ký tự.")

# ---- 1) Size-based ----
banner("Chiến lược 1 — SIZE-BASED (chunk_size=150, overlap=20)")
c1 = chunk_by_char(text, chunk_size=150, chunk_overlap=20)
print(f"→ Cắt ra {len(c1)} chunk. Xem 4 chunk đầu (để ý từ/câu bị CẮT NGANG):\n")
preview(c1, show=4)

# ---- 2) Sentence-based ----
banner("Chiến lược 2 — SENTENCE-BASED (5 câu/chunk, overlap 1 câu)")
c2 = chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1)
print(f"→ Cắt ra {len(c2)} chunk. Câu KHÔNG bị cắt giữa chừng (khác size-based).")
print("  Kích thước chunk LỆCH nhau vì mỗi chunk = 5 câu, mà câu dài ngắn khác nhau.\n")
preview(c2, show=4)

# --- MỔ XẺ: xem chiến lược 2 hoạt động ra sao ---
print("── MỔ XẺ chiến lược 2: trước tiên tách text thành các CÂU ──\n")
sents = re.split(r"(?<=[.!?])\s+", text)
print(f"Tổng cộng {len(sents)} câu. Xem 6 câu đầu (đánh số):\n")
for i in range(6):
    s = sents[i].replace("\n", " ").strip()
    if len(s) > 100:
        s = s[:100] + "…"
    print(f"  câu {i}: {s}")

print("\nGom 5 câu/chunk, overlap 1 câu -> chunk 0 = câu[0:5], chunk 1 = câu[4:9]…")
print("=> câu số 4 nằm ở CUỐI chunk 0 VÀ ĐẦU chunk 1 (phần overlap lặp lại).")
print("\nIn TRỌN chunk 0 và chunk 1 để anh thấy câu 4 xuất hiện ở cả hai:")
show_full(c2, [0, 1])

# ---- 3) Structure-based ----
banner("Chiến lược 3 — STRUCTURE-BASED (cắt theo heading '## ')")
c3 = chunk_by_section(text)
print(f"→ Cắt ra {len(c3)} chunk — mỗi chunk = MỘT SECTION trọn vẹn (sạch nhất):\n")
preview(c3, show=None)  # in hết để thấy mỗi section 1 chunk


# ==========================================================================
# ⭐ MINH HOẠ "VẤN ĐỀ CON BUG": vì sao chunk dở -> lấy nhầm ngữ cảnh
# ==========================================================================
# Anthropic kể chuyện từ "bug" (con bọ vs lỗi phần mềm). Tài liệu report.md này
# không có chữ 'bug', nhưng CÓ một từ mập mờ y hệt: "biomarker" xuất hiện ở CẢ HAI
# section khác nhau — Section 1 (Medical / XDR-471) và Section 9 (Pharma / CTX-204b).
# -> User hỏi "biomarker cho thử nghiệm THUỐC là gì?" mà retrieve dở thì rất dễ lôi
#    nhầm biomarker bên NGHIÊN CỨU Y KHOA về. Đây chính là "vấn đề con bug" ngoài đời.
banner('Vì sao chunking quan trọng — user hỏi về "biomarker" (từ mập mờ 2 section)')

question_keyword = "biomarker"


def find_hits(chunks, keyword):
    """Tìm (rất thô) các chunk có chứa keyword — mô phỏng bước 'retrieve' của RAG."""
    kw = keyword.lower()
    return [i for i, ch in enumerate(chunks) if kw in ch.lower()]


def section_title(section_chunk):
    """Lấy dòng heading (dòng đầu) của một section chunk để biết nó thuộc mảng nào."""
    return section_chunk.strip().splitlines()[0][:75]


# Structure-based: mỗi hit là 1 SECTION rõ ràng -> ta BIẾT chunk thuộc mảng nào,
# nên dễ chọn đúng (Pharma) và loại nhầm (Medical).
hits_struct = find_hits(c3, question_keyword)
print(f"[STRUCTURE-BASED] '{question_keyword}' xuất hiện ở {len(hits_struct)} section:")
for i in hits_struct:
    print(f"   → chunk {i}: {section_title(c3[i])}")
print("   => Ranh giới section RÕ: biết chunk nào là Medical, chunk nào là Pharma")
print("      -> chọn đúng ngữ cảnh dễ dàng.\n")

# Size-based: hit rải rác nhiều mẩu vụn, mỗi mẩu MẤT tiêu đề section
# -> chỉ nhìn chunk KHÔNG biết nó thuộc Medical hay Pharma -> dễ retrieve nhầm.
hits_size = find_hits(c1, question_keyword)
print(f"[SIZE-BASED]     '{question_keyword}' xuất hiện ở {len(hits_size)} chunk vụn: {hits_size}")
for i in hits_size:
    head = c1[i].replace("\n", " ").strip()[:80]
    print(f"   → chunk {i}: …{head}…")
print("   => Mỗi chunk chỉ ~150 ký tự, ĐÃ MẤT tiêu đề section -> nhìn vào không biết")
print("      thuộc Medical hay Pharma -> retrieve xong vẫn có thể trả lời SAI ngữ cảnh.")

print("\n💡 Bài học: structure-based cho ranh giới chủ đề SẠCH -> retrieve trúng section.")
print("   Nhưng nó CHỈ chạy khi tài liệu có cấu trúc (như Markdown này). Tài liệu")
print("   plain text/PDF lộn xộn thì phải quay về size-based + overlap (fallback tin cậy).")


# ==========================================================================
# 🧪 TỰ THỬ (gợi ý): bỏ comment từng dòng dưới để cảm nhận trade-off
# ==========================================================================
# print("\n--- Thử overlap=0 (không chồng lấn) ---")
# preview(chunk_by_char(text, chunk_size=150, chunk_overlap=0), show=4)
#
# print("\n--- Thử chunk_size lớn hơn (500) -> ít chunk hơn, mỗi chunk nhiều context hơn ---")
# print("Số chunk:", len(chunk_by_char(text, chunk_size=500, chunk_overlap=50)))
