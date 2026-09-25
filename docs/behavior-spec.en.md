# ElyFlame — How the Site Works

Behavior spec for front-end development. Written September 24, 2026, from the prototype (`index.html`, `site.css`, `site.js`) and the fixes sent to GPT6 Astra. Sources: `outputs/prd.en.md`, `outputs/brief.en.md`, `docs/sow.md`. `[confirm: …]` marks items waiting on the client or Kiryl.

## 1. General Rules

- Stack: plain HTML, CSS, and JS with no dependencies. Forms submit without JS; JS adds validation, the class finder, and the modal.
- The site has one primary button, Book a Trial. There's no Register in the header.
- Anything the client hasn't provided yet appears on the site as a placeholder in square brackets: "[Coach name]", "[Credentials]", trial times marked [sample], the "What to bring" list (the client's request, Sep 25). Gray boxes stand in for photos. These blocks carry `data-requires-content` so they get checked before launch. No "Coming soon" banners.
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

**Current section** is underlined in the menu. A line at 40% of the viewport decides which section is current; sections without their own item (the class finder, coaches, the finale, the form) count toward the item above them. Without JS, Home is underlined.

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

- On the right is a gymnast silhouette (an illustration, not a photo) with a floor shadow. The Ribbon starts at the tip of her stick.
- Once per load, after fonts are ready: the headline rises letter by letter (Serega Gentle), the gymnast's free leg rises from the hip (1.6 s), "fire." lands with a spring accent (Serega Emotional) as the leg nears the top, then the paragraph, button, and caption rise in.
- With reduced motion, everything is in place at once. If the script fails to load, the text appears after 4 s and the leg rises after 2.5 s.

## 7. Gallery and Video

Two blocks after "More than movement". Both carry `data-requires-content` until the client's photos and video arrive (questions 19 and 22).

**Gallery.** Eyebrow "Inside the academy", the heading "Practice, play, *perform.*", and a "Follow us on Instagram ↗" link. Six photo slots (the SOW asks for 6–9 tiles): three columns on desktop, a sideways-scrolling row on phones, where a tile is 78% of the width, so the next one peeks in, and the row snaps to tiles. Every photo is cropped square (`object-fit: cover`), so the client can upload any photo in WordPress. Until photos arrive, the slots are gray. Alt text describes the scene and never names a child.

**Video.** A dark band: eyebrow "On the carpet", the heading "See grace *in motion.*", and a silent 16:9 loop without controls. It starts by itself when the block comes on screen and pauses when it leaves (`muted`, `loop`, `playsinline`; the file loads only when the block is near). A 44 px magenta button in the bottom-left corner pauses and resumes it (`aria-label` "Pause video" / "Play video"): motion longer than 5 seconds must be stoppable. With reduced motion the video doesn't start: the poster shows with the button set to play. The loop is 10–20 s, has no sound and no text, and weighs about 4 MB at most; the poster is its first frame. Until the video arrives, the poster area is a dark placeholder.

## 8. Coaches and Safety

A section after the video. Two coach entries: a gray photo placeholder, "[Coach name]", "[Credentials]", and a one-line bio `[confirm: question 14]`. A trust row: "National judge, USA Gymnastics (founder)" and "USA Gymnastics member club". Certifications (SafeSport, CPR) aren't shown on the site; they're shared on a parent's request. Until bios arrive, the section shows placeholders (the client's request, Sep 25); `data-requires-content` marks it for a check before launch.

## 8.1 Finale

The "Let's light the spark" section and the footer form one dark stage with a glow. The section holds a line about booking, the Book a Trial button, and an email link. With JS running, the separate light booking section `#trial` is hidden and booking happens in the dialog; without JS it stays as the fallback form.

At the bottom of the footer stands the "team": a row of light silhouettes of girls with a ball, hoop, clubs, and rope (sprite `assets/gymnast/team.svg`, an illustration, not photos). The satin ribbon is strung like a garland between the sticks of the two end girls. As the footer scrolls in, the girls rise in one by one and the ribbon draws from right to left. The girls grow with the width (120–240 px) and stand in equal cells, as many as fit: 5 at 320 px, 6 at 390 px, 12 from 760 px. The two with sticks always stand at the ends. The rule is in `docs/footer-team.en.md`.

## 9. FAQ

An accordion built on `<details>`: each question opens and closes on its own, and the first one starts open. Works without JS.

## 10. What Could Change This Behavior

- The real trial slots and the Stripe account.
- Who translates the Russian and Ukrainian copy.
- The "she/her" tone is the client's call.
