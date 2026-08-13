---
name: seo
description: >
  Audit và nâng chất lượng SEO + AEO + GEO + E-E-A-T cho Website/Web App: technical SEO,
  schema JSON-LD, local SEO/MEO, tối ưu để AI (ChatGPT, Claude, Perplexity, AI Overviews)
  trích dẫn được, tăng tín hiệu E-E-A-T, hreflang/canonical, sitemap. Dùng khi audit site
  đã có hoặc nâng cấp on-page/technical. KHÔNG dùng khi chỉ tối ưu tốc độ thuần (không có
  mục tiêu SEO), hoặc khi đang build trang mới (on-page cơ bản thuộc skill build web).
allowed-tools: Read, AskUserQuestion
---

# SEO · AEO · GEO · E-E-A-T — audit & nâng cấp

Tầng **audit & tối ưu** cho site đã có. Khi *build* trang mới: on-page cơ bản
(title/meta/heading/alt/JSON-LD) thuộc `premium-web`; sitemap/robots/llms.txt dạng route
động thuộc `hono-stack` — skill này **kiểm tra và nâng cấp** đầu ra đó, không xây lại.
Tối ưu tốc độ thuần (không mục tiêu SEO) thuộc checklist performance của skill build web.

---

## ⚠️ Giới hạn — nói rõ trước khi nhận việc

Skill này cải thiện **điều kiện để được crawl, index và trích dẫn**. Nó **không bảo đảm**
thứ hạng, không bảo đảm được index, không bảo đảm AI sẽ trích dẫn. Ba thứ đó do search
engine và model quyết định, thay đổi liên tục, và không ai cam kết được.

Cách nói đúng với khách: *"đã xử lý hết rào cản kỹ thuật đã biết"* — không phải *"sẽ lên
top"* hay *"sẽ được ChatGPT trích dẫn"*.

## Nhãn bằng chứng — gắn cho MỌI khẳng định trong output

Lĩnh vực này trôi rất nhanh và đầy niềm tin dân gian. Mọi câu trong báo cáo audit phải mang
một trong bốn nhãn:

| Nhãn | Nghĩa | Bắt buộc kèm |
|---|---|---|
| `[Xác minh]` | Có tài liệu chính thức của Google/Bing/OpenAI/Anthropic… | Link + ngày đọc |
| `[Heuristic]` | Thực hành phổ biến, không có tài liệu xác nhận | Nói rõ đây là quy ước nghề |
| `[Thử nghiệm]` | Giả thuyết chưa có bằng chứng | Cách đo để tự kiểm |
| `[Chưa rõ]` | Không biết | Ghi thẳng — **không đoán** |

Luật cứng:

- **Không nâng cấp nhãn khi không có link.** `[Heuristic]` mãi là `[Heuristic]` cho tới khi
  tìm được tài liệu chính thức.
- **Không suy diễn nhân quả với ranking.** "Làm X → tăng hạng" chỉ được viết khi có tài liệu
  chính thức nói vậy. Gần như không bao giờ có.
- Báo cáo gửi khách **giữ nguyên nhãn**, không được lược bỏ cho gọn.

## Routing

| Việc | File PHẢI load |
|---|---|
| Bot đọc được không · index · schema · on-page | [references/technical.md](references/technical.md) |
| Tín hiệu tin cậy · entity · tác giả · Local SEO/MEO | [references/eeat-local.md](references/eeat-local.md) |
| Được AI trích dẫn · AI Overviews · theo dõi | [references/ai-search.md](references/ai-search.md) |

Audit toàn diện → load cả 3. Chỉ hỏi 1 mảng → load đúng file đó.

Mỗi reference có dòng `last_verified` ở đầu. **Cũ hơn ~3 tháng → phải đọc lại nguồn chính
thức trước khi dùng làm căn cứ**, đặc biệt `ai-search.md`.

---

## Quy trình thực thi

1. **Audit trước, sửa sau.** Chấm hiện trạng theo rubric bên dưới, liệt kê từng mục FAIL
   kèm **bằng chứng cụ thể**: URL, đoạn HTML thật, output lệnh, ảnh chụp công cụ.
2. **Sửa theo thứ tự phụ thuộc:** Technical (bot không đọc được thì mọi thứ khác vô nghĩa)
   → E-E-A-T & Schema (định danh thực thể) → On-page → AEO/GEO content → Monitoring.
3. **Kiểm chứng bằng công cụ, không bằng cảm giác** — chi tiết cách kiểm ở từng reference.
4. **Không tự sửa những thứ đang chạy tốt.** Đổi URL, đổi cấu trúc site, gộp trang đều có
   rủi ro mất traffic — đề xuất và giải thích rủi ro, để khách quyết.

## Rubric 100 điểm — thang nội bộ để xếp ưu tiên

> ⚠️ Đây là thang **tự đặt**, dùng để quyết định sửa gì trước. **Không phải chuẩn ngành,
> không map sang thứ hạng, không phải chứng nhận.** Trình bày với khách như một bảng ưu
> tiên công việc — đừng trình bày như điểm thi.

| Trụ | Điểm | Đạt tối đa khi |
|---|---:|---|
| 1. Technical SEO | 20 | Mọi mục technical pass; CWV field data đạt ngưỡng trên mobile |
| 2. On-Page & Semantic | 15 | Mọi mục on-page pass; schema pass validator đúng loại |
| 3. E-E-A-T | 25 | Mọi mục pass; entity đồng nhất toàn web |
| 4. AEO & GEO | 25 | Mọi mục pass; nội dung tự đứng được từng đoạn |
| 5. Content Strategy | 10 | Mọi mục pass |
| 6. Maintenance | 5 | Có lịch theo dõi GSC/Bing + quy trình đồng bộ số liệu |

Ngưỡng "đã xử lý xong": ≥ 95/100, **không mục Technical hoặc E-E-A-T nào FAIL**, mọi schema
pass validator, mọi con số kinh doanh đồng bộ giữa các nơi xuất hiện.

Mục `[Thử nghiệm]` (ví dụ `llms.txt`) **tính 0 điểm** — không được dùng làm điều kiện
nghiệm thu.

---

## 5. Business & Content Strategy — 10đ

- [ ] **Định vị & tone of voice:** xác định rõ chức năng site (phễu lọc chuyên gia hay phễu
      bán đại trà). Định vị cao cấp thì bỏ ngôn từ sales rẻ tiền.
- [ ] **Topic cluster theo pain:** nhắm "pain cluster" của đúng persona thay vì từ khoá
      volume cao sai tệp. Mỗi cluster: 1 trang trụ cột + bài vệ tinh internal link về trụ cột.
- [ ] **Cấu trúc bài dẫn dắt:** pain point → phân tích hệ thống/chuyên môn → giải pháp
      tổng thể → CTA trỏ landing page phù hợp.
- [ ] **1 trang = 1 intent:** không để 2 trang cạnh tranh cùng intent (keyword cannibalization).
      Phát hiện bằng GSC: nhiều URL cùng rank cho 1 query → cân nhắc gộp.
