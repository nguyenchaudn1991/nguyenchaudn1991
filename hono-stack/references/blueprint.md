# Blueprint — kiến trúc app Hono chuẩn (đúc từ topdoanhnghiep.com)

Mọi mẫu code dưới đây đã chạy production. Platform-agnostic — phần deploy xem
cloudflare.md / aws.md.

---

## 1. Cấu trúc file

```
src/
  index.ts        # Env type + domain types + app chính + routes public + SEO endpoints
  views.ts        # SSR trang public: layout() + từng page function + sanitizeHtml
  admin.ts        # sub-app /admin: auth, CRUD, upload
  admin-views.ts  # SSR trang admin (tách khỏi views public)
  i18n.ts         # (nếu đa ngôn ngữ) Locale, từ điển t, helper build path
public/           # asset tĩnh: styles.css, fonts/, images/, favicon.svg
schema.sql        # schema + seed — chạy lại được từ đầu (DROP TABLE IF EXISTS trước CREATE)
migrate_*.sql     # mỗi thay đổi schema sau khi live = 1 file migration riêng, không sửa schema.sql cũ
```

Quy tắc tách file: route nhận request → gọi **render helper** (query DB, gom data) →
gọi **page function** (thuần, chỉ nhận data → trả HTML). View không bao giờ query.

## 2. App chính & Env

```ts
import { Hono } from "hono";

export type Env = {
  DB: D1Database;          // AWS: thay bằng client tương ứng — xem aws.md
  UPLOADS: R2Bucket;
  SITE_URL: string;        // vars thường
  ADMIN_PASSWORD: string;  // secret — không bao giờ nằm trong config commit
};

const app = new Hono<{ Bindings: Env }>();
app.route("/admin", adminApp);   // sub-app tự quản auth
export default app;
```

Domain types (`Category`, `Post`…) export từ `index.ts`, view/admin import lại — 1 nguồn sự thật.

## 3. Middleware — đúng thứ tự

```ts
// 1) Security headers cho mọi HTML động (asset tĩnh dùng cơ chế headers riêng của platform)
app.use("*", async (c, next) => {
  await next();
  c.header("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");
  c.header("X-Frame-Options", "SAMEORIGIN");
  c.header("X-Content-Type-Options", "nosniff");
  c.header("Referrer-Policy", "strict-origin-when-cross-origin");
  c.header("Content-Security-Policy", "default-src 'self'; img-src 'self' data: https:; " +
    "style-src 'self' 'unsafe-inline'; script-src 'self'; base-uri 'self'; form-action 'self'; " +
    "frame-ancestors 'self'; object-src 'none'; upgrade-insecure-requests");
});
// CSP nới thêm domain analytics khi gắn GA/Cloudflare Insights; style 'unsafe-inline'
// chỉ khi content editor sinh style= inline.

// 2) Chuẩn hóa 1 URL duy nhất (SEO): www → apex 301
app.use("*", async (c, next) => {
  const url = new URL(c.req.url);
  if (url.hostname.startsWith("www.")) {
    url.hostname = url.hostname.slice(4);
    return c.redirect(url.toString(), 301);
  }
  await next();
});
```

### notFound & onError — bắt buộc có, đặt cuối `index.ts`

```ts
// 404 render bằng đúng layout của site (không phải trang trắng mặc định)
app.notFound(async (c) => c.html(notFoundPage(await getCategories(c.env.DB)), 404));

// Lỗi runtime: log đầy đủ, trả trang lỗi gọn — không lộ stack trace cho user
app.onError((err, c) => {
  console.error(`[${c.req.method}] ${c.req.path}`, err);
  return c.html(errorPage(), 500);
});
```

## 4. SSR bằng `hono/html`

```ts
import { html, raw } from "hono/html";
import type { HtmlEscapedString } from "hono/utils/html";
type Html = HtmlEscapedString | Promise<HtmlEscapedString>;

export function layout(opts: {
  title: string; description: string; canonical?: string;
  image?: string; head?: Html; body: Html;
}): Html {
  return html`<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>${opts.title}</title>
<meta name="description" content="${opts.description}" />
${opts.canonical ? html`<link rel="canonical" href="${opts.canonical}" />` : ""}
<link rel="stylesheet" href="/styles.css" />
${opts.head ?? ""}
</head>
<body>${opts.body}</body>
</html>`;
}
```

- `html\`\`` tự escape biến chèn vào — an toàn mặc định; chỉ `raw()` cho HTML đã sanitize/tự sinh.
- JSON-LD: `html\`<script type="application/ld+json">${raw(JSON.stringify(obj))}</script>\``.
- Mỗi trang = 1 function `xxxPage(props): Html` gọi `layout({...})`; route trả `c.html(xxxPage(...))`.
- i18n: mỗi locale 1 namespace URL (`/` vi, `/en/...` en); route đăng ký 2 lần trỏ cùng render
  helper với tham số locale; hreflang chỉ in khi bản dịch **tồn tại và đã publish** (query check).

## 5. Auth admin — session cookie ký HMAC, mật khẩu PBKDF2 (100% `crypto.subtle`)

Pattern: token = `username|role|expiry|HMAC(payload, secret)` đặt trong cookie
`HttpOnly; SameSite=Lax; Secure; Max-Age=7d`.

```ts
const enc = new TextEncoder();
async function hmacSign(data: string, secret: string): Promise<string> {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(data));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
// verify: parse cookie → check expiry → re-sign payload → so sánh chữ ký
```

- Mật khẩu user phụ (editor) lưu DB dạng `pbkdf2$iter$salt$hash` — derive bằng
  `crypto.subtle.deriveBits({ name: "PBKDF2", iterations: 100000, hash: "SHA-256" })`.
- Gate middleware đặt **sau** route login/logout, chặn mọi route còn lại của sub-app:
  ```ts
  admin.use("*", async (c, next) => {
    if (["/admin/login", "/admin/logout"].includes(new URL(c.req.url).pathname)) return next();
    const user = await verifySession(c.req.header("Cookie"), c.env.ADMIN_PASSWORD);
    if (!user) return c.redirect("/admin/login");
    c.set("user", user);   // Variables: { user: ... } trong generic của sub-app
    await next();
  });
  ```
- Phân quyền theo role ngay trong handler (`if (user.role !== "admin") return c.redirect("/admin")`);
  editor chỉ sửa/xóa bài của mình (check `created_by`).

## 6. Sanitize HTML từ editor (bắt buộc — lớp server)

Nội dung dán từ Word/WYSIWYG phải qua sanitize trước khi lưu **và** trước khi render bản cũ:
xóa `script/style/iframe/object/form/meta...`, comment (kể cả `<!--[if mso]>`), thẻ namespace
Office (`<o:p>`), mọi thuộc tính `on*=`, `javascript:` URL; thuộc tính `style=` chỉ giữ
`color` + `text-align`; `<img>` chỉ nhận `src` là `/uploads/...` hoặc `http(s)` (chặn `data:`,
`file:`). Mẫu regex đầy đủ: `topdoanhnghiep/src/views.ts` hàm `sanitizeHtml`.

## 7. Patterns CRUD đã kiểm chứng

- **Form error UX:** validate fail → render lại form kèm message + status 400, giữ nguyên
  data user đã nhập (`renderFormWithError` pattern) — không redirect mất dữ liệu.
- **UNIQUE conflict:** bắt lỗi từ DB, dịch sang thông báo người dùng ("slug đã tồn tại") —
  không dùng lỗi thô.
- **Slug:** validate `/^[a-z0-9-]+$/`; sinh từ tên có dấu: NFD normalize → bỏ dấu → `đ→d`.
- **published_at:** chỉ set lần đầu publish (`CASE WHEN ?='published' AND published_at IS NULL`).
- **Preview:** POST form → render đúng page function của site với flag `preview: true`
  (khách thấy đúng giao diện thật trước khi publish); bài đã lưu có thêm preview GET để share link.
- **Upload:** validate size (≤5MB) + content-type whitelist (`webp/jpeg/png`); key có
  timestamp `uploads/${Date.now()}-${name}.ext` → cache immutable 1 năm được; nén WebP
  phía trình duyệt trước khi gửi.
- **Múi giờ:** serverless chạy UTC — thời gian hiển thị VN phải cộng thủ công
  `new Date(Date.now() + 7 * 3600e3)` (hoặc lưu UTC + format bằng `Intl` theo timezone).

## 8. SEO endpoints (route động, không file tĩnh)

- **`/sitemap.xml`:** query mọi entity có URL → build XML; bài đa ngôn ngữ chỉ xuất URL
  đúng namespace locale (tránh 404 trong sitemap); `lastmod` từ `updated_at`.
- **`/robots.txt`:** `Allow: /`, `Disallow: /admin`, trỏ sitemap.
- **`/llms.txt`:** mô tả site + link trang chính cho AI crawler (ChatGPT/Gemini/Perplexity).
- Mỗi trang: 1 `<h1>`, canonical, OG đủ, JSON-LD đúng loại (ItemList/LocalBusiness/Article).
- **Checklist PageSpeed trước mỗi commit UI** (rút từ PAGESPEED.md production):
  hero preload + `fetchpriority="high"`, không lazy hero; mọi `<img>` có width/height;
  font `display=swap` + fallback render đúng dấu VN; trang public không thêm JS;
  analytics tải trễ qua `requestIdleCallback` (chỉ `async` là chưa đủ — từng gây LCP +2s);
  contrast WCAG AA, link trong đoạn văn phải gạch chân; touch target ≥44px, input ≥16px.

## 9. Schema SQL — quy ước

- `schema.sql` = schema + seed, chạy lại từ đầu được (DROP trước CREATE) — dev local reset thoải mái.
- Sau khi live: mỗi thay đổi = file `migrate_*.sql` riêng, apply thủ công lên remote.
- Cột quy ước: `slug UNIQUE` (hoặc `UNIQUE(slug, locale)` khi đa ngôn ngữ), `status 'draft'|'published'`,
  `created_at/updated_at TEXT DEFAULT (datetime('now'))`, `sort_order`, `active INTEGER`.
- Index cho query list thực tế (`CREATE INDEX idx_biz_cat ON businesses(category_id, rank)`).
- Cột dịch: `name_en TEXT DEFAULT ''` — rỗng = fallback về tiếng Việt (helper `localized()`).
