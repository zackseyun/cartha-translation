# En-Gedi: wider numerical renderer check

2026-09-05. The previously supported radius-7/direct-index/historical-corner
candidate exactly predicts **nine new archived texture values**, at three
columns and five rows. However, only nine of the 137 mask-valid predeclared
targets have the required local measurements for that candidate. The wider
spatial check is **incomplete**, not a whole-segment renderer validation or
an ancient-letter recovery result.

## Frozen design and actual inputs

The [new protocol](../sources/textual_restoration/discovery/en_gedi_wider_renderer_protocol.v1.json)
was written and hash-pinned before target texture values were inspected. An
independent judge inspected that protocol/hash before receiving new results.
Its SHA256 is
`52b6f6235f45c17391b3a6f1c9259e113991cb6b155c6b8485355924a2858a4e`.
This timing is a recorded workflow observation; a static file alone does not
prove predeclaration. The previous protocol and nine-pixel receipt are frozen.

Selection uses 17 columns `floor(i×1968/16)`, `i=0…16`, nine full-height rows
`floor(j×3357/8)`, `j=0…8`, and nine rows 1675–1683 around the existing
acquisition band. The 306 nominal slots become 289 unique coordinates after
deduplicating row 1678. Excluding the one overlapping prior-known coordinate
(984,1679) leaves **288 new targets**. The other eight previous coordinates
are not on this grid. Overlapping rows belong only to the acquisition-band
group, so subgroup totals do not count extra observations.

The band is intentionally informed by the existing acquisition location, not
by new intensities. No target was replaced after mask, mapping, neighborhood
or residual inspection. The full-height grid deliberately reveals missing
coverage. All eight old candidates were retained: radii 3.5/7, index shifts
0/+2, and standard/historical-corner interpolation. No radius, shift, rounding,
interpolation formula, contrast transformation or acceptance tolerance was
fitted to these observations.

Only one complete segment bundle is locally available: merge5. The private
inventory contains the approximately 132 MiB compressed six-channel map,
5.5 MiB texture, 29 KiB mask, and six approximately 3.7 MiB CT slices numbered
1648–1653. These are reconstructed CT measurements, not raw X-ray projections.
No second segment has the needed local bundle, and no new download occurred.
The multi-segment check therefore remains unperformed.

Input hashes include:

- Mapping: `7ddf1f829ea0ed793728cee4a0f98885ce4425860d54715998d2ced045065240`.
- Texture: `2899f925fc7be7346772e36b5814e7c5b7efd70c291677e88b68d1a8bce76b9c`.
- Mask: `053e96cb8658e68ab2d62a1ea99947f69115093fd40d93838663a55dd26d9087`.
- Frozen prior renderer receipt: `ed6373c7490973dea44346cce7fc758c3e1be9c27d2cd253e8e5abaca8937aa2`.

The [new measurement receipt](../sources/textual_restoration/discovery/en_gedi_wider_renderer_check.v1.json)
records every target, mapping position/normal, mask value, all eight candidate
statuses, exact missing slice numbers, raw predictions/residuals, histogram,
MAE, RMSE, maximum errors and hashes for every used CT payload. It also pins
the prior numerical code. The complete mapping gzip stream is parsed and
checked for scalar count and CRC integrity through the existing reader.

## Coordinate and numerical conventions

Coordinates refer to the unmodified merge5 PNG: x is column, y is row,
origin at top left, with no flips. Its 3358×1969 mapping stores six values
per pixel: volume x,y,z and normal nx,ny,nz. CT indexing is
`slices[z][y,x]`; the +2 candidate adds two to mapped z. No segment-to-master
registration was attempted.

The unchanged prior functions use float32 positions/normals, a float64 norm
before casting, half-voxel spacing, both signs, duplicated center and integer
nearest-even rounding before a maximum. Radius 7 means 28 samples reaching
±6.5 voxels, not samples at ±7. Radius 3.5 means 14 reaching ±3. The historical
candidate retains the previously identified c10 corner discrepancy; ordinary
trilinear remains a separate control. This is a candidate emulator, not
execution of the historical C++/OpenCV renderer or established bit-exact
behavior of every compiler/build.

All new neighborhood availability was determined from geometry, masks and
slice dimensions before new target texture values were read. Missing
measurements are not zero-valued voxels. A mask-invalid mapping is not a
sample at the volume origin. Invalid/nonfinite/zero normals fail the run.
For unavailable valid points, no prediction or residual is manufactured.

The unfitted criterion is signed residual = predicted integer maximum minus
archived integer texture value, with exact zero required at every evaluable
point. Empty groups are not passes. Any nonzero residual fails the observed
exact-match criterion; unavailable mask-valid targets make complete spatial
coverage incomplete even if observed residuals are all zero.

## Results and retained failures

Of 288 targets, 151 are mask-invalid and 137 mask-valid. Across any candidate,
15 points are evaluable; seven have common coverage across all eight. For
the primary candidate, 128 valid points lack local CT neighborhoods and nine
are evaluated. No out-of-volume result occurred in this run. The unavailable
points remain explicitly in each candidate's full denominator.

| Radius | z shift | Interpolation | Evaluable | Exact | MAE | Max absolute error |
|---:|---:|---|---:|---:|---:|---:|
| 3.5 | 0 | Standard | 10 | 0 | 321.400 | 852 |
| 3.5 | 0 | Historical corner | 10 | 4 | 283.200 | 854 |
| 3.5 | +2 | Standard | 13 | 0 | 456.462 | 976 |
| 3.5 | +2 | Historical corner | 13 | 0 | 459.462 | 877 |
| 7 | 0 | Standard | 9 | 0 | 92.222 | 473 |
| 7 | 0 | Historical corner | 9 | 9 | 0 | 0 |
| 7 | +2 | Standard | 12 | 0 | 438.750 | 976 |
| 7 | +2 | Historical corner | 12 | 0 | 411.917 | 816 |

These available sets differ, so raw candidate MAEs must not be treated as
a comparison on identical observations. On the common seven points, the
primary has seven exact matches; radius-3.5/direct/historical has three;
all other candidates have zero. Their respective maximum absolute errors,
in the table's order, are 746, 746, 976, 826, 473, 0, 976 and 816. Thus the
primary is the only candidate matching all seven, but there are point-level
ties. The receipt preserves every prediction group/tie; no automatic
renderer identity or source-selection promotion follows.

All nine new primary predictions and raw signed residuals:

| Texture (x,y) | Archived value | Predicted | Residual |
|---|---:|---:|---:|
| (984,1678) | 7634 | 7634 | 0 |
| (984,1680) | 7253 | 7253 | 0 |
| (738,1681) | 8013 | 8013 | 0 |
| (861,1681) | 6403 | 6403 | 0 |
| (984,1681) | 7431 | 7431 | 0 |
| (738,1682) | 7436 | 7436 | 0 |
| (861,1682) | 7247 | 7247 | 0 |
| (738,1683) | 7572 | 7572 | 0 |
| (861,1683) | 7415 | 7415 | 0 |

These span 246 texture pixels horizontally and five vertically, with three
distinct recorded normals. All remain in the same horizontal quartile and
small acquisition band. They extend the previous 32-pixel, single-row check
to additional locations, but are still spatially correlated. The whole-height
group contains 136 targets: 79 mask-invalid, 57 unavailable, **zero evaluated**.
The acquisition-band group contains 152: 72 invalid, 71 unavailable and nine
evaluated. Entire distant rows remain untested rather than silently excluded.
Per-row and per-quartile counts/errors are stored in the receipt.

## Reproduction, review and limits

The [new tool](../tools/textual_restoration/build_en_gedi_wider_renderer_check.py)
reproduces the old nine-pixel receipt from actual hash/CRC/length-checked
payloads before computing this experiment. It writes JSON only to stdout and
produces no image. Run using the bundled NumPy/Pillow Python:

```sh
/Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/textual_restoration/build_en_gedi_wider_renderer_check.py /Users/zack/Documents/Codex/2026-09-03/can-you-also-take-a-look/engedi-evidence.7vrr9M --verify-only
/Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -s tests -p 'test_en_gedi_wider_renderer.py'
```

The six new tests check selection accounting, nonvacuous criteria, signed
errors and missing denominators, geometry-only availability, invalid normals,
and saved raw-result summaries. They do not measure transcription accuracy.
After the first calculation, a reporting field was renamed so that a common
subset's status could not be confused with the full predeclared sample's
status; no selection, numeric convention, criterion or residual changed.
All six tests passed. The actual-data `--verify-only` run reproduced both
the new receipt and the frozen prior nine-pixel receipt.

The independent judge passed the bounded numerical/provenance reporting,
reran actual-data verification successfully, and used a separately implemented
scalar corner-weight calculation against the six actual CT slices to
reproduce all 88 evaluable candidate predictions with zero mismatches. That
check did not reuse `sample_line` or `interpolate_candidate`. It verifies an
independent implementation under the same assumed numerical conventions,
not an independent historical renderer, ink observation or recovered reading.
The judge retained the complete spatial result as incomplete/inconclusive;
no concrete repair was required.

The strongest counter-explanation remains that rounded maxima at these few
locations can be compatible with other untested implementations or parameter
sets. Exact matches help trace this archival rendering but do not establish
that its historical interpolation discrepancy is the best recovery algorithm.
The master image also involved later processing. No registration, physical
ink/damage labels, letter truth set, independently measured recovery accuracy,
new ancient reading or canonical edit has been established. The noncommercial
source payloads remain outside Git; only bounded numerical measurements and
provenance are recorded. Larger slice coverage and a second lawful segment
bundle are required before a genuinely wider renderer validation.
