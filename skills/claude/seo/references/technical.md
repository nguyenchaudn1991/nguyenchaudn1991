# Technical SEO + On-Page & Semantic

`last_verified: 2026-08-13` — kiểm lại nguồn chính thức nếu quá ~3 tháng.

## Mục lục

- 1. Technical SEO (20đ) — crawl, render, robots, bot matrix, sitemap, URL/i18n, ảnh, link
- 2. On-Page & Semantic (15đ) — title/meta, heading, schema JSON-LD, semantic HTML

---

## 1. Technical SEO — 20đ

### Core Web Vitals

- [ ] `[Xác minh]` Ngưỡng "tốt": **LCP < 2.5s · INP < 200ms · CLS < 0.1**, đo trên **mobile**.
      FID đã ngừng dùng từ 03/2024, INP thay thế — đừng còn tối ưu theo FID.
- [ ] **Phân biệt field và lab.** CrUX/Search Console = dữ liệu người dùng thật, đây mới là
      cái Google dùng. Lighthouse/PageSpeed lab = môi trường mô phỏng, dùng để **tìm nguyên
      nhân và chống hồi quy**. Một lần chạy lab đỏ không có nghĩa site đang tệ với người
      dùng thật, và ngược lại.
- [ ] Báo cáo cho khách phải tách rõ 2 loại. Không kết luận business từ 1 lần chạy lab.

### JS rendering & SSR/prerender (quan trọng với SPA)

- [ ] `[Heuristic]` Nội dung chỉ render bằng JS phía client có rủi ro **không được nhìn thấy**:
      Googlebot có render nhưng theo hàng đợi và có giới hạn; phần lớn crawler của AI
      **không chạy JS**. → SSR/prerender ra HTML tĩnh là chiến lược an toàn, không phụ thuộc
      vào việc bot nào chạy JS được tới đâu.
- [ ] Kiểm chứng bằng raw HTML, không phải DevTools (DevTools hiện DOM sau khi JS chạy):

```bash
curl -sL "<url>" | grep -o "<đoạn nội dung chính>"   # có ra chữ thật không?
curl -sL "<url>" | wc -c                              # rỗng/vài KB = nghi ngờ shell rỗng
```

> ⚠️ `curl -A "GPTBot"` **không chứng minh** bot thật vào được. Đổi User-Agent chỉ test
> xem server có trả nội dung khác theo UA hay không. Muốn biết bot thật có vào được: đọc
> `robots.txt`, kiểm rule ở CDN/WAF/firewall, và **soi server log** tìm request thật
> (verify bằng reverse-DNS/dải IP mà nhà cung cấp công bố).

### robots.txt & chính sách AI bot

- [ ] Không vô tình chặn `Googlebot`/`Bingbot`. Kiểm bằng report của Search Console.
- [ ] **Quyết định có chủ đích với từng bot — và biết rõ mình đang quyết cái gì.**

`[Xác minh — đọc lại doc chính thức của từng bên trước khi tư vấn]`

| Bot | Của | Mục đích | Chặn thì mất gì |
|---|---|---|---|
| `Googlebot` | Google | Crawl cho Google Search | Mất index Google |
| `Bingbot` | Microsoft | Crawl cho Bing | Mất index Bing |
| `OAI-SearchBot` | OpenAI | Lấy nội dung để **hiển thị/trích dẫn trong ChatGPT** | Mất cơ hội xuất hiện trong ChatGPT |
| `GPTBot` | OpenAI | Thu thập dữ liệu **huấn luyện model** | Không ảnh hưởng việc ChatGPT trích dẫn |
| `ClaudeBot` | Anthropic | Crawl nội dung | Xem doc Anthropic cho mục đích hiện hành |
| `PerplexityBot` | Perplexity | Crawl cho Perplexity | Mất cơ hội xuất hiện ở Perplexity |
| `Google-Extended` | Google | Token điều khiển dùng nội dung cho **Gemini/huấn luyện** | **Không ảnh hưởng Google Search** |

**Điểm hay bị nói sai:** "muốn được AI trích dẫn thì allow hết mọi AI bot" là **sai**. Bot
*search* và bot *training* là hai quyết định độc lập — chặn `GPTBot` (training) không làm mất
khả năng được ChatGPT trích dẫn, vì việc đó do `OAI-SearchBot` đảm nhiệm. Chủ site hoàn toàn
có thể cho phép trích dẫn nhưng từ chối làm dữ liệu huấn luyện.

Nguồn phải đọc lại: [OpenAI bots](https://developers.openai.com/api/docs/bots) ·
[Google crawlers](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers)

### Bing / IndexNow

- [ ] `[Heuristic]` Verify Bing Webmaster Tools và bật **IndexNow** để nội dung mới vào index
      Bing/Yandex nhanh hơn. Đây là kênh riêng, đáng làm vì rẻ.
- [ ] `[Chưa rõ]` **Không khẳng định "ChatGPT search dùng index của Bing".** Quan hệ giữa các
      AI search engine và index nền tảng thay đổi theo thời gian; OpenAI hiện vận hành
      crawler riêng (`OAI-SearchBot`). Cần nói gì về chuyện này → đọc doc hiện hành trước.

### Sitemap XML

- [ ] Sinh tự động và **wire vào build pipeline** (`generate-meta → generate-sitemap → build`)
      để luôn đồng bộ, không sửa tay.
- [ ] `[Xác minh]` **Sitemap là gợi ý, không phải lệnh.** Có trong sitemap không bảo đảm được
      index; không có cũng không bảo đảm bị bỏ qua. Đừng hứa với khách "làm sitemap là được
      index".
- [ ] `lastmod` **chỉ đổi khi nội dung thực sự đổi đáng kể**. Nếu tín hiệu này không đáng tin
      (ví dụ hardcode ngày build cho mọi URL), Google có thể **bỏ qua `lastmod`** và tự quyết
      lịch crawl. Nói "Google sẽ phớt lờ toàn bộ sitemap của domain" là **quá lời** — nhưng
      tín hiệu giả thì vô dụng, nên vẫn phải làm đúng.
- [ ] Trang đa ngôn ngữ chỉ xuất URL đúng namespace locale (tránh 404 trong sitemap).

### Cấu trúc URL & i18n

- [ ] URL **ổn định, mô tả được, crawl được** — đó mới là tiêu chí. Ngắn và chứa từ khoá là
      `[Heuristic]` dễ chịu, **không phải hard requirement**.
- [ ] ⚠️ **Không rewrite URL đang chạy tốt chỉ để "đẹp hơn".** Đổi URL = redirect chain, mất
      link equity, rủi ro mất traffic. Chỉ đổi khi có lý do nghiệp vụ rõ ràng, và luôn 301.
- [ ] `hreflang` đầy đủ cho từng phiên bản ngôn ngữ (kèm `x-default`); `canonical` tự trỏ
      chính xác. Hai thẻ này phải nhất quán với nhau và với sitemap.

### Mobile-first & A11y

- [ ] Responsive đúng; contrast đạt WCAG AA; thao tác được bằng bàn phím.
- [ ] `[Heuristic]` Làm accessibility **vì chất lượng sản phẩm, tuân thủ pháp lý và trải
      nghiệm người dùng** — đó là lý do đủ. Không hứa với khách rằng a11y sẽ tăng thứ hạng;
      không có tài liệu chính thức nào nói vậy.

### Image SEO

- [ ] WebP/AVIF, nén; `width`/`height` tường minh để chống CLS; `alt` mô tả đúng ngữ cảnh
      (mô tả thật, không nhồi từ khoá — alt nhồi keyword vừa vô dụng vừa hại a11y).

### Link & redirect

- [ ] **Không có orphan page** — kiểm bằng crawl toàn site, so danh sách URL crawl được với
      sitemap. Internal link đi theo **information architecture và user journey**, không phải
      theo quy tắc "mọi trang phải được link từ trang có traffic".
- [ ] Crawl depth hợp lý (trang quan trọng ≤ 3 click từ home).
- [ ] Đổi URL luôn 301; không để chuỗi redirect A→B→C; 404 có thiết kế và có lối đi tiếp.

---

## 2. On-Page & Semantic SEO — 15đ

### Title & meta description

- [ ] **Front-loading** giá trị/từ khoá lên đầu; mỗi trang một title duy nhất.
- [ ] `[Heuristic]` Độ dài tham khảo: title ~50–60 ký tự, description ~150–160 — đây là
      **ngưỡng hiển thị SERP hay bị cắt**, không phải pass/fail của Google. Kiểm bằng SERP
      preview thay vì đếm ký tự máy móc.
- [ ] `[Xác minh]` Google **có thể tự viết lại** title/description theo truy vấn. Description
      không phải ranking factor — nó là công cụ tăng CTR. Đừng hứa "meta chuẩn là lên hạng".
- [ ] Open Graph + Twitter Card đầy đủ.

### Heading

- [ ] Heading phản ánh đúng **cấu trúc nội dung** — đó là mục tiêu. `<h2>/<h3>` viết thành
      câu hỏi hoặc khẳng định rõ nghĩa; tránh heading mơ hồ kiểu "Tổng quan", "Chi tiết".
- [ ] `[Xác minh]` **Nhiều `<h1>` không phải lỗi SEO.** Google đã nói rõ điều này. 1 `<h1>`
      mỗi trang vẫn là quy ước tốt cho a11y và cho sự rõ ràng — giữ nó như `[Heuristic]`,
      đừng báo FAIL chỉ vì trang có 2 `<h1>`.

### Schema markup (JSON-LD)

- [ ] **Chỉ markup nội dung thực sự hiển thị trên trang.** Markup thứ người dùng không thấy
      là vi phạm guideline structured data.
- [ ] **FAQPage:** Google đã thu hẹp FAQ rich result (từ 08/2023 chỉ còn áp dụng cho một số
      loại site). Vẫn nên làm vì **cấu trúc Q&A rõ ràng giúp cả người đọc lẫn máy parse** —
      nhưng `[Thử nghiệm]` với phần "AI parse tốt hơn", và **không hứa với khách sẽ hiện
      FAQ trên Google**.
- [ ] **BreadcrumbList** khi UI/IA thực sự có breadcrumb — không thêm schema cho thứ không tồn tại.
- [ ] **Article/BlogPosting:** `author` trỏ tới Person (không phải string), `datePublished`/
      `dateModified` là ngày thật.
- [ ] **LocalBusiness** (hoặc subtype đúng ngành: `BeautySalon`, `Restaurant`, `MedicalClinic`…):
      `name`, `address` (PostalAddress đầy đủ), `geo`, `telephone`, `openingHoursSpecification`,
      `priceRange`, `sameAs` trỏ Google Business Profile + map.
- [ ] **Person/Organization** làm entity gốc — chi tiết ở `eeat-local.md`.
- [ ] **Validate bằng đúng công cụ:**
  - [Rich Results Test](https://search.google.com/test/rich-results) — chỉ kiểm **các loại
    rich result Google hỗ trợ**. Schema hợp lệ nhưng không phải loại Google render sẽ
    "không thấy gì" ở đây; đó **không** có nghĩa là markup sai.
  - [Schema Markup Validator](https://validator.schema.org/) — kiểm tính hợp lệ theo
    Schema.org cho mọi loại.
  - Cộng thêm: đối chiếu nội dung trong schema với nội dung hiển thị thật (content parity).

### Semantic HTML

- [ ] `<article>`, `<section>`, `<time datetime>`, list bằng `<ul>/<ol>`, bảng bằng `<table>`
      thật. `[Heuristic]` HTML có cấu trúc dễ parse hơn div-soup cho cả screen reader, trình
      trích xuất nội dung lẫn crawler.
