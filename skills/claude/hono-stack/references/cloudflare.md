# Cloudflare — deploy Hono lên Workers (D1 + R2 + Assets)

## Mục lục

1. [package.json tối thiểu](#1-packagejson-tối-thiểu)
2. [wrangler.jsonc mẫu](#2-wranglerjsonc-mẫu-annotated)
3. [Lệnh khởi tạo & vận hành](#3-lệnh-khởi-tạo--vận-hành)
4. [Cache asset](#4-cache-asset--public_headers)
5. [Giới hạn & mở rộng](#5-giới-hạn--mở-rộng)

Mặc định cho dự án cá nhân. Entry: `export default app` — Workers hiểu trực tiếp, không adapter.

---

## 1. package.json tối thiểu

```json
{
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "db:local": "wrangler d1 execute <db-name> --local --file=./schema.sql",
    "db:local:reset": "wrangler d1 execute <db-name> --local --file=./schema.sql",
    "db:migrate:local": "wrangler d1 migrations apply <db-name> --local",
    "db:migrate:remote": "wrangler d1 migrations apply <db-name> --remote"
  },
  "dependencies": { "hono": "^4.6.0" },
  "devDependencies": {
    "@cloudflare/workers-types": "^4",
    "typescript": "^5",
    "wrangler": "^4"
  }
}
```

> ⚠️ **KHÔNG tạo script nào chạy `schema.sql` với `--remote`.** `schema.sql` có
> `DROP TABLE IF EXISTS` (blueprint.md mục 9) → một lệnh là mất sạch dữ liệu production, và tên script
> kiểu `db:remote` khiến người/Agent gõ nhầm rất dễ. `schema.sql` **chỉ dùng cho local**.
> Mọi thay đổi schema trên môi trường đã live đi qua migration tăng dần (mục 3).

tsconfig.json tối thiểu (sai `types` là đỏ toàn bộ bindings):

```jsonc
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "lib": ["ESNext"],
    "types": ["@cloudflare/workers-types"],
    "noEmit": true
  },
  "include": ["src"]
}
```

## 2. wrangler.jsonc mẫu (annotated)

```jsonc
{
  "name": "<project>",
  "main": "src/index.ts",
  // Đặt = ngày tạo project (ngày đã test thật), KHÔNG copy ngày trong tài liệu này.
  // Bump = thay đổi hành vi runtime → chỉ bump kèm regression test.
  "compatibility_date": "<YYYY-MM-DD ngày khởi tạo project>",
  // Custom domain: Cloudflare tự tạo DNS + SSL khi deploy (domain phải nằm trong account)
  "routes": [
    { "pattern": "example.com", "custom_domain": true },
    { "pattern": "www.example.com", "custom_domain": true }  // app 301 về apex (blueprint mục 3)
  ],
  // Asset tĩnh serve trước Worker — file khớp path trả thẳng, không tính request Worker
  "assets": { "directory": "./public", "binding": "ASSETS" },
  "d1_databases": [
    { "binding": "DB", "database_name": "<db>", "database_id": "<uuid sau khi create>" }
  ],
  "r2_buckets": [
    { "binding": "UPLOADS", "bucket_name": "<project>-uploads" }
  ],
  // vars = config công khai; secret KHÔNG để đây
  "vars": { "SITE_URL": "https://example.com" }
}
```

## 3. Lệnh khởi tạo & vận hành

```bash
npx wrangler d1 create <db>            # lấy database_id điền vào wrangler.jsonc
npx wrangler r2 bucket create <name>
npm run db:local                       # nạp schema + seed vào D1 local (.wrangler/state)
npx wrangler dev                       # dev local (assets + D1 local + R2 local)
npx wrangler secret put ADMIN_PASSWORD # mật khẩu đăng nhập admin
npx wrangler secret put SESSION_SECRET # khoá ký session — KHÁC ADMIN_PASSWORD (blueprint mục 5)
npm run deploy
```

**Migration sau khi live** — dùng thư mục `migrations/`, không chạy file `.sql` rời:

```bash
npx wrangler d1 migrations create <db> add_column_x   # sinh migrations/0001_add_column_x.sql
npm run db:migrate:local                              # thử trên local trước
npx wrangler d1 migrations list <db> --remote         # xem cái nào sắp apply
npm run db:migrate:remote                             # apply lên production
```

Gate bắt buộc trước khi apply lên production:

1. Đã apply thành công trên local **và** trên một D1 preview/staging.
2. Đã `migrations list --remote` và đọc đúng danh sách sắp chạy.
3. Migration chỉ tiến (thêm cột/bảng/index). Cần `DROP`/`ALTER` phá huỷ → export dữ liệu
   trước (`wrangler d1 export`), và **xin xác nhận của người chủ dữ liệu**, không tự chạy.
4. `database_id`/environment ghi tường minh trong lệnh hoặc config — không dựa vào default.

- Secret khi dev local: file `.dev.vars` (gitignore) — `ADMIN_PASSWORD=...`.
- Types cho bindings: `wrangler types` sinh `worker-configuration.d.ts`.

## 4. Cache asset — `public/_headers`

```
/images/*
  Cache-Control: public, max-age=86400
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/styles.css
  Cache-Control: public, max-age=3600
```
Quy tắc: file thay-cùng-tên → max-age ngắn (1 ngày); file có hash/timestamp trong tên →
1 năm immutable. Ảnh upload R2 (key có timestamp) serve qua route với
`Cache-Control: public, max-age=31536000, immutable`:

```ts
app.get("/uploads/*", async (c) => {
  const obj = await c.env.UPLOADS.get(c.req.path.slice(1));
  if (!obj) return c.notFound();
  return new Response(obj.body, {
    headers: {
      "Content-Type": obj.httpMetadata?.contentType || "image/webp",
      "Cache-Control": "public, max-age=31536000, immutable",
    },
  });
});
```

## 5. Giới hạn & mở rộng

- Free tier: đủ dùng cho site nội dung; Workers Paid khi vượt. **Hạn mức và giá thay đổi
  thường xuyên — không tư vấn chi phí từ trí nhớ.** Đọc lại trước khi báo khách:
  [Workers limits](https://developers.cloudflare.com/workers/platform/limits/) ·
  [Pricing](https://developers.cloudflare.com/workers/platform/pricing/).
- Worker CPU limit: tránh xử lý ảnh/nén nặng trong Worker — nén phía trình duyệt trước khi upload (pattern blueprint mục 7).
- Cần cron → `"triggers": { "crons": [...] }` + `scheduled` handler; cần queue/stateful →
  Queues / Durable Objects — lúc đó gọi thêm skill `cloudflare` / `durable-objects` / `workers-best-practices` nếu có trong môi trường.
- D1 là SQLite: không connection pool, transaction qua `db.batch([...])`; tránh N+1 bằng JOIN.
