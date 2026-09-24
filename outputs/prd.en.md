# PRD: ElyFlame Academy of Rhythmic Gymnastics Website

Written September 24, 2026, with the `/prd` command from `outputs/brief.en.md` and `outputs/research.en.md` (a synthesis of the full research in `docs/research/2026-09-24-market-research.md`). Markers: `[confirm: …]` means data we don't have yet; *[hypothesis]* is a conclusion from the research that the client hasn't confirmed. Decisions made along the way are in `docs/decisions.en.md`.

## What It Is

A phone-first website for a rhythmic gymnastics academy in Buffalo Grove where parents find the right class for their child's age, book a $10 trial lesson, and register after the trial.

---

## Target Audience

The core group is parents of children under 8 in Buffalo Grove and the neighboring northwest Chicago suburbs who are looking for a first sport or a stronger program. They open the site on a phone, arrive from Instagram or Google Maps, and decide within 1–3 visits over one or two weeks. The second group is parents of girls 6+ heading into competitive gymnastics, including families ready to move from another club. The third, separate group is teens and adults from other sports who need the Stretching & Flexibility class. The client still has to confirm which group matters most for filling classes `[confirm: question 1]`.

---

## Core Problem

*[hypothesis]* Finding a gym is easy: schools show up on Google Maps and Instagram, and families will drive 18 miles for a good coach. Trusting one is hard when there's little information. None of the nearest competitors (Rhythmix, AP Rhythmic Academy, North Shore Rhythmics, Vitrychenko) publish prices, their trial is buried in text or handled as "leave a request and we'll contact you," and none of them explain the path for a beginner.

Each group has its own fears. A parent of a 3–5-year-old worries the child will feel out of place, the coach will be too strict, or the first visit will end in tears. A parent of a competitive girl fears a toxic culture and hidden costs: a review of one competitor literally says "abnormally strong obsession with money." After the Larry Nassar scandal, child safety is a sensitive topic in American gymnastics. Parents also hold two stereotypes about Eastern European coaching at once: "it gets results" and "it's too harsh."

---

## Key Use Cases

1. **Find a class and book a trial** (primary). The parent enters the child's age and experience in the Champion's Path, sees the matching level, and taps Book a Trial with the program preselected. They fill in a short form and get a confirmation with a "what to bring" checklist. How deep booking goes in v1 depends on a pending decision `[confirm: D1]`.
2. **Learn about the school to build trust.** Coaches and their credentials (the founder is on the USA Gymnastics national judges' list), safety measures, the path from level 1 to competition, athletes' achievements, and parent reviews.
3. **Prepare for the first class and get in touch.** The building entrance, parking, what to wear and bring, whether parents can watch; the FAQ and policies; tap-to-call, Get Directions, and the contact form.
4. **Find the Stretching class.** An adult or an athlete from another sport sees the class is open to them, checks the schedule, duration, level, and price, and books through the same trial flow.
5. **Register after the trial.** From the post-trial email, the "Already had your trial? Register" block on Parents' Info, or the footer, the parent goes to `/register`: parent and child details, class, waiver, first payment. Our own form or an external platform is the client's call `[confirm: question 7]`.

---

## Competitive Landscape

- **Rhythmix Inc.** (Buffalo Grove) — the main rival in "Buffalo Grove" searches. Strengths: 4.9★ from 30 Google reviews, a coaching family with a 30-year history, a clear level pathway. The site has no prices or schedule, and the trial is buried in the program text.
- **AP Rhythmic Academy & Stretching Studio** (Wheeling) — positioned almost exactly like ElyFlame: kids from age 3, levels up to 6+, Stretching in the name, a free trial. The most modern competitor site: a trial CTA above the fold, the schedule in tabs by level, its own tournament, and a uniform shop. No reviews or prices, and after the form it's manual back-and-forth.
- **North Shore Rhythmics** (Glenview, Deerfield) — the strongest brand: Tokyo 2020 Olympians and the "2024 USA Gymnastics Rhythmic Coaches of the Year." A beginner can't tell where to start, and sign-up sends families to park district sites.
- **Chicago Rhythmics** (Chicago) — the best example of transparency: published prices, a paid $15 trial explained in three steps, and safety up front. The whole process is manual: email, Zelle or PayPal, PDF forms.
- **Queen RG Club** (Lake Barrington) — published prices and online trial booking through a calendar. Coaches are barely visible, and the site is a Wix template.

**The gap we close.** No local competitor has an age-based class finder, and no site takes a parent from "which class fits my child" to a booked trial in one flow. ElyFlame closes this gap with the Champion's Path: age → level → Book a Trial with the program preselected. Around it: one primary CTA on every screen, a "coaches and safety" trust block featuring the founder's judging credentials, a first-visit page, and a separate Stretching funnel that competitors don't use. Online trial payment widens the gap if D1 is B or C. The research also names open pricing as a gap, but at launch we publish only the prices in the SOW: the trial and Stretching.

---

## MVP Scope

| Screen / feature | Description | MoSCoW |
|---|---|---|
| Header and footer | One primary button, Book a Trial, always on screen on mobile; a quiet Login link; no Register in the header. Footer: contacts, hours, links, social, Privacy and Terms | Must |
| Champion's Path class finder | Age and experience → level 1–6 → Book a Trial with the program preselected. Cards are built from the config | Must |
| Book a Trial form | A modal from any Trial button plus the `/free-trial` page. Fields per SOW 4.2, errors next to the field, a success screen with a summary and "what to bring," a server error screen, honeypot and rate limit, works without JS | Must |
| Emails after a request | The request to the academy, a confirmation to the parent | Must |
| Program config | Programs, ages, and schedule in one file that feeds the class finder and forms | Must |
| Home | Hero with Book a Trial, class finder, Why Choose Us, a map and contacts strip, the "Now Enrolling" banner | Must |
| Coaches and safety | Coach cards with credentials, SafeSport, CPR, whether parents can watch. Addresses the core pain: trust | Must |
| Contact | Tap-to-call and tap-to-email, address, Google Map and Get Directions, hours, parking and drop-off, contact form | Must |
| Hidden blocks | A block without client content isn't shown; in the mockups each such block has two states | Must |
| Event analytics | Book a Trial, form open and submit, class finder use, phone taps, Get Directions. Without it the metrics can't be measured `[confirm: D2]` | Must |
| SEO and accessibility | Title and meta, OG, sitemap, robots, `SportsClub` JSON-LD, WCAG 2.1 AA, mobile Lighthouse ≥ 90 — SOW acceptance criteria | Must |
| Legal | Privacy Policy and Terms of Use; the client provides the text | Must |
| About | What rhythmic gymnastics is, why ElyFlame, history and mission, the facility, achievements | Should |
| Parents' Info | FAQ, first class, policies, waiver and medical PDFs, uniform and equipment, private lessons, the "Already had your trial? Register" block | Should |
| Stretching | One page with a section per audience: who it's for, schedule, duration, level, price, benefits | Should |
| Testimonials | 3–6 reviews with the parent's name and the child's program | Should |
| Register | `/register` after the trial: parent → child → class → waiver → first payment. The first registrations only come after the first trials, and the format is waiting on the client `[confirm: question 7]` | Should |
| Online trial payment | A Stripe Payment Link in the email after the academy confirms (option C) `[confirm: D1, question 4]` | Should |
| Post-trial email | Links to leave a Google review and to register | Should |
| Gallery | 6–9 treated photos and a "Follow on Instagram" button | Should |
| Admin panel | Part of project 1 per the SOW (item 11). The primary scenario doesn't need it if requests go to email or a spreadsheet `[confirm: D5]` | Could |
| Video | A silent hero video and performance videos in dark sections, if the client sends originals | Could |
| Parent portal `app.elyflame.com` | Separate project 2, launching around January 1, 2027 | Won't (for now) |
| Instant booking with slot and payment (option B) | Phase 2; in the mockups C is nearly identical to B | Won't (for now) |
| Children's program prices | Phase 2, if the client allows publishing them `[confirm: question 8]` | Won't (for now) |
| Live Instagram feed | Phase 2; needs a server-side function for the token | Won't (for now) |
| Russian page `/ru/` | Phase 2 | Won't (for now) |
| Stretching landing pages per audience | Phase 2 | Won't (for now) |

**Launch minimum for October 12, 2026:** at least one coach with a photo and bio, the schedule, the address and phone number, and six or more real photos. We don't launch without them.

---

## MVP Success Metrics

- **Primary.** Trial requests from the site: ≥ `[confirm: monthly target based on open class spots, D4]` in the first month, October 12 to November 12, 2026.
- **Mobile visitor-to-request conversion.** The first month sets the baseline; later targets are set from it.
- **Share of requests through the class finder:** ≥ 50% by November 12, 2026. Validates the Champion's Path mechanic.
- **Share of trial families who complete registration:** `[confirm: current rate, D4]` by November 12, 2026. If Register is our own form, we count submissions; if it's an external platform, the client provides the number.
- **Google reviews:** ≥ 30 by January 12, 2027, matching Rhythmix, the review leader in Buffalo Grove.

Without analytics, the first three metrics can't be measured `[confirm: D2]`. Lighthouse ≥ 90 isn't a metric; it's an SOW acceptance criterion.

---

## Open Questions

**Decisions for Kiryl (PM):**
- D1. Trial booking depth: A — request, B — instant booking and payment, C — hybrid. Design recommends C for launch and B in phase 2.
- D2. Analytics tool and events.
- D3. Where requests go and where a child's data is stored, in line with the SOW's security requirements.
- D4. How many new students the academy needs per month, how many come to trials now, and what share registers.
- D5. Is the admin panel (SOW item 11) needed by October 12 if requests go to email or a spreadsheet?

**For the client** (numbers follow `docs/client-questions.en.md`, which has the full list):
- Recommendation: the owner's personal email is visible in the post author byline on the current elyflame.com.
- 1. Which group matters most for filling classes.
- 3–4. Is the trial paid ($10) or free (`/free-trial`); does the $10 count toward the first month; can we take payment online.
- 5. Where the class finder sends a 6-year-old with no experience: level 3 (ages 6–7) or level 4 (6+).
- 7. Registration: our own form or an external platform.
- 8. Can we publish children's program prices.
- 9–13. Schedule, office hours, class location, entrance and parking, whether parents can watch, phone number.
- 14–18. Coach bios and photos, the "P" judging mark, USA Gymnastics membership, athletes' results, parent reviews.
- 19–22. Original photos and videos, parental photo release, copy (policies, FAQ, Privacy, Terms), facility photos.
