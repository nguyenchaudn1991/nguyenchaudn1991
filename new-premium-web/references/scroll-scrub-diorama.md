# Scroll-Scrub Diorama (Thiết kế hoạt cảnh tương tác cuộn chuột)

Tài liệu này hướng dẫn cách xây dựng trang web kể chuyện (Storytelling) cao cấp, nơi camera bay xuyên suốt qua các hoạt cảnh 3D/Isometric (diorama) mượt mà dựa trên thao tác cuộn chuột của người dùng.

---

## 1. Nguyên lý chuỗi hoạt cảnh liền mạch (The Seamless Chain)
Để camera bay liên tục không có vết cắt (no cuts), hệ thống sử dụng một chuỗi các video ngắn xếp xen kẽ:
$$\text{Dive 1 (Bay vào cảnh 1)} \rightarrow \text{Connector 1 (Chuyển tiếp)} \rightarrow \text{Dive 2 (Bay vào cảnh 2)} \rightarrow \text{Connector 2} \rightarrow \dots$$

*   **Dive clips:** Đoạn video camera bay từ bên ngoài vào cận cảnh chi tiết một hoạt cảnh.
*   **Connector clips:** Đoạn video camera di chuyển từ chi tiết cảnh trước, bay lên cao hoặc dịch chuyển và hạ cánh xuống điểm bắt đầu của hoạt cảnh tiếp theo.

---

## 2. Quy trình sản xuất Asset với AI (Higgsfield)

### Bước 1: Tạo các ảnh tĩnh 3D Diorama
Sử dụng mô hình tạo ảnh (ví dụ `gpt_image_2`) để tạo ra ảnh tĩnh chất lượng cao cho từng phân đoạn cảnh với cùng một phong cách nghệ thuật (style preamble):
*   *Prompt mẫu:*
    `Soft matte low-poly clay diorama, isometric, tilt-shift miniature, warm light. On a plain solid white background with a soft contact shadow. Pastel green and beige color scheme. Centered, 3:2. Subject: A miniature coffee farm on hills.`

### Bước 2: Tạo các video Dive (Bay vào cảnh)
Từ các ảnh tĩnh đã chọn, sử dụng mô hình AI (như `seedance_2_0` hoặc `kling3_0`) để tạo video camera bay thẳng vào tiêu điểm của bức ảnh.

### Bước 3: Tạo các đoạn video Connector (Chuyển tiếp không vết cắt)
Đây là bước tối quan trọng để tạo hiệu ứng chuyển tiếp mượt mà. Điểm bắt đầu của Connector phải khớp từng khung hình với điểm kết thúc của Dive trước đó, và điểm kết thúc của Connector phải khớp với điểm bắt đầu của Dive sau đó.
1. **Trích xuất khung hình biên:** Sử dụng `ffmpeg` để cắt lấy khung hình cuối cùng của Dive trước và khung hình đầu tiên của Dive sau:
   ```bash
   # Lấy khung hình cuối cùng của Dive 1
   ffmpeg -sseof -0.15 -i dive_1.mp4 -frames:v 1 -q:v 2 dive_1_last.png
   # Lấy khung hình đầu tiên của Dive 2
   ffmpeg -ss 0 -i dive_2.mp4 -frames:v 1 -q:v 2 dive_2_first.png
   ```
2. **Sinh video nối:** Dùng Higgsfield CLI để tạo clip Connector đi từ `dive_1_last.png` sang `dive_2_first.png`:
   ```bash
   higgsfield generate create seedance_2_0 \
     --prompt "Continuous aerial camera transition. Pull back out of scene 1, rise into the sky, glide over the miniature world, and land onto scene 2. No cuts. Warm lighting." \
     --start-image dive_1_last.png --end-image dive_2_first.png \
     --aspect_ratio 16:9 --duration 5 --wait
   ```

---

## 3. Mã hóa Video tối ưu cho tua cuộn (Scrubbing)
Khi người dùng cuộn chuột, trình duyệt sẽ tua nhanh video (`video.currentTime = t`). Việc này ngốn rất nhiều CPU/GPU giải mã. Để tối ưu hóa, hãy sử dụng cấu hình nén video với khoảng cách keyframe cực ngắn (Small GOP) và loại bỏ âm thanh:
*   **Bản Desktop (1080p, `-g 8`):**
    ```bash
    ffmpeg -i input.mp4 -an -vf "unsharp=5:5:0.8:5:5:0.0" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart output.mp4
    ```
*   **Bản Mobile (720p, `-g 4` - Keyframe cực dày để điện thoại tua mượt):**
    ```bash
    ffmpeg -i input.mp4 -an -vf "scale=1280:720,unsharp=5:5:0.8:5:5:0.0" -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart output-m.mp4
    ```

---

## 4. Tích hợp bộ mã nguồn tua cuộn (Scrub Engine)
Sử dụng mã nguồn JS để ánh xạ tọa độ cuộn của người dùng vào thời gian phát video.

### Nguyên tắc lập trình mượt mà:
1. **Tải video qua Blob URL:** Tránh việc trình duyệt gửi yêu cầu range-request liên tục qua mạng. Hãy `fetch` toàn bộ video thành Blob và chuyển thành Object URL:
   ```javascript
   fetch(videoUrl)
     .then(res => res.blob())
     .then(blob => {
       video.src = URL.createObjectURL(blob);
     });
   ```
2. **Sử dụng RequestAnimationFrame (rAF):** Đồng bộ hóa việc cập nhật `currentTime` theo nhịp làm tươi của màn hình để chuyển động không bị xé hình.
3. **Giới hạn số lệnh tua trên Mobile (Coalesce Seeks):** Chỉ thực hiện lệnh gán `currentTime` mới khi trình duyệt đã hoàn tất lệnh tua trước đó (`video.seeking === false`).
4. **Mở khóa Video trên iOS (iOS Priming):** iOS Safari cấm tua video khi chưa có tương tác từ người dùng. Kích hoạt bằng cách cho chạy `play()` rồi `pause()` ngay trong sự kiện tương tác đầu tiên của người dùng (pointerdown).

