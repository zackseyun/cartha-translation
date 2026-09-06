# Leviticus: catalogue-to-index reconciliation

Date: 2026-09-05. This pass completes an identity-level screen of one published
DSS table against one pinned QDR index. It does not complete Leviticus textual
comparison, authenticate the table's objects, or cover every Leviticus tradition.

## Result

| Accounting unit | Result |
|---|---:|
| Catalogue target names screened | 30 |
| Names categorized as published in the 2020 table | 27 |
| Further names categorized as unpublished then | 3 |
| Target names with scoped QDR reference hits | 18 |
| Distinct matched QDR labels | 17 |
| Target names with none of the queried labels in QDR | 12 |
| Distinct Leviticus verse anchors in this QDR snapshot | 484 |
| Leviticus-tagged QDR labels without a candidate table match | 0 |

The 18/17 difference comes from testing two proposed parts of legacy 4Q24.
It is not an additional independent witness. The source's published count is
conditional on that split. Three unpublished names share the table's final
row; 11Q1's continuation on the preceding page is not a new row. The PDF skill
required full visual inspection of the table pages and footnotes before
entering these targets. Dates and disputed passage alternatives have not been
turned into machine-certified coverage in this pass.

## What the gaps mean

The twelve absent-name targets are 4Q119, 4Q120, 4QpaptgLev (also queried as
4Q156), 4Q249k, 4Q249l, 4Q365, 4Q366, 4Q367, EGLev, XLeva, XLevb and Xpaleo-Lev.
This is absence of explicit labels from the **pinned biblical JSON file**, not
proof that the objects are lost, inaccessible, absent from every QDR dataset,
or missing everywhere in POB. En-Gedi already has separately acquired evidence
and bounded comparisons in this project.

Current IAA search-index records identify the missing Greek and Aramaic
targets and give primary-publication routes:

- [4Q119](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q119-1):
  DJD IX, 161-165.
- [4Q120](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q120-1?locale=de_DE):
  Greek translation on papyrus; DJD IX, 167-186.
- [4Q156](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q156-1?locale=ru_RU):
  Aramaic targum on parchment; DJD VI, 86-89. The table's `4QpaptgLev`
  wording is retained as a source label, not adopted as a material claim.

These institutional metadata were consulted on September 5; their images and
DJD texts were not read here. The table's Greek witnesses are not independent
Hebrew transcriptions. Its quotation and reworked-Pentateuch candidates require
genre-specific comparison, not automatic exclusion and not automatic equal
weight with continuous-text witnesses. The three unpublished names require
current identity/publication/authenticity checks; the 2020 label is not current
status certification.

## 4Q24: a useful boundary, not an accepted fragment reassignment

The QDR chapter tags yield 31 distinct anchors for the proposed early-chapter
part and 101 for the later-chapter part. The early tags occur in `f1_7` and
`f8`; the later tags occur in six other groups. `f29` and `f30` have no
Leviticus-shaped reference tags and remain unassigned. Every legacy fragment
is retained in the receipt with its source-record and fragment ordinals.

This is evidence about the digital index's organization. It is not independent
verification of Tigchelaar's hands or physical joins. An input fragment spanning
both chapter scopes would be flagged as ambiguous; a label collision would
retain both record ordinals. The [identity review](LEVITICUS_WITNESS_IDENTITY_REVIEW_2026-09-05.md)
still governs the missing primary-source checks. Mur/HevLev's former `4Q26c`
label is likewise retained without inventing a Qumran findspot.

## Reproducibility and rights

The [target specification](../sources/textual_restoration/discovery/leviticus_catalogue_targets.v1.json)
contains all 30 names, explicit candidate label queries, source page locators,
role cautions and the two chapter filters. The
[derived receipt](../sources/textual_restoration/discovery/leviticus_catalogue_check.v1.json)
records exact input and implementation hashes. Both are metadata only: no
private transcription or complete verse-to-manuscript index is exported.

Catalogue: Himbaza, introduction to *The Text of Leviticus* (Peeters, 2020),
printed pp. 2-5 / PDF pages 15-18, visually rechecked using the existing renders.
The builder verifies the actual PDF against the previously inspected SHA256.
Full PDF and images remain outside Git; publisher open access is not assumed
to confer republication rights. QDR stays at commit
`f54f38464e18409eed8286fe24dd24f88d4735dd`, biblical JSON SHA256
`3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`.
Its CC BY-NC 4.0 terms are preserved; this screen does not relicense it.

```sh
.venv/bin/python tools/textual_restoration/build_catalogue_reconciliation.py \
  /private/tmp/pob-qdr/data/qdr.1.1.biblical.json \
  /Users/zack/Documents/Codex/2026-09-03/can-you-also-take-a-look/tmp/pdfs/leviticus-catalogue.NWLUid/the-text-of-leviticus-2020.pdf \
  --verify-only
.venv/bin/python -m unittest tests.test_catalogue_reconciliation tests.test_qdr_discovery
```

Private paths are acquisition locations on this workstation, not portable
dependencies. Reacquire lawful copies matching the hashes if those paths
expire. Tests use synthetic text and saved metadata without requiring the
private corpora; `--verify-only` separately recomputes against the real inputs.

## Next actions and translation effect

1. Prioritize primary-edition access and exact image/passages for 4Q119,
   4Q120 and 4Q156. Do not let QDR's Hebrew-heavy convenience coverage determine
   the whole discovery queue. Check 4Q120's uncertain Lev 2:7-8 coverage before
   treating it as useful evidence for the existing 2:8 dossier.
2. Resolve the quotation/reworked-text and unpublished targets against current
   catalogues and later reassessments, keeping explicit exclusions.
3. Add precise passage-survival and reading comparisons to the candidate
   identities; metadata hits alone cannot affect source selection.
4. Repeat the catalogue/index method for other books and other source classes.
   This implementation supplies reusable bookkeeping, not a finished all-OT
   census or a new recovery technique.

No Hebrew, Aramaic, Greek or POB English wording changed. Formal comparison
and registry counts are unchanged. No ImageGen output was used as evidence,
and no new ancient letters were claimed.

Verification: final real-input `--verify-only` passed; 173 repository tests and
nine numerical tests passed, including 13 new catalogue tests. These verify
the software's accounting and evidence boundaries, not physical identities
or ancient readings. Registry validation and local documentation-link checks
also passed; the central log records their exact scope.

Later follow-up: [4Q120 preservation review](4Q120_LEVITICUS_PRESERVATION_REVIEW_2026-09-05.md)
adds a published partial-word assessment and individual registry entry without
changing this QDR-screen receipt. The reported ending is supplied, so it cannot
independently decide the person contrast in our Lev 2:8 dossier.
