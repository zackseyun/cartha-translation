# Beyond Qumran: discovery reconciliation and restoration benchmark

Checked: 2026-09-04. This is a bounded follow-up to the
[source coverage audit](BIBLICAL_SOURCE_COVERAGE_AUDIT_2026-09-04.md), not a
completed census of Judean Desert manuscripts.

## What the existing index actually includes

The new [reproducible label screen](../sources/textual_restoration/discovery/qdr_non_qumran_screen.v1.json)
finds **22 labels already associated by naming convention with sites beyond
Qumran** in the pinned QDR dataset. They cover Murabba'at, Sdeir, Hever/Seiyal,
Masada and Arugot label groups. Do not report these as wholly missing simply
because the source is called Qumran Digital Reader.

This screen classifies label syntax, not excavated provenance, authenticity,
genre or surviving letters. Eight other nonstandard labels remain unassigned:
two PAM labels, three Xq labels, Xjoshua, Xjudges and X4. A photograph identifier
or an unknown-location label cannot become a new non-Qumran manuscript by
string matching. Biblical excerpts also need their own genre classification;
do not infer a continuous biblical scroll merely from verse tags.

Mur88 has 424 recognized biblical anchors, not the 427 obtained if
manuscript-shaped `Mur88 chapter:verse` locators are counted as Bible references.
The script uses the existing explicit biblical-book parser. These counts
include indexed reconstructions and are not counts of surviving verses.

The `Arugleviticus` index tags concern Leviticus 23:38-44 and 24:16-18.
The [versioned XLeviticus transcription](https://lexicon.qumran-digital.org/transcriptions/XLeviticus/2026-05-21/index.html?v=2026-05-21)
has corresponding passage coverage; this is a candidate alias requiring
object/bibliographic reconciliation, not an authenticated new object.
It is not the En-Gedi scroll in Leviticus 1-2.

## En-Gedi: a genuine restoration benchmark, not ImageGen

Consulted Segal et al., *Textus* 26 (2016), pp. 2-3 and 8-11, including full-page
visual inspection. The edition gives partial Lev 1:1-9 and 2:1-11, distinguishes
supplied text, reports agreement with Leningrad's consonants, and warns about
processing artifacts, including apparent extra letters. Its radiocarbon and
palaeographic date assessments differ; we retain both.
[Primary edition](https://openscholar.huji.ac.il/sites/default/files/he_bible_project/files/m._segal1.1.pdf).

Our [three-word spot check](../sources/textual_restoration/discovery/en_gedi_published_spot_check.v1.json)
matches the published forms at Lev 1:2, 2:2 and 2:7 to POB's source words.
It records exact edition locators and current verse hashes. This supports
retention at those words only, not approval of entire verses or independent
verification of the unwrapping. No canonical file was changed.

The [University of Kentucky project](https://www2.cs.uky.edu/dri/the-scroll-from-en-gedi/)
links its [Internet Archive dataset](https://archive.org/details/engedi-scroll).
Archive metadata was queried on the checked date; it declares CC BY-NC 4.0.
The following are **remote metadata**, not downloaded or locally verified assets:

| Asset | Listed bytes | Listed MD5 |
|---|---:|---|
| `EnGedi-MasterView-scale-hires.png` | 26,018,559 | `84e654a412d0b0bf508fb919ac9d6c7b` |
| `segmentations.zip` | 1,916,439,877 | `28a20f2e67a69705d4827c76225bcad1` |
| `slices.zip` | 3,870,475,614 | `d057db6bdd1d447cc36bb4a66a68c0df` |

The two archives total about 5.79 GB compressed. Do not silently import them
into POB or treat the noncommercial license as the project's license.

Proposed bounded experiment, **not yet executed**:

1. Select a small region with known readable letters, real loss and suspected
   processing artifacts; freeze the published labels and their uncertainties.
2. Acquire lawful assets, verify actual checksums and retain the measurement,
   segmentation and rendering provenance separately.
3. Compare original slices, surface mapping and rendered output. Vary documented
   processing parameters to detect unstable strokes or mixed layers.
4. Record observed, uncertain, supplied and processing-generated marks. Mask the
   reference text during the first reading pass where practical; declare prior
   familiarity. Do not call this a blind held-out test after consulting it here.
5. Measure false letters as well as recovered legible letters. Only then compare
   the accepted transcription to the source corpus and assess English impact.

This tests recovery of measured signal. Generative completion can illustrate a
hypothesis but must never enter the evidence stream. Reproducible processing
alone is insufficient: a reproducible artifact is still an artifact.

## Greek Minor Prophets: a missing individual entry

The En-Gedi acquisition status above is the September 4 snapshot; the
[September 5 asset follow-up](#en-gedi-asset-follow-up--2026-09-05) supersedes
its statement that all assets remain unacquired.

Registered **8HevXIIgr / Rahlfs 943** separately from the Hebrew/Aramaic IAA
family. The 2022 edition identifies Zech 8:16-17 material excavated in 2019,
assigned by that edition to the known Greek scroll. Its historical discussion distinguishes
revision from Old Greek and lists six partly preserved books. This is Greek
OT evidence, not NT or direct Hebrew evidence. New pieces do not create new
independent manuscript votes.
[Riestra, Ableman, Bitler and Sion, Textus 31 (2022), 159-189](https://doi.org/10.1163/2589255X-bja10019).

Identity/history were consulted through web text extraction; the direct PDF
download returned 403. No full reading or image collation is claimed. Queue
DJD VIII plus the 2022 Zechariah and 2023 Nahum publication updates before
retroversing any new Greek form into proposed Hebrew. The latter publication
is presently a bibliographic lead, not a consulted apparatus.

Later September 5 correction: the
[Greek catalogue follow-up](JUDEAN_GREEK_SOURCE_FOLLOWUP_2026-09-05.md)
supersedes the former registry instruction forcing one physical object.
Retain the catalogue umbrella and unresolved physical grouping, with hand
assignments and edition positions separately recorded. New fragment publicity
does not by itself settle that grouping or add independent reading votes.

## Remaining coverage work

The registry now has 18 mixed object/edition/family entries. The ten formal
comparison cases and 17 passage-coverage records remain unchanged; the three
En-Gedi word checks are a separate, deliberately narrower receipt.

Next, reconcile institutional identities and genres for the 22 labels and
add catalogue-backed omissions. A single Hebrew-oriented index does not cover
all Greek, Aramaic-versional, ritual or newly published material. In parallel
scope, the NT still requires the INTF/NTVMR object-and-passage ledger specified
in the [NT method](NT_TEXTUAL_WITNESS_METHOD.md); this OT pass does not advance
that ledger or justify a corpus-completeness claim.

## En-Gedi asset follow-up — 2026-09-05

Acquired the published master PNG: 26,018,559 bytes, 12100 × 5373 pixels.
Its MD5 matches the archive listing above; local SHA256 is
`1c2da746935f00b0020daf8d72fb0f3ff81b929811907eb5d75eb06d5a0faf10`.
The [asset receipt](../sources/textual_restoration/discovery/en_gedi_asset_check.v1.json)
records this and four independently CRC-checked payloads from `merge5` in
`segmentations.zip`: material, mesh, rendered texture and per-pixel mask.
Both texture and mask are 1969 × 3358. The material references `textured.png`;
the OBJ contains 8,909 vertex positions, texture coordinates and normals each,
and 17,357 faces. These counts do not establish coordinate conventions or
scientifically validate the mesh.

HTTP byte-range inspection downloaded the ZIP directory, not the 1.92 GB
archive. It has 29,285 entries, including 29,259 non-directory entries, and seven
segment groups: merge0–merge5 and remerge. The archive listing's 29,259 file
count therefore agrees after directory exclusion. Per-pixel mapping files and
slice projections are indexed, not acquired or validated. A tail-range probe
of `slices.zip` also succeeded; it did not acquire a scan slice or complete index.

The [bounded acquisition tool](../tools/dss/inspect_remote_zip.py) requires exact
206/Content-Range responses and a stable strong ETag, bounds download and
decompression sizes, checks local headers and member CRCs, and uses a new output
directory. It does not verify the complete ZIP's advertised MD5, establish
authenticity, or authorize redistribution. Its output receipt retains the full
index and byte-range hashes outside Git. Metadata and selected payloads remain
private research inputs under the dataset's declared CC BY-NC 4.0, not POB's
CC BY license. No downloaded image was modified or generated in this pass.

The master and individual texture were visually inspected at overview scale.
This was context-informed, not blind transcription. The published methods
describe segmentation, texturing and flattening, followed by manual mesh/image
merging and contrast adjustment. Thus the master is a processed composite,
not raw measurement or a direct camera photograph. A mask shares its texture's
dimensions but does not label text certainty; do not treat it as an ink truth map.
[Seales et al., 2016, methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC5031465/),
[institutional dataset route](https://www2.cs.uky.edu/dri/the-scroll-from-en-gedi/).

Next: acquire a selected mapping payload and corresponding raw CT region;
establish coordinate conventions and segment-to-master registration. Only then
define a real-damage control with traceable labels and test parameter stability.
The generic acquisition cap currently excludes the large compressed mapping;
any larger acquisition should be explicitly scoped, not silently treated as
already downloaded. No benchmark, new letter reading, source selection or
English change resulted from this pass.

Reproduce acquisition into a **new** private directory, then verify the acquired
master and selected members using the receipt builder:

```bash
.venv/bin/python tools/dss/inspect_remote_zip.py https://archive.org/download/engedi-scroll/segmentations.zip --size 1916439877 --output-dir /path/to/new-private-audit --member segmentations/merge5/textured.mtl --member segmentations/merge5/textured.obj --member segmentations/merge5/textured.png --member segmentations/merge5/PerPixelMask.png
.venv/bin/python tools/textual_restoration/build_en_gedi_asset_check.py /path/to/engedi-evidence --verify-only
.venv/bin/python -m unittest tests.test_remote_zip tests.test_en_gedi_spot_check
```

The builder expects `archive-metadata.json`, the master filename, and a
`segment-audit/` directory containing the acquisition tool's receipt/payloads.
Retrieve the metadata/master from the archive URLs already cited; the full
measurement archives are deliberately not required for this acquisition check.
The [central research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md) records this
stage and its limits alongside the rest of the project history.

## En-Gedi coordinate and intensity probe — 2026-09-05

This later pass supersedes the acquisition limits above: the merge5 mapping
payload, reconstruction log and four reconstructed CT slices are now acquired.
It does **not** supersede the outstanding transcription/calibration gates.

The mapping ZIP member was retrieved with an explicit 140,000,000-byte budget
using bounded streaming ranges. Its 137,909,235-byte gzip payload passed ZIP CRC
and SHA256 checks. Reading the complete inner gzip stream also checked its end
and checksum. The legacy OpenCV YAML has 3358 rows × 1969 columns × six double
channels: exactly 39,671,412 scalar values. The parser retains only selected
samples rather than loading the full matrix. Its dimensions match the texture
and mask; an exterior (0,0) sample has zero mask and zero mapping, not a valid
sample of the volume origin.

The scan index contains 4,504 numbered files, `0000.tif` through `4503.tif`.
Mac sidecars and a separate projection/preview image are excluded. Four actual
payloads, 1649–1652, passed CRC/SHA256 checks and are 1400 × 1400, unsigned
16-bit TIFFs. The log identifies NRecon reconstruction, 17.02417 micrometre
pixels, smoothing and artifact-correction settings. These are **reconstructed
CT volume slices**, not raw acquisition projections; “raw CT” in earlier
planning was too imprecise. The complete imaging reconstruction has not been
independently reproduced.

At preselected texture coordinate (984,1679), mask 255, the six recorded values
give position approximately (858.548,569.606,1649.463) and a unit normal. Current
Volume Cartographer documentation identifies its six-channel map as position
plus normal and indexes volume samples as slice[z][y,x]. This supports our
interpretation but does not prove that every convention in the 2016 export is
identical. The log starts at section 2 while archive filenames start at 0000;
we retain direct-index and +2 hypotheses without selecting either.
[Pinned map documentation](https://github.com/educelab/volume-cartographer/blob/7a3ebcd20cc9844dd055e8c59c505b7edcd33795/core/include/vc/core/types/PerPixelMap.hpp),
[pinned volume sampler](https://github.com/educelab/volume-cartographer/blob/7a3ebcd20cc9844dd055e8c59c505b7edcd33795/core/src/Volume.cpp).

We evaluated ordinary trilinear interpolation at offsets -4, -2, 0, +2 and +4
voxels along the recorded normal. Missing neighborhoods raise errors instead
of silently contributing black pixels. Values below are rounded for display;
the [receipt](../sources/textual_restoration/discovery/en_gedi_volume_probe.v1.json)
preserves the inputs, payload hashes and six-decimal results.

| Slice-index hypothesis | -4 | -2 | 0 | +2 | +4 |
|---|---:|---:|---:|---:|---:|
| Direct archive index | 7315 | 5669 | 3256 | 2273 | 65 |
| Add two to z index | 6570 | 6534 | 6225 | 4180 | 18 |

The published texture pixel is 7512. Neither profile reproduces the published
renderer: its neighborhood filtering, merging and contrast settings have not
been replicated. A near brightness match would not prove a correct origin or
ink. This is a coordinate/intensity sensitivity test at one geometric location,
not a glyph-selected sample, new decipherment, or measured accuracy benchmark.
No image was edited or generated; no source or English was changed.

Next: verify legacy coordinate/index conventions and segment-to-master mapping,
then select independently labeled real-damage regions and reproduce documented
texturing filters. Evaluate marks across processing choices before interpreting
them as letters. Keep material/mask certainty separate from ink certainty.

Reproduce with a Python runtime containing NumPy and Pillow:

```bash
python3 tools/textual_restoration/build_en_gedi_volume_probe.py /path/to/engedi-evidence --verify-only
python3 -m unittest tests.test_en_gedi_mapping
```

The builder expects the previous `segment-audit`, plus `mapping-audit`,
`scan-log-audit`, `slice-index` and `ct-probe-audit` acquisition receipts and
payloads. Fetch their exact members using `inspect_remote_zip.py`; the mapping
requires `--max-member-bytes 140000000`. All source payloads remain outside Git
under the declared noncommercial dataset license. The complete multi-GB archive
hashes remain unverified.

## En-Gedi historical renderer inspection — 2026-09-05

This is static source inspection, not execution of a historical renderer. The
[2016 primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC5031465/) specifies
bidirectional sampling along a line with a seven-voxel primary axis and maximum
filtering. This is more specific than the preceding probe's unresolved filter
description. It does not identify every export setting or executable revision.

The inspected Volume Cartographer commit is
`f8483920c3587f96c5866e9c8e7336f697a86935` (September 30, 2016). It was selected
as period code, **not** established as the exact code used for the paper or the
archived dataset. Relevant observations, with pinned sources:

- [PerPixelMap.cpp](https://github.com/educelab/volume-cartographer/blob/f8483920c3587f96c5866e9c8e7336f697a86935/common/src/PerPixelMap.cpp)
  writes `PerPixelMapping` as an OpenCV six-double matrix and reads row, column,
  then channel. This matches the acquired legacy YAML format.
- [compositeTextureV2.cpp](https://github.com/educelab/volume-cartographer/blob/f8483920c3587f96c5866e9c8e7336f697a86935/texturing/src/compositeTextureV2.cpp)
  writes position followed by normalized triangle normal into that map and
  passes a sampling interval of 0.5 to the texture function. Its radius is a
  caller-supplied value, not established here from the archived export.
- [texturingUtils.h](https://github.com/educelab/volume-cartographer/blob/f8483920c3587f96c5866e9c8e7336f697a86935/texturing/include/texturing/texturingUtils.h)
  routes the maximum filter through `SamplingAlongNormal`. It uses float-valued
  coordinates, normalizes the normal and samples both signs of
  `i * interval` for `i < int(radius / interval)`. Thus, if radius were 7 and
  interval 0.5, it would sample out to 6.5 on either side, with the center
  duplicated. This conditional calculation is not an assertion that the paper's
  seven-voxel axis means a software radius of 7.
- [VolumePkg accessors](https://github.com/educelab/volume-cartographer/blob/f8483920c3587f96c5866e9c8e7336f697a86935/volumepkg/include/volumepkg/volumepkg.h)
  return a `volcart::Volume`;
  [Volume.h](https://github.com/educelab/volume-cartographer/blob/f8483920c3587f96c5866e9c8e7336f697a86935/common/include/common/types/Volume.h)
  routes `interpolatedIntensityAt` to `interpolateAt` and integer samples to
  `slice[z][y,x]`.
- [Volume.cpp](https://github.com/educelab/volume-cartographer/blob/f8483920c3587f96c5866e9c8e7336f697a86935/common/src/Volume.cpp)
  forms filenames directly from the padded slice index. There is no +2
  adjustment in this path. Its interpolator rounds to uint16 and, in its `c10`
  expression, reuses corner `(x1,y0,z0)` where ordinary trilinear interpolation
  would use `(x1,y1,z0)`. That is an observed implementation discrepancy in
  this pinned revision, not evidence that the En-Gedi publication used it or
  that any published letter is wrong.

The period call chain makes direct indexing a better-motivated candidate than
adding the reconstruction-log label automatically. Nevertheless, the archived
mapping's exact origin/version and segment-to-master registration remain
unverified. The prior receipt is intentionally unchanged: its two hypotheses
and ordinary trilinear results record what was actually tested at that stage.

Next reproduction protocol: identify the export revision and radius convention
where possible; explicitly record coordinate precision, normal normalization,
sample endpoints, interpolation and rounding. If the original executable cannot
be established, label alternatives as candidate emulations. Use predeclared
development coordinates and separate held-out coordinates; do not select a
protocol solely because it fits the already observed center pixel. Any later
historical-bug emulation must be isolated from the correct standard interpolator
and tested on synthetic neighborhoods before use. A numerical texture match
would still not supply an ink label, validate a letter, or settle textual priority.

No renderer execution, new pixel result, image edit, benchmark, POB source change
or English change occurred in this follow-up. The
[central research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md) records the rationale,
alternative explanation and remaining gates.

## En-Gedi fixed candidate renderer test — 2026-09-05

The [frozen protocol](../sources/textual_restoration/discovery/en_gedi_renderer_protocol.v1.json)
was written and SHA256-recorded before inspecting the eight new texture values:
`39da0c620750511462a1a76d28edaa42bf507d11e0b7dac14d912b986bc13d14`.
The known center (984,1679) is a development point. Eight horizontal neighbors
at x = 968, 972, 976, 980, 988, 992, 996 and 1000, all y = 1679, are held out
from parameter selection. They are adjacent, correlated geometric controls,
not a representative sample of damage or independently labeled letters.

The eight candidates combine two radius parameters (3.5 and 7), two slice-index
offsets (0 and +2), and standard versus historical-corner interpolation. All
use float32 sample positions/normals, half-voxel intervals, both directions,
the historical loop's exclusive upper endpoint and duplicated center, and a
maximum over rounded samples. The two radii preserve the unresolved axis/radius
interpretation; neither was selected from a favorable texture match.

The [numerical implementation](../tools/textual_restoration/build_en_gedi_renderer_probe.py)
isolates the historical corner discrepancy from the existing correct trilinear
function. It uses explicit nearest-even rounding and a documented normalization
approximation. This is **candidate emulation**, not verified bit-exact OpenCV
execution or an identified historical executable. Synthetic tests exercise the
corner difference, sample endpoints, normalization, rounding and rejection of
missing/invalid data. They do not validate ancient-letter recovery.

The first attempted run stopped on an unavailable CT neighborhood; no result
receipt was written. A complete coordinate preflight then identified two
additional required slices, 1648 and 1653, beyond the four already acquired.
The fixed points and parameter grid were retained. Missing measurements are not
zero-valued voxels, and failed points must not be dropped to improve the score.

Both additional TIFFs were acquired with bounded HTTP ranges and passed ZIP
CRC, length and SHA256 checks. Each is 3,925,806 bytes, 1400 × 1400 unsigned
16-bit. The [result receipt](../sources/textual_restoration/discovery/en_gedi_renderer_probe.v1.json)
pins their hashes, all earlier inputs, the protocol and implementation files.
The acquired CT neighborhood now comprises slices 1648–1653. Full archive
checksums and raw X-ray projection acquisition remain outstanding.

Results below use absolute intensity errors in the stored 16-bit scale, **not**
percentages of letter-reading accuracy. The development set has one point;
the locally held-out set has eight. No points were removed or parameters tuned.

| Radius parameter | z offset | Interpolator | Center absolute error | Held-out exact matches | Held-out mean absolute error | Held-out maximum error |
|---|---:|---|---:|---:|---:|---:|
| 3.5 | 0 | Standard | 372 | 1/8 | 120.375 | 530 |
| 3.5 | 0 | Historical corner | 393 | 5/8 | 99.375 | 532 |
| 3.5 | +2 | Standard | 599 | 0/8 | 581.125 | 1475 |
| 3.5 | +2 | Historical corner | 660 | 0/8 | 596.875 | 1507 |
| 7 | 0 | Standard | 24 | 1/8 | 41.875 | 174 |
| 7 | 0 | Historical corner | 0 | 8/8 | 0 | 0 |
| 7 | +2 | Standard | 104 | 0/8 | 596.125 | 1926 |
| 7 | +2 | Historical corner | 14 | 0/8 | 593.000 | 1946 |

The radius-7/direct-index/historical-corner candidate exactly reproduces all
nine selected texture values, including the center's 7512 at normal offset -5.
The points span four distinct recorded normals but remain neighboring pixels
in one row of one segment. This is positive local numerical evidence for that
combination of conventions, not proof of the executable's identity, global
registration, all-segment fidelity or a unique algorithm. Several inputs can
produce identical rounded maxima, as the smaller-radius matches illustrate.
The receipt keeps `selected_candidate` null and all broader validation claims
false; those flags do not erase the nine observed exact numerical matches.

**Reproducing a published texture is not optimizing recovery.** Matching the
historical corner behavior helps trace how the archived pixels were made; it
does not make that nonstandard interpolation scientifically preferable. Keep
the ordinary trilinear branch as a separate prospective comparison. Evaluate
any claimed recovery improvement against measured data and independently
labeled real-damage controls, not agreement with a potentially imperfect
historical rendering or a desired biblical wording.

Next: freeze a wider spatial/multi-segment test of the locally supported
candidate before inspecting those output values; test alternative conventions
without fitting contrast or silently changing points. Then establish master
registration and independently labeled material/ink/damage controls. None of
the current nine samples has a validated ink or letter label. No new letter,
Hebrew source selection, English revision, image edit or generated image
resulted from this numerical test.

Reproduce using the NumPy/Pillow runtime and the existing private evidence
directory, now with `renderer-ct-audit/` for `slices/1648.tif` and `slices/1653.tif`:

```bash
python3 tools/textual_restoration/build_en_gedi_renderer_probe.py /path/to/engedi-evidence --verify-only
python3 -m unittest tests.test_en_gedi_mapping
.venv/bin/python -m unittest tests.test_en_gedi_spot_check tests.test_remote_zip
```
