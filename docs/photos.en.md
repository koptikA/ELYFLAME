# ElyFlame — photos and video

For the team (Kiryl, Ivan, Windy) and, through Kiryl, the client. September 25, 2026. How photos of the students get onto the site: where they go, the rules for children's photos, one visual style, the processing workflow, and the file requirements. Related decisions are in `docs/decisions.en.md`; open questions are 19, 22, and 25–29 in `docs/client-questions.en.md`.

## Status

- Parents have consented to publishing photos on the site (question 20). Written releases for every child in a frame still need confirming (question 25).
- Original photos and video haven't arrived (questions 19, 27, 28). Instagram copies are compressed to about 1080 px, and the logo and pink background are baked in, so a square crop cuts the logo.
- Until the files arrive, the site and Figma show gray placeholders. The blocks carry `data-requires-content`.
- Launch minimum: six or more real photos (brief, PRD).

## Where photos go

| Place | What | Size on the site |
|---|---|---|
| Gallery after "More than movement" | 6 photos of classes and performances | square; 397 px on desktop, 268 px on phones |
| Video band "On the carpet" | a silent 10–20 s background loop | 16:9, up to 1238 px wide |
| Coaches | coach portraits (question 14) | 190 × 190 on desktop, 110 × 170 on phones |
| Later: the gym | the gym and equipment (question 22) | not placed yet |

The hero and the footer stay illustrations: a gymnast silhouette and the "team" of silhouettes. Nobody mistakes an illustration for a student. This departs from SOW 3.1 and needs the client's confirmation (question 29).

## Rules for children's photos

- Only children whose parents signed a written photo release. If a group shot includes a child without one, the shot isn't used. The academy keeps the list of releases.
- If a parent withdraws consent, the photo comes off the site and out of Figma right away.
- No names: alt text describes the scene ("Gymnasts practicing with ribbons") and never names a child, a school, or a class time.
- EXIF metadata, including GPS location, is stripped on export.
- Choose movement, performances, and group shots. Don't use close-ups of bodies, awkward angles in leotards, or changing rooms.
- AI only enhances a photo (upscaling, light, color) and never changes people. We don't generate athletes (decision of Sep 24).
- Processing in an outside AI service (Figma Weave) needs the client's OK: the parents consented to publishing, not to processing by a third-party service (question 26). Without that OK, photos are graded locally and not upscaled.

## One style

1. **Reference.** 2–3 typical shots are graded by hand to the target look: warm white balance, highlights toward the cream of the site background (`--paper`), warm and deep shadows, no oversaturation, natural skin. Alena approves the reference.
2. **Brand layer in code.** On the site, CSS adds the soft brand gradient on top of the photos, and in dark sections the magenta → orange duotone (decision of Sep 24). It's the same for every photo and can be tuned without reprocessing.
3. **Series check.** All processed shots are reviewed side by side as one series before they go live.

## Workflow

| Step | Who | What |
|---|---|---|
| 1. Selection | Alena | Picks shots by the rules above; sharp, at least 1600 px on the long side |
| 2. Processing | Windy builds the Weave workflow; Claude runs it | A published Weave workflow with fixed steps only: upscaling when the shot is small, noise reduction, grading to the reference. No generative steps that could change a face or a body. Claude runs it through the Figma MCP in one batch; every run costs Weave credits and is approved first |
| 3. Review | Claude, then Alena | A before/after page with all shots side by side; check that people haven't changed. Alena gives the final yes |
| 4. Export | Claude | Crop to the slot (1:1 for the gallery), strip EXIF, WebP in three sizes into `assets/photos/`; alt text in EN/RU/UA through `tools/i18n.py` |
| 5. Figma | Alena or Claude | Drop each photo onto its "Photo 1…6" rectangle on both Home pages |
| 6. WordPress | the client, after launch | Uploads any photo into a gallery slot; the site crops it square (`object-fit: cover`) |

To run Weave from here, Alena links her Figma account to Weave once: app.weavy.ai/settings?section=profile.

## Where to put the files

- **Video:** `assets/video/performance.mp4`, `performance.webm`, `performance-poster.jpg`, replacing the placeholders with the same names; the site picks them up. A single source file goes to `assets/video/source/` and gets encoded from there.
- **Photo originals:** `assets/photos/originals/`. The folder is in `.gitignore`: originals keep EXIF and GPS. Processed copies without metadata go to `assets/photos/` and are committed.
- **Figma:** drop a photo onto a "Photo 1…6" rectangle.

## Video

- A silent loop, 10–20 s, 16:9, 720p, no text on screen: MP4 (H.264) and WebM, up to 3 MB each (or the source file, and we encode it).
- A performance or a class, shot steadily, without a logo baked in.
- The poster is the first frame.
- On the site it's a background loop with no controls: it plays only while on screen and stays on the poster with "reduce motion" on (`docs/behavior-spec.en.md`, section 7).
