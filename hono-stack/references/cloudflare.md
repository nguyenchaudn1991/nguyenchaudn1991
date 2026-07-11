# Cloudflare — deploy Hono lên Workers (D1 + R2 + Assets)

Mặc định cho dự án cá nhân. Entry: `export default app` — Workers hiểu trực tiếp, không adapter.

---

## 1. package.json tối thiểu

```json
{
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "db:local": "wrangler d1 execute <db-name> --local --file=./schema.sql",
    "db:remote": "wrangler d1 execute <db-name> --remote --file=./schema.sql"
  },
  "dependencies": { "hono": "^4.6.0" },
  "devDependencies": {
    "@cloudflare/workers-types": "^4",
    "typescript": "^5",
    "wrangler": "^4"
  }
}
```

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
  "compatibility_date": "2026-01-01",
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
npx wrangler secret put ADMIN_PASSWORD # secret production
npm run deploy
# migration sau khi live:
npx wrangler d1 execute <db> --remote --file=./migrate_xxx.sql
```

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

- Free tier: 100k req/ngày, D1 5GB, R2 10GB — dư cho site nội dung; Workers Paid ($5) khi vượt.
- Worker CPU limit: tránh xử lý ảnh/nén nặng trong Worker — nén phía trình duyệt trước khi upload (pattern blueprint mục 7).
- Cần cron → `"triggers": { "crons": [...] }` + `scheduled` handler; cần queue/stateful →
  Queues / Durable Objects — lúc đó gọi thêm skill `cloudflare` / `durable-objects` / `workers-best-practices` nếu có trong môi trường.
- D1 là SQLite: không connection pool, transaction qua `db.batch([...])`; tránh N+1 bằng JOIN.
