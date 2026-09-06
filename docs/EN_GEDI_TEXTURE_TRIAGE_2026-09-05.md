# En-Gedi: six remaining texture overviews

Date: 2026-09-05. Outcome: six selected PNG payloads acquired and verified;
all six visually inspected. `remerge` is the next **development** mapping
candidate. No letter, word, verse locator, blank control, or scientific reading
pass is established. The prior merge5 registration remains failed.

## Acquisition fixed before payload inspection

The [EduceLab dataset](https://archive.org/details/engedi-scroll) provides
En-Gedi data and virtual-unwrapping outputs under CC BY-NC 4.0. Its page and
license label were checked again in this pass. Images stay outside Git, under
upstream terms, and are not relicensed as POB content. No new independent
transcription was produced.

The [protocol](../sources/textual_restoration/discovery/en_gedi_texture_triage_protocol.v1.json)
selected every remaining `textured.png` entry except the previously acquired
merge5. All six choices and their indexed sizes, CRCs and offsets were written
before fetching these payloads. The pinned prior index has SHA-256
`6cd26c917e7b02f9650bd0b0e887d4462f22f3fe9244a8cecd7d96c771bb9a98`;
protocol SHA-256 is
`9f6c4e459aadb0d2f470fd4d2cdd2e9908e42e23a26c0fcc35dd9270c1380856`.

The 1,916,439,877-byte archive was accessed through verified HTTP ranges with
the prior strong ETag pinned from the first request. A fresh central-directory
check matched every selected member. Each member passed decompressed-length
and ZIP CRC checks before its payload was published locally and SHA-256 recorded.
The unchanged range-acquisition helper was reused. Unique segment filenames
avoid flattening six identically named upstream `textured.png` files.

Selected compressed bytes: **62,301,068**; expanded PNG bytes: **62,316,462**.
Both fit independently fixed 64 MiB batch budgets; every member also fits the
32 MiB per-member ceiling. Actual logged HTTP response-body bytes, including
index and headers read as ZIP payload ranges, total **65,415,587**. This number
excludes network protocol overhead. The full archive was not downloaded or
hash-verified. No masks, mappings, CT slices or raw X-ray projections were
acquired in this pass.

The [acquisition receipt](../sources/textual_restoration/discovery/en_gedi_texture_acquisition.v1.json)
is an exact copy of the private completed receipt, SHA-256
`a05d2fd77c61776760d60ff7cb846e782d326b825e7df3c02b13e4b12ebec522`.
It retains every successful HTTP range hash and every member hash. The tool
writes progress receipts and rejects an existing output directory, preventing
an interrupted run from silently restarting or overwriting earlier evidence.
This actual acquisition completed without a reported download error.

## What the unaltered overviews show

All six source PNGs were opened as full-image overviews. The display system
downsampled them to roughly 1,900–2,048 pixels high; no enhanced, cropped,
rotated or generated image was saved. These observations are deliberately
coarser than full-resolution paleographic inspection.

| Segment | Native pixels (width × height) | Overview observation |
| --- | --- | --- |
| merge0 | 2761 × 3996 | Faint broken bright rows left/central; extensive cracks and losses. |
| merge1 | 2805 × 4256 | Repeated bright text-shaped rows left/central; lower-left loss and distortion. |
| merge2 | 2192 × 4731 | Repeated rows upper/central and lower-right; large left/central tear. |
| merge3 | 2214 × 4562 | Faint rows left of a long dark fissure; sparse marks elsewhere. |
| merge4 | 1968 × 4529 | Mostly low-contrast surface/cracks at this scale; faint marks insufficient for a confident text/blank control. |
| remerge | 2400 × 4067 | Repeated rows upper/central, with large lower-central loss; next development candidate. |

The [triage record](../sources/textual_restoration/discovery/en_gedi_texture_triage.v1.json)
retains all six observations; none was discarded. `remerge` was selected only
after these views, for investigating a visibly text-shaped region and nearby
damage. It is not a blind test choice or a claim that it is objectively optimal.
Merge1/merge2 remain development alternatives. Similar tears in merge2 and
remerge suggest possible overlap, but do not validate correspondence. These
are outputs from one dataset, not six independent manuscripts or imaging
families. Bright shapes are not automatically authenticated ink.

No Hebrew transcription or verse/column assignment is inferred from the file
names or text-like rows. The [failed merge5 affine registration](EN_GEDI_REGION_GROUNDING_2026-09-05.md)
cannot supply accepted coordinates for any of these textures. Merge4's low
visibility is not a validated negative/blank label.

## Verification and next gate

```sh
.venv/bin/python tools/textual_restoration/check_en_gedi_textures.py /path/to/private/texture-directory
.venv/bin/python -m unittest tests.test_en_gedi_textures tests.test_remote_zip
```

The actual checker rehashed all six retained PNGs and verified their dimensions,
sizes, protocol/tool bindings and public/private receipt equality. Ten new
tests cover selection, filenames, budget/index drift, missing/altered payloads,
receipt/protocol drift and rejected reading/locator promotion. The existing
nine ZIP tests exercise bounded acquisition behavior. Passing these checks
does not prove the visual classifications or validate a reading benchmark.

Next acquire the selected segment's mapping and mask under a separate fixed
budget, establish its actual relation to the master/edition line, and only then
select CT neighborhoods and independently checked development labels. Preserve
supplied/uncertain distinctions and artifact alternatives. Freeze a distinct
evaluation set before tuning, and measure errors and abstentions across two
imaging families before claiming recovery quality. Canonical Hebrew, English,
notes, review flags and publication approval are unchanged.

## Independent review

A separately briefed read-only judge gave a bounded acquisition/overview PASS.
It independently rechecked every retained PNG's SHA-256, whole-file ZIP CRC,
internal PNG chunk CRCs, dimensions and length; verified the exact prior-index
selection and byte-identical public/private receipts; and reproduced budget
and range accounting. It opened all six unaltered overviews and ran the actual
checker plus all 19 focused/ZIP tests. No blocking defect was found.

This review supports retained-payload integrity and appropriately limited
development triage, not authenticated ink, letters, verse coordinates, blind
evaluation, whole-archive verification or publication. The judge noted that
prefetch chronology rests on the supplied execution history; retained files
alone cannot independently prove when selection occurred. The parent execution
did write the six-member protocol before invoking acquisition. The scientific
and labeling gates above remain open.
