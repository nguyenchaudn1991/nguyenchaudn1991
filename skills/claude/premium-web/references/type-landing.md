# Type 4 — Landing Page chuyển đổi (LP bán hàng / thu lead)

1 trang, 1 mục tiêu, 1 CTA. Đo bằng chuyển đổi (form gửi, điện thoại gọi, đặt lịch),
không phải bằng độ đẹp. Phù hợp: dịch vụ local (MEO), sản phẩm mới, chiến dịch quảng cáo,
tuyển dụng. Nếu audience Nhật → load thêm japanese-quality.md và theo cấu trúc LP kiểu Nhật bên dưới.

---

## 1. Nguyên tắc

- **1 CTA duy nhất** lặp lại 3–4 lần (sau hero, sau evidence, sau FAQ, sticky mobile). Nhiều mục tiêu = không phải LP, tách trang.
- **First view quyết định:** trong màn hình đầu (không cuộn) phải trả lời được: cho ai — được gì — làm gì tiếp. 3 giây.
- Bỏ nav đầy đủ: header chỉ logo + CTA (giữ user trong phễu); footer chỉ pháp lý + công ty.
- Anti AI-vibe vẫn áp nguyên: LP dễ rơi vào cliché nhất (3 card lợi ích, carousel testimonial, số tròn giả) — soi kỹ mục 6–7 của anti-ai-vibe.md.

## 2. Cấu trúc phễu (thứ tự đã kiểm chứng, kiểu Nhật)

1. **First View:** headline lợi ích cụ thể (không "Elevate your business") + sub 1 dòng + CTA + ảnh/visual thật. Badge tin cậy nếu có thật (実績◯件, ◯年).
2. **共感 (đồng cảm):** 3–4 nỗi đau đúng của khách — "こんなお悩みありませんか？" viết bằng lời khách hàng thật, không lời marketer.
3. **Giải pháp:** dịch vụ giải quyết từng nỗi đau như thế nào — đối chiếu 1-1 với mục trên.
4. **Evidence (khách Nhật đặc biệt cần):** số liệu thật (47件, 92.3%), case study trước/sau, logo khách, testimonial có tên+công ty thật. Không có evidence thật → nói thẳng với anh, đừng bịa.
5. **Flow sử dụng:** お申し込みの流れ 3–4 bước đánh số (01→02→03) — khách Nhật không mua khi chưa thấy quy trình.
6. **料金:** bảng giá rõ, có/không rõ ràng; nhấn 1 gói khuyến nghị bằng màu (không chỉ cao hơn).
7. **FAQ:** 5–8 câu thật (rào cản mua thật sự: giá, hủy, thời hạn, hỗ trợ).
8. **Final CTA + form.**

## 3. CTA & Form (EFO — nơi thắng thua)

- Nút CTA: động từ + lợi ích + giảm rủi ro — "無料で相談する（30秒で完了）" thay vì "送信"/"Submit". Màu accent duy nhất của trang, chỉ CTA được dùng đậm nhất.
- **Form ≤ 5 trường.** Mỗi trường thêm = rớt chuyển đổi. Tên, liên hệ, nội dung — đủ.
- 1 cột dọc; label trên field (không placeholder-làm-label); `autocomplete` + `inputmode` đúng (`tel`, `email`); lỗi inline bằng `:user-invalid`, thông báo cụ thể.
- Mobile: CTA sticky đáy màn hình (ẩn khi form đang hiển thị); nút gọi điện trực tiếp `tel:` cho dịch vụ local.
- Sau submit: trang/màn hình cảm ơn ghi rõ **bước tiếp theo và thời hạn phản hồi** ("1営業日以内にご連絡します").

## 4. Đo lường (LP không đo = LP bỏ đi)

- Gắn event cho: view section (IntersectionObserver), click CTA (vị trí nào), submit form, click tel.
- Script analytics load sau tương tác đầu / `requestIdleCallback` — không được phá LCP.
- Chuẩn bị A/B: headline và CTA text đặt ở đầu file / biến rõ ràng để thay nhanh.
- UTM passthrough vào hidden field của form (biết lead đến từ đâu).

## 5. Tốc độ = tiền quảng cáo

LP thường nhận traffic ads trả tiền — mỗi 0.5s LCP chậm là tiền đốt.
- LP greenfield độc lập: 1 file HTML + CSS inline, ảnh AVIF, **0 framework**; mục tiêu Lighthouse
  mobile ≥ 95. LP trong repo có sẵn giữ framework/bundler hiện hữu và đo theo cùng ngân sách.
- Hero image mobile riêng, nén kỹ; font: 1 family, 2 weight, hoặc system stack.
- Hiệu ứng: tối đa Tier 0 reveal (type-scroll.md) — LP không cần hơn.

## 6. Checklist riêng type này

- [ ] First view: 3 giây hiểu — cho ai / được gì / làm gì?
- [ ] 1 CTA duy nhất, lặp 3–4 điểm, sticky mobile?
- [ ] Evidence là số liệu/case thật (không bịa, không số tròn)?
- [ ] Flow 3–4 bước có đánh số? 料金 minh bạch?
- [ ] Form ≤ 5 trường, autocomplete/inputmode, lỗi inline, thank-you nêu bước tiếp theo?
- [ ] Event tracking đủ (CTA/submit/tel), UTM vào form?
- [ ] Lighthouse mobile ≥ 95?
