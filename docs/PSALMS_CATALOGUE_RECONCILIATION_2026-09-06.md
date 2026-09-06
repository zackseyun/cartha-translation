# Psalms catalogue reconciliation — 2026-09-06

## Result and scope

The existing Psalms book-map's **39 labels and 1,261 indexed anchors are all accounted for** in this bounded target list. This is not 39 independently verified manuscripts, nor 1,261 verses of surviving ink. The new coverage result is that 14 further literary-context target names lie outside the pinned QDR **biblical** file: 13 have exact labels in its sibling **non_biblical** file and in the full Qumran-Digital index; `4Q173a` does not. No new reading, translation, manuscript coordinate, or canonical change is accepted.

The list contains 53 catalogue/query targets, plus three separately excluded historical provenance holds. It is not a census of all Psalm witnesses, quotations, allusions, or ancient versions. It follows the existing Leviticus/Isaiah reconciliation pattern of explicit names, dataset-local ordinals, and unresolved identity, but adds a **label-only** check of the sibling nonbiblical dataset. The 2014 catalogue is not represented as a 2026 completeness statement.

Artifacts:

- `sources/textual_restoration/discovery/psalms_catalogue_targets.v1.json`: agent-reviewed sources, roles, exact query labels, source discrepancies, and historical holds.
- `sources/textual_restoration/discovery/psalms_catalogue_check.v1.json`: reproducible metadata receipt, including every biblical ordinal/anchor count, nonbiblical label ordinal, and modern catalogue link/class/version/ordinal.
- `tools/textual_restoration/check_psalms_catalogue.py` and `tests/test_psalms_catalogue.py`: bounded checks; existing tools and frozen files are unchanged.

## Sources actually consulted

Peter W. Flint's [Appendix II, *Contents of the Psalms Scrolls and Related Manuscripts*](https://academic.oup.com/edited-volume/35006/chapter/298748365), *The Oxford Handbook of the Psalms*, pp. 630–638, published **28 March 2014**, supplies the catalogue baseline. The [publisher's expanded table](https://academic.oup.com/view-large/343713300) was directly readable. It distinguishes copies from quoted/excerpted material and retains uncertainty and continuity signs. The HTML renders duplicate table rows; no manuscript totals were derived from rendered row counts.

[Appendix I](https://academic.oup.com/edited-volume/35006/chapter/298748176), pp. 621–629, same publication date, supplies composition-context checks, especially its Catena discussion and Texts 17–18. Publisher HTML and text returned by publisher-domain search were consulted; some later chapter-open calls failed on a redirect-safety error. No access wall was bypassed. No DJD edition, apparatus, PDF, or image pixels were consulted in this pass.

IAA institutional catalogue titles/metadata were checked for [4Q380](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q380-1?locale=en_US), [4Q381](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q381-1?locale=en_US), [4Q382](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q382-1), [4Q173](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q173-2), [11Q11](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/11Q11-1?locale=en_US), [5/6Hev Psalms](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/5_6Hev%201b%20891-1?locale=en_US), [Mas 1e](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/Mas%201e-1?locale=ar_EG), and [Mas 1f](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/Mas%201f-1). Some direct pages exposed only their title shell; fuller metadata came from the institutional page text returned by search. Catalogue publication dates are unspecified, not inferred from image dates. Bibliographic links and image inventories are **leads**, not claims that the cited editions or images were inspected. User comments on image pages were not treated as institutional evidence.

The full **2026-09-05 snapshot** of the [Qumran-Digital index](https://lexicon.qumran-digital.org/transcription-index/latest/index.html) was reparsed, not just the previous 269-row exported subset. This matters: that subset intentionally omitted nonbiblical-class entries lacking biblical-QDR matches. All relevant listed transcription versions are **2026-05-21**; this is a listed version date, not a date of transcription consultation. Qumran-Digital and Qumran Digital Reader are separate projects.

## Coverage accounting

| Check | Result | Meaning |
| --- | ---: | --- |
| Bounded catalogue targets | 53 | Names/query scopes, not independent physical objects |
| With scoped hits in biblical QDR | 39 | All current Psalms book-map labels |
| Biblical-QDR Psalm anchors | 1,261 | Reference tags, not verified ink |
| Biblical-QDR labels outside this list | 0 | Closed only against this frozen index |
| Supplemental target names outside biblical QDR | 14 | Includes literary compositions and a Psalm154 target |
| Exact target labels in nonbiblical QDR | 16 | 13 supplemental plus three overlapping collection labels |
| Target names matched in full modern index | 52 | Label-level links, not verified aliases/readings |
| Historical provenance holds outside target counts | 3 | No accepted manuscript identity/readings |

The three cross-file overlaps are `4Q88`, `11Q5`, and `11Q6`. Their biblical/nonbiblical record ordinals are respectively **144/87**, **233/668**, and **234/669**. They must not generate six witnesses or three newly discovered copies. Their modern catalogue class is `dss`, not `dss-biblical`, consistent with treating mixed collections carefully; CSS class does not settle ancient genre or textual authority.

The frozen WLC-labelled denominator remains 2,527, with 1,266 anchors lacking a same-labelled biblical-QDR reference tag. Nothing here converts that difference into lost words or missing manuscript verses. Psalm154 and other compositions outside the 150-Psalm denominator need separate discovery accounting, not false WLC-gap closure.

## Supplemental literary-context targets

All entries below have **no exact label in the biblical file**. NB ordinals are zero-based within `data/qdr.1.1.non_biblical.json`; QD ordinals are one-based within the full pinned catalogue. Labels are exact, including suffixes and case. The target JSON records source locators and uncertainty; references are catalogue-reported research leads, not independently checked survival.

| Exact label | Role / bounded comparison lead | NB ordinal | QD ordinal |
| --- | --- | ---: | ---: |
| `1Q16` | Pesher; Psalms57/68 | 9 | 9 |
| `1QHa` | Hodayot; quoted/excerpted Psalm26:12 | 6 | 6 |
| `4Q171` | Pesher; Psalms37/45; uncertain60 **or**108 | 106 | 109 |
| `4Q173` | Pesher; Psalms127/129; source spelling conflict below | 108 | 111 |
| `4Q173a` | House of the Stumbling Fragment; Psalm118:20 | absent | absent |
| `4Q174` | Florilegium; Psalms1/2/5 | 109 | 112 |
| `4Q176` | Tanhumim; named in catalogue introduction, precise Psalm locus unresolved here | 111 | 114 |
| `4Q177` | Catena A; multiple Psalm excerpts | 113 | 117 |
| `4Q380` | Non-Canonical Psalms A; no canonical-Psalm locus established here | 364 | 346 |
| `4Q381` | Non-Canonical Psalms B; Psalm18/86/89 reuse leads | 365 | 347 |
| `4Q448` | Psalm154 excerpt within another composition/prayer context | 443 | 425 |
| `4Q522` | Prophecy of Joshua containing Psalm122 | 556 | 538 |
| `11Q11` | Psalm91 in exorcistic/liturgical context | 671 | 650 |
| `11Q13` | Melchizedek; Psalm82 quotation | 673 | 652 |

The nonbiblical check reads only `scroll` labels and record ordinals. It does **not** scan Psalm reference tags, export transcription, or count preserved words in that file. Passage-level comparison must distinguish quoted lemma, paraphrase, commentary, restoration, and actually visible letters.

## Identity and source conflicts retained

1. Appendix II's introduction prints **4Q381–82** for Non-Canonical Psalms A/B. The IAA identifies **4Q380=A**, **4Q381=B**, and **4Q382=papParaphrase of Kings**. This supports an apparent numbering error, not a reason to relabel 4Q382 or turn it into another Psalms target.
2. The Psalm127/129 rows print **1Q173**, whereas the introduction names **4Q173** and IAA's 4Q173 page is Pesher Psalms B. The query uses the supported `4Q173` candidate but retains the inconsistent source form. `4Q173a` is neither truncated nor reassigned to `4Q173`/`4Q174` when absent.
3. Appendix II assigns **Psalm18:26–29** to **MasPsa (M1039–160)**. The candidate `Mas1e` record260 has only Psalm81–85 tags: 16/8/19/13/6 anchors respectively. This is an **unresolved catalogue/index conflict**, not evidence of a missing Psalm18 fragment. Inspect the actual Masada edition and object inventory before choosing between a catalogue error, alias problem, or genuine digital omission.
4. The source assigns Psalm109:3–4(?) to **11Q5 or 11Q6** and marks **11Q9** uncertain at Psalm50. Neither ambiguity is erased by exact QDR label matches. Alternative identifications are not extra witnesses.

## Non-Qumran coverage and historical holds

`5/6hev1b` (biblical ordinal249, 138 anchors) is the typography candidate for modern `5/6Hev1b` and the catalogue's 5/6HevPs. The IAA page locates its Psalms material in the Cave of Letters and uses `5/6Hev 1b 891`; a separately surfaced `*103` catalogue form must not be counted as another manuscript merely because there are multiple archive pages. Fragment-to-page joins are still unverified.

`Mas1e` (ordinal260, 62 anchors) and `Mas1f` (ordinal261, 8 anchors) are candidates for MasPsa and MasPsb. The IAA labels support the Masada/copy-letter association; they do not independently verify the older M-number crosswalk or the disputed Psalm18 allocation. Thus non-Qumran material is included without treating findspot labels as interchangeable with Qumran cave numbers.

The 2014 names **XQPs A (Schøyen Ps)**, **XQPs B (Green Ps)**, and **XQPs C (SwB Ps)** are recorded as historical provenance leads only. Their reported Psalm loci are retained in the JSON, but no present-day inventory crosswalk, excavated provenance, or object-specific authenticity determination was established. They are excluded from target/match totals and reading support. This pass neither authenticates them from a 2014 table nor blanket-labels all three forged without object-specific evidence.

## Concrete next comparisons, in priority order

1. **11Q11 / Psalm91:** consult DJD XXIII, pp.181–205 (IAA bibliography) and the matching plate/fragment context; compare the Psalm portion against `4Q84` and versional apparatus. Do not promote exorcistic framing or restored text to a new Psalm reading.
2. **4Q522 / Psalm122:** inspect the published Psalm-bearing portion, compare `11Q5`, and keep the surrounding Joshua composition separate. **4Q448 / Psalm154** requires its own extra-Masoretic composition scope; Appendix I Text17 does not describe a complete copy of Psalm154.
3. **4Q171 / Psalms37,45** and **4Q173 / Psalms127,129:** resolve edition fragment numbering and source spelling first; compare lemmas separately from interpretation. Keep the 60/108 alternative as one unresolved attribution.
4. **MasPsa / Psalm18 discrepancy** and **4Q173a identity:** edition/catalogue resolution before adding coverage. Exact absence from these three digital surfaces does not show that an ancient text is absent.
5. **11Q5/11Q6 Psalm118 Catena, 11Q5 Psalm145, 4Q98 Psalm33, and 4Q98g Psalm89:** source-reported extra material/order makes these useful comparison candidates. An English consequence would require establishing whether the difference is preserved wording, collection order, an excerpt, or editorial reconstruction; this pass supplies none.

## Reproducibility and limits

Both private QDR files were checked at commit `f54f38464e18409eed8286fe24dd24f88d4735dd`. The biblical input hash is the existing pin; the nonbiblical SHA-256 is `16edab67449e00ffda01368c78692f3a5bf311d0f0341926c9e2e658bc00d4ac`. The full modern-index SHA-256 is `e1211f26d0c37ac46bc7c8cdb23587393742abaef80fcce001bb8b90752683f5`. The receipt also pins target and checker/reconciler/scanner/parser bytes. Agent-consulted source claims are separately attributed and are not certified by the metadata program.

```sh
/Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/textual_restoration/check_psalms_catalogue.py /private/tmp/pob-qdr/data/qdr.1.1.biblical.json /private/tmp/pob-qdr/data/qdr.1.1.non_biblical.json /private/tmp/pob-qumran-digital-index-2026-09-05.html --verify-only
/Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -s tests -p test_psalms_catalogue.py -v
```

Validation on 2026-09-06: **8 tests passed** (initial run 0.004 s); the real-input `--verify-only` receipt check and `git diff --check` passed. The unit tests check exact/suffix-sensitive labels, dataset-local ordinals, cross-file overlap, input-pin failure, frozen book-map agreement, retained source conflicts, and no reading-support promotion.

The checked sources identify realistic next targets and expose the biblical-file scope gap. They do not close manuscript survival, authenticity, Greek/Syriac/versional apparatus, medieval Psalter coverage, translation, or physical identity. No restricted corpus text, complete verse index, source image, or edition was copied into the repository.
