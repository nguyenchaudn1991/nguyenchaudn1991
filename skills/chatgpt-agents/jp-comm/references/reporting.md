# Reporting — 納品報告・リリース連絡・週次報告

3 loại báo cáo định kỳ/nghiệp vụ. Chung: 結論ファースト, số liệu tự kiểm chứng trước khi
gửi (số lấy từ Backlog/tool phải xác nhận tay — đừng tin mù dữ liệu tracking), tiếng Nhật
です・ます, không dấu chấm than.

---

## 1. 納品報告 — báo cáo giao hàng

### Cấu trúc (đủ 5 mục)
1. **納品物一覧** — bảng: tên file/URL | version | ngày | cách lấy (link, mật khẩu gửi kênh riêng).
2. **対応内容サマリー** — làm những gì, đối chiếu với danh sách đã cam kết (từng mục ○ done).
3. **テスト結果** — số case thực hiện / pass / fail, môi trường test, link evidence.
   Có fail còn lại → ghi rõ vì sao chấp nhận giao (kèm thoả thuận nếu có).
4. **既知の事象・制限事項** — **không giấu**: hiện tượng đã biết, điều kiện tái hiện,
   workaround, kế hoạch xử lý. Khách tự phát hiện sau sẽ tệ hơn nhiều lần mình tự khai.
5. **ご確認のお願い** — xin khách 検収: kiểm cái gì, đến ngày nào, sau ngày đó xử lý
   thế nào (「◯日までにご指摘がない場合、検収完了とさせていただきます」— chỉ dùng khi
   quy trình 2 bên đã thống nhất kiểu này).

### NG
- Giao xong mới báo test "OK hết" không số liệu — khách cấp cao không tin chữ OK trần.
- File đặt tên tùy hứng — theo quy ước version (`_v1.2_YYYYMMDD`), khớp với 納品物一覧.

## 2. リリース連絡 — thông báo release

### 事前連絡 (theo change calendar/SLA của dự án; chưa có thì đề xuất gửi trước ≥ 2–3 ngày làm việc và xin xác nhận)
- 日時: ngày giờ **JST** + thời lượng dự kiến.
- 対象・内容: release cái gì, cho hệ thống/màn hình nào.
- 影響: user có bị gián đoạn không, downtime bao lâu, trong lúc đó hiện tượng gì
  (「◯時〜◯時の間、ログインできません」).
- 依頼事項: khách cần làm gì (tránh thao tác X trong khung giờ, xóa cache…).
- 中止条件・切り戻し: điều kiện hoãn và phương án rollback tóm tắt 1–2 dòng —
  khách cấp cao yên tâm khi thấy có đường lui.

### 完了報告 (ngay sau release)
- Kết quả: hoàn thành lúc mấy giờ, 確認内容 đã kiểm những gì (checklist ○).
- Trạng thái theo dõi: đang monitor gì, đến bao giờ.
- Kênh liên hệ khi phát hiện bất thường.
- **Có sự cố trong release → chuyển ngay sang khung 障害報告** (situations.md mục 1),
  không viết lẫn vào báo cáo release.

## 3. 週次報告 — báo cáo tuần

### Cấu trúc
1. **全体サマリー (1 dòng):** 順調 / 一部遅延 / 要相談 — kèm 1 câu lý do. Đây là dòng
   duy nhất chắc chắn được đọc; viết cuối cùng, sau khi xong các mục dưới.
2. **今週の実績:** việc hoàn thành kèm số (done x/y task, % tiến độ so kế hoạch) —
   đối chiếu được với tuần trước (trend), không chỉ chụp ảnh tuần này.
3. **来週の予定:** đầu việc + mốc.
4. **課題・リスク:** từ 課題表 (qa-management.md) — chỉ nêu mục cần khách biết/quyết,
   mỗi mục kèm "cần khách làm gì, đến ngày nào". Không có gì → ghi 「特になし」 rõ ràng.
5. **Q&A状況:** số câu đang chờ khách trả lời + câu quá hạn (link bảng Q&A).

### Nguyên tắc
- **Tin xấu báo sớm kèm đối sách** — tuần nào cũng 順調 rồi tuần cuối 要相談 là mất 信頼
  nặng nhất trong nghề này. Thấy rủi ro từ tuần N → xuất hiện trong report tuần N.
- Số liệu phải khớp chéo: con số trong 週次報告 = 課題表 = Backlog. Lệch 1 chỗ là khách
  nghi toàn bộ. **Số từ Backlog phải kiểm tay trước khi dùng** (ngày tháng/status trên
  tool không phải lúc nào cũng được cập nhật đúng).
- Format cố định tuần này qua tuần khác — khách đọc 30 giây vì biết chỗ nào có gì.
