---
name: jp-requirement
description: >-
  Use when handling requirements for Japanese clients: (1) phân tích yêu cầu /
  要件分析 / 要件整理 / nghiên cứu giải pháp / đề xuất phương án — from any source
  (pptx, .md, html, Figma, Backlog notes); (2) viết 要件定義書 / requirement
  definition document; (3) dịch & "nhai nhỏ" spec Nhật cho team dev VN — 仕様書,
  dịch spec, spec breakdown. Do NOT trigger for: 工数見積 / estimates and 議事録
  (company process, owned by another role); situation-based client communication —
  障害報告/催促/納期交渉/謝罪/依頼, Q&A管理, 週次報告 (→ skill jp-comm).
allowed-tools: Read, AskUserQuestion
---

# JP Requirement — phân tích yêu cầu → 要件定義書 → spec cho dev

Pipeline yêu cầu cho công việc DM/BrSE với khách Nhật cấp cao, không sâu kỹ thuật:
nhận yêu cầu mọi định dạng → phân tích + đề xuất options → chốt thành 要件定義書 →
nhai nhỏ cho team dev VN.

## Routing

| Việc | File PHẢI load |
|---|---|
| Phân tích yêu cầu / nghiên cứu giải pháp / đề xuất phương án + trade-off | [references/requirement-analysis.md](references/requirement-analysis.md) |
| Viết / review 要件定義書 | [references/yoken-teigi.md](references/yoken-teigi.md) |
| Dịch & nhai nhỏ spec Nhật cho dev VN | [references/spec-breakdown.md](references/spec-breakdown.md) |

Không load file không cần. Giao tiếp tình huống (báo bug, nhắc, deadline…), bảng Q&A,
báo cáo tuần → skill `jp-comm`. Trình bày kết quả thành deck 技術検討会 → skill
`meo-pptx`; thành trang web report → skill `premium-web` (type report).

## Nguyên tắc cốt lõi

1. **結論ファースト.** Kết luận/đề xuất/điều cần khách quyết đứng đầu tài liệu.
2. **Mọi khẳng định có căn cứ.** Số liệu + nguồn + điều kiện đo; chưa xác nhận →
   `未確認`/`調査中`/`〜と想定` — **cấm đoán rồi trình bày như sự thật**.
3. **Mọi giả định nói to:** liệt kê ở mục 前提. Chưa hiểu nhu cầu/solution space → hỏi mở
   ngắn; khi lựa chọn đã đủ → dùng A/B + khuyến nghị. Giả định ngầm là nguồn số 1 của làm-lại.
4. **Không trình bày 1 phương án như thể không có lựa chọn nào khác.** Luật thống nhất
   (áp cho cả 3 file reference — không có ngoại lệ):
   - Có **≥ 2 phương án khả thi khác nhau đáng kể về cách tiếp cận** → so sánh đủ, mỗi án
     có メリット/デメリット cả hai chiều, kèm 推奨 và lý do. Khách quyết, mình tư vấn.
   - Chỉ **1 đường đi khả thi** → nói thẳng là chỉ có 1, và **liệt kê các phương án đã cân
     nhắc rồi loại + lý do loại** (案として検討したが除外した理由). Đây vẫn là so sánh —
     chỉ khác ở chỗ kết quả đã rõ.
   - Cấm: đưa 1 án mà không cho khách thấy mình đã xét gì; và cấm độn "án làm nền" chỉ để
     đủ số lượng (1 án thật + 2 biến thể yếu = thao túng lựa chọn, không phải tư vấn).
5. **Không đưa 工数/estimate** khi chưa bàn team — 規模感 chỉ ở mức 大/中/小,
   ghi 「工数・スケジュールは別途ご提示します」.
6. **Viết cho khách 納得:** analogy/ví dụ trước, jargon sau (kèm giải thích 1 dòng);
   chi tiết kỹ thuật xuống 補足.
7. **Mirror + normalize vocabulary:** giữ nguyên source term để trace và giao tiếp với khách;
   đồng thời lập 用語集 với normalized term/định nghĩa. Thuật ngữ sai, mơ hồ hoặc mâu thuẫn
   phải được flag và hỏi lại, không âm thầm sửa nghĩa cũng không sao chép mơ hồ xuống dev.
8. **Số liệu soát chéo lượt cuối** trước khi gửi — 1 số sai = mất 信頼 cả tài liệu.
9. **Thứ tự ưu tiên nguồn** — khi các nguồn mâu thuẫn, KHÔNG tự chọn cái nào đúng:

   | Ưu tiên | Nguồn |
   |---:|---|
   | 1 | Hợp đồng / 決定事項 đã ký hoặc đã được 承認 chính thức |
   | 2 | 要件定義書 bản đã 承認 mới nhất |
   | 3 | Mail/văn bản chính thức từ người có thẩm quyền quyết |
   | 4 | 議事録 đã được khách xác nhận |
   | 5 | Chat/trao đổi miệng/ghi chú cá nhân |

   Mâu thuẫn giữa hai nguồn **cùng cấp**, hoặc nguồn cấp thấp mâu thuẫn nguồn cấp cao →
   **ghi vào 課題表 và hỏi người có thẩm quyền**, không im lặng chọn bên nào. Ghi rõ trong
   tài liệu là đang chờ chốt (`※未決 — 課題表 #N`).
   Thứ tự này có thể cấu hình lại theo quy ước của từng dự án — nhưng phải **thống nhất
   trước và ghi ra**, không đổi giữa chừng.

## Common mistakes

| Sai lầm | Sửa |
|---------|-----|
| Trình bày 1 phương án "tốt nhất" | Theo nguyên tắc 4: có ≥2 án khả thi thì so sánh đủ; chỉ 1 án thì ghi rõ đã loại án nào và vì sao |
| Đoán chỗ thiếu thông tin rồi làm tiếp | Ghi 前提 tạm; hỏi mở nếu chưa hiểu nhu cầu, A/B khi option đã đủ; kết luận phụ thuộc phải đánh dấu ※前提 |
| Kèm man-day cho từng option | Chỉ 規模感 大/中/小; 工数 chờ bàn team |
| Viết yêu cầu bằng từ mơ hồ (など・適宜…) | Bảng bẫy trong spec-breakdown.md áp cho cả chiều mình viết |
| 要件定義書 sửa im lặng sau khi khách 承認 | Mọi thay đổi qua 変更管理: version + 変更前→変更後 + lý do |
| Dịch spec word-by-word cho dev | Dịch ý + DoD từng mục + đánh dấu ※判断 chỗ mình phán đoán |
