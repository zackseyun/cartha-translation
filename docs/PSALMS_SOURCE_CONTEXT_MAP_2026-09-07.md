# Psalms source-context mapping — 2026-09-07

All **2,578 POB Psalm records** now have a documented source-context mapping
covering all **2,527 verse references** in the vendored WLC Psalms XML. This
resolves the mapping uncertainty in the preceding whole-OT screen, not every
translation/source-span or English numbering issue. No canonical record changed.

The [compact map](../sources/textual_restoration/inventory/psalms_source_context_map.v1.json)
records every chapter, inclusive record ranges and source offsets, ambiguity
candidates, contextual resolutions, the combined heading and input hashes.
Source matching uses the existing WLC parser's stored serialization, not a claim
that its punctuation placement reproduces manuscript layout. This is one edition,
not thousands of independently supporting witnesses.

| Initial match | Records | Resolution |
|---|---:|---|
| One exact source string in the same Psalm | 2,564 | Retain that source reference |
| Repeated exact source string | 13 | Neighboring unique references and order each select one candidate |
| No single exact verse | 1 | Psalm 60:0 combines WLC 60:1–2 |

For Psalm 60:0, the complete ordered letters, vowel points and accents match
the two-verse span after removing whitespace, morphology slashes and punctuation.
Punctuation placement differs. The map therefore labels this match differently
from the 2,577 exact single-verse matches. No missing verse was invented.

Fifty-two WLC first verses are each used as context in both POB heading record 0
and body record 1. This explains the apparent duplication seen in the earlier
chapter-concatenation screen. It does not mean both English records translate
the whole source verse, and it does not authorize deleting either record.

## Remaining reader-reference issues

The map is **not an English versification crosswalk**. Inspection found that
Psalms 51, 52 and 54 store the second heading component as numbered POB verse 1.
Their first body verse is POB verse 2, whereas the XML explicitly maps that source
verse to KJV verse 1. The same offset affects 35 body records across those Psalms.
Psalm 60 already combines its two heading components in record 0.

One other explicit XML KJV-reference mismatch occurs at POB Psalm 13:5. Its source
and English include both the trust/rejoicing and singing clauses of WLC 13:6;
the XML's KJV label is 13:6. Do not infer missing content from the numbered gap
or silently split the existing record. In total, 36 body IDs differ from an
explicit XML KJV-reference note. Those notes are mappings supplied by the local
edition, not a newly collated external English Bible.

Any reader-reference migration must preserve headings, source spans, notes and
old links and test the resulting verse IDs. It is separate from textual criticism
and was not applied here. Likewise, consistent rendering of repeated Hebrew
refrains is a separate English review, not automatic wording normalization.

## Verification and scope

The current-state test expands every range, compares every source string,
recomputes repeated-text candidates, verifies the unique neighboring anchors,
checks the combined heading's pointed-letter stream and proves both record and
source-reference coverage. The map retains the original ambiguity evidence
rather than concealing that text identity alone was insufficient.

The prior turn made verified progress on Judges' disclosure; that name question
remains parked. This pass used local files, existing parsing/normalization and
deterministic checks, without another research agent or acquisition. No Hebrew,
English, footnotes, IDs, generated reader bundle or deployment changed. The
manifest binds the inspected records; it is not a translation-accuracy score.

Closeout: seven mapping/inline-letter tests pass, and the full canonical path/hash
manifest is unchanged since the scan. Map SHA-256:
`428ea3b86a58faa9694fe64adc0754060c7f736c219bfe7eef34cbbd2d70266d`.
