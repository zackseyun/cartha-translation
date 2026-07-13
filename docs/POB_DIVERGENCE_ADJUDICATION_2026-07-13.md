# POB divergence adjudication — 2026-07-13

The ten POB verses surfaced publicly by the wording-divergence report were
rechecked against their Hebrew, Aramaic, or Greek source records. A high
divergence score was used only to prioritize review. It was **not** treated as
evidence that POB was wrong or that the majority wording was right.

The pass used two independent Azure reviews (GPT-5.6 Sol followed by GPT-5.6
Terra) and a final source-grounded editorial adjudication. Every accepted
change is recorded in the verse YAML with the previous rendering, the new
rendering, and its rationale. Consequential alternatives remain in footnotes.

## Results

| Reference | Adjudicated POB rendering | Provisional divergence, before → after | Why it changed |
| --- | --- | ---: | --- |
| Numbers 28:23 | “In addition to the regular morning burnt offering, you shall offer these.” | 51.31 → 25.43 | The former wording could make the morning and regular offerings sound like two different offerings. |
| Acts 20:37 | “They all wept a great deal, threw their arms around Paul’s neck, and kept kissing him.” | 50.11 → 37.64 | Preserves the vivid embrace and repeated Greek imperfect without wooden English. |
| Ezra 6:8 | “Moreover, I issue a decree … this house of God … the tribute collected in Beyond the River …” | 49.01 → 45.53 | Corrects two material Aramaic errors: דֵךְ means “this,” and מִדַּת means tribute or tax, not province. |
| Lamentations 3:22 | “Because of Yahweh’s steadfast love we are not consumed, for his mercies never come to an end.” | 48.96 → 30.30 | Restores the first-person plural verb in the pointed Masoretic text. The ancient/versional alternative remains footnoted. |
| Psalms 135:13 | “Yahweh, your name endures forever; Yahweh, your renown endures from generation to generation.” | 48.58 → 35.29 | Makes both verbless clauses natural and parallel while preserving “remembrance” and “memorial” as alternatives. |
| Matthew 26:46 | “Get up, let us go. Look, my betrayer is near.” | 48.07 → 27.57 | Preserves the urgency and present result of the Greek perfect in natural direct speech. |
| Leviticus 18:20 | “You shall not have sexual relations with your neighbor’s wife and so defile yourself with her.” | 47.85 → 17.77 | Translates the Hebrew sexual idiom instead of reproducing an opaque anatomical calque; also corrects the lexical record for the defilement phrase. |
| Psalms 7:14 | “Look: he labors with wickedness, conceives trouble, and gives birth to falsehood.” | 47.29 → 39.72 | Restores the labor sense of יְחַבֶּל and assigns conception to הָרָה while preserving the intentionally compressed birth imagery. |
| Proverbs 6:35 | “He will accept no ransom and will not be persuaded, no matter how large the bribe.” | 46.94 → 50.19 | Restores the verb’s volitional sense and the singular “bribe.” Its higher score after correction is a useful reminder that lexical distance is not error. |
| Ecclesiastes 5:8 | “The land’s profit is for everyone; even a king is served by the field.” | 46.50 → 32.29 | Uses the most straightforward passive construal while explicitly preserving the verse’s genuinely difficult alternative syntax. |

## Editorial classification

- **Material source or lexical correction:** Ezra 6:8; Lamentations 3:22;
  Leviticus 18:20; Psalms 7:14.
- **Meaning-preserving optimal-equivalence repair:** Numbers 28:23; Acts 20:37;
  Ecclesiastes 5:8.
- **Modern-English and discourse polish:** Psalms 135:13; Matthew 26:46;
  Proverbs 6:35.

## Iterative reranking audit

Regenerating the report after the first ten corrections caused previously
lower-ranked verses to enter the public top ten. The audit therefore continued
until **every verse in the regenerated top ten had been source-reviewed**.
This added 38 reviews: 36 main-text revisions, one retained rendering
(Revelation 2:27), and one retained rendering with a corrected note marker
(2 Corinthians 8:13). Together with the first pass, **48 distinct verses were
adjudicated**.

The process stopped only when all ten current leaders had already been
adjudicated. Their continued high scores are not unresolved errors: several
remain lexically distant from the public-domain comparison panel precisely
because the corrected POB preserves a defensible source feature.

| Reference | Editorial result | Final provisional divergence |
| --- | --- | ---: |
| Jeremiah 31:9 | Revised | 38.47 |
| Esther 4:14 | Revised | 19.60 |
| Revelation 2:27 | Retained | 45.56 |
| Proverbs 3:34 | Revised | 27.92 |
| Esther 4:8 | Revised | 42.95 |
| Habakkuk 1:7 | Revised | 48.43 |
| Nehemiah 13:19 | Revised | 20.95 |
| Jeremiah 40:4 | Revised | 42.20 |
| 2 Corinthians 9:5 | Revised | 41.90 |
| Judges 19:9 | Revised | 44.44 |
| 1 Kings 2:19 | Revised | 42.28 |
| Jeremiah 34:16 | Revised | 46.42 |
| Ezekiel 13:4 | Revised | 14.94 |
| Ecclesiastes 1:2 | Revised | 41.19 |
| Isaiah 27:11 | Revised | 35.75 |
| Luke 23:27 | Revised | 27.48 |
| Proverbs 14:20 | Revised | 15.89 |
| Psalms 81:9 | Revised | 37.63 |
| 2 Corinthians 8:13 | Retained prose; repaired note marker | 44.12 |
| Nehemiah 9:17 | Revised | 42.09 |
| Leviticus 14:57 | Revised | 26.73 |
| Jeremiah 33:18 | Revised | 20.05 |
| Nehemiah 9:28 | Revised | 43.21 |
| Psalms 118:25 | Revised | 41.09 |
| Daniel 6:5 | Revised | 45.65 |
| Matthew 23:10 | Revised | 23.19 |
| Job 34:26 | Revised | 24.95 |
| 2 Kings 8:6 | Revised | 38.01 |
| Psalm 148:12 | Revised | 38.59 |
| Isaiah 18:2 | Human-adjudicated revision | 32.42 |
| Numbers 15:29 | Revised | 41.39 |
| Joshua 23:11 | Revised | 35.52 |
| Exodus 12:39 | Revised | 36.73 |
| 2 Kings 9:15 | Revised | 42.21 |
| 2 Kings 2:16 | Revised | 32.16 |
| Ezekiel 20:8 | Revised | 36.87 |
| Joshua 2:19 | Revised | 34.42 |
| Hosea 13:2 | Revised | 46.40 |

### Material corrections found during reranking

- **Proverbs 3:34:** corrected a dangling conditional to the Hebrew
  asseverative sense, "Surely he scoffs at scoffers."
- **Proverbs 14:20:** repaired a reversed passive: the poor person is hated
  even by a neighbor; the poor person does not hate the neighbor.
- **Isaiah 27:11:** restored the plural dry-branch image instead of a singular
  "harvest" being broken.
- **Nehemiah 9:28:** attached "many" to "times," where it agrees, rather than
  to God's mercies.
- **Leviticus 14:57:** removed two fictitious literal "days" and used a ritual
  category broad enough for people, fabrics, and houses.
- **Jeremiah 33:18:** rendered the priestly promise as never lacking a serving
  representative, not one individual never being "cut off."
- **Isaiah 18:2:** received explicit human editorial adjudication because the
  national epithet and river clause are genuinely obscure; the selected main
  construal is now accompanied by precise alternatives.
- **Hosea 13:2:** repaired the sacrificed-object grammar and retained the
  difficult alternative syntax in notes.
- **Joshua 2:19:** preserved the parallel legal blood-on-the-head idiom while
  removing duplicated movement language.
- **Revelation 2:27:** retained "shepherd" despite its high divergence because
  it preserves the Greek verb and Psalm 2's royal-shepherd tension.

## Important limitation

Wording distance can identify passages worth inspecting, but it cannot decide
which rendering is correct. Source grammar, textual variants, discourse,
poetry, genre, and modern-English meaning must decide the revision. A verse may
remain highly divergent after adjudication because POB intentionally preserves
a source feature that comparison translations smooth or interpret differently.
