# ElyFlame — How the Site Works

Behavior spec for front-end development. Written September 24, 2026, from the prototype (`index.html`, `site.css`, `site.js`) and the fixes sent to GPT6 Astra. Sources: `outputs/prd.en.md`, `outputs/brief.en.md`, `docs/sow.md`. `[confirm: …]` marks items waiting on the client or Kiryl.

## 1. General Rules

- Stack: plain HTML, CSS, and JS with no dependencies. Forms submit without JS; JS adds validation, the class finder, and the modal.
- The site has one primary button, Book a Trial. There's no Register in the header.
- Anything the client hasn't provided yet appears on the site as a placeholder in square brackets: "[Founder name]", trial times marked [sample], the "What to bring" list (the client's request, Sep 25). Gray boxes stand in for photos. These blocks carry `data-requires-content` so they get checked before launch. No "Coming soon" banners.
- With the system "reduce motion" setting on, all animations and transitions are off and the Ribbon is a complete static line.
- Body text is 16 px or larger; labels are 14 px or larger.
- Functional text (class finder, form, FAQ) says "your child". "She/her" appears in at most 1–2 emotional headlines `[confirm: tone with the client]`.
- No generated photos of people. Until real photos arrive, use gray placeholders. Rules for children's photos, the style, and the processing workflow: `docs/photos.en.md`.
- Mobile layout applies up to 760 px, as in the prototype.
- Three languages: English (`/`), Russian (`/ru/`), Ukrainian (`/uk/`). The switcher is described in section 2. Each version has `hreflang` for all three and its own `canonical` `[confirm: who proofreads the translations]`.
- `tools/i18n.py` builds the Russian and Ukrainian pages from the English one, using the string tables in the script; don't edit `ru/` or `uk/` by hand. Program names stay English in the form's option values; only the visible text is translated.
- Cyrillic headings are set in Spectral SC: Cinzel has no Cyrillic, and Spectral SC also sets lowercase as small caps. It runs wider, so in Russian and Ukrainian the hero headline grows only as far as the room left of the gymnast allows (about 117 px at 1900 px, against 132 px in English) and stops short of her hand. There the star closes the first line ("Где грация ✳") and the second line starts at the left edge, so the accent word keeps its distance from the gymnast; on desktop the headline block keeps the English height, so the button and the scroll cue sit in the same place in all three languages, below the gymnast's feet; and long section headings are smaller on phones. The ELYFLAME logo stays in Cinzel everywhere; the line under it is translated.
- In running text and headings the town is written in Cyrillic, «Баффало-Гров»; the postal address stays in Latin so parents can type it into a map. Proper names stay in Latin too: ElyFlame Academy, USA Gymnastics, Silk Road International School.
- Display headings (h1, h2, the class finder result title) end with a period in all three languages, a brand device, as in "Where grace meets fire.". Buttons, field labels, and hints follow the norms of their own language.
- Browser translation: the switcher, the logo, and the addresses carry `translate="no"`. So does the hero headline while its letters animate; then the attribute comes off and the translator sees plain text, not single letters.

## 2. Header, Menu, Footer

**Header** stays on screen while scrolling: logo on the left, navigation Home · About · Parents' Info · Stretching · Contact, the Book a Trial button, and the language to its right. No Login link until the portal launches (project 2). The header button is shorter in Russian and Ukrainian: «Записаться» / «Записатися».

**Current page** is underlined and marked with `aria-current="page"` in source markup. Home remains current on Home; each inner page marks its own item. Scrolling does not change the current page; the section observer for navigation is removed.

**Language** is a globe, the current language code, and a chevron in the far right corner, after the button: a quiet utility that doesn't compete with the CTA. A click opens the list English / Русский / Українська, with a dot on the current one. Esc or a click elsewhere closes it. The interface codes are EN, RU, UA; the Ukrainian version lives at `/uk/`.

**Burger**: up to 1100 px in every language, since the Russian and Ukrainian items don't fit on one row. The menu opens as a sheet under the header and dims the page below.
- `aria-expanded` on the button reflects the state.
- The sheet closes when a link is tapped, on a tap on the dimmed page, and on Esc; after Esc, focus returns to the menu button.

**Phones (up to 767 px):** the header holds the logo, the Book a Trial button (always visible), and the burger. The language moves into the menu sheet as a segmented switcher EN | RU | UA, with the current one filled dark.

**Announcement bar** above the header: "$10 trial lesson · pay online or at the academy" and a "Find your first class →" link (hidden on phones). The orange link on the dark bar has a contrast of 8.4:1, passing AA and AAA.

The fixed bottom bar is gone; the header button replaces it.

**Footer:** logo, tagline, address, phone (224) 804-8324, email, call hours (Mon–Fri 9 am–10 pm, Sat 9 am–5 pm, Sun closed), page links, Instagram and Facebook, a Privacy Policy · Terms of Use row, and "© [current year] ElyFlame Academy. Site by Kirakito Technologies". No Register link: after the trial the Head Coach sends the Adobe form. The year updates automatically.

## 3. Ribbon

- One satin ribbon in SVG, behind the content. There are no other decorative lines on the page.
- A script builds the ribbon along a centerline: up to 12 px wide on desktop and 8 px on mobile, narrowing almost to a thread where it twists. It twists every 320 px of path (220 px on mobile). The color shifts smoothly from magenta #E9008D to orange #FDA63D and back over 1,600 px (1,100 px on mobile). The back side is paler and matte, the edges darker, and the flat stretches get a highlight.
- A mask does the drawing: a line wider than the ribbon (22 px, 16 px on mobile) along the same centerline whose visible length changes with scroll.
- Route: starts as a big loop in the hero, crosses the page between sections, passes behind headlines and illustrations, and makes large loops at section transitions, like the curled E in the logo. It never crosses body text.
- **Drawing on scroll.** The visible length follows the scroll position, with the tip staying about 70% down the viewport. Scrolling back up rewinds it.
- Implementation: a CSS scroll-driven animation. Keyframes are recalculated only when the layout changes (ResizeObserver, font loading, window resize); there are no scroll handlers.
- Unsupported browsers and reduced motion show the whole line, static.
- On mobile, the line stays clear of text and crosses the page between sections.
- In the "More than movement" section the left side holds only the ball (an orange sphere with a soft shadow on the background), with no backdrop and no flat hoop. After its loop the ribbon comes down to the ball, winds 1¼ turns around it like a hoop in perspective (an ellipse 1.5 ball radii wide, tilted −17°, the second turn lower than the first), and leaves down and to the right toward the next section. The far half of each turn passes behind the ball, the near half in front of it. On the ring the ribbon is flat and 30% wider, with one twist on the way in and one on the way out, and casts a light shadow. The ball is drawn in the same SVG as the ribbon; otherwise the ribbon couldn't pass both behind and in front of it. Mobile works the same way, with the ball centered above the copy and the ribbon leaving toward the right edge.
- The ribbon starts at the tip of the gymnast's stick in the hero. At the end it sweeps down the right side of the dark "Let's light the spark" section and slips behind the top edge of the footer.
- The script samples the path itself (`flatten()`); the browser's `getPointAtLength()` is too slow.
- **When content changes.** The route is rebuilt from the sections on the page whenever the layout changes, so longer copy, more FAQ items, a new section, or a hidden block move the ribbon with them. Each section in `<main>` gets a loop in its top padding; between loops the ribbon runs along the page edge (3.5% of the width from the edge on desktop, 2.5% on phones), outside the content column. Photos and video sit above the ribbon, so where it passes behind them it's hidden.
- **Rules for the WordPress build**, where the client edits content:
  1. Every block is a `main > section` with the standard section padding, and nothing goes in its top band: that's where the loop lives.
  2. Content stays inside the section's side padding. Full-bleed media only as a section background; the ribbon then passes behind it.
  3. The client edits content inside blocks. The blocks the route keys on (the hero with the gymnast, "More than movement" with the ball, the closing section) are fixed templates marked with data attributes, not ids the editor can change. If one of them is missing, the script skips that part of the route instead of throwing (the prototype still throws).
  4. Images and video have `width`/`height` or `aspect-ratio`, so the page doesn't jump after they load.
  5. Before launch and after big content changes, check the ribbon at 390 and 1440 px in all three languages with reduced motion on: the whole line is visible then.
- In Figma, draw the final state: the whole line.

## 4. Champion's Path (Class Finder)

### 4.1 Inputs

| Field | Options | Default |
|---|---|---|
| How old is your child? | 3, 4, 5, 6, 7, 8, 9, 10 or older | 4 |
| Any rhythmic gymnastics experience? | A brand-new beginning · Some recreational experience · Competitive experience | A brand-new beginning |

- For ages 3–5, Competitive experience is hidden. If it was selected and the age changes to 3–5, experience resets to A brand-new beginning.
- The result updates as soon as either field changes; there's no Show button.

### 4.2 The Six Levels

Stored as one config array, with data from SOW 2.1. All six points are always visible on the path.

| # | Label | Ages | Program | Apparatus | Result title | Result text |
|---|---|---|---|---|---|---|
| 1 | First steps | Age 3 | Recreational | Rope | A little spark of something big. | An introduction to movement, coordination, and playful exploration with the rope. |
| 2 | Find a rhythm | Ages 4–5 | Recreational | Rope, ball | Let curiosity lead. | Playful movement, growing confidence, and a first friendship with the rope and ball. |
| 3 | Build a base | Ages 6–7 | Competitive | Rope, ball, hoop | A new chapter begins. | Rope, ball, and hoop come together as athletes begin preparing for competition. |
| 4 | Grow stronger | Ages 6+ | Competitive | + Clubs | Make room for the next challenge. | Clubs join the repertoire, with a continued focus on stretching and apparatus skills. |
| 5 | Find expression | Ages 7+ | Competitive | + Ribbon (all five) | Let expression unfold. | The ribbon completes the apparatus repertoire as skills and flexibility develop. |
| 6 | Take the stage | Ages 8+ | Competitive | All apparatus | Bring ambition to the floor. | A pathway toward serious competitive gymnastics, with placement assessed by the coach. |

The overlapping ages "6–7" and "6+" come from the SOW. For now only levels 1 and 2 can be active. The texts for levels 3–6 stay in the config in case the client assigns levels by age `[confirm: question 5]`.

### 4.3 Which State Is Shown

| Age | A brand-new beginning | Some recreational | Competitive |
|---|---|---|---|
| 3 | Level 1 | Level 1 + experience line | — (option hidden) |
| 4–5 | Level 2 | Level 2 + experience line | — (option hidden) |
| 6 and older | Coach assessment | Coach assessment | Coach assessment |

### 4.4 What Each State Shows

| | Level 1 or 2 | Coach assessment |
|---|---|---|
| Path | The level's circle is filled magenta with a white number and a soft halo. The ✦ spark sits above it. Other circles are outlined | No circle is filled. Levels 3–6 are softly tinted as the possible range. The "Start with a coach assessment" label sits above the path on the left, with the spark next to it |
| Label | Possible starting point / Level 1 (or 2) | Starting point / Coach assessment |
| Title | From the levels table | Every path is individual. |
| Text | From the levels table | Age is only part of the picture. Tell us about your child's experience, and the coach will help find a suitable starting level at the trial. |
| Extra line | With Some recreational: "Great start. The coach will check if your child is ready for the next step." | — |
| Program passed to the form | Recreational | Competitive |

Every state shows "Your coach will confirm the right level at the trial." and a Book a Trial button.

### 4.5 Button and Form Link

Book a Trial in the result opens the form and fills in the program (Recreational or Competitive) and the child's age. The Explore Stretching button sets the program to Stretching & Flexibility and clears the age.

### 4.6 Motion, Accessibility, Mobile

- The spark moves to its new position in 0.65 s, easing out. A circle's fill changes in 0.25 s. With reduced motion, both are instant.
- `aria-current="step"` on the active circle or the coach assessment label. The result block has `aria-live="polite"`. The spark is hidden from screen readers.
- Desktop: a horizontal path with labels under the circles. Mobile: a vertical path, levels top to bottom, labels on the right.

## 5. Trial Booking Form

Booking is a hybrid (Kiryl's decision, D1): the parent fills in the details, picks a trial day and time, and pays $10, online via Stripe (preferred) or at the academy. The request goes to the academy, which confirms the time or texts the parent to reschedule.

### 5.1 Opening

- Any Book a Trial button opens the form in a `<dialog>`: centered on desktop, full screen on mobile.
- Without JS, the buttons link to the `#trial` section on the page, and the form posts to `/api/trial` (a placeholder until the back end is decided).
- Closing: the × button, Esc, or a click on the backdrop.

### 5.2 Fields

Error messages are Design's proposal.

| Field | Rule | Error message |
|---|---|---|
| Child's name | required, 2–50 characters | Enter your child's name |
| Child's age | required, 3–99; prefilled from the class finder | Enter your child's age / Age must be between 3 and 99 |
| Experience | required: None / Some recreational / Competitive | Select your child's experience |
| Program | required: Recreational / Competitive / Stretching & Flexibility; prefilled from the class finder, editable | Select a program |
| Trial day and time | required; fixed trial slots per program from the config `[confirm: real slots]` | Select a trial time for this program |
| Payment | radio buttons: Pay online now (recommended), the default / Pay at the academy | — |
| Parent's name | required, 2–80 characters | Enter your name |
| Phone | required, US mask (XXX) XXX-XXXX | Enter a phone number, like (555) 123-4567 |
| Email | required, valid address | Enter an email address, like name@example.com |
| Consent | must be checked | Confirm that the academy can contact you |

Spam protection per the SOW: a honeypot field, rate limiting, and an invisible CAPTCHA if needed (back end).

### 5.3 Validation and Errors (GOV.UK style)

- Fields are validated on submit. Each error sits right under its field and says what to fix.
- An error summary at the top of the form links to each field, and focus moves to it.
- Entered values are never cleared.

### 5.4 Submit Button States

Default, hover, focus, loading (spinner, button disabled), and error.

### 5.5 After Submitting

- Success: "Your trial request is in!", "The academy will confirm your trial time within 24 hours. If the time doesn't work, they'll text you to find another.", a summary (child, program, time, payment method, contact details), and a "What to bring" list `[confirm: list from the client]`. With online payment, Stripe Checkout opens before this screen.
- Server error (SOW): "Oops. Something went wrong. Please try again or call us at [phone]."
- In the prototype nothing is sent; only the success view is shown.

## 6. Hero

The headline "Where Grace Meets Fire" (SOW placeholder, `[confirm: question 23]`), a short paragraph, the Book a Trial button, and the line "$10 trial lesson · the academy confirms your time". Age appears only in the subheading (the competitive path from 6, first classes from 3); the announcement bar and the line under the button talk about the trial and its price. The ✳ ornament opens the headline's second line, one space from the word, and scales with it. On phones the illustration box grows to the figure's height, so the copy starts below her feet. A large placeholder for an athlete photo or a silent looping video sits on the right on desktop and under the headline on mobile. The Ribbon loop wraps around its edge.

### 6.1 Gymnast and Hero Entrance

- On the right is a gymnast silhouette (an illustration, not a photo) with a floor shadow. She is 520 px tall from 1440 px up and shrinks smoothly to 470 px at 1200 px and below, so her feet and the floor shadow always end above the scroll cue line ("Find the right class"), at least 14 px clear. The Ribbon starts at the tip of her stick.
- Once per load, after fonts are ready: the headline rises letter by letter (Serega Gentle), the gymnast's free leg rises from the hip (1.6 s), "fire." lands with a spring accent (Serega Emotional) as the leg nears the top, then the paragraph, button, and caption rise in.
- With reduced motion, everything is in place at once. If the script fails to load, the text appears after 4 s and the leg rises after 2.5 s.

## 7. Gallery and Video

Two blocks after "More than movement". Both carry `data-requires-content` until the client's photos and video arrive (questions 19 and 22).

**Gallery.** Eyebrow "Inside the academy", the heading "Practice, play, *perform.*", and a "Follow us on Instagram ↗" link. Six photo slots (the SOW asks for 6–9 tiles): three columns on desktop, a sideways-scrolling row on phones, where a tile is 78% of the width, so the next one peeks in, and the row snaps to tiles. Every photo is cropped square (`object-fit: cover`), so the client can upload any photo in WordPress. Each photo sits in a 6 px cream frame (`--paper-raised`) with the dropdown shadow and a slight tilt: −3°, 2°, −1.5°, 2.5°, −2°, 1.5°, repeating every six photos. On hover a photo straightens and rises 6 px. The first time the grid comes into view, the photos pop in one by one: 80 ms apart, from 60% size with a slight spring. Without JavaScript or with reduced motion, they simply stand in place. Until photos arrive, the slots are gray. Alt text describes the scene and never names a child.

**Video.** A dark band: eyebrow "On the carpet", the heading "See grace *in motion.*", and a decorative 16:9 background loop with no controls: `<video autoplay muted loop playsinline preload="auto">` with WebM and MP4 sources and the first frame as the poster; it's `aria-hidden`. An IntersectionObserver pauses it when the block leaves the viewport and resumes it when the block returns. With reduced motion the video never starts and only the poster shows. There's no pause button, a deliberate choice (Alena, Sep 25): WCAG 2.2.2 asks for a way to stop motion longer than 5 seconds, and the reduced-motion setting is the only way here. Files: `assets/video/performance.webm` and `performance.mp4`, 720p, up to 3 MB each, and `performance-poster.jpg`; the current files are placeholders with the same names.

## 8. Coaches: Founder and Team

The full section lives on About (`/about/#coaches`): the founder, expandable biography, and team. Home keeps a short introduction after the video: portrait, name, role, two badges, and “Meet the coaches →” linking to About. The team and biography are not duplicated on Home.

**Founder.** "Portrait + text": on the left the portrait takes 40% of the block (4:5, in the gallery's cream frame with a −2.5° tilt that straightens on hover and a pop-in on first view); on the right the eyebrow "Our coaches", the heading "Guidance with *heart and purpose.*", the name in large Cinzel, the role ("Founder") in Manrope, 2–3 lines about her approach, and two credential badges in a row: "National judge, USA Gymnastics" (medal icon) and "Member club, USA Gymnastics" (shield icon). On phones: heading, portrait, then the text. Until the real portrait arrives, the frame shows the ElyFlame monogram on sand, not a gray box. The name and the bio are placeholders `[confirm: question 14]`. Certifications (SafeSport, CPR) aren't shown on the site; they're shared on a parent's request. The "Content preview" note is gone. Update Sep 25: the portrait stops growing at 520 px wide on About and 420 px on Home, and on desktop the text block sits at the bottom of the portrait so the badges line up with its lower edge. The name and role are the draft from question 14, "Yelizaveta Yuvkhimenko, Founder and head coach", with a two-line bio built only from known facts and a placeholder quote from her in Cinzel with the ✳ ornament; all three wait for the client's confirmation. The eyebrow reads "Meet your coach" while the founder is alone; on About it switches to "Our coaches" once the team array has coaches (site.js). Home keeps "Meet your coach"; switch it by hand when the team appears.

**Team.** Under the founder, a "The team" block rendered from an array: `<script type="application/json" id="team-data">` holds `[{name, role, focus, photo, alt, bio}]`, and `site.js` builds one card per coach from `<template id="team-card">`. A card: a square photo (the monogram until there's one), the name in Cinzel, the role in Manrope, one line of specialization; no frames or shadows, only spacing. Grid: 3 columns on desktop, 2 on tablets (up to 1050 px), 1 on phones. Empty array: the block stays hidden (the case at launch). One coach: one wide card over two columns, photo left, text right. The founder block never changes with the team. Adding a coach means adding an object to the array (photo paths start with `/`) and translation rows in `tools/i18n.py`; in WordPress it's a repeater field with the same fields.

## 8.1 Finale

The "Let's light the spark" section and the footer form one dark stage with a glow. The section holds a line about booking, the Book a Trial button, and an email link. With JS running, the separate light booking section `#trial` is hidden and booking happens in the dialog; without JS it stays as the fallback form.

At the bottom of the footer stands the "team": a row of light silhouettes of girls with a ball, hoop, clubs, and rope (sprite `assets/gymnast/team.svg`, an illustration, not photos). The satin ribbon is strung like a garland between the sticks of the two end girls. As the footer scrolls in, the girls rise in one by one and the ribbon draws from right to left. The girls grow with the width (120–240 px) and stand in equal cells, as many as fit: 5 at 320 px, 6 at 390 px, 12 from 760 px. The two with sticks always stand at the ends. The rule is in `docs/footer-team.en.md`.

## 9. FAQ

The full FAQ lives on Parents’ Info. Native `<details>` let each question open and close independently; the first starts open. It works without JS and by keyboard. Home keeps a short introduction and “Read the parent guide →”.

## 10. What Could Change This Behavior

- The real trial slots and the Stripe account.
- Who translates the Russian and Ukrainian copy.
- The "she/her" tone is the client's call.


## 11. About Page

- URLs: `/about/`, `/ru/about/`, `/uk/about/`. The English source is `about/index.html`. Run `python tools/i18n.py` to build RU/UK; never edit generated pages by hand.
- Introduction: “A sport. An art. A place to begin.” and links to five page sections. No scrolling Ribbon or Home gymnast here; the page gets its own composition from the apparatus row. The shared footer silhouettes remain.
- The sport: rope, hoop, ball, clubs and ribbon, each shown by one of the footer girls (`assets/gymnast/team.svg`: kid-10 with the rope, kid-3 with the hoop, kid-1 with the ball, kid-7 with the clubs, kid-6 with the ribbon stick) in ink, all at one scale with their feet on one floor; the ribbon girl's satin ribbon is painted by `paintSatin()` from her stick tip (without JS she holds only the stick); rhythm, balance, coordination, strength, flexibility and expression; an Olympic sport since 1984.
- Why ElyFlame: six levels from first steps toward competition, with placement assessed by the coach at the trial. The founder is a USA Gymnastics national judge and the academy is a member club. History and mission have a separate placeholder block (question 21).
- Coaches: the full section from section 8 moves to About. The founder and team members have native `<details>` disclosures labelled “Read more”, accessible by keyboard. The founder’s disclosure also works without JS; team cards are created by JS. The `bio` field in `#team-data` supplies each detailed biography; an empty field hides that card’s disclosure. An empty array hides the team. Array text uses the shared translation tables and visible JSON fields are checked by the generator. Certifications are available only on a parent's request; no scans or SafeSport/CPR listings are public. The founder's name, biography and photo await question 14.
- Space (`#the-space`): two photo slots, a 4:3 room view and 1:1 equipment photo, using the gallery's cream frames and tilt. They stack on phones. Equipment and safety arrangements remain placeholders (22). Entrance, drop-off and pick-up use door #11. Parents can watch the trial; afterwards they may attend with the Head Coach's permission, at open practices, or as volunteers.
- Achievements (`#achievements`): a list with year, competition, result, category and level. One bracketed template row awaits question 17; no invented years, medals or results.
- Every Book a Trial link goes to the same-language Home with `#trial`. Home opens the single booking dialog on initial load, hash changes and history restoration. Without JS, the link reaches the one ordinary form on Home.
- Shared `site.js` initializes the finder, booking and Ribbon geometry only when their blocks exist. Navigation, language controls, coaches and the footer work on all pages. Reduced motion keeps images visible and disables entrances and hover lifts.

### Five Pages and Shared Navigation

Home (`/`), About (`/about/`), Parents’ Info (`/parents/`), Stretching (`/stretching/`) and Contact (`/contact/`) are standalone pages, each in EN/RU/UK. All shared header/footer menu items target the corresponding same-language page. Home links to the top of Home. Home sections are short previews with internal page links; the full address strip remains as required by the SOW.


The generator iterates over registered pages, uses shared translation tables and rebases relative links for any depth. Language switching keeps the current page (About → About); canonical and hreflang URLs target that page’s versions. Headers and footers are copied into each English page. The generator checks them after normalizing URLs and current-item markers, and checks language controls against shared helpers. A mismatch, stale translation row or English leftover fails the build before any files are written.

## 12. Stretching Page

- `/stretching/`, `/ru/stretching/`, `/uk/stretching/`: one weekly class, with five audience entries: dancers, figure skaters, martial artists, runners, and teens/adults. Three bracketed benefit placeholders await question 32; no unapproved benefit claims. Class structure, duration and entry requirements remain placeholders (30).
- The paper hero has text on the left and the wide front-split gymnast from `assets/gymnast/split.svg#split` on the right, in ink. She sits on a light mat, a `--sand` strip a little wider than her and drawn in the same SVG (viewBox `-160 0 2643 1340`, symbol pinned at 2323 × 1253), so she reads as grounded without a full-width line; the hero and the audience block are separated by spacing only. No ribbon, no mirroring, no animation. At 1440 the figure fills the right column; at 390 it sits below the button at the full content width. The subtitle names only the format, "Once a week · [60 minutes]" (duration is question 30); the audience lives in the next block. The temporary Home gymnast and hero footnote are removed; there is no scrolling Ribbon.
- Who it’s for: the five audiences are plain 20 px text in one line (wrapping on phones), split by a small decor ✳, so they support the heading instead of competing with it. The block ends with "Sounds like you? Book a trial →", which carries the program to the Home form like the hero button.
- No public schedule (answer 9): a bracketed placeholder directs visitors to ask the academy for times. No class or membership prices (answer 8 supersedes the Sep 24 decision). The confirmed $10 trial fee remains in the shared header (answer 3).
- Booking links carry the program to the single Home form: `../?program=stretching#trial`. Shared JS adds the same parameter to the shared header CTA on Stretching. Home accepts only the known key `stretching`, selects Stretching & Flexibility and leaves the participant age empty. Without JS the ordinary form opens and the program is selected manually.
- Home keeps a short introduction, the trial button and “Explore Stretching →”. Every Stretching menu item now targets the page. Parents’ Info and Contact are also standalone pages.
- The current trial form is designed for a parent and child; adult registration is open question 31. Adults can contact the academy directly.

## 13. Contact Page

- `/contact/`, `/ru/contact/`, `/uk/contact/`: 1250 Radcliffe Road, Buffalo Grove, IL 60089, in the Silk Road International School building; (224) 804-8324 and academy@elyflame.com. Phone and email links open their respective apps.
- **Phone hours**, not class hours: Monday–Friday 9 am–10 pm, Saturday 9 am–5 pm, Sunday closed. Class schedules are not published (answer 9).
- The light hero puts the heading, phone, email and call hours on the left; the contact form sits on the right. Phone and email have no external-link arrows.
- The second section has a large Google Maps iframe with `loading="lazy"`, a localized title, and no click/consent gate. The adjacent address names the school building; an ink text callout with the decor-colored ✳ identifies door #11 for entrance, parking, drop-off and pick-up. The persistent Get directions ↗ link opens Google Maps with `rel="noopener"` even if the iframe fails. The old oversized door number and separate Call us band are removed.
- Contact form: name, email, phone and message, with the same field treatment as the trial form. All fields are required; limits are 100/254/40/5000 characters, and phone accepts 10–15 digits with common punctuation. Errors appear beside fields with `aria-describedby` and `aria-invalid`; JS focuses the first invalid field. Typed values remain after validation. The form sends `POST /api/contact` with or without JS; a hidden language field preserves the locale. JS validates fields, submits the request and displays the server result; network errors offer retry or a call without losing entered values. Without JS, `tools/serve.py` returns the selected-language page with inline errors or validation confirmation; a base URL preserves links and assets. The receiving email address awaits question 33. The prototype stores/sends nothing and states this before and after validation. Production must supply a real POST handler and delivery integration; static hosting alone cannot process the no-JS POST. This supersedes the earlier no-form decision and restores SOW 3.4. Trial booking still uses the single Home form.
- Home retains the address strip with phone, email, call hours, door #11 and Get directions, plus “Plan your visit →”. Contact menus now target the standalone page. Parents’ Info also targets a standalone page.

## 14. Parents’ Info Page

- `/parents/`, `/ru/parents/`, `/uk/parents/`: a guide with four index links: FAQ, after the trial, policies/documents and clothing/equipment. Policies and documents share one section; private lessons move into FAQ. Including the hero and trial banner, there are six sections.
- FAQ moves from Home: experience, trial fee, previous training, teens/adults, parent observation and registration. There are 11 questions, including clothing, what to bring, the first lesson, absences/make-up classes and private lessons. Private lessons has a placeholder answer and email link without an arrow; its old #private-lessons anchor remains on the disclosure. The first question starts open; the rest are closed. Disclosures work independently, by keyboard and without JS. Unknown answers stay in square brackets (21).
- Parents may watch the trial; afterwards they attend with the Head Coach's permission, at open practices or as volunteers. This replaces the earlier incomplete answer.
- After the trial, the Head Coach sends an Adobe registration link. A child may join practice only after the form and first payment are complete. The steps explain the process without invented Adobe URLs or payment buttons.
- Refund/cancellation rules and the code of conduct remain placeholders. Clothing and equipment are listed separately for Recreational, Competitive and Stretching, without invented requirements. Private lesson details also await question 21; the email link is in the FAQ answer.
- Waiver and medical form: two text placeholders for PDF documents. No links, download buttons or `href="#"`; there are no file requests or 404s until files arrive. Add real links and document translations once checked PDFs are supplied.
- Home keeps its heading, short first-visit introduction, registration note and “Read the parent guide →”; the full FAQ is removed. All five pages are registered in `PAGES`; the transitional section-link rule is removed.

### Inner-page visual rules (Alena, Sep 25 revision)

Stretching, Contact and Parents’ Info start on paper. Dark stage is used for the trial banner before the shared footer, plus at most one other section: After the trial on Parents’ Info. Use existing silhouettes, paintSatin satin ribbon or a decor-colored ✳, at most one decorative composition per screen; no homemade line icons, arcs or oversized numbers. Column gaps are 40–88 px at desktop, with content aligned toward the start. Parents’ Info alternates a horizontal index, FAQ columns, dark registration, combined policies/documents and a clothing/equipment row. In registration, compact 01–02–03 numbers are connected by static paintSatin ribbon, in a reserved lane above descriptions on desktop and to their left on mobile. ResizeObserver updates the drawing when width changes; neither scroll nor reduced motion animates it. The ribbon stays clear of numbers and text. Without JS the steps remain readable without ribbon. One policies/documents index link replaces the separate document link; #documents remains inside the combined section. FAQ and unavailable PDF behavior are unchanged. External-site links use ↗; tel/mailto links do not.
