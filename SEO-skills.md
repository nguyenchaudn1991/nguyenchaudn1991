# SEO, AEO & GEO Mastery Guide (100 Points Standard)

Tài liệu này tổng hợp toàn bộ kỹ năng, tiêu chuẩn và checklist cần thiết để đạt 100 điểm về tối ưu hóa công cụ tìm kiếm truyền thống (SEO), công cụ trả lời tự động (AEO) và công cụ tìm kiếm tạo sinh (GEO). Bạn có thể dùng checklist này như một tiêu chuẩn (Standard) để áp dụng cho mọi dự án Website/Web App.

## 1. Technical SEO (Nền tảng Kỹ thuật)
Đảm bảo website thân thiện với các bot tìm kiếm, crawl và index dữ liệu mượt mà, chính xác.

- [ ] **Tốc độ tải trang & Core Web Vitals:** Đạt điểm xanh trên PageSpeed Insights. Tối ưu **LCP, INP, CLS** (Lưu ý: FID đã bị Google khai tử từ 03/2024, **INP** là metric chính thức thay thế — đừng còn tối ưu theo FID).
- [ ] **JS Rendering & SSR/Prerender (đặc biệt với SPA):** Nếu dự án là SPA (React/Vue/...), nội dung render bằng JS phía client sẽ **vô hình với phần lớn AI crawler** (chúng thường không chạy JS) và yếu với cả Googlebot. **Bắt buộc** prerender/SSR ra HTML tĩnh để nội dung thật nằm trong HTML nguồn (View Source thấy được text), không chỉ trong `<div id="root">` rỗng. Kiểm chứng bằng `curl`/View Source: nếu không thấy nội dung bài viết trong raw HTML → chưa đạt.
- [ ] **Mobile-First & A11y:** Layout chuẩn Mobile-first, responsive hoàn hảo trên mọi thiết bị. Đảm bảo độ tương phản màu sắc (Accessibility/A11y) tốt không bị báo lỗi.
- [ ] **Cấu trúc URL & Đa ngôn ngữ (I18N):**
  - URL ngắn gọn, chứa từ khóa, không chứa ký tự đặc biệt.
  - Setup thẻ `hreflang` và `canonical` tags đầy đủ, chính xác cho các phiên bản ngôn ngữ.
- [ ] **Sitemap & Robots.txt:**
  - `robots.txt` khai báo rõ ràng, không vô tình chặn các bot quan trọng.
  - Sinh XML sitemap tĩnh tự động, và **wire vào build pipeline** (ví dụ: `generate-meta → generate-sitemap → build`) để asset luôn đồng bộ với nội dung mới, tránh sinh/sửa tay file output rồi quên.
  - **Lưu ý cực kỳ quan trọng về `lastmod`:** Thuộc tính `lastmod` (ngày cập nhật) trong Sitemap **chỉ thay đổi khi nội dung thực sự thay đổi**. KHÔNG hardcode tự động cập nhật bằng ngày hiện tại (ngày build system) để tránh việc Google phát hiện tín hiệu giả mạo và phớt lờ toàn bộ sitemap của domain.
- [ ] **Tối ưu hình ảnh (Image SEO):**
  - Nén dung lượng ảnh, dùng định dạng next-gen như WebP.
  - **Bắt buộc** có thẻ `alt` mô tả chính xác ngữ cảnh hình ảnh và chứa từ khóa tự nhiên.
- [ ] **Xử lý Link & Redirect:**
  - **Chống Orphan Pages (Trang mồ côi):** Bất kỳ trang nào sinh ra (Landing page, Blog post) cũng bắt buộc phải có ít nhất 1 internal link trỏ đến từ trang khác đang có traffic.
  - Xử lý mượt mà lỗi 404 và luôn thiết lập Redirect 301 khi thay đổi cấu trúc URL.

## 2. On-Page & Semantic SEO (Tối ưu Nội dung & Cấu trúc Dữ liệu)
Giúp công cụ tìm kiếm hiểu chính xác cấu trúc, bối cảnh của nội dung và định danh đúng thực thể.

- [ ] **Thẻ Meta (Title & Description):**
  - **Front-loading:** Luôn ưu tiên đưa từ khóa ngành/giá trị cao lên ngay đầu thẻ Title và Meta Description để tối đa hóa CTR (Tỷ lệ click).
  - Giới hạn: Title < 60 ký tự, Meta Description < 160 ký tự.
  - Đảm bảo Open Graph (OG) Tags đầy đủ phục vụ Social Sharing.
- [ ] **Heading Tags (H1-H6):**
  - Chỉ dùng 1 thẻ `<h1>` duy nhất cho mỗi trang.
  - Các Heading (`<h2>`, `<h3>`) phải là các câu hỏi hoặc khẳng định rõ nghĩa, chứa từ khóa. Tránh dùng heading mơ hồ như "Tổng quan", "Chi tiết".
- [ ] **Cấu trúc Dữ liệu (Schema Markup / JSON-LD):**
  - **FAQPage Schema:** Bắt buộc cho các trang có phần Hỏi - Đáp. Đảm bảo nội dung trong schema HTML khớp 100% với giao diện để Google không báo lỗi mismatch.
  - **BreadcrumbList:** Mọi trang phụ đều cần có Breadcrumb schema để định vị cấu trúc.
  - **Entity Linking (`sameAs`):** Định danh thực thể chắc chắn bằng cách liên kết (`sameAs`) với các social profile thật (LinkedIn, GitHub, Google Maps...). Giữ **đồng nhất** bộ link này trên mọi trang để Google nối đúng 1 thực thể.
  - **Validate trước khi tin:** Mọi schema phải pass [Rich Results Test](https://search.google.com/test/rich-results) / Schema Validator — không "viết cho có".

## 3. Business & Content Strategy SEO (Chiến lược Nội dung & Kinh doanh)
Đảm bảo nội dung nhắm đúng Persona (chân dung khách hàng) và đi đúng phễu hành trình khách hàng.

- [ ] **Định vị & Tone of Voice:** Xác định rõ chức năng của website (Ví dụ: phễu lọc bài toán chuyên gia hay phễu bán hàng đại trà). Cấm dùng ngôn từ sales rẻ tiền/phổ thông nếu định vị ở mức cao cấp.
- [ ] **Chiến lược Topic Cluster:** Nhắm mục tiêu vào các "Pain Clusters" (Cụm nỗi đau của khách hàng) thay vì chỉ nhắm vào từ khóa có volume cao nhưng sai tệp.
- [ ] **Cấu trúc bài viết dẫn dắt:** Đi từ Pain point (Nỗi đau) ➔ Phân tích góc nhìn (Hệ thống/Chuyên môn) ➔ Đề xuất giải pháp tổng thể ➔ CTA link trỏ về Landing Page phù hợp.

## 4. AEO & GEO (Tối ưu cho AI Search & Answer Engine)
Tối ưu hóa để ChatGPT, Claude, Google SGE (Generative AI) ưu tiên trích dẫn nội dung của dự án. AI tìm kiếm câu trả lời nhanh, định dạng cấu trúc rõ ràng và các data độc quyền.

### Checklist nội dung chuẩn AEO/GEO:
- [ ] **Answer-First (Trả lời ngay lập tức):** 1-2 câu đầu tiên của bài viết (hoặc đoạn) phải trả lời thẳng thừng trực diện câu hỏi của tiêu đề/heading. Đặt TRƯỚC cả đoạn tóm tắt. Đây là đoạn AI hay bốc ra trích dẫn nguyên văn nhất.
- [ ] **TL;DR (Executive Summary):** Luôn có đoạn tóm tắt súc tích bằng 3 gạch đầu dòng (Bài toán ➔ Giải pháp ➔ Kết quả) đặt ở phần đầu bài. Nhồi mật độ LSI keywords (từ khóa ngách) cao tại đây.
- [ ] **Hỏi - Đáp Độc lập (Q&A Pairs):** Cung cấp 2-3 cặp Hỏi - Đáp dạng câu hỏi người dùng hay gõ. Mỗi câu trả lời phải tự đứng độc lập (không cần người/AI đọc đoạn trước mới hiểu ngữ cảnh).
- [ ] **Định nghĩa Thực chiến (Definitional Content):** KHÔNG copy định nghĩa lý thuyết từ Wikipedia. Hãy tự định nghĩa lại các khái niệm từ góc độ thực chiến và kinh nghiệm của dự án. AI ưu tiên các nguồn có trải nghiệm thật (EEAT).
- [ ] **Đóng gói Data & Framework độc quyền:** Thay vì viết luận điểm rời rạc, hãy đóng gói thông tin thành các "Khung quyết định" (Decision Framework), "Ma trận lựa chọn", Checklist, hoặc các con số đúc kết từ dự án thực tế. AI cực kỳ thích trích dẫn cấu trúc framework.
- [ ] **Freshness (Độ tươi mới thật):** Tín hiệu cập nhật phải chuẩn. Chỉ cập nhật thông số ngày sửa đổi (update) khi nội dung thực sự thay đổi — tuyệt đối không fake `dateModified` để giả vờ bài viết mới.
- [ ] **`llms.txt` / `llms-full.txt` (GEO discoverability):** Đặt file `llms.txt` (bản đồ ngắn) và/hoặc `llms-full.txt` (full nội dung dạng Markdown) ở root domain (`/llms.txt`). Đây là chuẩn đang nổi để các LLM (ChatGPT, Claude, Perplexity...) đọc nội dung sạch, không lẫn HTML/JS. Nên **sinh tự động lúc build** từ chính nguồn nội dung (trang tĩnh + blog meta) để khỏi lệch. Mỗi entry nên có: URL, tiêu đề, mô tả 1 dòng, và các bản ngôn ngữ.

## 5. Maintenance & Monitoring (Vận hành & Theo dõi định kỳ)
- [ ] Theo dõi Google Search Console (GSC) định kỳ: Kiểm tra trạng thái Index, xử lý trang Excluded.
- [ ] Xử lý kịp thời nếu có cảnh báo sụt giảm Core Web Vitals.
- [ ] **Đồng bộ thông số:** Nếu có bất kỳ con số kinh doanh cốt lõi nào thay đổi (VD: năm kinh nghiệm, số lượng nhân sự), phải sửa đồng bộ ở mọi nơi (Front-end code, HTML tĩnh, Schema) để AI/Bot không bị mâu thuẫn thông tin khi đọc.
