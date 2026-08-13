# Type 1 — Report Site (trang báo cáo / giải trình / đề xuất cho khách Nhật)

Trang web tĩnh để khách Nhật **đọc – hiểu – quyết định**: báo cáo tiến độ, giải trình sự cố,
đề xuất kỹ thuật, so sánh phương án. Đây là "bản web" của deck 技術検討会/課題検討会 —
cùng house style với bộ meo-pptx để khách thấy nhất quán.

**Luôn load kèm:** japanese-quality.md (audience mặc định là Nhật).

---

## 1. Định vị & nguyên tắc

- **Người đọc:** manager/kỹ sư Nhật, đọc trên PC công ty (Windows) hoặc in ra giấy.
- **結論ファースト:** kết luận/đề xuất đứng đầu trang, chi tiết giải trình theo sau.
- **1 trang = 1 chủ đề.** Nhiều chủ đề → mục lục + section rõ, không tách nhiều trang.
- **Mật độ cao nhưng sạch:** khách Nhật muốn đủ dữ liệu trong 1 màn nhìn — dày được, miễn canh chuẩn (đây là ngoại lệ của định hướng "Zen" — trang report ưu tiên mật độ như dashboard).
- **0 JS hoặc gần 0:** chỉ cho phép JS nhỏ cho TOC highlight; không animation trang trí.
- **1 file HTML tự chứa** (CSS inline trong `<head>`, SVG inline) → gửi qua Backlog/Slack, mở là chạy, không cần server.

## 2. House style (khớp meo-pptx)

```css
:root {
  --navy: #0E2240;        /* nền header, heading chính */
  --red: #C00000;         /* accent duy nhất: cảnh báo, số liệu quan trọng, 改善 */
  --ice: #EAF1F8;         /* nền card / hàng bảng xen kẽ */
  --ink: #1a1a1a;         /* body text */
  --line: #C9D4E0;        /* kẻ bảng, border */
  --ok: #2E7D32;          /* chỉ dùng cho trạng thái ○/OK khi cần */
}
body {
  font-family: "Hiragino Kaku Gothic ProN", Meiryo, "Noto Sans JP", sans-serif;
  color: var(--ink); line-height: 1.7; font-size: 15px;
}
table { font-variant-numeric: tabular-nums; }
```

- Đỏ `--red` = 1 nghĩa duy nhất (vấn đề/nhấn mạnh/改善) — không dùng trang trí.
- Tiêu đề section: dải nền navy chữ trắng, hoặc chữ navy đậm + khoảng trắng — **cấm gạch chân accent, cấm stripe cạnh card**.
- Ngôn ngữ: tiếng Nhật, です・ます調, không dấu chấm than, không emoji. Thuật ngữ kỹ thuật giữ katakana/EN chuẩn khách đang dùng.

## 3. Cấu trúc trang chuẩn

1. **Header:** tiêu đề + ngày (YYYY/MM/DD) + người trình bày + version.
2. **サマリー (bắt buộc, ngay đầu):** box 3–5 dòng — 結論 / 対応要否 / 期限. Đóng khung navy hoặc nền ice.
3. **目次:** TOC anchor link (sticky sidebar nếu trang dài; `scroll-behavior: smooth`).
4. **Thân bài theo pattern:** 現状 → 課題 → 原因 → 対策案 → 比較 → 推奨案 → スケジュール → 費用.
5. **Footer:** liên hệ + tài liệu tham chiếu (link Backlog ticket).

## 4. Component đặc trưng

### Bảng so sánh phương án (khách soi kỹ nhất)
- Kẻ đủ đường dọc + ngang, header nền navy chữ trắng, hàng xen kẽ nền `--ice`.
- Đánh giá bằng **◎ ○ △ ×** (không emoji, không icon màu mè); cột 推奨 đánh dấu bằng nền nhạt của `--red` (ví dụ `color-mix(in oklch, var(--red) 8%, white)`).
- Số canh phải, đơn vị trong ngoặc ở header: `費用 (万円)`, `工数 (人日)`.

### Flow 現状 vs 改善 (2 khối đối chiếu)
- 2 panel cạnh nhau (mobile: dọc), label 【現状】/【改善案】; điểm nghẽn ở 現状 và điểm cải thiện ở 改善 tô `--red`.
- Vẽ bằng **SVG inline** (box + arrow + số bước ①②③), không ảnh chụp, không thư viện diagram — SVG in sắc nét và diff được.

### Sequence diagram (giải trình xử lý kỹ thuật)
- SVG inline: lifeline dọc cho từng actor/hệ thống, mũi tên đánh số ①〜⑧, chú thích 技術ポイント dưới cùng.
- Layout tránh mũi tên cắt nhau: actor con người bên trái, hệ thống tự động bên phải.

### Box cảnh báo / quyết định cần khách
```html
<div class="decision">
  <span class="decision-label">ご判断いただきたい事項</span>
  <p>…（deadline: 2026/07/18）</p>
</div>
```
Nền ice, border-left 4px navy (border-left dày là cấu trúc ngữ nghĩa, khác stripe trang trí mảnh).

## 5. In ấn (khách Nhật hay in ra họp)

```css
@page { size: A4; margin: 14mm; }
@media print {
  .toc-sidebar { display: none; }
  section { break-inside: avoid; }
  h2 { break-after: avoid; }
  a { color: inherit; text-decoration: none; }
}
```
- Test bằng Print Preview: bảng không gãy giữa chừng, SVG không tràn, màu nền bảng in được (`print-color-adjust: exact` cho header bảng).

## 6. Checklist riêng type này

- [ ] サマリー có 結論 ngay màn hình đầu?
- [ ] Bảng: kẻ đủ, số canh phải, đơn vị ở header, ◎○△?
- [ ] Diagram SVG có đánh số bước, không mũi tên cắt nhau?
- [ ] 1 màu đỏ = 1 nghĩa, không lạm dụng?
- [ ] です・ます調 nhất quán, không dấu chấm than, không emoji?
- [ ] In A4 không vỡ layout?
- [ ] 1 file HTML mở offline chạy được, < 500KB (không tính ảnh)?
