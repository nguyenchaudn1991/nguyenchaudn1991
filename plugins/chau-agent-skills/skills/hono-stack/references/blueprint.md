# Blueprint — kiến trúc app Hono chuẩn (đúc từ topdoanhnghiep.com)

Mọi mẫu code dưới đây đã chạy production. Platform-agnostic — phần deploy xem
cloudflare.md / aws.md.

## Mục lục

| # | Mục | Đọc khi |
|---|---|---|
| 1–2 | Cấu trúc file · App chính & Env | Scaffold project mới |
| 3 | Middleware (security headers, CSP, HSTS, canonical URL) | Luôn luôn |
| 4 | SSR bằng `hono/html` · **JSON-LD an toàn** | Viết view |
| 5 | **Auth admin** (session HMAC, PBKDF2, CSRF) | Có khu vực đăng nhập |
| 6 | **Sanitize HTML từ editor** | Nhận nội dung từ WYSIWYG/Word |
| 7 | Patterns CRUD · **upload** · múi giờ | Làm form/CRUD |
| 8 | SEO endpoints · checklist PageSpeed | Trang public |
| 9 | Schema SQL & migration | Đụng DB |

Mục **3, 4, 5, 6, 7** có phần security — đọc nguyên mục, đừng chỉ copy code block.

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
schema.sql        # schema + seed — CHỈ LOCAL (có DROP TABLE IF EXISTS), không bao giờ chạy --remote
migrations/       # sau khi live: mỗi thay đổi schema = 1 file ở đây, apply tăng dần
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
  ADMIN_PASSWORD: string;  // secret — CHỈ để verify lúc login
  SESSION_SECRET: string;  // secret — CHỈ để ký session; độc lập hoàn toàn với mật khẩu
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
  c.header("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
  c.header("X-Frame-Options", "SAMEORIGIN");
  c.header("X-Content-Type-Options", "nosniff");
  c.header("Referrer-Policy", "strict-origin-when-cross-origin");
  c.header("Content-Security-Policy", "default-src 'self'; img-src 'self' data: https:; " +
    "style-src 'self' 'unsafe-inline'; script-src 'self'; base-uri 'self'; form-action 'self'; " +
    "frame-ancestors 'self'; object-src 'none'; upgrade-insecure-requests");
});
// CSP nới thêm domain analytics khi gắn GA/Cloudflare Insights.
//
// `style-src 'unsafe-inline'` ở đây là ĐÁNH ĐỔI CÓ CHỦ Ý, không phải mặc định vô thưởng
// vô phạt: sanitizer (mục 6) cho phép giữ `style="color|text-align"` từ nội dung editor.
// Muốn bỏ 'unsafe-inline' → sửa sanitizer strip sạch `style=`, chuyển sang class. Giữ
// `script-src 'self'` (không 'unsafe-inline') trong mọi trường hợp — đó mới là lớp chặn XSS.
//
// HSTS: KHÔNG thêm `preload` mặc định. `preload` là cam kết một chiều, gỡ ra rất chậm và
// khoá TOÀN BỘ subdomain vào HTTPS. Chỉ thêm khi đã đủ: mọi subdomain (kể cả nội bộ/
// staging) chạy HTTPS, includeSubDomains đã chạy ổn định một thời gian, và chủ domain
// hiểu chi phí rollback.

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
- **JSON-LD — `raw(JSON.stringify(obj))` là lỗ XSS.** `raw()` của Hono không escape gì cả,
  nên chỉ cần một trường trong `obj` (tên bài, mô tả do admin nhập) chứa `</script>` là
  thoát khỏi thẻ và chạy được script. Serialize qua hàm riêng:

  ```ts
  // Escape ký tự có nghĩa trong ngữ cảnh <script>. Kết quả vẫn là JSON hợp lệ
  // (\uXXXX nằm trong string literal), parser JSON-LD đọc bình thường.
  function jsonLdScript(obj: unknown): string {
    return JSON.stringify(obj)
      .replace(/</g, "\\u003c")
      .replace(/>/g, "\\u003e")
      .replace(/&/g, "\\u0026")
      .replace(/\u2028/g, "\\u2028")    // LINE SEPARATOR — phá JS string
      .replace(/\u2029/g, "\\u2029");  // PARAGRAPH SEPARATOR
  }
  // dùng: html`<script type="application/ld+json">${raw(jsonLdScript(obj))}</script>`
  ```

  Test regression bắt buộc: đặt title bài = `</script><script>alert(1)</script>` rồi
  xem raw HTML — phải thấy chuỗi đã escape, không thấy thẻ `<script>` thứ hai.
- Mỗi trang = 1 function `xxxPage(props): Html` gọi `layout({...})`; route trả `c.html(xxxPage(...))`.
- i18n: mỗi locale 1 namespace URL (`/` vi, `/en/...` en); route đăng ký 2 lần trỏ cùng render
  helper với tham số locale; hreflang chỉ in khi bản dịch **tồn tại và đã publish** (query check).

## 5. Auth admin — session cookie ký HMAC, mật khẩu PBKDF2 (100% `crypto.subtle`)

Pattern: token = `v1|username|role|expiry|HMAC(payload, SESSION_SECRET)` đặt trong cookie
`HttpOnly; Secure; SameSite=Lax; Path=/admin; Max-Age=7d`.

> **Hai secret, hai việc — không được gộp.** `SESSION_SECRET` ký session; `ADMIN_PASSWORD`
> chỉ dùng verify lúc login. Lấy mật khẩu làm khoá ký thì đổi mật khẩu là đá văng toàn bộ
> session, và bất kỳ chỗ nào lộ khoá ký đều thành lộ mật khẩu đăng nhập.
> `SESSION_SECRET` sinh ngẫu nhiên ≥ 32 byte, lưu bằng cơ chế secret của platform.

```ts
const enc = new TextEncoder();

// 1 key cho cả sign lẫn verify → verify dùng được crypto.subtle.verify
async function sessionKey(secret: string) {
  return crypto.subtle.importKey("raw", enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

export async function signSession(username: string, role: string, secret: string) {
  // username/role không được chứa "|" — validate ngay lúc tạo user
  const payload = `v1|${username}|${role}|${Date.now() + 7 * 864e5}`;
  const sig = await crypto.subtle.sign("HMAC", await sessionKey(secret), enc.encode(payload));
  const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return `${payload}|${hex}`;
}

export async function verifySession(token: string | undefined, secret: string) {
  if (!token) return null;
  const i = token.lastIndexOf("|");
  if (i < 0) return null;
  const payload = token.slice(0, i);
  const hex = token.slice(i + 1);
  if (!/^[0-9a-f]{64}$/.test(hex)) return null;
  const sig = Uint8Array.from(hex.match(/../g)!, (h) => parseInt(h, 16));
  // crypto.subtle.verify so sánh constant-time. KHÔNG re-sign rồi `===` chuỗi —
  // so sánh chuỗi thoát sớm ở byte khác nhau đầu tiên, rò rỉ qua thời gian phản hồi.
  const ok = await crypto.subtle.verify("HMAC", await sessionKey(secret), sig, enc.encode(payload));
  if (!ok) return null;
  const [v, username, role, expiry] = payload.split("|");
  if (v !== "v1") return null;                      // bump "v1" = vô hiệu hoá mọi session cũ
  if (!(Number(expiry) > Date.now())) return null;  // check expiry SAU khi chữ ký hợp lệ
  return { username, role };
}
```

- Mật khẩu lưu DB dạng `pbkdf2$iter$salt$hash` — **lưu kèm `iter` trong chuỗi hash** để
  nâng cost sau này mà không làm hỏng hash cũ. Số vòng lặp lấy theo
  [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
  ở thời điểm dựng project (mức khuyến nghị cho PBKDF2-HMAC-SHA256 đã lên tới hàng trăm
  nghìn vòng và còn tăng) — **đọc lại tài liệu, đừng chép con số từ file này**. Runtime hỗ
  trợ Argon2id thì ưu tiên Argon2id. Khi user đăng nhập mà `iter` trong hash thấp hơn mức
  hiện hành → re-hash và ghi đè.
- **CSRF:** `SameSite=Lax` đã chặn cookie đi kèm POST cross-site — đó là lớp chính. Bổ sung
  cho mọi route mutation: đối chiếu header `Origin` với `SITE_URL` (hoặc yêu cầu
  `Sec-Fetch-Site: same-origin`), lệch thì trả 403.
- Gate middleware đặt **sau** route login/logout, chặn mọi route còn lại của sub-app:
  ```ts
  admin.use("*", async (c, next) => {
    if (["/admin/login", "/admin/logout"].includes(new URL(c.req.url).pathname)) return next();
    const user = await verifySession(getCookie(c, "session"), c.env.SESSION_SECRET);
    if (!user) return c.redirect("/admin/login");
    c.set("user", user);   // Variables: { user: ... } trong generic của sub-app
    await next();
  });
  ```
- Phân quyền theo role ngay trong handler (`if (user.role !== "admin") return c.redirect("/admin")`);
  editor chỉ sửa/xóa bài của mình (check `created_by`).

## 6. Sanitize HTML từ editor (bắt buộc — lớp server)

> **Không tự viết sanitizer bằng regex.** HTML không phải ngôn ngữ chính quy: thẻ lồng sai,
> attribute thiếu ngoặc, entity mã hoá nhiều lớp, ngữ cảnh parse riêng của `<svg>`/`<math>`…
> đều có biến thể qua mặt regex. Và danh sách "xoá thẻ xấu" (blacklist) thì luôn thiếu —
> phải là **allowlist chạy trên parser thật**.

Dùng sanitizer allowlist đã được audit và còn bảo trì, chạy ở **tầng server**. Sanitize
**trước khi lưu**, và sanitize lại **trước khi render nội dung cũ** — dữ liệu lưu từ trước
khi có sanitizer vẫn nằm trong DB.

Allowlist tối thiểu cho nội dung bài viết:

| Nhóm | Cho phép |
|---|---|
| Thẻ | `p br strong em u s h2 h3 h4 ul ol li blockquote a img table thead tbody tr th td` |
| `a` | `href` chỉ `http(s):` / `mailto:` / đường dẫn nội bộ `/…`; ép `rel="noopener nofollow"` khi trỏ ra ngoài |
| `img` | `src` chỉ `/uploads/…` hoặc `https:`; `alt`, `width`, `height` |
| `style=` | chỉ `color`, `text-align` — hoặc bỏ hẳn nếu muốn siết CSP (mục 3) |
| Bỏ sạch | `script style iframe object embed form input meta link svg math`, mọi `on*=`, URL `javascript:`/`data:`/`file:`, comment (kể cả `<!--[if mso]>`), thẻ namespace Office (`<o:p>`) |

Corpus test chạy lại mỗi lần đổi sanitizer:
`<img src=x onerror=alert(1)>` · `<svg><script>alert(1)</script></svg>` ·
`<a href="java&#115;cript:alert(1)">` · `<div onclick=alert(1)>` ·
`<p style="background:url(javascript:alert(1))">` · thẻ không đóng · entity mã hoá 2 lớp.

Không có sanitizer chạy được trên runtime đích → **lưu plain text hoặc Markdown rồi render
bằng renderer có escape**, đừng nhận HTML thô rồi tự lọc.

## 7. Patterns CRUD đã kiểm chứng

- **Form error UX:** validate fail → render lại form kèm message + status 400, giữ nguyên
  data user đã nhập (`renderFormWithError` pattern) — không redirect mất dữ liệu.
- **UNIQUE conflict:** bắt lỗi từ DB, dịch sang thông báo người dùng ("slug đã tồn tại") —
  không dùng lỗi thô.
- **Slug:** validate `/^[a-z0-9-]+$/`; sinh từ tên có dấu: NFD normalize → bỏ dấu → `đ→d`.
- **published_at:** chỉ set lần đầu publish (`CASE WHEN ?='published' AND published_at IS NULL`).
- **Preview:** POST form → render đúng page function của site với flag `preview: true`
  (khách thấy đúng giao diện thật trước khi publish); bài đã lưu có thêm preview GET để share link.
- **Upload:** `Content-Type` và đuôi file là do client khai — **không tin**. Đọc magic bytes
  để biết định dạng thật (`FF D8 FF` JPEG · `89 50 4E 47` PNG · `RIFF`…`WEBP`), lệch
  whitelist thì từ chối. Validate cả size (≤5MB) **và** kích thước ảnh (chặn decompression
  bomb). **Key do server sinh, ngẫu nhiên** — `uploads/${crypto.randomUUID()}.webp` — không
  dùng tên file người dùng (tránh path traversal, đè key, polyglot); tên gốc lưu riêng làm
  nhãn hiển thị và phải escape khi render. Serve kèm `Content-Type` đúng +
  `X-Content-Type-Options: nosniff` + `Content-Disposition: inline`. Vẫn giữ nén WebP phía
  trình duyệt trước khi gửi.
- **Múi giờ:** serverless chạy UTC. **Lưu UTC, chỉ đổi lúc hiển thị:**
  `new Intl.DateTimeFormat("vi-VN", { timeZone: "Asia/Ho_Chi_Minh", … }).format(d)`.
  Không cộng tay `+7h` vào timestamp — giá trị sau khi cộng không còn là epoch đúng, và rất
  dễ bị cộng lần thứ hai ở tầng khác.

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

- `schema.sql` = schema + seed, chạy lại từ đầu được (DROP trước CREATE) — **CHỈ dùng cho
  local**. Vì có `DROP`, tuyệt đối không tạo script npm nào chạy file này với `--remote`.
- Sau khi live: mỗi thay đổi = 1 file trong `migrations/`, apply bằng
  `wrangler d1 migrations apply` (cloudflare.md mục 3). Không sửa file migration đã apply.
- Cột quy ước: `slug UNIQUE` (hoặc `UNIQUE(slug, locale)` khi đa ngôn ngữ), `status 'draft'|'published'`,
  `created_at/updated_at TEXT DEFAULT (datetime('now'))`, `sort_order`, `active INTEGER`.
- Index cho query list thực tế (`CREATE INDEX idx_biz_cat ON businesses(category_id, rank)`).
- Cột dịch: `name_en TEXT DEFAULT ''` — rỗng = fallback về tiếng Việt (helper `localized()`).
