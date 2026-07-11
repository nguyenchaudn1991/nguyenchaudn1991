# Single Scroll Effect (Hiệu ứng cuộn chuột tối giản cho 1 Video hoặc 1 Ảnh)

Tài liệu này hướng dẫn cách cấu hình hiệu ứng cuộn chuột khi dự án chỉ sử dụng duy nhất **1 video** hoặc **1 hình ảnh tĩnh** làm điểm nhấn, giúp tiết kiệm tối đa thời gian sản xuất và băng thông tải trang.

---

## 1. Phương án A: Chỉ dùng 1 Video duy nhất (Single Video Scrub)
Áp dụng khi bạn có sẵn 1 video lia camera 3D, quay vòng sản phẩm hoặc một đoạn chuyển động tuyến tính ngắn.

### A. Cơ chế hoạt động
Trình duyệt sẽ biến toàn bộ chiều dài trang (hoặc chiều dài container) thành thanh tua để thay đổi `currentTime` của video từ `0` đến hết thời lượng dựa theo vị trí cuộn chuột.

### B. Cách cấu hình
Sử dụng bộ engine tích hợp nhưng bỏ qua mảng `connectors` và chỉ khai báo duy nhất 1 item trong `sections`:
```javascript
mountScrollWorld(document.getElementById('world'), {
  sections: [
    { 
      id: 'single-hero', 
      still: 'assets/hero-still.webp', 
      clip: 'assets/hero-scrub.mp4' 
    }
  ]
  // Không khai báo connectors hay connectorsMobile
});
```

---

## 2. Phương án B: Chỉ dùng 1 Ảnh duy nhất (CSS Parallax & Zoom)
Áp dụng cho các thiết kế tối giản, sạch sẽ (Zen style), chỉ dùng 1 hình ảnh chất lượng cao làm nền và tạo hiệu ứng phóng to/thu nhỏ (Zoom) hoặc dịch chuyển đa tầng khi cuộn trang.

### A. Ưu điểm
*   Tải trang cực nhanh (0% tải video).
*   Không ngốn CPU giải mã trên di động.
*   Hoàn toàn bằng CSS gốc (CSS-Only), đạt điểm PageSpeed tối đa.

### B. Mẫu CSS thực thi (Sử dụng Animation Timeline của trình duyệt)
```css
/* Container tạo không gian cuộn */
.zoom-container {
  height: 150vh; 
  view-timeline-name: --zoom-timeline;
}

/* Ảnh cố định trên màn hình và zoom/blur nhẹ khi cuộn trang */
.zoom-image {
  position: fixed;
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 100dvh;
  object-fit: cover;
  animation: zoom-animation linear both;
  animation-timeline: --zoom-timeline;
  animation-range: entry 0% exit 100%;
}

@keyframes zoom-animation {
  from { 
    transform: scale(1); 
    filter: blur(0px); 
  }
  to { 
    transform: scale(1.25); 
    filter: blur(3px); 
  }
}
```
