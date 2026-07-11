---
name: new-premium-web
description: >-
  Thiết kế và xây dựng website đạt chất lượng hình ảnh cao cấp (Premium), trông như 
  được thiết kế thủ công tinh tế (Handcrafted) bởi designer chuyên nghiệp, không bị 
  rập khuôn AI-vibe (AI smell). Tích hợp tối ưu hiệu năng và PageSpeed bằng Modern Web APIs, 
  và hỗ trợ hiệu ứng cuộn camera bay qua diorama (Scroll-Scrub Diorama).
  Triggers on: thiết kế web, design website, premium website, làm web chuyên nghiệp, 
  tránh AI vibe, tránh AI look, làm web đẹp, thiết kế giao diện, landing page xịn.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# New Premium Web — Quy chuẩn thiết kế thủ công, cao cấp và chuyên nghiệp

Bộ skill này hướng dẫn AI Agent thiết kế và xây dựng các sản phẩm website cao cấp, đảm bảo giao diện **độc bản, tinh tế và có hồn (Handcrafted)**, loại bỏ hoàn toàn các lỗi thiết kế rập khuôn tự động của AI. Đồng thời tích hợp chuẩn kỹ thuật web hiện đại để đạt hiệu năng tối đa.

---

## 1. Nguyên tắc cốt lõi (Không thương lượng)

1. **Không sử dụng bảng màu AI phổ thông:** Tránh tuyệt đối các dải màu gradient tím-xanh neon quá bão hòa, hoặc nền đen kịt dạng `#000000` thuần túy. Những màu này tạo cảm giác rẻ tiền và tự động.
2. **Typography phải có cá tính:** Tránh dùng font mặc định hệ thống hoặc lạm dụng `Inter`/`Open Sans` trên mọi thành phần. Font chữ là tín hiệu thiết kế mạnh mẽ nhất.
3. **Bố cục mang tính dẫn dắt:** Tránh bố cục đối xứng tuyệt đối hoặc hàng 3 thẻ (3-card columns) đều chằn chặn. Hãy phá vỡ sự rập khuôn bằng cách bố trí bất đối xứng, lưới không đồng đều (masonry), hoặc khoảng trống có chủ đích.
4. **Không lạm dụng hiệu ứng phát sáng (glow/neon):** Không sử dụng viền phát sáng, bóng đổ lòe loẹt xung quanh thẻ hoặc nút bấm. Chiều sâu của thiết kế đến từ các lớp màu (layering) và bóng đổ tự nhiên có sắc độ tương thích với nền (tinted shadow).
5. **Hiệu ứng tối giản nhưng mượt mà:** Mọi tương tác phải rẻ về mặt xử lý (chỉ sử dụng `transform`/`opacity` cho hoạt ảnh), đảm bảo không ảnh hưởng đến chỉ số LCP/INP trên di động.

---

## 2. Quy trình thiết kế & triển khai

### Bước 1: Khảo sát khách hàng & Định hình phong cách
1. **Xác định đối tượng khách hàng:** Hỏi khách hàng về lĩnh vực, tệp người dùng mục tiêu và thương hiệu.
2. **Đề xuất Brand Kit độc bản:** Gợi ý bảng màu desaturated (độ bão hòa dưới 80%) kết hợp 1 màu nhấn (accent color) duy nhất và bộ typography phù hợp.

### Bước 2: Thiết kế giao diện & Bố cục (Layout)
1. **Thiết lập Typography:**
   * Tiếng Anh: Ưu tiên font hiện đại như `Geist`, `Outfit`, `Satoshi`, `Cabinet Grotesk`.
   * Tiếng Việt: Sử dụng `Be Vietnam Pro` hoặc `Plus Jakarta Sans` có hỗ trợ Latin Extended chuẩn (tránh lỗi hiển thị dấu tiếng Việt).
2. **Quy hoạch khoảng trống (Whitespace):** Áp dụng quy chuẩn khoảng trắng có phân cấp rõ rệt. Khoảng cách giữa các khối nội dung lớn phải rộng rãi, gấp đôi khoảng cách thông thường để trang web "thở" được.
3. **Bố cục lưới bất đối xứng:** Sử dụng CSS Grid thay vì Flexbox thủ công để chia tỷ lệ khung hình có điểm nhấn (ví dụ lưới 2-1 hoặc 1-3).

### Bước 3: Tối ưu tương tác & Code hiện đại
1. Áp dụng các chỉ dẫn kỹ thuật trong **[modern-web-best-practices.md](references/modern-web-best-practices.md)**.
2. Sử dụng các thẻ HTML5 ngữ nghĩa và các tính năng CSS hiện đại (`:has()`, `@starting-style`, dialog gốc, popover) để giảm tối đa kích thước file Javascript.
3. **Nếu chỉ yêu cầu 1 video hoặc 1 ảnh tĩnh có hiệu ứng cuộn mượt mà (Tối giản):**
   * Đọc và thực thi theo hướng dẫn **[single-scroll-effect.md](references/single-scroll-effect.md)**.
4. **Nếu yêu cầu kể chuyện qua nhiều hoạt cảnh bay liên tục (Diorama World phức tạp):**
   * Đọc và thực thi theo hướng dẫn **[scroll-scrub-diorama.md](references/scroll-scrub-diorama.md)**.

### Bước 4: Kiểm thử chất lượng (Audit)
1. Chạy audit giao diện ở nhiều kích thước màn hình (đặc biệt là di động).
2. Kiểm tra chỉ số PageSpeed (đảm bảo FCP < 1.2s, LCP < 2.5s, CLS < 0.1).
3. Đảm bảo trang web hỗ trợ chế độ giảm chuyển động (`prefers-reduced-motion: reduce`).

---

## 3. Tài liệu tham khảo đi kèm

* **[references/modern-web-best-practices.md](references/modern-web-best-practices.md)**: Các kỹ thuật CSS/JS hiện đại tối ưu hiệu năng PageSpeed.
* **[references/single-scroll-effect.md](references/single-scroll-effect.md)**: Cách cấu hình hiệu ứng cuộn cho duy nhất 1 ảnh hoặc 1 video.
* **[references/scroll-scrub-diorama.md](references/scroll-scrub-diorama.md)**: Quy trình sản xuất video nối bằng Higgsfield cho thế giới nhiều hoạt cảnh.
