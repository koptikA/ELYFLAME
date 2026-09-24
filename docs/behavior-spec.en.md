# ElyFlame — How the Site Works

Behavior spec for front-end development. Written September 24, 2026, from the prototype (`index.html`, `site.css`, `site.js`) and the fixes sent to GPT6 Astra. Sources: `outputs/prd.en.md`, `outputs/brief.en.md`, `docs/sow.md`. `[confirm: …]` marks items waiting on the client or Kiryl.

## 1. General Rules

- Stack: plain HTML, CSS, and JS with no dependencies. Forms submit without JS; JS adds validation, the class finder, and the modal.
- The site has one primary button, Book a Trial. There's no Register in the header.
- A block without client content isn't shown (`data-requires-content` attribute). No "Coming soon" placeholders.
- With the system "reduce motion" setting on, all animations and transitions are off and the Ribbon is a complete static line.
- Body text is 16 px or larger; labels are 14 px or larger.
- Functional text (class finder, form, FAQ) says "your child". "She/her" appears in at most 1–2 emotional headlines `[confirm: tone with the client]`.
- No generated photos of people. Until real photos arrive, use gray placeholders.
- Mobile layout applies up to 760 px, as in the prototype.
- Three languages: English (`/`), Russian (`/ru/`), Ukrainian (`/uk/`), a switcher in the header, `hreflang` both ways `[confirm: who translates the copy]`. Addresses and the brand name carry `translate="no"`. After its animation the headline is plain text again, so browser translation sees words, not letters.

## 2. Header, Menu, Bottom Bar, Footer

**Header** stays on screen while scrolling: logo on the left, navigation Home · About · Parents' Info · Stretching · Contact, and the Book a Trial button. No Login link until the portal launches (project 2).

**Mobile menu** opens with the Menu button.
- `aria-expanded` on the button reflects the state.
- The menu closes when a link is tapped and on Esc; after Esc, focus returns to the Menu button.

**Mobile bottom bar** "Book a Trial $10" is fixed to the bottom of the screen.
- It hides while another Book a Trial button or the form's submit button is at least 75% visible (ignoring 110 px at the top for the header and 88 px at the bottom for the bar itself), so two identical buttons never sit next to each other.
- While hidden, it can't be clicked or reached by screen readers (`inert`, `aria-hidden`).
- There's no bottom bar on desktop.

**Footer:** logo, tagline, address, phone (224) 804-8324, email, call hours (Mon–Fri 9 am–10 pm, Sat 9 am–5 pm, Sun closed), page links, Instagram and Facebook, a Privacy Policy · Terms of Use row, and "© [current year] ElyFlame Academy. Site by Kirakito Technologies". No Register link: after the trial the Head Coach sends the Adobe form. The year updates automatically.

## 3. Ribbon

- One satin ribbon in SVG, behind the content. There are no other decorative lines on the page.
- A script builds the ribbon along a centerline: up to 12 px wide on desktop and 8 px on mobile, narrowing almost to a thread where it twists. It twists every 320 px of path (220 px on mobile). The color shifts smoothly from magenta #E9008D to orange #FDA63D and back over 1,600 px (1,100 px on mobile). The back side is paler and matte, the edges darker, and the flat stretches get a highlight.
- A mask does the drawing: a wide line along the same centerline whose visible length changes with scroll.
- Route: starts as a big loop in the hero, crosses the page between sections, passes behind headlines and illustrations, and makes large loops at section transitions, like the curled E in the logo. It never crosses body text.
- **Drawing on scroll.** The visible length follows the scroll position, with the tip staying about 70% down the viewport. Scrolling back up rewinds it.
- Implementation: a CSS scroll-driven animation. Keyframes are recalculated only when the layout changes (ResizeObserver, font loading, window resize); there are no scroll handlers.
- Unsupported browsers and reduced motion show the whole line, static.
- On mobile, the line stays clear of text and crosses the page between sections.
- The ribbon starts at the tip of the gymnast's stick in the hero. At the end it sweeps down the right side of the dark "Let's light the spark" section and slips behind the top edge of the footer.
- The script samples the path itself (`flatten()`); the browser's `getPointAtLength()` is too slow.
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

The headline "Where Grace Meets Fire" (SOW placeholder, `[confirm: question 23]`), a short paragraph, the Book a Trial button, and the line "Ages 3 & up · $10 trial lesson". A large placeholder for an athlete photo or a silent looping video sits on the right on desktop and under the headline on mobile. The Ribbon loop wraps around its edge.

### 6.1 Gymnast and Hero Entrance

- On the right is a gymnast silhouette (an illustration, not a photo) with a floor shadow. The Ribbon starts at the tip of her stick.
- Once per load, after fonts are ready: the headline rises letter by letter (Serega Gentle), the gymnast's free leg rises from the hip (1.6 s), "fire." lands with a spring accent (Serega Emotional) as the leg nears the top, then the paragraph, button, and caption rise in.
- With reduced motion, everything is in place at once. If the script fails to load, the text appears after 4 s and the leg rises after 2.5 s.

## 7. Coaches and Safety

A section after "More than movement". Two coach entries: a gray photo placeholder, "[Coach name]", "[Credentials]", and a one-line bio `[confirm: question 14]`. A trust row: "National judge, USA Gymnastics (founder)" and "USA Gymnastics member club". Certifications (SafeSport, CPR) aren't shown on the site; they're shared on a parent's request. The section has `data-requires-content` and stays hidden on the live site until the client sends bios.

## 7.1 Finale

The "Let's light the spark" section and the footer form one dark stage with a glow. The section holds a line about booking, the Book a Trial button, and an email link. With JS running, the separate light booking section `#trial` is hidden and booking happens in the dialog; without JS it stays as the fallback form.

At the bottom of the footer stands the "team": a row of light silhouettes of girls with a ball, hoop, clubs, and rope (12 on desktop, 6 on mobile; sprite `assets/gymnast/team.svg`, an illustration, not photos). The satin ribbon is strung like a garland between the sticks of the two end girls. As the footer scrolls in, the girls rise in one by one and the ribbon draws from right to left.

## 8. FAQ

An accordion built on `<details>`: each question opens and closes on its own, and the first one starts open. Works without JS.

## 9. What Could Change This Behavior

- The real trial slots and the Stripe account.
- Who translates the Russian and Ukrainian copy.
- The "she/her" tone is the client's call.
