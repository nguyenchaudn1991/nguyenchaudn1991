---
name: premium-design
description: >-
  Audit and refactor websites to premium visual quality that looks handcrafted, 
  not AI-generated. Covers design patterns, typography, color, layout, and 
  component choices. Also includes a Japanese-quality mode (日本品質) drawn from a 
  Japanese client design guideline — apply when the audience/client is Japanese. 
  Triggers on: design audit, avoid AI look, redesign website, premium quality check, 
  does this look generic, component review, Japanese client, 日本品質, khách Nhật.
---

# Premium Design — Avoid AI Vibe

Build websites that **look intentional and handcrafted**, not like they were fed to 
an AI generator and shipped.

> This skill is a **design audit checklist**. Use when reviewing mockups, refactoring 
> existing sites, or building new features. It identifies generic patterns and 
> prescribes specific replacements.
>
> **PageSpeed is not covered here.** That's a separate concern (see mobile-first-performance skill).

---

## When to Use This Skill

✅ Use this when:
- Reviewing a design (Figma mockup, prototype) before implementation
- Refactoring an existing website that feels "generic" or "AI-generated"
- Building a new site or feature and want to avoid obvious AI patterns
- Auditing a finished site ("Does this look like I built it with care?")
- Making component decisions (buttons, cards, modals, etc)

❌ Do NOT use this for:
- Quick MVP/prototype (constraints too strict for speed)
- Data dashboards (different rules apply)
- Internal admin panels (UX priorities are different)
- Blog posts (copy audit, not design audit)

---

## Non-negotiable Rules

1. **No generic "AI" color palette.** Avoid purple-blue gradients, oversaturated accents, pure `#000000` backgrounds. 
   These are the strongest "AI smell" signals.

2. **Typography must have character.** Never ship with browser defaults or Inter/Open Sans everywhere.
   Font choice is the single biggest design signal. Change this first for maximum impact.

3. **Layout hierarchy must feel intentional.** Symmetry + three equal columns is the most common AI pattern.
   Break it with asymmetry, varied card heights, or masonry.

4. **No cliche component patterns.** 3-card carousel with dots, pill badges, hollow "ghost" buttons everywhere, 
   generic modals — these are AI fingerprints.

5. **Avoid generic stock imagery.** Real team photos, candid shots, or consistent illustrations.
   "Diverse team smiling at laptops" is an immediate AI red flag.

6. **No glow / neon / light-emission effects.** Glowing box-shadows around buttons, cards, or borders;
   neon text glow; cursor-following spotlight borders; floating gradient orbs as "ambient light" —
   these are THE signature AI look. Depth comes from tinted neutral shadows and layering,
   never from things that emit light.

7. **Every effect must be cheap.** Premium ≠ heavy. Animate only `transform`/`opacity`,
   keep `backdrop-filter` blur off large surfaces, respect `prefers-reduced-motion`.
   If an effect hurts mobile LCP/INP, cut the effect, not the speed
   (see mobile-first-performance skill for budgets).

---

## Design Audit

### Typography

**Check for these problems and fix them:**

- **Browser default fonts or Inter everywhere.** 
  - For **English:** Replace with `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, `JetBrains Mono` (code)
  - For **Vietnamese:** `Be Vietnam Pro`, `Plus Jakarta Sans` (ensure full Latin Extended support to prevent diacritic clipping)
  - For **Japanese:** `Noto Sans JP`, `Shippori Mincho`, `Zen Kaku Gothic` (increase line-height to 1.6-1.8 for breathing room)

- **Broken Vietnamese or Japanese text.** 
  - VN: Line-height minimum 1.5 (tone marks overlap otherwise)
  - JP: Use `word-break: keep-all` + `overflow-wrap: break-word` to prevent mid-word breaks in Kanji
  - JP: Increase font size slightly (12-14px body, not 13px)

- **Headlines lack presence.** Increase display text size (48px+), tighten `letter-spacing` (negative), reduce line-height to ~1.1. Headlines should feel heavy and intentional.

- **Body text too wide.** Limit paragraph width to ~65 characters (roughly 320-380px). Increase line-height to 1.6.

- **Only Regular (400) and Bold (700) weights used.** Introduce Medium (500) and SemiBold (600) for subtle hierarchy without jumping to bold.

- **Numbers in proportional font.** Enable `font-variant-numeric: tabular-nums` for data-heavy interfaces, or use monospace for financial figures.

- **Missing `letter-spacing` adjustments.** Use negative tracking for large headers (−0.02em to −0.03em), positive tracking for small caps or labels (+0.05em).

- **All-caps subheaders everywhere.** Try lowercase italics, sentence case, or small-caps instead. All-caps is harsh.

- **Orphaned words on last line.** Single words sitting alone. Fix with `text-wrap: balance` or `text-wrap: pretty`.

---

### Color and Surfaces

- **Pure `#000000` background or oversaturated accent colors.** 
  - Replace `#000` with off-black: `#0a0a0a`, `#121212`, or tinted dark navy `#0E1B2E`
  - Keep accent saturation below 80%. Desaturated accents blend better than screaming neons.

- **More than one accent color.** Pick one. Remove the rest. Consistency beats variety.

- **Mixing warm and cool grays.** Stick to one gray family. Tint all grays with a consistent hue (all cool or all warm, not both).

- **Purple/blue "AI gradient" aesthetic.** Most common AI fingerprint. Replace with:
  - Neutral base + single accent color, OR
  - Subtle gradient (radial or mesh, not linear 45°), OR
  - Flat, desaturated color

- **Generic `box-shadow` (pure black at low opacity).** Tint shadows to match background hue:
  - On blue background → use dark blue shadow
  - On warm background → use warm dark shadow
  This adds dimensionality without looking "floaty".

- **Flat design with zero texture.** Add subtle noise, grain, or micro-patterns to backgrounds. Pure flat feels sterile. Use `background-image: url('noise.png')` at low opacity or CSS noise (via SVG or canvas).

- **Perfectly even gradients.** Break uniformity with:
  - Radial gradients instead of linear
  - Noise overlays
  - Mesh gradients (subtle color shifts)

- **Inconsistent lighting direction.** Audit all shadows to suggest a single, consistent light source (e.g., always top-left).

- **Random dark sections in a light mode page.** A sudden dark section breaking an otherwise light page looks like copy-paste. 
  Either commit to full dark mode or keep a consistent background tone throughout. Use slightly darker shades of the same palette, not a sudden jump to `#111`.

- **Empty, flat sections with no visual depth.** Sections that are just text on plain background feel unfinished. Add:
  - High-quality background imagery (blurred, overlaid, or masked)
  - Subtle patterns or ambient gradients
  - Use placeholder images from `https://picsum.photos/seed/{name}/1920/1080` when real assets unavailable

---

### Layout

- **Everything centered and symmetrical.** Break symmetry with:
  - Offset margins
  - Mixed aspect ratios (tall image + short text)
  - Left-aligned headers over centered content

- **Three equal card columns as feature row.** Most generic AI layout ever. Replace with:
  - 2-column zig-zag
  - Asymmetric grid (3-2-1 or 2-3)
  - Horizontal scroll (mobile-friendly)
  - Masonry layout

- **Using `height: 100vh` for full-screen sections.** Replace with `min-height: 100dvh` (prevents iOS Safari viewport bug on mobile).

- **Complex flexbox percentage math.** Use CSS Grid for reliable multi-column structures.

- **No max-width container.** Add container constraint (~1200-1440px) with auto margins so content doesn't stretch edge-to-edge on ultrawide screens.

- **Cards of equal height forced by flexbox.** Allow variable heights, or use masonry when content varies in length.

- **Uniform border-radius on everything.** Vary the radius:
  - Tighter on inner elements (8-12px)
  - Softer on containers (16-24px)

- **No overlap or depth.** Elements sit flat next to each other. Use negative margins to create layering and visual depth.

- **Symmetrical vertical padding.** Top and bottom padding identical. Adjust optically — bottom often needs to be 10-20% larger to feel balanced.

- **Dashboard always left sidebar.** Try top navigation, floating command menu, or collapsible panel instead.

- **Missing whitespace.** Double the spacing. Let the design breathe. Dense layouts work for dashboards, not for marketing.

- **Buttons not bottom-aligned in card groups.** When cards have different content, CTAs end up at random heights. Pin buttons to the bottom so they form a clean line.

- **Feature lists starting at different vertical positions.** In pricing tables or comparison cards, ensure lists start at the same Y position across all columns.

- **Inconsistent vertical rhythm in side-by-side elements.** Align shared elements (titles, descriptions, prices, buttons) across all items. Misaligned baselines look broken.

- **Mathematical alignment that looks optically wrong.** Centering by math doesn't always look centered to the eye. Icons next to text, play buttons in circles, or text in buttons often need 1-2px optical adjustments.

---

### Interactivity and States

- **No hover states on buttons.** Add background shift, scale, or translate. Something must happen.

- **No active/pressed feedback.** Add `scale(0.98)` or `translateY(1px)` on click to simulate physical interaction.

- **Instant transitions with zero duration.** Add smooth transitions (200-300ms easing) to all interactive elements.

- **Missing focus ring.** Ensure visible focus indicators for keyboard navigation (required for accessibility).

- **No loading states.** Replace generic spinners with skeleton loaders that match the actual layout shape.

- **No empty states.** An empty dashboard is a missed opportunity. Design a "getting started" or "no results" view.

- **No error states.** Add clear, inline error messages for forms. Never use `window.alert()`.

- **Dead links.** Buttons linking to `#`. Either link to real destinations or visually disable them.

- **No indication of current page in navigation.** Style the active nav link differently so users know where they are.

- **Scroll jumping.** Anchor clicks jump instantly. Add `scroll-behavior: smooth`.

- **Animations using `top`, `left`, `width`, `height`.** Switch to `transform` and `opacity` for GPU-accelerated, smooth animations.

---

### Effects — the AI-era blacklist

These effects appear on nearly every AI-generated site of 2024–2026. Finding ANY of them
is an instant "AI made this" tell — remove on sight:

- **Floating gradient orbs / blurred blobs** drifting in the hero background
- **Glow borders / spotlight cards** — borders or shadows that emit colored light (static or cursor-following)
- **Animated gradient text** — shimmer or hue-cycling on headlines
- **Typewriter / typing-cursor effect** on hero headlines
- **Particle / starfield / matrix backgrounds**
- **3D tilt on every card** (`transform: rotateX/rotateY` chasing the cursor)
- **Cursor trails or custom blob cursors**
- **Dot-grid background + radial glow** combo (the default "AI SaaS" hero)

**What premium actually looks like:** one considered font, disciplined spacing, tinted
neutral shadows, hairline borders, restrained 200–300ms motion on interaction — and
nothing that moves without a reason.

**Effects budget (speed is part of premium):**
- Max 1–2 "expensive" effects per page (glassmorphism nav OR grain overlay — not everything at once)
- `backdrop-filter` only on small surfaces; never full-viewport
- Scroll-driven animation via `IntersectionObserver` / CSS scroll-driven animations — no scroll-jacking, no heavy JS animation lib for what CSS can do
- Always implement `prefers-reduced-motion: reduce` — disable decorative motion entirely

---

### Content

- **Generic placeholder names.** 
  - VN: Use realistic, region-contextual names ("Trần Hoàng Nam", not "Nguyễn Văn A" which is too generic)
  - JP: Use natural names ("佐藤 健太", not "山田太郎" which is overused)
  - Avoid: "John Doe", "Jane Smith", "Alice", "Bob"

- **Cultural context for design tone:**
  - **Japan:** Push for "Zen" aesthetic (abundant whitespace, minimalistic balance) rather than dense info-heavy style
  - **Vietnam:** Prefer clear, concise, trustworthy copy + social proof (testimonials, numbers, team)

- **Fake round numbers.** Use organic, messy data: `47.2%`, `$99.00`, `+1 (312) 847-1928` (not `50%`, `$100.00`).

- **Placeholder company names.** Invent contextual, believable brand names. Never "Acme Corp", "Nexus", "SmartFlow".

- **AI copywriting clichés.** Never use: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Tapestry", "In the world of...", "Powerful".

- **Exclamation marks in success messages.** Remove them. Be confident, not loud.

- **"Oops!" error messages.** Be direct: "Connection failed. Try again." or "We couldn't save your changes."

- **Passive voice.** Use active: "We couldn't save your changes" not "Mistakes were made."

- **All blog post dates identical.** Randomize dates to appear real.

- **Same avatar image for multiple users.** Use unique assets for every distinct person.

- **Lorem Ipsum.** Never use placeholder Latin text. Write real draft copy.

- **Title Case On Every Header.** Use sentence case instead: "Getting started with your account", not "Getting Started With Your Account".

---

### Component Patterns

- **Generic card look (border + shadow + white background).** Remove the border, or use only background color, or use only spacing. 
  Cards should exist only when elevation communicates hierarchy.

- **Always one filled button + one ghost button.** Add text links or tertiary styles to reduce visual noise.

- **Pill-shaped "New" and "Beta" badges.** Try square badges, flags, corner ribbons, or plain text labels.

- **Accordion FAQ sections.** Use a side-by-side list, searchable help, or inline progressive disclosure.

- **3-card carousel testimonials with dots.** Replace with:
  - Masonry wall of quotes
  - Embedded social posts
  - Single rotating quote with pagination
  - Simple list (no rotation)

- **Pricing table with 3 identical towers.** Highlight the recommended tier with color and emphasis, not just extra height.

- **Modals for everything.** Use inline editing, slide-over panels, or expandable sections instead of popups for simple actions.

- **Avatar circles exclusively.** Try squircles or rounded squares (border-radius: 4-8px) for a less generic look.

- **Light/dark toggle always sun/moon switch.** Use a dropdown, system preference detection, or integrate into settings menu.

- **Footer link farm with 4 columns.** Simplify. Focus on main navigational paths and legally required links only.

---

### Iconography

- **Lucide or Feather icons exclusively.** These are the "default" AI icon choice. Use instead:
  - Phosphor (modern, 6 weights)
  - Heroicons (clean, Tailwind-friendly)
  - Custom SVG icon set (strongest signal of care)
  
  **Exception:** If the project already uses Lucide/Feather throughout, prioritize consistency over replacement. Only apply this rule to new projects or when doing a full design overhaul. Partial replacement mid-project creates more inconsistency than the original problem.

- **Cliche metaphors.** Replace:
  - Rocketship for "Launch" → use spark, bolt, arrow
  - Shield for "Security" → use fingerprint, vault, lock
  - Magnifying glass for "Search" → use binoculars, finder

- **Inconsistent stroke widths.** Audit all icons and standardize to one stroke weight (1.5px, 2px, etc).

- **Missing favicon.** Always include a branded favicon (don't use default).

- **Stock "diverse team" photos.** Use real team photos, candid shots, or consistent illustration style instead.

---

### Code Quality

- **Div soup.** Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.

- **Inline styles mixed with CSS classes.** Move all styling to the project's styling system.

- **Hardcoded pixel widths.** Use relative units (`%`, `rem`, `em`, `max-width`) for flexible layouts.

- **Missing alt text on images.** Describe image content for screen readers. Never leave `alt=""` or `alt="image"` on meaningful images.

- **Arbitrary z-index values like `9999`.** Establish a clean z-index scale in the theme/variables.

- **Commented-out dead code.** Remove all debug artifacts before shipping.

- **Import hallucinations.** Verify every import actually exists in `package.json` or project dependencies.

- **Missing meta tags.** Add proper `<title>`, `description`, `og:image`, and social sharing meta tags.

---

### Strategic Omissions (What Gets Forgotten)

- **No legal links.** Add privacy policy and terms of service links in footer.

- **No "back" navigation.** Every page needs a way to return (back button, home link, breadcrumbs).

- **No custom 404 page.** Design a helpful, branded "page not found" experience.

- **No form validation.** Add client-side validation for emails, required fields, format checks.

- **No "skip to content" link.** Essential for keyboard users. Add a hidden skip-link in the HTML.

- **No cookie consent.** If required by jurisdiction, add a compliant consent banner.

---

## Japanese Quality Mode (日本品質)

**Khi audience / khách hàng là Nhật → bật mode này** (layer thêm, không thay thế audit trên).
Đọc và áp `references/japanese-quality.md` — kỷ luật thiết kế Nhật rút từ design guideline chuẩn
của khách (ニューロマジック). Với khách Nhật, **độ chỉn chu = độ tin cậy (信頼)**: lệch vài px / kẻ
bảng mất / heading sai cấp weight đều bị xem là "làm ẩu, không đáng tin".

Ưu tiên flag thêm (chi tiết trong reference):
- **Weight hierarchy kỷ luật:** heading bold ↔ body regular rõ; không bold loạn / mảnh loạn.
- **Spacing có nghĩa:** gap block↔block **phải lớn hơn** gap heading↔body; canh lề đối xứng, nhất quán.
- **Màu tiết chế:** 1 màu = 1 nghĩa; contrast nền/chữ ưu tiên cao nhất.
- **AI-smell (Nhật cực ghét):** gạch chân dưới tiêu đề · stripe màu cạnh card · gradient/shadow tràn lan · emoji làm icon.
- **Icon nhất quán:** 1 bộ, cùng stroke, nghĩa cố định.
- **Bảng & số:** kẻ bảng hiện rõ & đều · số canh phải (`tabular-nums`) · đơn vị trong ngoặc ở header.

Lưu ý phạm vi: skill này dành **web/marketing** → giữ định hướng "Zen, nhiều whitespace" cho landing.
Nếu là **code FE của sản phẩm dashboard** có design system riêng (token màu/font cụ thể) → đó là việc
của skill `meo-frontend-check`, không phải skill này.

---

## Design Techniques (High-Impact Patterns)

When designing, pull from these to avoid generic layouts:

### Typography Enhancement
- **Variable font animation.** Interpolate weight or width on scroll or hover
- **Outlined-to-fill transitions.** Text starts as stroke, fills with color on scroll entry
- **Text mask reveals.** Large typography acts as window to video/imagery behind it

### Layout Enhancement
- **Broken grid / asymmetry.** Elements deliberately ignore column structure — overlap, bleed off-screen, offset with randomness
- **Whitespace maximization.** Aggressive negative space to force focus on single element
- **Parallax card stacks.** Sections stick and physically stack over scroll
- **Split-screen scroll.** Two halves of screen slide in opposite directions

### Motion Enhancement
- **Smooth scroll with inertia.** Decouple scrolling from browser defaults for cinematic feel
- **Staggered entry.** Elements cascade in with slight delays (Y-axis translation + opacity fade)
- **Spring physics.** Replace linear easing with spring-based motion on interactive elements
- **Scroll-driven reveals.** Content enters through expanding masks, wipes, or SVG draws tied to scroll progress

### Surface Enhancement
- **True glassmorphism.** Go beyond `backdrop-filter: blur` — add 1px inner border + subtle inner shadow. Keep the blurred surface SMALL (nav bar, small card) — full-screen blur kills mobile performance
- **Hairline material edges.** 1px inner top border in low-opacity white/light to suggest a physical edge under consistent top lighting — reads premium without emitting light (never a glow border)
- **Grain and noise overlays.** Fixed pointer-events-none overlay with subtle noise to break digital flatness
- **Colored, tinted shadows.** Shadows carry hue of background rather than generic black

---

## Fix Priority

Apply changes in this order for maximum visual impact with minimum risk:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliche patterns for modern alternatives
6. **Add loading, empty, error states** — makes it feel finished
7. **Polish typography scale and spacing** — premium final touch

---

## How to Verify It Works

After applying this skill, check against these checklists:

### ✅ Visual Checklist (Subjective)

- [ ] Does this look like it took manual care? (Not "I fed it to Claude and shipped it")
- [ ] No 3-column card farm, purple-blue gradient, or Lucide icons everywhere?
- [ ] No glow/neon anywhere? (glow shadows, spotlight borders, gradient orbs, shimmer text, particles)
- [ ] `prefers-reduced-motion` respected? Expensive effects ≤ 1–2 per page?
- [ ] No AI-generic copy ("Elevate", "Seamless", "Unleash")?
- [ ] Japanese or Vietnamese text renders correctly? (Tone marks, Kanji line-breaks clean?)
- [ ] Typography feels intentional? (Not browser defaults or Inter)
- [ ] Color palette feels considered? (Not oversaturated, not random accents)
- [ ] Hover states exist? Buttons respond to interaction?
- [ ] Whitespace feels generous? Not cramped?

### ✅ Technical Checklist

- [ ] Semantic HTML (no div soup)?
- [ ] All imports exist in `package.json`?
- [ ] No inline styles mixed with classes?
- [ ] All images have `alt` text?
- [ ] Focus rings visible for keyboard nav?
- [ ] No console errors or warnings?

### ✅ Content Checklist

- [ ] No Lorem Ipsum or placeholder text?
- [ ] All names are realistic and contextual (VN/JP appropriate)?
- [ ] All avatar images unique (no duplicates)?
- [ ] Error, loading, and empty states designed?
- [ ] Legal links present (privacy, terms)?

---

## Rules

- Work with the existing tech stack. Do not suggest framework migrations.
- Do not break existing functionality. Test after every change.
- Before importing any new library, check `package.json` first.
- Keep changes reviewable and focused. Small targeted improvements over big rewrites.
- If unsure about a design choice, ask "Would a real designer do this?" before shipping.

---

## Field Notes — lessons from real client projects

> Verified on production work (topdoanhnghiep.com, 06/2026). Each item cost a real
> bug or client complaint — read before repeating them.

### Typography (Vietnamese)

- **Verify diacritics with a screenshot, not assumptions.** Playfair Display ships a
  Vietnamese subset but renders stacked tone marks broken ("xuống tiền" → "xuô´ng tiê`n").
  For VN serif headlines use **Lora**. Always screenshot a heavy-diacritic phrase
  (e.g. "xuống tiền", "thẩm định") before approving any font.
- **The fallback font must also support Vietnamese.** With `font-display: swap`, users
  on slow connections see the fallback first. Georgia breaks VN tone marks → fallback
  serif must be `"Times New Roman", serif`. A broken half-second flash is still broken.

### Color and Surfaces

- **No accent-colored glow shadows on dark backgrounds.** A red/purple/blue
  `box-shadow` under a button on a navy/dark section reads as "neon AI vibe" —
  a real client spotted and rejected it. On dark surfaces use a darker neutral
  shadow of the background hue, or none.
- **Brand accents need a dark variant for white backgrounds.** Decorative gold
  #C9A227 fails WCAG AA on white (~2.3:1). Keep two tokens: `--gold` (dark, ≥4.5:1,
  for text on light) and `--gold-bright` (only on navy/dark). Same rule applies to
  any saturated brand accent used as text.

### Hero background images (clients ALWAYS ask about these)

- **Design the overlay as a gradient with a protected text zone**, e.g. 80% opacity
  over the text side thinning to 20% on the open side — not one flat opacity.
  Add a subtle `text-shadow` as a safety net so later overlay reductions don't
  immediately break readability.
- **Expect the client to ask 2–3 times to "show the photo more".** Concede in steps,
  and hold a hard floor around 70% over the text zone (WCAG contrast). Past that,
  the correct lever is a **brighter image**, not a thinner overlay — offer a new
  image prompt instead of another opacity cut.
- **Write image-gen prompts around the layout, not the subject.** If a card/list
  overlays the right side and text covers the left, a "beautiful reception desk on
  the right" will be hidden. Prompt for ambient composition, no single focal object,
  detail concentrated in the zone the UI leaves open (usually the top third).

### Working with non-technical clients

- Drop-in asset folder with a README: fixed filenames (`hero.webp`, `hero_sp.webp`),
  exact sizes, compression instructions (squoosh.app, quality ~80). "Replace the file,
  same name, done" beats any CMS for one-off brand assets.
- Placeholder strategy: a branded monogram tile (brand gradient + initial letter)
  looks intentional while waiting for real photos; random stock/picsum photos look
  like a mistake and can be contextually wrong.
