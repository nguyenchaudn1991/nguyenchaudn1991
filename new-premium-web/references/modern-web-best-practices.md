# Modern Web Best Practices (Kỹ thuật và API Web Hiện Đại)

Tài liệu này tổng hợp các API trình duyệt hiện đại nhất (Modern Web APIs) giúp giảm tải Javascript rác, tăng tốc độ tải trang (PageSpeed), và tối ưu hóa hiệu năng theo tiêu chuẩn Core Web Vitals (đặc biệt là LCP và INP).

---

## 1. Giao diện & Tương tác (Không dùng JS không cần thiết)

### A. Popover API & Dialog gốc (Modal & Menus)
Tránh sử dụng các thư viện ngoài để tạo modal/tooltip/popover. Hãy dùng các API gốc có sẵn để tối ưu hóa khả năng tiếp cận (Accessibility) và giảm thiểu JS:
* **Hộp thoại (Dialog):** Sử dụng thẻ `<dialog>` gốc.
  ```html
  <dialog id="my-modal">
    <form method="dialog">
      <button>Đóng</button>
    </form>
  </dialog>
  <button onclick="document.getElementById('my-modal').showModal()">Mở Modal</button>
  ```
* **Popover (Menu/Tooltip):** Sử dụng thuộc tính `popover` và `popovertarget`. Tự động xử lý việc đóng khi click ra ngoài mà không cần một dòng JS nào.
  ```html
  <button popovertarget="my-menu">Mở Menu</button>
  <div id="my-menu" popover>
    <p>Nội dung menu...</p>
  </div>
  ```

### B. Neo vị trí phần tử (CSS Anchor Positioning)
Thay vì sử dụng Popper.js hay Floating UI để gắn tooltip/dropdown bên cạnh nút kích hoạt:
```css
.tooltip {
  position: absolute;
  position-anchor: --my-btn;
  top: anchor(bottom);
  left: anchor(center);
  transform: translateX(-50%);
}
```

### C. Hiệu ứng động lúc hiển thị (@starting-style)
Tạo hiệu ứng transition cho các phần tử bắt đầu xuất hiện trên DOM (như Modal hoặc Popover khi mở ra) hoàn toàn bằng CSS:
```css
.modal {
  transition: opacity 0.3s ease, transform 0.3s ease;
  opacity: 1;
  transform: scale(1);
}
@starting-style {
  .modal {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

---

## 2. Layout & Typography Hiện Đại (CSS-First)

### A. Container Queries (Thay thế Media Queries)
Thiết kế component co giãn theo độ rộng của thẻ cha (Container) chứ không theo toàn bộ màn hình, giúp component tái sử dụng cực tốt ở mọi vị trí:
```css
.card-container {
  container-type: inline-size;
}
@container (min-width: 400px) {
  .card {
    display: flex; /* chuyển sang layout ngang khi container đủ rộng */
  }
}
```

### B. Căn chỉnh con hoàn hảo (CSS Subgrid)
Đồng bộ các thành phần bên trong nhiều card khác nhau (ví dụ: tiêu đề card dài ngắn khác nhau nhưng dòng mô tả bên dưới vẫn thẳng hàng nhau):
```css
.card-grid {
  display: grid;
  grid-template-rows: subgrid;
}
```

### C. Phối màu hiện đại (OKLCH & Color-Mix)
* Sử dụng không gian màu `oklch()` để có các gam màu nhất quán, mượt mà và tự nhiên hơn không gian RGB/HSL cũ.
* Tạo màu tint/shade động trực tiếp bằng CSS:
  ```css
  --accent-soft: color-mix(in oklch, var(--accent) 15%, transparent);
  ```

### D. Tinh chỉnh Typography chống lỗi giao diện
* **Chống mồ côi từ (Orphans):** Dùng `text-wrap: balance` cho các tiêu đề (Heading) và `text-wrap: pretty` cho các đoạn văn bản (Body) để trình duyệt tự căn chỉnh dòng thông minh, không bao giờ để một chữ đứng lẻ loi một dòng ở cuối.
* **Tự động co giãn ô nhập liệu:** Dùng `field-sizing: content` trên các thẻ `<textarea>` hoặc `<input>` để chúng tự co giãn theo nội dung gõ vào mà không cần viết script JS autogrow.

---

## 3. Tối ưu hóa hiệu năng (PageSpeed & Core Web Vitals)

### A. Tải trước thông minh (Speculation Rules API)
Khai báo trước cho trình duyệt để nó tải trước hoàn toàn trang tiếp theo trong nền (khi người dùng chuẩn bị hover vào link), giúp chuyển trang ngay lập tức (0ms delay):
```html
<script type="speculationrules">
{
  "prerender": [
    {
      "source": "list",
      "urls": ["/contact.html", "/about.html"]
    }
  ]
}
</script>
```

### B. Bỏ qua dựng hình vùng khuất (Content-Visibility)
Tăng tốc độ tải trang ban đầu bằng cách bỏ qua việc vẽ/dựng hình các phần nằm dưới màn hình (chưa cuộn tới):
```css
.footer-section, .heavy-comments-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px; /* Ước lượng chiều cao để tránh nhảy thanh cuộn */
}
```

### C. Tương tác mượt mà (Nhịp đập INP)
Khi thực hiện các tác vụ tính toán Javascript nặng, hãy sử dụng `scheduler.yield()` (hoặc fallback `requestAnimationFrame`) để nhường luồng xử lý chính (main thread) cho các tương tác của người dùng, tránh gây đơ/lag trang web:
```js
async function runHeavyTask() {
  for (let step of steps) {
    processStep(step);
    if (globalThis.scheduler?.yield) {
      await scheduler.yield(); // Nhường luồng cho tương tác của người dùng
    }
  }
}
```

### D. Báo lỗi form chuẩn xác (:user-invalid)
Chỉ hiển thị lỗi validate form sau khi người dùng đã tương tác và di chuyển ra ngoài ô nhập liệu, tránh việc vừa tải trang đã hiện thông báo lỗi đỏ lòe làm người dùng khó chịu:
```css
input:user-invalid {
  border-color: var(--error-color);
}
```
