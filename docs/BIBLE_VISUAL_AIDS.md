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

### Three teaching-first tests

Every candidate image must pass all three before it is generated, and again at
review:

1. **Teaching-value test.** The image must explain a physical setting, object,
   process, quantity, route, position, or symbol that materially helps the
   reader. Calm anonymous action may be shown when the action itself explains
   how something worked; cinematic reenactment is still rejected.
2. **Label test.** The image needs 3–6 genuinely useful labels (places, parts,
   functions, distances, quantities, or process steps), not decorative copy.
3. **Focus test.** People may demonstrate scale, work, movement, or group
   positions, but the teaching information remains the subject. Avoid named
   characters and faces in focus; never manufacture an authoritative portrait.

### Visual language

- **Formats:** any type in the [taxonomy](#what-earns-an-aid) — annotated
  reconstruction, cutaway, plan/diagram, map or route profile, object plate,
  process plate, naturalist plate, bird's-eye chart, comparison panels,
  timeline, relationship chart, structure infographic, symbol explainer.
- **Style:** two registers, kept consistent within each. *Pictorial* types
  (place, object, how, nature, birdseye) are matte, realistic
  historical-reconstruction painting; natural daylight; neutral documentary
  tone. *Diagrammatic* types (map, scale, compare, timeline, people,
  structure, symbol) use a warm parchment-and-ink palette with clean
  typography and restrained color. Both share the same label-chip annotation
  system so the library reads as one family.
- **Never:** cinematic close-ups, dramatic rim lighting, lens flares, glows or
  halos, shallow depth-of-field portrait framing, "movie still" or
  "movie poster" composition, visible emotion as the subject.
- **Annotation layer:** 3–6 callouts.
  Dark rounded label chips, white text, thin white leader lines pointing at
  the feature — matching the approved Acts 3 reference image. Labels name
  places, parts, functions, measurements, quantities, or short process steps,
  usually in five words or fewer. No other text, no watermark.
  Labels are baked in by Codex Image Gen with exact spelling supplied in the
  prompt; any garbled character is an automatic regeneration. Labels are
  English for now — if localization becomes a requirement, switch to a
  clean-plate + programmatic-overlay pipeline rather than per-language bakes.

### People and the divine

- Anonymous workers, travelers, crowds, armies, and scale figures may be
  prominent enough to explain a process or position, but never portrait-like.
- Avoid depicting the passage's named characters (no authoritative Peter,
  Paul, or Mary portrait); use anonymous role figures when a person is needed.
- **Never depict Jesus, God, the Holy Spirit, angels, demons, or any
  heavenly being, in any form, in any aid.**
- Human dignity always: no gore, no nudity, no suffering rendered as
  spectacle. Battles may appear only as maps, positions, or siege
  engineering — never carnage.

### What earns an aid

Anchor verses qualify through whatever concrete information they leave hard
to picture—not only the world they assume. The taxonomy of aid types (expanded
2026-08-12 for the abundant catalog — see [Density](#density)):

| Type key | Aid type | What it is | Examples |
| --- | --- | --- | --- |
| `place` | Place reconstruction | Annotated matte reconstruction of a built place or space | temple courts, house roofs, prisons, tombs, sheepfolds, city walls |
| `map` | Map / route | Cartographic map, journey route, or terrain profile | Sea of Galilee, Jerusalem–Jericho road, exile and missionary maps |
| `object` | Object plate | Museum-style plate of an object, garment, tool, coin, or unit | ephod, phylacteries, stone jars, slings, lamps, ships, armor, denarius |
| `how` | How it worked | Process plate or step diagram of a practice or trade | threshing, gleaning, fishing methods, money changing, burial, sacrifice procedure |
| `scale` | Scale & measurement | Measured diagram with modern units and a human for scale | Noah's ark, tabernacle plan, Solomon's temple, ten thousand talents |
| `nature` | Naturalist plate | Field-guide plate of a plant, animal, or phenomenon | mustard plant, wheat vs. darnel, locust stages, hyssop, sycamore |
| `birdseye` | Bird's-eye scene | Elevated wide view of a setting with the story's positions marked by labeled markers and arrows — never by depicting the actors | Valley of Elah, the siege of Jerusalem, the storm route to Malta |
| `compare` | Side-by-side | Two- or three-panel comparison of things the verse contrasts | new wine/old wineskins, house on rock/sand, narrow/wide gate |
| `timeline` | Timeline / sequence | Ordered strip of dates, reigns, hours, or steps | kings of Israel and Judah, the hours of the crucifixion day, seventy weeks |
| `people` | Who's who | Relationship, succession, or genealogy chart with named nodes and neutral silhouettes | Herod's family, the twelve, the tribes, the priestly line |
| `structure` | Structure of the passage | Typographic infographic of a list, parallel, chiasm, or argument | Beatitudes, fruit of the Spirit, the armor of God, the Ten Commandments |
| `symbol` | Symbol explainer | Labeled diagram explaining what each element of a symbolic image stands for — clearly schematic, never a literal scene | the seven lampstands, Daniel's statue, Ezekiel's temple plan |

The first five are the original reference-figure lanes; the rest were added
so the catalog can go wider without becoming cinematic. Every type still
passes the teaching-first tests: the bird's-eye scene may chart anonymous
positions and movement, the symbol explainer diagrams rather than literalizes,
and who's-who charts use neutral silhouettes rather than invented portraits.

### What never gets an aid

- Sensational or devotional reenactments of miracles, healings, theophanies,
  resurrections, the crucifixion, the transfiguration, Gethsemane, or Pentecost
  flames. Their settings, mechanics, routes, positions, and material context
  may qualify when presented as teaching diagrams rather than sacred cinema.
- Symbolic and visionary imagery: Revelation's beasts and throne room,
  Ezekiel 1, Daniel 7–8, Zechariah's visions. Never literalize a vision.
  Schematic diagram lanes are allowed: measured architecture, scale diagrams,
  symbol relationships, and plain geography may be rendered without turning
  a vision into a photorealistic scene.
- Doctrine, discourse, genealogy, and poetry in general. (A concrete object
  inside poetry — rod and staff, winnowing fork — may qualify as an object
  plate.)

### Density

**Direction (2026-08-12): step up toward abundance.** The original doctrine
was rarity — a handful per book. The absolute set shipped as catalog v3; the
curated Wave 2 expansion shipped on 2026-08-16 as catalog v4. Teaching-first
Waves 3–36 now ship as catalog v29 (**320 unique assets, 457 placements across
53 books**). Zack's direction is now that aids should be plentiful wherever they
genuinely help, stepping up in tiers rather than
flooding at once. Subtlety is preserved by the affordance (the wrapped verse
number costs nothing when unopened), not by scarcity.

The tiers come from `tools/bible_visual_aid_map.py`, which scores every
canonical verse and caps anchors per chapter. Counts are anchors (verse
placements), not unique images — reuse brings the image count down.

| Tier | Settings | Anchors | Coverage | What it feels like |
| --- | --- | --- | --- | --- |
| Shipped (v29) | absolute set + curated Waves 2–36 | 457 | 1.5% | a teaching layer across 53 books |
| **Wave A — next broad step** | published exclusions + editorial dispositions | ~454 new (+457 shipped) | 2.9% | roughly one aid every chapter or two |
| Wave B | `--min-score 5 --per-chapter-cap 2` | ~1,400 | 4.5% | one to two per chapter in narrative books |
| Wave C (abundant) | `--min-score 5 --per-chapter-cap 3` | ~1,800 | 5.8% | most chapters have an aid; dense chapters have several |
| Ceiling | `--min-score 4 --per-chapter-cap 4` | ~3,500 | 11% | picture-book territory — do not ship |

Catalog v17's contextual-caption update is now live. The refreshed map remains an
editorial queue, not an auto-generation list; it lives at
`~/Documents/New project/output/bible-visual-aid-map/wave-a-v29-reviewed/`
beside the Codex publish staging tree, with
`published_anchor_ids-v29.json` and the cumulative
`editorial-dispositions.json` one level up. Review every row against the
teaching-first tests before generation, then read `pob_visual_aid_opened`
analytics by aid type before deciding
whether Wave B or C is worth it. Pass `--exclude-ids` with the current
published anchor set on every rerun so the queue proposes only new
placements. Per-chapter caps stay in place at every
tier: no chapter becomes a picture book. One image is still reused across
every anchor it serves (the tabernacle cutaway serves Exodus 26, Exodus 40,
and Hebrews 9).

### Captions, certainty, disclaimers

- Every caption answers **why this image helps with the Scripture placement**.
  Lead with the reference and explain the concrete connection to the passage:
  the setting, movement, object, practice, quantity, position, or wording that
  becomes clearer. For example, the John 13 dining-layout caption explains how
  reclining on the left side allowed the disciple beside Jesus to lean back
  toward his chest and ask the question in verses 24–25.
- Explain enough of the story or verse context to make the image's relevance
  obvious, while still letting Scripture narrate the event. Do not merely name
  what the image contains.
- Reader copy must never expose image-generation or editorial instructions such
  as "diagram only," "no people," "published," "map lane," or "flagged for
  editorial care." Those constraints belong in production metadata, not the
  caption.
- Reused images need placement-specific wording whenever the reason they help
  changes. A reclining-table diagram, for example, explains physical proximity
  in John 13 but banquet arrangement in Luke 5 and Matthew 22.
- Keep the `historical_certainty` field and the compact on-image-sheet
  disclaimer: "Visual details may be interpreted or created. Artist
  reconstruction."
  Where identification is contested (e.g., which gate was "Beautiful"),
  describe by function and say so in the caption; do not present one
  identification as settled.
- Titles name the place or object ("A Capernaum house"), not the action
  ("Digging through the roof").

### Presentation in the reader

Aids must be invisible until sought. The affordance is the **verse number
itself**: when a verse anchors an aid, its superscript number is wrapped in a
small rounded chip — white in light mode; in dark mode a subtly elevated
surface tone from the reader theme, never white. Tapping the wrapped number
opens the sheet. Nothing else is added to the reading column: no inline pills,
no cards, no extra rows between verses, no auto-expansion. The chip keeps the
verse number legible in its normal accent color, carries an accessible label
naming the aid, and gets a comfortable tap target. Web and mobile must present
the same affordance (POB cross-platform parity).

## Codex Image Gen prompt templates

`annotated-reference-v2` remains valid for pure setting and object plates.
Use `teaching-first-v1` when anonymous activity, positions, quantities, or a
schematic vision element materially improves comprehension. It follows the
same visual system, but replaces “do not depict the event” with: “teaching
clarity comes first; calm anonymous action or position markers are allowed,
but do not create a dramatic cinematic reenactment.” Record the selected
version in each manifest entry.

### `annotated-reference-v2`

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

- [ ] Passes the teaching-value, label, and focus tests.
- [ ] No named characters; no divine or angelic beings; dignity preserved.
- [ ] Every label spelled exactly; no stray text artifacts anywhere in frame.
- [ ] Style matches the library (matte reconstruction, daylight, no drama).
- [ ] Caption explains why the aid helps with this exact Scripture placement;
      reused placements have context-specific copy where needed.
- [ ] No prompt/editorial notes appear in reader copy (`diagram only`, `no
      people`, `published`, lane names, generation constraints, and similar).
- [ ] Title names the place/object/concept rather than dramatizing the action.
- [ ] `visual_type`, `historical_certainty`, disclaimer, alt text set;
      alt text describes the figure without narrating the event.
- [ ] Thumbnail still legible at small size.
- [ ] `prompt_version` is `annotated-reference-v2` or `teaching-first-v1`;
      image URLs get a bumped `?v=` query so CDN caches refresh.

## Pipeline

1. **Select:** the curated shortlist in
   [`BIBLE_VISUAL_AID_SHORTLIST.md`](BIBLE_VISUAL_AID_SHORTLIST.md) is the
   shipped absolute set. For the abundant waves, run
   `tools/bible_visual_aid_map.py` against the compiled reader corpus at the
   wave's tier settings; its per-book `books/*.json` output is the editorial
   queue (each row carries aid type, format, working title, cues, and a
   typed prompt). `tools/bible_visual_aid_candidates.py` is the older,
   narrower discovery net and is superseded by the map for selection.

   ```bash
   python tools/bible_visual_aid_map.py \
     --books-root ../cartha.website/public/bibles/pob/books \
     --out-dir /tmp/bible-visual-aid-map --min-score 6 --per-chapter-cap 2
   ```
2. **Review:** an editor confirms a visual would clarify the passage, chooses
   the format (reconstruction, cutaway, map, diagram, object plate), fixes
   the label set, and adds historical/source constraints.
3. **Generate:** use Codex Image Gen with the `annotated-reference-v2`
   template. One approved concept produces one final asset; discarded
   variants do not enter the catalog.
4. **Verify:** run the QA checklist above.
5. **Publish:** build the per-book manifests with the canonical production
   tooling in `zackseyun/cartha-music-production/bible_visual_aids/`, then
   upload the final image plus versioned JSON under `bible-visual-aids/v1/`.
   Its tests require every placement to carry a contextual "Why this helps"
   caption and reject production-note language. Mobile and web fetch the same
   public catalog.

Generated queues and image binaries are production artifacts and must not be
committed to this translation repository.

```bash
python tools/bible_visual_aid_candidates.py \
  --translation-root translation \
  --out /tmp/bible-visual-aid-candidates.jsonl
```

Each published manifest entry includes a verse range, title, alt text, caption,
image URL, visual type, historical-certainty label, prompt version, generator,
and review timestamp. An entry may also carry an `images` array (each item:
`image_url`, `thumbnail_url`, `alt_text`) when one anchor benefits from more
than one figure — e.g., a labeled overview plus an interior view (Acts 3:11).
The sheet renders them stacked in order under the entry's single caption;
`image_url` stays set to the first figure for single-image clients. The reader displays a **Visual aid** pill only when an
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
