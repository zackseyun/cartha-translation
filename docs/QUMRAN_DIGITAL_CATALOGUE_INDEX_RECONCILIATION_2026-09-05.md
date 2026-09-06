# Whole-index discovery reconciliation — 2026-09-05

This pass extends discovery beyond the earlier Leviticus and Isaiah samples.
It parses the **entire current Qumran-Digital transcription index**, then
reconciles its biblical-labelled entries and matches elsewhere against all
265 labels in our pinned Qumran Digital Reader (QDR) biblical dataset.
These are different projects, not independent manuscript witnesses or
independent editions merely because their websites differ.

## Sources actually checked

- [Qumran-Digital transcription index](https://lexicon.qumran-digital.org/transcription-index/latest/index.html): downloaded 216,543 bytes of index HTML only; SHA-256 `e1211f26d0c37ac46bc7c8cdb23587393742abaef80fcce001bb8b90752683f5`.
- [Index stylesheet](https://lexicon.qumran-digital.org/transcription-index/v1/styles/style.css): directly checked that `dss-biblical` is italic; SHA-256 `a9ab746af1af354d995e262a7112911fc6919cb226219afdba5b727cb5299c1d`.
- [Project FAQ](https://lexicon.qumran-digital.org/faq/v1/en/index.html), §§3.7 and 3.9: the genre distinction is pragmatic, and the default transcription version is current. SHA-256 `84ca2de5c5f5542189ff157d517a32d38680015855e4173ea6e714ae6ee8e706`.
- QDR `data/qdr.1.1.biblical.json`, [pinned revision](https://github.com/evenderekh/qdr/tree/f54f38464e18409eed8286fe24dd24f88d4735dd): independently verified SHA-256 `3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`. Its 266 records have 265 distinct labels: `4Q483` occurs twice.

The primary index is from Qumran-Digital (DFG project 465277421), continuing
Qumran-Wörterbuch. QDR is Michael Muzar's reader using ETCBC/Naaijer/Abegg-derived
data, with its existing CC BY-NC 4.0 restriction. This pass exports only factual
catalogue/label metadata. It does not import either project's full transcriptions,
apparatus, images, or full verse-to-manuscript index, nor relicense them.

## Result

| Screen | Result |
| --- | ---: |
| All index entries parsed | 1,173 |
| `dss-biblical` entries | 263 |
| Other `dss` / `non-dss` entries | 866 / 44 |
| Biblical-class exact display-label matches to QDR | 231 |
| Biblical-class typography-only alias candidates | 19 |
| Biblical-class entries without either match | 13 |
| Exact QDR label matches anywhere in index | 237 |
| QDR labels with typography candidate but no exact match | 19 |
| QDR labels with neither kind of match | 9 |

The receipt exports 269 catalogue rows: all 263 biblical-class rows and six
exact matches outside that class: **2Q29, 4Q88, 4Q249j, 4Q483, 11Q5, 11Q6**.
This is an important safeguard: filtering only the biblical class would hide
relevant leads already present in our legacy dataset. It does not decide the
genre of any of those six sources.

Typography candidates change only case, whitespace and periods. Examples are
`1QIsaa` → `1Qisaa`, `PAM 43.113` → `Pam43113`, and `Mur. 1` → `Mur1`.
Slashes, hyphens, digits and letter suffixes remain significant. No fuzzy
renaming or manuscript-number reassignment was performed. An exact label is
also only a label match: neither type verifies physical identity, fragment
joins, date, findspot, preservation, independence or textual support.

The 13 catalogue biblical-class entries without a label candidate are:
`4Q8`, `4Q47a`, `4Q54a`, `4Q54b`, `4Q101a`, `4Q116a`, `11Q28`, `11QpapLev`,
`XLeviticus`, `XAmos`, `Mur. 5a`, `4Q464c`, `4Q69c`.

The nine unmatched QDR labels are:
`4Q103a`, `4Q12a`, `4Q26c`, `4Q38c`, `4Q38d`, `4Q8c`, `4Q8d`,
`Arugleviticus`, `X4`.

These are **identity/reconciliation queues**, not discoveries of 22 new or
missing manuscripts. Some may be aliases, reassignments, different catalogue
scope, unpublished or disputed material, or source-version differences. This
pass has not established which. In particular, `Arugleviticus` missing from
this index must not become physical absence or an unverified assignment to
another named manuscript.

Every exported URL preserves the identifier and the listed `2026-05-21`
target version. A link date is not evidence that we opened that transcription,
that every text changed on that date, or that the manuscript was discovered
then. No underlying transcription was consulted **by this index pass**; earlier
passage-specific consultations remain separately recorded.

## Reproduction and verification

[Builder](../tools/textual_restoration/build_catalogue_index.py),
[metadata receipt](../sources/textual_restoration/discovery/qumran_digital_catalogue_index.v1.json),
and [tests](../tests/test_catalogue_index.py).

The downloaded HTML stays outside Git at
`/private/tmp/pob-qumran-digital-index-2026-09-05.html`; the index's `latest` URL
is mutable, so a future download is accepted only if it matches the pinned
hash. Preserve this snapshot outside the repository if long-term offline
reproduction is required. A changed hash requires review, not automatic update.

```sh
.venv/bin/python -m tools.textual_restoration.build_catalogue_index \
  --index /private/tmp/pob-qumran-digital-index-2026-09-05.html \
  --qdr /private/tmp/pob-qdr/data/qdr.1.1.biblical.json --check
.venv/bin/python -m unittest tests.test_catalogue_index
```

Thirteen focused tests check superscript display/URL separation, entities, navigation
exclusion, truncated HTML, unknown classes, duplicate entries/anchors, foreign
URLs, conflicting version parameters, conservative alias rules, ambiguous
candidates, record collisions, missing lists, and bounded receipt accounting.
The actual hash-pinned inputs also reproduce the saved receipt. These tests
establish parsing/accounting behavior, not ancient textual truth.

An independent judge found that the first parser could silently omit a row
whose `li` changed to `div`, accept blank query parameters, and accept an unclosed
superscript. Those malformed inputs now fail closed: the parser checks the
observed `ol > li > a > sup` nesting, retains blank query values for validation,
and requires balanced tags. Three added regression tests exercise those cases
and related orphan-anchor, unknown/duplicate-query and mismatched-tag forms.
The original pinned index still reproduces the same receipt and counts; this
repair changes input validation, not the evidence or source conclusions.

## Next decisions and translation impact

1. Resolve the 13/9 discrepant labels against primary institutional catalogues
   and published editions; record accepted aliases with specific evidence.
2. Verify the 19 typography candidates and the `4Q483` collision before counting
   physical sources. Classify the six outside-category matches case by case.
3. For verified identities, acquire only authorized passage-level evidence and
   separate preserved ink, uncertain reading, reconstruction, correction and
   literary quotation before collation.
4. Extend the independent census to Greek Judean Desert material and other OT
   collections; this index's 263 biblical labels are not an all-OT denominator.

No Hebrew, Aramaic, Greek source selection or English POB wording changed.
The methodological improvement is an explicit whole-index discrepancy queue,
not a claim that all known OT witnesses have been found, compared or restored.

## Parent follow-up: identity and authenticity holds

The separate [hold record](../sources/textual_restoration/discovery/catalogue_identity_holds.v1.json)
keeps XAmos out of secure ancient support pending review of a published
authenticity challenge; it does not declare a laboratory-proven forgery.
XLeviticus/Arugleviticus remains a candidate crosswalk with a newly located
primary-edition bibliography, not En-Gedi Leviticus 1–2. These follow-ups do
not modify the raw index counts or the index pass's consultation scope.
