# ElyFlame Academy website

Design and prototype repo for the ElyFlame Academy of Rhythmic Gymnastics site (Buffalo Grove, IL), launching October 12, 2026. Alena K (design) works here; Kiryl L is the PM; Ivan K builds production.

## Where things live

- Product: `outputs/brief.md`, `outputs/prd.md`, `outputs/research.md`. Read them before changing scope or copy.
- Behavior spec: `docs/behavior-spec.md` is the source of truth for how the site works. When behavior changes, update it in the same change.
- Decisions: `docs/decisions.md`. Add a row when a change affects scope or style, or departs from the SOW (`docs/sow.md`).
- Open questions: `docs/client-questions.md`. Cite them by number (D1–D5 for the PM, 1–24 for the client).
- Prototype: `index.html`, `site.css`, `site.js` at the root.
- Pipeline commands: `.claude/commands/` (`/brief` → `/research` → `/prd`).

## Documents

- Every document is a pair: `name.md` in Russian for Alena, `name.en.md` in English for the team. Edit both in the same change.
- The team reads documents in the Kirakito wiki (English, WordPress, under the page ElyFlame RG), so the `.en.md` version is what gets published. `outputs/wiki/` holds generated paste-ready HTML and is gitignored.

## Prototype rules

- Plain HTML, CSS, and JS with no build step; forms submit without JS. Reach for browser features before libraries.
- Colors come from the tokens in `:root` of `site.css`; raw hex belongs only to the illustration palette.
- Type floor: body 16 px, labels 14 px, buttons 15 px. Caps live only in Cinzel headings; labels are sentence case.
- Magenta (`--pink`) marks interactive elements and the hero headline.
- `↗` marks external links; internal actions use `→`.
- The header holds one primary button, Book a Trial. Register lives in the footer and the post-trial email.
- People appear only in real client photos with parental consent; until those arrive, use gray placeholders or brand illustrations.
- Functional copy (class finder, form, FAQ) says "your child".
- The ribbon is a satin SVG: `paintSatin()` in `site.js` builds it along the path from `layoutRibbon()`, and a scroll-driven mask reveals it. The About ball lives in the same SVG; the ring's near half goes to `.ribbon-front`, painted over the ball. Keep ribbon passes more than ~20 px apart, or the mask uncovers the later pass early. Its route stays clear of text and buttons. Sample paths with `flatten()`; `getPointAtLength()` costs ~1 ms per call and froze page load for seconds.
- The hero entrance lives in `hero-reveal.js` (an ES module, so preview over http, not file://): headline letters, the "fire." accent and the gymnast's leg start together.

## Done means checked

- Serve with `python -m http.server 4173 --bind 127.0.0.1` from the repo root.
- Look at 1440 px and 390 px: no console errors, no horizontal scroll from 320 to 1920 px, the ribbon clear of text.
- Audit generated UI with the `design-anti-slop` skill.

## Working together

- Two agents edit this repo: Claude Code and GPT6 Astra. One agent edits the prototype files at a time; commit before handing over.
- Git is local only; there is no remote.
