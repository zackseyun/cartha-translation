# 2 Samuel 13:37: exact disclosure candidate

Date: 2026-09-06. Research-only, unapproved and unapplied. Checkpoint:
`b7ad6bd106b88ba90b6ecd9a1d3a82573cf7774e`. The
[machine record](../sources/textual_restoration/applications/samuel13_37_disclosure_candidate.v1.json)
contains the **complete original and candidate YAML as exact UTF-8 strings**,
their hashes, all seven field changes, archival values and actual export checks.
This is not a canonical writer or an application transaction.

## Reader-facing proposal

> But Absalom fled and went to Talmai son of Ammihur[a], king of Geshur. And he mourned[b] for his son all the days.

**a — new name disclosure (`textual_variant`):**

> 'Ammihur' follows the written form in the retained Hebrew source; its traditional reading (qere) is 'Ammihud.' Aleppo's written form also ends in r; the revised Leningrad transcription ends in d, with uncertainty about the preceding letter. These written forms also differ from the qere in another Hebrew letter. The consulted Greek and Syriac texts have d-ending forms, while the Latin Vulgate has 'Amiur.' In the published Dead Sea Scroll transcription of 4Q51, the name is supplied in a gap. The earliest form remains uncertain.

**b — existing mourning note, body and reason unchanged (`lexical_alternative`):**

> The subject of 'he mourned' is implicit in Hebrew and is understood from context to be David.

The old note's identity is explicit in the before/after record: its former
marker **a** becomes **b**, and it moves from the name to “he mourned.” New
note **a** belongs to Ammihur. Normal reading order is a, b; no duplicated or
unbound markers are permitted. The sole added main-line bytes are `[b]` after
“he mourned”; the meaning of existing `[a]` changes through its new note body.
No marker-free English word, punctuation or space changes.

## Why this narrow change

The [reviewed Hebrew controls](SAMUEL_13_37_HEBREW_CONTROLS_2026-09-06.md),
[version controls](SAMUEL_13_37_VERSION_CONTROLS_2026-09-06.md), and
[independent research review](../sources/textual_restoration/discovery/samuel13_37_controls_review.v1.json)
establish a disclosure problem, not authority to replace the name. WLC's
retained written form and Aleppo's body have het–vav–resh; the published UXLC
Leningrad transcription has het–vav–dalet with a separate vav/yod uncertainty;
the qere has he–vav–dalet. Thus neither a shared English transliteration nor
“d-ending” equates every Hebrew letter. The consulted Greek/Syriac forms are
not unanimous version evidence: Vulgate Amiur is a contrary control. QDR's
4Q51 patronymic is supplied, not surviving ink. Detailed authority/sigla and
rights boundaries remain in the research dossiers rather than the reader note.

The note deliberately does not call Ammihur original, or the corrected
Leningrad transcription identical to the qere. The strongest objection is
that retained Ammihur may not best transcribe Leningrad, while the d-ending
controls deserve serious consideration. The strongest counterweight is the
independent Aleppo written resh and Vulgate Amiur, together with the absence
of surviving patronymic letters in this DSS transcription. Direction of change
remains unresolved. A source correction, qere-based English name, and earliest
form reconstruction are different decisions; none is made here.

The defect in the old note placement is direct: a reader selecting Ammihur
currently receives an explanation of “he mourned,” not of the name. The
existing mourning explanation is preserved, not expanded with King David,
Amnon, geographical material, or version-specific duration.

The controlling method, source-near standard, `DOCTRINE.md`, both repository
revision documents and the full revision-prompt policy were read and pinned.
Q1: the name identifies Talmai's father; the subsequent source clause reports
mourning with an implicit subject. Q2: the main English is retained; its defects
here concern disclosure and attachment, not a proved mistranslation. Q3: the
patronymic rationale addresses the construction/article but not the variation;
the mourning rationale expressly engages David's contextual identification.
All lexical decisions therefore remain unchanged, including historical HALOT
labels; no fresh lexicon consultation is implied. Current 13:36–39 context
was read. Other anchors in neighboring verses and 13:39's contested wording
are outside this scope, not certified by this candidate.

The reader note is necessarily more technical than the original sole note:
“qere” is glossed immediately, but the manuscript names and spelling distinctions
still add reading load. That is the main readability tradeoff. Dropping the
contrary version or the supplied-text qualification would make the account
simpler but less adequate to this documented dispute. Independent judgment may
still require a tighter formulation; the research PASS is not candidate approval.

## Exact change and provenance boundary

| Component | Before → candidate |
| --- | --- |
| `translation.text` | Add only mourning anchor `[b]`; name anchor stays `[a]` |
| `translation.footnotes` | New name note a; old note body/reason preserved as b |
| `status` | `revised` → `draft` |
| `revision_pass` | Remove live field; preserve complete old object in history |
| `cross_check` | Preserve complete old object in history; current `needs_review`, no old scores |
| `review_history` | Add exact old status/revision/cross-check values, bound to this baseline |
| `note_proposal` | Add explicitly unapproved/unapplied scope and provenance disclaimers |

The original input hashes of the old model reviews are **not verified**. Their
archival binding identifies the baseline file from which values were copied,
not an invented earlier input. They do not certify the new note. `ai_draft`
and the complete lexical block remain byte-identical; the source block and
edition WLC remain byte-identical. The exact original 4,069-byte YAML is retained
in the machine record; the candidate is 6,146 bytes. No current approval score,
fresh revision timestamp or fabricated reviewer is added.

- Baseline SHA256: `b6ce63c3ce743f13332997712d04a70258d6844b24428d74556ee58794f87e22`.
- Candidate YAML SHA256: `63d80b610ed4c20bc4da1b4716447727cdda57a70c1a75bd8545fc7b90c8ada1`.
- New note UTF-8 SHA256: `043ae830d69cfbea5ff5d1b50e355a001a5f2f8ebeed62b3a247b7395060a531`.

## Actual checks and what they do not certify

Using the repository Python environment and existing exporter/helpers, the
complete **2SA book** was exported twice: the actual baseline, then a single
in-memory target overlay. Both contain **24 chapters / 695 verses**. The exact
target text and both notes survive in a, b order; replacing the candidate row
with the baseline row makes all other exported content identical. A manifest
of all 695 input YAML hashes is unchanged before/after export. No canonical
file, generated asset or deployed reader was written.

The candidate passes the existing verse schema. The baseline already fails
its `status` enum because the schema allows `draft`, not `revised`; this is
reported, not suppressed. The status reset is independently required because
the old review cannot approve new note bytes. Source metadata is omitted by
the mobile exporter by design: the helper's `draft_source_preserved: false`
is therefore a transport limit, not a source-YAML difference.

An additional read-only check reconstructed the expected parsed record using
the seven exact declared changes, required full-record equality, the complete
expected marked English string and exactly one marker each in order a, b.
Four negative controls were rejected: duplicate inline marker, reversed note
order, unrelated lexical edit, and altered archived agreement score. The saved
baseline/candidate UTF-8 hashes and all 15 derivative pins were rechecked.
These are bounded integrity tests, not a newly frozen executor or the full
repository regression suite.

## Dependencies before any application

Fifteen matching `translation_*` records are pinned unchanged as context. Their
source equality does not certify English-note freshness. The simplified record
has the old English base note/anchor and explicitly names David and Amnon in
its main text. German has an old English base snapshot but already attaches its
own mourning note to the pronoun. Neither is rewritten, synchronized or newly
approved; an English 2SA export is not multilingual publication.

Known affected history includes the research review's exact canonical binding,
both Samuel control receipts, earlier image receipts and the UXLC comparison's
canonical join. The all-OT current digest also changes under a future application.
The existing Genesis→Jeremiah→Numbers sample replay must remain frozen; a
separately reviewed, exact fourth-target historical wrapper would be needed,
with actual current digest/export measured outside overlays and unknown drift
rejected. This is a bounded dependency inventory, not an exhaustive guarantee.

Next gate: independent judgment of these exact candidate bytes, then a separate
application design and integration audit if authorized. No transaction intent,
canonical application, whole-verse approval, earliest-source promotion,
multilingual synchronization, image relicensing or publication approval is
created by this package.
