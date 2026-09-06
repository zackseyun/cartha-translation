# Hebrew pilot: applied multi-witness adjudication

Checked: 2026-09-05 · Method 1.0.0

Generated from the [decision dataset](../sources/textual_restoration/decisions/hebrew_pilot.v1.json). These are working editorial choices from published readings, not new image restorations, cross-model-reviewed decisions, or published POB changes.

Older witnesses receive a modest preference; no numerical vote or authenticity percentage is used.

## 1 Samuel 17:4

**Working preference:** Prefer four, retaining six as a material variant.
**Priority confidence:** moderate (editorial judgment, not a probability).
**Wording-level outcome:** provisional selection within this unit.

| Candidate | Hebrew excerpt | English effect |
|---|---|---|
| six | שש | His height was six cubits and a span. |
| four | ארבע | His height was four cubits and a span. |

### Witness matrix

Every non-local row below is a published report; archival pixels were not independently re-read in this pass.

| Witness | Language / role | Reported reading | Date basis | Related evidence group | Source |
|---|---|---|---|---|---|
| Leningrad / WLC | Hebrew / direct-language | six | physical-copy: 1008/1009 CE; older readings can be preserved | masoretic | local-baseline |
| 4QSam-a / 4Q51 | Hebrew / direct-language | four | physical-copy: First century BCE, approximate | samuel-q-lxx | qd-4q51-2025, iaa-4q51, hays-2005 |
| Codex Vaticanus | Greek / ancient-version | four cubits and a span | physical-copy: Fourth century CE | samuel-old-greek | hays-2005 |
| Antiochene / Lucianic Greek tradition | Greek / ancient-version | four | translation-tradition: Later revision with earlier textual antecedents; no individual copy collated here | samuel-old-greek | hays-2005 |
| Josephus, Antiquities 6.171 | Greek / retelling | four | work-composition: First century CE composition; not a first-century surviving manuscript | samuel-old-greek | hays-2005 |
| Symmachus, as reported in the Hexaplaric tradition | Greek / ancient-version | six | translation-tradition: Around 200 CE translation; indirect attestation | masoretic-related | hays-2005 |
| Jerome / Vulgate | Latin / ancient-version | six | translation-tradition: Late fourth-century translation; individual manuscript not collated | masoretic-related | hays-2005 |

Baseline: [translation/ot/1_samuel/017/004.yaml](../translation/ot/1_samuel/017/004.yaml).

- **Why prefer it:** An early direct Hebrew numeral converges with the Greek tradition and an ancient retelling. This is more than a two-copy contrast.
- **Strongest objection:** Six is also ancient, as versional evidence shows. An intentional reduction of six remains possible; manuscript age cannot rule it out.
- **Transmission explanation:** Assimilation of the numeral to nearby six hundred is plausible, not demonstrated. A simpler number is not automatically earlier.
- **Effect of age:** Modest advantage to the early Hebrew attestation of four. Do not date the six reading only to Leningrad.
- **Independence caution:** Greek tradition and Josephus are related evidence, not three or four independent Hebrew votes.
- **Publication decision:** Record four as the working critical choice and retain six in the apparatus; canonical files remain unchanged in this research pass.

Still unresolved:
- Verify consequential manuscript assignments against an apparatus or page image before promotion.
- Determine whether a broader Samuel literary-form policy changes the target text.

Not used to force a result:
- Conflicting summaries of Alexandrinus were not used to break the tie.
- Five-cubit reports were not fully collated and are not adjudicated in this pilot.

## Deuteronomy 32:8

**Working preference:** Prefer a divine referent (sons of God); the exact earlier Hebrew form remains open.
**Priority confidence:** moderate (editorial judgment, not a probability).
**Wording-level outcome:** exact earlier form unresolved.

| Candidate | Hebrew excerpt | English effect |
|---|---|---|
| israel | בני ישראל | according to the number of the sons of Israel |
| god | בני אלוהים | according to the number of the sons of God |

### Witness matrix

Every non-local row below is a published report; archival pixels were not independently re-read in this pass.

| Witness | Language / role | Reported reading | Date basis | Related evidence group | Source |
|---|---|---|---|---|---|
| Leningrad / WLC | Hebrew / direct-language | sons of Israel | physical-copy: 1008/1009 CE; older readings can be preserved | masoretic | local-baseline |
| 4QDeutj / 4Q37 | Hebrew / direct-language | sons of God | physical-copy: Herodian-period Hebrew parchment according to the IAA institutional record | qumran-deut-j | qd-4q37-2026, iaa-4q37, tov-2023 |
| Samaritan Pentateuch reference (MS Dublin Chester Beatty Library 751) | Hebrew / direct-language | sons of Israel | textual-tradition: Ancient Hebrew textual tradition represented here by the pinned DT-UCPH transcription | samaritan | dt-ucph-sp-7.1.3, tov-2023 |
| Greek manuscript 848 / Papyrus Fouad 266 | Greek / ancient-version | sons of God | physical-copy: Pre-Christian Greek papyrus; exact date not used as a numerical score | deut-old-greek | tov-2023 |
| Main Septuagint tradition | Greek / ancient-version | angels / messengers of God | translation-tradition: Ancient Greek translation preserved in later copies | deut-old-greek | lxx-morph-rahlfs, tov-2023 |
| Peshitta | Syriac / ancient-version | sons of Israel | translation-tradition: Ancient Syriac translation; no individual copy collated | deut-syriac | tov-2023 |
| 4QpaleoDeutr / 4Q45 | Hebrew (Paleo-Hebrew script) / direct-language | the decisive final phrase is not preserved | physical-copy: Hasmonean-period Paleo-Hebrew parchment according to the IAA institutional record | qumran-paleodeut-r | qd-4q45-2026, iaa-4q45 |

Baseline: [translation/ot/deuteronomy/032/008.yaml](../translation/ot/deuteronomy/032/008.yaml).

- **Why prefer it:** The versioned 4Q37 transcription directly preserves 'sons of God,' and the Old Greek preserves the same divine referent as 'angels of God'; the following verse about Israel as Yahweh's own portion coheres naturally with that contrast.
- **Strongest objection:** The Samaritan Hebrew tradition and Peshitta join MT on Israel. The symbolism of the nations and Israel supplies a contextual explanation for that reading.
- **Transmission explanation:** A change of referent in transmission is plausible. This pilot does not assert a particular scribe's theological motive or exclude every alternative history.
- **Effect of age:** The Herodian direct Hebrew witness and the ancient Greek tradition modestly favor the divine referent; the later Masoretic and Samaritan copies can still preserve old readings, so age is not used as an automatic override.
- **Independence caution:** Greek sons and angels readings are related versional support, not separate complete Hebrew witnesses.
- **Publication decision:** Retain 'sons of God' as the leading critical English candidate, preserve 'sons of Israel' in the apparatus, and distinguish Greek 'angels' as versional interpretation. Do not change English alone while the verse still records WLC as its canonical source.

Still unresolved:
- Crosswalk DJD fragment 12 to the IAA plate-fragment identifiers, then verify the visible letters against color and infrared images.
- Consult the DJD XIV material discussion and verify the early Greek 'sons' witnesses individually before promotion.
- Define how a POB critical-source selection replaces or supplements a verse's WLC source field so Hebrew and English cannot diverge.

Not used to force a result:
- No reconstructed 'sons of El' reading is asserted as the uniquely recovered autograph.
- 4Q45 is not counted for either reading because the decisive final phrase is not preserved.

## Psalm 145 after verse 13

**Working preference:** Tentatively include a nun line; do not yet select its exact wording.
**Priority confidence:** moderate (editorial judgment, not a probability).
**Wording-level outcome:** exact earlier form unresolved.

| Candidate | Hebrew excerpt | English effect |
|---|---|---|
| absent | — | No corresponding nun line. |
| present | נאמן אלוהים בדבריו וחסיד בכול מעשיו | God is faithful in his words and loyal in all his deeds. |

Representative Qumran wording; exact earliest form is not settled.

### Witness matrix

Every non-local row below is a published report; archival pixels were not independently re-read in this pass.

| Witness | Language / role | Reported reading | Date basis | Related evidence group | Source |
|---|---|---|---|---|---|
| Leningrad / WLC | Hebrew / direct-language | no nun line | physical-copy: 1008/1009 CE; older readings can be preserved | masoretic | local-baseline |
| 11QPs-a / 11Q5 | Hebrew / direct-language | נאמן אלוהים בדבריו וחסיד בכול מעשיו; XVII 2–3, no supplied/uncertain letters marked in this excerpt | physical-copy: First century CE, approximate | qumran-psalms | flint-2010, qd-11q5-2026 |
| Septuagint Psalter | Greek / ancient-version | Rahlfs Ps 144:13a: Lord; in his words (no all); hosios in all his works | translation-tradition: Ancient Greek tradition, later manuscript copies | psalter-old-greek | gentry-2009, lxx-morph-rahlfs |
| Peshitta Psalter | Syriac / ancient-version | CAL 145:013: Lord; in his words (no all); zadiq (righteous) in all his deeds. Its verse 17 instead has merciful in the second colon. | translation-tradition: Ancient Syriac tradition; individual copy not collated | psalter-syriac | gentry-2009, cal-ps145-2026 |
| Greek-based Latin Psalter, Weber–Gryson 2007 display | Latin / critical-edition | line present; Dominus; in omnibus verbis suis / sanctus in omnibus operibus suis | edition-publication: 2007 critical edition, live publisher text checked 2026-09-05; not a newly dated ancient copy | psalter-old-greek | gentry-2009, weber-gryson-psalter-greek |
| Kennicott 142 marginal reading | Hebrew / direct-language | line present; Yahweh; all his words | physical-copy: Medieval manuscript; marginal hand and dependence not independently checked | late-hebrew-margin | gentry-2009 |
| Targum Psalms | Aramaic / ancient-version | CAL 81002, 145:013–014: corresponding nun line absent; chapter text consulted 2026-09-05 | translation-tradition: Individual witness and exact date not collated | psalter-mt-related | gentry-2009, cal-tgps145-2026 |
| Hebrew-based Latin Psalter, Weber–Gryson 2007 display | Latin / critical-edition | line absent in publisher VUL PSA.144:13–14; not absent from every edition of the Hebrew-based Latin Psalter | edition-publication: 2007 critical edition of the Hebrew-based Latin translation; publisher display checked 2026-09-05 | latin-hebrew-psalter-editions | gentry-2009, weber-gryson-psalter-hebrew |
| Hebrew-based Latin Psalter, Harden 1922 edition | Latin / critical-edition | Printed p. 187 includes the line with Dominus and both omnibus qualifiers; apparatus reports omission in A H R (Amiatine, Hubertianus, Ricemarch). | edition-publication: 1922 printed edition; text, apparatus and sigla visually checked 2026-09-05 | latin-hebrew-psalter-editions | harden-hebrew-psalter-1922 |

Baseline: [translation/ot/psalms/145/013.yaml](../translation/ot/psalms/145/013.yaml).

- **Why prefer it:** A Hebrew scroll and multiple ancient versional streams attest a nun line, fitting the acrostic sequence.
- **Strongest objection:** The Qumran form contains other expansion. The line could complete an acrostic, and its second half resembles verse 17. Omission is also ancient.
- **Transmission explanation:** Both loss and acrostic repair are plausible. Inclusion is the present working preference, not an assertion that the Qumran wording is the exact original.
- **Effect of age:** Early Hebrew presence matters, but early omission and uncertain relationships prevent age from deciding exact wording.
- **Independence caution:** Greek-based Latin is not an independent Hebrew vote. Hebrew-based Latin editions disagree: Weber–Gryson omits the line, Harden prints it and records A H R omission. These edition controls do not establish independent ancient support or Jerome's original reading. The medieval Hebrew margin has uncertain derivation.
- **Publication decision:** A source-specific POB reader note was added 2026-09-05; source and English main wording remain unchanged. Pre-note baseline SHA256 2c910e360bd957bafa39c032ea79aa8ceabfc4b9e9289586700a6030a5e39166. Retain the separate line-presence preference, but hold exact-wording promotion. The formal comparison records the directly consulted Hebrew, Greek and Syriac controls without upgrading old reports to new manuscript collations.

Still unresolved:
- God versus Yahweh/Lord is not resolved as the earliest divine designation.
- The directly consulted 11Q5, Rahlfs and CAL controls lack all before words; the two line-present Latin editions have it. Verify the Hebrew marginal hand and the Latin manuscript history before any retroversion.
- Explain the Harden / Weber–Gryson Hebrew-based Latin disagreement using the full modern apparatus and individual witnesses; published A H R omissions are not fresh manuscript collations.
- Resolve Hebrew hasid / Greek hosios versus Syriac zadiq locally; the Syriac adjective does not itself prove an underlying Hebrew tsadiq.
- Check the argument for secondary acrostic repair and the relation to verse 17 before final adoption.

Not used to force a result:
- No single Latin Vulgate vote: distinguish Greek-based and Hebrew-based Psalters, and variation within each. The earlier blanket attribution of absence to Jerome's Hebrew Psalter is superseded by edition-specific evidence.

## Sources

- **weber-gryson-psalter-hebrew:** [Weber–Gryson 2007 Hebrew-based Latin Psalter, publisher display](https://www.die-bibel.de/bibel/VUL/PSA.144) — Publisher PSA.144:13–14 = POB Psalm 145, checked 2026-09-05; corresponding line absent.
- **weber-gryson-psalter-greek:** [Weber–Gryson 2007 Greek-based Latin Psalter, publisher display](https://www.die-bibel.de/en/bible/VULA/PSA.144) — Publisher PSA.144:13 = POB Psalm 145, checked 2026-09-05; line has both omnibus qualifiers.
- **harden-hebrew-psalter-1922:** [J. M. Harden, Psalterium iuxta Hebraeos Hieronymi (1922)](https://archive.org/download/psalteriumiuxtah00lond/psalteriumiuxtah00lond.pdf) — Printed p. 187 / PDF page 223; sigla pp. xi–xii, xvii–xviii and method p. xxix; visually checked 2026-09-05. PDF SHA256 e65a762914345706c36631d68da0bd0f6d4a87afd3230c705bc08101620b015e.
- **cal-tgps145-2026:** [CAL Lagarde-derived Targum Psalms control](https://cal.huc.edu/get_a_chapter.php?cset=H&file=81002&sub=145) — 81002, 145:013–014/017, consulted 2026-09-05; corresponding nun line absent from displayed edition text.
- **qd-11q5-2026:** [Qumran-Digital 11Q5 versioned transcription](https://lexicon.qumran-digital.org/transcriptions/11Q5/2026-05-21/index.html?v=2026-05-21) — column XVII 2–3; surrounding 1–5 and 9–10 inspected 2026-09-05.
- **cal-ps145-2026:** [CAL Leiden-derived Peshitta Psalms control](https://cal.huc.edu/get_a_chapter.php?cset=S&file=62027&sub=145) — 62027, 145:013 and 145:017, consulted 2026-09-05; edition basis https://cal.huc.edu/get_file_info.php?coord=62027145.
- **hays-2005:** [J. Daniel Hays, Reconsidering the Height of Goliath](https://www.otgateway.com/files/JETS-PDFs/48/48-4/JETS_48-4_701-714.pdf) — JETS 48/4 (2005), pp. 704–706.
- **tov-2023:** [Emanuel Tov, The Sons of Israel or God? — Deuteronomy 32:8](https://www.thetorah.com/article/the-sons-of-israel-or-god-deuteronomy-32-8) — Witness table and notes 2–4.
- **qd-4q37-2026:** [Qumran-Digital 4Q37 versioned transcription](https://lexicon.qumran-digital.org/transcriptions/4Q37/2026-05-21/index.html?v=2026-05-21) — fragment 12, lines 13–14.
- **qd-4q51-2025:** [Qumran-Digital 4Q51 versioned transcription](https://lexicon.qumran-digital.org/transcriptions/4Q51/2025-03-11/index.html) — fragments 12–14, line 3.
- **qd-4q45-2026:** [Qumran-Digital 4Q45 versioned transcription](https://lexicon.qumran-digital.org/transcriptions/4Q45/2026-05-21/index.html?v=2026-05-21) — fragment 35, lines 3–4.
- **iaa-4q37:** [IAA Leon Levy Digital Library manuscript record for 4Q37](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q37-1?locale=en_US) — manuscript identity, period, material, publications, and image inventory.
- **iaa-4q51:** [IAA Leon Levy Digital Library manuscript record for 4Q51](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q51-2?locale=en_US) — manuscript identity and institutional image inventory.
- **iaa-4q45:** [IAA Leon Levy Digital Library manuscript record for 4Q45](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q45-1?locale=en_US) — manuscript identity, period, material, publications, and image inventory.
- **dt-ucph-sp-7.1.3:** [DT-UCPH Samaritan Pentateuch Text-Fabric 7.1.3](https://github.com/DT-UCPH/sp) — Deuteronomy 32:8; commit 2f2120286ac48d4ff3d04e0107e33efd864aa9e1.
- **lxx-morph-rahlfs:** [OpenScriptorium lxx-morph Rahlfs Septuagint control](https://github.com/OpenScriptorium/lxx-morph) — Deuteronomy 32:8 and Psalms 144:13a/17; commit c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2; Psalms file SHA256 a34b87a5fbe2857fb453c3bd1bcd2cb0408bb2522b409b6e44d678356ee08103.
- **gentry-2009:** [Peter J. Gentry, The Text of the Old Testament](https://etsjets.org/wp-content/uploads/2010/06/www.etsjets.org_files_JETS-PDFs_52_52-1_JETS-52-1-19-45-Gentry.pdf) — JETS 52/1 (2009), p. 31, comparative apparatus.
- **flint-2010:** [Peter W. Flint, The Significance of the Biblical Dead Sea Scrolls](https://swbtsv7.s3.amazonaws.com/media/Theology_Journal/53.1/53.1_Flint.pdf) — Southwestern Journal of Theology 53/1 (2010), pp. 19–21.
