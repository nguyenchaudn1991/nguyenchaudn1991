---
name: seo
description: >
  Chuẩn 100 điểm SEO + AEO + GEO + E-E-A-T cho mọi Website/Web App.
  Dùng khi: audit SEO, tối ưu on-page/technical SEO, local SEO/MEO, làm nội dung
  được AI (ChatGPT, Claude, Perplexity, Google AI Overviews) trích dẫn, tăng độ
  tin cậy E-E-A-T, viết schema JSON-LD, llms.txt, hreflang/canonical.
  Triggers: SEO, AEO, GEO, EEAT, E-E-A-T, schema, JSON-LD, sitemap, llms.txt,
  AI Overviews, answer engine, generative engine, audit website, index Google,
  local SEO, Google Business Profile. Do NOT trigger khi chỉ tối ưu
  tốc độ/PageSpeed thuần (không có mục tiêu SEO) hoặc khi đang build trang mới
  (on-page cơ bản đã nằm trong skill build web).
---

# SEO · AEO · GEO · E-E-A-T Mastery Guide (Chuẩn 100 điểm)

Tiêu chuẩn (Standard) áp dụng cho mọi dự án Website/Web App để đạt trạng thái hoàn hảo trên cả 4 trụ:
- **SEO** — Google/Bing crawl, index, rank đúng.
- **AEO** (Answer Engine Optimization) — được bốc làm câu trả lời trực tiếp (Featured Snippet, AI Overviews).
- **GEO** (Generative Engine Optimization) — được ChatGPT/Claude/Perplexity/Gemini trích dẫn làm nguồn.
- **E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness) — tín hiệu tin cậy để cả Google lẫn AI dám dẫn nguồn.

> **Phân công với skill khác (nếu có trong môi trường):** skill này là tầng **audit & tối ưu**.
> Khi *build* trang mới, on-page cơ bản (title/meta/heading/alt/JSON-LD) đã thuộc `premium-web`;
> sitemap/robots/llms.txt dạng route động đã thuộc `hono-stack` — skill này **kiểm tra và nâng cấp**
> các đầu ra đó theo thang điểm dưới, không xây lại từ đầu. Việc tối ưu tốc độ thuần (không mục
> tiêu SEO) thuộc về checklist performance của skill build web.

## 0. Quy trình thực thi (bắt buộc theo thứ tự)

1. **Audit trước, sửa sau.** Chấm điểm hiện trạng theo thang 100 điểm bên dưới, liệt kê từng mục FAIL kèm bằng chứng (URL, đoạn HTML, ảnh chụp lệnh curl).
2. **Sửa theo độ ưu tiên:** Technical (bot không đọc được thì mọi thứ khác vô nghĩa) → E-E-A-T & Schema (định danh thực thể) → On-page → AEO/GEO content → Monitoring.
3. **Kiểm chứng bằng công cụ thật, không tin cảm giác:**
   - `curl -A "GPTBot" <url>` / View Source → nội dung chính phải nằm trong raw HTML.
   - [Rich Results Test](https://search.google.com/test/rich-results) → mọi schema phải pass.
   - PageSpeed Insights → LCP/INP/CLS xanh trên mobile.
   - Gõ thử câu hỏi thương hiệu vào ChatGPT/Perplexity → kiểm tra AI có nhắc/trích đúng thông tin không.
4. **Định nghĩa "hoàn hảo":** ≥ 95/100 điểm, không mục nào ở nhóm Technical và E-E-A-T bị FAIL, mọi schema pass validator, mọi con số kinh doanh đồng bộ 100% giữa các nơi xuất hiện.

## Thang điểm 100

| Trụ | Điểm | Điều kiện đạt tối đa |
| --- | --- | --- |
| 1. Technical SEO | 20 | Mọi checkbox mục 1 pass, CWV xanh mobile |
| 2. On-Page & Semantic | 15 | Mọi checkbox mục 2 pass, schema pass validator |
| 3. E-E-A-T | 25 | Mọi checkbox mục 3 pass, entity đồng nhất toàn web |
| 4. AEO & GEO | 25 | Mọi checkbox mục 4 pass, có llms.txt tự sinh |
| 5. Content Strategy | 10 | Mọi checkbox mục 5 pass |
| 6. Maintenance | 5 | Có lịch theo dõi GSC/Bing + quy trình đồng bộ số liệu |

## 1. Technical SEO (Nền tảng Kỹ thuật) — 20đ

- [ ] **Core Web Vitals:** Đạt điểm xanh PageSpeed Insights bản **mobile**. Tối ưu **LCP < 2.5s, INP < 200ms, CLS < 0.1** (FID đã bị khai tử từ 03/2024 — INP là metric chính thức, đừng còn tối ưu theo FID).
- [ ] **JS Rendering & SSR/Prerender (đặc biệt với SPA):** Nội dung render bằng JS phía client **vô hình với phần lớn AI crawler** (GPTBot, ClaudeBot, PerplexityBot thường không chạy JS) và yếu với cả Googlebot. **Bắt buộc** SSR/prerender ra HTML tĩnh — View Source phải thấy text thật, không chỉ `<div id="root">` rỗng. Kiểm chứng: `curl <url> | grep "<đoạn nội dung chính>"`.
- [ ] **Robots.txt & AI bot policy:** Khai báo rõ ràng, không vô tình chặn Googlebot/Bingbot. **Quyết định có chủ đích** với AI bot: muốn được AI trích dẫn thì phải **allow** `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `OAI-SearchBot` — chặn chúng là tự loại mình khỏi GEO.
- [ ] **Bing/IndexNow:** ChatGPT search dùng index của Bing. Phải verify Bing Webmaster Tools và setup **IndexNow** để nội dung mới vào index Bing nhanh — thiếu Bing là mất kênh GEO lớn nhất.
- [ ] **Sitemap XML:** Sinh tự động và **wire vào build pipeline** (`generate-meta → generate-sitemap → build`) để luôn đồng bộ, không sửa tay. **`lastmod` chỉ đổi khi nội dung thực sự đổi** — hardcode ngày build là tín hiệu giả mạo, Google sẽ phớt lờ toàn bộ sitemap của domain.
- [ ] **Cấu trúc URL & I18N:** URL ngắn, chứa từ khóa, không ký tự đặc biệt. `hreflang` đầy đủ cho từng phiên bản ngôn ngữ (kèm `x-default`), `canonical` tự trỏ chính xác — hai thẻ này phải nhất quán với nhau.
- [ ] **Mobile-First & A11y:** Responsive hoàn hảo, contrast đạt chuẩn WCAG AA. A11y tốt cũng là tín hiệu Trust.
- [ ] **Image SEO:** WebP/AVIF, nén dung lượng, `width/height` để chống CLS, thẻ `alt` mô tả đúng ngữ cảnh chứa từ khóa tự nhiên.
- [ ] **Link & Redirect:** Không orphan page (mọi trang có ≥ 1 internal link từ trang có traffic). 404 xử lý mượt, đổi URL luôn có Redirect 301. Không chuỗi redirect (A→B→C).

## 2. On-Page & Semantic SEO — 15đ

- [ ] **Title & Meta Description:** **Front-loading** từ khóa/giá trị cao lên đầu. Title < 60 ký tự, Description < 160 ký tự, mỗi trang duy nhất. Open Graph + Twitter Card đầy đủ.
- [ ] **Heading:** 1 `<h1>` duy nhất/trang. `<h2>/<h3>` là câu hỏi hoặc khẳng định rõ nghĩa chứa từ khóa — cấm heading mơ hồ kiểu "Tổng quan", "Chi tiết".
- [ ] **Schema Markup (JSON-LD):**
  - **FAQPage** cho trang có Hỏi-Đáp — lưu ý: Google đã **tắt FAQ rich result** cho site thường (chỉ còn gov/health, từ 08/2023) → làm FAQPage vì **AEO/GEO và entity** (AI parse Q&A chuẩn hơn), không hứa với khách là "sẽ hiện sao/FAQ trên Google".
  - **BreadcrumbList** cho mọi trang phụ.
  - **Article/BlogPosting** cho bài viết: `author` trỏ tới Person (không phải string), `datePublished`/`dateModified` thật.
  - **LocalBusiness** (hoặc subtype đúng ngành: `BeautySalon`, `Restaurant`, `MedicalClinic`…) cho doanh nghiệp có địa điểm: `name`, `address` (PostalAddress đầy đủ), `geo`, `telephone`, `openingHoursSpecification`, `priceRange`, `sameAs` trỏ Google Business Profile + map.
  - **Person/Organization** làm entity gốc (chi tiết ở mục 3).
  - **Validate trước khi tin:** mọi schema phải pass Rich Results Test — không "viết cho có".
- [ ] **Semantic HTML:** `<article>`, `<section>`, `<time datetime>`, danh sách dùng `<ul>/<ol>`, bảng dùng `<table>` thật — AI parser trích bảng/list HTML chuẩn dễ hơn nhiều so với div-soup.

## 3. E-E-A-T (Experience · Expertise · Authoritativeness · Trust) — 25đ

Đây là trụ quyết định việc Google VÀ các AI engine có **dám trích dẫn** không. Từng chữ một phải có bằng chứng máy đọc được:

### Experience (Trải nghiệm thực)
- [ ] **Bằng chứng "tôi đã làm":** Case study có số liệu thật (con số, thời gian, quy mô), ảnh chụp/diagram tự làm — không dùng stock/AI image cho phần bằng chứng. Nội dung viết từ góc nhìn người trực tiếp làm ("chúng tôi đã triển khai X, gặp lỗi Y, xử lý bằng Z").
- [ ] **Định nghĩa thực chiến:** KHÔNG copy định nghĩa Wikipedia. Tự định nghĩa lại khái niệm từ kinh nghiệm dự án — AI ưu tiên trích nguồn có trải nghiệm gốc thay vì nguồn nhai lại.

### Expertise (Chuyên môn)
- [ ] **Byline mọi bài viết:** Mỗi bài có tên tác giả, link tới trang tác giả. Không bài nào "vô danh".
- [ ] **Trang tác giả/About chuẩn entity:** 1 trang "Về tôi/About" duy nhất làm **entity home**, liệt kê credential thật (năm kinh nghiệm, chứng chỉ, chức danh, dự án). Đây là trang canonical để mọi máy hiểu "người này là ai".
- [ ] **Person schema đầy đủ:** `jobTitle`, `worksFor`, `knowsAbout` (list chủ đề chuyên môn), `hasCredential` (chứng chỉ), `alumniOf` — máy đọc được chuyên môn chứ không chỉ người đọc.

### Authoritativeness (Thẩm quyền)
- [ ] **Entity Linking (`sameAs`) đồng nhất:** Person/Organization schema liên kết `sameAs` tới đúng bộ profile thật (LinkedIn, GitHub, Google Maps, X...). **Cùng 1 bộ link trên mọi trang** — lệch nhau là Google tách thành nhiều thực thể.
- [ ] **Nhất quán tên/thông tin cross-platform:** Tên, chức danh, mô tả trên website = LinkedIn = GitHub = mọi profile. AI model học entity từ toàn bộ web — mâu thuẫn ở đâu là loãng thẩm quyền ở đó.
- [ ] **Được nhắc đến ngoài domain:** Guest post, phỏng vấn, directory ngành, mention trên nguồn uy tín. GEO research cho thấy AI ưu tiên entity xuất hiện trên nhiều nguồn độc lập.

### Trustworthiness (Tin cậy)
- [ ] **HTTPS toàn site, trang Liên hệ thật** (form/email/địa chỉ hoạt động), Privacy Policy nếu thu thập dữ liệu.
- [ ] **Không fake tín hiệu:** Không fake `dateModified`, không fake review, không nhồi credential không có thật. Một tín hiệu giả bị phát hiện → mất trust toàn domain.
- [ ] **Trích nguồn khi nêu số liệu ngoài:** Số liệu không phải của mình thì link tới nguồn gốc (primary source). Số liệu của mình thì nêu rõ bối cảnh đo (dự án nào, thời điểm nào).
- [ ] **Đồng bộ số liệu tuyệt đối:** Một con số kinh doanh (năm kinh nghiệm, số nhân sự, số khách hàng) xuất hiện ở N nơi (UI, HTML tĩnh, schema, llms.txt, README, LinkedIn) thì cả N nơi phải giống nhau — AI đọc chéo và mất trust khi thấy mâu thuẫn.

### Local SEO / MEO (khi doanh nghiệp có địa điểm phục vụ)
- [ ] **NAP đồng nhất tuyệt đối:** Name–Address–Phone trên website = Google Business Profile = mọi directory/map/SNS, **từng ký tự** (cách viết tầng/phòng, dấu cách, số điện thoại có/không mã vùng). Lệch NAP là tín hiệu local xấu nhất.
- [ ] **Google Business Profile là entity local gốc:** category chính xác, giờ mở cửa thật, ảnh thật định kỳ, review được trả lời; website ↔ GBP link 2 chiều (`sameAs` trong LocalBusiness schema trỏ GBP/map URL).
- [ ] **1 địa điểm = 1 trang riêng** trên website (URL riêng, LocalBusiness schema riêng, nội dung riêng theo khu vực) — không gộp nhiều chi nhánh vào 1 trang.
- [ ] **Tín hiệu khu vực trong nội dung:** tên khu vực xuất hiện tự nhiên trong title/H1/nội dung/alt; đường đi, landmark gần đó — đúng ngôn ngữ khách địa phương dùng khi tìm.

## 4. AEO & GEO (Tối ưu cho AI Search & Answer Engine) — 25đ

Tối ưu để ChatGPT, Claude, Perplexity, Google AI Overviews ưu tiên trích dẫn. AI tìm: câu trả lời đứng độc lập, cấu trúc rõ, data độc quyền, entity đáng tin.

- [ ] **Answer-First:** 1-2 câu đầu tiên của bài (và của mỗi section) trả lời thẳng câu hỏi của tiêu đề/heading — đặt TRƯỚC cả đoạn dẫn nhập. Đây là đoạn AI bốc trích nguyên văn nhiều nhất.
- [ ] **TL;DR (Executive Summary):** 3 gạch đầu dòng (Bài toán → Giải pháp → Kết quả) ở đầu bài, mật độ LSI keywords cao.
- [ ] **Q&A Pairs độc lập:** 2-3 cặp Hỏi-Đáp theo câu người dùng hay gõ. Mỗi câu trả lời **tự đứng được** — không cần đọc đoạn trước vẫn hiểu (AI trích từng đoạn rời, không trích cả bài).
- [ ] **Đóng gói Framework/Data độc quyền:** Decision Framework, ma trận lựa chọn, checklist, con số đúc kết từ dự án thật. AI cực thích trích cấu trúc framework có tên riêng.
- [ ] **Thống kê + trích dẫn trong bài:** GEO research (Princeton, 2024) chỉ ra thêm **số liệu thống kê, trích dẫn nguồn, và quote chuyên gia** làm tăng đáng kể khả năng được generative engine dẫn nguồn — áp dụng cả 3 vào bài trụ cột.
- [ ] **Bảng so sánh:** Nội dung dạng "A vs B", "trước vs sau" đóng thành `<table>` HTML thật — AI Overviews và Perplexity trích bảng rất thường xuyên.
- [ ] **`llms.txt` / `llms-full.txt`:** Đặt ở root domain. `llms.txt` = bản đồ ngắn (mỗi entry: URL, tiêu đề, mô tả 1 dòng, các bản ngôn ngữ); `llms-full.txt` = full nội dung Markdown sạch. **Sinh tự động lúc build** từ chính nguồn nội dung để không lệch.
- [ ] **Freshness thật:** Cập nhật nội dung trụ cột định kỳ với thông tin mới thật, khi đó mới đổi `dateModified`. Tuyệt đối không fake ngày.
- [ ] **Kiểm chứng đầu ra GEO:** Định kỳ hỏi ChatGPT/Perplexity/Claude các câu hỏi thuộc chủ đề của site → ghi lại site có được nhắc/trích không, thông tin có đúng không. Sai thì truy ngược nguồn AI đang đọc để sửa.

## 5. Business & Content Strategy — 10đ

- [ ] **Định vị & Tone of Voice:** Xác định rõ chức năng site (phễu lọc chuyên gia hay phễu bán đại trà). Cấm ngôn từ sales rẻ tiền nếu định vị cao cấp.
- [ ] **Topic Cluster theo Pain:** Nhắm "Pain Clusters" của đúng persona thay vì từ khóa volume cao sai tệp. Mỗi cluster: 1 trang trụ cột + các bài vệ tinh internal link về trụ cột.
- [ ] **Cấu trúc bài dẫn dắt:** Pain point → Phân tích góc nhìn hệ thống/chuyên môn → Giải pháp tổng thể → CTA trỏ về Landing Page phù hợp.
- [ ] **1 trang = 1 intent:** Không để 2 trang cạnh tranh cùng 1 từ khóa/intent (keyword cannibalization).

## 6. Maintenance & Monitoring — 5đ

- [ ] **Google Search Console + Bing Webmaster Tools định kỳ:** Trạng thái index, trang Excluded, cảnh báo CWV, số lần xuất hiện trên AI Overviews (GSC đã tách báo cáo).
- [ ] **Theo dõi AI referral traffic:** Phân tách traffic từ `chatgpt.com`, `perplexity.ai`, `gemini.google.com`... trong analytics — đây là KPI của GEO.
- [ ] **Quy trình đồng bộ số liệu:** Bất kỳ con số kinh doanh cốt lõi nào thay đổi → sửa đồng loạt mọi nơi (front-end, HTML tĩnh, schema, llms.txt, profile ngoài) trong cùng 1 lần.
