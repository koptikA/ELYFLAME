# ElyFlame — Creative Concept

Approved by Design on September 24, 2026. Based on the [market research](research/2026-09-24-market-research.md) and the [references](../refs/README.md).

## Concept

The three ideas work together: the Ribbon is the style, the Champion's Path is the mechanic, and the Stage sets the rhythm of each page.

### 1. The Ribbon — signature motif

The E in the ElyFlame mark curls like a ribbon, and the ribbon is one of the apparatus in rhythmic gymnastics. A thin ribbon in the brand gradient (magenta → orange) runs through the whole site. It draws itself as the visitor scrolls and ties the sections together.

- Technique: an SVG path with `stroke-dashoffset` driven by scroll. It runs on plain JS with no libraries and doesn't hurt the Lighthouse score.
- With `prefers-reduced-motion`, the ribbon is a static line.
- References: [CodePen — scroll-controlled line](https://codepen.io/Tonkz/pen/aVrzaR), [Ballerina](https://ballerina-dance.com/) (motion that feels like dance).

### 2. The Champion's Path — core mechanic

Levels 1–6 appear as a path, not a table: from "first steps at age 3" to "serious competition". The class finder lives on this path. A parent enters the child's age and experience, a spark moves to the matching level, and a "Book a Trial" button appears with that program preselected.

- Parents see the long-term journey, not just the next step.
- The research confirms that no local competitor offers an age-based class finder, and only elite clubs (NSR, Vitrychenko) show the path to competition.
- Reference: [CodePen — object moving along a path](https://codepen.io/yesvin/pen/XymwvX).

### 3. The Stage — page rhythm

The base is light, because parents need trust and readability. Selected sections are dark, like a stage under spotlights, with a soft gradient glow:
- achievements;
- the "Now Enrolling" banner;
- performance videos.

The client already has a logo version on black.

- Reference: [Mougins en Danse](https://www.mouginsendanse.fr/) (quiet premium feel, typography-led).

## Additions from the research

1. **Prices on program cards.** None of the nearest competitors publish prices, and negative reviews of one of them complain about an "obsession with money". Present each price with "no hidden fees".
2. **Book a trial in one minute.** Flow: age → time slot → $10 payment → confirmation and a "what to bring" note. Present the $10 as a spot reservation; competitors charge $15–25. Whether it counts toward the first month is the client's call.
3. **"Safety & coaches" section.** The founder is a USA Gymnastics national judge, and a judge knows exactly what earns points. Show SafeSport, CPR, and USAG membership alongside it (membership to be confirmed).
4. **"Your first class" page.** A photo of the entrance to the Silk Road International School building, parking, drop-off, whether parents can watch, and what to bring. It removes first-visit anxiety.
5. **Stretching as its own funnel.** Separate pages and copy for figure skaters, dancers, and adults, with their own search keywords and their own booking button. No competitor does this.
6. **Languages.** Decided on Sept 24: the site launches in English only, as in the SOW. A Russian landing page (`/ru/` with `hreflang`) stays as a phase 2 idea. If we come back to it, the client chooses the languages (Russian, Ukrainian, or both).
7. **Google review requests.** An email or SMS with a review link after the trial and again after 30 days. Reviews are the main driver of local ranking. The target is 30+ reviews, the level Rhythmix has.
8. **A gallery instead of a live Instagram feed** at launch, plus a "Follow on Instagram" button. The live feed moves to phase 2 behind a serverless function, because the Basic Display API has been shut down and the new API requires a token.

## Urgent for the client (via Kiryl)

elyflame.com currently runs an empty WordPress site with a "Hello world!" post, and the post shows the owner's personal email as its author. Change the author's display name or delete the post before launch.
