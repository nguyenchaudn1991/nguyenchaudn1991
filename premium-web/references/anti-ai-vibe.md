# Anti AI-Vibe — checklist audit đầy đủ (áp cho mọi type)

Trang phải trông **có chủ đích và handcrafted**. File này là checklist audit — dò từng mục,
mục nào dính thì sửa theo hướng dẫn kèm theo.

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
- **Nhiều accent** → giữ 1, bỏ hết phần còn lại.
- **Trộn gray ấm + lạnh** → 1 họ gray duy nhất, tint theo 1 hue.
- **Gradient tím-xanh "AI"** → nền trung tính + 1 accent; hoặc gradient radial/mesh rất nhẹ.
- **Shadow đen generic** → tinted shadow theo hue của nền (nền xanh → shadow xanh đậm).
- **Accent màu sáng làm text trên nền trắng** → phải có biến thể tối đạt WCAG ≥ 4.5:1 (2 token: `--accent` cho nền sáng, `--accent-bright` chỉ dùng trên nền tối).
- **Glow shadow màu accent trên nền tối** → khách thật đã từng reject; dùng shadow trung tính tối hơn nền, hoặc bỏ.
- **Flat 100% vô hồn** → noise/grain rất nhẹ, hoặc ảnh nền mờ; section trống trơn chỉ chữ trên nền phẳng = chưa xong.
- **Section tối đột ngột giữa trang sáng** → giữ 1 tông xuyên suốt, đậm nhạt cùng palette.
- **Hướng sáng loạn** → mọi shadow theo 1 nguồn sáng (thường top-left).

## 3. Layout

- **Mọi thứ căn giữa + đối xứng** → offset margin, tỷ lệ ảnh trộn, header canh trái trên nội dung giữa.
- **3 card đều nhau làm feature row** → zig-zag 2 cột, lưới 3-2/2-3, masonry, hoặc horizontal scroll.
- **`height: 100vh`** → `min-height: 100dvh` (bug viewport iOS Safari).
- **Không max-width** → container 1200–1440px, margin auto.
- **Border-radius đồng loạt** → trong nhỏ (8–12px), ngoài mềm (16–24px).
- **Không có lớp chồng/độ sâu** → negative margin tạo layering có chủ đích.
- **Thiếu whitespace** → nhân đôi khoảng cách; gap block↔block PHẢI lớn hơn gap heading↔body.
- **Nút trong nhóm card không thẳng hàng đáy** → pin CTA xuống đáy card.
- **Baseline lệch giữa các cột song song** → title/desc/price/CTA cùng Y qua các cột (subgrid).
- **Căn giữa toán học nhưng lệch mắt** → tinh chỉnh quang học 1–2px (icon cạnh chữ, play button).

## 4. Hiệu ứng — blacklist thời AI (thấy là xóa)

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

- Tên người thật theo ngữ cảnh: VN "Trần Hoàng Nam" (không "Nguyễn Văn A"); JP "佐藤 健太" (không "山田太郎"); cấm John Doe.
- Số hữu cơ: `47.2%`, `¥99,800` — không `50%`, `$100.00`.
- Tên công ty tin được — cấm "Acme", "Nexus", "SmartFlow".
- Cấm cliché AI: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Powerful".
- Error message trực tiếp, chủ động: "Không lưu được thay đổi. Thử lại." — cấm "Oops!", cấm bị động, bỏ dấu chấm than trong success message.
- Ngày blog ngẫu nhiên tự nhiên; avatar mỗi người 1 ảnh riêng; cấm Lorem Ipsum; sentence case cho header.
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

- [ ] Nhìn như có người chăm chút? (không "feed AI rồi ship")
- [ ] Không dính mục nào trong blacklist hiệu ứng?
- [ ] VN/JP render đúng (dấu, ngắt Kanji)? Đã screenshot kiểm tra?
- [ ] 1 accent, palette tiết chế, shadow tinted?
- [ ] Hover/focus/loading/empty/error đầy đủ?
- [ ] `prefers-reduced-motion` hoạt động? Hiệu ứng đắt ≤ 2?
- [ ] Copy thật, tên thật, số hữu cơ, không cliché?
- [ ] Semantic HTML, alt text, meta, legal links, 404?
