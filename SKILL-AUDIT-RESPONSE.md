# Phản hồi bản audit 6 skill — đối chiếu theo source

**Ngày:** 2026-08-13
**Phản hồi cho:** [`SKILL-AUDIT-FEEDBACK.md`](SKILL-AUDIT-FEEDBACK.md)
**Đối tượng đọc:** Agent đã viết bản audit, và Agent tiếp quản việc sửa
**Trạng thái:** đã verify theo line · đã tách 2 edition · **đã sửa xong toàn bộ backlog P0 + P1** (`hono-stack`, `meo-pptx`, `seo`, `jp-requirement`, `premium-web`, `jp-comm`) — xem §7

---

## 1. Kết luận ngắn

Bản audit **đúng khoảng một nửa**. Nó tìm ra vài lỗi thật sự nghiêm trọng — đặc biệt ở
`hono-stack` và `seo` — và những lỗi đó đáng sửa ngay. Nhưng điểm số bị kéo xuống một cách
có hệ thống bởi 3 loại sai số, trong đó nghiêm trọng nhất là **một số finding P0 trích dẫn
dòng nói nội dung khác với điều audit mô tả**.

Đề nghị: giữ nguyên phần phát hiện security của `hono-stack` và phần factual drift của `seo`;
rút lại hoặc hạ mức các finding trong §5 dưới đây; chấm lại theo §6.

**Điều quan trọng nhất:** không phải "audit sai nên bỏ qua". `hono-stack` có 1 dòng có thể
xoá sạch DB production. Đó là phát hiện giá trị nhất của cả bản audit và nó **đúng**.

---

## 2. Phương pháp — để re-derive, đừng tin bảng này

Bản audit này được kiểm bằng đúng 1 quy tắc:

> **Mở file, đọc dòng được trích, so với điều finding nói.**

Cách làm lại:

```bash
mkdir -p /tmp/verify && cd /tmp/verify
for z in hono-stack jp-comm jp-requirement meo-pptx premium-web seo; do
  unzip -o -q "$z.zip" -d "$z"
done
```

SHA-256 của 6 zip **khớp đúng** bảng ở §2 bản audit → hai bên đọc cùng một file, mọi lệch
nhau là lệch ở diễn giải, không phải ở phiên bản.

Ba câu hỏi áp cho từng finding:

1. **Dòng được trích có nói đúng điều finding mô tả không?** — nếu không, finding sai bất kể
   lập luận sau đó hay đến đâu.
2. **Skill đã có guardrail cho việc này ở chỗ khác chưa?** — rất nhiều finding P0 bị trùng
   với một luật đã tồn tại cách đó vài chục dòng.
3. **Đây là claim cần nguồn, hay là kinh nghiệm nghề / ví dụ minh hoạ?** — ba loại này cần
   ba chuẩn khác nhau, không được áp chung một chuẩn "phải có citation".

Câu 3 là chỗ bản audit trượt nhiều nhất.

---

## 3. Bối cảnh đã thay đổi: 2 edition

Sau khi audit, bộ skill đã được tách thành 2 bản (xem [`skills/README.md`](skills/README.md)):

```
skills/claude/    → Claude Code    (~/.claude/skills/<name>/)
skills/chatgpt-agents/  → ChatGPT/Codex & runtime khác  (.agents/skills/<name>/)
```

Điều này **làm một số finding của bản audit đúng hơn**, và cần ghi nhận sòng phẳng:

| Finding | Trước | Sau khi có bản `chatgpt-agents/` |
|---|---|---|
| C-01 — chuẩn hoá layout `<name>/SKILL.md` | Không cần, zip là artifact phân phối | **Hợp lý** — đã áp dụng cho cả 2 edition |
| MP-01 — `meo-pptx` để SKILL.md ở root zip | Lỗi nhỏ | **Đúng, đã sửa** — normalize thành `meo-pptx/SKILL.md` |
| MP-09 — gọi Agent là "Claude" | Không thành vấn đề | **Đúng cho bản `chatgpt-agents/`, đã sửa** |
| C-02 — bỏ `allowed-tools` | Sai với Claude | **Đúng cho bản `chatgpt-agents/`, đã áp dụng ở đó** |
| H-04 / JR-03 / MP-03 / MP-15 — khai báo dependency + fallback | Nhẹ | **Đúng và quan trọng hơn** — đã thêm block "Phụ thuộc & fallback" vào bản `chatgpt-agents/` |

Cái vẫn không đồng ý: **mức độ**. Đây là convention đóng gói, không phải P0 chặn sử dụng —
và `allowed-tools` là field hợp lệ, có tài liệu chính thức trong Claude Code, nên mô tả nó là
"field lạ có thể bị validator bỏ qua" là sai với runtime chính của bộ skill này. Đúng cách xử
lý là **tách edition**, không phải xoá field khỏi bản Claude.

Tương tự: `agents/openai.yaml` chỉ giúp 1 vendor. Thứ thật sự portable là `description` tốt —
cả 6 skill đều đã có.

---

## 4. Ba sai số hệ thống

### 4.1. Chấm bằng chuẩn của 1 vendor, gọi đó là "baseline"

Bản audit lấy convention OpenAI/Codex làm chuẩn tuyệt đối (`.agents/skills/`,
`agents/openai.yaml`, `quick_validate.py`) và trừ điểm mọi skill vì không theo. Nhưng bộ skill
này chạy đa runtime. Chuẩn đúng phải là **vendor-neutral**: thư mục `<name>/SKILL.md`, prose
không gọi tên runtime cụ thể, dependency có fallback. Đã áp dụng ở §3.

**Ảnh hưởng:** mọi skill mất điểm oan ở C-01, C-02, C-03 và phần lớn mục "P1 portability".

### 4.2. Nhiều finding P0 là đọc nhầm dòng

Đây là nhóm nghiêm trọng nhất, vì P0 được định nghĩa là "sửa trước khi cho Agent dùng rộng".
Chi tiết ở §5.

### 4.3. Áp chuẩn citation lên kinh nghiệm nghề và ví dụ minh hoạ

Bản audit yêu cầu xoá hoặc gắn nguồn cho:

- `premium-web` — "khách sẽ xin lộ ảnh thêm 2–3 lần, nhượng từng nấc, sàn cứng ~70%" (PW-13)
- `premium-web` — "glow shadow màu accent trên nền tối: khách thật đã từng reject" (PW-10)
- `meo-pptx` — 「処理時間を50%削減」 (MP-06), 「50〜70%減」「98%減」 (MP-12)

Hai cái đầu là **kinh nghiệm thực chiến** — đúng thứ làm skill có giá trị hơn prompt rỗng.
Chuẩn đúng cho loại này là ghi rõ phạm vi ("bài học từ dự án X", không phải luật phổ quát),
**không phải xoá**. Hai cái sau là **ví dụ minh hoạ format**, không phải claim số liệu — xem §5.

---

## 5. Disposition từng finding đã đối chiếu

Ký hiệu: **ACCEPT** = đúng, sửa · **REFRAME** = có hạt nhân đúng nhưng sai mức/sai cách diễn
đạt · **REJECT** = không đúng với source.

### 5.1. REJECT — trích dẫn không khớp source

| ID | Mức audit | Audit nói | Dòng thật nói gì |
|---|---|---|---|
| **JR-07** | P0 | "thiếu Why now là thiếu 80%" — số liệu bịa | `requirement-analysis.md:15` là ô bảng về **Backlog note**: "Loại này thiếu 80% thông tin → trọng tâm dồn vào Bước 2". Không liên quan "why now". Đây là nhấn mạnh tu từ trong ô bảng, không phải claim thống kê |
| **JR-15** | P0 | "Cho translator tự quyết khi mơ hồ, kể cả high-impact" | `spec-breakdown.md` nguyên tắc 3: "Chỗ nào mình phán đoán khi dịch → đánh dấu `※判断` kèm cách hiểu đã chọn. Đây là những chỗ rủi ro nhất — **reviewer và khách phải soi được**." Đúng pattern "đề xuất, không tự quyết" mà audit đòi |
| **MP-06** | P0 | Ví dụ "50%" là bịa số liệu | `SKILL.md:57` là **ví dụ ngữ pháp** so sánh 体言止め vs です・ます:「処理時間を50%削減」NOT「〜削減することができます」. Không phải claim hiệu năng |
| **MP-12** | P0 | "50〜70%減/98%減" là performance claim không nguồn | `SKILL.md:218-219` là **mẫu format bảng** before/after ("express the improvement (e.g. …)"). Ngoài ra §0.2 đã có luật in hoa: "**NEVER fabricate** progress, backlog, or status numbers… do not invent figures, completion %, ticket counts, or dates" — audit không nhắc luật này |
| **H-05** | P2 | "PageSpeed checklist trỏ blueprint §8 nhưng §8 là SEO endpoints" | Checklist PageSpeed nằm **đúng trong §8**, `blueprint.md:180-184`. Reference chính xác |
| **H-19** | P1 | "Claim routes/views/auth không đổi mâu thuẫn với khác biệt storage" | `aws.md:3-4` viết có điều kiện: "Cùng 1 app Hono, **chỉ đổi entry + cách nạp env + tầng storage**. Code routes/views/auth giữ nguyên **nếu blueprint được tuân thủ** (Web Standard APIs only)". Đã nói storage đổi. Không mâu thuẫn |
| **MP-05** | P1 | Mâu thuẫn "user tự overlay" vs "template đã supply" | §0.7 và §1b nhất quán: template của khách cấp header/footer, **user áp sau**, skill chỉ giữ safe band. Không có 2 giả định xung đột |
| **MP-04** | P1 | "Ép tiếng Nhật vô điều kiện", fix = "ghi rõ trong description" | Description đã ghi sẵn: "for **Japanese customers**", "**Japanese output**". Fix đã có sẵn từ đầu |

### 5.2. REFRAME — có hạt nhân đúng, sai mức

| ID | Mức audit | Mức đúng | Lý do |
|---|---|---|---|
| **PW-05** | P0 | P2 | Không có mâu thuẫn: `SKILL.md:56` ("cấm tên giả 'Nguyễn Văn A'/'山田太郎', số tròn giả") và `anti-ai-vibe.md:76-77` ("VN 'Trần Hoàng Nam' không 'Nguyễn Văn A'") nói **cùng một luật chống placeholder lộ liễu**. **Nhưng hạt nhân đúng:** skill không phân biệt nội dung mockup với nội dung ship thật → nên thêm data-truth gate. Đó là cải tiến thật, không phải sửa lỗi vi phạm trung thực |
| **JC-08 / JC-13** | P0 | P2 | 「ご異論がなければA案で進めさせていただきます（◯日まで）」là **chuẩn mực thương mại Nhật**, không phải agent tự suy diễn approval. `situations.md:52-54` đã giới hạn "chỉ dùng cho việc rủi ro thấp". Thêm điều kiện "đã thống nhất bằng văn bản" là chặt hơn thực tế ngành |
| **JR-10** | P0 | P2 | `requirement-analysis.md:41-42` đã yêu cầu: ghi 前提 ở đầu tài liệu **và** đánh dấu mọi kết luận phụ thuộc (`※前提1による`). Bổ sung "không áp dụng cho production/security/financial" là hợp lý, nhưng đây là bước **phân tích yêu cầu**, không phải implementation |
| **JR-12** | P0 | P1 | 承認 kèm 未決事項 có 期限 là quy trình bình thường ở dự án SI Nhật, và `yoken-teigi.md:26-27` đã chặn 前提 chưa xác nhận không được nằm ở mục đã chốt. **Hạt nhân đúng:** nên phân loại severity — còn hở scope/security/cost thì không được 承認 |
| **JR-14** | P0 | P2 | Câu "dev không cần đọc bản gốc" là **mục tiêu chất lượng** của tài liệu, và nguyên tắc 2–3 ngay sau đó đã bắt traceability `§4.2 → 4.2` + đánh dấu `※判断`. Nên đổi thành "working contract có traceability" — sửa câu chữ, không phải sửa hành vi |
| **H-07** | P0 | P2 | CSP chỉ nới `'unsafe-inline'` cho **`style-src`**; `script-src` vẫn là `'self'`. Tác động XSS thấp hơn nhiều so với mô tả. `blueprint.md:58-59` đã có comment giới hạn điều kiện dùng |
| **H-13** | P1 | P2 | `blueprint.md:170-171` **đã** nêu phương án `Intl` ("hoặc lưu UTC + format bằng `Intl` theo timezone"). Vấn đề thật chỉ là thứ tự ưu tiên — nên đảo `Intl` lên làm mặc định |
| **H-20** | P1 | P3 | Bundle `--target=node20` chạy trên runtime Node 22 là hợp lệ và phổ biến. Không nhất quán về mặt tài liệu, không phải bug |
| **PW-17** | P0 | P3 | Inline critical CSS là khuyến nghị hiệu năng phổ biến, và skill đã giới hạn phạm vi "với trang 1 file". Xung đột CSP chỉ xảy ra với site dùng strict CSP — đáng ghi chú, không phải P0 |
| **PW-14 / PW-18** | P1 | P3 | `performance.md:3` **đã** ghi profile: "đo mobile, throttle 4x", và §7 đã yêu cầu soi từng chỉ số (LCP element, nguồn CLS, INP handler) chứ không dừng ở điểm số |
| **MP-10** | P0 | P2 | Có tension thật giữa "≥6 node + concrete data" và nguy cơ bịa. Nhưng §3 đã khoanh vùng rõ: "explanatory, **not verified data**", và §0.2 cấm bịa số liệu tiến độ. Nên siết ở chỗ "所要時間/API名 phải từ nguồn", không phải bỏ density bar |
| **SEO-20** | P1 | P3 | **Princeton 2024 là paper có thật** — Aggarwal et al., "GEO: Generative Engine Optimization", KDD 2024 — và skill tóm tắt đúng nội dung (thêm thống kê/trích dẫn/quote làm tăng khả năng được dẫn nguồn). Cần bổ sung link + phạm vi, không phải xoá claim |
| **SEO-21** | P0 | P1 | Mô tả sai rubric: `llms.txt` **không** được cho 25 điểm — nó là 1 trong 9 checkbox của trụ AEO/GEO 25đ. Hạt nhân đúng: chưa có bằng chứng adoption → nên hạ xuống mục thử nghiệm |
| **SEO-12** | P1 | P3 | Title <60 / description <160 là heuristic hành nghề phổ biến, không phải lỗi. Riêng "1 H1 duy nhất" thì đúng là Google đã nói nhiều H1 không phải lỗi SEO — sửa riêng câu đó |

### 5.3. ACCEPT — đúng, cần sửa

| ID | Mức | Xác nhận |
|---|---|---|
| **H-15** | **P0** | ✅ **Đã sửa.** `cloudflare.md:15` — `"db:remote": "wrangler d1 execute <db> --remote --file=./schema.sql"` trong khi `blueprint.md:18` quy định `schema.sql` có "DROP TABLE IF EXISTS trước CREATE". **`npm run db:remote` = xoá sạch DB production.** Đây là phát hiện giá trị nhất của bản audit |
| **H-11** | **P0** | ✅ **Đã sửa.** `blueprint.md:149-155` — sanitize HTML bằng regex, và trỏ tới "`topdoanhnghiep/src/views.ts` hàm `sanitizeHtml`" là file **không có trong package**. Cả 2 vế đều đúng |
| **H-09** | **P0** | ✅ **Đã sửa.** `blueprint.md:118-147` — `ADMIN_PASSWORD` vừa là mật khẩu vừa là HMAC signing secret. Đúng. *(Lưu ý: cookie đã đặt `SameSite=Lax` nên rủi ro CSRF thấp hơn mô tả của audit, nhưng việc gộp secret là lỗi thật)* |
| **H-08** | **P0** | ✅ **Đã sửa.** `blueprint.md:113` — `raw(JSON.stringify(obj))` cho JSON-LD. Chuỗi chứa `</script>` phá được context. `raw()` của Hono không escape |
| **H-22** | **P0** | ✅ **Đã sửa.** `aws.md:59,75` — CloudFront + `FunctionUrlAuthType.NONE`. Function URL public → bypass được CloudFront/WAF qua origin trực tiếp |
| **H-06** | P1 | ✅ **Đã sửa.** `blueprint.md:50` — `preload` trong HSTS mặc định. Khó rollback, khoá cả subdomain |
| **H-10** | P1 | ✅ **Đã sửa.** `blueprint.md:135` — PBKDF2 100.000 iterations, thấp hơn guidance OWASP hiện hành (600.000 cho PBKDF2-HMAC-SHA256) |
| **H-12** | P1 | ✅ **Đã sửa.** `blueprint.md:167-168` — upload tin content-type + giữ tên người dùng |
| **H-17 / H-18** | P1 | ✅ **Đã sửa.** `compatibility_date` hard-code `2026-01-01`; giá/limit free tier hard-code, sẽ trôi |
| **SEO-07** | **P0** | `SKILL.md:56` "ChatGPT search dùng index của Bing" — đã lỗi thời, OpenAI có `OAI-SearchBot` riêng. Và `SKILL.md:55` gộp bot training (`GPTBot`, `Google-Extended`) với bot search (`OAI-SearchBot`) thành một luật "muốn được trích dẫn thì allow hết" — sai về mục đích từng bot |
| **SEO-19** | P1 | `SKILL.md:111` — "mật độ LSI keywords cao". "LSI keywords" là thuật ngữ SEO đã bị bác bỏ |
| **SEO-14** | P1 | `SKILL.md:78` — E-E-A-T là "trụ quyết định việc Google VÀ AI có dám trích dẫn". Google nói rõ E-E-A-T không phải ranking factor cụ thể |
| **SEO-08** | P1 | `SKILL.md:57` — "Google sẽ phớt lờ **toàn bộ sitemap của domain**" là phóng đại |
| **SEO-01** · **SEO-02** | P1 | Cả file không có **một ngày verify nào**, trong khi đây là lĩnh vực trôi nhanh nhất. Đây mới là vấn đề gốc của `seo`, không phải chữ "100 điểm" |
| **MP-02** | P1 | `SKILL.md:12-15` — description trigger cả "flowchart / architecture diagram / use case diagram" kèm "**even if 'MEO' or 'pptx' is not mentioned**". Trigger rộng thật, sẽ cướp task diagram không liên quan. ✅ **Đã sửa** — description rút 128→61 từ, bỏ hẳn vế này và danh sách keyword |
| **MP-03 / MP-15** | P1 | `pptxgenjs`, `python -m markitdown`, "office unpack/pack scripts" không được khai báo, không có fallback. **Đã sửa ở bản `chatgpt-agents/`**; bản `claude/` dựa vào tool sẵn có của runtime |
| **MP-16** | P1 | `SKILL.md` 345 dòng, **0 reference** — vẽ 1 diagram vẫn phải đọc cả 9 pattern + Report mode. ✅ **Đã sửa** — tách `references/diagrams.md` (97) + `references/report-mode.md` (25); SKILL.md còn 268. Nội dung không cắt (tổng 390 > 345). `seo` còn cùng vấn đề → gộp vào mục 6 §7 |
| **JR-04** | P1 | Mâu thuẫn thật: `SKILL.md:39` "**Không bao giờ** 1 phương án duy nhất: ≥2 options" vs `requirement-analysis.md:49-51` "Nếu chỉ tồn tại 1 đường đi khả thi → nói thẳng và chứng minh vì sao các đường khác bị loại". Checklist `:96` lại quay về "≥2 options". Cần 1 luật duy nhất |
| **PW-08** | P1 | `SKILL.md:76-80` — bước 3 nhảy thẳng vào "đề xuất brand kit độc bản" mà chưa có bước inspect design system sẵn có. Catch tốt nhất của phần `premium-web` |
| **JC-15** | P1 | Thiếu checklist privacy trước khi gửi (recipient/CC-BCC, attachment đúng version, dữ liệu khách, credential nội bộ). Bổ sung hợp lý |

### 5.4. Chưa đối chiếu — cần verify trước khi hành động

Các finding sau **chưa được kiểm theo line** trong lần rà này. Đừng coi là đúng, cũng đừng
coi là sai — áp phương pháp §2 rồi mới quyết:

- `jp-comm`: **đã verify 2026-08-13 → phần lớn REJECT, skill đã có sẵn guard:**
  - JC-11 (completion %) — `reporting.md:49` đã ghi `done x/y task` + bắt so trend với tuần
    trước. Chính là numerator/denominator mà audit đòi. **Đã có sẵn.**
  - JC-14 (batch cadence) — `qa-management.md:28` đã viết chữ **"ví dụ"**. Fix của audit là
    "gắn nhãn example" → **đã gắn từ đầu.**
  - JC-13 (deemed approval) — `qa-management.md:26-27` còn chặt hơn `situations.md`:
    "**KHÔNG dùng cho việc ảnh hưởng nghiệp vụ/tiền**". Càng khẳng định P0 là sai mức.
  - JC-12 (manual verify số Backlog) — kinh nghiệm nghề đúng (tracking tool hay stale),
    thuộc nhóm sai số §4.3. **REJECT.**
  - JC-10 (cadence 2–3 ngày) — `reporting.md:28` viết "**≥** 2–3 ngày làm việc", là mức tối
    thiểu chứ không phải SLA cứng. Yếu, P3.
  - Còn lại chưa đối chiếu: JC-06, JC-07, JC-09, JC-16.
- `jp-requirement`: JR-11, JR-13, JR-16, JR-17
- `premium-web`: PW-15, PW-16, PW-19 *(`performance.md` phần sau, `type-scroll.md`)*
- `hono-stack`: H-01, H-02, H-14, H-16, H-21
- `seo`: SEO-05, SEO-10, SEO-11, SEO-15, SEO-16, SEO-17, SEO-18, SEO-23

⚠️ **SEO-22 cần verify riêng.** Bản audit dẫn nguồn "Google Search — GenAI performance
reports rollout, tháng 6/2026". Không xác nhận được nguồn này. Đồng thời `seo/SKILL.md:129`
viết "GSC đã tách báo cáo" cho AI Overviews — theo hiểu biết tính đến 5/2026 thì Google
**chưa** tách, số liệu AI Overviews gộp trong báo cáo Web search thường. **Cả câu trong skill
lẫn câu sửa của audit đều cần kiểm lại từ nguồn chính thức trước khi viết vào file.**

---

## 6. Điểm chấm lại

| Skill | Audit | Chấm lại | Lý do lệch |
|---|---:|---:|---|
| `jp-comm` | 8.1 | **8.5** | 2 P0 (deemed approval) là REFRAME; JC-15 là bổ sung đúng |
| `jp-requirement` | 8.2 | **8.5** | 4 P0: 2 REJECT, 2 REFRAME. Chỉ JR-04 là lỗi cấu trúc thật |
| `premium-web` | 6.0 | **7.5** | PW-17 gần như REJECT, PW-05 REFRAME, PW-10/12/13 đánh vào kinh nghiệm nghề. PW-08 giữ nguyên |
| `meo-pptx` | 6.2 | **7.0** | 2/4 P0 là REJECT (đọc nhầm ví dụ). Nhưng MP-01/03/09/15 đúng và **nặng hơn** trong bối cảnh 2 edition |
| `hono-stack` | 6.8 | **7.0** | 5 P0 security đều đúng; trừ lại H-05/H-19 REJECT, H-07/H-13/H-20 REFRAME |
| `seo` | 4.5 | **5.5** | Hướng đúng, mức quá tay. Đây là vấn đề **viết lại câu chữ + gắn ngày**, không phải làm lại skill |

**Khác biệt về thứ hạng đáng chú ý:** `hono-stack` nên xếp **dưới** `premium-web` và
`meo-pptx`, không phải trên. Lý do: lỗi của nó sinh ra code chạy production, còn lỗi của hai
skill kia chủ yếu là đóng gói và cách diễn đạt. Bản audit xếp ngược.

---

## 7. Backlog sửa — theo thứ tự

### P0 thật — ✅ **ĐÃ LÀM XONG 2026-08-13**

Cả 5 mục dưới đã sửa trong `skills/claude/` và `skills/chatgpt-agents/`. Chi tiết before/after ở
[`skills/README.md`](skills/README.md). ⚠️ Code đã sửa nhưng **chưa chạy test thật** — xem danh sách test bắt buộc ở cuối README đó.

1. `hono-stack/references/cloudflare.md:15` — **xoá script `db:remote` trỏ `schema.sql`**.
   Thay bằng migration tăng dần, bắt buộc chỉ định env/database ID rõ ràng.
2. `blueprint.md:149-155` — thay sanitizer regex bằng allowlist parser-based; xoá tham chiếu
   tới file ngoài package.
3. `blueprint.md:118-147` — tách `SESSION_SECRET` khỏi `ADMIN_PASSWORD`.
4. `blueprint.md:113` — escape `<`, `>`, `&`, U+2028/U+2029 trước khi `raw()` cho JSON-LD.
5. `aws.md:59,75` — bỏ `authType: NONE`; dùng OAC/IAM origin verification.

### P1 — độ chính xác nội dung

6. ~~`seo` — factual drift + tách reference.~~ ✅ **Đã làm 2026-08-13.** Cụ thể: bỏ claim Bing index, sửa taxonomy bot theo mục đích, hạ E-E-A-T xuống
   quality lens, sửa câu sitemap, bỏ "LSI keywords", hạ `llms.txt` xuống thử nghiệm,
   **gắn `last_verified` cho từng nhóm claim**. Tách reference cùng lúc (SEO-23) — cùng cách
   đã làm cho `meo-pptx`; đặt `last_verified` theo từng file reference hợp lý hơn theo dòng.
7. ~~`hono-stack` — HSTS, PBKDF2, upload, timezone.~~ ✅ **Đã làm 2026-08-13** (H-06, H-10, H-12, H-13, H-17, H-18, H-20, H-03).
8. ~~`meo-pptx` — thu hẹp trigger + tách reference.~~ ✅ **Đã làm 2026-08-13** (MP-02, MP-16).
9. ~~`jp-requirement` — luật số option + thứ tự ưu tiên nguồn.~~ ✅ **Đã làm 2026-08-13** (JR-04 sửa ở cả 3 chỗ: SKILL.md nguyên tắc 4, checklist requirement-analysis, bảng Common mistakes; JR-18 thêm bảng ưu tiên nguồn 5 cấp + luật xử lý mâu thuẫn).
10. ~~`premium-web` — inspect design system + data-truth gate.~~ ✅ **Đã làm 2026-08-13** (PW-08 thêm bước 0 vào quy trình; PW-05 thêm "Cổng dữ liệu thật" phân loại A/B ở anti-ai-vibe.md mục 6, wire vào luật 6 của SKILL.md và checklist bàn giao).
11. ~~`jp-comm` — checklist privacy trước khi gửi.~~ ✅ **Đã làm 2026-08-13** (JC-15, 9 mục).

### P2 — verify

12. Đối chiếu nhóm §5.4 theo phương pháp §2.
13. Viết trigger / non-trigger / boundary prompt cho từng skill — phần này của bản audit
    (C-03) **đúng và hữu ích bất kể runtime nào**.

### Không làm

- Xoá `allowed-tools` khỏi bản `claude/` — field hợp lệ, đã tách edition ở `agents/`.
- Thêm `agents/openai.yaml` — chỉ phục vụ 1 vendor; `description` tốt mới là thứ portable.
- Xoá kinh nghiệm thực chiến vì "không có nguồn" — khoanh phạm vi, đừng xoá.
- Sửa các mục ở §5.1 — trích dẫn không khớp source.

---

## 8. Ghi chú cho Agent sửa tiếp

Bộ skill giờ có 2 edition. Delta gần như chỉ nằm trong `SKILL.md`; `references/` giống hệt
nhau byte-for-byte trừ 1 dòng trong `meo-pptx/references/report-mode.md`. Nghĩa là:

- Sửa `references/` → làm 1 lần, chép sang edition kia.
- Sửa `SKILL.md` → sửa `claude/` trước, port sang `agents/`, giữ 4 delta trong
  [`skills/README.md`](skills/README.md).
- Sau mỗi đợt sửa chạy `diff -r skills/claude skills/agents` để delta không trôi.

Vì gần hết P0 nằm trong `hono-stack/references/`, sửa 1 lần là port được cả 2 edition.

---

## 9. Phụ lục — disposition ĐẦY ĐỦ 115 finding

§5 ở trên chỉ dispositioned 86/115 ID. Phần này đóng nốt 29 ID còn lại để **không finding nào
bị bỏ qua trong im lặng** — đúng nguyên tắc "no silent caps" mà chính bản audit đề ra.

### 9.1. ✅ Đã sửa (chưa kịp ghi ở §5)

| ID | Nội dung | Đã xử lý thế nào |
|---|---|---|
| H-23 | `blueprint.md` >100 dòng không có mục lục | Thêm mục lục 9 mục + cột "đọc khi" |
| SEO-03 | Giả UA GPTBot bằng `curl` không chứng minh bot thật vào được | `technical.md` có hộp cảnh báo riêng: UA spoof chỉ test server có trả khác theo UA; muốn biết bot thật thì đọc robots/CDN/WAF + server log + verify reverse-DNS |
| SEO-04 | Rich Results Test không validate mọi schema | Tách rõ RRT (chỉ loại Google render) vs Schema Markup Validator (mọi loại) + kiểm content parity |
| SEO-06 | Trộn lab "xanh" với field CWV | Tách hẳn 2 khái niệm; cấm kết luận business từ 1 lần chạy lab |
| SEO-09 | URL ngắn/keyword thành hard requirement | Đổi tiêu chí thành ổn định + mô tả được + crawl được; thêm cảnh báo không rewrite URL đang chạy tốt |
| SEO-13 | FAQ schema / BreadcrumbList bị tuyệt đối hoá | Chỉ markup nội dung hiển thị thật; breadcrumb khi UI có breadcrumb; phần "AI parse tốt hơn" hạ xuống `[Thử nghiệm]` |
| MP-11 | Ví dụ model cụ thể dễ lỗi thời | `diagrams.md` đổi sang 案A vs 案B / 現行 vs 提案 + ghi lý do tránh tên sản phẩm |
| MP-13 | Ép mọi slide phải có visual | Thêm ngoại lệ: bảng/text có cấu trúc vẫn tính 可視化 khi đó là cách biểu diễn trung thực nhất; cấm diagram trang trí |
| PW-04 | Cấm font/grid đối xứng như luật phổ quát | Giải quyết bằng PW-08 bước 0: house style chỉ áp khi greenfield/redesign; repo có design system thì nhất quán với nó thắng |
| PW-06 | Ép mọi component có đủ mọi state | Đổi thành "mọi state **có áp dụng**"; thêm yêu cầu focus-visible + bàn phím + touch |
| PW-07 | Trộn FCP lab với Core Web Vitals | Tách: CWV (field) riêng, ngân sách lab (Lighthouse 4x, có FCP) riêng, ghi rõ FCP không phải CWV |
| JC-03 | "Timing quan trọng hơn content" | Đổi thành: báo sớm **những gì đã xác nhận** + ghi phần chưa rõ + hẹn giờ update; không đánh đổi độ chính xác |
| JR-06 | "Never skip/reorder" quá cứng | Cho phép lặp/quay lại bước trước; giữ ràng buộc "không bỏ kết quả bắt buộc của bước nào" |
| JR-08 | Chặn toàn bộ tiến độ khi chưa có なぜ今 | Ghi thành 未決事項 + hỏi ngay; vẫn chạy tiếp điều tra hiện trạng; chỉ chặn 推奨 và 要件定義書 |
| JC-01 · JR-01 · PW-02 | `allowed-tools` ngoài baseline | Giải quyết bằng tách edition: giữ ở `claude/`, bỏ ở `chatgpt-agents/` |

### 9.2. ❌ REJECT — không sửa, kèm lý do

| ID | Audit nói | Vì sao không sửa |
|---|---|---|
| JC-04 | Luôn đưa 2 option làm mail thông báo dài dòng | Nguyên tắc 7 đã giới hạn phạm vi: "**Đề xuất** trong giao tiếp (VD 納期交渉)". Thông báo thuần facts không rơi vào đây |
| MP-07 | "70% visual weight" khó đo, viết như pass/fail | Nguyên văn là "**~**70%", nằm trong "Dominance rule" về cân bằng màu — là heuristic tỷ lệ, không phải tiêu chí nghiệm thu |
| MP-08 | Rule mật độ dễ tạo slide chật | §5.3 Visual QA đã có cổng overflow + contrast + title-wrap, bắt fix rồi verify lại |
| MP-14 | Tự chèn placeholder slide tạo output không dùng được | Đó chính là thiết kế trung thực: ô ghi `［要手動入力：verify済みデータ］` + speaker note nhắc. Nó **không** giả vờ là bản final — ngược lại, buộc người dùng phải điền |
| PW-01 | Description lệ thuộc keyword, dễ sai | `premium-web` cố ý là skill **chỉ chạy khi gọi đích danh**; danh sách keyword chính là cơ chế đó, và đã có negative boundary rõ. Khác hẳn `meo-pptx` — cái đó bị sửa vì nó tự mở rộng ra ngoài phạm vi |
| PW-03 | SKILL.md lặp `anti-ai-vibe.md` | Đã ghi sẵn trong Common mistakes: "10 luật là tóm tắt; audit cuối phải theo checklist đầy đủ". Đây là progressive disclosure đúng chuẩn, không phải lặp thừa |
| PW-11 | Hover/animation thiếu reduced-motion | `anti-ai-vibe.md` mục 4 đã bắt buộc `prefers-reduced-motion: reduce`, mục 5 đã bắt focus ring |
| PW-12 | "JP Zen / VN social proof" là stereotype | Đây là **hiểu biết thị trường** của người làm BrSE tuyến Nhật — nói về kỳ vọng thẩm mỹ của thị trường và khách hàng, không phải suy diễn về con người. Thuộc nhóm sai số §4.3 |

### 9.3. ⏸ REFRAME — có hạt nhân đúng nhưng ưu tiên thấp, chưa làm

| ID | Hạt nhân đúng | Mức |
|---|---|---|
| JR-05 | "Mirror vocabulary, không đổi" có thể giữ nguyên thuật ngữ sai/mơ hồ. Nên thêm glossary chuẩn hoá + đánh dấu chỗ mâu thuẫn, vẫn giữ từ gốc để trace | P2 |
| JC-02 | Giả định mọi người nhận là senior non-technical. Phạm vi này đã ghi ở phần mở đầu skill nên không sai — nhưng thêm bước phân loại audience/medium/urgency sẽ chặt hơn | P3 |
| JC-05 · JR-09 | Câu hỏi đóng A/B + 推奨 là đúng manner với khách Nhật cấp cao và tiết kiệm thời gian của họ. Hạt nhân đúng: khi **chưa biết không gian giải pháp**, phải hỏi mở trước rồi mới đóng | P3 |
| JR-02 | Xử lý khi thiếu connector/file tool. Bản `chatgpt-agents/` đã có block fallback; bản `claude/` dựa vào tool sẵn có của runtime | P3 |
| PW-09 | "display 48px+" nên là `clamp()` responsive thay vì số cứng | P3 |

### 9.4. Cách kiểm lại phụ lục này

```bash
grep -oE '\| (C|H|JC|JR|MP|PW|SEO)-[0-9]+' SKILL-AUDIT-FEEDBACK.md | sed 's/| //' | sort -u > /tmp/all.txt
grep -oE '(C|H|JC|JR|MP|PW|SEO)-[0-9]+' SKILL-AUDIT-RESPONSE.md | sort -u > /tmp/done.txt
comm -23 /tmp/all.txt /tmp/done.txt   # phải rỗng
```
