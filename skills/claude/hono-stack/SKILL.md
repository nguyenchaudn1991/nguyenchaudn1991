---
name: hono-stack
description: >-
  Use when the user mentions Hono / HONO stack, or starts a new web project /
  API / SSR site and asks to build it with Hono — keywords: "hono", "hono-stack",
  "dự án hono", "web hono", "API hono", "Hono + Cloudflare", "Hono + AWS",
  "Workers + D1 + R2". Also use when porting a Hono app between Cloudflare and AWS.
  Do NOT trigger for frontend-only work, static sites without a backend, or
  projects already committed to another framework (Next.js, Express, Rails…).
allowed-tools: Read, AskUserQuestion
---

# Hono Stack — 1 codebase, chạy Cloudflare hoặc AWS

Chuẩn dựng dự án web/API bằng **Hono**, đúc từ dự án production `topdoanhnghiep.com`
(Hono 4 + Cloudflare Workers + D1 + R2, SSR không framework). Mục tiêu kép: ship nhanh
**và** tích lũy kinh nghiệm Hono — nên code phải chuẩn Web Standard để chạy được cả
Cloudflare (dự án cá nhân) lẫn AWS (dự án công ty, cùng stack với MEO dashboard).

---

## Routing — chọn platform, load đúng file

| Tình huống | File PHẢI load |
|---|---|
| Mọi dự án Hono (luôn luôn) | [references/blueprint.md](references/blueprint.md) — kiến trúc app, SSR, auth, SEO, patterns |
| Deploy **Cloudflare** (mặc định cho dự án cá nhân) | + [references/cloudflare.md](references/cloudflare.md) |
| Deploy **AWS** (dự án công ty) | + [references/aws.md](references/aws.md) |
| Không rõ platform | Hỏi 1 câu: "Cá nhân (Cloudflare) hay công ty (AWS)?" — rồi load |

Không load file platform không dùng. Nếu môi trường có các skill `wrangler`,
`workers-best-practices`, `cloudflare` → có thể gọi bổ sung cho tác vụ Cloudflare sâu
(DO, Queues, cron) thay vì phình file ở đây.

## Nguyên tắc cốt lõi (mọi dự án Hono)

1. **Web Standard APIs only trong code dùng chung.** `fetch`, `crypto.subtle`, `Request/Response`,
   `URL` — cấm `node:fs`, `node:crypto`, `Buffer` trong routes/views/logic. Đây là điều kiện
   để cùng 1 app chạy Workers lẫn Lambda.
2. **Bindings/env luôn qua type `Env` + generic `Hono<{ Bindings: Env }>`** — một chỗ khai báo
   duy nhất; code truy cập `c.env.X`. Khác platform chỉ khác cách *nạp* Env (xem file platform).
3. **SSR bằng `hono/html`** (tagged template + `raw()`), **0 framework frontend** mặc định.
   Chỉ cân nhắc `hono/jsx` khi component nhiều và lồng sâu. Trang public mục tiêu **0 JS**.
4. **Sub-app cho từng khu vực** (`app.route("/admin", adminApp)`) — mỗi sub-app tự quản
   middleware/auth của nó.
5. **SQL prepared statements + bind, typed kết quả** (`.all<T>()` / `.first<T>()`) — cấm nối
   chuỗi SQL.
6. **TypeScript strict**, giữ dependency runtime tối thiểu — mục tiêu là `hono` và không gì
   khác; thêm dep nào cũng phải có lý do. Xác nhận bằng lockfile hiện tại, không tin con số
   trong tài liệu.
7. Phân công với skill `premium-web` (nếu có trong môi trường): **hono-stack quyết
   backend/deploy/cấu trúc dự án; premium-web quyết toàn bộ UI/design** (anti AI-vibe +
   PageSpeed áp nguyên khi build giao diện public).

## Quy trình dựng dự án mới

1. Xác định platform → load refs theo bảng trên.
2. Scaffold theo **blueprint.md** (cấu trúc file, Env, middleware, layout SSR).
3. Schema DB + seed: `schema.sql` **chỉ cho local**; sau khi live dùng `migrations/` tăng dần
   (quy ước ở blueprint mục 9, lệnh ở cloudflare.md mục 3).
4. Build routes public → SEO endpoints (sitemap/robots/llms.txt) → admin (auth) → upload.
5. Nghiệm thu: chạy dev local, test các flow chính; trang public soi checklist PageSpeed
   trong blueprint mục 8.

## Common mistakes

| Sai lầm | Sửa |
|---------|-----|
| Dùng `process.env` trong route | `c.env.X` (Workers) — AWS xem cách map trong aws.md (`env(c)` từ `hono/adapter`) |
| Import `node:*` / `Buffer` trong code chung | Web Standard: `crypto.subtle`, `TextEncoder`, `atob/btoa` |
| Thêm React/framework "cho tiện" | `hono/html` đủ cho SSR; trang public 0 JS là lợi thế cạnh tranh |
| Trộn logic query vào view | View = hàm thuần nhận data đã đủ; query nằm ở render helper của route |
| Quên sanitize HTML từ editor/admin | Sanitizer allowlist **parser-based**, không tự viết regex (blueprint mục 6) |
| Cookie session không ký | HMAC-sign + expiry + HttpOnly + SameSite (blueprint mục 5) |
| Ký session bằng `ADMIN_PASSWORD` | Tách `SESSION_SECRET` riêng; verify bằng `crypto.subtle.verify` (blueprint mục 5) |
| `raw(JSON.stringify(obj))` cho JSON-LD | Escape `<`/`>`/`&`/U+2028/U+2029 trước khi `raw()` (blueprint mục 4) |
| Script npm chạy `schema.sql --remote` | `schema.sql` chỉ local; production đi qua `migrations/` (cloudflare.md mục 3) |
| Lambda Function URL `authType: NONE` | `AWS_IAM` + CloudFront OAC; test `curl` thẳng phải ra 403 (aws.md mục 5) |
| Tin `Content-Type` file upload | Đọc magic bytes; key ngẫu nhiên do server sinh (blueprint mục 7) |
