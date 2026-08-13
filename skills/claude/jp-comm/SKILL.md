---
name: jp-comm
description: >-
  Use when writing Japanese business communication to clients: (1) situations —
  障害報告 / báo bug cho khách, 催促 / nhắc khách chưa trả lời, 納期交渉 / thương lượng
  deadline, 謝罪 / xin lỗi, 依頼 / nhờ khách; (2) Q&A管理・課題表 — tạo/quản lý bảng
  câu hỏi và issue với khách; (3) báo cáo — 納品報告, リリース連絡, 週次報告 / weekly
  report. Keywords: 敬語, viết mail khách Nhật, soạn tin nhắn khách. Do NOT trigger
  for: 議事録 and 工数見積 (company process, owned by another role); requirement
  analysis / 要件定義 (→ skill jp-requirement).
allowed-tools: Read, Write, AskUserQuestion, Skill
---

# JP Comm — giao tiếp chuẩn manner với khách Nhật cấp cao

Soạn giao tiếp tiếng Nhật cho công việc DM/BrSE: đúng khung từng tình huống, đúng mức
敬語, số liệu chuẩn. Đối tượng đọc là **quản lý cấp cao, không sâu kỹ thuật**.

## Routing

| Việc | File PHẢI load |
|---|---|
| Tình huống: 障害報告 · 催促 · 納期交渉 · 謝罪 · 依頼 | [references/situations.md](references/situations.md) |
| Bảng Q&A / 課題表 với khách (tạo, viết câu hỏi, vận hành, đóng) | [references/qa-management.md](references/qa-management.md) |
| 納品報告 · リリース連絡 · 週次報告 | [references/reporting.md](references/reporting.md) |

Không load file không cần. Phân tích yêu cầu / viết 要件定義書 / dịch spec → skill
`jp-requirement`, không phải skill này.

Trước khi viết, xác định **kênh** (email / Backlog comment / chat / tài liệu), người nhận,
quan hệ, mức khẩn cấp và việc người đọc cần làm. Email cần mở/kết đầy đủ; Backlog cần ngắn,
trace được; chat cần gọn nhưng vẫn giữ facts, owner và next update. Không copy nguyên một
register cho mọi kênh.

## Nguyên tắc cốt lõi (áp cho mọi văn bản gửi khách)

1. **結論ファースト.** Điều khách cần biết/quyết định đứng đầu.
2. **Mọi khẳng định có căn cứ.** Số liệu kèm nguồn + điều kiện; chưa xác nhận → ghi
   `未確認`/`調査中`, **cấm đoán rồi viết như sự thật**. 1 số sai = mất 信頼 cả văn bản.
3. **Số liệu soát chéo lượt cuối trước khi gửi:** đơn vị, mốc thời gian (JST), tổng khớp
   từng dòng, nhất quán giữa các chỗ xuất hiện (báo cáo = 課題表 = Backlog).
4. **Viết để khách 納得:** ví dụ/analogy trước, thuật ngữ sau (kèm 1 dòng giải thích);
   chi tiết kỹ thuật đẩy xuống cuối hoặc phụ lục.
5. **Tin xấu báo sớm, kèm đối sách.** Báo sớm **những gì đã xác nhận**, ghi rõ phần chưa rõ và
   hẹn giờ update — chứ không đánh đổi độ chính xác lấy tốc độ. Đoán sai rồi đính chính còn
   mất 信頼 hơn báo chậm 1 tiếng.
6. **Ngôn ngữ:** tiếng Nhật です・ます調, không dấu chấm than, không emoji, dùng đúng
   thuật ngữ khách đang dùng.
7. **Chọn kiểu câu hỏi theo độ rõ của vấn đề.** Chưa hiểu nhu cầu/solution space → hỏi mở
   ngắn để khám phá. Đã có các lựa chọn đầy đủ → đóng A/B + khuyến nghị để khách quyết nhanh.
   Có ≥2 phương án khả thi khác nhau đáng kể thì trình bày trade-off; chỉ có 1 thì nói rõ
   các phương án đã cân nhắc và lý do loại, không độn option yếu.
8. **Không đưa 工数/estimate** khi chưa bàn team — 「工数は別途ご提示します」.

## Soát trước khi gửi (bắt buộc — mail gửi đi không rút lại được)

Chạy hết checklist này trước MỌI văn bản gửi ra ngoài. Sai một mục ở đây gây thiệt hại lớn
hơn mọi lỗi 敬語 cộng lại.

- [ ] **Người nhận đúng chưa?** Kiểm từng địa chỉ To/CC. Cảnh giác autocomplete chọn nhầm
      người trùng tên — đặc biệt khi có nhiều khách hàng cùng lúc.
- [ ] **BCC hay CC?** Gửi nhiều khách không quen nhau → BCC. Lộ danh sách địa chỉ của khách
      này cho khách khác là sự cố rò rỉ thông tin, không phải lỗi nhỏ.
- [ ] **Reply-All có cần thiết không?** Nội dung nội bộ/nhạy cảm → trả lời riêng.
- [ ] **File đính kèm:** đúng file, **đúng version**, đã mở ra xem lại. Excel còn sheet ẩn/
      comment/lịch sử sửa không? PDF còn vết redact giả (bôi đen nhưng copy ra vẫn đọc được)?
- [ ] **Dữ liệu của khách khác:** ảnh chụp màn hình, log, câu query, tên miền, tên dự án của
      khách A **không được lọt** vào tài liệu gửi khách B. Soi kỹ screenshot trước khi gửi.
- [ ] **Thông tin nội bộ:** credential, token, URL staging/admin, đường dẫn server, tên nhân
      sự nội bộ, ước lượng chi phí nội bộ — đã bỏ hết chưa?
- [ ] **Dữ liệu cá nhân:** có PII của người dùng cuối trong log/mẫu dữ liệu không? Che hoặc
      thay bằng dữ liệu giả trước khi gửi.
- [ ] **Đúng kênh:** khách quy định trao đổi qua Backlog/kênh chỉ định → không tự chuyển sang
      mail cá nhân hay chat ngoài chỉ vì tiện.
- [ ] **Số liệu đã soát chéo** (nguyên tắc 3) và **không có ETA/工数 tự bịa** (nguyên tắc 8).

Tin nhắn báo sự cố gấp cũng phải qua checklist này — vội là lúc dễ gửi nhầm nhất.

## Common mistakes

| Sai lầm | Sửa |
|---------|-----|
| Điều tra xong mới báo sự cố | 第一報 ngay khi phát hiện, nguyên nhân 調査中 (situations.md) |
| 了解しました với khách | 承知いたしました (bảng 敬語 trong situations.md) |
| Nhắc khách kiểu trách móc | Impact theo lịch + cushion words, leo thang 3 nấc |
| Xin lỗi kèm bào chữa cùng câu | 謝罪 và nguyên nhân tách mục riêng |
| Số Backlog đưa thẳng vào report | Kiểm tay trước — tracking tool hay lệch thực tế |
| Hỏi mở dù solution space đã rõ / hỏi đóng khi còn chưa hiểu nhu cầu | Khám phá bằng câu hỏi mở ngắn trước; chỉ đóng A/B + khuyến nghị khi lựa chọn đã đủ |
