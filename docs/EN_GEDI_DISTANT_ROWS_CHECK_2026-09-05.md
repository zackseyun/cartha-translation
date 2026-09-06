# En-Gedi: prospective distant-row measurement check

Date: 2026-09-05. The fixed historical-corner/radius-7/direct-index emulator
matches ten newly evaluable texture values across six distant rows. It now
matches 19 of 19 evaluated values in the original 288-target sample, but
118 other mask-valid targets remain unavailable. This is stronger spatial
evidence for a numerical rendering candidate, not a complete renderer
validation, image restoration or ancient-letter accuracy result.

## Prospective design and acquisition

The [protocol](../sources/textual_restoration/discovery/en_gedi_distant_rows_protocol.v1.json)
was frozen before new intensities and residuals were inspected. Its SHA256 is
`14b6f640f385370f34eec0342b20f32ab7879ac7d08ce77b1fcd5e390289eb5b`.
The independent judge checked this protocol and recomputed the selection
before receiving new results. This is a recorded workflow observation, not
independently timestamped proof from a static file.

For every nonempty whole-height row in the previous sample, choose the valid
point nearest column 984, breaking ties toward smaller x. The six acquisition
anchors are at x984, y419/839/1258/2098/2517/2937. The union of missing slices
needed by all eight fixed methods contains 36 additional CT images. Selection
used existing masks, geometry and missing-neighborhood records, not new target
intensities. It is centered and availability-informed, not a random spatial
sample or a blind transcription. Prior results and literary context were known.

The [acquisition/evaluation tool](../tools/textual_restoration/build_en_gedi_distant_rows.py)
verified the frozen ZIP index and geometry rule, requested the current central
directory with the pinned strong ETag, and checked selected members' names,
sizes, offsets and CRCs before bounded acquisition. No full 3.87 GB archive
was downloaded. The selected payloads total 31,703,069 compressed and
141,329,016 uncompressed bytes, within the predeclared 32 MiB / 144 MiB caps.
Including directory and member headers, logged HTTP response bytes total
32,477,915. All 36 selected payloads passed CRC, length and SHA256 checks.
The full archive's advertised checksum was not verified.

The original six CT slices and the 36 new ones supply 42 reconstructed CT
slices. These are not raw X-ray projections. Data remains private outside Git
under the dataset's declared CC BY-NC 4.0 terms, not POB's license. The stable
local acquisition directory is the task's
`research_sources/en-gedi-distant-ct-2026-09-05/`.
The source is the [published En-Gedi dataset](https://archive.org/details/engedi-scroll),
already identified in the earlier acquisition dossier. No generative model,
new segmentation, image modification or new imaging permission was involved.

## Measurement contract

Reproduce the earlier full 288-point receipt from actual inputs first, then
re-evaluate every original point and all eight methods with expanded slice
availability. Keep the previous mapping, mask, texture, float/rounding rules,
normal sampling interval and aggregation unchanged. Radius 7 retains the
historical loop's 28 samples reaching plus/minus 6.5 voxels; it is not a new
radius fitted here. The old candidate's corner convention and ordinary
trilinear interpolation remain separate methods. No flipped axes, contrast
fit, target replacements or relaxed error tolerance were introduced.

The [measurement receipt](../sources/textual_restoration/discovery/en_gedi_distant_rows_check.v1.json)
has SHA256 `102668ae837f884a1eece4357c548bdeda8095d22c1b1204558b460cda179394`.
It retains all 288 points, availability states, 164 evaluated predictions,
raw signed residuals, selected-anchor results, row/group summaries, acquisition
provenance and code/input hashes. Missing voxels never become zero values.

Exact success requires predicted integer minus archived integer to equal zero
at every evaluated point. An empty group is not a pass. Full-scope status
remains incomplete whenever valid targets lack data; separately, any nonzero
observed residual **fails that model's observed exact-match gate**. The label
`scope_status: incomplete` must not conceal those observed failures.

## Results

Of 288 targets, 151 are mask-invalid and 137 valid. Across any method 27
points are evaluable; 14 are common to all eight methods. The availability
sets differ, so full available-set error means are not directly comparable
as if calculated on identical observations.

| Radius | z shift | Interpolation | Evaluable | Exact | Observed gate | Common 14 exact | Common max error |
|---:|---:|---|---:|---:|---|---:|---:|
| 3.5 | 0 | Standard | 20 | 3 | Fail | 2 | 3459 |
| 3.5 | 0 | Historical corner | 20 | 11 | Fail | 7 | 3209 |
| 3.5 | +2 | Standard | 22 | 0 | Fail | 0 | 1753 |
| 3.5 | +2 | Historical corner | 22 | 0 | Fail | 0 | 1691 |
| 7 | 0 | Standard | 19 | 4 | Fail | 3 | 566 |
| 7 | 0 | Historical corner | 19 | 19 | Pass, observed only | 14 | 0 |
| 7 | +2 | Standard | 21 | 0 | Fail | 0 | 1367 |
| 7 | +2 | Historical corner | 21 | 0 | Fail | 0 | 1375 |

All eight full spatial scopes remain incomplete. The primary model's
whole-height group has ten evaluated, 47 unavailable and 79 mask-invalid
targets. Its old acquisition-band group remains nine evaluated, 71 unavailable
and 72 mask-invalid. Thus this acquisition advances previously unmeasured
distant rows, not merely the same center neighborhood again.

New primary observations (each prediction exactly equals the archived value;
all signed residuals are zero):

| Texture x,y | Archived/predicted integer |
|---|---:|
| 984,419 | 9102 |
| 1107,419 | 5674 |
| 738,839 | 6082 |
| 861,839 | 5122 |
| 984,839 | 3762 |
| 1107,839 | 8692 |
| 984,1258 | 8229 |
| 984,2098 | 10904 |
| 984,2517 | 9137 |
| 984,2937 | 10505 |

Six predeclared anchors and four newly available neighboring sample points
are included because the protocol required evaluating the entire old sample.
The four neighbors were not substituted for failing anchors. Horizontal
support is still concentrated near the center; no second segment was tested.
Point-level ties exist among methods, but no alternative passes all 14 common
points. Neither this candidate comparison nor correlated samples establishes
independent evidence about any Hebrew letter.

## Verification, limitations and next step

The five new tests exercise the frozen protocol, explicit nonzero failures,
missing/invalid denominators, empty groups, corrupt/unsafe payload rejection,
and saved-result accounting. Twenty numerical tests passed including the old
mapping and wider checks. Actual-data re-execution verifies old and new
receipts; tests are consistency checks, not scholarly acceptance criteria.

The independent judge reran the five focused tests and actual receipt
reproduction, then implemented a separate scalar eight-corner sampler without
the shared sampling functions. Against all 42 hash/CRC-verified slices, all
164 evaluable predictions, maximizing offsets, sample counts and residuals
reproduced. Execution and final scope reporting received a bounded PASS.
The same fixed numerical conventions were tested, not arbitrary historical
builds; full spatial validation remains INCOMPLETE and letter accuracy untested.

```sh
/Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/textual_restoration/build_en_gedi_distant_rows.py /Users/zack/Documents/Codex/2026-09-03/can-you-also-take-a-look/engedi-evidence.7vrr9M /Users/zack/Documents/Codex/2026-09-03/can-you-also-take-a-look/research_sources/en-gedi-distant-ct-2026-09-05 --verify-only
```

Prior receipts are unchanged. No canonical source, English or note was
modified by this numerical task. Publication approval, exact historical
compiler/build identity, lateral and multi-segment validation, segment-to-master
registration and independently labeled real-damage/ghost-stroke controls
remain open. The next scientific step is to connect measured regions with
defensible image/edition labels and test reading errors and abstentions;
reproducing an archived texture alone does not demonstrate recovered text.
