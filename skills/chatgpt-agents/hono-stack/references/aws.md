# AWS — deploy Hono lên Lambda (dự án công ty, cùng stack MEO dashboard)

## Mục lục

1. [Entry — adapter](#1-entry--adapter-honoaws-lambda)
2. [Env & bindings](#2-env--bindings--khác-biệt-lớn-nhất-so-với-workers)
3. [Map storage](#3-map-storage-cloudflare--aws)
4. [Expose HTTP](#4-expose-http--chọn-1)
5. [IaC tối thiểu](#5-iac-tối-thiểu-cdk--tham-khảo-dự-án-công-ty-theo-chuẩn-infra-sẵn-có)
6. [Dev local](#6-dev-local--khác-biệt-runtime-cần-nhớ)

Cùng 1 app Hono, chỉ đổi **entry** + cách nạp env + tầng storage. Code routes/views/auth
giữ nguyên nếu blueprint được tuân thủ (Web Standard APIs only).

---

## 1. Entry — adapter `hono/aws-lambda`

```ts
// src/lambda.ts  (entry AWS — src/index.ts vẫn export default app cho Cloudflare)
import { handle } from "hono/aws-lambda";
import app from "./index";
export const handler = handle(app);
```

Bundle bằng esbuild. **`--target` phải khớp runtime khai trong IaC** (mục 5) — một version
duy nhất dùng chung cho code, CI và tài liệu:
```bash
esbuild src/lambda.ts --bundle --platform=node --target=node22 \
  --format=esm --outfile=dist/index.mjs --external:@aws-sdk/*
```

## 2. Env & bindings — khác biệt lớn nhất so với Workers

Lambda không có "bindings" — env vào qua `process.env`. Để code chung không đổi, dùng
helper `env()` của Hono (tự đọc đúng nguồn theo runtime):

```ts
import { env } from "hono/adapter";
app.get("/x", (c) => {
  const { SITE_URL } = env<{ SITE_URL: string }>(c); // Workers: c.env / Lambda: process.env
});
```

- Config thường → Lambda environment variables (đặt trong IaC).
- Secret → **SSM Parameter Store (SecureString)** hoặc Secrets Manager; đọc 1 lần lúc cold
  start, cache ở module scope (không đọc mỗi request).
- Type `Env` trong `index.ts` vẫn là 1 nguồn sự thật — trên AWS, khởi tạo object env/clients
  ở entry rồi truyền vào qua `app.use` set vào `c.env`-tương-đương (contextStorage) hoặc
  module singleton.

## 3. Map storage Cloudflare → AWS

| Cloudflare | AWS | Ghi chú |
|---|---|---|
| D1 (SQLite) | **Aurora Serverless v2 (Postgres/MySQL) + RDS Proxy**, hoặc DynamoDB | Query layer nên bọc sau 1 interface `db.ts` để swap; theo chuẩn dự án công ty đang dùng |
| R2 | **S3** (`@aws-sdk/client-s3`) | Upload giữ nguyên pattern validate + timestamped key; serve qua CloudFront, không stream qua Lambda |
| Assets binding (`public/`) | **S3 + CloudFront** | CloudFront behavior: `/images/*`, `/fonts/*`… trỏ S3; default behavior trỏ Lambda |
| `wrangler secret` | SSM/Secrets Manager | |
| Workers cron triggers | EventBridge Scheduler → Lambda | |

`@aws-sdk/*` chỉ import trong file tầng AWS (entry/db/s3 client) — không lọt vào
views/routes chung.

## 4. Expose HTTP — chọn 1

| Cách | Khi nào |
|---|---|
| **Lambda Function URL (`AWS_IAM`) + CloudFront OAC** | Mặc định cho web SSR — rẻ, đơn giản, CloudFront lo custom domain + cache + WAF. Bắt buộc IAM+OAC, xem mục 5 |
| API Gateway HTTP API | Cần authorizer/throttling/usage plan chuẩn hạ tầng công ty |
| ALB | Đã có VPC/ALB sẵn trong hệ thống nội bộ |

CloudFront trước Lambda: cache HTML động `max-age` ngắn hoặc bỏ qua; asset S3 cache dài
(tương đương `_headers` bên Cloudflare — cache policy đặt ở CloudFront behavior).

## 5. IaC tối thiểu (CDK — tham khảo; dự án công ty theo chuẩn infra sẵn có)

```ts
const fn = new lambdaNodejs.NodejsFunction(this, "App", {
  entry: "src/lambda.ts",
  runtime: lambda.Runtime.NODEJS_22_X,
  memorySize: 512,
  environment: { SITE_URL: "https://example.com" },
});
// authType AWS_IAM + OAC: Function URL KHÔNG gọi thẳng được, bắt buộc qua CloudFront.
const url = fn.addFunctionUrl({ authType: lambda.FunctionUrlAuthType.AWS_IAM });
const oac = new cloudfront.FunctionUrlOriginAccessControl(this, "Oac", {
  signing: cloudfront.Signing.SIGV4_ALWAYS,
});
// default behavior → FunctionUrlOrigin.withOriginAccessControl(url, { originAccessControl: oac })
// /assets/*        → S3Origin(bucket)
```

> ⚠️ **Không dùng `FunctionUrlAuthType.NONE`.** Function URL khi đó là public endpoint:
> ai biết URL đều gọi thẳng Lambda, **bỏ qua CloudFront và WAF** — mọi rule rate-limit/
> geo-block/bot đặt ở CloudFront thành vô nghĩa. Dùng `AWS_IAM` + Origin Access Control để
> chỉ CloudFront ký được request.
>
> **Test bắt buộc:** `curl` thẳng vào Function URL phải trả `403`. Nếu trả `200` là còn
> đường bypass — chưa được lên production. Nếu hạ tầng công ty bắt buộc `NONE`, phải bù
> bằng cách verify shared secret header do CloudFront gắn, ngay tại tầng app.

Nếu công ty dùng Terraform/SAM/Serverless Framework → giữ nguyên phần code Hono, chỉ
viết lại khối IaC theo chuẩn đó.

## 6. Dev local & khác biệt runtime cần nhớ

- Dev local không cần Lambda: `@hono/node-server` chạy thẳng app —
  ```ts
  // dev.ts
  import { serve } from "@hono/node-server";
  import app from "./index";
  serve({ fetch: app.fetch, port: 3000 });
  ```
- Cold start: giữ dependency mỏng (esbuild bundle 1 file), init client ở module scope.
- Lambda có Node APIs nhưng **đừng dùng** trong code chung (giữ tính portable về Workers).
- Timezone Lambda cũng là UTC — quy tắc +7h/`Intl` trong blueprint mục 7 áp nguyên.
- Log: `console.log` → CloudWatch; thêm request-id middleware khi cần trace.
