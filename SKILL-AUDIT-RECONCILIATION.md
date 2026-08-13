# Đối soát cuối — 6 skill, tách Claude và ChatGPT/Codex Agents

**Ngày đối soát:** 2026-08-13
**Đã đọc:** `SKILL-AUDIT-FEEDBACK.md`, `SKILL-AUDIT-RESPONSE.md`, `skills/README.md` và source của cả hai edition
**Mục tiêu:** chốt phần nào của audit giữ lại, phần nào cần sửa, và skill nào dùng ở runtime nào

**Cập nhật cuối:** source đã được tối ưu và validator local đã pass ngày 2026-08-13.
Trạng thái chính xác là **content/packaging validated**; chưa gọi là runtime forward-tested trên
Claude Code, Codex và ChatGPT cloud.

## 1. Kết luận

Phản hồi trong `SKILL-AUDIT-RESPONSE.md` **đúng ở điểm cốt lõi**: bộ skill phải được đánh giá
theo hai target khác nhau. Audit ban đầu đã dùng quy ước OpenAI cho cả edition Claude, nên
finding về `allowed-tools`, `.agents/skills/` và `agents/openai.yaml` bị áp sai phạm vi.

Phản hồi cũng đúng khi chỉ ra một số finding đọc sai ngữ cảnh, đặc biệt với ví dụ minh họa
trong `meo-pptx` và kinh nghiệm nghề trong `premium-web`. Những mục đó không nên giữ ở P0.

Tuy nhiên, phản hồi có hai câu cần chỉnh:

1. `allowed-tools` trong Claude Code là quyền **pre-approve** tool, không phải danh sách giới
   hạn tool. Tool không nằm trong danh sách vẫn có thể được gọi và đi qua permission flow.
2. “Đã sửa xong/đã đóng toàn bộ P0 + P1” là quá sớm. Source đã được sửa, nhưng `hono-stack`
   chưa qua security test và cả sáu skill chưa qua forward test. Trạng thái đúng là
   **implemented, not verified**.

Do đó, không dùng lại điểm số audit cũ hoặc điểm số phản biện như chứng nhận. Chỉ chấm lại
sau khi test hành vi trên từng runtime.

## 2. Ba target cần phân biệt

| Target | Source edition | Cách cài | Frontmatter/runtime note |
|---|---|---|---|
| Claude Code CLI | `skills/claude/<name>/` | Project: `.claude/skills/<name>/`; cá nhân: `~/.claude/skills/<name>/` | Hỗ trợ extension như `allowed-tools`; đây là pre-approval và cần least privilege |
| Claude Agent SDK | Dùng nội dung edition Claude nhưng cấu hình permission ở SDK | `setting_sources` + `skills` trong SDK | `allowed-tools` trong `SKILL.md` không áp dụng; dùng `allowedTools` của SDK |
| Codex/OpenAI agents local | `skills/chatgpt-agents/<name>/` | Project: `.agents/skills/<name>/`; cá nhân: `$CODEX_HOME/skills/<name>/` | Baseline đang dùng chỉ dựa vào `name` + `description`; `agents/openai.yaml` là metadata OpenAI optional/recommended, không phải điều kiện portable |
| ChatGPT cloud | Đóng gói/upload từ edition `chatgpt-agents` | ChatGPT → Plugins → Skills → Create → Upload | Là bản cloud riêng; không đồng nghĩa file local ở máy đã tự xuất hiện trên ChatGPT |

### ChatGPT cloud và hai máy nhà/công ty

Theo tài liệu OpenAI tại ngày đối soát, Personal Skills áp dụng cho các gói đủ điều kiện như
Business, Enterprise, Healthcare và Edu. ChatGPT cho upload skill trong
`Plugins → Skills → Create → Upload`.

Điểm cần lưu ý: Personal Skills phải được thêm riêng trên desktop và web/mobile; OpenAI ghi
rõ các surface này **không tự đồng bộ skill với nhau**. Vì vậy đăng nhập cùng một tài khoản
ở máy nhà và công ty chưa đủ để bảo đảm local skill được sync.

Khuyến nghị vận hành:

- Dùng repo này làm source of truth.
- Với Codex local ở mỗi máy: checkout/pull repo rồi copy edition `chatgpt-agents` vào vị trí
  local/project tương ứng.
- Với ChatGPT cloud: upload package từ edition `chatgpt-agents` trong Skills UI; nếu dùng
  workspace công ty, tuân theo quyền upload/share/install của admin.
- Không để secret, credential, dữ liệu khách hoặc file nội bộ nhạy cảm trong package upload.

## 3. Kiểm tra trạng thái split hiện tại

Split đã tồn tại và về cấu trúc là hợp lý:

```text
skills/
├── claude/
│   ├── hono-stack/
│   ├── jp-comm/
│   ├── jp-requirement/
│   ├── meo-pptx/
│   ├── premium-web/
│   └── seo/
└── chatgpt-agents/
    └── cùng 6 skill
```

Đối chiếu byte-level cho thấy đúng 7 file khác nhau giữa hai edition:

- 6 file `SKILL.md`.
- `meo-pptx/references/report-mode.md` khác một câu xưng hô runtime.

Các reference khác giống nhau. Sáu bản `chatgpt-agents/SKILL.md` chỉ có `name` và
`description` trong frontmatter. Những marker sửa security của `hono-stack` và evidence
labels của `seo` đều có mặt trong source hiện tại.

## 4. Disposition audit ban đầu

### Giữ lại

- P0 security thật của `hono-stack`: remote schema reset, JSON-LD script context, regex
  sanitizer, dùng password làm signing secret và Function URL public bypass.
- Factual drift của `seo`: mục đích `OAI-SearchBot`/`GPTBot`, E-E-A-T, sitemap, LSI,
  `llms.txt` và lab-vs-field.
- Trigger quá rộng và dependency không được khai báo của `meo-pptx`.
- Mâu thuẫn rule số phương án của `jp-requirement`.
- Data-truth gate của `premium-web`.
- Privacy pre-send check của `jp-comm`.

### Rút lại hoặc hạ mức

- Không coi `allowed-tools` là field lạ ở edition Claude.
- Không bắt `agents/openai.yaml` như điều kiện portable hoặc điều kiện đạt 10/10.
- Không coi ví dụ format số trong `meo-pptx` là fabricated claim nếu nó được gắn rõ là ví dụ
  và không đi vào deliverable như dữ liệu thật.
- Không xóa kinh nghiệm nghề chỉ vì không có paper; phải gắn phạm vi “project lesson” và
  không biến nó thành universal fact.
- Hạ các finding đã trích sai line/ngữ cảnh theo disposition trong
  `SKILL-AUDIT-RESPONSE.md`.

## 5. Vấn đề mới phát hiện sau khi tách edition

### R-01 — `allowed-tools` đang mô tả sai tác dụng

**Vị trí:** `skills/README.md` trước khi đối soát, dòng bảng edition.
**Đã sửa tài liệu:** đổi “giới hạn tool” thành “pre-approve tool”.

Rủi ro thật là permission: project skill có thể tự xin pre-approve quyền rộng sau khi user
trust workspace. Vì vậy không nên điền `Bash`, `Write`, `Edit` một cách rộng chỉ để bớt prompt.

### R-02 — `allowed-tools` Claude cần normalize — ĐÃ SỬA

Trước đây năm file dùng scalar có dấu phẩy và quyền rộng:

```yaml
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
```

Đã normalize cả sáu skill Claude về `allowed-tools: Read, AskUserQuestion`. Đây chỉ là quyền
pre-approve tối thiểu; Bash/Write/Edit/WebFetch vẫn đi qua permission flow khi workflow cần.
Nếu mục tiêu là **cấm** tool, phải dùng deny/permission settings; `allowed-tools` không làm việc đó.

### R-03 — tên `chatgpt-agents` bao gồm hai cơ chế phân phối

Nội dung có thể dùng chung, nhưng cách cài khác nhau:

- Codex/agent local: thư mục `.agents/skills/<name>/`.
- ChatGPT cloud: upload skill trong Skills UI.

README/package release nên tạo hai artifact từ cùng edition nếu cần phát hành:

```text
dist/codex/<name>/SKILL.md
dist/chatgpt/<name>.zip
```

### R-04 — hai bản copy thủ công có nguy cơ drift — ĐÃ CÓ VALIDATOR

Quy trình hiện tại là sửa Claude trước rồi chép sang ChatGPT/Agents. Sáu skill vẫn quản lý
được, nhưng về lâu dài dễ lệch reference hoặc quên delta.

Đã thêm `skills/scripts/validate-skills.mjs`, fail khi tree/frontmatter/link/ToC hoặc diff ngoài
allowlist bị lệch. Build/generate từ common source vẫn là cải tiến tương lai; validator hiện tại
đã chặn rủi ro drift trước commit.

Một build script tương lai có thể:

1. Copy common body/references từ source chung.
2. Áp overlay frontmatter và runtime wording cho Claude/OpenAI.
3. Validate cả hai output.
4. Fail nếu diff ngoài allowlist bảy file/delta đã định nghĩa.
5. Tạo ZIP ChatGPT cloud và folder Codex từ cùng commit.

## 6. Verification đã làm và chưa làm

### Đã làm

- Đọc đầy đủ audit, phản hồi và README.
- Kiểm tree của cả hai edition.
- Kiểm diff giữa editions: đúng 7 file khác nhau như README mô tả.
- Kiểm frontmatter bản ChatGPT/Agents.
- Kiểm các marker P0 đã được đưa vào source `hono-stack`.
- Kiểm evidence labels và bot taxonomy mới trong source `seo`.
- Chạy `node skills/scripts/validate-skills.mjs`: pass đủ 2 edition × 6 skill, frontmatter,
  relative links, ToC reference dài, edition drift và stale-rule markers.
- Kiểm tra `meo-pptx`: canvas đúng 10.83 × 7.5 in, ghi rõ đây là vùng nội dung để copy/paste
  vào A4 đã có header/footer; không normalize thành ISO A4.
- Kiểm tra `jp-comm`/`jp-requirement`: question style theo discovery/decision, deemed approval
  có governance, số DoD phải có source/owner, ambiguity high-risk phải xin authority.
- Kiểm tra `premium-web`: house style là default có lý do, không cấm kỹ thuật đẹp; hỗ trợ
  user giao "tự quyết"; giữ stack sẵn có; bắt buộc screenshot desktop/mobile và một vòng sửa.

### Chưa làm

- Chưa chạy security test cho code mẫu `hono-stack`.
- Chưa forward-test trigger/non-trigger/boundary prompt trên Claude Code, Codex và ChatGPT
  cloud.
- Chưa upload thử package lên ChatGPT Skills scanner.

## 7. Backlog chốt

### P0 — acceptance test khi materialize `hono-stack` thành project chạy thật

Các mục sau không thể chạy trên package Markdown thuần; chúng là gate bắt buộc của project được
sinh ra từ skill, không phải blocker cấu trúc để phát hành bộ skill:

- [ ] Test session tampering và expiry/version migration.
- [ ] Test JSON-LD với `</script>`, U+2028/U+2029 và dữ liệu không tin cậy.
- [ ] Chạy XSS corpus qua sanitizer.
- [ ] Test upload MIME spoof/polyglot/oversize/decompression bomb.
- [ ] Gọi thẳng Lambda Function URL và xác nhận bị từ chối.
- [ ] Dry-run migration; xác nhận không còn đường chạy `schema.sql` lên production.

### P1 — packaging/runtime

- [x] Policy `allowed-tools`: chỉ pre-approve `Read, AskUserQuestion` cho Claude.
- [x] Validator chạy được cho cả hai edition; pass ngày 2026-08-13.
- [ ] Tạo build script để tránh sync thủ công.
- [ ] Tạo artifact riêng cho Codex folder và ChatGPT upload ZIP.
- [ ] Nếu cần trải nghiệm UI tốt trong Codex, thêm `agents/openai.yaml`; không coi đây là
  requirement của Claude hoặc Agent Skills portable.

### P2 — forward test

- [x] Đã viết matrix: mỗi skill 3 prompt phải trigger, 2 prompt không trigger, 2 boundary prompt
  tại `skills/evals/trigger-matrix.md`.
- [ ] Chạy cùng prompt trên Claude Code và Codex; ghi delta output.
- [ ] Với ChatGPT cloud đủ điều kiện, upload và test auto-activation/explicit activation.
- [ ] Chấm điểm lại dựa trên output và test evidence, không dựa trên prose alone.

## 8. Nguồn chính thức dùng để chốt runtime

- [Claude Code — Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Agent SDK — Skills và tool restrictions](https://code.claude.com/docs/en/agent-sdk/skills)
- [Agent Skills — Specification](https://agentskills.io/specification)
- [Agent Skills — Client implementation và `.agents/skills`](https://agentskills.io/client-implementation/adding-skills-support)
- [OpenAI — Skills in ChatGPT](https://help.openai.com/en/articles/20001066)

## 9. Handoff rule

Từ đây, Agent sửa skill phải ghi rõ đang sửa target nào: `shared`, `claude`,
`chatgpt-agents`, hay cả hai. Không được nói “đã xong” nếu mới sửa prose; phải báo tách bạch
`implemented`, `validated`, `forward-tested` và `production-verified`.
