# Bible visual aids

Bible visual aids are a supplemental, opt-in layer. They never replace the
Scripture text and must not present an AI reconstruction as archaeological
certainty.

This document is the governing spec for **what a visual aid is allowed to look
like**. Codex Image Gen sessions must follow the Art direction section below;
it overrides any older prompt guidance (`historical-scene-v1` is retired — see
[Catalog dispositions](#catalog-dispositions)).

## Art direction — two complementary lanes

A visual aid may be either a **reference figure** or an opt-in **narrative
reconstruction**. Reference figures are the labeled reconstructions found in a
study Bible or on a museum placard: they explain the physical world a passage
assumes — places, structures, objects, routes, practices — without acting out
the event. Narrative reconstructions help a reader picture a passage whose
positions, participants, or emotional setting are otherwise difficult to hold
together. They may show the event, but must remain visibly interpretive rather
than presenting invented details as history, portraiture, or doctrine.

Both lanes are supplemental. Scripture remains the narrator, and every sheet
retains the artist-reconstruction disclaimer. Prefer the reference lane when
the setting or object is sufficient; use the narrative lane only when seeing
the described moment adds material teaching or comprehension value.

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
2. **Clarity test.** A reference figure needs 3–6 genuinely useful labels
   (places, parts, functions, distances, quantities, or process steps), not
   decorative copy. A narrative reconstruction normally has no baked-in text;
   its composition must make the verse's key relationship immediately clear.
3. **Focus test.** People may demonstrate scale, work, movement, group
   positions, or a passage-described relationship, but the teaching information
   remains the subject. Narrative figures must not become authoritative
   portraits; use restrained facial specificity and composition.

### Verse-picture and literary-form gate

Before those three tests, every placement must pass a stricter semantic gate:

1. **Actual verse picture.** The aid must clarify what the anchor verse is
   actually describing, not merely a noun or nearby idea that happened to match
   discovery cues.
2. **Literary form.** A metaphor, parable, prophetic image, vision, or analogy
   must be identified as such in the caption. A realistic reconstruction must
   never make figurative language look like a historical event.
3. **Reuse validity.** Reusing an asset requires a fresh target-verse review for
   location, era, people, action, and literary function. A valid primary image
   may still be false or anachronistic at another anchor.
4. **No interpretive smuggling.** Debated identifications and reconstructions
   must be qualified; popular background theories are not treated as facts the
   verse supplies.

For example, Matthew 3:3 is fulfilled by John preparing people through
preaching and repentance. A realistic road crew filling valleys literalizes
Isaiah's prophetic metaphor and fails this gate. Matthew therefore uses a
narrative reconstruction of John preaching, while Isaiah 40:3–4 uses a clearly
schematic prophetic-metaphor diagram.

### Visual language

- **Formats:** any type in the [taxonomy](#what-earns-an-aid) — annotated
  reconstruction, cutaway, plan/diagram, map or route profile, object plate,
  process plate, naturalist plate, bird's-eye chart, comparison panels,
  timeline, relationship chart, structure infographic, symbol explainer, or
  narrative reconstruction.
- **Style:** three registers, kept consistent within each. *Pictorial* types
  (place, object, how, nature, birdseye) are matte, realistic
  historical-reconstruction painting; natural daylight; neutral documentary
  tone. *Diagrammatic* types (map, scale, compare, timeline, people,
  structure, symbol) use a warm parchment-and-ink palette with clean
  typography and restrained color. *Narrative* scenes use the same matte
  historical-reconstruction register, natural light, restrained emotion, and
  documentary realism, but omit baked-in labels so the scene remains readable.
- **Never:** sensational close-ups, dramatic rim lighting, lens flares, halos,
  fantasy spectacle, "movie poster" composition, or emotion detached from the
  passage's actual wording.
- **Annotation layer:** Reference figures use 3–6 callouts.
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
- Reference figures avoid the passage's named characters; use anonymous role
  figures when a person is needed to explain scale, work, or position.
- Narrative reconstructions may depict people or heavenly beings explicitly
  described in the passage, including Jesus or angels, when their presence is
  essential to comprehension. Keep faces non-authoritative and historically
  plausible; do not imply that appearance, ethnicity, clothing detail, wings,
  halo, or supernatural visual effects are supplied by the text when they are
  not.
- Named recurring figures use the persistent registry at
  `data/bible_visual_aid_character_registry.json`. Jesus is locked to the
  **Sermon on the Mount** video references, Peter to **The True Baptism**, and
  Saul/Paul to **Road to Damascus**. Their exact reference files live in the
  `cartha-video-studio` character cards and must be attached on every
  generation; prose resemblance is not enough. A newly introduced named
  figure gets a card plus stable face and full-body references before a second
  scene is generated. Approved frames may strengthen that card, but an
  existing identity is never silently replaced.
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
| `scene` | Narrative reconstruction | Clearly interpretive, text-free reconstruction of a described moment whose people, positions, or emotional setting materially aid comprehension | the angels at the head and feet of the empty burial place, Ruth approaching the threshing floor, Paul before the Areopagus |

The first five are the original reference-figure lanes; the rest were added
so the catalog can go wider without becoming cinematic. Every type still
passes the teaching-first tests: the bird's-eye scene may chart anonymous
positions and movement, the symbol explainer diagrams rather than literalizes,
and who's-who charts use neutral silhouettes rather than invented portraits.

### What never gets an aid

- Sensational, manipulative, or devotionalized reenactments that add spectacle
  beyond the passage. Miracles, healings, resurrection appearances, the
  crucifixion, the transfiguration, Gethsemane, and Pentecost require heightened
  editorial care, but may qualify as restrained narrative reconstructions when
  the depicted relationship is genuinely helpful and invented details are kept
  visibly interpretive.
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
Waves 3–48 plus Narrative Reconstruction Waves 1–7 and the full semantic audit
now ship as catalog v51 (**420 unique assets, 669 placements across
53 books**). Zack's direction is now that aids should be plentiful wherever they
genuinely help, stepping up in tiers rather than
flooding at once. Subtlety is preserved by the affordance (the wrapped verse
number costs nothing when unopened), not by scarcity.

The tiers come from `tools/bible_visual_aid_map.py`, which scores every
canonical verse and caps anchors per chapter. Counts are anchors (verse
placements), not unique images — reuse brings the image count down.

| Tier | Settings | Anchors | Coverage | What it feels like |
| --- | --- | --- | --- | --- |
| Shipped (v51) | curated Waves 2–48 + Narrative Waves 1–7 + semantic corrections | 669 | 2.1% | audited reference figures and text-grounded scenes across 53 books |
| **Wave A — next broad step** | published exclusions + editorial dispositions | 0 new (+669 shipped) | 2.1% | roughly one aid every chapter or two |
| Wave B | `--min-score 5 --per-chapter-cap 2` | ~1,400 | 4.5% | one to two per chapter in narrative books |
| Wave C (abundant) | `--min-score 5 --per-chapter-cap 3` | ~1,800 | 5.8% | most chapters have an aid; dense chapters have several |
| Ceiling | `--min-score 4 --per-chapter-cap 4` | ~3,500 | 11% | picture-book territory — do not ship |

Catalog v17's contextual-caption update is now live. The refreshed map remains an
editorial queue, not an auto-generation list; it lives at
`~/Documents/New project/output/bible-visual-aid-map/wave-a-v48-reviewed/`
beside the Codex publish staging tree, with
`published_anchor_ids-v48.json` and the cumulative
`editorial-dispositions.json` one level up. Review every row against the
teaching-first tests before generation, then read `pob_visual_aid_opened`
analytics by aid type before deciding
whether Wave B or C is worth it. Pass `--exclude-ids` with the current
published anchor set on every rerun so the queue proposes only new
placements. Per-chapter caps stay in place at every
tier: no chapter becomes a picture book. One image is still reused across
every anchor it serves (the tabernacle cutaway serves Exodus 26, Exodus 40,
and Hebrews 9).

### Narrative reconstruction expansion

`tools/bible_narrative_scene_map.py` is the separate discovery pass for the
scene lane. It scores narrated moments where visible position, movement,
embodied emotion, encounter, or passage-described heavenly participation adds
real comprehension value; it rejects discourse-only and symbolic-vision rows,
flags sensitive scenes for heightened review, and writes text-grounded
`narrative-reconstruction-v2-character-locked` prompts. Named recurring
figures are resolved through the persistent character registry, so the queue
records exact cards and reference files rather than relying on prose
resemblance. It never auto-approves an image.

The current expanded published-text scan lives at
`~/Documents/New project/output/bible-narrative-scene-map/wave-a-v51-character-locked-reviewed/`.
Narrative Wave 1 shipped eight reviewed scenes in catalog v42: Jacob and Esau's
reunion, Joseph listening through an interpreter, Abigail's intercession,
Jehoiakim cutting and burning the scroll, the father welcoming the returning
son, Jesus blessing the children, Dorcas's widows showing her garments, and
the sealing of Daniel's den. Wave 2 adds the Shunammite mother's reunion,
David's fast, Joseph weeping in private, David sparing Saul, the unconsumed
bush, Jesus raising the boy by the hand, Naomi's roadside farewell, and Peter
raising Cornelius. Wave 3 adds Hagar at bowshot distance, Rebekah at the spring,
Ruth at Boaz's feet, Eli awaiting the messenger, Saul's anointing, Naaman in the
Jordan, David mourning Absalom, and Mordecai's public honor in Susa. Catalog
Wave 4 adds Gideon threshing in the winepress, Ananias welcoming Saul, Peter at
the gate, Mary meeting Jesus outside Bethany, Mary and Elizabeth's greeting,
Abraham's three visitors, Josiah hearing the discovered law, and Jonah waiting
east of Nineveh. Wave 5 adds Jairus's plea, Elisha crossing the Jordan, Joseph
reuniting with Israel, Jesus touching the man with a skin disease, Solomon
hearing the two women, Uriah receiving the sealed letter, Moab's red-water
mistake, and Paul's guarded lodging in Rome. Wave 6 adds Joseph reassuring his
brothers, the Syrophoenician mother's plea, Ittai's loyal crossing, Elisha's
acted arrow prophecy, Saul's spear beside David's lyre, Daniel's open-window
prayer, Mordecai at the palace gate, and Paul's garment-shaking gesture. Wave
7 begins the larger identity-consistent expansion with the Transfiguration,
Jesus washing Peter's feet, and Paul in the midst of the Areopagus. Catalog
v51 now contains **53 unique narrative images / 55 narrative placements**.
The refreshed character-locked queue contains 83 high-confidence candidates
after published-anchor proximity and prior dispositions are removed. The
long-term target is roughly 150–250 carefully selected narrative images, so
future editorial passes may add important hand-curated scenes that the text
heuristic misses; neither count is an automatic publication target. The
narrative disposition ledger records 143 rejected candidates and 51
published candidates so neither class can silently re-enter the queue. The
queue count is not a promise to publish every match.

### Full semantic audit

Catalog v44 completed a placement-by-placement audit of the live catalog:

- **632 live placements** received explicit pass or corrected dispositions.
- **95 placements or shared source captions** were corrected for literary form,
  uncertainty, target-specific reuse wording, or reader-copy quality.
- **21 misleading placements** were retired, including anachronistic reuse,
  wrong locations, debated theories presented as settled, and literalized
  prophetic imagery.
- Matthew 3:1–3 now shows John preaching in the wilderness; Isaiah 40:3–4 now
  uses a schematic road-metaphor explainer.

The reproducible check is `tools/audit_bible_visual_aid_semantics.py`. It joins
every catalog row to the published verse text, rejects production language in
reader captions, enforces parable/comparison/vision wording, detects anchor
collisions, and requires a manual disposition for every live placement. The
current ledger and report live beside the publish tree as
`bible-visual-aid-semantic-audit-v48-ledger.json` and
`bible-visual-aid-semantic-audit-v48-final.json`.

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

Use `narrative-reconstruction-v1` when the described participants and their
relationship are themselves the teaching value. These images normally contain
no labels, never claim portrait accuracy, and must not add supernatural visual
details that the passage does not describe.

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

### `narrative-reconstruction-v1`

```text
Narrative reconstruction for [REFERENCE]. Show the passage-described moment in
a restrained, historically plausible way that helps the reader understand
[KEY RELATIONSHIP OR POSITION].

Scene: [SETTING, TIME, AND REQUIRED PHYSICAL CONTEXT].
Participants: [WHO THE TEXT EXPLICITLY DESCRIBES]. Keep faces non-authoritative;
do not invent portrait certainty or supernatural details absent from the text.
Composition: [THE SPATIAL OR EMOTIONAL RELATIONSHIP THAT MUST READ IMMEDIATELY].
Style: matte realistic historical reconstruction, natural light, restrained
emotion, documentary realism; no spectacle, halos, lens flare, or poster drama.
Text: no title, labels, quotation, watermark, or other baked-in text.
Historical care: [ERA, CLOTHING, ARCHITECTURE, AND UNCERTAINTIES].
```

## Publish QA checklist

Before an image enters the manifest:

- [ ] Passes the teaching-value, clarity, and focus tests.
- [ ] Reference figures contain no named characters or heavenly beings;
      narrative figures are text-grounded, non-authoritative, and dignified.
- [ ] Every required reference label is spelled exactly; narrative scenes have
      no stray text artifacts anywhere in frame.
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
