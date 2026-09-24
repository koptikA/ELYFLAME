# Stitch Prompt: ElyFlame Academy of Rhythmic Gymnastics Website

## Product Context
A phone-first website for a rhythmic gymnastics academy in Buffalo Grove, IL. Parents of children aged 3–8 find the right class by their child's age, book a $10 trial lesson, and register after the trial; teens and adults from other sports come for the Stretching & Flexibility class.

## Visual Language
Graceful, energetic, premium, and warm toward parents; never generic or corporate. A restrained light base with lots of whitespace and one signature motif: a thin ribbon line in the brand gradient (magenta #E9008D → orange #FDA63D) that runs through the page and links sections, echoing the ribbon-shaped E in the ElyFlame flame logo. Selected sections are dark (#0D0D0D) like a stage under spotlights, with a soft gradient glow. Headings in Cinzel (short, normal case), body text in Manrope at 16 px or larger. Primary buttons use the gradient with white text kept on the magenta side; secondary buttons are outlined in magenta. Photos show real athletes only, so every image area stays an empty placeholder.

## Screens to Generate
Generate 5 connected screens in one consistent style. Each screen is a separate artboard. Mobile screens are 390 px wide; desktop screens are 1440 px wide with content up to 1200 px. The content is the same in both sizes; desktop differences are listed under Desktop Layout. All interface text is in English.

### Screen 1: Home
- Purpose: a parent arriving from Instagram or Google Maps understands what the academy is, trusts it, and taps Book a Trial.
- Content:
  - Header: logo on the left, a burger menu (Home, About, Parents' Info, Stretching, Contact, and a quiet Login link), and a compact Book a Trial button. No Register button.
  - Hero: the tagline "Where Grace Meets Fire" (placeholder), one line about classes for ages 3+, a "Book a $10 Trial" button, and a secondary text link "Find the right class".
  - Class finder teaser: "How old is your child?" with an age field and a Show button that leads to Screen 2.
  - Why Choose Us: 3–4 cards, each with an icon, a short title, and one line of text.
  - Coaches and safety: 2 coach cards (photo, name, credential line) and a row of safety badges: SafeSport, CPR, USA Gymnastics national judge.
  - Location strip: map, address 1250 Radcliffe Rd, Buffalo Grove, IL 60089, a phone number, hours, and a Get Directions button.
  - "Now Enrolling" banner on a dark stage background with a Book a Trial button.
  - Footer: logo, address, phone, email, hours, page links, Instagram and Facebook, Privacy and Terms.
  - Mobile only: a sticky bottom bar with Book a Trial that stays on screen while scrolling.
- **Visual slots** (leave as empty placeholder areas):
  - Logo_Slot in the header
  - Hero_Photo_Placeholder for an athlete photo or a silent looping video
  - Ribbon_Line_Placeholder: a thin line crossing the page between sections
  - Icon_Slot_1 to Icon_Slot_4 for the Why Choose Us cards
  - Coach_Photo_Slot_1 and Coach_Photo_Slot_2
  - Badge_Slot_1 to Badge_Slot_3 for the safety badges
  - Map_Placeholder
  - Stage_Glow_Background behind the Now Enrolling banner
  - Logo_Dark_Slot in the Now Enrolling banner and Footer_Logo_Slot

### Screen 2: Champion's Path (class finder)
- Purpose: a parent enters the child's age and experience and sees the matching level and program.
- Content:
  - Title and one line: "Find the right class".
  - Age field and experience chips: None, Some rhythmic (recreational), Competitive.
  - Levels 1–6 shown as a vertical path, not a table: Level 1 (age 3, Recreational), Level 2 (4–5, Recreational), Level 3 (6–7, Competitive), Level 4 (6+, Competitive), Level 5 (7+, Competitive), Level 6 (8+, Competitive). The path runs from "first steps at 3" to "serious competition".
  - A spark marker sits on the matching level (show the state for a 4-year-old with no experience: Level 2).
  - Result card next to the marker: program name, age range, apparatus (Rope, Ball), a note that the coach confirms the level at the trial, and a "Book a Trial" button with this program preselected.
- **Visual slots** (leave as empty placeholder areas):
  - Logo_Slot in the header
  - Path_Line_Placeholder for the curved level path
  - Spark_Marker_Slot
  - Apparatus_Icon_Slot_1 to Apparatus_Icon_Slot_5 (rope, ball, hoop, clubs, ribbon)

### Screen 3: Book a Trial (form)
- Purpose: a parent books a trial lesson in under a minute.
- Content:
  - A bottom sheet or full-screen modal over the page, titled "Book a $10 Trial", with a close button.
  - Fields: child's name; child's age; experience (None / Some RG recreational / RG competitive); program (prefilled from the class finder, editable); preferred day (from the program's schedule); parent's name; phone (US format, (XXX) XXX-XXXX); email; a consent checkbox to be contacted.
  - One field shown in an error state: a red message right under the field that says how to fix it, for example "Enter your child's age".
  - Submit button "Book a Trial" with a loading state.
- **Visual slots** (leave as empty placeholder areas):
  - Ribbon_Accent_Placeholder: a short ribbon line in the sheet header

### Screen 4: Trial Booked (confirmation)
- Purpose: the parent sees the request went through and knows what happens next.
- Content:
  - Heading "You're booked!" and the line "We'll contact you within [24 hours] to confirm your trial."
  - Booking summary: child, program, preferred day, parent contact.
  - "What to bring" checklist with 3–4 items.
  - Links to directions and Parents' Info.
- **Visual slots** (leave as empty placeholder areas):
  - Confirmation_Illustration_Placeholder above the heading
  - Icon_Slot_1 to Icon_Slot_4 for the checklist items

### Screen 5: Contact
- Purpose: a parent calls, writes, or finds the way to the first class.
- Content:
  - Tap-to-call phone, tap-to-email academy@elyflame.com, and the address.
  - Map with a Get Directions button.
  - Office and class hours.
  - Parking and drop-off / pick-up notes.
  - Contact form: name, email, phone, message, and a Send button.
  - The same header, footer, and sticky Book a Trial bar as Screen 1.
- **Visual slots** (leave as empty placeholder areas):
  - Logo_Slot in the header
  - Map_Placeholder
  - Icon_Slot_1 to Icon_Slot_4 for phone, email, address, and hours

## Desktop Layout
- Header: logo on the left, the full navigation in one row, a quiet Login link, and the Book a Trial button on the right. The header stays on screen while scrolling, so there is no bottom bar.
- Home: hero text on the left and Hero_Photo_Placeholder on the right; Why Choose Us cards in one row; coach cards side by side; in the location strip, the map on one side and the details on the other.
- Champion's Path: the levels run as a horizontal path across the page, with the result card under the spark.
- Book a Trial: a centered dialog about 560 px wide over a dimmed page; short fields in pairs (child's name and age, phone and email).
- Trial Booked: the booking summary and the What to bring list side by side.
- Contact: the map on one side, the contact details and form on the other.
- Buttons, links, and level chips have hover states.

## Technical Requirements
- Clean, editable layers when exported to Figma.
- 8 px grid.
- The same typography on every screen.
- Every visual placeholder is its own layer with a clear name (Hero_Photo_Placeholder, Icon_Slot_1, Stage_Glow_Background, and so on).
- Buttons and form fields are at least 48 px tall for touch.
- Do not generate photos of people; keep every photo area as an empty placeholder.

## To Confirm
- Phone number and office hours: not confirmed by the client yet.
- The schedule for the "Preferred day" field: not provided yet.
- The "What to bring" list: the client hasn't provided it; use generic items for now.
- Coach names and credentials: not provided yet; use placeholders.
- Booking depth (decision D1): the form is designed for option C (preferred day, confirmation by the academy, then a payment link).
