# ElyFlame — website concept

An English-language, responsive design implementation of the approved Ribbon / Champion’s Path / Stage direction. Plain HTML, CSS, and JavaScript; no build step or dependencies.

## Preview

Run `python -m http.server 4173 --bind 127.0.0.1` from this folder, then open http://127.0.0.1:4173. You can also open `index.html` directly. Google Fonts requires an internet connection; local serif and sans-serif fallbacks are provided.

## Implemented

- Hero entrance (`hero-reveal.js`, ES module — preview over http): headline letters (Serega Gentle), the "fire." accent (Serega Emotional) and the gymnast's leg start together; libraries in `lib/`.
- Dark finale: the closing section and the footer form one stage; the ribbon sweeps down its right side and slips behind the footer.
- Footer team: traced silhouettes from `assets/gymnast/team-sheet.jpg` (sprite `assets/gymnast/team.svg`) with the satin ribbon strung between two sticks; a view timeline makes them rise in.

- Responsive homepage with Cinzel headlines, whitespace, apparatus art, and a dark stage. The hero shows a gymnast silhouette traced from `assets/gymnast/sheet-2.jpg` (a generated illustration, not a photo). coloured with clip paths (skin, sleeveless magenta leotard, dark hair, dark stick) and standing on a soft floor shadow. On load the free leg rises from the hip once (1.6 s); the stick stays still, so the ribbon is attached from the first frame. Reduced motion shows the final pose.
- A `.ribbon-anchor` at the stick tip (21.6% / 0.7% of the figure box) marks where the page ribbon starts; `layoutRibbon()` leaves it along the stick, up and to the right.
- One continuous 2.5 px magenta-to-orange SVG ribbon. Large hero and section-transition loops cross reserved whitespace and wrap the apparatus illustration. CSS scroll-driven animation draws and rewinds it. JavaScript recalculates geometry/keyframes only on layout changes; there is no scroll handler. Unsupported browsers and reduced-motion preferences show the full line. No second decorative line in Stretching.
- Six levels in one `levels` array in `site.js`, with the requested labels, ages, programs, apparatus and result copy. Ages 3–5 use levels 1–2; ages 6+ use coach assessment and tint levels 3–6. Competitive experience is hidden/disabled for ages 3–5 and resets when switching to those ages. Recreational experience adds the readiness note. Mobile levels form a vertical path; the spark moves in 0.65 seconds and respects reduced motion.
- Native booking dialog from every trial link. The finder prefills program, age and experience; Stretching prefills its program. One form is moved into the dialog, avoiding duplicate IDs and preserving entered values. Escape, focus containment and focus return use the native dialog behavior.
- Child name/age/experience, editable program, sample preferred day, parent name, US phone mask, email and contact consent. Sample schedules are in the `programs` config. Field-specific errors, linked/focused error summary, `aria-invalid`, error descriptions, and loading/disabled/error button states.
- **Local-only booking simulation:** submit waits briefly, then displays the requested “You're booked!” view, option-C payment explanation, safe-text booking summary and placeholder packing list. Both form and confirmation explicitly identify the prototype. No network request, email, payment, local storage or real reservation is made. Edit returns to the preserved fields.
- Without JavaScript the form remains in `#trial`, uses native validation and has `method="post" action="/api/trial"`. **That endpoint is only a placeholder and is not implemented by the static preview server.**
- Two coach entries with gray `.coach-photo` placeholders, credentials/bio placeholders and a safety row. The section carries `data-requires-content`. Adding `data-production` to `<body>` hides marked content previews.
- SOW navigation, quiet Login, footer logo/contact placeholders/page links/social links/2026 credit and post-trial registration link. Login, registration and legal anchors reveal explicit content placeholders rather than pretending those services exist.
- Parent FAQ, map directions, keyboard focus, semantic headings, and a mobile trial dock that yields to a visible inline trial button.

## Before production

This is a design prototype, not the complete production PRD. Confirm D1–D5 and the outstanding questions in `docs/client-questions.en.md`, particularly booking/payment arrangements, age overlap and program placement. Levels 3–6 are retained in the config for later client-approved matching; they cannot currently become the selected level.

Implement `/api/trial` with server validation, rate limiting, spam protection, approved data handling and email delivery. Replace the local simulation with a checked server response, connect payment links after academy confirmation, and revise the confirmation wording to match the actual booking status. Test both JavaScript and no-JavaScript submissions on that backend. Replace all sample days and packing items with approved content.

Supply real hero media, coach portraits/bios/credentials, safety confirmations, phone, opening hours, policies, legal text and at least six real athlete photos with publication permission. Remove or hide content previews until confirmed; `data-production` hides marked sections but does not by itself make this prototype launch-ready. Confirm the founder's judge credential before publication. Replace placeholder login/registration/legal panels with the actual destinations. Parent portal, registration, analytics, payment, standalone inner pages and a contact-form backend remain unimplemented.

Run production accessibility and Lighthouse checks after real media and integrations are in place; no performance score is claimed for this prototype.

Existing planning documents and wiki pages are preserved.
