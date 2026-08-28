# Anti AI-Vibe — checklist audit đầy đủ (áp cho mọi type)

## Mục lục

1. [Typography](#1-typography)
2. [Màu & bề mặt](#2-màu--bề-mặt)
3. [Layout](#3-layout)
4. [Hiệu ứng](#4-hiệu-ứng--cliché-thời-ai-mặc-định-là-xóa)
5. [Tương tác & states](#5-tương-tác--states)
6. [Nội dung](#6-nội-dung)
7. [Component](#7-component)
8. [Icon & ảnh](#8-icon--ảnh)
9. [Hero có ảnh nền](#9-hero-có-ảnh-nền-khách-luôn-hỏi-mục-này)
10. [Code & phần hay quên](#10-code--phần-hay-quên)
11. [Thứ tự sửa](#thứ-tự-sửa-impact-lớn--rủi-ro-thấp)
12. [Checklist bàn giao](#checklist-bàn-giao)

Trang phải trông **có chủ đích và handcrafted**. File này là checklist audit — dò từng mục,
mục nào dính thì sửa theo hướng dẫn kèm theo.

> ### ⚠️ Cách đọc file này
>
> Đây **không phải danh sách cấm kỹ thuật**. Mỗi mục có dạng *triệu chứng → cách chữa mặc định*,
> và cách chữa đó đúng cho **trường hợp không có design direction**.
>
> Đã có creative direction (SKILL.md bước 3) và direction đó **cố ý** dùng thứ nằm trong danh
> sách — gradient, glow, đối xứng, 3 card, Inter, nền phẳng — thì **giữ**, ghi 1 dòng lý do
> trong handoff. Kỹ thuật không xấu; dùng nó vì quán tính mới xấu.
>
> Chỉ 4 nhóm là bất biến, không direction nào vượt: **sự thật dữ liệu · accessibility ·
> performance · reduced-motion** (SKILL.md mục A), cộng danh sách khách Nhật (mục D) khi
> audience là Nhật.

---

## 1. Typography

- **Font mặc định / Inter tràn lan** → EN: `Geist`, `Outfit`, `Satoshi`, `Cabinet Grotesk`; VN: `Be Vietnam Pro`, `Plus Jakarta Sans` (Latin Extended đầy đủ); JP: `Noto Sans JP`, `Zen Kaku Gothic`, hoặc system stack JP (xem performance.md).
- **Dấu tiếng Việt vỡ** → line-height ≥ 1.5; **screenshot cụm nhiều dấu** ("xuống tiền", "thẩm định") trước khi chốt font. Playfair Display vỡ dấu VN → serif VN dùng **Lora**. Font fallback cũng phải hỗ trợ VN (Georgia vỡ dấu → fallback `"Times New Roman", serif`).
- **Tiếng Nhật gãy chữ** → `word-break: keep-all` + `overflow-wrap: break-word`; body 14px+; line-height 1.6–1.8.
- **Headline thiếu lực** → display 48px+, letter-spacing âm (−0.02em), line-height ~1.1.
- **Đoạn văn quá rộng** → max ~65 ký tự/dòng (~60–68ch), line-height 1.6.
- **Chỉ dùng weight 400/700** → thêm 500/600 cho phân cấp tinh tế.
- **Số dùng font tỷ lệ** → `font-variant-numeric: tabular-nums` cho bảng/số liệu.
- **Chữ mồ côi cuối dòng** → `text-wrap: balance` (heading) / `text-wrap: pretty` (body).
- **ALL-CAPS mọi subheader** → sentence case, hoặc small-caps + tracking dương (+0.05em).

## 2. Màu & bề mặt

- **`#000000` thuần / accent chói** → off-black `#0a0a0a`/`#121212`/navy `#0E1B2E`; accent bão hòa < 80%.
  *(Mặc định. Đen tuyệt đối và màu rực bão hòa cao hợp lệ khi chính nó là concept — ví dụ OLED
  showroom, brand neon, poster in offset.)*
- **Nhiều accent** → giữ 1, bỏ hết phần còn lại.
- **Trộn gray ấm + lạnh** → 1 họ gray duy nhất, tint theo 1 hue.
- **Gradient tím-xanh "AI"** → nền trung tính + 1 accent; hoặc gradient radial/mesh rất nhẹ.
- **Shadow đen generic** → tinted shadow theo hue của nền (nền xanh → shadow xanh đậm).
- **Accent màu sáng làm text trên nền trắng** → phải có biến thể tối đạt WCAG ≥ 4.5:1 (2 token: `--accent` cho nền sáng, `--accent-bright` chỉ dùng trên nền tối).
- **Glow shadow màu accent trên nền tối** → khách thật đã từng reject; dùng shadow trung tính tối hơn nền, hoặc bỏ.
- **Flat 100% vô hồn** → noise/grain rất nhẹ, hoặc ảnh nền mờ.
  *(Mặc định — áp khi section phẳng là do lười, không do chọn. Editorial tối giản: **chỉ
  typography + whitespace trên nền phẳng vẫn có thể xuất sắc**, khi nhịp chữ, cỡ chữ và
  khoảng trắng đủ tinh. Phân biệt bằng câu hỏi: bỏ hết trang trí đi thì phần chữ có tự đứng
  được không?)*
- **Section tối đột ngột giữa trang sáng** → giữ 1 tông xuyên suốt, đậm nhạt cùng palette.
- **Hướng sáng loạn** → mọi shadow theo 1 nguồn sáng (thường top-left).

## 3. Layout

- **Mọi thứ căn giữa + đối xứng** → offset margin, tỷ lệ ảnh trộn, header canh trái trên nội dung giữa.
  *(Mặc định. Đối xứng có chủ đích là ngôn ngữ thiết kế hợp lệ — trang trọng, nghi lễ, luxury,
  cổ điển. Cấm là cấm đối xứng **vì không nghĩ ra gì khác**.)*
- **3 card đều nhau làm feature row** → zig-zag 2 cột, lưới 3-2/2-3, masonry, hoặc horizontal scroll.
  *(Mặc định. 3 hạng mục thật sự ngang cấp và để so sánh trực tiếp — pricing, 3 gói dịch vụ —
  thì hàng 3 card là biểu diễn đúng. Vấn đề là dùng nó cho **mọi** section.)*
- **`height: 100vh`** → `min-height: 100dvh` (bug viewport iOS Safari).
- **Không max-width** → container 1200–1440px, margin auto.
- **Border-radius đồng loạt** → trong nhỏ (8–12px), ngoài mềm (16–24px).
- **Không có lớp chồng/độ sâu** → negative margin tạo layering có chủ đích.
- **Thiếu whitespace** → nhân đôi khoảng cách; gap block↔block PHẢI lớn hơn gap heading↔body.
- **Nút trong nhóm card không thẳng hàng đáy** → pin CTA xuống đáy card.
- **Baseline lệch giữa các cột song song** → title/desc/price/CTA cùng Y qua các cột (subgrid).
- **Căn giữa toán học nhưng lệch mắt** → tinh chỉnh quang học 1–2px (icon cạnh chữ, play button).

## 4. Hiệu ứng — cliché thời AI (mặc định là xóa)

Các tổ hợp dưới đã mòn đến mức thành dấu hiệu "sinh bằng AI". Xóa khi chúng xuất hiện vì
quán tính. Giữ khi direction biến chính nó thành chủ đề và nói rõ trong handoff.

- Gradient orb / blob mờ trôi trong hero
- Glow border / spotlight card (tĩnh hay theo chuột)
- Animated gradient text (shimmer, đổi hue)
- Typewriter effect trên headline
- Particle / starfield / matrix background
- 3D tilt mọi card theo con trỏ
- Cursor trail / blob cursor
- Dot-grid + radial glow ("AI SaaS hero" mặc định)
- **Riêng khách Nhật, thêm:** gạch chân accent dưới tiêu đề · stripe màu dọc cạnh card · card "bồng bềnh" gradient/shadow tràn lan · emoji làm icon (→ dùng số 01/02 hoặc nhãn chữ)

**Premium thật sự =** 1 font có chủ đích, spacing kỷ luật, tinted shadow, hairline border
(1px trắng mờ ở mép trên — gợi cạnh vật lý, KHÔNG phải glow), motion 200–300ms có lý do.

**Ngân sách hiệu ứng:** tối đa 1–2 hiệu ứng đắt/trang; `backdrop-filter` chỉ trên bề mặt nhỏ
(nav, card nhỏ — không bao giờ full-viewport); scroll-driven qua CSS/IntersectionObserver;
luôn có `prefers-reduced-motion: reduce` tắt motion trang trí.

## 5. Tương tác & states

- Hover: đổi nền/scale/translate — phải có phản hồi.
- Active: `scale(0.98)` hoặc `translateY(1px)`.
- Transition 200–300ms cho mọi phần tử tương tác; focus ring rõ (accessibility).
- Loading = skeleton đúng shape (không spinner generic); empty state có hướng dẫn; error inline (cấm `alert()`).
- Nav phải đánh dấu trang hiện tại; anchor có `scroll-behavior: smooth`; không link chết `#`.
- Animation cấm `top/left/width/height` → chỉ `transform`/`opacity`.

## 6. Nội dung

> ### ⚠️ Cổng dữ liệu thật — đọc trước khi áp mục này
>
> Các luật dưới đây nói về **chất lượng viết của nội dung mẫu**, không phải giấy phép bịa
> dữ liệu. Phân biệt hai loại, không được lẫn:
>
> **A. Nội dung mẫu cho bản demo/mockup** — tên người, tên công ty, ngày tháng, đoạn văn
> minh hoạ. Ở đây áp dụng các luật dưới: viết cho tự nhiên, đừng để lộ `Nguyễn Văn A` /
> `Lorem Ipsum` / `$100.00` vì nó làm trang trông như chưa làm xong.
>
> **B. Nội dung mang tính khẳng định về thế giới thật** — **TUYỆT ĐỐI KHÔNG BỊA**, kể cả
> trong demo:
> - Testimonial, review, đánh giá, trích lời khách hàng
> - Tên/logo khách hàng, đối tác, "được tin dùng bởi…"
> - Số liệu kinh doanh: doanh thu, số user, tỷ lệ tăng trưởng, số dự án, số năm kinh nghiệm
> - Chứng chỉ, giải thưởng, thành viên hiệp hội, con số nhân sự
> - Ảnh/avatar người thật, số liệu case study
>
> Loại B **chỉ được lấy từ khách hàng cung cấp**. Chưa có → dùng placeholder **lộ rõ là
> placeholder**: `[Testimonial — chờ khách cung cấp]`, `[Số liệu cần xác minh]`,
> khối xám có nhãn. Placeholder xấu là đúng chủ đích — nó buộc phải điền trước khi lên
> production.
>
> **Không bao giờ ship loại B khi chưa xác minh.** Testimonial bịa trên site chạy thật là
> quảng cáo sai sự thật, không phải lỗi thẩm mỹ. Bàn giao mà còn placeholder → **nói rõ
> trong handoff** danh sách những chỗ khách phải điền.

- Tên người thật theo ngữ cảnh (nội dung loại A): VN "Trần Hoàng Nam" (không "Nguyễn Văn A"); JP "佐藤 健太" (không "山田太郎"); cấm John Doe.
- Số hữu cơ cho số liệu minh hoạ **không mang tính khẳng định**: `47.2%` thay vì `50%`, `¥99,800` thay vì `$100.00`. Số nào là tuyên bố về doanh nghiệp thật → loại B, xem cổng trên.
- Tên công ty tin được — cấm "Acme", "Nexus", "SmartFlow". Tên khách hàng thật → loại B.
- Cấm cliché AI: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Powerful".
- Error message trực tiếp, chủ động: "Không lưu được thay đổi. Thử lại." — cấm "Oops!", cấm bị động, bỏ dấu chấm than trong success message.
- Ngày blog ngẫu nhiên tự nhiên; cấm Lorem Ipsum; sentence case cho header. Avatar: ảnh người
  thật chỉ dùng khi khách cung cấp — còn lại dùng monogram/illustration (mục 8), không lấy
  ảnh người lạ làm "khách hàng".
- Tông theo văn hóa: **Nhật** = Zen, nhiều whitespace, tiết chế; **VN** = rõ ràng, đáng tin, social proof (số liệu, testimonial, đội ngũ).

## 7. Component

- Card generic (border+shadow+nền trắng) → bỏ border, hoặc chỉ nền, hoặc chỉ spacing.
- 1 nút filled + 1 nút ghost mọi nơi → thêm text link/tertiary.
- Pill badge "New/Beta" → badge vuông, flag, hoặc nhãn chữ thường.
- FAQ accordion → danh sách 2 cột, hoặc disclosure inline.
- Carousel testimonial 3 card + dots → masonry quotes, 1 quote xoay có pagination, hoặc list tĩnh.
- Pricing 3 tháp giống nhau → nhấn tier khuyến nghị bằng màu/emphasis, không chỉ cao hơn.
- Modal cho mọi thứ → inline edit, slide-over panel, expandable section.
- Avatar tròn tuyệt đối → squircle/rounded square 4–8px.
- Footer 4 cột link farm → tối giản còn đường điều hướng chính + link pháp lý.

## 8. Icon & ảnh

- Lucide/Feather mặc định → Phosphor, Heroicons, hoặc SVG tự vẽ. (Ngoại lệ: dự án đang dùng sẵn → giữ nhất quán.)
- Ẩn dụ mòn: rocket→spark/bolt; shield→fingerprint/vault; kính lúp→finder.
- 1 stroke weight thống nhất toàn bộ; favicon có brand.
- Cấm stock "diverse team smiling at laptops" → ảnh thật, candid, hoặc illustration đồng bộ.
- **Placeholder khi chưa có ảnh thật:** tile monogram brand (gradient brand + chữ cái đầu) — trông có chủ đích; picsum/stock ngẫu nhiên trông như lỗi.

## 9. Hero có ảnh nền (khách LUÔN hỏi mục này)

- Overlay dạng **gradient có vùng bảo vệ chữ**: ~80% phía chữ → 20% phía thoáng; thêm `text-shadow` nhẹ làm lưới an toàn.
- Khách sẽ xin "lộ ảnh thêm" 2–3 lần → nhượng từng nấc, sàn cứng ~70% trên vùng chữ (WCAG). Quá sàn → đổi **ảnh sáng hơn**, không mỏng overlay thêm.
- Prompt sinh ảnh viết theo **layout**, không theo chủ thể: composition thoáng, không focal object đơn lẻ, chi tiết dồn vào vùng UI để trống.

## 10. Code & phần hay quên

- HTML semantic (`nav/main/article/section`) — cấm div soup; cấm inline style trộn class.
- Đơn vị tương đối (`rem/%/max-width`); alt text mô tả thật; z-index theo scale trong biến, cấm `9999`.
- Mọi import phải có trong `package.json`; xóa dead code/comment debug.
- Meta đủ: `<title>`, description, `og:image`; favicon.
- Link pháp lý (privacy/terms) ở footer; 404 có thiết kế; form có validate client-side; skip-link cho keyboard.

---

## Thứ tự sửa (impact lớn → rủi ro thấp)

1. Đổi font → 2. Dọn palette → 3. Hover/active states → 4. Layout & spacing →
5. Thay component cliché → 6. Loading/empty/error states → 7. Polish type scale.

## Checklist bàn giao

**Direction (hỏi trước tiên):**
- [ ] Trang có đúng cảm giác mà design thesis mô tả không?
- [ ] **Signature moment có thật không** — có một khoảnh khắc người xem sẽ nhớ và kể lại?
- [ ] Bỏ direction đi thì trang có khác đi không? Không khác → direction chỉ là giấy tờ.
- [ ] Mọi thứ nằm trong mục C (cliché) hoặc lệch mặc định mục B đều **cố ý và đã ghi lý do**?

**Thi công:**
- [ ] Nhìn như có người chăm chút? (không "feed AI rồi ship")
- [ ] Cliché hiệu ứng: không còn cái nào lọt vào do quán tính?
- [ ] VN/JP render đúng (dấu, ngắt Kanji)? Đã screenshot kiểm tra?
- [ ] Palette/shadow nhất quán với chính nó (dù là hệ nào)?
- [ ] Hover/focus/loading/empty/error đầy đủ?
- [ ] `prefers-reduced-motion` hoạt động? Hiệu ứng đắt ≤ 2?
- [ ] Copy thật, tên thật, số hữu cơ, không cliché?
- [ ] **Cổng dữ liệu thật (mục 6): không còn testimonial/logo/số liệu/chứng chỉ nào tự bịa?
      Placeholder loại B còn sót đã liệt kê trong handoff chưa?**
- [ ] Semantic HTML, alt text, meta, legal links, 404?
