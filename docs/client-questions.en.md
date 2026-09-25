# ElyFlame — Questions for the Client

Prepared by Design (Alena K) from the SOW and the market research. Answers from Kiryl and the client came in on September 25, 2026; items marked "Open" still need an answer and stay as placeholders in the design.

## Decisions for Kiryl (PM)

**D1. How deep the trial booking goes in v1.**
- **A. Request.** The parent submits their details, and the academy calls back to confirm a time and take payment. Every competitor works this way. It takes the least effort, but it adds a step, and some parents won't wait for the call.
- **B. Instant booking.** The parent picks a day and a time slot from the schedule, pays $10 online via Stripe, and gets a confirmation right away. This sets us apart from competitors the most. It requires an exact schedule, the client's approval for online payments, and more back-end work.
- **C. Hybrid.** The parent picks a preferred day from the schedule, and the request goes to the academy. Once the academy confirms, the parent receives an email with a $10 payment link (Stripe Payment Link).

Design recommendation: **C** for launch, **B** in phase 2. For parents, C feels almost the same as B, and it doesn't depend on the client setting up online payments by October 12.

**Kiryl's decision:** C, hybrid. The parent fills in the details, picks a day and time, and pays; the request goes to the academy, which confirms it or texts the parent to reschedule. Trial times are fixed but sometimes change for specific reasons; this may change as volume and academy staff grow.

**D2. Analytics.** The SOW doesn't include analytics, and without it we can't measure the main metric: trial bookings. We need to choose a tool (Google Analytics 4, or a cookie-banner-free option like Plausible) and set up events: Book a Trial clicks, form opened, form submitted, class finder used, phone taps, and Get Directions clicks.

**Kiryl's decision:** Google Analytics.

**D3. Where submissions go.** Should trial and contact requests go only to the academy's email, or also to a Google Sheet or CRM so none get lost? Submissions include a child's name and age, so wherever they're stored has to meet the security requirements in the SOW.

**Kiryl's decision:** Academy email + Google Sheet, with a foundation for future Google Drive file uploads.

**D4. Enrollment targets for the site's metrics.** We need three numbers from the client: how many new students the academy needs per month (open spots per program), how many trial lessons happen per month today, and what share of trial families go on to register. The target metrics in the brief and PRD depend on these numbers, and they stay as placeholders until we have them.

**Kiryl's decision:** Target: 5+ new students per month. Trials today: about 1–5 per month; target 10+. About 50% of trial families register.

**D5. Do we need an admin panel for launch?** The SOW includes an admin panel in project 1 (item 11). If trial requests simply arrive by email or in a Google Sheet (see D3), the academy can manage without it at first. If we do build it for launch, design needs to know what it's for, for example viewing trial requests or editing classes and the schedule, since those screens would need to be designed too.

Design recommendation: no admin panel at launch if requests go to email or a Google Sheet.

**Kiryl's decision:** No admin panel at launch. Its future purpose: automatic notifications and reminders for all members, and automatic plus manual payments (Zelle, Stripe, Venmo, PayPal or others).

## Audience and priorities

1. Which group matters most for filling classes right now: parents of 3–5-year-olds (Recreational), parents of girls 6+ heading into competition (Competitive, including transfers from other clubs), or adults and athletes from other sports (Stretching)? Is there a group we've missed?
   **Answer:** RG is the main focus; Stretching is a single weekly class, a benefit for adults and others. The focus is girls 6+ heading into Level 4 and up. Ages 3–4 are less preferred: very young, more care for coaches.
2. In what language do parents usually message you (DMs, email)? Roughly what share of families speak Russian or Ukrainian? The site launches in English only, as in the SOW. Your answer will tell us whether another language version is worth adding in phase 2.
   **Answer:** Academy emails are in English only. The website needs 3 languages: Russian, English, Ukrainian.

## Trial lesson and enrollment

3. Is the trial lesson $10 or free? The SOW says "Cost $10", but the URL is `/free-trial`. If it's paid, does the $10 count toward the first month?
   **Answer:** $10. "Free" in the SOW is a mistake.
4. Can we take the trial payment online (e.g., via Stripe), or is it paid only in person?
   **Answer:** Both, but online through the site is preferred.
5. The level age ranges overlap: Level 3 is 6–7 and Level 4 is 6+. Where should a 6-year-old with no experience go?
   **Answer:** The Head Coach decides after the trial lesson; ages per level are approximate.
6. Registration happens only after the trial. How does the family get from the trial to registration today: does the coach send a link, do they fill in the Adobe form, or something else?
   **Answer:** Manually through the Head Coach: after the trial they send a link to the Adobe form (no practice without it). Payment is collected separately after a reminder from Administration (no practice without payment).
7. Do you already use a platform for tuition and payments (iClassPro, Jackrabbit, etc.), or are you waiting for the 2027 internal portal? This decides where the Register button leads.
   **Answer:** No.

## Pricing and schedule

8. May we publish prices on the site? None of the nearby competitors do, and we see this as a strong advantage for ElyFlame. We need prices per program, the registration fee, and any discounts (e.g., for siblings).
   **Answer:** No. Prices and fees are not public; a parent gets them on request from Administration or the Head Coach.
9. The class schedule per program: days, times, and duration.
   **Answer:** Not publicly disclosed.
10. Office or front-desk hours.
   **Answer:** Calls: Monday–Friday 9 am–10 pm, Saturday 9 am–5 pm, Sunday closed.

## Location

11. Are classes held in the Silk Road International School building at 1250 Radcliffe Rd, Buffalo Grove? The SOW mentions both "Silk Road International School Chicago" and the Buffalo Grove address.
   **Answer:** Only the Silk Road International School building at 1250 Radcliffe Rd, Buffalo Grove.
12. How do families find the entrance, where do they park, and where do they drop off and pick up? Can parents watch the class?
   **Answer:** Entrance, parking, drop-off and pick-up: door #11. Parents can watch the trial lesson only; after that they may not attend practice unless approved by the Head Coach, at an open practice, or when volunteering.
13. The phone number for the site. A third-party directory lists (224) 804-8324. Please confirm.
   **Answer:** Yes, (224) 804-8324.

## Coaches and trust

14. Coach bios and photos: athletic ranks, judging credentials, certifications (SafeSport, CPR), and experience. For the founder: her name as it should appear (Yelizaveta Yuvkhimenko?), her role (founder and head coach?), 2–3 lines about her approach, and a portrait. For each other coach: name, role, one line of specialization, and a square photo.
   **Answer:** Open.
15. Public records show Yelizaveta Yuvkhimenko on the USA Gymnastics Rhythmic National Judges' List. May we mention this on the site? What does the "P" next to her name in the list mean?
   **Answer:** Yes, mention it. Certifications are not disclosed publicly, only on a parent's request. The meaning of "P" is still open.
16. Is the academy a USA Gymnastics member club? We need confirmation before stating it on the site.
   **Answer:** Yes.
17. Athletes' results: competitions, placements, and years.
   **Answer:** Open.
18. 5–10 parent testimonials with permission to publish (parent's first name and the child's program).
   **Answer:** Open.

## Content and photos

19. Original photos and videos of classes and performances. Instagram images are compressed to about 1080 px, which isn't enough for large sections on desktop.
   **Answer:** Open.
20. Do you have parental consent (a photo release) to publish children's photos on the website? Posting on the club's social media and publishing on the site are different things.
   **Answer:** Yes.
21. Copy: your story and mission, policies (refunds, cancellations, make-ups, code of conduct), FAQ, uniform and equipment requirements, private lesson terms, Privacy Policy, and Terms of Use.
   **Answer:** Open.
22. Photos of the gym and equipment.
   **Answer:** Open.
23. Tagline: do we keep "Where Grace Meets Fire", or do you have your own?
   **Answer:** Keep "Where Grace Meets Fire" for now.

## Minor

24. The SOW footer says "© 2027", but the site launches in 2026. OK to show the current year and update it automatically?
   **Answer:** Yes.

## Children's photos and video (added Sep 25)

The process and the rules are in `docs/photos.en.md`.

25. Does the academy have a signed photo release for every child who will appear on the site, including group shots? Who keeps the list, and who tells us if a parent withdraws consent?
   **Answer:** Open.
26. May we process the children's photos in an outside AI service (Figma Weave: upscaling, light, color; people aren't changed)? The parents consented to publishing, not to processing by a third-party service. If not, we grade the photos locally and don't upscale them.
   **Answer:** Open.
27. Original photos without the logo and the pink background: the Instagram posts have them baked in, and a square crop cuts the logo. We need the camera or phone originals, at least 1600 px on the long side.
   **Answer:** Open.
28. A video for the "On the carpet" band: a silent 10–20 s clip of a performance or a class, 16:9, 720p, no text on screen, MP4 and WebM up to 3 MB each (or the source file, and we encode it).
   **Answer:** Open.
29. Do you confirm illustrations instead of a photo or video in the hero and the footer (a gymnast silhouette and a row of silhouettes)? SOW 3.1 asks for a full-width photo or video in the hero; real photos go to the gallery.
   **Answer:** Open.

## Recommendation

**The current site at elyflame.com.** The domain runs a WordPress site with a single "Hello world!" post. On the post page (https://elyflame.com/?p=1), the owner's personal email is visible in the author byline and in the author page URL. If that isn't intentional, the post can be deleted or switched to a draft. The issue goes away once the new site replaces WordPress.
