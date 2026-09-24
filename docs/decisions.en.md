# ElyFlame — Decision Log

| Date | Decision | Why | Owner |
|---|---|---|---|
| Sep 24 | Concept: the Ribbon (style), the Champion's Path (class finder mechanic), and the Stage (light base with dark sections), plus 8 additions from the research | Stand out from competitors' template sites; no local competitor has an age-based class finder | Alena |
| Sep 24 | The site is English-only, as in the SOW. A Russian `/ru/` page is a phase 2 idea | Timeline; the core audience speaks English | Alena |
| Sep 24 | Docs are kept in two languages: `name.md` (RU) and `name.en.md` (EN) | Alena works in Russian; the client and team work in English | Alena |
| Sep 24 | Stretching is one page, `/stretching`, with a section per audience. Separate landing pages are phase 2 | Timeline, less copy to produce | Alena |
| Sep 24 | The header has one primary button, Book a Trial, plus a quiet Login link. Register moves out of the header: it's reachable from the post-trial email, an "Already had your trial?" block on Parents' Info, and the footer | Registration only happens after a trial; one primary action (Hick's law); refs KidStrong and Goldfish, anti-ref The Little Gym | Alena (deviates from SOW 3.3) |
| Sep 24 | Photos get one consistent treatment: warm color grade and a soft brand gradient. Dark sections use a magenta → orange duotone applied as a CSS filter | Instagram shots are inconsistent; one treatment turns them into a series | Alena |
| Sep 24 | AI only enhances photos (upscaling, light, color) and never alters people. No AI-generated athletes | The photos show children; the SOW requires "real athlete photos" | Alena |
| Sep 24 | Fonts: Cinzel for headings, Manrope for body text | Cinzel echoes the logo wordmark; Manrope reads well at 16 px on mobile | Alena |
| Sep 24 | We don't use Fluid Functionalism as code. We borrow its state and motion principles, and Fluid Hover only on desktop. Fluid is a good fit for the portal (project 2) | The SOW stack is vanilla; Fluid's sizing is built for dense apps | Alena |
| Sep 24 | Browser features first: `<dialog>`, `<details>`, `scroll-snap`, built-in form validation, and CSS scroll-driven animations. GSAP only if needed. Type and spacing scales come from Utopia | Performance, accessibility, less code | Alena |
| Sep 24 | Prices follow the SOW: $10 for the trial and the price on the Stretching page. Children's program prices aren't published at launch | The client hasn't given prices or permission to publish them (question 8). If they allow it, a pricing block comes in phase 2 | Alena |
| Sep 24 | Blocks without client content are hidden; no "Coming soon" placeholders. In the mockups each such block has two states: with content and hidden. Launch minimum: 1 coach with photo and bio, the schedule, address and phone, 6+ real photos | The October 12 launch doesn't move; an empty placeholder undermines parents' trust | Alena |
| Sep 24 | Success metrics: trial requests per month (main), mobile visitor-to-request conversion, share of requests through the class finder ≥ 50%, trial-to-registration rate, 30+ Google reviews by Jan 12, 2027. Lighthouse ≥ 90 is an acceptance requirement, not a metric | Metrics measure the site's results; the SOW requires Lighthouse for sign-off | Alena |
| Sep 24 | Site behavior is recorded in `docs/behavior-spec.en.md`: a class finder with three states (level 1, level 2, coach assessment for ages 6+ and competitive experience), the program Competitive instead of Competitive assessment, the SOW 4.2 form built for option C, a single Ribbon, and "your child" in functional text | Level ages 3–6 overlap (question 5), so 6+ goes to the coach; forms and copy follow the SOW and GOV.UK | Alena |
| — | Trial booking depth: A (request), B (instant booking), or C (hybrid). Recommendation: C for launch, B in phase 2 | — | **Waiting on Kiryl (D1)** |
| — | Analytics (D2), where submissions go (D3), enrollment targets (D4), admin panel at launch (D5) | — | **Waiting on Kiryl** |

**Headings in HTML.** For Ivan: type headings in normal case ("Our Coaches"), not in all caps. Cinzel already renders lowercase letters as small caps, and screen readers won't spell the text out letter by letter.
