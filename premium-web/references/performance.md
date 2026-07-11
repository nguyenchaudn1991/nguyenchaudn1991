# Performance — PageSpeed & Modern Web APIs (áp cho mọi type)

Ngân sách cứng (đo **mobile**, throttle 4x): **LCP < 2.5s · CLS < 0.1 · INP < 200ms · FCP < 1.2s**.
Nguyên tắc: hiệu ứng nào phá ngân sách → cắt hiệu ứng, không hy sinh tốc độ.

---

## 1. Ảnh (nguồn LCP số 1)

- Định dạng: **AVIF** (fallback WebP) qua `<picture>`; chất lượng ~80 (squoosh.app).
- Luôn khai `width`/`height` (hoặc `aspect-ratio`) → chống CLS.
- Hero/LCP image: `fetchpriority="high"`, KHÔNG lazy; preload nếu là background:
  ```html
  <link rel="preload" as="image" href="hero.avif" fetchpriority="high">
  ```
- Dưới màn hình đầu: `loading="lazy" decoding="async"`.
- `srcset` + `sizes` theo breakpoint thực; bản mobile riêng (`hero_sp.webp`) nếu crop khác.
- Asset cho khách tự thay: folder cố định + README (tên file cố định `hero.webp`, kích thước chính xác, hướng dẫn nén) — "thay file cùng tên là xong".

## 2. Font

- **JP:** ưu tiên system stack — 0 byte tải:
  ```css
  font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, "Noto Sans JP", sans-serif;
  ```
  Nếu bắt buộc webfont JP (Noto Sans JP): subset + `font-display: swap`, chỉ 2 weight.
- **VN/EN webfont:** WOFF2, subset đúng ký tự (VN cần Latin Extended), tối đa 2 family × 2–3 weight, preload file chính:
  ```html
  <link rel="preload" as="font" type="font/woff2" href="font.woff2" crossorigin>
  ```
- `font-display: swap` + fallback cùng metrics (dùng `size-adjust` nếu cần) → chống CLS khi swap. Fallback cũng phải render đúng dấu VN.

## 3. JavaScript

- Trang tĩnh (report/content/LP): mặc định **0 framework, 0 bundler** — 1 file HTML + CSS + (nếu cần) 1 file JS nhỏ `defer`.
- Mọi `<script>` đặt `defer`; third-party (analytics, chat) load sau tương tác đầu hoặc `requestIdleCallback`.
- Tác vụ JS nặng: nhường main thread
  ```js
  if (globalThis.scheduler?.yield) await scheduler.yield();
  ```
- Thư viện animation chỉ được phép khi type-scroll.md cho phép (đúng tier), luôn `defer` + load có điều kiện.

## 4. CSS-first — thay JS bằng API gốc

| Nhu cầu | Dùng gốc, không thư viện |
|---------|--------------------------|
| Modal | `<dialog>` + `showModal()` |
| Menu/tooltip/popover | thuộc tính `popover` + `popovertarget` (tự đóng khi click ngoài) |
| Gắn tooltip cạnh nút | CSS Anchor Positioning (`position-anchor`, `anchor()`) |
| Hiệu ứng lúc mount | `@starting-style` + `transition` |
| Component co giãn theo cha | Container Queries (`container-type: inline-size` + `@container`) |
| Thẳng hàng nội dung giữa các card | `grid-template-rows: subgrid` |
| Accordion đơn giản | `<details>`/`<summary>` |
| Textarea tự cao | `field-sizing: content` |
| Validate form | `:user-invalid` (chỉ báo lỗi sau khi user rời ô) |

- Màu: `oklch()` + `color-mix(in oklch, var(--accent) 15%, transparent)` cho tint/shade động.
- Chống orphan: `text-wrap: balance` (heading), `text-wrap: pretty` (body).

## 5. Render & điều hướng

- Section dưới màn hình / nặng:
  ```css
  .below-fold { content-visibility: auto; contain-intrinsic-size: 0 500px; }
  ```
- Prerender trang tiếp theo (site nhiều trang):
  ```html
  <script type="speculationrules">
  { "prerender": [{ "source": "list", "urls": ["/contact.html"] }] }
  </script>
  ```
- CSS critical inline trong `<head>` với trang 1 file; tránh chain import CSS.
- `min-height: 100dvh` thay `100vh`.

## 6. Animation rẻ

- Chỉ `transform` + `opacity` (GPU); cấm animate `top/left/width/height/box-shadow`.
- `will-change` chỉ đặt ngay trước khi animate, gỡ sau khi xong; không rải sẵn.
- Scroll-reveal: CSS scroll-driven animations (`animation-timeline: view()`) hoặc `IntersectionObserver` — không lib.
- `backdrop-filter: blur` chỉ trên bề mặt nhỏ; cấm full-viewport.
- Luôn có:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
  }
  ```
  (giữ lại transition opacity thiết yếu nếu việc tắt gây mất nội dung).

## 7. Đo & nghiệm thu

1. Lighthouse mobile (DevTools hoặc PageSpeed Insights) — mục tiêu **Performance ≥ 90**.
2. Soi từng chỉ số: LCP element là gì? CLS đến từ đâu (font swap? ảnh thiếu size?)? INP handler nào?
3. Test màn hình hẹp 375px và throttle CPU 4x.
4. Nếu có skill `mobile-first-performance` trong môi trường → có thể gọi bổ sung cho audit sâu (Next.js/iOS); không bắt buộc.
