# Requirement Analysis — từ yêu cầu thô đến đề xuất có trade-off

## Mục lục

1. [Intake theo định dạng nguồn](#bước-0--intake-theo-định-dạng-nguồn)
2. [Cấu trúc hóa yêu cầu](#bước-1--cấu-trúc-hóa-yêu-cầu)
3. [不明点 & giả định](#bước-2--不明点--giả-định-mục-quyết-định-chất-lượng)
4. [Nghiên cứu giải pháp](#bước-3--nghiên-cứu-giải-pháp)
5. [Bảng so sánh & trade-off](#bước-4--bảng-so-sánh--trade-off)
6. [Tài liệu đầu ra](#bước-5--tài-liệu-đầu-ra)
7. [Checklist trước khi gửi](#checklist-trước-khi-gửi)

Quy trình 5 bước, đầu vào là bất kỳ thứ gì khách gửi, đầu ra là tài liệu phân tích
khách đọc 5 phút là quyết được. Phân tích vốn là việc lặp — được phép quay lại bước trước khi
có thông tin mới, nhưng **không được bỏ kết quả bắt buộc của bước nào** trước khi chốt tài liệu.

---

## Bước 0 — Intake theo định dạng nguồn

| Nguồn | Cách đọc | Bẫy cần tránh |
|---|---|---|
| **.pptx** | Dùng skill pptx để extract text + speaker notes | Thông tin nằm trong diagram/hình → phải render slide ra ảnh xem, đừng chỉ tin text; notes hay chứa ý thật của khách |
| **.md / .html** | Đọc thẳng | HTML: xem cả comment, phần bị ẩn (display:none), bảng lồng nhau |
| **Figma** | Có MCP Figma → dùng; không có → xin khách export PDF/PNG rồi đọc ảnh | Chỉ nhìn happy path trong design — hỏi các trạng thái không vẽ (lỗi, rỗng, loading); annotation nhỏ ngoài lề frame |
| **Backlog note vài dòng** | Đọc + đọc cả ticket liên quan/comment cũ nếu truy cập được | Thường thiếu bối cảnh/điều kiện → trọng tâm dồn vào Bước 2; không tự suy ra phần còn thiếu |
| **Nhiều nguồn trộn nhau** | Đọc hết rồi đối chiếu | Mâu thuẫn giữa các nguồn → liệt kê ra, hỏi khách nguồn nào là mới nhất, không tự chọn |

Đọc xong bắt buộc trả lời được: **khách đang đau ở đâu (業務課題) và vì sao bây giờ (なぜ今)?**

Chưa trả lời được → ghi thành 未決事項 và **hỏi khách ngay**. Trong lúc chờ, vẫn làm tiếp phần
điều tra hiện trạng và khảo sát kỹ thuật (không phụ thuộc câu trả lời đó). Nhưng **không được
chốt 推奨 hay viết 要件定義書** khi chưa biết なぜ今 — thiếu nó thì không có căn cứ xếp ưu tiên.

## Bước 1 — Cấu trúc hóa yêu cầu

Ép mọi yêu cầu thô vào khung sau (mục nào nguồn không có → ghi `記載なし`, đừng bỏ trống):

1. **背景・目的** — bài toán kinh doanh đằng sau, không phải tính năng. "Muốn thêm nút X"
   luôn có một "vì sao" phía sau — tìm nó, vì có khi giải pháp đúng không phải nút X.
2. **要求一覧** — từng yêu cầu 1 dòng, đánh số (R-01, R-02…), phân loại **MUST / WANT**
   theo chữ khách dùng (「必須」「できれば」) — không tự nâng/hạ mức.
3. **非機能要求** — hiệu năng, bảo mật, số lượng user/data, thiết bị, ngôn ngữ.
4. **制約条件** — deadline, ngân sách (nếu khách nói), hệ thống hiện có phải giữ,
   quy định công ty khách.
5. **成功の定義** — làm xong thì đo bằng gì? Khách không nói → tự đề xuất chỉ số và
   đưa vào mục xác nhận.

## Bước 2 — 不明点 & giả định (mục quyết định chất lượng)

- Liệt kê **mọi** điểm chưa rõ thành bảng: `# | 不明点 | 仮の前提（暫定） | ご確認したい事項`.
- Chọn kiểu câu hỏi theo độ rõ: chưa biết đủ nhu cầu/option → hỏi mở ngắn để khám phá;
  khi lựa chọn đã exhaustive → dùng **lựa chọn đóng** để khách trả lời nhanh:
  「AとBのどちらを想定されていますか。弊社としてはAを推奨します（理由：…）」.
  Không ép A/B giả khi solution space còn chưa rõ.
- Nguyên tắc: **phân tích vẫn tiến hành trên 前提 tạm** (ghi rõ ở đầu tài liệu), không dừng
  chờ khách — nhưng mọi kết luận phụ thuộc 前提 nào thì đánh dấu (※前提1による).
- Vòng đời câu hỏi (gửi batch, nhắc, đóng) quản lý theo bảng Q&A của skill `jp-comm`.

## Bước 3 — Nghiên cứu giải pháp

- Điều tra hiện trạng trước (hệ thống hiện có, dữ liệu thật, giới hạn kỹ thuật) — số liệu
  hiện trạng là nền cho mọi so sánh.
- Tìm **2–3 phương án khả thi** thật sự khác nhau về cách tiếp cận (không phải 1 phương án
  + 2 biến thể làm nền). Nếu chỉ tồn tại 1 đường đi khả thi → nói thẳng và chứng minh vì sao
  các đường khác bị loại (案として検討したが除外した理由).
- Mỗi option phải điều tra đủ: cơ chế hoạt động, căn cứ (docs chính thức — trích link/version),
  giới hạn đã biết, ảnh hưởng vận hành, rủi ro. Chỗ nào chưa chắc → `要検証` kèm cách kiểm chứng
  (PoC nhỏ, hỏi vendor…).

## Bước 4 — Bảng so sánh & trade-off

Format chuẩn (khách Nhật đọc bảng trước, đọc văn sau):

| 観点 | 案1: … | 案2: … | 案3: … |
|---|---|---|---|
| 概要 | 1 dòng | 1 dòng | 1 dòng |
| 効果（課題への適合度） | ◎/○/△/× + 1 dòng lý do | | |
| 開発規模感 | 大/中/小 (KHÔNG man-day) | | |
| 運用負荷 | ◎/○/△/× | | |
| リスク | nêu rủi ro chính | | |
| 拡張性 | ◎/○/△/× | | |
| ランニングコスト | định tính hoặc số nếu có căn cứ | | |

- Dưới bảng: **メリット/デメリット** viết rõ thành lời cho từng án — bảng để so nhanh,
  lời để khách 納得 vì sao.
- **推奨案 + 理由** (gắn với 課題 ở Bước 1, không phải "vì công nghệ mới").
- Rủi ro của chính 推奨案 + cách giảm thiểu — tự nói trước khi khách hỏi.

## Bước 5 — Tài liệu đầu ra

Thứ tự cố định (結論ファースト):

1. **サマリー** — 3–5 dòng: 課題 → 推奨案 → xin khách quyết gì, hạn nào.
2. **背景・課題整理** (Bước 1 rút gọn)
3. **前提・仮定** (Bước 2)
4. **各案の比較** (Bước 4 — bảng + メリデメ)
5. **推奨案の詳細** (cơ chế, ví dụ dễ hiểu cho người không kỹ thuật, flow 現状→改善 nếu có)
6. **リスクと対策**
7. **ご確認事項** (câu hỏi dạng lựa chọn)
8. **補足** (chi tiết kỹ thuật cho đội kỹ thuật phía khách, nếu có)

Kênh gửi: comment Backlog (ngắn) / file .md / deck 技術検討会 / trang web report —
cùng nội dung, đổi vỏ theo kênh (có skill trình bày chuyên dụng trong môi trường thì dùng).

## Checklist trước khi gửi

- [ ] サマリー đứng đầu, khách đọc 5 phút nắm được cần quyết gì?
- [ ] Mọi số liệu có nguồn/điều kiện đo, đã soát chéo 1 lượt cuối?
- [ ] Không còn khẳng định nào thiếu căn cứ (未確認/調査中 đã đánh dấu đủ)?
- [ ] Theo đúng luật số phương án (SKILL.md nguyên tắc 4): có ≥ 2 án khả thi thì so sánh đủ,
      メリデメ cả 2 chiều cho TỪNG án (kể cả án mình không thích); chỉ có 1 án khả thi thì đã
      ghi rõ các án đã cân nhắc và lý do loại?
- [ ] Không lộ man-day; 規模感 chỉ ở mức 大/中/小?
- [ ] Người không kỹ thuật đọc thân bài có hiểu không (jargon đã có giải thích/analogy)?
- [ ] Thuật ngữ khớp 100% với từ khách dùng trong tài liệu gốc?
