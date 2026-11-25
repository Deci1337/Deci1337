# Design System: Deci1337 GitHub Profile
**Project ID:** github.com/Deci1337/Deci1337 (no Stitch project; tokens live in `scripts/tokens.py`)

## 1. Visual Theme & Atmosphere
Quiet, dense and deliberate. The profile reads like a well-set technical document with a wine-cellar palette: deep near-black red surfaces, one warm metallic accent, generous margins. No emoji, no badges walls, no neon. Every visual is a vector asset generated from one script, so spacing, color and type stay consistent across the whole page.

Motion is ambient and slow: things *draw in* or *travel*, they never blink, bounce or sparkle. One animated motif (the agent graph in the header) carries the identity; everything else is still or animates once.

## 2. Color Palette & Roles

### Dark theme (default reading)
| Name | Hex | Role |
|---|---|---|
| Cellar Black | `#140809` | Asset background behind all cards |
| Oxblood Surface | `#1B0B0E` | Card and tile fill |
| Dried Rose Line | `#3B1A20` | 1px borders, rules, inactive edges |
| Deep Wine | `#6E1423` | Secondary fills, heatmap mid level |
| Bordeaux | `#8E2433` | Node strokes, chips, emphasis strokes |
| Champagne | `#C9A27E` | The only accent: section numbers, tags, signals, highest activity |
| Linen Text | `#F3E7E2` | Titles and primary text |
| Faded Mauve | `#A68E89` | Body text, descriptions |
| Ash Rose | `#6E5854` | Tertiary labels, legends |

### Light theme
| Name | Hex | Role |
|---|---|---|
| Paper | `#F6F0EC` | Asset background |
| Warm White | `#FBF7F4` | Card fill |
| Blush Line | `#E4D3CD` | Borders and rules |
| Claret | `#7A1626` | Primary accent stroke in light mode |
| Garnet | `#9A2A3A` | Chips, node strokes |
| Old Brass | `#9C7450` | Accent (champagne darkened for contrast on paper) |
| Ink | `#2A0F14` | Titles |
| Smoke Mauve | `#76605C` | Body text |
| Dust | `#B49F99` | Tertiary labels |

Rule: maximum two accent colors on any asset (wine family + champagne/brass). Activity heatmap is the only place with a 5-step scale, and it stays inside the same family.

## 3. Typography Rules
* **Display / UI:** Inter Tight (OFL). Titles 600, body 400, tags 500.
* **Technical labels:** JetBrains Mono (OFL), sentence case, near-zero tracking. Used for section numbers, tags, dates, stack monograms. No uppercase tracked labels.
* **All text inside SVG is converted to outlines** at build time (`scripts/svgtext.py`). GitHub serves SVG through `<img>`, which blocks webfonts; outlines guarantee identical rendering on Windows, macOS, Linux and mobile.
* Scale (px in the 840-wide canvas): 68 name · 22 card title · 18 lead · 14–15 body · 11–13 mono labels.
* Tight negative tracking on large display text (−1.5px at 68px), none on body.
* Prose that matters for search and mobile reading (About) stays real Markdown text, not SVG.

## 4. Component Stylings
* **Header:** 840×280 card, gently rounded corners (20px), 1px line border, no glow. Name block on the left, agent graph (orchestrator + five agents: spec, code, review, test, ship) on the right.
* **Contact pills:** pill-shaped (fully rounded), 44px tall, 1px border, own line icons (18px, 1.6 stroke) + label. No brand logos.
* **Section divider:** mono number in champagne, title in Inter Tight 600, hairline rule with a 24px champagne lead-in. Static, so it renders the same in every viewer.
* **Work tiles / project cards:** subtly rounded (14px), flat surface fill, 1px border, no shadows. Structure is always: mono tag → title → 2–3 lines of body → stack chips. A small drawn arrow marks clickable cards.
* **Chips:** 22px tall, rounded 6px, 1px border, mono 11px. Information, not decoration.
* **Stack tiles:** monogram square (22px, 5px radius, bordeaux stroke) + label. One style for every technology instead of mixed vendor logos.
* **Activity panel:** stats row (three numbers) + contribution heatmap (11px cells, 3px gap, 2px radius) + legend. Generated daily by a GitHub Action.

Depth: completely flat. Hierarchy comes from borders, contrast and spacing, never from drop shadows.

## 5. Layout Principles
* Canvas width 840 for all full-width assets; embedded with `width="100%"`.
* Project cards: 410×230, two per row (`width="49%"`).
* Outer padding inside cards 28–48px; vertical rhythm on an 8px grid.
* Each asset ships as `name-dark.svg` / `name-light.svg`, switched with `<picture>` + `prefers-color-scheme`.
* Under 600px the README switches to `name-m-*.svg`: 420-wide single-column versions (header, work, hackathons, stack, activity, dividers, footer). Project cards keep their 410×230 frame but show only tag + title at large size, because the `<img>` width is fixed at 49%.
* `<a><picture>` must sit inside a `<p>` block, otherwise GitHub's Markdown parser splits the picture apart.
* All assets are committed in `assets/` and linked by relative path: no third-party image services.

## 6. Motion Rules
* SMIL only (works inside `<img>`), no JS, no filters heavier than a gradient.
* Durations 1.6–60s; easing linear or spline ease-out. Never faster than 1.2s per movement.
* Infinite loops only in the header graph (signal travel with node flash, 8s cycle; dashed orbit, 60s rotation). No pulsing rings.
* Dividers, cards, stack and activity are static. (Offscreen `<img>` animations may never tick, so nothing important can depend on an animation having run.)
* No blinking, typing effects, twinkles, waving shapes or color cycling.
