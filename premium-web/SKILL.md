---
name: premium-web
description: >-
  Use ONLY when the user explicitly names this skill ("premium-web") or types an exact
  trigger keyword for one of 4 website types: (1) "web report" / "trang báo cáo" /
  報告サイト / "giải trình khách Nhật" — report/explanation site for Japanese clients;
  (2) "web scroll" / "trang scroll" / "scroll experience" / "hiệu ứng cuộn" — premium
  scroll-driven site; (3) "web content" / "trang nội dung" / "content site" — content-first
  website; (4) "web LP" / "landing page" / "LP chuyển đổi" — conversion landing page.
  Do NOT auto-trigger on general web design, CSS, frontend, or dashboard requests
  that lack these keywords.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# Premium Web — 4 loại website, 1 chuẩn chất lượng

Skill hợp nhất để xây website theo **4 loại chuyên biệt**, với 2 điều kiện tiền đề
**bắt buộc cho mọi loại**: (a) **anti AI-vibe** — trông handcrafted, không rập khuôn AI;
(b) **PageSpeed** — đạt Core Web Vitals trên mobile.

> **Trigger discipline:** Chỉ chạy skill này khi user gọi đích danh hoặc gõ đúng keyword
> trong bảng routing bên dưới. Yêu cầu web/CSS chung chung → KHÔNG dùng skill này.

---

## Routing — chọn đúng 1 loại, load đúng 1 file

| # | Loại | Keyword trigger | File PHẢI load |
|---|------|-----------------|----------------|
| 1 | **Report** — trang báo cáo / giải trình / đề xuất cho khách Nhật (vấn đề → nguyên nhân → đối sách) | `web report`, `trang báo cáo`, `報告サイト`, `giải trình khách Nhật` | [references/type-report.md](references/type-report.md) |
| 2 | **Scroll** — trải nghiệm cuộn cao cấp (storytelling, scrub, sticky scenes) | `web scroll`, `trang scroll`, `scroll experience`, `hiệu ứng cuộn` | [references/type-scroll.md](references/type-scroll.md) |
| 3 | **Content** — web thường, ưu tiên nội dung dễ đọc (blog, docs, giới thiệu công ty) | `web content`, `trang nội dung`, `content site` | [references/type-content.md](references/type-content.md) |
| 4 | **Landing** — LP chuyển đổi (bán hàng, thu lead, khai trương dịch vụ) | `web LP`, `landing page`, `LP chuyển đổi` | [references/type-landing.md](references/type-landing.md) |

**Quy tắc load (tối ưu token):**
- Luôn load: file type được chọn + [references/anti-ai-vibe.md](references/anti-ai-vibe.md) + [references/performance.md](references/performance.md). **Không được bỏ qua 2 file này** — chúng là điều kiện tiền đề.
- Chỉ load [references/japanese-quality.md](references/japanese-quality.md) khi khách/audience là **Nhật** (Type 1 mặc định là Nhật → luôn load).
- KHÔNG load file của các type không được chọn.
- User gọi skill nhưng không rõ type → hỏi 1 câu duy nhất với 4 lựa chọn, rồi tiếp tục.

**Phối hợp với skill `hono-stack`** (khi dự án có backend Hono): hono-stack quyết
backend/deploy/cấu trúc dự án; premium-web quyết toàn bộ UI/design. Hai skill không
mâu thuẫn — cả hai cùng bắt buộc PageSpeed, và mục tiêu "trang public 0 JS" của
hono-stack khớp với ngân sách hiệu ứng ở đây.

---

## Điều kiện tiền đề (áp cho cả 4 loại — không thương lượng)

### A. Anti AI-vibe — 10 luật cứng
1. Không palette AI: cấm gradient tím-xanh, accent quá bão hòa (>80%), nền `#000000` thuần (dùng off-black `#0a0a0a`/`#121212` hoặc navy tối).
2. Chỉ **1 màu accent**. 1 màu = 1 nghĩa, dùng nhất quán.
3. Typography có cá tính: cấm Inter/Open Sans/mặc định hệ thống tràn lan. VN: `Be Vietnam Pro`/`Plus Jakarta Sans` (check dấu tiếng Việt bằng screenshot); JP: `Noto Sans JP`/system JP stack, line-height 1.6–1.8.
4. Cấm mọi hiệu ứng phát sáng: glow border, neon shadow, gradient orb trôi nổi, shimmer text, particle/starfield, dot-grid + radial glow, 3D tilt theo chuột. Chiều sâu = tinted shadow + layering, không phải ánh sáng.
5. Phá đối xứng: cấm hàng 3 card đều chằn chặn làm layout chính; dùng lưới bất đối xứng (2-1, zig-zag, masonry).
6. Copy thật: cấm Lorem Ipsum, "Elevate/Seamless/Unleash/Next-Gen", tên giả "Nguyễn Văn A"/"山田太郎", số tròn giả (50%, $100).
7. Icon 1 bộ duy nhất, cùng stroke; cấm emoji làm icon (khách Nhật đặc biệt ghét).
8. Mọi animation chỉ dùng `transform`/`opacity`; tối đa 1–2 hiệu ứng "đắt" mỗi trang; luôn có `prefers-reduced-motion: reduce`.
9. Hover/active/focus/loading/empty/error states phải tồn tại — thiếu state = trang chưa xong.
10. Bảng và số: kẻ bảng rõ, số canh phải `tabular-nums`, đơn vị trong ngoặc ở header.

→ Chi tiết + checklist audit đầy đủ: **anti-ai-vibe.md** (bắt buộc đọc trước khi viết code).

### B. PageSpeed — ngân sách cứng (mobile-first)
- **LCP < 2.5s · CLS < 0.1 · INP < 200ms · FCP < 1.2s** — đo trên mobile, không phải desktop.
- Ảnh: AVIF/WebP + `srcset` + width/height tường minh; hero = `fetchpriority="high"`, dưới màn hình = `loading="lazy"`.
- JS: mặc định **0 framework** cho trang tĩnh; mọi script `defer`; thư viện chỉ khi type file cho phép.
- Hiệu ứng nào phá ngân sách trên mobile → cắt hiệu ứng, không hy sinh tốc độ.

→ Kỹ thuật chi tiết (modern CSS/JS APIs, font strategy, content-visibility…): **performance.md**.

---

## Quy trình chung (mọi type đi qua 5 bước)

1. **Xác định type + load refs** theo bảng routing (chỉ hỏi nếu không rõ type).
2. **Khảo sát ngắn:** lĩnh vực, audience (Nhật? → thêm japanese-quality.md), brand có sẵn (màu/logo/font), nội dung đầu vào.
3. **Đề xuất brand kit độc bản:** 1 palette desaturated + 1 accent + bộ font — theo quy định riêng của type file.
4. **Build** theo cấu trúc trong type file. HTML semantic, CSS-first, JS tối thiểu.
5. **Audit trước khi bàn giao** — chạy checklist trong anti-ai-vibe.md + đo PageSpeed theo performance.md; kiểm tra responsive (mobile trước) và `prefers-reduced-motion`.

## Common mistakes

| Sai lầm | Sửa |
|---------|-----|
| Trigger skill cho yêu cầu web chung chung | Chỉ chạy khi có keyword/gọi đích danh |
| Load cả 4 type file "cho chắc" | Chỉ load type được chọn |
| Bỏ qua anti-ai-vibe.md vì "đã nhớ 10 luật" | 10 luật là tóm tắt; audit cuối phải theo checklist đầy đủ |
| Thêm GSAP/Lenis cho type 1/3/4 | Thư viện scroll chỉ được phép trong type-scroll.md, đúng tier quy định |
| Khách Nhật nhưng quên japanese-quality.md | Type 1 luôn load; type khác load khi audience Nhật |
