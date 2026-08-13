# Skills — 2 edition

Cùng 1 bộ 6 skill, đóng gói thành 2 bản vì runtime khác nhau có convention khác nhau.
Nội dung nghiệp vụ **giống hệt**; chỉ khác phần giao tiếp với runtime.

```
skills/
├── claude/           # Claude Code / claude.ai
└── chatgpt-agents/   # ChatGPT/Codex, Gemini CLI, và các agent runtime khác
```

## Cài đặt

| Runtime | Chép vào | Ghi chú |
|---|---|---|
| Claude Code (user-level) | `~/.claude/skills/<name>/` | Dùng được ở mọi project |
| Claude Code (project-level) | `<repo>/.claude/skills/<name>/` | Chỉ trong repo đó |
| Codex | `<repo>/.agents/skills/<name>/` | Bản `chatgpt-agents/` |
| Runtime khác | theo convention của runtime đó | Bản `chatgpt-agents/` |

Cấu trúc mỗi skill đã chuẩn hoá thành `<name>/SKILL.md` (+ `references/` nếu có),
nên giải nén/chép thẳng vào thư mục skill của runtime là chạy.

## Khác nhau giữa 2 edition

Delta rất nhỏ. Gần như toàn bộ nằm trong `SKILL.md`; `references/` giống hệt nhau
byte-for-byte ở 2 bản, **trừ đúng 1 dòng** trong `meo-pptx/references/report-mode.md`
(xưng hô runtime).

| | `claude/` | `chatgpt-agents/` |
|---|---|---|
| `allowed-tools` trong frontmatter | Chỉ pre-approve `Read, AskUserQuestion`; Bash/Write/Edit/WebFetch vẫn phải xin quyền khi cần. Field này không phải allowlist hạn chế tool và không có tác dụng tương tự trong Claude Agent SDK | **Bỏ** — chỉ còn `name` + `description` theo baseline OpenAI |
| Xưng hô runtime | "Claude" | "the agent" |
| Peer skill (`jp-comm`, `meo-pptx`…) | Giả định có, gọi qua tool `Skill` | Khai báo **optional + fallback** rõ ràng |
| Tool ngoài (pptxgenjs, markitdown, MCP Figma) | Thường có sẵn | Bắt buộc **check trước khi chạy**, có stop condition trung thực |

Không dùng số dòng chênh lệch làm chuẩn vì nội dung sẽ tiếp tục phát triển; dùng danh sách file
và loại delta ở bảng trên để kiểm tra drift.

## Quy tắc sync khi sửa nội dung

Vì delta chỉ nằm ở `SKILL.md`:

1. Sửa `references/` → chép thẳng từ edition này sang edition kia.
   Ngoại lệ duy nhất: `meo-pptx/references/report-mode.md` — chép xong nhớ đổi lại
   "Claude" ↔ "the agent" ở dòng `Allowed (…builds these)`.
2. Sửa `SKILL.md` → sửa ở `claude/` trước, port sang `chatgpt-agents/`, rồi **giữ nguyên 4 delta
   trong bảng trên**.
3. Kiểm tra lại delta chưa bị trôi:

```bash
diff -r skills/claude skills/chatgpt-agents
```

Kết quả mong đợi: đúng **7 file** khác nhau — cả 6 `SKILL.md` và
`meo-pptx/references/report-mode.md` — và mọi khác biệt đều thuộc 4 loại trong bảng trên.

Validator không cần dependency:

```bash
node skills/scripts/validate-skills.mjs
```

Script kiểm tra đủ 6 skill ở cả hai edition, frontmatter theo runtime, link nội bộ, mục lục cho
reference dài, drift ngoài allowlist và các câu hướng dẫn cũ đã bị loại.

Forward-test cases nằm ở [`evals/trigger-matrix.md`](evals/trigger-matrix.md): mỗi skill có
3 trigger, 2 non-trigger và 2 boundary prompt để chạy lại trên từng runtime sau khi cài.

## Đã sửa

**`meo-pptx` — tách reference + rút trigger (2026-08-13).** SKILL.md trước đây 345 dòng,
0 reference: mỗi lần vẽ 1 diagram vẫn phải đọc cả 9 pattern + Report mode. Đã tách theo
nguyên tắc **giữ cái luôn cần, tách cái có điều kiện**:

| | Trước | Sau |
|---|---:|---:|
| `SKILL.md` | 345 dòng | **304** |
| `references/diagrams.md` | — | 98 |
| `references/report-mode.md` | — | 25 |
| `description` | 128 từ | **61** |

Nội dung **không bị cắt** — tổng còn nhiều hơn trước. Mục đích là để
`diagrams.md` phình thoải mái khi thêm pattern mới mà không làm loãng luật cứng ở §0.
Description bỏ danh sách keyword và bỏ vế `even if "MEO" or "pptx" is not mentioned`
(nguyên nhân over-trigger — MP-02).

`seo` từng có cùng vấn đề (131 dòng, 0 reference) — đã xử lý, xem mục bên dưới.

**`hono-stack` — dọn security (2026-08-13).** Toàn bộ P0 + P1 đã được implement trong source,
nhưng chưa được coi là verified cho tới khi chạy test ở phần Trạng thái:

| | Trước | Sau |
|---|---|---|
| Script `db:remote` chạy `schema.sql` (có `DROP TABLE`) | xoá sạch DB production | **Bỏ hẳn.** `schema.sql` chỉ local; production đi qua `migrations/` + gate 4 bước |
| Sanitizer HTML | regex tự viết, trỏ file không có trong package | Allowlist parser-based + bảng allowlist + corpus test XSS |
| Ký session | dùng luôn `ADMIN_PASSWORD` | Tách `SESSION_SECRET`; verify bằng `crypto.subtle.verify` (constant-time); token có version |
| JSON-LD | `raw(JSON.stringify(obj))` | `jsonLdScript()` escape `<` `>` `&` U+2028/2029 + test regression |
| Lambda Function URL | `authType: NONE` (bypass được CloudFront/WAF) | `AWS_IAM` + CloudFront OAC; test `curl` thẳng phải ra 403 |
| HSTS | `preload` mặc định | Bỏ `preload`, kèm điều kiện bật |
| PBKDF2 | hard-code 100.000 vòng | Trỏ OWASP + lưu `iter` trong hash + re-hash khi đăng nhập |
| Upload | tin `Content-Type`, giữ tên file user | Magic bytes + key `randomUUID()` do server sinh + `nosniff` |
| Múi giờ | cộng tay `+7h` | `Intl.DateTimeFormat` với `timeZone` |

Thêm mục lục cho `blueprint.md` (194 → 305 dòng), và 6 dòng mới trong bảng
"Common mistakes" của SKILL.md để các bẫy trên bị chặn ngay từ file gốc.

**`seo` — factual drift + tách reference (2026-08-13).** Skill điểm thấp nhất, sửa nặng nhất:

| | Trước | Sau |
|---|---|---|
| Cấu trúc | 131 dòng, 0 reference | SKILL.md 107 + 3 reference (361 dòng), mỗi file có `last_verified` |
| Khung tin cậy | không có | **4 nhãn bắt buộc** cho mọi khẳng định: `[Xác minh]` (link+ngày) · `[Heuristic]` · `[Thử nghiệm]` · `[Chưa rõ]` |
| "ChatGPT search dùng index Bing" | nói như sự thật | Bỏ; hạ thành `[Chưa rõ]` kèm yêu cầu đọc doc hiện hành |
| Bot AI | gộp chung "muốn được trích dẫn thì allow hết" | **Bảng phân loại theo mục đích**: search (`OAI-SearchBot`) vs training (`GPTBot`, `Google-Extended`) là 2 quyết định độc lập |
| E-E-A-T | "trụ quyết định việc Google/AI có trích dẫn" | Không phải ranking factor — là khung đánh giá chất lượng; giữ vì tín hiệu cụ thể kiểm chứng được |
| Sitemap | "fake lastmod → Google phớt lờ toàn bộ sitemap" | Sitemap là gợi ý, không bảo đảm index; tín hiệu sai thì bị bỏ qua |
| "LSI keywords" | yêu cầu mật độ cao | Bỏ — thuật ngữ sai lệch, không phải kỹ thuật search engine dùng |
| `llms.txt` | điều kiện đạt điểm tối đa trụ AEO/GEO | `[Thử nghiệm]`, **0 điểm**, không dùng nghiệm thu |
| Princeton 2024 | trích tên trổng | Citation đầy đủ (Aggarwal et al., KDD 2024, arXiv) + giới hạn phạm vi |
| 1 `<h1>`, title <60 | pass/fail | `[Heuristic]`; nhiều `<h1>` không phải lỗi SEO |
| GSC AI Overviews | "đã tách báo cáo" | `[Chưa rõ]` — bắt tự mở Search Console của khách mà xem |
| Thang 100 điểm | "chuẩn 100 điểm / hoàn hảo" | **Giữ nguyên thang** nhưng dán nhãn rubric nội bộ để xếp ưu tiên, kèm mục "Giới hạn phải nói với khách" |

**`jp-requirement`** — JR-04: luật số phương án thống nhất ở cả 3 chỗ từng mâu thuẫn.
JR-18: bảng ưu tiên nguồn 5 cấp + luật xử lý mâu thuẫn (không tự chọn, đưa vào 課題表).

**`premium-web`** — PW-08: thêm bước 0 "khảo sát cái đang có trước khi đề xuất cái mới",
house style chỉ áp khi greenfield/redesign. PW-05: **Cổng dữ liệu thật** phân loại A (nội
dung mẫu — viết cho tự nhiên) vs B (testimonial, logo khách, số liệu kinh doanh, chứng chỉ —
**không bao giờ bịa**, kể cả trong demo).

**`jp-comm`** — JC-15: checklist 9 mục soát trước khi gửi (nhầm người nhận, CC/BCC, version
file đính kèm, dữ liệu khách khác lọt vào, credential nội bộ, PII, đúng kênh).

## Trạng thái

**Toàn bộ thay đổi P0 + P1 đã được implement; content/packaging validator đã pass.**
Xem bản đối soát cuối tại
[`../SKILL-AUDIT-RECONCILIATION.md`](../SKILL-AUDIT-RECONCILIATION.md).

**Cả 115 finding của bản audit đều đã có disposition** — §5 và phụ lục §9 của file đó, kiểm
lại được bằng lệnh grep ở §9.4.

Còn lại nhóm P2 cần runtime ngoài repo: chạy forward test trigger / non-trigger / boundary trên
Claude Code, Codex và ChatGPT cloud.

⚠️ Các mẫu code trong `hono-stack` đã sửa nhưng **chưa được chạy/test thật**. Do đó chưa được
gọi là production-ready. Trước khi dùng
làm baseline production, tối thiểu phải test: session tampering, `curl` thẳng Function URL,
XSS qua JSON-LD, corpus sanitizer, và upload polyglot.
