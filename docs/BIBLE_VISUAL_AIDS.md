# Bible visual aids

Bible visual aids are a supplemental, opt-in layer. They never replace the
Scripture text and must not present an AI reconstruction as archaeological
certainty.

This document is the governing spec for **what a visual aid is allowed to look
like**. Codex Image Gen sessions must follow the Art direction section below;
it overrides any older prompt guidance (`historical-scene-v1` is retired — see
[Catalog dispositions](#catalog-dispositions)).

## Art direction — show the stage, not the play

A visual aid is a **reference figure**, the kind of labeled reconstruction
found in a study Bible or on a museum placard. It explains the physical world
a passage assumes — places, structures, objects, routes, practices — so the
reader can picture what is happening. It **never illustrates the event
itself**. The Scripture text stays the only narrator of the story.

The approved house-style example is the annotated Temple-courts image for Acts
3: a wide reconstruction of the outer courts with callout labels for the
Portico of Solomon, the Beautiful Gate, and the Outer Courts, and anonymous
crowds for scale. What it is *not*: a cinematic painting of men carrying the
lame man toward the gate. The first explains the setting the chapter assumes;
the second competes with the text by acting the story out.

### Three gate tests

Every candidate image must pass all three before it is generated, and again at
review:

1. **One-verse-earlier test.** The image must be exactly as accurate one verse
   *before* its anchor as at the anchor. If drawing it required knowing what
   happens in the verse, it is a scene illustration, not an aid — reject.
2. **Label test.** If you cannot attach 3–5 genuinely useful labels (places,
   parts, functions, distances), the verse probably does not need an aid.
3. **Anonymity test.** Deleting every human from the image should barely
   reduce its value. People appear only as small anonymous figures giving
   scale and life — never the passage's named characters, never faces in
   focus.

### Visual language

- **Formats:** wide or elevated establishing reconstruction, architectural
  cutaway, plan/diagram, labeled map or route profile, or object plate.
- **Style:** matte, realistic historical-reconstruction painting; natural
  daylight; neutral documentary tone. One consistent style across the whole
  library so aids read as one system.
- **Never:** cinematic close-ups, dramatic rim lighting, lens flares, glows or
  halos, shallow depth-of-field portrait framing, "movie still" or
  "movie poster" composition, visible emotion as the subject.
- **Annotation layer:** 3–5 callouts (up to 6 on maps and object plates).
  Dark rounded label chips, white text, thin white leader lines pointing at
  the feature — matching the approved Acts 3 reference image. Labels name
  places, parts, functions, or measurements, in five words or fewer. Labels
  never name people and never describe actions. No other text, no watermark.
  Labels are baked in by Codex Image Gen with exact spelling supplied in the
  prompt; any garbled character is an automatic regeneration. Labels are
  English for now — if localization becomes a requirement, switch to a
  clean-plate + programmatic-overlay pipeline rather than per-language bakes.

### People and the divine

- Anonymous, small-scale, incidental figures only.
- Never depict the passage's named characters (no Peter, no Paul, no Mary).
- **Never depict Jesus, God, the Holy Spirit, angels, demons, or any
  heavenly being, in any form, in any aid.**
- Human dignity always: no gore, no nudity, no suffering rendered as
  spectacle. Battles may appear only as maps, positions, or siege
  engineering — never carnage.

### What earns an aid

Anchor verses qualify through the world they assume, not the drama they
contain:

| Category | Examples |
| --- | --- |
| Architecture & spaces | temple courts, house roofs, prisons, tombs, sheepfolds, city walls |
| Objects & material culture | ephod, phylacteries, stone jars, slings, lamps, ships, armor |
| How things worked | threshing, gleaning, fishing methods, money changing, burial practice |
| Geography, routes & maps | Sea of Galilee, Jerusalem–Jericho road, journey and exile maps |
| Scale & measurement | Noah's ark dimensions, tabernacle plan, Solomon's temple, measured visions as plan-view diagrams |

### What never gets an aid

- The event of the passage: miracles in progress, healings, theophanies,
  resurrections, the crucifixion, the transfiguration, Gethsemane, Pentecost
  flames. (An adjacent *setting* can still qualify — the Bethesda pool
  layout, yes; the healing, no.)
- Symbolic and visionary imagery: Revelation's beasts and throne room,
  Ezekiel 1, Daniel 7–8, Zechariah's visions. Never literalize a vision.
  The single exception is the diagram lane: measured architectural visions
  (Ezekiel 40–48) may be rendered as neutral plan-view diagrams, and plain
  geography in visionary books (the seven churches' locations) as maps.
- Doctrine, discourse, genealogy, and poetry in general. (A concrete object
  inside poetry — rod and staff, winnowing fork — may qualify as an object
  plate.)

### Density

Rarity is part of the subtlety. Most chapters get zero aids; a chapter never
gets more than two; a whole book ships with a handful. One image should be
reused across every anchor it serves (the tabernacle cutaway serves Exodus 26,
Exodus 40, and Hebrews 9).

### Captions, certainty, disclaimers

- Captions explain the *thing* ("A portico was a roofed colonnade…"), never
  retell the story beat.
- Keep the `historical_certainty` field and the on-image-sheet disclaimer.
  Where identification is contested (e.g., which gate was "Beautiful"),
  describe by function and say so in the caption; do not present one
  identification as settled.
- Titles name the place or object ("A Capernaum house"), not the action
  ("Digging through the roof").

### Presentation in the reader

Aids must be quiet. The affordance is a small pill/marker near the anchor
verse that opens the sheet on demand — never a full-width interruption card
sitting between verses, and never autoplaying or auto-expanding. Web and
mobile must present the same quiet affordance (POB cross-platform parity).

## Codex Image Gen prompt template (`annotated-reference-v2`)

Fill the slots; keep the rest verbatim. Record `prompt_version:
"annotated-reference-v2"` in the manifest entry.

```text
Annotated reference visual for [REFERENCE]. Do NOT depict the events of this
passage happening; show the [setting/object/route] as it would appear on an
ordinary day.

Subject: [WHAT TO RENDER — e.g., "the outer courts of Herod's Temple,
Jerusalem, early 1st century AD, seen from an elevated viewpoint"].

Composition: [WHAT MUST BE VISIBLE AND FROM WHERE — e.g., "colonnaded portico
running along the right, monumental gold-plated gate at far right, broad open
plaza, city hills in the background"].

Style: matte realistic historical-reconstruction painting, natural daylight,
neutral documentary tone, museum-plate quality. No cinematic lighting, no
glow, no halo, no lens flare, no shallow depth of field.

People: small anonymous figures for scale only; no identifiable individuals,
no faces in focus, no Bible characters, no divine or angelic beings.

Annotations: [N] labeled callouts — dark rounded rectangles with white text
and thin white leader lines pointing at the feature — reading exactly:
1. "[LABEL 1]"
2. "[LABEL 2]"
3. "[LABEL 3]"
Spell labels exactly as given. No other text, numbers, or watermark anywhere.

Historical accuracy: [ERA + CONSTRAINTS — e.g., "Herodian masonry, no Roman
arches in the court, dress of the period"]. Where identification is debated,
keep details generic and plausible; distinguish reconstruction from certainty.
```

## Publish QA checklist

Before an image enters the manifest:

- [ ] Passes one-verse-earlier, label, and anonymity tests.
- [ ] No named characters; no divine or angelic beings; dignity preserved.
- [ ] Every label spelled exactly; no stray text artifacts anywhere in frame.
- [ ] Style matches the library (matte reconstruction, daylight, no drama).
- [ ] Caption explains the thing, not the story; title names place/object.
- [ ] `visual_type`, `historical_certainty`, disclaimer, alt text set;
      alt text describes the figure without narrating the event.
- [ ] Thumbnail still legible at small size.
- [ ] `prompt_version` is `annotated-reference-v2`; image URLs get a bumped
      `?v=` query so CDN caches refresh.

## Pipeline

1. **Select:** start from the curated editorial shortlist in
   [`BIBLE_VISUAL_AID_SHORTLIST.md`](BIBLE_VISUAL_AID_SHORTLIST.md). The
   heuristic queue from `tools/bible_visual_aid_candidates.py` is a
   supplemental discovery net, not a publishing list.
2. **Review:** an editor confirms a visual would clarify the passage, chooses
   the format (reconstruction, cutaway, map, diagram, object plate), fixes
   the label set, and adds historical/source constraints.
3. **Generate:** use Codex Image Gen with the `annotated-reference-v2`
   template. One approved concept produces one final asset; discarded
   variants do not enter the catalog.
4. **Verify:** run the QA checklist above.
5. **Publish:** upload the final image plus a per-book versioned JSON manifest
   under `bible-visual-aids/v1/`. Mobile and web fetch the same public
   catalog.

Generated queues and image binaries are production artifacts and must not be
committed to this translation repository.

```bash
python tools/bible_visual_aid_candidates.py \
  --translation-root translation \
  --out /tmp/bible-visual-aid-candidates.jsonl
```

Each published manifest entry includes a verse range, title, alt text, caption,
image URL, visual type, historical-certainty label, prompt version, generator,
and review timestamp. The reader displays a **Visual aid** pill only when an
approved entry exists, then opens a dismissible full-image sheet with the
caption and reconstruction disclaimer.

## Catalog dispositions

Published `historical-scene-v1` entries (Acts, 2026-08-05) are superseded:

- `act-3-2-beautiful-gate` — **regenerate** as the annotated Temple-courts
  reference image (labels: Beautiful Gate, Portico of Solomon, Outer Courts).
- `act-3-11-solomons-portico` — **replace** with the same shared courts image
  (one asset, two anchors) or a labeled portico detail in house style.
- `act-3-6-8-raised-to-his-feet` — **retire, no replacement.** It illustrates
  the healing itself and fails the one-verse-earlier test by definition.
