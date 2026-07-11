# Type 2 — Scroll Experience (trải nghiệm cuộn cao cấp)

Trang storytelling nơi cuộn chuột điều khiển hoạt cảnh. Nguyên tắc chọn công nghệ:
**leo thang theo tier — bắt đầu ở tier thấp nhất đáp ứng được yêu cầu, chỉ lên tier
cao hơn khi có lý do cụ thể.** Tier càng cao càng tốn hiệu năng và công sản xuất asset.

> Cấm scroll-jacking (chiếm quyền cuộn, cuộn bị "khựng" theo section). Cuộn phải luôn
> là của người dùng; hiệu ứng chỉ *phản ứng theo* vị trí cuộn.

---

## Tier 0 — Reveal cơ bản (mặc định cho 90% nhu cầu)

Phần tử fade/slide vào khi cuộn tới. **0 thư viện.**

```css
@supports (animation-timeline: view()) {
  .reveal {
    animation: enter linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 60%;
  }
}
@keyframes enter { from { opacity: 0; transform: translateY(24px); } }
```
Fallback (Safari cũ) bằng IntersectionObserver ~10 dòng, thêm class `.in-view`.
Stagger: `animation-delay`/`transition-delay` bậc 60–90ms theo thứ tự con.

## Tier 1 — Sticky scene + CSS scroll-driven (CSS-only, PageSpeed tối đa)

Cho hero 1 ảnh/1 cảnh: pin phần tử bằng `position: sticky`, ánh xạ tiến độ cuộn vào
transform bằng `animation-timeline`.

```css
.scene-wrap { height: 250vh; view-timeline-name: --scene; }
.scene {
  position: sticky; top: 0; height: 100dvh; overflow: clip;
}
.scene img {
  height: 100%; width: 100%; object-fit: cover;
  animation: zoom linear both;
  animation-timeline: --scene;
  animation-range: entry 0% exit 100%;
}
@keyframes zoom { from { transform: scale(1); } to { transform: scale(1.22); } }
```
Biến thể cùng kỹ thuật: parallax đa lớp (mỗi lớp 1 tốc độ translate), text mask reveal,
outlined-to-fill text, split-screen 2 nửa trượt ngược chiều, card stack (các section
sticky chồng lên nhau bằng `top` lệch dần).

## Tier 2 — GSAP ScrollTrigger (khi cần scrub/pin/timeline đồng bộ phức tạp)

Dùng khi: nhiều tween phải khớp 1 timeline, pin lồng nhau, horizontal scroll section,
hoặc cần scrub với inertia. Đây là tier duy nhất được phép thêm thư viện.

- Chỉ `gsap.min.js` + `ScrollTrigger` (~70KB gzip), load `defer`; **Lenis** (smooth scroll
  inertia, ~10KB) là tùy chọn — chỉ thêm khi khách muốn cảm giác "trôi" điện ảnh, và phải
  test INP mobile sau khi thêm.
- **Self-host file thư viện** (copy vào `/js/` của dự án), không load từ CDN — khớp CSP
  `script-src 'self'`, không phụ thuộc bên thứ ba, cache tự kiểm soát.
- Mẫu chuẩn:
  ```js
  gsap.registerPlugin(ScrollTrigger);
  gsap.timeline({
    scrollTrigger: { trigger: ".chapter", start: "top top", end: "+=200%", scrub: 0.6, pin: true }
  })
  .to(".layer-back", { yPercent: -20 }, 0)
  .to(".panel-2", { xPercent: -100 }, 0.5);
  ```
- Vẫn chỉ animate `transform`/`opacity`; `ScrollTrigger.matchMedia()` để tắt/pha loãng
  hiệu ứng trên mobile; `prefers-reduced-motion` → không init timeline, hiện nội dung tĩnh.

## Tier 3 — Media scrub (video/ảnh-sequence tua theo cuộn, kiểu Apple)

Chỉ khi **đã có sẵn asset chuyển động** (video render 3D, quay sản phẩm, xuất từ
Blender/Spline/After Effects, hoặc video AI do anh tự sinh từ tool khác — pipeline
Higgsfield cũ đã bỏ). Không có asset → thuyết phục dùng Tier 1/2, đừng tự chế.

### 3a. Video scrub (1 video duy nhất)
Ánh xạ tiến độ cuộn → `video.currentTime`.

**Mã hóa bắt buộc** (scrub ngốn CPU giải mã — keyframe phải dày):
```bash
# Desktop 1080p (GOP 8)
ffmpeg -i in.mp4 -an -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart out.mp4
# Mobile 720p (GOP 4 — tua mượt trên điện thoại)
ffmpeg -i in.mp4 -an -vf "scale=1280:720" -c:v libx264 -preset slow -crf 23 \
  -pix_fmt yuv420p -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart out-m.mp4
```

**4 nguyên tắc engine:**
1. Fetch video thành **Blob URL** rồi mới gán `src` (tránh range-request liên tục).
2. Cập nhật `currentTime` trong **rAF loop**, lerp về giá trị đích để mượt.
3. **Coalesce seeks:** chỉ seek mới khi `video.seeking === false` (bắt buộc trên mobile).
4. **iOS priming:** iOS cấm seek trước tương tác — gọi `play()` rồi `pause()` ngay trong
   sự kiện `pointerdown`/`touchstart` đầu tiên.
5. Poster = ảnh tĩnh frame đầu (`still.webp`) hiện ngay để LCP không đợi video; video
   fetch sau khi trang tải xong.

### 3b. Canvas image-sequence (chất lượng scrub cao nhất)
60–120 frame AVIF/WebP vẽ lên `<canvas>` theo tiến độ cuộn. Nặng băng thông → chỉ cho
1 hero section; preload frame đầu, lazy phần còn lại theo hướng cuộn; mobile giảm còn
~40 frame 720p hoặc rơi về Tier 1.

---

## Ngân sách & nghiệm thu riêng type này

- Hiệu ứng scroll "đắt" (Tier 2–3): **tối đa 1 cụm/trang**; phần còn lại Tier 0.
- LCP element phải là ảnh tĩnh/poster — không bao giờ đợi video/JS.
- Kiểm tra: cuộn bằng bánh xe, trackpad, kéo thanh cuộn, phím PgDn — cả 4 phải tự nhiên.
- `prefers-reduced-motion: reduce` → mọi tier rơi về nội dung tĩnh có đủ thông tin.
- Mobile thật (hoặc throttle 4x): không rớt frame khi cuộn, INP < 200ms.
- Nội dung phải đọc được nếu JS fail (Tier 2–3 progressive enhancement trên HTML tĩnh).

## Chọn tier nhanh

| Yêu cầu của anh | Tier |
|-----------------|------|
| "Section hiện dần khi cuộn cho sang" | 0 |
| "1 ảnh hero zoom/parallax theo cuộn" | 1 |
| "Chương-hồi, pin section, horizontal scroll, nhiều lớp khớp nhau" | 2 |
| "Camera bay qua cảnh như Apple" + **có sẵn video/frame** | 3 |
| Như trên nhưng **chưa có asset** | Đề xuất lại: Tier 1/2, hoặc anh chuẩn bị asset trước |
