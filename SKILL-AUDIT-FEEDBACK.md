# Audit 6 skills — feedback ban đầu theo line và kế hoạch sửa

> **LƯU Ý SAU PHẢN BIỆN (2026-08-13):** Đây là bản audit ban đầu trên 6 ZIP trước khi
> bộ skill được tách thành edition Claude và ChatGPT/Codex Agents. Một số finding trong
> file này áp chuẩn OpenAI lên edition Claude, một số finding đọc sai ngữ cảnh hoặc nâng
> mức P0 quá cao. **Không dùng file này một mình để quyết định sửa.** Đọc tiếp
> [`SKILL-AUDIT-RESPONSE.md`](SKILL-AUDIT-RESPONSE.md) và bản chốt
> [`SKILL-AUDIT-RECONCILIATION.md`](SKILL-AUDIT-RECONCILIATION.md).

**Ngày audit:** 2026-08-13
**Phạm vi:** 6 file ZIP tại thư mục gốc của workspace
**Trạng thái:** Review-only — chưa sửa nội dung bên trong ZIP
**Đối tượng đọc:** tác giả skill, reviewer và Agent tiếp quản việc sửa

## 1. Kết luận ngắn

Hai skill gần mức dùng ổn nhất là `jp-requirement` và `jp-comm`. Bốn skill còn lại cần sửa trước khi coi là production-ready:

- `hono-stack`: có lỗi an toàn thực tế ở auth, JSON-LD, HTML sanitization và remote DB script.
- `premium-web`: có chỉ dẫn tạo tên, số liệu, ngày và avatar “trông thật”; điều này vi phạm nguyên tắc trung thực dữ liệu.
- `seo`: nhiều khẳng định tuyệt đối hoặc lỗi thời, trộn crawler tìm kiếm với crawler training, và biến heuristic thành “điểm chuẩn” không có cơ sở.
- `meo-pptx`: trigger quá rộng, phụ thuộc template/tool không được đóng gói, có ví dụ số liệu bịa và quy tắc mật độ dễ ép Agent bịa thêm nội dung.

Điểm `10/10` trong báo cáo này có nghĩa là skill đáp ứng đủ bảy nhóm tiêu chí **và đã qua forward test**. Nội dung viết hay nhưng chưa được test trên prompt thật thì tối đa chỉ nên coi là release candidate.

## 2. Cách đọc line reference

Quy ước: `archive.zip :: đường/dẫn/trong/zip:Lx-Ly`.

Line number được chốt theo đúng các ZIP có SHA-256 dưới đây. Sau khi sửa, line sẽ dịch; reviewer cần đối chiếu bằng nội dung issue, không chỉ bằng số line.

| Archive | Bytes | SHA-256 |
|---|---:|---|
| `hono-stack.zip` | 12,823 | `154B67C69755ABE267650DAC164FE0323C4660E313D22E6ED87251272F1906C7` |
| `jp-comm.zip` | 11,844 | `189E0B0E3C1E8364F538D02599BF8654B79C2779272BCFE7163894E61CE59CED` |
| `jp-requirement.zip` | 11,809 | `257DA5AE627317981EA7EF7E0805F0E52E5E18D94DADD8EE95E1D289A848701D` |
| `meo-pptx.zip` | 9,960 | `721AD85FD57C209BF8BEE67D3F1B5EE03BD1B01BB8B3C020FD89ACAAF267BC44` |
| `premium-web.zip` | 25,889 | `ECFEABEC0563FD54A9CF33D0D6379D36F195EA1F17FD4754652AA5EB3EF746EE` |
| `seo.zip` | 7,063 | `B9254421686F8F4C6CDE4DDD8DCFC87F58FC2ED13F396EDB636C4C3F4ECD7418` |

## 3. Baseline chấm điểm

| Nhóm | Điểm tối đa | Điều kiện để đủ điểm |
|---|---:|---|
| Trigger và ranh giới phạm vi | 1.5 | Kích hoạt đúng intent, có negative boundary, không giành việc của skill khác |
| Đúng dữ liệu và cập nhật | 2.0 | Không bịa; claim dễ drift có nguồn, ngày kiểm tra và cách refresh |
| Safety và governance | 1.5 | Có guardrail cho security, dữ liệu, approval và hành động không đảo ngược |
| Workflow và tính hành động | 1.5 | Agent biết input, decision gate, output và stop condition |
| Portability và tích hợp | 1.5 | Đóng gói đúng, dependency/tool rõ, có fallback |
| Maintainability | 1.0 | Progressive disclosure, không lặp, reference dài có mục lục |
| Verification | 1.0 | Có validator hoặc forward-test matrix và acceptance criteria |

Điểm review nhanh trước đó chỉ là triage. Audit theo line phát hiện thêm lỗi P0/P1 nên cần hiệu chỉnh:

| Skill | Điểm review nhanh | Điểm audit sâu | Lý do chưa thể 10 |
|---|---:|---:|---|
| `jp-requirement` | 8.5 | **8.2** | Mâu thuẫn rule số phương án, vài câu tuyệt đối, thiếu source precedence/approval authority |
| `jp-comm` | 8.5 | **8.1** | Governance của deemed approval chưa đủ, cadence/SLA bị hard-code, thiếu privacy pre-send check |
| `hono-stack` | 7.5 | **6.8** | Lỗi security và migration có thể gây hậu quả thật; dependency/version chưa quản lý |
| `meo-pptx` | 6.5 | **6.2** | Trigger quá rộng, thiếu asset/template, quy tắc mật độ thúc đẩy bịa nội dung |
| `premium-web` | 7.0 | **6.0** | Có chỉ dẫn tạo social proof giả và nhiều aesthetic rule bị biến thành luật tuyệt đối |
| `seo` | 5.0 | **4.5** | Nhiều factual claim sai/không có nguồn, score tự đặt, crawler taxonomy sai |

> Điểm là thước đo nội bộ để ưu tiên sửa, không phải chứng nhận chính thức của OpenAI.

## 4. Lỗi chung của cả 6 package

### C-01 — ZIP chưa phải trạng thái cài đặt/discoverable

**Vị trí:** cấp package, không gắn với một line.
**Mức độ:** P0 nếu mục tiêu là để Codex tự discover trong repo.

Hiện tại cả sáu skill chỉ nằm dưới dạng ZIP. Codex không tự quét `SKILL.md` nằm trong archive. Cần giải nén thành:

```text
.agents/
└── skills/
    ├── hono-stack/
    │   ├── SKILL.md
    │   └── references/
    └── ...
```

Riêng `meo-pptx.zip` đặt `SKILL.md` ngay ở root archive, khác năm package còn lại. Nếu extract thẳng vào `.agents/skills/`, file có thể rơi sai cấp. Hãy bọc thành `meo-pptx/SKILL.md`.

### C-02 — Frontmatter chứa field không thuộc baseline đang dùng

**Vị trí:**

- `hono-stack.zip :: hono-stack/SKILL.md:L10`
- `jp-comm.zip :: jp-comm/SKILL.md:L11`
- `jp-requirement.zip :: jp-requirement/SKILL.md:L11`
- `premium-web.zip :: premium-web/SKILL.md:L12`

Các file thêm `allowed-tools`. Theo baseline `skill-creator` dùng trong audit này, frontmatter chỉ giữ `name` và `description`. Field lạ có thể bị validator hoặc runtime khác bỏ qua/không tương thích.

**Cách sửa:** xóa `allowed-tools` khỏi YAML. Nếu skill cần dependency/tool, mô tả capability trong workflow và khai báo UI/dependency metadata ở `agents/openai.yaml` khi phù hợp; luôn có fallback nếu tool không khả dụng.

### C-03 — Thiếu metadata và test contract

Không package nào có `agents/openai.yaml`; không package nào có forward-test matrix. `openai.yaml` là optional, nhưng nên thêm `display_name`, `short_description`, `default_prompt` để skill dễ hiểu và dễ gọi trong nhiều môi trường.

Mỗi skill cần tối thiểu:

1. 3 prompt phải trigger.
2. 2 prompt không được trigger.
3. 2 prompt biên/ambiguous.
4. Acceptance criteria cho output.
5. Chạy `quick_validate.py` sau khi unpack.

## 5. Skill `hono-stack`

### Điểm mạnh cần giữ

- Tách core portability khỏi adapter Cloudflare/AWS là hướng kiến trúc tốt.
- Có decision gate theo platform và có checklist build/deploy.
- References cụ thể hơn phần lớn skill kỹ thuật thông thường.

### Issues theo line

| ID | Mức | Line | Vấn đề cụ thể | Cần sửa ra sao |
|---|---|---|---|---|
| H-01 | P1 | `hono-stack/SKILL.md:L15-L18` | Gọi đây là “production pattern” và gắn với một implementation cá nhân/công ty nhưng không có version, provenance hay ngày verify. | Đổi thành “baseline đã dùng ở project X, cần verify lại”; thêm `last_verified`, runtime/version matrix và link tới nguồn chính thức. |
| H-02 | P2 | `hono-stack/SKILL.md:L29` | Discovery chỉ hỏi platform, chưa đủ để quyết định storage, auth, compliance và vận hành. | Trước tiên đọc repo; chỉ hỏi những quyết định không suy ra được. Bổ sung traffic profile, data model, security boundary, region và deployment ownership. |
| H-03 | P1 | `hono-stack/SKILL.md:L48` | Claim “exactly 1 dependency” là snapshot dễ lỗi thời và không phải invariant của kiến trúc. | Xóa con số cứng; thay bằng “giữ core dependency tối thiểu, xác nhận bằng lockfile hiện tại”. |
| H-04 | P1 | `hono-stack/SKILL.md:L49-L51` | Phụ thuộc vào skill khác nhưng package không khai báo dependency và không có fallback. | Ghi rõ optional dependency; nếu thiếu, dùng workflow nội bộ tương đương hoặc dừng với input cần thiết, không giả định skill tồn tại. |
| H-05 | P2 | `hono-stack/SKILL.md:L59-L60` | Tham chiếu “PageSpeed checklist — blueprint §8” không khớp cấu trúc reference; §8 đang là SEO endpoints. | Sửa heading/anchor chính xác hoặc tách checklist performance riêng. |
| H-06 | P0 | `hono-stack/references/blueprint.md:L50` | Bật `Strict-Transport-Security: ...; preload` mặc định có thể khóa cả subdomain vào HTTPS trước khi hạ tầng sẵn sàng. | Chỉ bật `preload` sau checklist: toàn bộ subdomain HTTPS, includeSubDomains hợp lệ, chủ domain chấp thuận và hiểu rollback khó. Default chỉ nên HSTS không preload hoặc do project quyết định. |
| H-07 | P0 | `hono-stack/references/blueprint.md:L54-L59` | CSP mặc định cho phép `'unsafe-inline'`, làm giảm đáng kể giá trị chống XSS. | Dùng nonce/hash cho inline script/style; nếu buộc phải relax, ghi lý do và scope theo route, không copy mặc định. |
| H-08 | P0 | `hono-stack/references/blueprint.md:L112-L113` | `raw(JSON.stringify(obj))` có thể đóng thẻ `<script>` nếu dữ liệu JSON-LD chứa chuỗi không tin cậy. Hono ghi rõ `raw()` không escape. | Dùng serializer an toàn cho script context: escape `<`, `>`, `&`, U+2028, U+2029 trước khi `raw`; chỉ nhận schema đã validate. Thêm XSS regression test với payload `</script><script>...`. |
| H-09 | P0 | `hono-stack/references/blueprint.md:L118-L147` | Auth dùng `ADMIN_PASSWORD` làm session-signing material; verify bằng re-sign/string compare; không thấy CSRF/origin defense. | Tách `SESSION_SECRET`; verify signature bằng Web Crypto, constant-time semantics; rotate/version token; kiểm tra `Origin` hoặc CSRF token cho mutation; đặt cookie `Secure`, `HttpOnly`, `SameSite` theo flow. |
| H-10 | P0 | `hono-stack/references/blueprint.md:L131-L140` | PBKDF2 100,000 iterations thấp hơn guidance OWASP hiện tại; không có algorithm/version migration. | Ưu tiên Argon2id khi runtime hỗ trợ. Nếu cần PBKDF2-HMAC-SHA256, calibrate theo guidance hiện tại và lưu version/cost cùng hash; tại ngày audit OWASP nêu 600,000 cho trường hợp FIPS. |
| H-11 | P0 | `hono-stack/references/blueprint.md:L151-L155` | Regex-based HTML sanitization không đủ chống XSS; “full regex ở repo khác” là dependency không tồn tại trong package. | Thay bằng parser-based allowlist sanitizer đã audit; thêm corpus test cho event handlers, malformed tags, SVG/MathML, encoded payload. Nếu không có sanitizer portable thì lưu plain text/Markdown an toàn. |
| H-12 | P1 | `hono-stack/references/blueprint.md:L167-L168` | Upload tin `Content-Type`/extension và giữ tên người dùng; có thể dẫn tới polyglot, path/key hoặc content-sniffing issue. | Decode/validate magic bytes, re-encode ảnh nếu có thể, randomize storage key, tách display name đã sanitize, giới hạn size/dimension và serve với content headers an toàn. |
| H-13 | P1 | `hono-stack/references/blueprint.md:L170-L171` | Cộng tay `+7h` làm sai epoch và có nguy cơ double-shift. | Lưu UTC; chỉ format lúc hiển thị bằng `Intl.DateTimeFormat(..., { timeZone: 'Asia/Ho_Chi_Minh' })`. |
| H-14 | P1 | `hono-stack/references/blueprint.md:L178` | `llms.txt` bị trình bày gần như requirement crawler, trong khi hiệu quả citation/ranking chưa được chứng minh. | Đưa vào mục “optional experiment”; không tính pass/fail production và không hứa tăng citation. |
| H-15 | P0 | `hono-stack/references/cloudflare.md:L15` | Script `db:remote` chạy `schema.sql`; nếu file chứa DROP/seed, tên lệnh khiến Agent dễ phá dữ liệu live. | Bỏ remote schema reset. Dùng migration tăng dần trong thư mục migrations; bắt buộc explicit environment/database ID, backup/preview và approval trước production migration. |
| H-16 | P1 | `hono-stack/references/cloudflare.md:L17-L19` | Version và typing strategy dễ drift; vừa pin `@cloudflare/workers-types` vừa khuyên generate type bằng Wrangler. | Chọn một source of truth cho bindings/types; pin/test version trong lockfile và có cadence cập nhật. |
| H-17 | P1 | `hono-stack/references/cloudflare.md:L49` | Hard-code `compatibility_date = "2026-01-01"`; ngày này không tự động phù hợp project mới hoặc code cũ. | Dùng ngày đã test của project lúc tạo; ghi policy bump định kỳ và regression test trước khi đổi. |
| H-18 | P1 | `hono-stack/references/cloudflare.md:L113` | Giá/limit hard-code sẽ drift. | Link tài liệu limits/pricing, thêm ngày kiểm tra, yêu cầu Agent refresh trước khi tư vấn chi phí. |
| H-19 | P1 | `hono-stack/references/aws.md:L3-L4` | Claim routes/views/auth “không đổi” mâu thuẫn với khác biệt storage/runtime được mô tả sau đó. | Mô tả portability boundary: route contract có thể giữ; adapter, limits, auth edge và observability phải test riêng. |
| H-20 | P1 | `hono-stack/references/aws.md:L19,L71` | Runtime Node 20 và Node 22 không nhất quán. | Chọn runtime đang được project và AWS hỗ trợ tại thời điểm triển khai; một version trong code, CI và tài liệu. |
| H-21 | P1 | `hono-stack/references/aws.md:L46` | Map D1 sang Aurora hoặc DynamoDB như hai lựa chọn ngang nhau dù transaction/query/ops rất khác. | Thêm decision matrix: access pattern, join/transaction, consistency, scale, cold start, cost và năng lực vận hành. |
| H-22 | P0 | `hono-stack/references/aws.md:L59,L75` | CloudFront + public Lambda Function URL `authType: NONE` có thể cho phép bypass CloudFront/WAF qua origin URL. | Dùng origin access/control phù hợp hoặc IAM/secret-origin verification; threat-model direct-origin bypass và test request thẳng Function URL. |
| H-23 | P2 | `hono-stack/references/blueprint.md:L1-L194` | Reference dài hơn 100 line nhưng không có mục lục; khó progressive disclosure. | Thêm ToC ngắn và tách security/auth/upload thành reference riêng. |

### Điều kiện để lên 10

- Sửa toàn bộ H-06 đến H-12, H-15 và H-22 trước khi dùng làm code-generation baseline.
- Có CI matrix cho shared core, Cloudflare adapter và AWS adapter.
- Có test auth tampering, CSRF, XSS JSON-LD, sanitizer, upload polyglot và direct-origin bypass.
- Version/limits/cost claim có ngày kiểm tra hoặc được chuyển thành link refresh-at-runtime.

## 6. Skill `jp-comm`

### Điểm mạnh cần giữ

- Tập trung vào facts, next update và decision ownership phù hợp bối cảnh Delivery Manager/BrSE.
- Template theo tình huống thực tế, dùng được ngay.
- Quy tắc không biến assumption thành fact là nền tảng tốt.

### Issues theo line

| ID | Mức | Line | Vấn đề cụ thể | Cần sửa ra sao |
|---|---|---|---|---|
| JC-01 | P1 | `jp-comm/SKILL.md:L11` | `allowed-tools` ngoài baseline frontmatter. | Xóa; quản lý capability/dependency qua workflow và metadata phù hợp. |
| JC-02 | P1 | `jp-comm/SKILL.md:L16-L17` | Giả định mọi người nhận đều là senior non-technical trong khi trigger rộng. | Thêm classification: audience, relationship, medium, urgency và mức kiến thức; chọn độ chi tiết theo classification. |
| JC-03 | P1 | `jp-comm/SKILL.md:L39` | “Timing quan trọng hơn content” là tuyệt đối, có thể khuyến khích báo sớm nhưng sai. | Đổi thành: gửi sớm **facts đã xác nhận**, đánh dấu unknown và hẹn giờ update; accuracy không được đánh đổi. |
| JC-04 | P2 | `jp-comm/SKILL.md:L42` | Luôn đưa 2 option làm email thông báo đơn giản dài và giả tạo. | Chỉ bắt buộc option khi cần quyết định/đàm phán; thông báo thuần facts chỉ cần impact, action, next update. |
| JC-05 | P1 | `jp-comm/SKILL.md:L54` | Câu “client chỉ cần gật” mang tính dẫn dắt; nhiều vấn đề chưa đủ hiểu để đưa closed options. | Dùng closed question khi option exhaustive; nếu chưa rõ nhu cầu, hỏi discovery question mở rồi mới đóng quyết định. |
| JC-06 | P1 | `jp-comm/references/situations.md:L11-L12` | “Trong vài giờ” và “trễ tệ hơn incomplete” không gắn severity/SLA. | Dùng agreed incident SLA; luôn ghi timestamp update tiếp theo. Incomplete chỉ được phép khi là dữ kiện đã xác nhận và unknown được nêu rõ. |
| JC-07 | P2 | `jp-comm/references/situations.md:L16` | Bắt đúng 7 section theo thứ tự cho mọi incident làm template cứng. | Giữ mandatory data fields nhưng có biến thể first alert, progress update, resolution và postmortem. |
| JC-08 | P0 | `jp-comm/references/situations.md:L52-L54` | “Không phản hồi coi như approve” chỉ dựa vào low risk; thiếu thỏa thuận governance/contract. | Chỉ dùng deemed approval nếu cơ chế này đã được hai bên thống nhất bằng văn bản, owner rõ, scope đảo ngược được và có deadline/timezone. Nếu chưa có, im lặng không phải approval. |
| JC-09 | P1 | `jp-comm/references/situations.md:L71-L72` | Schedule impact/man-day có thể bị Agent tự suy ra. | Bắt buộc nguồn estimate, owner và timestamp; nếu chưa có, ghi “đang estimate”, không tự điền số. |
| JC-10 | P1 | `jp-comm/references/reporting.md:L28` | 2–3 business days là cadence cứng, không phù hợp incident/change calendar khác nhau. | Dùng SLA/change calendar của project; nếu chưa có, đề xuất cadence và xin xác nhận. |
| JC-11 | P1 | `jp-comm/references/reporting.md:L49` | Completion `%` dễ gây hiểu nhầm nếu denominator thay đổi. | Chỉ dùng khi baseline ổn định; ghi numerator/denominator, scope snapshot và nguồn. Nếu không, dùng milestone/forecast confidence. |
| JC-12 | P2 | `jp-comm/references/reporting.md:L59-L61` | “Luôn manual verify” tốn công và không tạo audit trail nhất quán. | Dùng source-of-truth + timestamp + automated reconciliation; manual review cho exception/high-risk. |
| JC-13 | P0 | `jp-comm/references/qa-management.md:L24-L27` | Lặp lại deemed approval nhưng chưa có governance gate. | Áp dụng cùng guardrail JC-08; QA không tự suy diễn approval từ im lặng. |
| JC-14 | P2 | `jp-comm/references/qa-management.md:L28` | Batch cadence được viết như rule dù chỉ nên là ví dụ. | Gắn nhãn “example”; cadence do defect severity, release gate và SLA quyết định. |
| JC-15 | P1 | Toàn skill | Thiếu privacy/confidentiality pre-send check. | Thêm checklist recipient/CC-BCC, attachment đúng version, customer data, credential/URL nội bộ, channel được phép và retention. |
| JC-16 | P2 | `jp-comm/references/situations.md:L1-L140` | Reference >100 line không có ToC. | Thêm mục lục theo incident/change/delay/meeting/escalation. |

### Điều kiện để lên 10

- Deemed approval chỉ tồn tại sau governance gate rõ ràng.
- Có golden examples cho first incident alert, bad-news update, delay negotiation và QA decision.
- Có privacy pre-send check và test prompt chống tự bịa ETA/man-day.

## 7. Skill `jp-requirement`

### Điểm mạnh cần giữ

- Quy trình từ intent đến requirement/spec có traceability tốt.
- Chú trọng ambiguity, acceptance criteria và bilingual alignment.
- Có cách trình bày option/trade-off phù hợp BrSE.

### Issues theo line

| ID | Mức | Line | Vấn đề cụ thể | Cần sửa ra sao |
|---|---|---|---|---|
| JR-01 | P1 | `jp-requirement/SKILL.md:L11` | `allowed-tools` ngoài baseline frontmatter. | Xóa và khai báo dependency/fallback rõ hơn trong workflow. |
| JR-02 | P1 | `jp-requirement/SKILL.md:L4-L10` | Nhận nhiều loại input nhưng không nói cách xử lý khi thiếu connector/file tool. | Thêm route: đọc file trực tiếp nếu có; dùng connector khi available; nếu không, yêu cầu export/đính kèm. Không giả vờ đã đọc nguồn. |
| JR-03 | P1 | `jp-requirement/SKILL.md:L28-L30` | Gọi peer skill nhưng không khai báo dependency/fallback. | Ghi optional dependency và output contract; nếu skill kia thiếu, chạy reference nội bộ tương ứng. |
| JR-04 | P1 | `jp-requirement/SKILL.md:L39` và `references/requirement-analysis.md:L49-L51,L96` | Mâu thuẫn: một nơi “không bao giờ chỉ một option”, nơi khác cho phép một feasible option. | Rule thống nhất: so sánh ≥2 khi có ≥2 phương án khả thi khác biệt đáng kể; nếu chỉ một, ghi các alternative đã loại và lý do. |
| JR-05 | P1 | `jp-requirement/SKILL.md:L45` | “Mirror vocabulary, không đổi” có thể giữ nguyên thuật ngữ sai/mơ hồ. | Giữ source term để trace; thêm normalized glossary và flag conflict/ambiguity, không tự âm thầm sửa nghĩa. |
| JR-06 | P2 | `jp-requirement/references/requirement-analysis.md:L4` | “Never skip/reorder” quá cứng cho quá trình phân tích vốn lặp. | Chuyển thành required outcomes/gates; cho phép iterate nhưng không bỏ outcome bắt buộc. |
| JR-07 | P0 | `jp-requirement/references/requirement-analysis.md:L15` | Claim “thiếu Why now là thiếu 80%” là số liệu không có nguồn. | Xóa 80%; mô tả hậu quả định tính hoặc trích nguồn thật. |
| JR-08 | P1 | `jp-requirement/references/requirement-analysis.md:L18-L19` | Chặn toàn bộ tiến độ nếu chưa có “why now”. | Đánh dấu open question; tiếp tục phần phân tích reversible không phụ thuộc, chỉ block quyết định bị ảnh hưởng. |
| JR-09 | P1 | `jp-requirement/references/requirement-analysis.md:L38-L40` | Mặc định mọi câu hỏi là closed option có thể bias khách hàng. | Closed question khi option exhaustive; dùng open discovery khi chưa biết solution space. |
| JR-10 | P0 | `jp-requirement/references/requirement-analysis.md:L41-L42` | Cho phép tiếp tục trên assumption nhưng thiếu risk boundary. | Chỉ tiếp tục analysis/prototype reversible; block production implementation, security/compliance, financial commitment và change khó rollback. |
| JR-11 | P2 | `jp-requirement/references/requirement-analysis.md:L52` | Có yêu cầu docs hiện tại nhưng thiếu access date/source priority. | Lưu URL, version/access date; ưu tiên source chính thức, source project và decision record theo thứ tự quy định. |
| JR-12 | P0 | `jp-requirement/references/yoken-teigi.md:L29` | Cho phép approval khi còn unresolved item mà không phân loại severity. | Chỉ cho approve khi item còn lại là non-blocking, owner/deadline rõ. Không approve nếu còn scope, acceptance, security, compliance hoặc cost risk chưa chốt. |
| JR-13 | P2 | `jp-requirement/references/yoken-teigi.md:L54-L56` | Báo khách hàng cho mọi typo gây noise. | Phân biệt editorial correction không đổi nghĩa với requirement change; chỉ loại sau cần approval/change log ngoài. |
| JR-14 | P0 | `jp-requirement/references/spec-breakdown.md:L4-L5` | Hứa dev không cần đọc nguồn và spec “chắc chắn” đúng; guarantee này không thể kiểm chứng. | Nói spec là working contract có traceability; authoritative source vẫn phải accessible, high-risk cần bilingual review. |
| JR-15 | P0 | `jp-requirement/references/spec-breakdown.md:L16-L17` | Cho translator tự quyết khi mơ hồ, kể cả quyết định high-impact. | Translator chỉ đề xuất. Với high-risk/meaning-changing ambiguity phải block và xin authority xác nhận. |
| JR-16 | P1 | `jp-requirement/references/spec-breakdown.md:L35-L38` | Mapping ngữ pháp Nhật sang modality quá tuyệt đối; nghĩa phụ thuộc context/contract. | Dùng như heuristic; ghi exception, quote source và reviewer cho legal/contract/security wording. |
| JR-17 | P1 | `jp-requirement/references/spec-breakdown.md:L53` | DoD yêu cầu số cụ thể có thể thúc Agent tự bịa. | Chỉ dùng số từ source/estimate owner; nếu chưa có, ghi `TBD — owner/date`, không invent. |
| JR-18 | P1 | Toàn skill | Thiếu source precedence, approval authority và conflict-resolution contract. | Thêm thứ tự: signed contract/approved decision > current approved requirement > meeting note > chat; conflict phải log và được authority resolve. Tùy project mà thứ tự được cấu hình. |

### Điều kiện để lên 10

- Một rule duy nhất cho số option, assumption và approval.
- Có trace matrix `source → requirement → acceptance test → approval`.
- Forward test với nguồn mâu thuẫn VI/JP, thiếu “why now”, chỉ có một option và requirement chứa số chưa xác nhận.

## 8. Skill `meo-pptx`

### Điểm mạnh cần giữ

- Art direction rõ, có nhiều pattern slide thực dụng.
- Có ý thức kiểm tra overflow và không che giấu asset thiếu.
- Các mode deck MEO cụ thể, có thể trở thành template skill tốt nếu được đóng gói lại.

### Issues theo line

| ID | Mức | Line | Vấn đề cụ thể | Cần sửa ra sao |
|---|---|---|---|---|
| MP-01 | P0 | Package root | `SKILL.md` nằm thẳng ở root ZIP, không nằm trong thư mục `meo-pptx/`. | Chuẩn hóa `meo-pptx/SKILL.md`, rồi đặt dưới `.agents/skills/meo-pptx/`. |
| MP-02 | P0 | `SKILL.md:L12-L15` | Description trigger cho “flowchart/diagram” nói chung, dễ hijack task Figma, web hoặc architecture không liên quan PPTX/MEO. | Giới hạn intent: tạo/chỉnh deck PowerPoint MEO hoặc user gọi rõ house style này. Thêm negative boundary cho diagram độc lập, web UI và slide không liên quan MEO. |
| MP-03 | P1 | `SKILL.md:L20-L26` | Dựa vào “base PPTX”/tooling bên ngoài nhưng package không chứa asset hay khai báo dependency. | Thêm `assets/meo-base-template.pptx` nếu có quyền phân phối; khai báo dùng presentations skill/tool; nếu thiếu template, chuyển sang draft mode và báo rõ. |
| MP-04 | P1 | `SKILL.md:L32` | Ép tiếng Nhật vô điều kiện. | Nếu skill chỉ dành cho MEO tiếng Nhật, ghi rõ trong description. Nếu không, lấy ngôn ngữ từ user/source và dùng Japanese QA chỉ khi output Nhật. |
| MP-05 | P1 | `SKILL.md:L52-L55` | Mâu thuẫn giữa “user tự overlay” và “template đã supply”. | Tách hai mode: `template-provided` và `content-only`; detect input rồi chọn workflow, không dùng cả hai giả định. |
| MP-06 | P0 | `SKILL.md:L57` | Ví dụ “50%” dù không có source, trái nguyên tắc không bịa số. | Dùng `[XX% — nguồn]` hoặc câu định tính; validator phải fail nếu còn số không có source mapping. |
| MP-07 | P2 | `SKILL.md:L88-L89` | “70% visual weight” khó đo và bị viết như pass/fail. | Gắn nhãn heuristic; acceptance thật là readability, hierarchy, no overflow và source coverage. |
| MP-08 | P1 | `SKILL.md:L146-L170` | Rule mật độ/one-topic cứng có thể tạo slide chật. | Đặt minimum font/spacing và overflow gate trước density; split slide khi không đạt. |
| MP-09 | P1 | `SKILL.md:L177,L294` | Gọi Agent là “Claude”, làm skill không portable và gây nhầm runtime. | Đổi thành “Agent/Codex” hoặc câu trung lập theo capability. |
| MP-10 | P0 | `SKILL.md:L198-L204` | Ép ≥6 node và “concrete data” dù source có thể không đủ, tạo động lực bịa thêm. | Không tạo node/data chỉ để đạt mật độ. Chọn diagram nhỏ hơn hoặc ghi data gap; số node là guideline tối đa/phù hợp, không minimum. |
| MP-11 | P1 | `SKILL.md:L210` | Ví dụ model cụ thể dễ drift. | Dùng `Option A/B` hoặc yêu cầu verify model catalog hiện tại, kèm source/date. |
| MP-12 | P0 | `SKILL.md:L218-L219` | Ví dụ 50–70% và 98% là performance claim không có nguồn. | Thay bằng placeholder có nhãn hoặc source-gated numbers; tuyệt đối không xuất lên customer deck nếu chưa verify. |
| MP-13 | P2 | `SKILL.md:L284-L285` | Bắt mọi slide phải có visual, kể cả khi bảng/text mới chính xác hơn. | Cho structured text/table khi đó là biểu diễn trung thực và dễ đọc nhất. |
| MP-14 | P1 | `SKILL.md:L300-L307` | Tự chèn placeholder slide vào deliverable hoàn chỉnh có thể tạo output không dùng được. | Nếu asset bắt buộc thiếu, dừng và yêu cầu asset hoặc giao bản `DRAFT` được gắn nhãn rõ; không giả vờ final. |
| MP-15 | P1 | `SKILL.md:L313-L316` | Hard-code tool/command (`markitdown`, mechanics) nhưng dependency không bảo đảm tồn tại. | Route qua presentations skill/runtime được bundle; khai báo fallback và kiểm tra command trước khi dùng. |
| MP-16 | P1 | `SKILL.md:L1-L346` | Monolithic dù chứa nhiều variant/mode; không có asset hoặc script QA. | Giữ SKILL.md là router; tách `visual-identity.md`, `technical-mode.md`, `report-mode.md`, `qa.md`; thêm template và script overflow/source-number check. |

### Điều kiện để lên 10

- Đóng gói template thật và workflow render/verify thật.
- Validator bắt overflow, font nhỏ, asset thiếu và số liệu không có source.
- Test cả `template-provided`, `content-only`, output Nhật và prompt diagram không liên quan để bảo đảm không trigger sai.

## 9. Skill `premium-web`

### Điểm mạnh cần giữ

- Có taxonomy page type và reference riêng theo use case.
- Quan tâm performance, responsive state và Japanese typography.
- Có ý thức chống giao diện rập khuôn do AI tạo.

### Issues theo line

| ID | Mức | Line | Vấn đề cụ thể | Cần sửa ra sao |
|---|---|---|---|---|
| PW-01 | P1 | `premium-web/SKILL.md:L4-L11` | Description lệ thuộc danh sách keyword, dễ false-positive/false-negative. | Viết theo intent: build/redesign visually driven frontend; nêu rõ không trigger cho bugfix nhỏ, backend-only, SEO-only hoặc chỉnh copy. |
| PW-02 | P1 | `premium-web/SKILL.md:L12` | `allowed-tools` ngoài baseline frontmatter. | Xóa; khai báo dependency/fallback bằng cấu trúc được hỗ trợ. |
| PW-03 | P2 | `premium-web/SKILL.md:L50-L60` | Lặp phần lớn `anti-ai-vibe.md`, làm skill dài và dễ lệch rule. | SKILL.md chỉ giữ 5 invariant; chi tiết route sang reference. |
| PW-04 | P1 | `premium-web/SKILL.md:L53-L55` | Cấm font/grid đối xứng/gradient như luật phổ quát, có thể phá design system hiện hữu và accessibility. | Áp dụng house style chỉ cho greenfield khi user không có brand; với repo có sẵn, preserve tokens/component language. Biến rule thành heuristic có lý do. |
| PW-05 | P0 | `premium-web/SKILL.md:L56` và `references/anti-ai-vibe.md:L76-L81` | Main skill nói “copy thật” nhưng reference lại bảo tạo tên, số liệu, ngày và avatar trông organic. Đây là social proof giả. | Xóa toàn bộ synthetic proof. Chỉ dùng dữ liệu user cung cấp/verify được; nếu thiếu, dùng placeholder lộ rõ như `[Tên khách hàng]`, `[Số liệu đã xác minh]`, không publish placeholder. |
| PW-06 | P1 | `premium-web/SKILL.md:L59` | Bắt mọi component có hover/focus/loading/error dù state không áp dụng. | Viết “mọi state **có áp dụng**”; interaction phải keyboard/touch-aware và reduced-motion-aware. |
| PW-07 | P1 | `premium-web/SKILL.md:L65` | Trộn FCP lab target với Core Web Vitals/field quality. | Tách field CWV khỏi lab budget; target theo project baseline/device, không coi một số FCP là universal pass. |
| PW-08 | P1 | `premium-web/SKILL.md:L76-L80` | Discovery thiên về brand kit mới, có thể vô tình redesign khi user chỉ cần sửa scoped. | Bước 0 phải inspect existing architecture/design system; chỉ đề xuất brand kit khi greenfield hoặc user yêu cầu redesign. |
| PW-09 | P1 | `premium-web/references/anti-ai-vibe.md:L10-L15` | Font rules cứng như 48px và cấm weight không dựa trên asset thật. | Inspect font files/variable axes; dùng responsive `clamp()` và readability test; không tải weight không dùng. |
| PW-10 | P2 | `premium-web/references/anti-ai-vibe.md:L22,L29,L36` | Saturation <80, asymmetry và decoration bị biến thành công thức “premium”. | Xóa threshold mỹ học không đo được; ưu tiên contrast, hierarchy, brand fit và task clarity. |
| PW-11 | P1 | `premium-web/references/anti-ai-vibe.md:L67-L72` | Hover/animation rule không đủ điều kiện interaction/touch/reduced motion. | Chỉ animate affordance tương tác; có `prefers-reduced-motion`, focus-visible và touch fallback. |
| PW-12 | P0 | `premium-web/references/anti-ai-vibe.md:L76-L82` | Ngoài fake proof, còn gán stereotype “JP Zen/VN social proof”. | Thay bằng evidence từ audience research, analytics và brand brief; không suy diễn theo quốc tịch. |
| PW-13 | P2 | `premium-web/references/anti-ai-vibe.md:L107` | Claim “client sẽ hỏi 2–3 lần” là anecdote không có nguồn. | Xóa hoặc ghi rõ là lesson của một project, không phải universal rule. |
| PW-14 | P1 | `premium-web/references/performance.md:L3` | Protocol Lighthouse 4x đơn giản, thiếu tool/version/device/field-vs-lab. | Ghi reproducible test profile và dùng field data khi có; lab dùng regression, không dùng như business guarantee. |
| PW-15 | P1 | `premium-web/references/performance.md:L35` | “0 bundler, one file” có thể phá cấu trúc project hiện hữu. | Chỉ dùng cho standalone static greenfield; trong repo hiện hữu phải theo build system hiện tại. |
| PW-16 | P1 | `premium-web/references/performance.md:L47-L58` | Dùng modern CSS/API nhưng thiếu compatibility/fallback policy. | Xác định browser support matrix, progressive enhancement và fallback trước khi dùng. |
| PW-17 | P0 | `premium-web/references/performance.md:L72` | Inline critical CSS có thể vi phạm CSP. | Ưu tiên external critical CSS hoặc nonce/hash theo security policy; không khuyên inline vô điều kiện. |
| PW-18 | P1 | `premium-web/references/performance.md:L91` | Lighthouse ≥90 được viết như quality gate phổ quát. | Dùng project-specific lab budget; pass cuối phải gồm accessibility, interaction, console, responsive và field metrics khi có. |
| PW-19 | P2 | `premium-web/references/anti-ai-vibe.md:L1-L135`, `type-scroll.md:L1-L126` | References >100 line không có ToC. | Thêm mục lục; cân nhắc tách data-truth/accessibility khỏi aesthetic patterns. |

### Điều kiện để lên 10

- Xóa hoàn toàn chỉ dẫn fake social proof và thêm `data truth gate` trước publish.
- Tôn trọng design system hiện hữu mặc định; house style chỉ là opt-in.
- Browser QA có responsive, keyboard, reduced motion, console và performance profile tái lập được.

## 10. Skill `seo`

### Điểm mạnh cần giữ

- Bao quát technical SEO, structured data, local SEO và AI-search visibility.
- Có ý thức kiểm tra raw HTML và Search Console.
- Có checklist cụ thể, dễ biến thành audit workflow nếu chuẩn hóa evidence.

### Issues theo line

| ID | Mức | Line | Vấn đề cụ thể | Cần sửa ra sao |
|---|---|---|---|---|
| SEO-01 | P0 | `seo/SKILL.md:L4-L7,L15-L21` | Hứa “100 points”, ranking/citation/perfect outcome mà skill không thể bảo đảm. | Đổi mục tiêu thành audit và cải thiện eligibility/quality; tuyên bố rõ không guarantee crawl, index, ranking hay AI citation. |
| SEO-02 | P1 | `seo/SKILL.md:L31-L38` | Score tự đặt bị gọi là “perfect”; người đọc có thể hiểu là chuẩn ngành. | Gắn nhãn internal prioritization rubric; tách `verified fact`, `heuristic`, `experiment`; không map trực tiếp sang ranking. |
| SEO-03 | P1 | `seo/SKILL.md:L34` | Giả User-Agent GPTBot bằng `curl` không chứng minh bot thật truy cập được. | Kiểm robots/CDN/auth, server log, verified bot IP/reverse-DNS theo docs hiện tại; UA spoof chỉ là smoke test HTTP behavior. |
| SEO-04 | P1 | `seo/SKILL.md:L35,L73` | Rich Results Test không validate mọi Schema.org markup. | Dùng RRT cho loại rich result Google hỗ trợ; dùng Schema Markup Validator/lint JSON-LD cho schema khác; kiểm content parity. |
| SEO-05 | P1 | `seo/SKILL.md:L37,L118` | Prompt thủ công vào ChatGPT bị dùng như deterministic citation test. | Gắn nhãn observational sample; log model/date/query/locale và không suy ra causal ranking từ một lần trả lời. |
| SEO-06 | P1 | `seo/SKILL.md:L53` | Trộn PageSpeed lab “green” với field Core Web Vitals. | Báo riêng CrUX/field và Lighthouse/lab; không fail business outcome chỉ vì một lab run. |
| SEO-07 | P0 | `seo/SKILL.md:L54-L56` | Khẳng định tuyệt đối về JS và trộn mục đích crawler. OpenAI phân biệt `OAI-SearchBot` dùng cho search và `GPTBot` dùng cho training; hai setting độc lập. | Tạo bot-purpose matrix có nguồn/ngày verify. Raw HTML là resilience strategy, không được giải thích sai capability từng bot. Bỏ claim “ChatGPT search dùng Bing” nếu không có nguồn hiện hành. |
| SEO-08 | P1 | `seo/SKILL.md:L57` | Nói fake `lastmod` khiến Google bỏ qua cả sitemap là quá mức. Sitemap vốn là hint, không guarantee indexing. | Nói chính xác: `lastmod` phải phản ánh thay đổi đáng kể; tín hiệu không chính xác có thể bị bỏ qua. Không hứa sitemap tạo index/ranking. |
| SEO-09 | P2 | `seo/SKILL.md:L58` | URL ngắn/keyword/no-special-char bị biến thành hard requirement. | Ưu tiên stable, descriptive, crawlable URL; không rewrite URL đang có chỉ để “ngắn” nếu gây redirect/link risk. |
| SEO-10 | P1 | `seo/SKILL.md:L59` | Gọi accessibility là causal ranking/trust signal không có bằng chứng đủ. | Giữ accessibility vì user quality, compliance và usability; không hứa ranking benefit. |
| SEO-11 | P2 | `seo/SKILL.md:L61` | Bắt mọi page được link từ “traffic page” là rule tùy tiện. | Audit orphan pages và crawl depth; internal link theo information architecture/user journey. |
| SEO-12 | P1 | `seo/SKILL.md:L65-L66` | `<60` title, `<160` description và “exactly one H1” không phải hard Google pass/fail. | Viết concise/descriptive; dùng SERP preview và semantic hierarchy. Multiple H1 không tự động là SEO failure. |
| SEO-13 | P1 | `seo/SKILL.md:L68-L69` | FAQ schema/AI parse và BreadcrumbList “mọi subpage” bị tuyệt đối hóa. | Chỉ markup content thực sự hiện trên page, đúng eligibility hiện hành; breadcrumb schema khi UI/IA có breadcrumb. Không promise AI benefit. |
| SEO-14 | P0 | `seo/SKILL.md:L78` | Nói E-E-A-T “quyết định được cite”; Google nói E-E-A-T không phải một ranking factor cụ thể. | Dùng E-E-A-T như quality lens, đặc biệt trust; không gán causal score/citation guarantee. |
| SEO-15 | P1 | `seo/SKILL.md:L82,L90-L92,L96,L98` | Nhiều câu “AI thích/mất trust” không có nguồn và không đo được. | Chuyển thành hypothesis/heuristic; chỉ nâng thành rule khi có nguồn hoặc experiment tái lập, có giới hạn. |
| SEO-16 | P1 | `seo/SKILL.md:L87,L90` | Person schema field và cùng một `sameAs` trên mọi page bị coi là bắt buộc. | Chỉ dùng property accurate/relevant; xây central entity page/graph rồi reference hợp lý, tránh lặp không cần thiết. |
| SEO-17 | P2 | `seo/SKILL.md:L101` | Yêu cầu NAP giống từng ký tự là quá cứng. | Consistent identity quan trọng, nhưng cho phép format/punctuation theo platform; canonical data source phải rõ. |
| SEO-18 | P1 | `seo/SKILL.md:L103` | “Một location một page” có thể tạo doorway pages nếu nội dung không unique/useful. | Chỉ tạo location page có nhu cầu và nội dung thực sự riêng; nếu không, consolidate. |
| SEO-19 | P0 | `seo/SKILL.md:L110-L115` | Claim “AI extract most often”, “likes” và LSI keyword không có cơ sở; “LSI keywords” là thuật ngữ SEO gây hiểu sai. | Giữ answer-first/table vì readability; bỏ LSI. Mọi nghiên cứu được viện dẫn phải có paper/link, methodology và phạm vi áp dụng. |
| SEO-20 | P1 | `seo/SKILL.md:L114` | “Princeton 2024” không có citation chính xác, nhưng được dùng như rule. | Thêm tên paper/URL/metric/limitations hoặc xóa claim. Không generalize nghiên cứu hẹp thành requirement. |
| SEO-21 | P0 | `seo/SKILL.md:L116` | `llms.txt`/`llms-full.txt` được cho 25 điểm dù chưa có bằng chứng ranking/citation. | Chuyển thành optional experiment 0 điểm; không làm điều kiện release. |
| SEO-22 | P1 | `seo/SKILL.md:L129` | “Dedicated GenAI view” đúng hướng theo rollout tháng 6/2026 nhưng chưa nói chỉ rollout cho một subset site. | Viết “where available”; có fallback annotation + regular performance data nếu property chưa được cấp view. |
| SEO-23 | P1 | `seo/SKILL.md:L1-L132` | Toàn bộ lĩnh vực dễ drift nằm trong một file, gần như không có source/date. | SKILL.md làm router; tách `technical.md`, `structured-data.md`, `local.md`, `ai-search-experiments.md`, `evidence-matrix.md`; thêm `last_verified` từng reference. |

### Điều kiện để lên 10

- Xóa toàn bộ ranking/citation guarantee và mọi số điểm không có evidence contract.
- Bot matrix, structured-data eligibility, CWV và Search Console feature đều có official source + ngày verify.
- Audit output phải phân biệt rõ: `Verified issue`, `Heuristic`, `Experiment`, `Unknown`.
- Forward test trên site SSR, SPA, local business và site không có GenAI report; kiểm tra Agent không bịa outcome.

## 11. Thứ tự sửa đề xuất

### P0 — sửa trước khi cho Agent dùng rộng

1. Unpack đúng `.agents/skills/<name>/` và normalize `meo-pptx`.
2. `hono-stack`: auth/CSRF, JSON-LD XSS, sanitizer, migration remote và public Lambda origin.
3. `premium-web`: xóa synthetic social proof/cultural stereotype.
4. `seo`: xóa guarantee, sửa bot taxonomy, E-E-A-T, `llms.txt` scoring và unsupported causal claims.
5. `meo-pptx`: xóa số liệu giả, bỏ minimum node/data và thu hẹp trigger.
6. `jp-comm`/`jp-requirement`: thêm governance gate cho approval/assumption.

### P1 — làm skill portable và maintainable

1. Xóa frontmatter field ngoài baseline.
2. Thêm `agents/openai.yaml`.
3. Khai báo dependency/fallback.
4. Tách reference theo progressive disclosure; reference >100 line có ToC.
5. Thêm source/date cho claim dễ drift.

### P2 — xác nhận chất lượng thực tế

1. Chạy `quick_validate.py` cho cả sáu thư mục.
2. Viết trigger/non-trigger/boundary prompts.
3. Chạy forward test và lưu output lỗi.
4. Sửa skill dựa trên hành vi thật, không chỉ lint.
5. Chấm lại theo cùng rubric; chỉ cho 10 khi acceptance criteria đều có evidence.

## 12. Definition of Done dùng chung

- [ ] Skill discoverable ở `.agents/skills/<skill-name>/SKILL.md`.
- [ ] YAML chỉ có field được baseline/validator hỗ trợ.
- [ ] Description nêu intent, trigger và negative boundary.
- [ ] Không có invented metric, testimonial, credential, guarantee hoặc ETA.
- [ ] Claim dễ drift có official source và ngày kiểm tra.
- [ ] Hành động destructive/high-risk có approval gate và scope rõ.
- [ ] Dependency/tool không có thì skill có fallback hoặc stop condition trung thực.
- [ ] `SKILL.md` ngắn gọn; variant/details nằm trong references cần thiết.
- [ ] Reference dài có mục lục.
- [ ] `quick_validate.py` pass.
- [ ] Forward test gồm trigger, non-trigger và adversarial/boundary case.
- [ ] Output thực tế đạt acceptance criteria, không chỉ “Agent nói đã xong”.

## 13. Nguồn chuẩn dùng trong audit

- [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI — Crawlers: OAI-SearchBot, GPTBot](https://developers.openai.com/api/docs/bots)
- [Hono — HTML helper và `raw()`](https://hono.dev/docs/helpers/html)
- [Cloudflare Workers — Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
- [Cloudflare Workers — Limits](https://developers.cloudflare.com/workers/platform/limits/)
- [OWASP — Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Google Search — Crawling and indexing](https://developers.google.com/search/docs/crawling-indexing)
- [Google Search — Sitemaps are hints](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google Search — Helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google Search — Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)
- [Google Search — Snippet controls and meta descriptions](https://developers.google.com/search/docs/appearance/snippet)
- [Google Search — GenAI performance reports rollout, June 2026](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)

## 14. Handoff note cho Agent sửa tiếp

Không sửa tất cả bằng search/replace mù. Mỗi issue P0 cần một acceptance test đi kèm. Khi sửa ZIP, nên làm trên thư mục đã unpack, review diff, validate, forward-test rồi mới đóng gói lại nếu thật sự cần phát hành ZIP. Bản trong `.agents/skills/` mới là source of truth để Agent trong repo dùng chung; ZIP chỉ nên là artifact phân phối.
