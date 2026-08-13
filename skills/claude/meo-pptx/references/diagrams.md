# Diagram & slide patterns — build spec

House patterns cho content slide. Chọn pattern theo bảng §3a trong SKILL.md, rồi build đúng spec dưới.

## Mục lục

- Comparison table
- Current-vs-Improved flow (現状フロー → 改善フロー)
- Before/After effect table
- Numbered step explanation
- Sequence-style architecture diagram (処理シーケンス図)
- Use case diagram (ユースケース図)
- User flow diagram (ユーザーフロー図)
- Swimlane diagram (スイムレーン図)
- Categorized table (カテゴリ分類表)
- Simple chart (数値の可視化)
- Horizontal timeline (スケジュール)
- 2×2 matrix (優先度マトリクス)

---


Every content slide uses at least one:

- **Comparison table** — e.g. 案A vs 案B, 現行 vs 提案 (dùng tên thật của phương án đang bàn;
  tránh ví dụ gắn tên model/sản phẩm cụ thể vì chúng lỗi thời rất nhanh). Ice-blue (`CBD5E8`) header row,
  `CCCCCC` borders, ✅/❌ or ◯/✕ marks; highlight the recommended column subtly.
- **Current-vs-Improved flow (現状フロー → 改善フロー)** — the signature layout:
  - Two labeled blocks: **現状フロー** and **改善フロー**.
  - Each is a **vertical stack of step boxes** (ice-blue fill, navy text) connected by
    **downward arrows ↓**.
  - Optional middle arrow/divider between the two flows.
  - Put the pain point in `C00000`, the gain in green.
- **Before/After effect table** — rows of metric | 改善前 | 改善後 | 効果(%); express the
  improvement (e.g. 「50〜70%減」「98%減」) — green for the gain column.
- **Numbered step explanation** — when describing a process (API取得 → Sleep() → DB…).
- **Sequence-style architecture diagram (処理シーケンス図)** — the signature layout for
  architecture / system-integration / use-case topics (this is what the customer expects
  instead of a sparse box-and-arrow row):
  - **5–7 component columns** as lifeline headers across the top (navy `0E2240` header
    boxes, white bold text; the NEW/proposed component in red `C00000`), e.g.
    監視対象システム / Datadog / エージェント / 外部API / Slack / 担当者.
  - **Dashed vertical lifelines** (grey `9AA7BC`, dashType dash) under each header.
  - **Numbered horizontal arrows ①②③… top→bottom** between lifelines (navy 1.75pt,
    triangle head pointing in the flow direction). Label above each arrow: red bold
    circled number + navy bold 9.5pt text carrying **concrete data** — API name, payload
    fields, formats (アラートID・重大度 / Logs API / Block Kit形式), not generic verbs.
  - **Self-steps** (a component processing internally) as a small ice-blue box centered
    on its lifeline with the numbered label inside.
  - **技術ポイント strip** at the bottom: 4 small cells (red bold label + navy detail),
    e.g. 実行環境 / 使用API / 所要時間(試算) / セキュリティ.
  - Target 7–9 numbered steps; reference the step numbers in the takeaway band
    (e.g. 「追加開発は③〜⑦のみ」).
- **Use case diagram (ユースケース図)** — for "who can do what" overview slides:
  - **System boundary**: large `EEF1F6` rect with a navy top band carrying the system
    name; use cases as **ice-blue ellipses inside**, each labeled red circled number +
    navy bold text.
  - **Layout rule — no line crossings**: human-facing use cases in the LEFT column
    (near the actors), automated/system use cases in the RIGHT column (near external
    systems). Connector lines must not cross an ellipse.
  - **Actors** = stick figures drawn from shapes (head ellipse + 4 lines, navy 1.75pt),
    label below. **External systems** = grey dashed-border rects on the right, labeled
    「（外部システム）」. Never use emoji or clip-art for actors.
  - Add a **role legend strip** under the diagram (担当者＝…／管理者＝…／①〜③＝全自動)
    and reference the numbers in the takeaway.
- **User flow diagram (ユーザーフロー図／フローチャート)** — for operation/screen flows:
  - Vertical main path: navy **start pill** (roundRect) → numbered ice-blue step boxes →
    **decision diamond** (white fill, red 1.75pt border, red circled number) → green
    **end pill**. Branch labels はい／いいえ next to the arrows (red bold for the
    critical branch), keep them 1–3 characters — put the detailed condition elsewhere.
  - Branch path runs to the RIGHT as its own numbered column.
  - **Density comes from side cards**: left column carries 判断基準 and 所要時間の目安
    cards (navy band + `EEF1F6` body) so the flow itself stays readable.
- **Swimlane diagram (スイムレーン図)** — for cross-role processes:
  - 3–4 horizontal lanes, navy header cell on the left (role name, white bold),
    lane bodies alternating `FFFFFF` / `EEF1F6` with `CCCCCC` border.
  - Steps as ice-blue boxes placed **inside the owning role's lane**, numbered
    ①②…, each with a small grey note line (SLA・成果物). Start step columns at
    x ≥ lane-header right edge + 0.9" so boxes never overlap the headers.
  - Arrows (navy, triangle head) connect step to step across lanes, including
    diagonals; add an **SLA strip** (`CBD5E8`) under the lanes.
- **Categorized table (カテゴリ分類表)** — for feature/requirement inventories:
  - First column = category cells with `rowspan`, fill `1E293B`, white bold, centered.
  - Header row `CBD5E8`; body rows navy text; **優先度 column** uses ◎（red bold）／
    ○（navy）／△（grey）with a legend line under the table; final column = phase
    (PoC / Phase 2 / Phase 3) so the table doubles as a roadmap.
  - 8–10 body rows fit on the 10.83 × 7.5 in content canvas at 10.5pt with rowH ≈ 0.4.
- **Simple chart (数値の可視化)** — when the topic carries quantities/%/trends, prefer a
  real chart over a table: bar/column/line via pptxgenjs `addChart`. House chart style:
  bars in navy `0E2240` / ice-blue `CBD5E8`, the ONE highlighted bar/series in red
  `C00000`; flat 2D only (never 3D, never default Office multi-color theme); Meiryo
  data labels; gridlines `CCCCCC` or none; drop the legend when ≤2 series — label
  directly. Numbers 半角 with comma separators, unit in the axis/header (件, %, 秒).
- **Horizontal timeline (スケジュール)** — a single horizontal line, navy milestone
  markers, labels alternating above/below, current position or deadline flagged in
  `C00000`. Use for phases/roadmap instead of a bullet list of dates.
- **2×2 matrix (優先度マトリクス)** — grey `CCCCCC` axes with 9–10pt labels, items as
  small ice-blue boxes, the recommended quadrant/item emphasized in red text.
