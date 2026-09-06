# En-Gedi remerge: acquired geometry, not recovered letters

Checked 2026-09-05. The selected texture's coordinate map and mask were
acquired and verified. The complete map parsed successfully; 38 of 68 fixed
samples are mask-valid. This advances access to the scan geometry of a
visibly text-shaped development region. No CT indexing, master/edition-line
correspondence, letter label or reading improvement is established.

## Fixed acquisition and sampling

Following the [six-texture triage](EN_GEDI_TEXTURE_TRIAGE_2026-09-05.md), the
[new protocol](../sources/textual_restoration/discovery/en_gedi_remerge_mapping_protocol.v1.json)
selected exactly `remerge/PerPixelMapping.yml.gz` and `remerge/PerPixelMask.png`
from the [EduceLab archive](https://archive.org/details/engedi-scroll). This
selection and 68 unique texture coordinates were fixed before the mapping
payload was fetched: 56 whole-texture grid points and 12 upper/central
development points. The texture overview was already known, so this is not
a blind reading experiment. All points, including invalid ones, are retained.

The prior index hash and strong ETag were pinned, with a fresh selected-member
directory match before download. Each member's compressed and expanded ZIP
size fits a 256 MiB ceiling; each corresponding batch total also fits 256 MiB.
Totals: 237,731,153 compressed bytes and 237,811,326 expanded ZIP payload bytes.
The mapping payload is itself gzip-compressed; these ZIP totals are **not**
its expanded ASCII size. Nested decoding has a separate 2 GiB byte ceiling.
64 verified HTTP ranges carried 240,845,435 response-body bytes. The full
1,916,439,877-byte ZIP was not acquired or hash-verified.

The [acquisition receipt](../sources/textual_restoration/discovery/en_gedi_remerge_acquisition.v1.json)
is byte-identical to the private original, SHA-256
`226846e53d167cdd23f6e7244fe27f56c529cb4127941c0da2517befdbb3ed85`.
Mapping gzip SHA-256 is
`948aa089e675a321be1e97505fbf564b55d5f4c2625b934900d6def6f6b3b83c`;
mask SHA-256 is
`4f7697c20c2ac741eaa34408cd60bcc5dedba28b09467c6391b1e18d099b1a3a`.
Length, ZIP CRC and payload hashes were checked. Private upstream assets
retain CC BY-NC terms; no image, mapping payload or full edition enters Git.

## Executed mapping inspection

The [result](../sources/textual_restoration/discovery/en_gedi_remerge_mapping_check.v1.json)
records 2400 × 4067 positions, each with six coordinate/normal scalars:
**58,564,800 scalars** in **1,169,004,178 expanded ASCII bytes**. The complete
gzip stream was decoded through its end/CRC and the scalar count checked;
only the requested samples were retained, not a new full matrix copy.
The existing mapping parser was reused unchanged. No image was edited.

The whole mask has 6,499,042 values of 255 and 3,261,758 zeros. Of the fixed
68 samples, 38 are 255 and 30 are zero. All twelve upper/central development
points are mask-valid. Their recorded z coordinates range from about 852.586
to 1477.817. Across all 38 valid samples, recorded z ranges from about 852.586
to 4052.985, with normal lengths between 0.9999999999999998 and 1.0. These
are sampled geometry bounds, not full-map extrema or validation of every normal.
Mask validity is not an ink or letter classification.

This narrows future CT-neighborhood selection, but no new CT slices or
renderer experiment was run here. The old merge5 affine registration remains
failed and cannot supply coordinates for this segment. Exact scan-index
conventions and segment/master/edition-line correspondence still need their
own evidence. No word or verse is assigned to the bright marks.

## Judge-found byte-count defect and repair

Before accepting an inspection result, the judge found that the original
text-mode gzip opening could translate CRLF to LF. Its character counter
could therefore undercount actual expanded ASCII bytes. A six-byte fixture
reproduces the old four-character count. The repair explicitly uses
`newline=""`; six bytes are now counted and a four-byte cap rejects them.
Bare CR and non-ASCII input are also tested.

The original acquisition implementation is preserved byte-for-byte as a
[historical text snapshot](../sources/textual_restoration/discovery/en_gedi_remerge_acquisition_tool.v1.txt),
SHA-256 `cfc1fae81538634339a29186c86bac5ce148f237d96fa0853c15919965d1cfa3`.
It is a provenance artifact, not an additional executable tool. The unchanged
private acquisition receipt still binds that implementation. The corrected
inspection explicitly checks that archived hash and separately records its
current implementation; history was not relabeled. No faulty numeric result
was published before the repair.

A separate parent binary-stream count found the same 1,169,004,178 bytes,
20,719,247 line feeds and zero carriage returns in the actual payload.
Thus the defect was a real cap-invariant issue, not an observed numerical
change in this LF-only file. The independent judge reproduced the complete
corrected result without writes, independently counted bytes with system gzip,
checked receipt/range accounting and passed all 18 remerge/ZIP tests. It gave
a bounded repair/acquisition/geometry PASS, not a scientific reading PASS.

## Reproduce and continue

```sh
python3 tools/textual_restoration/en_gedi_remerge_mapping.py /path/to/private/remerge-map --texture /path/to/private/remerge.png
python3 -m unittest tests.test_en_gedi_remerge_mapping tests.test_remote_zip
```

Inspection requires NumPy and Pillow. The no-write command verifies the saved
output against actual inputs. `--write` refuses to replace differing evidence.
Next establish the text-region/master/edition correspondence and explicitly
fix CT index conventions and neighborhoods; then separate development labels
from frozen evaluation data and measure errors/abstentions. No canonical
Hebrew/English/notes, source selection, transcription or publication approval
changed in this pass.
