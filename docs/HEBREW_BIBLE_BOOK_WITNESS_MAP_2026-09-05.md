# Hebrew Bible: all-39-book witness discovery map — 2026-09-05

This is an executed corpus-wide **discovery map**, not a count of ancient manuscripts or a preserved-text coverage percentage. It makes every canonical OT book explicit, including zero hits. It supplements the frozen prior receipts and changes no source or English text.

The pinned QDR corpus contains 266 records / 265 labels and 218,217 word records. There are 318 book–record pairs across 36 books. Zero-hit books: **1_chronicles, nehemiah, esther**. A zero means no biblical reference tag in this file, not no surviving witness or no project base text.

[JSON receipt](../sources/textual_restoration/discovery/hebrew_bible_book_map.v1.json) records every contributing label and record ordinal, one exact nested locator per book–record pair, source reference spellings, catalogue label candidates, role candidates and inherited holds. It exports neither transcription nor a full verse-to-manuscript index. QDR remains CC BY-NC 4.0.

| Book | WLC anchors | QDR anchors | Same-label overlap | Records / labels |
| --- | ---: | ---: | ---: | ---: |
| genesis | 1533 | 338 | 338 | 27 / 26 |
| exodus | 1213 | 805 | 805 | 40 / 40 |
| leviticus | 859 | 484 | 484 | 17 / 17 |
| numbers | 1289 | 514 | 514 | 12 / 12 |
| deuteronomy | 959 | 679 | 679 | 62 / 62 |
| joshua | 658 | 65 | 64 | 3 / 3 |
| judges | 618 | 57 | 57 | 4 / 4 |
| ruth | 85 | 42 | 42 | 4 / 4 |
| 1_samuel | 811 | 336 | 336 | 4 / 4 |
| 2_samuel | 695 | 398 | 398 | 4 / 4 |
| 1_kings | 817 | 57 | 57 | 3 / 3 |
| 2_kings | 719 | 16 | 16 | 1 / 1 |
| 1_chronicles | 943 | 0 | 0 | 0 / 0 |
| 2_chronicles | 822 | 4 | 4 | 1 / 1 |
| ezra | 280 | 15 | 15 | 1 / 1 |
| nehemiah | 405 | 0 | 0 | 0 / 0 |
| esther | 167 | 0 | 0 | 0 / 0 |
| job | 1070 | 73 | 73 | 4 / 4 |
| psalms | 2527 | 1261 | 1261 | 39 / 39 |
| proverbs | 915 | 52 | 52 | 3 / 3 |
| ecclesiastes | 222 | 36 | 36 | 2 / 2 |
| song_of_songs | 117 | 49 | 49 | 4 / 4 |
| isaiah | 1291 | 1291 | 1291 | 22 / 22 |
| jeremiah | 1364 | 305 | 305 | 6 / 6 |
| lamentations | 154 | 62 | 62 | 4 / 4 |
| ezekiel | 1273 | 148 | 148 | 7 / 7 |
| daniel | 357 | 188 | 188 | 8 / 8 |
| hosea | 197 | 134 | 134 | 3 / 3 |
| joel | 73 | 62 | 62 | 3 / 3 |
| amos | 146 | 118 | 118 | 4 / 4 |
| obadiah | 21 | 21 | 21 | 2 / 2 |
| jonah | 48 | 48 | 48 | 4 / 4 |
| micah | 105 | 100 | 100 | 3 / 3 |
| nahum | 47 | 47 | 47 | 2 / 2 |
| habakkuk | 56 | 47 | 47 | 2 / 2 |
| zephaniah | 53 | 45 | 45 | 4 / 4 |
| haggai | 38 | 36 | 36 | 3 / 3 |
| zechariah | 211 | 59 | 59 | 4 / 4 |
| malachi | 55 | 32 | 32 | 2 / 2 |

The WLC denominator is verse-element count, including its headings and numbering conventions. QDR/WLC intersection is a same-label comparison: it does not verify reference alignment, continuous preservation, literary order, or the decisive letters. Book/record totals are not additive independent-witness totals, because one source record can index multiple books.

## Reference and preservation accounting

All 218,217 word records partition into 212,374 biblical tags, 5,791 source fragment/line tags, 24 source numeric locator tags, and 28 empty references. There are 0 unresolved reference values. Only explicit book spellings are normalized (`Ex` → `Exod`, `Is` → `Isa`); manuscript/fragment/line tags stay unassigned to a biblical passage. The numeric locators occur under 1Q8 and Mur88; their missing `f` is retained, not silently repaired. The receipt accounts for every nonbiblical prefix and all source-prefix disagreements.

Three entire source records have no biblical tag: **Pam43113, Pam43124 and X4**. They remain book-unassigned instead of disappearing from the 266-record denominator. The sole recognized tag outside the WLC anchor set is **Josh 5:0** (19 word tags); it is retained as a numbering/alignment issue.

The bracket diagnostics distinguish all Hebrew letters inside square brackets, mixed inside/outside letters, no letters inside, no Hebrew letters, and unresolved fragment syntax. State crosses verse and line boundaries within each fragment. Any unbalanced or nested fragment is wholly unresolved for letter classification. These are **syntax bins**, not directly preserved / supplied / partial manuscript counts: even balanced brackets cannot establish damaged ink, omitted brackets, correction hands, authenticity, or continuity across physical fragments. The first locator is a discovery example only and may point wholly into supplied wording.

Among biblical-tagged word records, 21,933 have all Hebrew letters inside balanced square brackets, 3,622 mix inside/outside letters, 37,373 have none inside, 14,461 have no Hebrew letters, and **134,985 remain unresolved because their source fragment has unbalanced/nested bracket syntax**. This large unresolved remainder is a reason to acquire edition-context evidence before counting direct-word coverage.

## Identity, genre and acquisition queues

The six index matches outside the biblical class (2Q29, 4Q88, 4Q249j, 4Q483, 11Q5, 11Q6) remain visible. Biblical-class membership does not distinguish continuous copies from liturgical excerpts. Existing Leviticus/Isaiah catalogue role reports are linked with their book scope; quoted, cryptic, reworked and pesher targets remain separate from continuous-copy claims. No genre is inferred from a verse hit.

4Q8a/4Q8b have known cross-project content conflicts; 4Q8c/4Q8d have candidate content crosswalks, not verified physical aliases. 4Q483 ordinals 2 and 209 remain distinct records under one colliding label, with no independent manuscript count. The 4Q24 proposed split remains held. 4Q54b/4Q69c must not supply two independent votes; 4Q54a/4Q47a face the 4Q29 fragment 3 challenge. XAmos authenticity and XLeviticus/Arugleviticus identity remain held. See the [identity follow-up](QUMRAN_CATALOGUE_IDENTITY_FOLLOWUP_2026-09-05.md) and linked receipts.

The 13 unmatched catalogue names and nine unmatched QDR labels remain acquisition/identity queues, not 22 missing manuscripts. The present index provides no book assignment for every unmatched label; this map deliberately does not invent one. The already published 4Q103a is a concrete example of why an absent index label is not an absent source.

The QDR-side raw label mismatches now have an explicit book queue: Genesis — 4Q8c, 4Q8d, 4Q12a; Leviticus — 4Q26c, Arugleviticus; Deuteronomy — 4Q38c, 4Q38d; Proverbs — 4Q103a; book-unassigned — X4. Known content crosswalks and holds qualify these queues; they do not erase the original syntax mismatch. The receipt separately exports all 18 target rows without QDR query labels from the held Leviticus/Isaiah catalogues, including Greek, Aramaic, quoted, rewritten and pesher lanes. These selected source lists are not expanded into an invented all-book quotation census.

For 1 Chronicles, Nehemiah and Esther, start from the extant Masoretic controls and book-specific critical apparatus, then independent catalogue discovery; QDR cannot provide positive book tags here. For every other book, resolve its per-record identity/genre and exact-word preservation before claiming support. All 39 rows retain primary-family gaps: Masoretic codices/apparatus, broader Judean Desert census and physical mapping, Greek/revision apparatus, Syriac/other versions, and quotations. All five Torah books additionally retain Samaritan manuscript/critical-apparatus gaps despite the completed reference-edition screen. Aramaic portions remain Aramaic. Targum applicability requires book-specific investigation.

These family flags are the prior audit's remaining systematic work, not a claim that no selected passages have been consulted. The map does not yet close the audit's all-institutional-catalogue criterion. This pass reads saved authoritative receipts and pinned data; it does not claim a fresh online catalogue or apparatus consultation.

## Reproduce

```sh
.venv/bin/python -m tools.textual_restoration.build_hebrew_bible_book_map --qdr /private/tmp/pob-qdr/data/qdr.1.1.biblical.json --check
.venv/bin/python -m unittest tests.test_hebrew_bible_book_map
```

The builder rejects a changed QDR hash, saves the hashes of all 39 WLC files and every local evidence input, and regenerates this report and the bounded JSON. Private upstream bytes must be retained separately for offline reproduction. Tests verify accounting and conservative boundaries, not ancient textual truth.
