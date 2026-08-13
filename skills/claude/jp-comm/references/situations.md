# Situations — 5 tình huống giao tiếp với khách Nhật cấp cao

## Mục lục

1. [障害報告](#1-障害報告--báo-bugsự-cố-tình-huống-nặng-nhất-cấu-trúc-chặt-nhất)
2. [催促・リマインド](#2-催促リマインド--nhắc-khách-chưa-trả-lời)
3. [納期交渉](#3-納期交渉--thương-lượng-deadline)
4. [謝罪](#4-謝罪--xin-lỗi-sự-cố--sai-sót)
5. [依頼](#5-依頼--nhờ-khách-làm-việc--cung-cấp-thông-tin)
6. [Bảng 敬語 tra nhanh](#bảng-敬語-tra-nhanh-lỗi-hay-gặp-với-khách)

Mỗi tình huống: cấu trúc bắt buộc → mức 敬語 → khung mẫu → điều cấm (NG).
Chung cho cả 5: です・ます調, không dấu chấm than, không emoji, số liệu soát chéo trước khi gửi.

---

## 1. 障害報告 — báo bug/sự cố (tình huống nặng nhất, cấu trúc chặt nhất)

### Nguyên tắc thời điểm: báo theo 3 nhịp, KHÔNG đợi điều tra xong
- **第一報** (ngay khi phát hiện, theo incident SLA đã thống nhất): chỉ ghi facts đã xác nhận
  + phạm vi ảnh hưởng tạm biết + 「原因は調査中です」+ **giờ cụ thể** của lần báo tiếp.
  Báo sớm không có nghĩa là đoán; unknown phải được đánh dấu rõ.
- **続報**: cập nhật theo đúng giờ đã hẹn, kể cả khi chưa có gì mới (「進展なし、引き続き調査中」).
- **最終報**: đầy đủ theo cấu trúc dưới.

### Cấu trúc 最終報 (bắt buộc đủ 7 mục, đúng thứ tự)
1. **事象** — hiện tượng gì, phát sinh từ khi nào đến khi nào (ngày giờ cụ thể, timezone),
   phát hiện bằng cách nào.
2. **影響範囲** — ai/bao nhiêu user/bao nhiêu data bị ảnh hưởng, **con số cụ thể** + cách đếm;
   phần ĐÃ xác nhận không ảnh hưởng cũng ghi rõ (影響なしと確認済み: …).
3. **暫定対応** — đã xử lý ngay những gì, từ mấy giờ, hiện trạng đã ổn định chưa.
4. **直接原因** — nguyên nhân trực tiếp gây ra hiện tượng (VD: query X thiếu điều kiện Y).
5. **根本原因** — vì sao lỗi đó lọt được đến production (VD: thiếu test case cho pattern Y,
   review không có checklist mục này). Đào đến tầng quy trình, không dừng ở tầng code.
6. **恒久対策** — sửa tận gốc: nội dung + ngày hoàn thành dự kiến.
7. **再発防止策** — thay đổi quy trình/cơ chế để loại lỗi cùng họ (thêm test tự động,
   thêm mục checklist, thêm monitor/alert) + ngày áp dụng.

### 敬語 & tone
- Mở đầu + kết thúc có 謝罪 đúng mức, ngắn gọn:
  「この度は多大なご迷惑をおかけし、誠に申し訳ございません。」
- Thân bài = **sự thật + số liệu, văn trung tính** — không bào chữa, không cảm xúc.
- Phần nguyên nhân: **断定** (「〜が原因です」) hoặc 「調査中」— **cấm** 「たぶん」「〜と思います」.

### NG
- Đổ lỗi (cho môi trường, cho bên thứ ba, cho... khách) — kể cả khi đúng, cách viết phải là
  sự kiện khách quan, không phải quy trách nhiệm.
- Gộp 直接原因 và 根本原因 làm một — khách cấp cao soi đúng chỗ này.
- 再発防止策 chung chung kiểu 「注意します」「気をつけます」 — phải là cơ chế, không phải lời hứa.

---

## 2. 催促・リマインド — nhắc khách chưa trả lời

### Cấu trúc: cushion → nhắc lại yêu cầu → impact theo deadline → giảm gánh nặng trả lời
- Thang leo (escalation ladder):
  - **Lần 1** (quá hạn nhẹ): nhắc nhẹ, kèm lại nội dung cần trả lời để khách khỏi lục mail cũ.
  - **Lần 2**: nêu **impact khách quan theo lịch** — không trách người:
    「◯月◯日までにご回答いただけない場合、リリースが◯日程度後ろ倒しになる見込みです。」
  - **Lần 3**: đề xuất đổi kênh — 「お電話または15分ほどのお打ち合わせでご相談させて
    いただくことも可能です。」
- Khi lựa chọn đã đầy đủ, kèm phương án A/B để trả lời trong 1 phút. Có thể dùng
  「ご異論がなければA案で進めさせていただきます（◯日まで）」chỉ khi cơ chế deemed approval
  đã được hai bên thống nhất, việc rủi ro thấp + đảo ngược được, owner/deadline/timezone rõ.
  Nếu chưa có governance đó, im lặng **không phải** approval.

### 敬語 mẫu
「お忙しいところ恐れ入ります。◯月◯日にご相談いたしました件につきまして、
その後いかがでしょうか。」

### NG
- 「まだですか」「早くお願いします」— mọi cách viết đọc ra vị trách móc.
- Nhắc mà không đính kèm lại nội dung gốc (bắt khách tự đi tìm).

---

## 3. 納期交渉 — thương lượng deadline

### Nguyên tắc: báo NGAY khi thấy rủi ro trễ (không đợi chắc chắn trễ), và đến bàn đàm phán bằng options — không bằng lời xin.
### Cấu trúc
1. **Kết luận trước:** 「◯◯の影響により、当初予定の◯月◯日でのリリースが困難な見込みです。」
2. **Nguyên nhân khách quan + số liệu:** tiến độ hiện tại (% + căn cứ đếm), việc phát sinh là gì,
   ảnh hưởng bao nhiêu ngày công.
3. **2–3 options** (có skill `jp-requirement` thì dùng đúng format bảng so sánh của nó):
   - 案1: giữ deadline, giảm scope (nêu rõ cắt gì, cắt xong ảnh hưởng gì)
   - 案2: lùi deadline giữ nguyên scope (lùi đến ngày nào, căn cứ tính)
   - 案3: chia 2 đợt release (đợt 1 phần lõi đúng hạn, đợt 2 phần còn lại)
4. **推奨 + lý do**, và xin khách quyết trước ngày ◯ (nêu lý do vì sao cần quyết trước ngày đó).

### NG
- Hứa deadline mới khi chưa bàn với team (vi phạm nguyên tắc estimate của skill).
- Nêu nguyên nhân kiểu than khổ (nhân sự ốm, bận việc khác) mà không kèm con số và đối sách.
- Đợi sát ngày mới báo — thời điểm báo quan trọng hơn nội dung báo.

---

## 4. 謝罪 — xin lỗi sự cố / sai sót

### Cấu trúc: 謝罪 → 事実 → 原因 → 対策 → 再発防止 → 謝罪 kết
(Sự cố kỹ thuật → dùng nguyên khung 障害報告 mục 1; mục này cho sai sót giao tiếp/tài liệu/chậm trễ.)

### Chọn đúng mức — xin lỗi quá đà cho việc nhỏ làm mất giá trị lời xin lỗi việc lớn:
| Mức | Dùng khi | Câu |
|---|---|---|
| Nhẹ | gửi nhầm file, lỗi typo trong tài liệu, trả lời trễ | 「失礼いたしました。」/「申し訳ございません。」 |
| Trung | sai số liệu đã gửi, trễ hạn nội bộ | 「大変申し訳ございません。」+ nguyên nhân + bản sửa |
| Nặng | sự cố ảnh hưởng nghiệp vụ khách, sai cam kết | 「多大なご迷惑をおかけしましたこと、深くお詫び申し上げます。」+ đủ khung 5 mục |

### Quy tắc vàng
- **Xin lỗi và bào chữa không đứng chung 1 câu.** Nguyên nhân trình bày ở mục riêng,
  dạng sự kiện khách quan.
- Sai số liệu đã gửi → gửi bản đính chính NGAY kèm bảng 「誤 → 正」 rõ ràng, không sửa im lặng.

---

## 5. 依頼 — nhờ khách làm việc / cung cấp thông tin

### Cấu trúc: lý do → nội dung cụ thể → hạn + lý do của hạn → giảm gánh nặng
1. **Vì sao cần:** 「◯◯を進めるにあたり、△△のご確認が必要となります。」
2. **Cần chính xác cái gì:** liệt kê đánh số, mỗi mục 1 việc, kèm format mong muốn
   (「Excelの3列目にご記入ください」) — khách không phải đoán.
3. **Hạn + lý do hạn:** 「◯月◯日までにいただけますと、予定どおり△△に着手できます。」
   — hạn gắn với lợi ích của khách, không phải mệnh lệnh.
4. **Giảm gánh nặng:** đính kèm template điền sẵn được 80%, hoặc đưa lựa chọn A/B,
   hoặc 「たたき台を作成しましたので、修正点のみご指摘ください」(mình làm nháp, khách chỉ sửa).

### 敬語 mẫu
「お手数をおかけしますが、◯◯をご確認いただけますと幸いです。」
「ご多忙のところ恐縮ですが、何卒よろしくお願いいたします。」

### NG
- 「〜してください」 trần (mệnh lệnh) → 「〜いただけますと幸いです」「〜いただけますでしょうか」.
- Nhờ 1 email 5 việc không hạn — tách việc, mỗi việc 1 hạn.

---

## Bảng 敬語 tra nhanh (lỗi hay gặp với khách)

| Tình huống | NG (suồng sã / sai) | Đúng với khách |
|---|---|---|
| Đã hiểu/nhận | 了解しました | 承知いたしました / かしこまりました |
| Xem tài liệu khách | 見ました | 拝見いたしました |
| Nói/báo | 言います | 申し上げます |
| Làm | やります | いたします / 対応いたします |
| Hỏi | 聞きたいです | お伺いしたいのですが / ご教示いただけますでしょうか |
| Biết rồi | 知っています | 存じております |
| Công ty mình / khách | うち / そちら | 弊社 / 御社（貴社 trong văn bản） |
| Gửi kèm | 送ります | お送りいたします / 添付いたします |
| "OK không?" | いいですか | よろしいでしょうか |
| Từ chối/không làm được | できません | 難しい状況です。代替案として〜はいかがでしょうか (luôn kèm phương án thay thế) |
