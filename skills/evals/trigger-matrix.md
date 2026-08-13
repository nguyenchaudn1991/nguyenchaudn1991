# Trigger matrix — 6 skills

Use this matrix for forward tests after installing an edition into Claude Code, Codex, or
ChatGPT cloud. A pass means the runtime activates only the expected skill, respects the stated
boundary, and does not claim it read files/tools that are unavailable.

## `hono-stack`

| Type | Prompt | Expected |
|---|---|---|
| Trigger | “Dựng API Hono trên Cloudflare Workers, dùng D1 và R2.” | Activate; route Cloudflare reference. |
| Trigger | “Port app Hono hiện tại từ Workers sang AWS Lambda.” | Activate; inspect source first, route AWS reference. |
| Trigger | “Tạo SSR site bằng Hono, deploy được cả Cloudflare và AWS.” | Activate; explain portability boundary. |
| Non-trigger | “Làm landing page React tĩnh, không có backend.” | Do not activate. |
| Non-trigger | “Fix middleware auth của app Express hiện tại.” | Do not activate. |
| Boundary | “Tạo API mới, framework nào cũng được.” | Do not force Hono; ask/choose based on project constraints. |
| Boundary | “Sửa Cloudflare Worker hiện có nhưng project không dùng Hono.” | Do not hijack; use Cloudflare workflow. |

## `jp-comm`

| Type | Prompt | Expected |
|---|---|---|
| Trigger | “Soạn initial incident report tiếng Nhật cho khách, hiện mới xác nhận lỗi login.” | Activate; facts/unknowns/next-update time, no guessing. |
| Trigger | “Tạo Q&A 管理表 để chốt 3 câu hỏi với khách Nhật.” | Activate; discovery questions can be open, decisions closed when exhaustive. |
| Trigger | “Viết weekly report tiếng Nhật cho khách.” | Activate; verify source/status and channel-appropriate tone. |
| Non-trigger | “Phân tích 要件 và viết requirement definition.” | Route to `jp-requirement`. |
| Non-trigger | “Lập 工数見積 cho sprint tiếp theo.” | Do not activate; owned by another process. |
| Boundary | “Viết 議事録 cuộc họp khách Nhật.” | Do not activate; explain boundary briefly. |
| Boundary | “Soạn mail Nhật giúp anh, em tự quyết.” | Activate, infer safe defaults; ask only if missing audience/action changes the result. |

## `jp-requirement`

| Type | Prompt | Expected |
|---|---|---|
| Trigger | “Phân tích requirement Nhật từ Figma và Backlog notes, đề xuất options.” | Activate; read available sources, log conflicts, compare feasible options. |
| Trigger | “Viết 要件定義書 cho chức năng duyệt đơn.” | Activate; include authority, unresolved items and acceptance criteria. |
| Trigger | “Dịch và nhai nhỏ spec Nhật này cho team dev VN.” | Activate; retain source terms, glossary and traceability. |
| Non-trigger | “Soạn mail xin lỗi sự cố bằng tiếng Nhật.” | Route to `jp-comm`. |
| Non-trigger | “Estimate man-day cho tài liệu này.” | Do not activate; owned by another process. |
| Boundary | “Dịch file tiếng Nhật này.” | Ask whether it is a requirement/spec; do not assume. |
| Boundary | “Spec mơ hồ nhưng cứ chọn cách hiểu hợp lý và code production.” | Activate analysis, but block meaning-changing/high-risk assumptions pending authority. |

## `meo-pptx`

| Type | Prompt | Expected |
|---|---|---|
| Trigger | “Tạo file .pptx 技術検討会 cho khách MEO Nhật theo house style của Châu.” | Activate; use custom 10.83 × 7.5 in content canvas. |
| Trigger | “Edit deck MEO này, giữ header/footer template khách và sửa phần content.” | Activate; preserve content canvas/safe area, render QA. |
| Trigger | “Làm 課題検討会 PowerPoint MEO từ số liệu đã cung cấp.” | Activate; no invented metrics, report mode when applicable. |
| Non-trigger | “Vẽ flowchart kiến trúc để nhúng vào README.” | Do not activate. |
| Non-trigger | “Làm slide keynote marketing không liên quan MEO.” | Do not activate. |
| Boundary | “Vẽ MEO flowchart cho tài liệu Word, không cần PowerPoint.” | Do not activate; deliverable is not `.pptx`. |
| Boundary | “Làm PowerPoint cho khách Nhật nhưng không phải MEO.” | Do not activate unless user explicitly requests this house style. |

## `premium-web`

| Type | Prompt | Expected |
|---|---|---|
| Trigger | “Dùng premium-web làm trang scroll experience thật độc lạ cho brand này.” | Activate; propose distinct directions; keep beauty, justify choices. |
| Trigger | “Làm web LP chuyển đổi cho dịch vụ này, em tự quyết visual direction.” | Activate; choose recommended direction and continue without blocking. |
| Trigger | “Tạo trang báo cáo / web report giải trình cho khách Nhật.” | Activate; load report + Japanese references. |
| Non-trigger | “Fix lỗi CSS nút submit đang lệch 2px.” | Do not activate full redesign workflow. |
| Non-trigger | “Thêm API endpoint cho dashboard.” | Do not activate. |
| Boundary | “Làm landing page trong repo React hiện tại.” | Activate; inspect and preserve existing stack/design system. |
| Boundary | “Làm website đẹp hơn, không có keyword/type cụ thể.” | Do not auto-trigger; clarify scope or use general frontend workflow. |

## `seo`

| Type | Prompt | Expected |
|---|---|---|
| Trigger | “Audit SEO + AEO + GEO cho website hiện tại.” | Activate; verify current claims/sources and label evidence. |
| Trigger | “Kiểm tra hreflang, canonical và sitemap đa ngôn ngữ.” | Activate; technical SEO route. |
| Trigger | “Tối ưu local SEO/MEO và schema cho doanh nghiệp Đà Nẵng.” | Activate; no invented business facts. |
| Non-trigger | “Chỉ tối ưu tốc độ JavaScript, không có mục tiêu SEO.” | Do not activate. |
| Non-trigger | “Build landing page mới với on-page cơ bản.” | Keep basic on-page in web-building workflow. |
| Boundary | “Thêm `llms.txt` để chắc chắn ChatGPT trích dẫn site.” | Activate audit context, reject guarantee; treat as experiment. |
| Boundary | “Cam kết đưa site lên top Google trong 30 ngày.” | Activate only to assess SEO; refuse unverified guarantee. |
