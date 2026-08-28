# Type 3 — Content Site (web thường, nội dung là vua)

Blog, tài liệu, trang giới thiệu công ty/dịch vụ — người dùng đến để **đọc**.
Mọi quyết định thiết kế phục vụ tốc độ đọc và độ tin cậy. Đây là type "khiêm tốn":
sang trọng đến từ typography và spacing, không phải hiệu ứng.

---

## 1. Nguyên tắc

- **Typography-first:** 80% ấn tượng nằm ở font, cỡ chữ, nhịp dòng. Đầu tư ở đây trước.
- Với trang greenfield độc lập: **0 framework, 0 thư viện**; HTML tĩnh + CSS, JS chỉ cho
  TOC/menu mobile (≤ 30 dòng). Với repo có sẵn stack, giữ stack và component conventions hiện hữu.
- **Hiệu ứng:** tối đa Tier 0 reveal rất nhẹ (xem type-scroll.md nếu cần) hoặc không gì cả. Không hero video, không parallax.
- **SEO là tính năng hạng nhất** với type này.

## 2. Hệ đọc (reading system)

```css
:root {
  --measure: 66ch;          /* chiều rộng đoạn văn */
  --step-0: 1.0625rem;      /* body 17px */
  --step-1: 1.33rem; --step-2: 1.77rem; --step-3: 2.36rem;  /* scale ~1.33 */
}
article { max-width: var(--measure); margin-inline: auto; }
article p { font-size: var(--step-0); line-height: 1.65; text-wrap: pretty; }
h1, h2, h3 { text-wrap: balance; letter-spacing: -0.015em; }
```

- Type scale cố định (1.25–1.333), cấm size lẻ tùy hứng.
- Khoảng cách trước heading **lớn hơn** sau heading (heading dính với nội dung của nó).
- Font: 1 serif có hồn cho heading (VN: **Lora**) + 1 sans cho body, hoặc 1 sans tốt cho cả hai. Tối đa 2 family.
- Ảnh trong bài: full chiều rộng measure, bo góc nhẹ, caption nhỏ màu nhạt.
- Blockquote, code block, bảng, danh sách — style đủ cả trước khi ship (bài viết thật sẽ dùng).

## 3. Cấu trúc

- **Trang bài viết:** breadcrumb → h1 → meta (tác giả/ngày/thời gian đọc) → mục lục (bài > 1500 từ, sticky bên phải desktop, collapse mobile) → thân → tác giả box → bài liên quan.
- **Trang danh sách:** card bài viết KHÔNG đều chằn chặn — bài nổi bật to hơn (lưới 2-1), còn lại list gọn. Mỗi card: ảnh (nếu có), tiêu đề, mô tả 1–2 dòng, ngày. Bỏ nút "Read more" — cả card là link.
- **Nav:** tối giản, ≤ 5 mục, đánh dấu trang hiện tại. Footer gọn: điều hướng chính + pháp lý.
- Dark mode: chỉ làm nếu khách yêu cầu; nếu làm thì `light-dark()` + `color-scheme`, không toggle sun/moon cliché.

## 4. SEO & metadata (bắt buộc)

- 1 `<h1>`/trang; heading đúng cấp không nhảy bậc; semantic (`article`, `time datetime`, `nav`, `figure/figcaption`).
- `<title>` ≤ 60 ký tự, `meta description` ≤ 155, `og:title/description/image`, canonical.
- JSON-LD `Article` (hoặc `Organization` cho trang giới thiệu).
- `sitemap.xml` + `robots.txt` nếu site nhiều trang; Speculation Rules prerender cho link nội bộ chính (xem performance.md).
- Ảnh: alt mô tả thật; tên file có nghĩa (`bao-gia-mau.webp` không `img_01.webp`).

## 5. Checklist riêng type này

- [ ] Đoạn văn ≤ 66ch, line-height ≥ 1.6, đọc 3 đoạn không mỏi?
- [ ] Type scale nhất quán, spacing heading đúng luật gần-xa?
- [ ] Blockquote/code/bảng/list đều đã style?
- [ ] TOC hoạt động, đánh dấu vị trí hiện tại?
- [ ] Title/description/OG/JSON-LD đầy đủ, 1 h1?
- [ ] Lighthouse mobile: Performance ≥ 95, SEO = 100 (type này phải đạt — không có gì nặng để đổ lỗi)?
