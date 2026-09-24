# PRD: ElyFlame Academy of Rhythmic Gymnastics Website

Written September 24, 2026, with the `/prd` command from `outputs/brief.en.md` and `outputs/research.en.md` (a synthesis of the full research in `docs/research/2026-09-24-market-research.md`). Updated September 25, 2026, with the answers from Kiryl and the client (`docs/client-questions.en.md`). Markers: `[confirm: …]` means data we don't have yet; *[hypothesis]* is a conclusion from the research that the client hasn't confirmed. Decisions are in `docs/decisions.en.md`; site behavior is in `docs/behavior-spec.en.md`.

## What It Is

A phone-first website in three languages for a rhythmic gymnastics academy in Buffalo Grove, where parents find the right class for their child's age and experience, pick a trial lesson time, and pay for it ($10).

---

## Target Audience

The core group is parents of girls 6+ in Buffalo Grove and the neighboring northwest Chicago suburbs who want a competitive path (Level 4 and up), including families ready to move from another club. The second is parents of 3–5-year-olds: there are classes for them, but the academy enrolls them more carefully. The third is teens and adults from other sports coming to the weekly Stretching & Flexibility class. Parents open the site on a phone, arriving from Instagram or Google Maps; families speak English, Russian, and Ukrainian.

---

## Core Problem

*[hypothesis]* Finding a gym is easy: schools show up on Google Maps and Instagram, and families will drive 18 miles for a good coach. Trusting one is hard when there's little information. The nearest competitors (Rhythmix, AP Rhythmic Academy, North Shore Rhythmics, Vitrychenko) bury their trial in text or handle it as "leave a request and we'll contact you," and none of them explain the path for a beginner.

A parent of a competitive girl is choosing between clubs and fears a toxic culture and hidden costs: a review of one competitor literally says "abnormally strong obsession with money." A parent of a little one worries the child will feel out of place. After the Larry Nassar scandal, child safety is a sensitive topic in American gymnastics, and parents hold two stereotypes about Eastern European coaching at once: "it gets results" and "it's too harsh."

---

## Key Use Cases

1. **Find a class and book a trial** (primary). The parent enters the child's age and experience in the Champion's Path, sees the matching level, and taps Book a Trial. In the form they pick a trial day and time and pay $10 online (or choose to pay at the academy). The academy confirms the time or texts them to reschedule.
2. **Learn about the school to build trust.** Coaches; the founder is a USA Gymnastics national judge; the academy is a USA Gymnastics member club; the path from level 1 to competition, achievements, and reviews. Coach certifications are shared on request.
3. **Prepare for the first class and get in touch.** Entrance, parking, drop-off and pick-up at door #11; parents can watch the trial lesson only. Tap-to-call (224) 804-8324, call hours, Get Directions, FAQ, and the contact form.
4. **Find the Stretching class.** An adult or an athlete from another sport sees the weekly class and books through the same trial flow.
5. **Know what happens after the trial.** The FAQ explains that the Head Coach sends the registration form, and the child starts once the form and first payment are done. There's no registration on the site.

---

## Competitive Landscape

- **Rhythmix Inc.** (Buffalo Grove) — the main rival in "Buffalo Grove" searches: 4.9★ from 30 Google reviews, a coaching family with a 30-year history, a clear level pathway. No prices or schedule, and the trial is buried in the program text.
- **AP Rhythmic Academy & Stretching Studio** (Wheeling) — positioned almost exactly like ElyFlame: kids from age 3, levels up to 6+, Stretching in the name, a free trial. The most modern competitor site, but after the form it's manual back-and-forth.
- **North Shore Rhythmics** (Glenview, Deerfield) — the strongest brand: Tokyo 2020 Olympians and the "2024 USA Gymnastics Rhythmic Coaches of the Year." A beginner can't tell where to start.
- **Chicago Rhythmics** (Chicago) — transparency: prices, a paid $15 trial in three steps, safety up front. The whole process is manual: email, Zelle or PayPal, PDF forms.
- **Queen RG Club** (Lake Barrington) — the only one with online trial booking through a calendar; coaches are barely visible.

**The gap we close.** No local competitor has an age-based class finder, and none takes a parent from "which class fits" to a paid trial in one flow. ElyFlame closes this with the Champion's Path and booking with a time slot and online payment. Around it: one primary CTA, the founder's judging credentials and USA Gymnastics membership, a first-visit page, and three languages that no competitor offers. Program prices aren't published, per the client's decision.

---

## MVP Scope

| Screen / feature | Description | MoSCoW |
|---|---|---|
| Header and footer | One primary button, Book a Trial, always on screen on mobile. Footer: contacts, call hours, links, social, Privacy and Terms. No Register or Login until the portal | Must |
| Three languages | English, Russian, Ukrainian: separate URLs `/`, `/ru/`, `/uk/`, a switcher in the header, `hreflang` `[confirm: who translates and proofreads]` | Must |
| Champion's Path class finder | Age and experience → level 1–6 → Book a Trial with the program preselected. The Head Coach sets the final level | Must |
| Book a Trial form | A modal from any Trial button plus the `/trial` page. SOW 4.2 fields + trial day and time + payment method. Errors next to fields, an error summary, works without JS | Must |
| Trial payment | $10 online via Stripe at booking; a "pay at the academy" option | Must |
| Emails and Google Sheet | The request goes to the academy's email and a Google Sheet (with a foundation for Google Drive); the parent gets a confirmation | Must |
| Program config | Programs, ages, and trial times in one file | Must |
| Home | Hero with the gymnast illustration, class finder, Why Choose Us, contacts, dark finale | Must |
| Coaches and trust | Coach cards, "National judge, USA Gymnastics", "USA Gymnastics member club". Certifications on request | Must |
| Contact | Tap-to-call and tap-to-email, address, map and Get Directions, call hours, door #11, contact form | Must |
| Analytics | Google Analytics 4: Book a Trial, form open and submit, payment, class finder use, phone taps, Get Directions | Must |
| SEO and accessibility | Title and meta, OG, sitemap, robots, `SportsClub` JSON-LD, WCAG 2.1 AA, mobile Lighthouse ≥ 90 | Must |
| Legal | Privacy Policy and Terms of Use; the client provides the text | Must |
| About | The sport, why ElyFlame, history and mission, the facility, achievements | Should |
| Parents' Info | FAQ, first class, policies, uniform and equipment, private lessons, what happens after the trial | Should |
| Stretching | One page about the weekly class | Should |
| Testimonials | 3–6 reviews with the parent's name and the child's program | Should |
| Post-trial email | A link to leave a Google review | Should |
| Footer team | Gymnast silhouettes with apparatus and the ribbon strung between two sticks | Could |
| Registration on the site | Registration goes through the Head Coach and the Adobe form | Won't |
| Admin panel | Not needed at launch (D5); later for notifications, reminders, and payments | Won't (for now) |
| Program prices and schedule | Not published; on request only | Won't |
| Parent portal `app.elyflame.com` | Separate project 2, around January 1, 2027 | Won't (for now) |
| Live Instagram feed | Phase 2; needs a server-side function | Won't (for now) |

**Launch minimum for October 12, 2026:** at least one coach with a photo and bio, the address and phone number, six or more real photos, and copy in all three languages.

---

## MVP Success Metrics

- **Primary.** Trial lessons from the site: 10 or more a month (1–5 today).
- **Academy goal.** 5 or more new students a month at roughly 50% conversion after the trial; the academy counts registrations.
- **Mobile visitor-to-request conversion.** The first month in Google Analytics sets the baseline.
- **Share of requests through the class finder:** at least 50%.
- **Share of trials paid online** — growing month over month.
- **Google reviews:** 30 or more by January 12, 2027.

A mobile Lighthouse score of 90+ is an SOW acceptance criterion, not a metric.

---

## Open Questions

**For Kiryl and the client:**
- Who translates and proofreads the Russian and Ukrainian copy.
- The Stripe account: who owns it, where the money goes, how the $10 is refunded on cancellation.
- Who owns the Google Sheet and Google Analytics, and who gets access.
- The real trial days and times per program.
- Confirm illustrations instead of photos in the hero and footer (departs from SOW 3.1).

**For the client** (numbers follow `docs/client-questions.en.md`):
- 14. Coach bios and photos.
- 15. What the "P" next to the judge's name means.
- 17–18. Athletes' results and parent testimonials.
- 19, 21–22. Original photos and videos, copy (history, policies, FAQ, uniform, private lessons, Privacy, Terms), facility photos.
