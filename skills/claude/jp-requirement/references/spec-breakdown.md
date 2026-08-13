# Spec Breakdown — dịch & "nhai nhỏ" spec Nhật cho team dev VN

Đầu vào: 要件定義書 / 仕様書 / 設計書 / ticket Backlog tiếng Nhật.
Đầu ra: working contract tiếng Việt đủ rõ để dev triển khai hằng ngày, nhưng **không thay thế
source gốc**. Mọi mục phải trace ngược được; chỗ dịch/phán đoán rủi ro cao cần bilingual
review và authority xác nhận trước khi triển khai phần bị ảnh hưởng.

---

## Nguyên tắc

1. **Dịch ý + ngữ cảnh nghiệp vụ, không dịch từng chữ.** Nhưng thuật ngữ nghiệp vụ
   giữ nguyên tiếng Nhật kèm giải thích — vì lúc trao đổi ngược với khách phải dùng
   đúng từ của khách (mirror vocabulary).
2. **Traceability:** mỗi mục trong bản dịch đánh số khớp mục gốc (`§4.2 → 4.2`).
   Dev thắc mắc → trỏ ngược được về đúng đoạn spec gốc trong 5 giây.
3. **Chỗ nào mình phán đoán khi dịch → đánh dấu `※判断`** kèm cách hiểu đã chọn.
   Đây là những chỗ rủi ro nhất — reviewer và khách phải soi được.
4. **Không bỏ sót "chữ nhỏ":** chú thích cuối trang, ghi chú trong ngoặc, nội dung
   trong bảng/hình, comment trong file — spec Nhật hay giấu điều kiện quan trọng ở đó.

## Bẫy ngôn ngữ spec Nhật (bảng soi bắt buộc)

### Từ mơ hồ — gặp là biến thành câu hỏi cho khách (đưa vào bảng Q&A — skill `jp-comm`)
| Từ | Vì sao nguy hiểm | Hành động |
|---|---|---|
| 「など」「等」 | danh sách không đóng — còn gì nữa? | Hỏi danh sách đầy đủ, hoặc chốt "chỉ những mục đã liệt kê" |
| 「適宜」「必要に応じて」 | "tùy tình huống" — ai quyết, tiêu chí gì? | Hỏi tiêu chí cụ thể |
| 「基本的に」「原則として」 | tức là CÓ ngoại lệ — ngoại lệ nào? | Hỏi danh sách ngoại lệ |
| 「別途」 | "sẽ có sau" — bao giờ, ai đưa? | Ghi vào 課題表 kèm deadline |
| 「〜を想定」 | giả định của khách, chưa chắc là yêu cầu | Xác nhận là MUST hay chỉ là ví dụ |

### Từ chỉ mức bắt buộc — dịch sai là dev làm sai scope
| Spec gốc | Mức | Dịch |
|---|---|---|
| 〜すること / 〜とする | BẮT BUỘC | "Phải…" |
| 〜が望ましい | khuyến nghị | "Nên… (không bắt buộc — confirm nếu ảnh hưởng công số)" |
| 〜してもよい / 〜も可 | tùy chọn | "Được phép…" |
| 〜しないこと / 〜不可 | CẤM | "Không được…" |

### Quy ước dữ liệu Nhật — chuyển đổi phải ghi chú tường minh
- Ngày: 和暦 (令和6年 = 2024)? YYYY/MM/DD? — chốt format lưu và format hiển thị riêng.
- 全角/半角: field nào bắt buộc half-width (mã, số điện thoại), field nào cho full-width — spec Nhật rất hay có yêu cầu này, dev VN rất hay bỏ qua.
- Tiền: làm tròn thuế (切り捨て/切り上げ/四捨五入) — sai 1 yên là bug nghiệp vụ.
- 締め日 (ngày chốt), 営業日 vs 暦日 (ngày làm việc vs ngày lịch) — hỏi lịch nghỉ khách nếu liên quan.

## Cấu trúc bản "nhai nhỏ" cho dev

1. **Bối cảnh nghiệp vụ (3–5 dòng):** khách là ai, tính năng này ai dùng, để làm gì —
   dev hiểu "tại sao" thì tự xử lý edge case đúng hướng hơn.
2. **Yêu cầu theo mục** (đánh số khớp gốc), mỗi mục:
   - **Input → Xử lý → Output** rõ ràng
   - **Điều kiện biên & ngoại lệ** (kể cả suy ra từ "chữ nhỏ")
   - **DoD** — làm xong kiểm thế nào là đạt. Số/ngưỡng phải đến từ source hoặc owner đã
     xác nhận; chưa có thì ghi `TBD — owner/date`, không tự tạo số cho đủ testability.
3. **Out of scope:** những gì spec KHÔNG yêu cầu (chống làm thừa — dev hay "tiện tay").
4. **用語集:** JP | đọc | nghĩa VI | ghi chú ("khi hỏi khách dùng đúng từ này").
5. **Danh sách câu hỏi đang mở** (từ bảng bẫy ở trên) + trạng thái — mục nào bị chặn
   bởi câu hỏi nào ghi rõ, dev biết phần nào làm được ngay, phần nào chờ.

## Tự kiểm trước khi đưa dev

- [ ] Đọc bản dịch với tư cách dev: có mục nào 2 cách hiểu không?
- [ ] Mọi `※判断` đã liệt kê và (nếu rủi ro cao) đã hỏi khách?
- [ ] Số, đơn vị, format ngày, 全角/半角 đã có ghi chú chuyển đổi?
- [ ] Bảng/hình trong spec gốc đã đọc hết chưa (không chỉ dịch phần văn)?
- [ ] Out of scope đã ghi? DoD từng mục đã có?
