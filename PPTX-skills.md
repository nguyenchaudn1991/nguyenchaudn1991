---
name: meo-pptx
description: >-
  Create MEO client-meeting PowerPoint decks (.pptx) in Chau's house style for
  Japanese customers. Use whenever the user asks to build, draft, or update a
  customer-facing PPTX for MEO meetings — especially (1) "Technical" decks that
  explain business + technical topics with comparison tables and current-vs-improved
  flow diagrams, or (2) "Report" decks (progress / 課題検討会 agenda). Locks a fixed
  visual identity: Meiryo font, A4 size, navy #0E2240, ice-blue cards, red #C00000
  accent, Japanese output. Triggers on: MEO pptx, 技術検討会, 課題検討会, 進捗報告,
  agenda slide, flow comparison slide, 現状フロー/改善フロー, client deck in Japanese.
---

# MEO PPTX — Chau's house style

Build customer-facing PowerPoint decks for MEO client meetings that look like Chau's
own work, **not** generic AI output. This skill **layers a locked visual identity and
two slide modes on top of the standard pptx file-creation machinery**.

> Use the base PPTX tooling (pptxgenjs to create from scratch, or the office
> unpack/pack scripts to edit a template) for the mechanics. This skill defines
> **how the result must look and what it must contain**.

---

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

---

## 1. Locked visual identity

**Slide size:** A4 (`type="A4"`, 9906000 × 6858000 EMU, landscape). Dense, readable,
print-friendly agenda style — not sparse marketing slides.

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

**Typography sizes (A4):**

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

On the A4 layout (10.83 × 7.5 in):

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
detail**. Claude may generate the full content here (it's explanatory, not verified data).

Reusable slide patterns (every content slide uses at least one):

- **Comparison table** — e.g. GPT-5 mini vs GPT-4.1 mini. Ice-blue (`CBD5E8`) header row,
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

Pack one topic onto one slide: lead with the flow/table (可視化), add a short takeaway
band at the bottom. No plain title + bullets — every slide carries a visual.

---

## 4. Report mode (進捗報告・課題検討会)

Goal: agenda + important-topic slides for a progress meeting. **Progress/backlog data is
verified and entered by the user — this skill does NOT generate it.**

Allowed (Claude builds these), following the lean skeleton in §2:
- Cover (with agenda folded in).
- **重要トピック / 課題** explanation slides (same patterns as Technical mode — tables,
  flows, before/after) for qualitative topics that don't depend on unverified numbers.
- まとめ / 次のアクション.

For any progress/backlog/status table, insert a **placeholder slide**:
- Title + correctly formatted empty table (columns like 項目 | ステータス | 進捗 | 備考,
  `CCCCCC` borders, ice-blue header).
- Fill cells with a visible marker: `［要手動入力：verify済みデータ］`.
- Add a speaker-note / on-screen reminder: 「※進捗・課題の数値は手動で確認・入力すること」.
- **Never** auto-fill completion %, ticket counts, dates, or status flags.

When unsure whether data is "verified" → treat it as unverified and leave a placeholder.

---

## 5. Build & QA workflow

1. **Create:** use pptxgenjs (from scratch) or unpack/pack an existing deck as template.
   Set `defineLayout` / slide size to A4; set every text run's font to Meiryo; apply the
   §1 palette explicitly (don't rely on theme defaults).
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

- [ ] A4 landscape, Meiryo throughout
- [ ] Lean skeleton: cover(+agenda folded in) + ~1 slide/topic; **no divider slides** unless asked
- [ ] Navy `0E2240` cover; ice-blue content cards; red `C00000` used only for emphasis
- [ ] Japanese text, house labels (現状フロー/改善フロー/課題/改善案/効果)
- [ ] Technical: comparison tables + vertical ↓ flows + before/after effect tables
- [ ] Report: NO invented progress data; placeholders + manual-input reminders instead
- [ ] Cards: flat fill or navy top-band only — **NO colored side bar/stripe**, no gradient/shadow
- [ ] Every slide has content + a visual element; no plain title+bullets; no under-title lines; no empty chrome slides
- [ ] Header/footer reserves respected: content within y 0.65–6.85; **no skill-drawn footer/page number** (user overlays their own)
- [ ] Visual QA pass done (overflow / contrast / alignment / title-wrap)
