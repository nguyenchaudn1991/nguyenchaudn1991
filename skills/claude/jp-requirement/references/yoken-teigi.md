# 要件定義書 — viết tài liệu định nghĩa yêu cầu (tiếng Nhật, khách duyệt)

Đầu vào: kết quả phân tích (requirement-analysis.md) đã được khách chọn phương án.
Đầu ra: 要件定義書 khách 承認 được — là "hợp đồng nội dung" giữa 2 bên, mọi tranh cãi
sau này đều quay về tài liệu này. Viết bằng tiếng Nhật です・ます (bảng được dùng 体言止め).

---

## Cấu trúc chuẩn (đủ 13 mục — mục không áp dụng ghi 「該当なし」, không xóa)

1. **改訂履歴** — bảng version | ngày | người sửa | nội dung sửa (đặt đầu tài liệu).
2. **背景・目的** — bài toán kinh doanh + mục tiêu đo được (KPI sau khi làm xong).
3. **用語定義** — thuật ngữ nghiệp vụ dùng trong tài liệu (dùng đúng từ của khách).
4. **現状業務フロー (As-Is)** — flow hiện tại + điểm đau (đánh dấu trên flow).
5. **新業務フロー (To-Be)** — flow sau khi có hệ thống; đối chiếu được với As-Is.
6. **システム化範囲** — trong scope VÀ **ngoài scope (対象外)** viết tường minh —
   mục 対象外 là mục chống tranh cãi quan trọng nhất tài liệu.
7. **機能要件一覧** — bảng: ID (FR-001…) | 機能名 | 概要 | 優先度 (MUST/WANT theo chữ
   khách đã dùng) | 備考. Chi tiết từng FR viết mục con nếu cần.
8. **非機能要件** — 性能 (response, số user đồng thời, khối lượng data — số + điều kiện đo) /
   可用性 (giờ vận hành, mục tiêu khôi phục) / セキュリティ (auth, quyền, log) / 運用・保守
   (backup, monitoring, ai vận hành).
9. **外部インターフェース** — hệ thống ngoài kết nối: chiều, format, tần suất, chủ quản.
10. **データ要件** — data chính, nguồn, khối lượng, yêu cầu migrate.
11. **移行要件** — chuyển từ hệ cũ: data nào, ai làm, khi nào, tiêu chí xong.
12. **前提条件・制約事項** — 前提 từ bước phân tích (đã được khách xác nhận) + ràng buộc
    (deadline, môi trường, quy định). 前提 chưa xác nhận → KHÔNG được nằm ở đây, còn ở 未決事項.
13. **課題・未決事項** — link sang 課題表/Q&A (skill `jp-comm`), ghi số tham chiếu.
    Chỉ được 承認 khi mục còn lại là **non-blocking**, owner/deadline rõ và phần bị ảnh hưởng
    được khoanh. Còn unresolved về scope, acceptance, security/compliance, tiền hoặc quyết định
    khó rollback → **block approval** cho tới khi authority chốt.

## Luật viết từng câu yêu cầu

- **1 yêu cầu = 1 câu = 1 ID.** Câu chứa 「および」「また」 nối 2 yêu cầu → tách 2 ID.
- **Kiểm thử được:** người thứ ba đọc xong phải viết được test case. Cấm 「使いやすい」
  「高速に」「柔軟に」 trần — phải kèm số + điều kiện đo (「3秒以内（100件表示時）」).
- **Cấm chính những từ mơ hồ mà mình soi khách** (bảng trong spec-breakdown.md):
  「など」「適宜」「基本的に」「別途」… — mình viết ra thì dev và khách cũng sẽ hiểu lệch.
- Chủ ngữ rõ: hệ thống làm hay người vận hành làm (「システムは〜」/「運用担当者は〜」).
- Mọi số liệu có đơn vị + bối cảnh (件/ngày? 件/tháng? peak hay trung bình?).

## Traceability — sợi chỉ xuyên suốt dự án

```
課題 (phân tích) → FR-ID (要件定義書) → mục spec-breakdown cho dev → test case → 納品報告
```
- Mỗi FR ghi nó giải quyết 課題 nào; thay đổi từ Q&A nào (「Q-12回答により追加」).
- Sau này khách hỏi "vì sao có tính năng này" / dev hỏi "làm để làm gì" → trả lời trong 10 giây.

## Quy trình chốt & quản lý thay đổi

1. **Draft nội bộ** → tự review bằng checklist dưới → **khách review** (đi kèm 1 trang
   tóm tắt điểm cần khách nhìn kỹ — đừng ném 30 trang trần) → sửa → **承認** (ghi ngày,
   người duyệt, version 1.0).
2. **Sau 承認, thay đổi nghĩa/scope đi qua 変更管理:** ghi vào 改訂履歴 + đánh version mới +
   thông báo khách bằng bảng 「変更前 → 変更後 + 理由」. Sửa editorial thuần túy không đổi
   nghĩa có thể gộp vào revision note nội bộ; hễ có khả năng đổi cách hiểu thì phải xử lý như
   requirement change, không sửa im lặng.
3. Thay đổi làm tăng scope → nói rõ ảnh hưởng lịch trước khi nhận (工数 cụ thể chờ team,
   nhưng "có ảnh hưởng lịch" phải nói ngay — dùng khung 納期交渉 của skill `jp-comm` nếu cần).

## Checklist trước khi gửi khách review

- [ ] Đủ 13 mục (mục không áp dụng có ghi 該当なし)?
- [ ] 対象外 (out of scope) viết tường minh?
- [ ] Mọi FR có ID, 1 câu 1 yêu cầu, kiểm thử được, không từ mơ hồ?
- [ ] 非機能 có số + điều kiện đo (không có chữ "nhanh/dễ/linh hoạt" trần)?
- [ ] 前提 trong mục 12 đều đã được khách xác nhận; chưa xác nhận nằm ở mục 13 kèm hạn?
- [ ] Thuật ngữ khớp 100% chữ khách dùng; 用語定義 đủ?
- [ ] Số liệu soát chéo lượt cuối; 改訂履歴 đúng version?
- [ ] Kèm 1 trang tóm tắt "điểm cần quý khách xác nhận" khi gửi?
