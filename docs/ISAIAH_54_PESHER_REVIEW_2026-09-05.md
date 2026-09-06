# Isaiah 54:11–12: quotation boundaries and reader-note repair

Checked 2026-09-05. Published-text research, not a new decipherment or complete
Isaiah apparatus collation. The [machine-readable receipt](../sources/textual_restoration/discovery/isaiah54_pesher_review.v1.json)
records sources, qualifications, counterargument and before/after hashes.

## Source result

The missing-commentary queue produced a useful discriminating witness. In
4Q164 frg. 1 line 4, the published quotation tail includes an extra quantifier
before the architectural term. The following explicit interpretation marker
separates it from commentary about twelve figures and the Urim and Thummim.
The preceding biblical words in line 3 are supplied, not preserved. Line 1
mixes interpretive material with foundation wording; its stone word has a
supplied ending. These distinctions prohibit importing whole pesher lines as
the biblical source.

Consulted the 2025-08-25 and 2026-02-11 texts, then followed the version list
to its latest listed release, 2026-05-21. The target main-text readings agree;
this is not a claim of byte-identical pages or independent witnesses.
[Qumran-Digital 4Q164, frg. 1](https://lexicon.qumran-digital.org/transcriptions/4Q164/2026-05-21/index.html),
[version list](https://lexicon.qumran-digital.org/transcriptions/4Q164/changelog.html?v=2025-08-25).
The site credits DFG project 465277421 and displays CC BY-SA 4.0. Its publication
lineage includes Qumran-Wörterbuch and a predecessor by Martin Abegg. This is
not the same licence or exact dataset as the private QDR biblical JSON.

| Control | What this bounded comparison establishes |
|---|---|
| POB WLC, Isaiah 54:12 | No quantifier before “pinnacles”; its “all” belongs later with the boundary phrase |
| 1QIsaa, column 45 line 11, pinned QDR transcription | Contiguous clause without that extra quantifier; no new image reading |
| 4Q164, frg. 1 lines 3–4 | Published quotation tail has the extra quantifier; preceding clause supplied |
| 4Q57, frg. 44–47 line 4 | Architectural term survives, but the preceding gap cannot establish absence of the quantifier |
| 4Q69a, frg. 1 line 3 | The relevant clause is supplied; it cannot establish absence of the quantifier |

The last two controls were checked against their full published lines:
[4Q57, release 2026-02-11](https://lexicon.qumran-digital.org/transcriptions/4Q57/2026-02-11/index.html),
[4Q69a, release 2026-02-11](https://lexicon.qumran-digital.org/transcriptions/4Q69a/2026-02-11/index.html?v=2026-02-11).
Their listed releases are consultation pins, not claims of latest-release use.
The Great Isaiah direct web route failed; its control comes from the locally
hash-verified published QDR transcription, not that unread web page. The private
corpus remains outside Git. Identical editorial cross-references are not extra
manuscript votes.

Outcome: retain the current Hebrew and English provisionally. An early Hebrew
quotation can preserve an important alternative, but adaptation to commentary
is a live counter-explanation here. The wider apparatus and textual history
have not been adjudicated. Neither this quantifier nor the commentary's imagery
settles the English architectural or gemstone terminology. Do not add “all”
before “pinnacles” or translate the biblical noun as the commentary's referent
on this evidence alone.

## Extraction hazard and implemented safeguard

The exact QDR references are `Is 54:11` and `Is 54:12`; the earlier `Isa`
queries returned no hits because the extractor matches exact labels. Corrected
queries return four labels at verse 11 and three at verse 12, not seven
independent manuscripts or seven complete verses.

More consequentially, in 4Q69a physical line 3 the opening supply bracket falls
in verse 11, while its closing bracket falls in verse 12. Filtering words to
verse 12 alone drops the opening bracket and can misrepresent supplied wording
as surviving. Full-line consultation establishes the actual boundary.

Added opt-in `--include-line-context` to the extractor: it retains the original
reference excerpt, adds the complete current physical line and zero-based
selected-word positions, and explicitly leaves preservation unassessed. This
is not automatic bracket-state interpretation; a bracket may start on an
earlier line. Default output is unchanged for existing consumers/receipts.

```sh
.venv/bin/python tools/textual_restoration/extract_qdr_passages.py \
  /private/tmp/pob-qdr/data/qdr.1.1.biblical.json \
  --reference 'Is 54:11' --reference 'Is 54:12' --include-line-context
.venv/bin/python -m unittest tests.test_isaiah54_pesher
```

The private input path is workstation-specific. Its SHA256 is
`3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`.
Use context output for licensed private study, not bulk publication.

## Actual POB change

Moved existing note markers only:

- Isaiah 54:11: a from “afflicted one” to “sapphires”; b from “behold” to “antimony.”
- Isaiah 54:12: b from “sparkling stone” to “pinnacles”; d from “sparkling stone”
  to “boundary walls.” Markers a/c retain their correct ruby/stone targets.

Source text, English lexical wording, note bodies and other YAML bytes remain
unchanged. Tests reverse the exact text replacement and reproduce both baseline
file hashes. Earlier draft/revision/cross-check metadata remain historical;
they do not certify this marker-only repair or imply a fresh independent pass.
The local exporter retains the corrected strings and all six note bodies;
this does not repair or verify the deployed website's separate disclosure path.

## Open evidence and access limits

Direct web requests initially failed; ordinary links from the accessible
edition/version pages later succeeded for 4Q164. No authentication or access
control was bypassed. No HTML snapshot hash, DJD V consultation, manuscript
image inspection or two-family review is claimed. ImageGen was not used.

Next: read the full edition and later reassessments, crosswalk physical images,
compare the full Hebrew/Greek apparatus and discriminating versions, and assess
the vocabulary separately. The six-pesher acquisition task and full Isaiah
coverage remain open. This supplement is not a new formal registry comparison
or source-selection approval; the 26/20/13/1 ledger counts are unchanged.

Verification: 225 repository tests and nine numerical tests passed (234 total),
including seven new preservation-boundary, reversible-edit and export tests.
An actual full `export_book('ISA')` run retained the two notes at 54:11 and
four at 54:12 with every expected anchor; no export artifact was published.
Registry validation and Git whitespace checks passed; 96 local documentation
file-link targets resolved. These checks protect the evidence and editing
boundaries; they do not independently prove the published ancient readings.

## Greek, Syriac and Targum follow-up — 2026-09-05

The [versional supplement](../sources/textual_restoration/discovery/isaiah54_versions_review.v1.json)
adds edition-level controls, not new physical manuscript collations. The prior
pesher receipt and its marker repairs remain unchanged.

| Consulted control, 54:12 | Architecture | “All” before architecture | “All” before boundary |
|---|---|---|---|
| POB WLC | Current English: pinnacles | No | Yes |
| Pinned Rahlfs digital text | Battlements/parapet | No | No |
| CAL Leiden-derived Peshitta | Walls | No | No |
| CAL HaKeter-derived Targum Jonathan, text 1 | Woodwork/timbers | No | Yes |

The Greek comes from the unchanged OpenScriptorium checkout at commit
`c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`, Isaiah JSON SHA256
`c60980806a91bfde385004f5bbc030268f95803503527224ba760330390bed56`.
Read surface fields at 54:11–13, not the dataset's model-generated analyses.
This is Rahlfs edition wording, not a direct Vaticanus reading or the full
Göttingen apparatus. LSJ's defensive sense confirms the Greek architectural
gloss; it cannot independently settle Hebrew semantics.
[Greek dataset](https://github.com/OpenScriptorium/lxx-morph/tree/c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2),
[LSJ, ἔπαλξις, senses 1/1b](https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionaries.v1:lsj-n37987/).

CAL identifies its Peshitta Isaiah as Leiden-derived with selected corrections
from 7a1, not a direct reading of one manuscript. Its lexical tools confirm
wall, jasper and crystal terminology. The Greek and Syriac both lack the
boundary quantifier present in WLC, yet both express “all” with children in
54:13. This is a local contrast, not a whole-book omission-rate study. Therefore
their absence of the extra architectural quantifier does not uniquely recover
a Hebrew omission. Shared gemstones and wording also require a dependence
check before calling them independent support; dependence is not established.
[Peshitta chapter](https://cal.huc.edu/get_a_chapter.php?cset=S&file=62012&sub=54),
[edition basis](https://cal.huc.edu/get_file_info.php?coord=62012&return=/ot_peshitta.html),
[wall lexical analysis](https://cal.huc.edu/getlex.php?coord=620125412&hasvariant=0&word=1).

Targum Jonathan's text 1 gives a wood-related term, contextually woodwork or
timbers, and retains the boundary quantifier. CAL identifies its Bar Ilan text
and distinguishes Sperber variants and toseftot; these are not merged into one
text or counted as independent copies. Its default pointing is converted from
Babylonian to Tiberian conventions. The language is Aramaic despite Hebrew
script. This is further non-uniform interpretation, not recovered Hebrew.
[Targum chapter](https://cal.huc.edu/get_a_chapter.php?cset=H&file=51012&sub=54),
[source/numbering conventions](https://cal.huc.edu/get_file_info.php?coord=51012&return=/showsubtexts.php?subtext%3D51012),
[wood lexical analysis](https://cal.huc.edu/getlex.php?coord=5101254121&hasvariant=0&word=2).

The Hebrew check used Sefaria's documented read-only lexicon API. Its actual
**BDB Dictionary, BDB10425, sense 5** explicitly allows pinnacles/battlements at
Isaiah 54:12. The API also returns an augmented Strong entry; that is a separate
resource, not the consulted full BDB sense. Source metadata identifies Brown,
Driver and Briggs, Oxford 1906. The target sense was read completely after
filtering the initially truncated multi-entry response. No fresh HALOT or DCH
consultation is claimed.
[Exact lexicon query](https://www.sefaria.org/api/words/%D7%A9%D7%9E%D7%A9%D7%AA%D7%99%D7%9A?lookup_ref=Isaiah%2054.12&never_split=1),
[API documentation](https://developers.sefaria.org/reference/get-words).

English assessment: “battlements” is a defensible candidate and more directly
expresses the Greek defensive imagery. “Pinnacles” can suggest a more pointed
or ornamental shape. But the Hebrew lexicon allows both, versions differ, and
the complete source/lexical evidence is still open. Retain POB with its existing
alternative note; do not claim a demonstrated English correction or replace
its ruby/sparkling-stone choices with Greek/Syriac gemstone names automatically.

No source, English, notes, canonical metadata, selection gate or deployed reader changed.
Registered the particular Targum edition and extended existing Greek/Peshitta
coverage: now 27 mixed registry entries, still 20 physical coverage records,
13 formal comparison cases and one unpromoted selection. New checks protect
the distinction between edition wording, version interpretation and Hebrew
inference. Full book apparatuses, physical witnesses and review remain pending.

Follow-up verification: 230 repository tests plus nine numerical tests passed
(239 total); the saved Greek excerpt exactly reproduced from the hash-pinned
real input. Registry validation passed at 27/20/13/1, 105 local Markdown
file-link targets resolved, and Git whitespace checks passed. The new five
tests check versional distinctions, unchanged canonical files and lexical
source identity, not historical priority or independent translation approval.

## Printed Greek apparatus follow-up — 2026-09-05

The [Swete receipt](../sources/textual_restoration/discovery/isaiah54_swete_review.v1.json)
adds a visually checked printed control. Volume III is the **1905 third
edition**, established from its title and edition-history pages, not the
1909–1930 range formerly given in the local README. The downloaded PDF matches
the existing manifest hash, has 932 PDF pages, and places printed page 202 at
one-based PDF page 226. The complete target page, including the apparatus,
was inspected; OCR served only to locate it.
[Source scan](https://archive.org/download/theoldtestamenti03swetuoft_202003/theoldtestamenti03swetuoft.pdf).

At 54:12 the printed main text lexically agrees with the earlier Rahlfs control:
architectural battlements, jasper, crystal and selected
stones, without “all” before either architecture or boundary. The final word
has an acute in Swete and a grave in the pinned digital control; source forms
remain unchanged. Raw-string identity initially failed a test, which now
checks this explicit difference instead of hiding it. Verse 13 has
the children quantifier. The verse-12 apparatus reports three spelling loci,
including `επαλξις א* (-ξεις אc.b)`; the crystal report carries `vid` and must
retain that uncertainty. No addition of the disputed quantifier is reported
there. These are edition reports, not freshly verified manuscript readings
or independently dated correction hands. The receipt deliberately does not
construct complete manuscript verse strings from the selective apparatus.

The page has base siglum B and apparatus margin א/A/Q. The volume's sigla list
identifies Vaticanus, Sinaiticus, Alexandrinus and Marchalianus respectively.
Introduction v–vi explains the generally Vaticanus-based Prophets; viii–ix
distinguishes Marchalianus annotations from its text. Page x explicitly warns
that silence of the palimpsest Cryptoferratensis **Γ** can result from inability
to decipher. OCR misrenders Γ as F. Γ is not in this target page's apparatus
margin, and no omission vote is assigned to it. A book-level list of available
manuscripts is not passage-level attestation.

Decision: retain POB provisionally. This improves the provenance of our Greek
control but adds no independent ancient witness and does not prove universal
Greek agreement or a unique Hebrew retroversion. The prior versional counter-
explanation remains live: Greek also lacks the WLC boundary quantifier. No
source, English, notes, application gate, About content or deployment changed.

Next full-apparatus target is specifically Ziegler's *Isaias*, Göttingen XIV,
third edition (1983), verified in the project's publication list. Only that
bibliography, not its full Isaiah 54 apparatus, was consulted in this pass.
[Göttingen publication list](https://septuaginta.uni-goettingen.de/publications/septuaginta/).
Direct manuscript/hand checks, full Hebrew apparatus and pesher priority remain
open. The new tests protect edition identity, bounded apparatus claims and
unchanged POB files; they do not independently validate the ancient readings.
