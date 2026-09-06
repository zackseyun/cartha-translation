# Genizah Psalm 145: a located passage, not an omission vote

Date: 2026-09-06. Status: bounded image observation and held source inference;
no canonical change. This follows the [40-hit catalogue pilot](GENIZAH_BIBLICAL_CATALOGUE_PILOT_2026-09-06.md)
and supplements, without rewriting, the [Psalm 145 dossier](PSALM_145_SOURCE_COMPARISON_2026-09-05.md).
The [machine record](../sources/textual_restoration/discovery/genizah_psalm145_abbreviation_check.v1.json)
pins the actual inputs and image requests.

## Result

T-S A43.8 does contain the relevant Psalm 145 region on Cambridge's **second
canvas, labelled 1v**, not the last canvas examined in the pilot. In the
right-hand leaf's inner/left text column, the incipits **מלכותך** (the mem
entry, corresponding to verse 13) and **סומך** (the samech entry, corresponding
to verse 14) begin adjacent physical rows. No separately written nun-initial
row is visible between those rows.

That is a layout observation, **not a secure continuous-text omission**. The
mem entry itself is contracted relative to the retained WLC verse; nearby
entries also abbreviate text. This copy's selection/abbreviation could conceal
a line present in its exemplar. Conversely, its sequence is compatible with
an exemplar that lacked the line. This observation does not decide between
those explanations, and is not an additional independent vote for the priority
of the Masoretic omission. No claim is made about every margin, column, damaged
area, or other place where text might occur in the manuscript.

## What was actually consulted

- The existing Cambridge TEI and eight-canvas manifest retained in the pilot;
  their checksums are reused and explicitly pinned, not represented as fresh
  catalogue downloads. The TEI describes Psalms 119:38–145:16 and mixed full
  writing with occasional lemma/serugin abbreviation. It supplies no copy date;
  the collection's acquisition date is not a manuscript date.
- Newly downloaded institutional overview JPEGs for canvas 1/1r and canvas
  2/1v. Canvas 1r was inspected for orientation and context, not fully
  transcribed. Canvas 1v shows the Psalm 145 title תהלה לדוד and acrostic
  context on its right-hand leaf. These are content anchors, not a fresh
  codicological reconstruction of all eight leaves.
- Two new source-coordinate regions of canvas 2: the title/context column and
  the inner column containing the adjacent mem/samech entries. The latter is
  the decisive observation image. Its complete returned 1300 × 1700 pixels
  were viewed without generating or completing any strokes.
- Current POB Psalm 145:13–14 YAML, including the retained WLC source,
  lexical rationales, English, disclosure and historical review metadata.
  The earlier dossier's 11Q5 and versional comparisons are background, not
  freshly repeated manuscript collations in this check.

Only canvases 1 and 2 were newly examined here. The pilot examined canvas 8.
Canvases 3–7 were not newly inspected, and no complete folio-order or
passage-coverage mapping is claimed. Once the actual target region was located,
those other canvases were not necessary to this bounded layout claim.

## Reproducible image location and limits

Institutional [record](https://cudl.lib.cam.ac.uk/view/MS-TS-A-00043-00008/2),
[manifest](https://cudl.lib.cam.ac.uk/iiif/MS-TS-A-00043-00008), and
[TEI](https://services.cudl.lib.cam.ac.uk/v1/metadata/tei/MS-TS-A-00043-00008/).
The browser's text retrieval of the record failed; public HTTPS requests to
the image service succeeded. This access limitation was not a source finding.

Canvas 2 image service:
`https://images.lib.cam.ac.uk/iiif/MS-TS-A-00043-00008-000-00002.jp2`.
Its fresh `info.json` advertises 6054 × 3100 source pixels and a 2000 × 2000
response maximum. The whole-image request `/full/2000,/0/default.jpg` returned
2000 × 1024 pixels, not a full-resolution master.

The decisive region request is
`/3050,800,1300,1700/full/0/default.jpg`; the title/context request is
`/4000,300,1600,2000/full/0/default.jpg`. Coordinates are x, y, width, height
in the advertised source image. Returned JPEG dimensions match each requested
region. These are institutional JPEG derivatives at source-coordinate scale,
not raw camera data, spectral exposures or lossless masters. No local
enhancement, thresholding, generative fill or ImageGen was used.

Cambridge's TEI assigns CC0 to metadata, not to manuscript images. Its image
terms permit research use and direct publication requests to the library.
Downloaded images remain private; the repository contains locations, hashes,
observations and review records, not image copies or public embeds.

## Four decisions and English impact

1. **Observation:** a securely located adjacent mem/samech row sequence in the
   inspected region, with abbreviation evident locally.
2. **Transcription:** only the identifying incipits and title are asserted
   here. No expanded shorthand, complete verse transcription, supplied letters,
   new hand assignment or independent blind reading is claimed.
3. **Text selection:** held. The witness's abbreviation behavior prevents
   equating the layout with absence in a continuous exemplar. The prior
   dossier's separate questions about inclusion and exact wording remain open.
4. **Translation:** unchanged. Current POB retains the Masoretic main text and
   discloses 11Q5's additional line and the standard Greek wording difference.
   This check supplies no new source selection or identified English defect
   warranting replacement. It does not re-certify the old model-review scores
   or approve a new note. No derivative translation or public reader changed.

The method improvement is concrete: catalogue labels such as “mostly full”
must be tested at the decisive local unit. A physically preserved interval is
not automatically a continuous-text attestation of omission when the copy
systematically shortens entries. Abbreviated witnesses remain useful evidence,
but their inferential limits must travel with every comparison.

## Review and next evidence

The independent judge inspected the actual native region and overview images
after receiving the target and proposed claim. This is an adversarial,
context-informed check, **not** a second blinded transcription or a benchmark
pass. Its exact artifact judgment is stored separately; no approval is
presumed from these preparation notes.

To strengthen an absence claim, compare this copy's complete local selection
practice and any positively identified related material, or locate another
continuous Hebrew witness preserving the disputed interval. Do not reconstruct
an absent nun entry merely from acrostic expectations. A full catalogue census,
the unresolved Psalm 145 apparatus questions and the broader restoration
benchmark remain unfinished.
