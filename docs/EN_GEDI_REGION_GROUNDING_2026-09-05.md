# En-Gedi: region grounding before a reading benchmark

2026-09-05. The fixed merge5-to-master affine registration **failed** its
coarse validation gate. No letter labels or recovery score were produced.
Visual comparison suggests that merge5 belongs to the initial blank margin,
not a text column; the failed fit must not be promoted to an accepted
pixel-level correspondence. This changes the next acquisition priority.

## Edition and images actually inspected

The parent hash-verified the existing Segal et al. preliminary edition
(`23cee43ef796528b1376fc3e2fba0ac8e066604523fa7db3f0086f892945e425`)
and rendered/read complete PDF pages 5,7,8,9,10,15,20. Figure2 and p5 identify
the large initial blank area to the right of the inscribed columns. Page7
distinguishes 18 surviving lines from 17 reconstructed lines per column.
Pages8–10 preserve the transcription's supply/uncertainty boundaries and
identify imaging distortions. These are published interpretations of rendered
measurements, not direct access to an unrolled physical scroll.
[Institutional edition](https://openscholar.huji.ac.il/sites/default/files/he_bible_project/files/m._segal1.1.pdf).

The PDF skill's visual checks were important: text extraction dropped much
of the bracketed Hebrew. `pdftotext` was unavailable; pypdf extraction aided
navigation, while full rendered pages supplied the decisive layout evidence.
The renderer emitted a font-configuration warning; the relevant complete
pages were visually inspected. Appendix p15 expressly qualifies Yardeni's
drawings as conjectural and discusses distortion and blurred enlarged contours.
Figure3 on p20 is therefore an alignment aid, not independent ink ground truth.

The parent also viewed the complete, immutable published master PNG and
merge5 texture PNG. Their shapes and cracks suggest a correspondence to
the right blank margin. This is a context-informed visual hypothesis, not
absence-of-ink certification. The [EduceLab archive](https://archive.org/details/engedi-scroll)
was consulted again and retains its declared noncommercial license. Licensed
source images remain private outside Git; no image edits or generated images
were produced. Analysis resized arrays do not replace source imagery.

## Fixed development experiment and observed failure

The [protocol](../sources/textual_restoration/discovery/en_gedi_registration_protocol.v1.json)
SHA256 is `824d27f65a5092b3f9aef0504875818bc53dae4292da1f140dd0c8d061128669`.
It was written and independently read before feature-matching results.
Both images, prior numeric outcomes and textual context were already known:
this is not a pristine held-out experiment. The fixed every-third feature
split is correlated, not spatially independent. Static hashes alone do not
prove predeclaration timing.

The [tool](../tools/textual_restoration/register_en_gedi_segment.py) uses the
documented [OpenCV SIFT/BF matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html),
a fixed ratio/mutual-match filter and fitting-only RANSAC affine model, with
original-pixel coordinates and no validation refit. The optional OpenCV
4.13.0.92 wheel was installed only into a private task-local dependency
directory. Actual OpenCV is4.13.0 and NumPy2.3.5. The runtime reported eight
threads despite the code requesting one; the actual value is recorded.
No source-file or global package changes were needed.

The [receipt](../sources/textual_restoration/discovery/en_gedi_registration_check.v1.json)
SHA256 is `f9af202b19413d80234a2721cc9593d3c945014e786a7fe81da590dcef55c6ab`.
It preserves all372 matches, partitions, residuals, the matrix, exact resize
scales and all19 prior measured-target projections with null letter labels.
The judge identified that these are descriptor pairs, not372 distinct locations:
there are327 unique geometric pairs, and32 validation rows share an identical
geometric pair with fitting rows (SIFT can return several orientations).
The parent reproduced those counts. This further limits independence; the
frozen experiment was not deduplicated or refitted after observing failure.

| Fixed criterion | Observed | Outcome |
|---|---:|---|
| At least12 fitting inliers |98 of248 fitting pairs|Pass |
| At least8 validation pairs |124|Pass |
| At least80% validation pairs within20 master pixels |60/124 =48.39%|Fail |
| Fitting-inlier horizontal span at least25% of texture width |81.10%|Pass |
| Fitting-inlier vertical span at least50% of texture height |36.70%|Fail |

Thus even the deliberately coarse development-region gate fails. A local
warp, feature ambiguity or other differences between the segment and composite
may explain this; the present experiment does not isolate the cause. We did
not relax thresholds, discard validation mismatches or search another model
to turn this same experiment green. The affine's projected rectangle lies
approximately at master x7971–10213/y628–4202, consistent with the visual
blank-margin hypothesis, but **unaccepted projected coordinates are not a
manuscript locator**. No prior measured point is now certified as a Hebrew
letter, blank pixel or ghost artifact. Earlier integer-value agreements
remain numerical results, not reading accuracy.

## Coordinate defect and versioned correction

The parent raised a pixel-center concern during review; the judge independently
confirmed a P2 defect using an actual OpenCV area-resize ramp and its primary
implementation. V1 lifted feature coordinates by scale alone. In integer
pixel-center coordinates, the correct lift is `(u + 0.5) * scale - 0.5`.
V1's matrix and projections therefore cannot be called correctly labeled
original-pixel-center coordinates, even apart from its failed spatial fit.
[OpenCV4.13.0 resize implementation](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp).

The original protocol, tool and receipt remain immutable. A separate
[correction tool](../tools/textual_restoration/correct_en_gedi_registration_coordinates.py)
first reproduces the entire actual v1 run, then conjugates its affine by the
texture/master center-offset translations. It shifts feature coordinates,
retains every descriptor pair, fitting mask and partition, and recomputes
projections of the original19 integer pixel targets without shifting those
original targets. This is not a new feature search, RANSAC fit or threshold.

The [v2 receipt](../sources/textual_restoration/discovery/en_gedi_registration_check.v2.json)
has SHA256 `6d358d16f5d9744b3e304caced3327866a8719d6a16cf2f3f23f458aa3185a75`.
Texture offsets are approximately(0.500508,0.5), master offsets(1.5,1.500372).
Fixed-original target projections move approximately(1.061456,0.945537)
master pixels. Maximum absolute residual change is1.84e-12 pixels from
floating-point arithmetic; the same criterion checks still FAIL. Correct
coordinate bookkeeping does not make the registration acceptable. The
uncertified rectangle is approximately x7972–10214/y629–4202 in v2.

## Reading-control implications and next acquisition

Three explicit artifact targets in the edition are I6 below מועד, II14
above the first word, and II12 between aleph and taw. The II12 stroke is
described as probably a ghost of taw, not certain proof of its physical
cause. II7's qoph shape is separately qualified. They are development leads,
not four independently authenticated negative labels. Exact segment/edition
region mapping must precede use, and supplied letters must not be scored as
observed ink. Known edition/context exposure prevents calling this material
a new blind benchmark.

The safe next step is to inspect text-bearing segment textures, then acquire
their masks/mappings and the actual required CT neighborhoods. The existing
verified ZIP index identifies merge0–4 and remerge texture members (roughly
8–11MB each), but these six have not been acquired or assigned textual loci
in this pass. Choose a bounded acquisition and preserve all outcomes, rather
than continuing to accumulate measurements from an unlocated blank region.
No full archive acquisition is necessary for initial triage.

A reading benchmark still requires image/edition alignment, independent
preservation-aware development labels, a separately frozen evaluation set,
letter/token scoring units, explicit errors/abstentions and real-damage
controls across two imaging families. Yardeni's drawing and Segal's edition
must not be counted as independent measurements of the same generated surface.
ImageGen remains illustration-only and cannot fill missing evidence. No
source selection, canonical English, note or publication approval changed.

## Reproduction

Run with OpenCV4.13.0 available to the bundled numerical Python:

```sh
PYTHONPATH=/Users/zack/Documents/Codex/2026-09-03/can-you-also-take-a-look/engedi-registration-runtime.ZW3oqS /Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/textual_restoration/register_en_gedi_segment.py /Users/zack/Documents/Codex/2026-09-03/can-you-also-take-a-look/engedi-evidence.7vrr9M
```

The default command recomputes without writing. The six regression tests
check provenance, all residuals, partitions, unreplaced targets, empty-data
failure and the preserved failed gate; they do not test paleographic truth.
Four additional tests cover pixel-center offsets, affine conjugation, unchanged
partitions/failure and original-target handling. Thirty numerical regression
tests passed, including the earlier measured-CT suites. The parent reproduced
v1 exactly from the actual images before constructing v2. The v2 correction
command has the same evidence-directory argument and default read-only mode
as the original registration command.

Final independent coordinate-review outcome: bounded PASS. A fresh separately
briefed judge derived the3×3 matrix conjugation, checked all372 corrected
coordinate/residual rows, ran all ten registration tests and reproduced v2
exactly from the actual images (including the complete frozen v1 run).
Both receipt hashes matched. No actionable repair defect remained; the
scientific registration gate still FAILS. This review did not supply new
PDF/ink inspection, a different-model-family experiment or publication approval.
