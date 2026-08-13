---
name: meo-pptx
description: >-
  Build or edit MEO client-meeting PowerPoint decks (.pptx) in Chau's house style for
  Japanese customers — 技術検討会 (business + technical explanation, comparison tables,
  現状/改善フロー) and 課題検討会 / 進捗報告. Locks Meiryo, a custom 10.83 × 7.5 in
  content canvas, navy #0E2240, ice-blue cards, red #C00000, Japanese output. Only
  when the deliverable is a .pptx file.
  Do NOT use for standalone diagrams, non-MEO slides, or web design.
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion, Skill
---

# MEO PPTX — Chau's house style

Build customer-facing PowerPoint decks for MEO client meetings that look like Chau's
own work, **not** generic AI output. This skill **layers a locked visual identity and
two slide modes on top of the standard pptx file-creation machinery**.

> Use the base PPTX tooling (pptxgenjs to create from scratch, or the office
> unpack/pack scripts to edit a template) for the mechanics. This skill defines
> **how the result must look and what it must contain**.

---
## Routing

| Task | File to load |
|---|---|
| Every deck (always) | This file — §0 hard rules, §1 visual identity, §2 skeleton, §3a visual-choice table |
| Drawing any diagram / table / chart on a content slide | + [references/diagrams.md](references/diagrams.md) |
| Progress report / 課題検討会 deck | + [references/report-mode.md](references/report-mode.md) |

Do not load a file you do not need.


## 0. Non-negotiable rules (read first)

1. **Output language = Japanese.** All on-slide text is Japanese. Section/flow labels
   use the house wording (現状フロー / 改善フロー / 課題 / 改善案 / 効果 …).
2. **NEVER fabricate progress, backlog, or status numbers.** In Report mode the user
   verifies all progress data by hand. This skill only builds **topic / agenda /
   explanation** slides. If a data/progress table is needed, insert a clearly marked
   placeholder slide (see §4 Report mode) and tell the user to fill it manually —
   do not invent figures, completion %, ticket counts, or dates.
3. **Lock the visual identity below.** Do not substitute default Office colors
   (4472C4 etc.), Calibri/Arial, or 16:9. Those are the "AI smell" to avoid.
4. **Never put an accent line under a title.** Use whitespace or a navy background
   band instead.
5. **NEVER put a colored accent bar/stripe on the side of a card** (a thin/thick
   vertical colored line on the left or right edge of a box). This is the single
   strongest "AI smell" — do not do it under any circumstance. See §1a for what to
   do instead.
6. **Slide economy — content-first (default).** The customer values **content + 可視化
   (flow/table)**, not chrome. Do NOT spend slides on section dividers, and do NOT emit
   any slide that carries no content or visual. A real MTG file has 4–5 topics; target
   roughly **(topics + 1) slides**, not (topics × 3). See §2. Only add divider/agenda
   chrome when the user explicitly asks for it.
7. **Reserve header/footer zones — the user overlays their own.** Chau's base pptx adds
   a top header (red rule line) and a bottom navy footer band (name + page number).
   Skill content must stay inside the **safe area** (§1b) and must **NOT draw its own
   footer / page number** — the template already supplies them (avoids double page numbers).
8. **Japanese must read native, not machine-translated.** On-slide text uses concise
   体言止め style (「処理時間を50%削減」, NOT 「処理時間を50%削減することができます」).
   Full です・ます sentences only in notes/annotations — and keep the register consistent.
   半角 for digits/Latin, 全角 punctuation (、。・) for Japanese. No redundant polite
   chains (〜させていただきます as connective), no direct-translation phrasing. A native
   reader skimming the deck must find nothing "off".

---

## 1. Locked visual identity

**Content canvas:** custom `MEO_CONTENT` layout, **10.83 × 7.5 in**
(`9906000 × 6858000 EMU`, landscape). This is intentionally the usable content canvas,
not ISO A4: the user copies/pastes the generated content into an A4 customer template that
already owns the header and footer. **Preserve these dimensions; do not normalize to A4.**
Dense, readable, print-friendly agenda style — not sparse marketing slides.

**Font:** **Meiryo** (メイリオ) for everything. Latin fallback: Arial. Never Calibri.

**Color palette (hex):**

| Role | Hex | Use |
|------|-----|-----|
| Primary navy (dominant) | `0E2240` | Title slides, section header bands, dark text |
| Navy variants | `1A1F2B`, `1E293B`, `1E2761` | Secondary dark surfaces / deep text |
| Ice-blue card (light) | `D5DAE4` | Main content card / box fill |
| Ice-blue light | `CBD5E8`, `EEF1F6`, `CADCFC`, `E2E8F0` | Alt cards, table header fills, soft panels |
| **Red accent** | `C00000` | Emphasis, key takeaways, warnings, important flags (use sparingly but deliberately) |
| Soft coral | `FF6B6B` | Lighter emphasis / callout (esp. accent text on navy) |
| Success green | `27AE60`, `00B050`, `D4EDBC` | Positive status, "改善後 / 効果" gains, ✓ |
| Neutral grey | `595959` | Captions, muted body |
| Table border / divider | `CCCCCC` | Table gridlines, thin separators |
| Surface | `FFFFFF` / `F2F2F2` | Slide / panel background |
| Text on navy | `FFFFFF` | |

**Dominance rule:** navy + ice-blue carry ~70% of the visual weight; red `C00000` is the
single sharp accent; green only for positive/after states. Never give all colors equal weight.

### 1a. Card styling — avoid the AI look

Cards/boxes are where AI decks give themselves away. **Banned vs allowed:**

| ❌ Banned (AI smell) | ✅ Use instead |
|------|------|
| Thin/thick **colored vertical bar on the left or right edge** of a card | Flat single-fill card (ice-blue `D5DAE4`), OR a **full-width navy header band on TOP** of the card with white title, body below |
| Colored accent **line under the title** | Whitespace, or the navy top band |
| Card with a coloured 1-side border only | Either a full even border in `CCCCCC`, or no border + fill only |
| Drop shadows / glow / rounded "floating" cards everywhere | Flat rectangles, square or lightly rounded corners, consistent across the deck |
| Gradient fills | Solid fills only |
| Emoji as section icons | No emoji; use the number (01/02) or plain text label |

**Card recipe (default):** rectangle, solid `D5DAE4` fill, optional even `CCCCCC`
1px border, navy `0E2240` text, internal padding ≥ 0.2". To label a card, put a
**navy band across the top** (full width of the card) with white text — never a
side stripe. Emphasis inside a card = make the key word `C00000`, not a colored edge.

**Typography sizes (custom content canvas):**

| Element | Size |
|---------|------|
| Cover topic number / big number | 60–72pt bold, navy or white-on-navy |
| Slide title | 28–34pt bold |
| In-slide section kicker (01 機能概要) | 12–14pt bold, red `C00000` on light bg |
| Section header inside slide | 18–22pt bold |
| Body / table | 11–14pt |
| Caption / source (出典) | 9–10pt grey `595959` |

### 1b. Safe content area — reserve the user's header & footer

The customer's template overlays a **top header (red rule line)** and a **bottom navy
footer band (identity + page number)**, added by the user afterward. All generated
content must avoid those zones.

On the custom MEO content canvas (10.83 × 7.5 in):

| Zone | Range (in) | Owner |
|------|-----------|-------|
| Header reserve (red rule) | y 0 – 0.55 | user — leave empty |
| **Safe content band** | **y 0.65 – 6.85, x 0.60 – 10.23 (w ≈ 9.63)** | skill |
| Footer reserve (navy band) | y 6.95 – 7.5 | user — leave empty |

Rules:
- Place kicker / title / cards / tables **only inside the safe band**; nothing may enter
  the top 0.55" or bottom 0.55".
- **Do not draw a skill footer** (doc name / page number) — the user's band supplies it.
  No `pageNo` counter, no `n / total`.
- Balance content **vertically within the safe band** (roughly centered), and keep
  **equal left/right margins** so it reads centered, not pushed to one edge.
- Cover/closing (full-navy) slides are exempt from the reserves only if the user is NOT
  overlaying header/footer on them — when unsure, keep the same safe band.

---

## 2. Deck skeleton — lean / content-first (default)

Chrome slides (cover, agenda, divider) are cost, not value. Spend slides on **content
and 可視化**, nothing else.

**Default skeleton:**

1. **Cover (1 slide)** — navy `0E2240` background, white title, date `YYYYMMDD`, meeting
   name. **Fold the agenda into the lower half of this slide** (list the 4–5 topics,
   numbered) — do NOT make a separate agenda slide.
2. **Content slides — the body.** Rule: **1 topic = 1 slide** (max 2 only if genuinely
   dense). Each topic's number/label lives in the **in-slide kicker** at top-left
   (e.g. `01　機能概要`) — this *replaces* the divider slide entirely.
3. **(Optional) まとめ・次のアクション** — only when there are real action items; otherwise drop it.

**Rules:**

- **No standalone section-divider slides by default.** The kicker line on each content
  slide is the section marker. (A 4-topic deck = cover + 4 content [+ optional matome]
  ≈ 5–6 slides, not 13.)
- **No separate agenda slide** — it goes on the cover. Only break it out if the user asks.
- **Never emit an empty/structural slide** that has no content, table, or flow.
- **Opt-in chrome:** add divider slides / a full agenda slide ONLY when the user
  explicitly asks for a formal presentation feel, or the deck is a single large topic
  that needs internal chapters.

---

## 3. Technical mode (技術検討会)

Goal: explain a topic so the customer understands both **business value and technical
detail**. Claude may write the full **explanation** here — how something works, why it
matters, what the trade-offs are. That freedom covers *prose and structure*, **not facts**:
API names, endpoints, payload fields, timings, versions, severity levels and component names
must come from the source or be marked 「要確認」. Explanatory ≠ inventable.

### 3a. Visualization decision table — choose BEFORE writing the slide

Default posture: **if the content can be visualized inside the safe area, visualize it.**
Plain text is the last resort, never the default. Map content type → visual:

| Content type | Visual to use |
|---|---|
| Process / sequence of steps | 現状フロー→改善フロー, or numbered step boxes |
| A vs B / option comparison | comparison table (✅/❌, ◯/✕) |
| Quantities, %, trends over time | **chart** (bar / line — see pattern below) |
| Schedule / milestones / phases | horizontal timeline |
| Priority / positioning of items | 2×2 matrix |
| System structure / integration / architecture | **sequence-style architecture diagram (処理シーケンス図)** — see §3b; a plain box-and-arrow row is below the density bar |
| Who can do what / feature-role scope | **use case diagram (ユースケース図)** — see §3b |
| User operations / screen flow with a decision | **user flow diagram (ユーザーフロー図)** with branch diamond — see §3b |
| Cross-role process (customer / BrSE / dev…) | **swimlane diagram (スイムレーン図)** — see §3b |
| Feature / requirement / task inventory | **categorized table (カテゴリ分類表)** with rowspan category column — see §3b |
| Metric改善 (before → after) | before/after effect table |

**Density bar (Chau's expectation):** the customer reads content slides like pages of a
設計書, so lean toward **density, not slide count** — a real MTG has many topics, never
7-8 slides per topic. A rich diagram typically carries ~6+ numbered steps/nodes with
concrete labels (API名・payload項目・所要時間・重大度…) and a supporting data strip.

> ⚠️ **Density comes from the source, never from a quota.** The numbers above describe what
> a well-sourced slide usually looks like — they are **not** a minimum to hit.
>
> - A 3-node diagram is correct **if the real system has 3 nodes.** Do not invent steps to
>   look thorough.
> - **Never invent** API names, payload fields, timings, severity levels, or component names.
>   §3 lets the agent write the *explanation*; it does not license inventing *facts*. A wrong
>   API name in a customer deck is worse than a sparse slide.
> - Data not in the source → either leave it out, or label it 「要確認」 and tell the user.
> - Genuinely dense topic that breaks the minimum font/spacing in §1 → **split to a second
>   slide.** Readability outranks the 1-topic-1-slide guideline.
>
> Sparse slide with real content beats dense slide with invented content. Every time.

### 3b. Slide patterns → `references/diagrams.md`

Every content slide uses at least one house pattern. Pick the pattern from the §3a table,
then **load [references/diagrams.md](references/diagrams.md) and follow its build spec
exactly** — palette, node counts, connector rules and label content are specified there.

Patterns available: comparison table · 現状/改善フロー · before/after effect table ·
numbered steps · 処理シーケンス図 · ユースケース図 · ユーザーフロー図 · スイムレーン図 ·
カテゴリ分類表 · chart · timeline · 2×2 matrix.

Pack one topic onto one slide: lead with the flow/table/chart (可視化), add a short
takeaway band at the bottom. No plain title + bullets — every slide carries a visual.

Ngoại lệ duy nhất: khi **bảng hoặc text có cấu trúc là cách biểu diễn trung thực và dễ đọc
nhất** cho nội dung đó (danh sách điều kiện, định nghĩa, điều khoản). Bảng vẫn tính là 可視化.
Không được vẽ diagram trang trí chỉ để "có visual".

---

## 4. Report mode (進捗報告・課題検討会) → `references/report-mode.md`

Agenda + important-topic slides for a progress meeting. **Progress/backlog data is verified
and entered by the user — this skill does NOT generate it** (§0.2).

Building a report deck → **load [references/report-mode.md](references/report-mode.md)** for
what the agent may build and the placeholder-slide protocol for any progress/status table.

---

## 5. Build & QA workflow

1. **Create:** use pptxgenjs (from scratch) or unpack/pack an existing deck as template.
   Define `MEO_CONTENT` at 10.83 × 7.5 in; do not switch to ISO A4. Set every text run's
   font to Meiryo; apply the §1 palette explicitly (don't rely on theme defaults).
2. **Content QA:** extract text (`python -m markitdown out.pptx`) and confirm Japanese
   renders, no leftover placeholder like `xxx`/`lorem` (except the intentional
   `［要手動入力］` markers), correct order.
3. **Visual QA:** render to images and check for overflow, low contrast (navy text on
   navy, light-on-light), misaligned flow boxes, arrows not connecting, title wrap
   (long titles overlapping the kicker), and **that nothing intrudes into the header
   (top 0.55") or footer (bottom 0.55") reserves**. Fix → re-verify at least once.
4. **Self-check against the "AI smell" list:** no Calibri, no default Office blue, no
   16:9, no under-title accent lines, **no colored side-bar/stripe on any card**,
   no gradients/shadows/emoji-icons, no fabricated numbers, **no divider/agenda chrome
   slides unless asked**.

---

## 6. Quick checklist before delivering

- [ ] Custom `MEO_CONTENT` canvas 10.83 × 7.5 in, Meiryo throughout; not normalized to ISO A4
- [ ] Lean skeleton: cover(+agenda folded in) + ~1 slide/topic; **no divider slides** unless asked
- [ ] Navy `0E2240` cover; ice-blue content cards; red `C00000` used only for emphasis
- [ ] Japanese text, house labels (現状フロー/改善フロー/課題/改善案/効果)
- [ ] Technical: comparison tables + vertical ↓ flows + before/after effect tables
- [ ] Architecture/integration topics use the sequence-style diagram (①〜⑧ numbered steps + 技術ポイント strip); density bar met (≥6 steps/nodes, concrete data in labels)
- [ ] Right diagram type chosen per §3a: ユースケース図（役割）／ユーザーフロー図（操作・分岐）／スイムレーン図（部門横断）／カテゴリ分類表（一覧）; connector lines never cross node shapes
- [ ] Visualization decision table applied — numbers→chart, schedule→timeline, steps→flow; charts in house palette (flat 2D, one red highlight, no Office theme colors)
- [ ] Japanese reads native: 体言止め on slides, consistent register, 半角 digits — no translation smell
- [ ] Report: NO invented progress data; placeholders + manual-input reminders instead
- [ ] Cards: flat fill or navy top-band only — **NO colored side bar/stripe**, no gradient/shadow
- [ ] Every slide has content + a visual element; no plain title+bullets; no under-title lines; no empty chrome slides
- [ ] Header/footer reserves respected: content within y 0.65–6.85; **no skill-drawn footer/page number** (user overlays their own)
- [ ] Visual QA pass done (overflow / contrast / alignment / title-wrap)
