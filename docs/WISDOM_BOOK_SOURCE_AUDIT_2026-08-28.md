# Wisdom-book source-audit baseline — 2026-08-28

## Why this audit exists

A reader comparison of POB Psalm 91 with the NKJV exposed a process gap: the POB wording could be lexically defensible word by word while still sounding unnatural (`will lodge`), unnecessarily technical (`pinions`), or more interpretive than the Masoretic text (`you have said` in Psalm 91:9).

The issue was not divergence from NKJV by itself. The issue was that automated reviewers accepted locally defensible glosses without adequately testing the completed poem for natural English, source additions, and coherent register.

## Current evidence

| Book | Verse files | Files with a recorded source-audit adjudication |
|---|---:|---:|
| Psalms | 2,578 | 57 |
| Job | 1,070 | 0 |
| Proverbs | 915 | 0 |
| Ecclesiastes | 222 | 0 |
| Song of Songs | 117 | 0 |

Most records do contain AI draft and cross-check metadata. Those model passes are useful evidence, but they are not counted here as source audits.

A public-domain comparison-panel run scored 2,526 Psalm rows and 2,324 rows in the four surrounding wisdom books. The alignment verifier found no surviving neighboring-verse offsets. The score is a review-priority signal, not a verdict; published agreement never overrides the Hebrew.

## Immediate correction completed

Psalm 91 received a reader-triggered source audit. Nine POB verses and their SPOB grounding were revised. The changes:

- removed awkward gloss-English (`will lodge`, `length of days`);
- replaced technical or falsely precise wording (`pinions`, `cobra`);
- removed interpretation from the main text where the Hebrew did not express it (`have said`, `securely`);
- retained literal senses, lexical uncertainty, and alternate syntactic readings in notes;
- added the governing process in `docs/SOURCE_NEAR_EDITORIAL_STANDARD.md`.

## Ordered review program

1. **Psalms:** review every chapter as a poetic unit, starting with reader reports and the high-risk/divergence queue. Current first queue includes Psalms 81:15; 9:6; 61:7; 37:1; 17:7; 59:4; 109:19; and 15:4.
2. **Job:** begin with 36:18; 2:3; 42:11; 6:29; 11:12; 33:6; 35:15; and 20:20. Job's difficult Hebrew requires especially conservative claims.
3. **Proverbs:** begin with 16:20; 9:7; 29:10; 28:18; 13:23; 13:11; 14:9; and 17:14, then review proverb pairs as complete sayings.
4. **Ecclesiastes:** begin with 9:2; 3:19; 4:8; 2:3; 12:5; 8:14; 2:26; and 8:17, preserving the book's deliberate ambiguity and repeated vocabulary.
5. **Song of Songs:** begin with 6:12; 6:10; 8:12; 6:9; 7:3; 6:7; 2:7; and 1:15, avoiding euphemistic expansion or flattening of its poetry.

Each pass must distinguish automated review, recorded source adjudication, named human or credentialed-scholar review, generated-reader synchronization, and live publication. None of those stages implies another.
