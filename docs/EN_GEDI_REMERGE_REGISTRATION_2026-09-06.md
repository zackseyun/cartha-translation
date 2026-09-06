# En-Gedi remerge registration: failed coarse gate retained

Reviewed 2026-09-06. The saved development registration **fails** its frozen
coarse gate. This check documents and tests the existing result; it does not
rerun image feature extraction, alter the fitted transform, or accept a verse,
letter, or reading coordinate.

The inputs are the [frozen protocol](../sources/textual_restoration/discovery/en_gedi_remerge_registration_protocol.v1.json),
[registration tool](../tools/textual_restoration/register_en_gedi_remerge.py),
and [saved result](../sources/textual_restoration/discovery/en_gedi_remerge_registration_check.v1.json).
Their protocol and implementation hashes, the shared helper hash, and the
prior mapping receipt hash match their declared pins. The result's SHA-256 is
`d1c0062b8faf78224ce5fa9c747bc631de439ead390f98c6f09925265742a55d`.
These files were read without modification.

The saved run found 14,817 texture keypoints and 15,000 master keypoints.
Its mutual ratio matcher produced 1,065 pairs. Geometric deduplication retained
957 and recorded all 108 rejections. The retained pairs divide into 605 fitting
pairs and 352 validation pairs. The affine fit has 116 training inliers.

| Frozen gate | Saved observation | Required | Result |
|---|---:|---:|---|
| Training inliers | 116 | At least 12 | Pass |
| Validation pairs | 352 | At least 8 | Pass |
| Validation residual at most 20 master pixels | 82/352 = 23.2955% | At least 80% | Fail |
| Training inlier texture x-span / width | 22.6805% | At least 25% | Fail |
| Training inlier texture y-span / height | 34.0778% | At least 50% | Fail |

Sufficient matching counts did not establish adequate spatial coverage or
agreement on held-out features. Validation residuals measure geometric image
correspondence, not the accuracy of recovered Hebrew. Neither these counts nor
the 82 nearby validation features are accepted readings.

The protocol lifts analysis coordinates to native pixel centers using the exact
dimension ratio: `(analysis + 0.5) * scale - 0.5`. The texture changes from
2400 × 4067 to 1200 × 2033, so its vertical ratio is `4067/2033`, not exactly 2.
The master changes from 12100 × 5373 to 3025 × 1343. Deduplication rejects a pair
when either native texture or native master pixel bin already belongs to a
retained pair. Rejected pairs do not reserve their unused endpoints. Validation
uses entire 256-pixel texture tiles, with the frozen tile rule assigning each
tile wholly to one partition. This reduces feature leakage; adjacent tiles and
image features can still be correlated.

All 68 points from the prior geometry check remain present, including their
original texture coordinates and mask values. Their affine projections are
development outputs. Every `accepted_verse_locator` and `accepted_letter_label`
is null. `reading_benchmark_executed`, `image_outputs_written`, and
`canonical_change` remain false. No accepted source-to-master reading coordinates
are produced by this failed gate. The prior exposure recorded in the protocol
also prevents calling this a blind reading benchmark.

## Bounded verification

The new [nine tests](../tests/test_en_gedi_remerge_registration.py) check:

- Frozen protocol, implementation, helper, and prior-receipt bindings.
- Pixel-center lifting, native image edges, and the odd-height dimension ratio.
- Deduplication at either endpoint, rejection reasons, unused endpoint reuse,
  and descriptor-distance tie ordering.
- Tile-boundary behavior, same-tile holdout separation, and saved validation
  rows retaining null RANSAC-inlier labels.
- The complete retained/rejected accounting, the actual failed gate, empty
  evidence failing, and all prior points remaining unaccepted.

The saved pair collection reproduces the recorded gate exactly when evaluated
by the shared gate helper. Replaying geometric deduplication over the saved
retained and rejected matches recovers their memberships and rejection reasons.
These are unit and receipt checks, not a rerun of SIFT, matching, or RANSAC from
the original images. The saved runtime reports OpenCV 4.13.0, NumPy 2.3.5, and
eight OpenCV threads; the tool requests one thread. That recorded runtime value
is preserved, and these checks make no claim about fresh pipeline reproducibility.

Separately, the independent judge reran the complete image pipeline and the
tool's full-object comparison reproduced the saved receipt, including the eight
reported threads. Its diagnostic found `getNumThreads()` returning eight both
before and after `setNumThreads(1)` on this GCD-backed build. Consequently the
record is **one thread requested, eight reported**, not a claim of effective
single-thread execution. The judge also recomputed residuals, both-endpoint
uniqueness, tile separation and null labels. This bounded reporting-integrity
PASS does not turn the scientific gate into a pass.

The next geometric attempt needs a separately recorded development protocol
for local distortion or explicit segment-to-master correspondences, followed
by independent controls. Do not retune this frozen experiment, remove its
failed regions, or treat a locally plausible projection as accepted text.

Ran the following command from the repository root with the bundled Python and
the already available OpenCV runtime:

```sh
PYTHONPATH=/Users/zack/Documents/Codex/2026-09-03/can-you-also-take-a-look/engedi-registration-runtime.ZW3oqS /Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -s tests -p test_en_gedi_remerge_registration.py -v
```

Result: **9 tests passed** in 0.031 seconds. No protocol, tool, result, canonical
text, registry, or central research document was changed in this check.
