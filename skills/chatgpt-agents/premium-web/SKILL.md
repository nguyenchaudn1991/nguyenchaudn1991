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

## Triết lý: cấm mặc định vô thức, KHÔNG cấm kỹ thuật

**Không kỹ thuật nào tự thân tạo ra "AI vibe".** Gradient, glow, đối xứng, lưới 3 card,
Inter, glassmorphism, 3D, dark mode — tất cả đều đã tạo ra những trang xuất sắc. Chúng chỉ
thành "AI vibe" khi xuất hiện **vì đó là mặc định**, không vì một lý do thiết kế nào.

Cấm theo danh sách kỹ thuật thì tránh được cái xấu phổ thông, nhưng lại đẻ ra một cái mặc
định mới — font lạ + palette desaturated + 1 accent + masonry + tinted shadow. Đó cũng là
một loại AI vibe, chỉ tinh vi hơn.

> **Câu hỏi kiểm duy nhất cho mọi quyết định thị giác:**
> *"Tại sao thứ này ở đây?"*
> Trả lời được bằng design thesis → **giữ, kể cả khi nó nằm trong mọi blacklist.**
> Trả lời "vì nó trông hiện đại" / "vì ai cũng làm thế" / im lặng → **xóa.**

### Creative direction — bắt buộc, là bước 3 của quy trình

Đưa **2–3 hướng khác nhau về bản chất** (không phải 3 biến thể màu), mỗi hướng gồm:

| Mục | Nội dung |
|---|---|
| **Design thesis** | 1 câu: trang này *là* cái gì. VD "một hồ sơ thầu in trên giấy dày", "một phòng trưng bày tối chỉ có ánh đèn rọi vật thể" |
| **Cảm xúc** | Người xem cảm thấy gì trong 3 giây đầu |
| **Signature motif** | 1 yếu tố lặp lại làm nên nhận diện (đường kẻ, khối, cách cắt ảnh, ký tự, khoảng âm) |
| **Grid logic** | Đối xứng hay bất đối xứng — **và vì sao**. Đối xứng có chủ đích là hợp lệ |
| **Typography contrast** | Tương phản đến từ đâu: size, weight, style, hay ngôn ngữ chữ |
| **Color / material / light** | Bảng màu đến từ đâu (brand, vật liệu, bối cảnh) và ánh sáng hành xử thế nào |
| **Motion language** | Chuyển động *nói* điều gì, không phải "có animation" |
| **Signature moment** | 1 khoảnh khắc người xem sẽ nhớ và kể lại |
| **Cố tình KHÔNG dùng** | Kỹ thuật nào bị loại và vì sao — sự tiết chế cũng là quyết định |

User chọn 1 hướng → mới build. Nếu user nói **"tự quyết"**, agent chọn hướng recommended,
ghi 2–3 lý do ngắn rồi tiếp tục, không chặn tiến độ. Mọi quyết định sau đó phải truy được về
thesis đã chọn. Không có direction → không được code, vì lúc đó chỉ còn cách chạy theo mặc định.

**Ba hướng phải khác nhau về bản chất**, không phải 3 biến thể màu của cùng một layout.
Nếu cả 3 đều ra desaturated + 1 accent + masonry thì đó chưa phải 3 hướng — đó là 1 hướng
sơn 3 màu.

## A. Bất biến — thứ THẬT SỰ không thương lượng

Bốn nhóm này là **đúng/sai**, không phải thẩm mỹ. Không direction nào được phép vi phạm.

1. **Sự thật dữ liệu.** Cấm bịa testimonial, logo khách hàng, số liệu kinh doanh, chứng chỉ,
   giải thưởng — xem "Cổng dữ liệu thật" ở anti-ai-vibe.md mục 6. Cấm Lorem Ipsum và cliché
   rỗng ("Elevate/Seamless/Unleash/Next-Gen") trong bản bàn giao.
2. **Accessibility.** Contrast WCAG AA cho mọi text; focus-visible rõ trên mọi phần tử tương
   tác; thao tác được bằng bàn phím; touch target ≥ 44px; HTML semantic; alt thật.
3. **Performance.** Ngân sách ở mục B. Hiệu ứng phá ngân sách trên mobile → cắt hiệu ứng.
4. **Motion an toàn.** `prefers-reduced-motion: reduce` phải tắt được mọi motion trang trí;
   animation chỉ `transform`/`opacity`; không auto-play gây chóng mặt.

## B. Mặc định của nhà — lệch được, nhưng phải nói lý do

Đây là **điểm khởi đầu tốt**, không phải luật. Direction cho phép thì đi ngược lại thoải mái —
chỉ cần ghi 1 dòng lý do trong handoff.

| Mặc định | Được đi ngược khi |
|---|---|
| Palette desaturated, 1 accent | Direction cần nhiều accent có hệ thống (data viz, phân loại, brand nhiều màu), hoặc màu rực **là** concept |
| Tránh gradient tím-xanh | Gradient xuất phát từ brand/vật liệu/hiện tượng thật (hoàng hôn, kim loại, quang phổ) và không phải preset |
| Chiều sâu bằng tinted shadow + layering | Direction lấy **ánh sáng** làm ngôn ngữ chính (showroom tối, neon phố đêm, sci-fi) — lúc đó glow là nội dung, không phải trang trí |
| Lưới bất đối xứng | Đối xứng phục vụ thesis: trang trọng, nghi lễ, cân bằng, luxury, cổ điển |
| Tránh hàng 3 card đều nhau | 3 hạng mục thật sự ngang cấp và so sánh trực tiếp (pricing, 3 dịch vụ song song) |
| Font có cá tính (VN: `Be Vietnam Pro`/`Plus Jakarta Sans`; JP: `Noto Sans JP`) | Product UI cần trung tính, hoặc brand đã có font riêng. **Inter không bị cấm** — chỉ cấm chọn Inter vì không nghĩ |
| Nền có noise/grain/ảnh | Editorial tối giản: **chỉ typography + whitespace trên nền phẳng vẫn có thể xuất sắc** nếu nhịp chữ và khoảng trắng đủ tinh |

## C. Cliché — cấm vì đã mòn, không vì kỹ thuật xấu

Những **tổ hợp cụ thể** dưới đây đã bị dùng đến mức trở thành dấu hiệu "sinh bằng AI". Cấm
dùng chúng **ở dạng mặc định**. Vẫn được dùng nếu direction biến chính nó thành chủ đề — và
phải nói rõ trong handoff là cố ý.

- Gradient orb/blob mờ trôi trong hero · dot-grid + radial glow ("AI SaaS hero")
- Animated gradient text (shimmer, đổi hue) · typewriter effect trên headline
- Particle/starfield/matrix background · 3D tilt mọi card theo con trỏ · cursor trail
- Glow border/spotlight card rải khắp trang
- Hàng 3 card giống hệt làm layout chính của **mọi** section

## D. Khách Nhật — danh sách từ rejection thật (giữ cứng khi audience là Nhật)

Đây **không phải thẩm mỹ chủ quan** mà là phản hồi đã nhận từ khách thật. Với audience Nhật,
coi như bất biến; audience khác thì về nhóm B.

- Gạch chân accent dưới tiêu đề · stripe màu dọc cạnh card
- Card "bồng bềnh" gradient/shadow tràn lan
- Emoji làm icon (→ dùng số 01/02 hoặc nhãn chữ)
- Glow shadow màu accent trên nền tối

## E. Nghề — chất lượng thi công, độc lập với direction

Direction nào cũng phải đạt. Đây là phần phân biệt "đẹp trong ảnh chụp" với "đẹp khi dùng thật".

1. **Nhất quán nội bộ.** 1 bộ icon, 1 stroke weight, 1 hệ spacing, 1 hệ bo góc, 1 nguồn sáng
   cho toàn bộ shadow. Direction lạ đến mấy cũng phải nhất quán với chính nó.
2. **Mọi state có áp dụng đều tồn tại** (hover/active/focus/loading/empty/error) — thiếu
   state áp dụng được = trang chưa xong. Text tĩnh không cần loading state.
3. **Ngân sách hiệu ứng:** tối đa 1–2 hiệu ứng "đắt" mỗi trang. Nhiều hơn thì không còn
   khoảnh khắc nào nổi bật — và thường là dấu hiệu chưa có direction.
4. **Bảng và số:** kẻ bảng rõ, số canh phải `tabular-nums`, đơn vị trong ngoặc ở header.
5. **Chi tiết cuối:** không link chết `#`, nav đánh dấu trang hiện tại, 404 có thiết kế,
   meta + favicon đủ, link pháp lý ở footer.

→ Checklist audit đầy đủ: **anti-ai-vibe.md** (bắt buộc đọc trước khi viết code).

## F. PageSpeed — ngân sách cứng (mobile-first)
- **Core Web Vitals (field — dữ liệu người dùng thật):** LCP < 2.5s · CLS < 0.1 · INP < 200ms.
- **Ngân sách lab (Lighthouse mobile, throttle 4x):** thêm FCP < 1.2s. Đây là ngưỡng nội bộ để
  chống hồi quy — **không phải Core Web Vital**, đừng báo khách như chỉ số Google chấm.
- Ảnh: AVIF/WebP + `srcset` + width/height tường minh; hero = `fetchpriority="high"`, dưới màn hình = `loading="lazy"`.
- JS: **trang tĩnh greenfield độc lập** mặc định 0 framework; repo đã có stack thì giữ stack
  hiện hữu. Mọi script phù hợp phải `defer`; chỉ thêm thư viện khi type file và ngân sách cho phép.
- Hiệu ứng nào phá ngân sách trên mobile → cắt hiệu ứng, không hy sinh tốc độ.

→ Kỹ thuật chi tiết (modern CSS/JS APIs, font strategy, content-visibility…): **performance.md**.

---

## Quy trình chung

0. **Khảo sát cái đang có TRƯỚC khi đề xuất cái mới.** Dự án đã có code/design system thì
   **mặc định là tôn trọng nó**, không phải thay nó:
   - Có design token / biến CSS / Tailwind config / component library sẵn? → dùng lại, đừng
     đẻ ra hệ màu thứ hai.
   - Font, spacing scale, border-radius, ngôn ngữ component đang dùng là gì? → khớp theo.
   - Yêu cầu chỉ là sửa một phần (1 trang, 1 section)? → **chỉ đụng đúng phần đó.** Không tự
     ý redesign những chỗ không được yêu cầu.
   - Chỉ đề xuất brand kit mới khi: **greenfield không có brand**, hoặc user **nói rõ là muốn
     redesign**. Nghi ngờ → hỏi 1 câu, đừng tự quyết.

   10 luật anti AI-vibe bên dưới là **house style cho trường hợp mình được quyết**. Vào repo
   có sẵn hệ thống thiết kế thì nhất quán với hệ thống đó thắng, trừ khi user yêu cầu ngược lại.
1. **Xác định type + load refs** theo bảng routing (chỉ hỏi nếu không rõ type).
2. **Khảo sát ngắn:** lĩnh vực, audience (Nhật? → thêm japanese-quality.md), brand có sẵn (màu/logo/font), nội dung đầu vào.
3. **Creative direction — 2–3 hướng khác nhau về bản chất** theo bảng ở mục "Triết lý" bên trên.
   User chọn 1 hướng rồi mới sang bước 4; nếu user giao "tự quyết", agent chọn hướng recommended,
   ghi 2–3 lý do và đi tiếp. Brand kit (palette + font + motif) **suy ra từ direction đã chọn**,
   không phải chọn trước rồi mới nghĩ concept. Bước 0 xác định là repo có sẵn design system →
   direction phải nằm trong khuôn khổ hệ thống đó, không đề xuất brand kit mới.
4. **Build** theo cấu trúc trong type file, bám direction đã chọn. HTML semantic, CSS-first,
   JS tối thiểu. Mọi quyết định thị giác phải truy được về thesis.
5. **Render và audit trước khi bàn giao** — mở trang thật, chụp ít nhất desktop 1440px và mobile
   375–390px; kiểm tra console, keyboard/focus và các tương tác chính. So theo checklist
   anti-ai-vibe.md + PageSpeed trong performance.md, responsive và `prefers-reduced-motion`.
   **Bắt buộc có ít nhất 1 vòng sửa sau khi nhìn screenshot.** Soi lại direction: trang có đúng
   cảm giác thesis mô tả không, signature moment có đáng nhớ không? Nếu bỏ direction đi mà trang
   vẫn y hệt → direction chỉ là giấy tờ, chưa vào thiết kế. Không có browser/render tool thì phải
   ghi rõ **chưa visual-verify**, không được gọi là hoàn tất.

## Common mistakes

| Sai lầm | Sửa |
|---------|-----|
| Trigger skill cho yêu cầu web chung chung | Chỉ chạy khi có keyword/gọi đích danh |
| Nhảy thẳng vào code, không có direction | Bước 3 bắt buộc — không có thesis thì mọi lựa chọn đều là mặc định |
| Coi mục B/C như luật cấm | B là mặc định (lệch được, nói lý do); C cấm **cliché mặc định**, không cấm kỹ thuật. Chỉ A và D mới là bất biến |
| Direction nào cũng ra desaturated + 1 accent + masonry | Đó là mặc định mới, cũng là AI vibe. Direction phải khác nhau về **bản chất** |
| Load cả 4 type file "cho chắc" | Chỉ load type được chọn |
| Bỏ qua anti-ai-vibe.md vì "đã nhớ 10 luật" | 10 luật là tóm tắt; audit cuối phải theo checklist đầy đủ |
| Thêm GSAP/Lenis cho type 1/3/4 | Thư viện scroll chỉ được phép trong type-scroll.md, đúng tier quy định |
| Khách Nhật nhưng quên japanese-quality.md | Type 1 luôn load; type khác load khi audience Nhật |
