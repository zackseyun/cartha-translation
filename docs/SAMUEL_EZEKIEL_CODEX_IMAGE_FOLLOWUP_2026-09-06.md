# Samuel and Ezekiel: Leningrad image follow-up

Date: 2026-09-06. Context-informed agent inspection of two accessible color
photographs. Not a blinded transcription, new decipherment, source selection,
human specialist review, or calibration result. Companion:
[image record](../sources/textual_restoration/discovery/samuel_ezekiel_image_followup.v1.json).

## Outcome

The five-consonant edition screen now reaches actual manuscript images.
For 2 Samuel13:37, the final letter's local visual form favors the publisher's
dalet reading; the preceding short stroke remains a separate vav/yod question.
For Ezekiel16:36, the image does **not** settle bet versus kaf confidently.
Neither outcome authorizes changing the canonical Hebrew or English. These
are local, known-reading checks—not claims that missing text has been restored.

## Acquisition and identity

The [publisher's image instructions](https://www.tanach.us/Pages/LC%20images.html)
describe Sefaria color images, folio-side naming and separate ketiv/qere layout.
The Tanach browser loaded 2Samuel13:37 and its Sefaria image selector, but Go
produced no new tab or visible image; no console error explained the failure.
No popup/security setting was changed. An earlier guessed `LCImages.html`
URL failed; following the actual About-page link supplied the correct URL.
Two direct web-reader change-history opens failed despite their earlier
successful consultation; those failures are not new source evidence.

The [documented Sefaria Manuscripts API](https://developers.sefaria.org/reference/get-manuscripts)
then returned the exact public image URLs and manuscript/page metadata.
Ordinary capped HTTPS retrieval succeeded, without credentials or bypasses.

| Passage | API page ID and reported range | Raw color JPEG |
| --- | --- | --- |
| 2Samuel13:37 | LC_Folio_175v; II Samuel13:18–14:1 | [F175B](https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F175B.jpg), 4,084×4,120 pixels; 5,800,931 bytes |
| Ezekiel16:36 | LC_Folio_283v; Ezekiel16:21–47 | [F283B](https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F283B.jpg), 3,617×4,137 pixels; 4,073,656 bytes |

Both API records credit Bruce Zuckerman/West Semitic Research in collaboration
with the Ancient Biblical Manuscript Center, courtesy Russian National Library,
Saltykov-Schedrin. That attribution is preserved, not replaced by a claim that
Sefaria photographed the manuscript. The metadata's USC source URL currently
renders a Dead Sea Scrolls overview; it is not an independently verified
Leningrad photograph-license page. No image redistribution license was obtained;
full images and crops remain private. UXLC's reusable biblical-text terms are
not extended to these photographs.

The API's folio mapping, filename and neighboring text agree. The Samuel
page includes the relevant Absalom/Talmai sequence in its leftmost main column
and the ensuing flight/mourning narrative. The Ezekiel target lies in its
middle column, in the sequence beginning with the oracle formula and continuing
through nakedness, lovers, idols and children's blood. These anchors establish
the local passage independently of the disputed letter. The folio numbers are
metadata identities; this report does not invent a visible modern folio number
on either verso photograph.

## What was visually observed

Full-page images were viewed for context; those initial displays were reduced
by the image viewer. The subsequent PNG crops were decoded-native, unresized
pixel rectangles viewed at original detail. There was no enhancement, threshold,
rotation, generative fill or model-produced stroke. Coordinates use top-left
origin and exclusive right/bottom edges; all seven rectangles and hashes are
in the companion record. Pixel-exactness verifies the derivative, not a reading.

### 2 Samuel13:37 — separate final letter from preceding stroke

The publisher locator is folio175B, reading-order column3, line19, word13:37.7.
The body word after בן lies in target rectangle `[470,2540,830,2680]`. Its final
character has an angular cap/shoulder compatible with dalet, compared with the
nearby dalets in דוד (13:39) and the resh of גשור in the following body line.
This local comparison favors the published dalet over the vendored final resh.
It is a qualitative observation, not a quantified palaeographic classifier.
The short stroke immediately before that final letter remains ambiguous enough
that this check does not resolve the publisher's separate vav/yod uncertainty.

A separately inspected left-margin rectangle contains a small reading and
qere indicator compatible with the published reading tradition. This does not
make it an independent manuscript or erase the body/margin distinction.
The actual vendored XML already gives qere עַמִּיה֖וּד alongside ketiv עמיחור;
UXLC changes the body ending to dalet while retaining its uncertainty note.
The qere's he and the written form's het must not be silently homogenized.
The full-word spellings here are published XML controls, not claims that this
single image inspection independently certifies every sign or vocalization.

The current POB prints **Ammihur[a]**. Its sole note is actually about the
implicit subject of “he mourned,” understood as David—not a disclosure of the
name's ketiv/qere. The marker's position after Ammihur is therefore misleading
for that note's topic. This is a concrete reader-facing follow-up in addition
to the name/source question, not evidence that the name variant is already
disclosed. Any proposed Ammihud rendering, source-patch label and corrected
note anchor need their own exact source/English/metadata review. Nothing is
applied here; the historical HALOT-labelled decisions were read, not freshly
verified against HALOT.

### Ezekiel16:36 — preserve the bet/kaf hold

The publisher locator is folio283B, column2, line14, word16:36.10. The target
rectangle `[1430,2195,1770,2320]` contains the word ending the line after ערותך.
The relevant initial sign has uneven dark strokes and a poorly differentiated
lower/right contour. Nearby כ in כל and ב in בניך, visible in the native context
rectangle, supply local shape comparisons, but do not make that target contour
decisive. This inspection abstains between bet and kaf; it does not infer the
physical cause of the irregularity or reconstruct a missing projection.

The publisher already flags uncertainty: summary/header c versus detailed
action/current XML t must not be converted into certainty by choosing the
more convenient label. POB currently follows the bet form with “in your
prostitutions”; a kaf-based analysis could affect the relation expressed by
that phrase, but this image check does not select its syntax or English.
The separate bronze/wealth interpretation and older revision history are
outside this letter question and are not reapproved by it.

## Next gates

The image availability/identity gap is closed for these two targets; the
uncertainty and application gates are not. Preserve the strongest contrary
reading, seek the relevant BHL apparatus/alternative photographic evidence for
Ezekiel and Samuel's short stroke, and keep exact diplomatic spelling separate
from a reading tradition and critical-text priority. A second report-aware
agent can audit these observations, but cannot retroactively supply a blinded
two-family result. Images shown to this pass are development evidence, not
held-out evaluation material. ImageGen supplies no evidential restoration.
