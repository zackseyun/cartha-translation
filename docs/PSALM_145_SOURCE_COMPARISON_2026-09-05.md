# Psalm 145: presence is not exact wording

Checked 2026-09-05. This upgrades the existing provisional pilot with directly
consulted edition/transcription controls; it is not a newly discovered variant.

| Consulted control | Corresponding line | Designation | Words phrase | Second-colon adjective |
|---|---|---|---|---|
| WLC Hebrew | Absent | — | — | — |
| 11Q5 published Hebrew | Present | God | in his words | חסיד, here glossed loyal |
| Rahlfs Greek 144:13a | Present | Lord | in his words | ὅσιος, holy/pious |
| CAL Peshitta 145:13 | Present | Lord | in his words | ܙܕܝܩ, righteous |
| CAL Targum 145:13→14 | Absent | — | — | — |

Only 11Q5 is a newly mapped individual manuscript here. Edition controls are
not manuscript votes. None of the three present-line controls in this first table explicitly has
“all” before words; all have it before deeds/works.

The Hebrew line occupies XVII 2–3: the final word of line 2 and first five
printed words of line 3, without supplied-letter brackets or uncertainty marks
in this excerpt. The recurring blessings are separate units. The second colon
recurs at verse 17, XVII 9–10. This is published-text evidence, not freshly read
pixels. [Qumran-Digital 11Q5, version 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/11Q5/2026-05-21/index.html?v=2026-05-21).

The Syriac control has “righteous” here but “merciful” in its verse 17's second
colon. That does not prove a different underlying Hebrew adjective. Its text
is Leiden-derived with selected 7a1 corrections, not a direct reading of one
manuscript. An attempted lexical-link request returned an unrelated entry and
was excluded. [Peshitta chapter](https://cal.huc.edu/get_a_chapter.php?cset=S&file=62027&sub=145),
[edition information](https://cal.huc.edu/get_file_info.php?coord=62027145).
The Targum display moves directly from kingdom/dominion to supporting the fallen;
this does not certify absence in every copy.
[Targum chapter](https://cal.huc.edu/get_a_chapter.php?cset=H&file=81002&sub=145).

## Reproducible checks

The [receipt](../sources/textual_restoration/discovery/psalm145_control_check.v1.json)
checks 21 WLC poetic openings, excluding only the verified two-word title in
verse 1. Their sequence lacks nun. It also verifies bounded QDR morphological
tokens against the separately consulted Hebrew and the Greek suffixed reference
`Ps 144:13a`. A verse-tag-only extraction includes flanking blessings; an
integer-only Greek importer misses the added line. Neither index agreement nor
acrostic completion proves historical priority or legible ink.

QDR commit `f54f38464e18409eed8286fe24dd24f88d4735dd` and Greek commit
`c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2` are external pinned inputs.
The receipt exports hashes and mapping metadata, not full corpus text.
CAL displays were consulted live, not frozen or fully imported.

```bash
.venv/bin/python tools/textual_restoration/build_psalm145_check.py /path/to/qdr.1.1.biblical.json /path/to/lxx-morph/db/seeds/lxx_morph/psalms-lxx.json --verify-only
.venv/bin/python -m unittest tests.test_psalm145_check tests.test_ot_witness_registry
```

## Decision and POB impact

Retain the earlier moderate working preference for considering inclusion,
without selecting exact wording. Early Hebrew attestation and the alphabetic
position support inclusion; early acrostic repair using familiar language and
verse 17 is a substantial counter-explanation. The scroll's recurring blessings
show a different form, not that every difference is secondary. These are
editorial hypotheses, not observed scribal intentions. Removing the modest
chronological preference leaves structural evidence but no decisive direction
of change.

Keep inclusion, divine designation, “all” before words, and the adjective
separate. The [POB note](../translation/ot/psalms/145/013.yaml) now quotes a
working translation of the Hebrew witness: “God is faithful in his words and
loyal in all his deeds.” It discloses Greek's designation and retention of MT.
“Loyal” is a lexical choice, not the only possible English equivalent. Hebrew
source and English main words are unchanged. Old review scores do not certify
this new note; its review was one context-informed Codex pass plus consistency
tests, not an independent blinded review.

The formal ledger has 13 cases and 20 coverage records, not 20 completed
collations; the first pass had 22 registry entries, now 25 after the Latin
follow-up below. The existing pilot, sample,
English-impact baseline and generated reports have been synchronized.

## Latin follow-up: an edition is not a uniform tradition

The earlier pilot's blanket “Jerome's Hebrew Psalter lacks the line” is too
broad. Direct consultation produces this more precise record:

| Consulted edition | Corresponding line | Qualification |
|---|---|---|
| Weber–Gryson 2007, *iuxta Hebraeos*, publisher VUL | Absent | Edition-specific absence, not a physical lacuna |
| Weber–Gryson 2007, *iuxta LXX*, publisher VULA | Present | Lord; **all** his words; holy in **all** his works |
| Harden 1922, *iuxta Hebraeos*, p. 187 | Present | Same two “all” qualifiers; apparatus explicitly reports omission in A H R |

Both publisher pages label this Psalm 144; Harden labels it 145. Opening and
flanking clauses confirm alignment with POB Psalm 145. The publisher's
Hebrew-based display passes from mem to samech without the corresponding line.
Its Greek-based display includes it. Neither full modern apparatus was
available in these displays.
[Hebrew-based text](https://www.die-bibel.de/bibel/VUL/PSA.144),
[Greek-based text](https://www.die-bibel.de/en/bible/VULA/PSA.144).

Harden's printed p. 187 (PDF page 223) was visually checked, not merely OCR-read.
His apparatus has `om. clausulam fidelis ... operibus suis AHR`. In **Harden's**
sigla, A is the Amiatine Psalter, H Codex Hubertianus (Add. 24142), and R the
Ricemarch Psalter (Trinity College Dublin A 4. 20). These are the editor's
historical identifiers, not newly checked holding-library records. The sigla
and method pages were also visually checked (xi–xii, xvii–xviii, xxix).
Harden warns that his A evidence comes through problematic earlier collations.
His selective apparatus states exceptions to inference from silence; we retain
the explicit A H R report without manufacturing individually verified readings
for every unmentioned witness.
[Harden's digitized edition](https://archive.org/download/psalteriumiuxtah00lond/psalteriumiuxtah00lond.pdf).

PDF SHA256: `e65a762914345706c36631d68da0bd0f6d4a87afd3230c705bc08101620b015e`.
The three edition records add no physical passage-coverage records. The full
PDF is retained outside the repository; only bounded evidence and provenance
are recorded here. Modern publisher displays were consulted live, not frozen.

This corrects attribution and verifies a Latin “all his words” form; it does
not recover that word in Hebrew. Cross-influence between Latin Psalters is a
possibility to test, not an established explanation for this unit. Neither
Harden's inclusion nor Weber–Gryson's omission alone settles Jerome's initial
Latin text, its Hebrew exemplar, or the earliest Hebrew Psalm. The moderate
working inclusion preference is unchanged, exact wording remains unresolved,
and this follow-up changes no POB source or English main text.

## Open evidence

Inspect full Hebrew/Greek/Syriac apparatuses, the late Hebrew marginal hand,
and the modern Latin apparatus and manuscript attestations behind the edition
disagreement above. Old Latin and Roman Psalter coverage remains open; the
three editions do not complete Latin collation. Brettler's *Supplementation in Psalms:
Illustrations from Psalm 145*, pp. 3–20, is an important follow-up: only its
publisher preview/metadata were accessible, not the full argument.
[Publisher record](https://www.jstor.org/stable/j.ctvvnhmb.5).

The LOC exhibition confirms the displayed nun-line witness and Sanders
publication. Its object-page route returned 403; current custody, image rights,
region mapping and new paleographic review remain unverified, as recorded in
the coverage ledger. [LOC captions](https://wwws.loc.gov/exhibits/scrolls/bib.html).
ImageGen would illustrate known wording, not recover ancient letters. No
generated image or fresh restoration was used; source promotion remains open.
