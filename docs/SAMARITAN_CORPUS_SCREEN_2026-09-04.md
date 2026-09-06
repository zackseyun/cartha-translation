# Whole-Torah Samaritan/WLC screen

Follow-up: the [September 5 incense-altar alignment](EXODUS_INCENSE_ALIGNMENT_2026-09-05.md)
maps the relocated block explicitly and separates order from local wording.

Checked 2026-09-04. This extends comparison beyond the six selected Torah cases
to every verse node in the pinned DT-UCPH Samaritan dataset. It is a discovery
screen of two digital controls, **not a completed critical apparatus**.
Verification rerun 2026-09-05: the saved screen matches full recomputation;
124 targeted tests and the OT registry/coverage validator pass.

## Actual scope and findings

| Book | SP verse nodes | WLC verses | Same-label consonantal matches | Same-label differences |
|---|---:|---:|---:|---:|
| Genesis | 1,533 | 1,533 | 516 | 1,017 |
| Exodus | 1,203 | 1,213 | 328 | 875 |
| Leviticus | 859 | 859 | 320 | 539 |
| Numbers | 1,289 | 1,289 | 459 | 830 |
| Deuteronomy | 957 | 959 | 249 | 708 |
| Total | 5,841 | 5,853 | 1,872 | 3,969 |

All 5,841 SP nodes have matching WLC reference labels. Twelve WLC labels have
no separate SP node: Exodus 30:1-10 and Deuteronomy 34:2-3. These are **index
facts, not twelve proven textual omissions**. Fifteen differing SP verses
match some other WLC verse's consonants within the same book; repeated formulas
and parallel passages prevent automatic reassignment.

The output stores aggregate counts, unmatched labels, these ambiguous matches,
and twenty large length-difference leads. It exports no source transcription
or full verse index. Small differences can be consequential; length is only
one discovery route, not a historical-priority or English-impact score.

## Follow-up checks that change our alignment method

**Exodus incense-altar instructions:** directly reading SP 26:35 in the pinned
dataset confirms that it continues with the altar-making, incense and annual
atonement instructions corresponding to WLC 30:1-10. The two blocks also have
wording differences; this is not a claim of exact text identity. We must align
the moved block before classifying additions and omissions. Leaving it at
26:35 in one tradition and at 30:1-10 in the other is legitimate evidence,
not an extraction error to hide. No manuscript-image verification or decision
about which order is earlier has been made.

**Deuteronomy 34:** SP 34:1 in this dataset uses a different geographic
description, followed by no separate 34:2-3 nodes. Do not manufacture those
verses by copying WLC, or call their absence merely a numbering issue. A
passage-range comparison and manuscript/edition review must decide the scope
of the alternate description. This passage belongs to the Garizim 1 portion
of the digital control, not Chester Beatty 751 or Rylands MS 1.

**Genesis 30:36:** the source README explicitly says additions formerly labelled
36a-c are grouped under 36. Direct consultation confirms extended dream/speech
material there. Comparing 36 alone against WLC is a valid lead but not a
complete analysis of the relationship with parallel material elsewhere.

These findings demonstrate why POB needs many-to-many passage alignment,
preserved order, and explicit source boundaries before global variant totals
can be interpreted. They do not justify combining different literary forms
into an otherwise unattested longer text.

## Provenance and reproducibility

Source: [DT-UCPH SP pinned commit](https://github.com/DT-UCPH/sp/tree/2f2120286ac48d4ff3d04e0107e33efd864aa9e1),
Text-Fabric 7.1.3. Attribution: Højgaard, Naaijer and Schorch; Samaritanus
project. The source identifies Chester Beatty Library 751 through Deut 32:36
and Garizim 1 from 32:36b; that boundary verse is composite. Its CC BY-NC 4.0
terms remain attached to the external research input. No corpus import or
relicensing into POB occurred.

Seven required feature files and the README are hash-pinned. The reader uses
the dataset's **sign slots**, not morphology-word nodes. All 399,392 slots
were accounted for exactly once; only Hebrew letters and spaces occur. WLC
inputs are the five vendored XML books, each hashed in the receipt. Only direct
written-word children are read; qere, notes and paragraph signs are excluded.

Normalization decomposes presentation forms and compares Hebrew consonants,
ignoring spacing, vowels, accents and punctuation. It preserves matres and
final forms. Thus an equal result does not establish the same vocalization,
word division or meaning. A different result does not distinguish spelling,
copying, editorial change or bad alignment. Neither is a translation decision.

```bash
.venv/bin/python tools/textual_restoration/build_samaritan_screen.py /path/to/sp/tf/7.1.3
.venv/bin/python tools/textual_restoration/build_samaritan_screen.py /path/to/sp/tf/7.1.3 --verify-only
.venv/bin/python -m unittest tests.test_samaritan_screen
```

The [saved receipt](../sources/textual_restoration/discovery/samaritan_wlc_screen.v1.json)
is recomputed from the actual input files, not accepted because its totals
look plausible. Unit tests separately check normalization, qere exclusion,
unmatched labels, ambiguous matching, metadata-only export and accounting.

## Critical editions and remaining work

The registry now explicitly includes the two digital controls already used in
our case records: DT-UCPH SP and lxx-morph Rahlfs. Neither becomes another
ancient manuscript merely by being registered. The
[Schorch Genesis publisher record](https://www.degruyterbrill.com/document/doi/10.1515/9783110711783/html)
describes a broader manuscript-based critical edition; its full apparatus was
not consulted in this pass.

The [author repository's OHB sample record](https://digitalcommons.unl.edu/classicsfacpub/98/)
confirms a Deut 32:1-9 sample with textual commentary. Its download returned
403, and the legacy project sample route was unavailable. The sample is
registered as an access gap, not cited for an exact reconstructed reading.
No PDF was acquired, visually inspected or hashed. This narrows the next
access task without preventing corpus screening.

The registry contains **22 mixed object/edition/family entries**. Formal case
coverage remains **11 cases / 19 records**. No canonical Hebrew/Aramaic source,
English verse, adjudicated selection or image evidence changed in this pass.

Next: resolve passage-range alignment for the large structural leads, sample
small and equal-consonant units to avoid length bias, and review the relevant
critical apparatus before advancing any source-and-English candidate.
