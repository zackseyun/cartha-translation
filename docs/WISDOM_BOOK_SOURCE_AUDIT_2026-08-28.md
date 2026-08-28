# Wisdom-book source audit — 2026-08-28

## Why this audit exists

A reader comparison of POB Psalm 91 with the NKJV exposed a process gap: wording could be lexically defensible word by word while still sounding unnatural (`will lodge`), unnecessarily technical (`pinions`), or more interpretive than the Masoretic text (`you have said` in Psalm 91:9).

Divergence from NKJV was not itself the problem. The problem was that earlier automated reviewers accepted locally possible glosses without adequately testing the completed poem for natural English, source additions, coherent register, and honest ambiguity.

## Completed scope

| Book | Verse files | Source-audited |
|---|---:|---:|
| Psalms | 2,578 | 2,578 |
| Job | 1,070 | 1,070 |
| Proverbs | 915 | 915 |
| Ecclesiastes | 222 | 222 |
| Song of Songs | 117 | 117 |
| **Total** | **4,902** | **4,902** |

Every record was reviewed against its WLC Hebrew, immediate literary context, existing POB reasoning, natural-English requirements, and public-domain comparison diagnostics. GPT-5.6 Sol performed the primary review; GPT-5.6 Terra independently adjudicated every proposed change. The 187 lower-confidence or structurally difficult cases received a third GPT-5.6 Sol high-scrutiny adjudication.

Final status:

- **3,550 revised** records;
- **1,352 confirmed unchanged** records;
- **0 unresolved/escalated** records;
- **0 orphaned, partial, extra, or unparsable footnotes**;
- **0 unresolved consistency-lint flags**;
- clean Psalm numbering and reader-corpus guards.

These are recorded model-assisted source audits, not named human or credentialed-scholar sign-off. Every file states `human_or_scholar_review: false` so the provenance cannot be overstated.

## Governing corrections

The pass:

- replaced unnatural gloss-English with source-faithful modern English;
- removed unexpressed verbs, motives, adjectives, agents, and doctrinal conclusions;
- removed false zoological or object precision;
- preserved concrete Hebrew images before explaining their implications;
- translated ordinary Hebrew idioms into ordinary English while retaining important literal forms in notes;
- repaired footnote placement and removed notes that documented no meaningful alternative;
- restored `Yahweh` wherever stale metadata incorrectly revived `the LORD`;
- repaired Psalm 60:0 so its normalized verse-0 record contains both Masoretic superscription lines rather than dropping the historical notice;
- documented legitimate contextual gloss variation rather than forcing mechanical one-word uniformity.

The reusable editorial rules are in `docs/SOURCE_NEAR_EDITORIAL_STANDARD.md`; the repeatable audit implementation is `tools/wisdom_source_audit.py`.

## Validation and publication boundary

A source audit, SPOB synchronization, generated-reader publication, and live deployment are distinct stages. This report establishes the completed POB source audit. SPOB redrafting/review and production evidence must be reported separately, and no automated audit is represented as credentialed scholarly review.
