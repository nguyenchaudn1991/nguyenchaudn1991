# Q&A管理・課題表 — quản lý câu hỏi & issue với khách

Mục tiêu: không câu hỏi nào rơi rớt, khách trả lời nhanh, mọi 課題 có người cầm + hạn.
Q&A và 課題 là 2 bảng khác nhau — đừng trộn: **Q&A = cần thông tin/quyết định từ khách;
課題 = việc cần giải quyết** (có thể của mình hoặc của khách).

---

## 1. Bảng Q&A chuẩn

| No | 分類 | 質問内容 | 背景・影響 | 希望回答期限 | 優先 | 回答 | ステータス | 回答日 |
|---|---|---|---|---|---|---|---|---|

- **分類:** 仕様 / 環境 / データ / 運用 / その他 — để khách route người trả lời.
- **背景・影響:** vì sao hỏi + không có câu trả lời thì cái gì đứng ("開発着手できません"
  / "◯◯の実装が仮実装になります") — khách cấp cao ưu tiên theo impact.
- **希望回答期限 phải có lý do** gắn với lịch chung (「◯日までに頂けると△△に間に合います」).
- **ステータス:** 未回答 → 回答済 → 確認中 → クローズ. Chỉ close khi mình đã xác nhận
  hiểu đúng (xem mục 3).

## 2. Viết câu hỏi để được trả lời nhanh

1. **1 câu hỏi = 1 vấn đề.** Câu gộp 3 ý sẽ nhận về câu trả lời 1 ý.
2. **Khám phá trước, đóng sau:** chưa biết đủ nhu cầu/option → hỏi mở ngắn. Khi lựa chọn đã
   đầy đủ, đưa A/B + khuyến nghị để khách chọn nhanh:
   「AとBのどちらでしょうか。弊社ではA（理由：…）を想定しています。」
3. **Deemed approval có governance:** chỉ dùng 「ご異論がなければ◯日以降、A案で進めさせて
   いただきます。」khi hai bên đã thống nhất cơ chế này, việc rủi ro thấp + đảo ngược được,
   owner/deadline/timezone rõ. KHÔNG dùng cho nghiệp vụ, tiền, security/compliance; không có
   thỏa thuận trước thì im lặng không phải approval.
4. **Gửi theo nhịp batch** (ví dụ gom đến 16h thứ 3 & thứ 6), trừ câu **blocking** —
   gửi ngay và ghi rõ đang chặn việc gì. Bắn lẻ tẻ từng câu = khách bỏ sót + khó chịu.
5. Quá hạn không trả lời → leo thang theo 催促 ladder trong situations.md (lần 2 nêu
   impact lịch, lần 3 đề xuất 15 phút call).

## 3. Đóng câu hỏi đúng cách (chỗ hay sinh bug nghiệp vụ nhất)

- Khách trả lời mơ hồ → **paraphrase lại rồi mới close:**
  「〜という理解でよろしいでしょうか。」— được xác nhận mới chuyển クローズ.
- **Không sửa/không viết đè** vào ô 回答 của khách — bổ sung thì thêm dòng/ghi chú mới,
  giữ nguyên văn khách viết (audit trail).
- Câu trả lời làm **thay đổi spec** → phản ánh ngay vào bản spec-breakdown (đánh dấu
  ngày + số Q&A tham chiếu: 「Q-12回答により変更」) và báo dev — Q&A đóng mà spec
  không cập nhật là nguồn lệch chuẩn kinh điển.

## 4. Bảng 課題表 chuẩn

| No | 課題 | 影響 | 対応方針 | 担当 | 期限 | ステータス | 更新日 |
|---|---|---|---|---|---|---|---|

- **担当 ghi rõ 弊社/御社 + tên** — 課題 không người cầm là 課題 không bao giờ đóng.
- **影響** viết bằng hệ quả nghiệp vụ/lịch, có số khi được (「対応しない場合、◯◯業務が
  手作業になります」).
- Mỗi MTG định kỳ rà 1 lượt: cập nhật ステータス, 課題 quá hạn phải nêu trong 週次報告
  (xem reporting.md), close phải có evidence (link commit/tài liệu/số Q&A).
- 課題 phát sinh từ chỗ mơ hồ của spec (「別途」「など」…) → sinh ra từ spec-breakdown.md,
  ghi nguồn gốc để truy ngược.

## NG chung

- Hỏi mà không nói vì sao cần (khách không ưu tiên được).
- Danh sách 30 câu chưa phân loại/ưu tiên gửi 1 cục (khách cấp cao sẽ... không đọc).
- Close câu hỏi dựa trên "chắc ý khách là vậy".
- Q&A nằm rải rác trong email/chat không vào bảng — 3 tuần sau không ai tìm lại được.
