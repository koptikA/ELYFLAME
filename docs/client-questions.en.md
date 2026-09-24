# ElyFlame — Questions for the Client

Prepared by Design (Alena K) from the SOW and the market research. The questions are ordered by priority. Every unanswered item becomes a placeholder in the design.

## Urgent

**A personal contact is exposed on elyflame.com.** The domain currently runs an empty WordPress site with a single "Hello world!" post (https://elyflame.com/?p=1), and the post shows the owner's personal email address as its author. Please change the author's display name in WordPress or delete the post before launch. The issue goes away once the new site replaces WordPress.

## Decisions for Kiryl (PM)

**D1. How deep the trial booking goes in v1.**
- **A. Request.** The parent submits their details, and the academy calls back to confirm a time and take payment. Every competitor works this way. It takes the least effort, but it adds a step, and some parents won't wait for the call.
- **B. Instant booking.** The parent picks a day and a time slot from the schedule, pays $10 online via Stripe, and gets a confirmation right away. This sets us apart from competitors the most. It requires an exact schedule, the client's approval for online payments, and more back-end work.
- **C. Hybrid.** The parent picks a preferred day from the schedule, and the request goes to the academy. Once the academy confirms, the parent receives an email with a $10 payment link (Stripe Payment Link).

Design recommendation: **C** for launch, **B** in phase 2. For parents, C feels almost the same as B, and it doesn't depend on the client setting up online payments by October 12.

**D2. Analytics.** The SOW doesn't include analytics, and without it we can't measure the main metric: trial bookings. We need to choose a tool (Google Analytics 4, or a cookie-banner-free option like Plausible) and set up events: Book a Trial clicks, form opened, form submitted, class finder used, phone taps, and Get Directions clicks.

**D3. Where submissions go.** Should trial and contact requests go only to the academy's email, or also to a Google Sheet or CRM so none get lost? Submissions include a child's name and age, so wherever they're stored has to meet the security requirements in the SOW.

**D4. Enrollment targets for the site's metrics.** We need three numbers from the client: how many new students the academy needs per month (open spots per program), how many trial lessons happen per month today, and what share of trial families go on to register. The target metrics in the brief and PRD depend on these numbers, and they stay as placeholders until we have them.

## Audience and priorities

1. Which group matters most for filling classes right now: parents of 3–5-year-olds (Recreational), parents of girls 6+ heading into competition (Competitive, including transfers from other clubs), or adults and athletes from other sports (Stretching)? Is there a group we've missed?
2. In what language do parents usually message you (DMs, email)? Roughly what share of families speak Russian or Ukrainian? The site launches in English only, as in the SOW. Your answer will tell us whether another language version is worth adding in phase 2.

## Trial lesson and enrollment

3. Is the trial lesson $10 or free? The SOW says "Cost $10", but the URL is `/free-trial`. If it's paid, does the $10 count toward the first month?
4. Can we take the trial payment online (e.g., via Stripe), or is it paid only in person?
5. The level age ranges overlap: Level 3 is 6–7 and Level 4 is 6+. Where should a 6-year-old with no experience go?
6. Registration happens only after the trial. How does the family get from the trial to registration today: does the coach send a link, do they fill in the Adobe form, or something else?
7. Do you already use a platform for tuition and payments (iClassPro, Jackrabbit, etc.), or are you waiting for the 2027 internal portal? This decides where the Register button leads.

## Pricing and schedule

8. May we publish prices on the site? None of the nearby competitors do, and we see this as a strong advantage for ElyFlame. We need prices per program, the registration fee, and any discounts (e.g., for siblings).
9. The class schedule per program: days, times, and duration.
10. Office or front-desk hours.

## Location

11. Are classes held in the Silk Road International School building at 1250 Radcliffe Rd, Buffalo Grove? The SOW mentions both "Silk Road International School Chicago" and the Buffalo Grove address.
12. How do families find the entrance, where do they park, and where do they drop off and pick up? Can parents watch the class?
13. The phone number for the site. A third-party directory lists (224) 804-8324. Please confirm.

## Coaches and trust

14. Coach bios and photos: athletic ranks, judging credentials, certifications (SafeSport, CPR), and experience.
15. Public records show Yelizaveta Yuvkhimenko on the USA Gymnastics Rhythmic National Judges' List. May we mention this on the site? What does the "P" next to her name in the list mean?
16. Is the academy a USA Gymnastics member club? We need confirmation before stating it on the site.
17. Athletes' results: competitions, placements, and years.
18. 5–10 parent testimonials with permission to publish (parent's first name and the child's program).

## Content and photos

19. Original photos and videos of classes and performances. Instagram images are compressed to about 1080 px, which isn't enough for large sections on desktop.
20. Do you have parental consent (a photo release) to publish children's photos on the website? Posting on the club's social media and publishing on the site are different things.
21. Copy: your story and mission, policies (refunds, cancellations, make-ups, code of conduct), FAQ, uniform and equipment requirements, private lesson terms, Privacy Policy, and Terms of Use.
22. Photos of the gym and equipment.
23. Tagline: do we keep "Where Grace Meets Fire", or do you have your own?

## Technical

24. Is the Instagram account `elyflamerg_yuvkhimenko` a Business or Creator account? A live feed on the site needs one of these. For launch, we propose a curated gallery plus a "Follow" button, with the live feed in phase 2.
25. Who manages the elyflame.com domain and the WordPress hosting right now? We need access for the migration.

## Minor

26. The SOW footer says "© 2027", but the site launches in 2026. OK to show the current year and update it automatically?
