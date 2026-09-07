# Ruth 3:15 — who entered the city?

Checked 2026-09-06 (local date), following the Exodus count closeout.
**Retain the masculine Hebrew and “he” provisionally; improve disclosure and
repair two misplaced anchors.** This expands passage comparison to Ruth, not
to a claim that Ruth's manuscripts have been fully collated.

Baseline: `d0bf3da4c2bc374ca1cae1016f9108c39adf46ce`;
[verse](../translation/ot/ruth/003/015.yaml) SHA256 before change:
`b669e6cbf77909ae35bc87eb0c3439cb0451aaca075345d907094506ce42073e`.
The target came from the existing local-note inventory, not a new casebook
or infrastructure project. No previous dedicated Ruth 3:15 dossier was found.

## Evidence that actually distinguishes the alternatives

The current WLC source has masculine ויבא, not feminine ותבא. This is a
consonantal difference, not just a choice of vowel pointing. In context,
“he” continues Boaz's measuring/loading actions and fits his gate business
in 4:1. “She” follows Ruth carrying the gift and reaching Naomi in 3:16–17.
Either could be a contextual assimilation; narrative smoothness alone cannot
determine direction. No critical Hebrew source change is justified here.

[Qumran-Digital 2Q17, version 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/2Q17/2026-05-21/index.html),
fragment 1, complete lines 1–7 were checked. Line 4 begins with preserved
loading-related wording, but the supply bracket opens within barley and runs
through the arrival clauses into verse 16. The disputed verb is wholly
supplied, not another ancient vote for “he.” This published transcription is
not a fresh image reading. Its displayed WLC comparison must also not be
mistaken for fragment ink. The full pinned QDR index gives target-reference
hits only in 2Q17 fragment 1 lines 3–4; this is dataset coverage, not an
exhaustive manuscript census. Both transcriptions of 2Q17 represent one object.

The local Rahlfs surface-text control has `καὶ εἰσῆλθεν εἰς τὴν πόλιν` at
Ruth 3:15, without an expressed subject. This third-person finite verb does
not mark gender. Verse 16 explicitly names Ruth; that permits either a
continuation or a change of subject. An English “she” translation of the
Greek must not become an independent attestation of Hebrew ותבא.

The [CATSS Ruth parallel text and variants](https://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxvar/2Historical/08Ruth.html)
identifies its variants as Wright/Kraft's larger-Cambridge-based transcription
(ca. 1984; HTML/Unicode conversion 2008), not Rahlfs's own apparatus.
Units 3:15(3400) and (3500) report additions of Ruth (`l o e₂`) and Boaz (`w`)
respectively. These are source-local sigla, not newly resolved shelfmarks or
independently read manuscripts. Thus explicit subjects occur in reported
Greek variants even though the checked base verb itself is gender-neutral.
No claim of Greek unanimity, earliest Greek priority, or modern Göttingen
apparatus consultation follows. The header and target/adjacent units were read.

[SIL's published translator notes, 3:15c](https://tips.translation.bible/story/sil-translators-notes-on-ruth-315/)
report “she” for Syriac and Vulgate and recommend retaining “he.” This is an
attributed versional report, not our direct collation of those versions.
Their recommendation is not an additional witness. The stronger alternative
and its narrative argument remain open; the project's retention is provisional.
Unidentified Hebrew manuscripts mentioned in search results have not been
assigned identities, dates or readings by this pass.

Local input SHA256 values (only Greek surface fields used):

- `/private/tmp/pob-lxx-morph/db/seeds/lxx_morph/ruth.json`:
  `12a6e181fca2a04b6f073974af676a9c6a32f144062541d370d20af6c3d6e249`.
- `/private/tmp/pob-qdr/data/qdr.1.1.biblical.json`:
  `3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`.

## Applied correction and independent review

Marker `a` now follows the six measures of barley, not “said”; marker `b`
now follows the city clause, not “on her.” The revised textual note separates
Hebrew gender, reported versional readings, Greek ambiguity/explicit-name
variants, and 2Q17's supply. Modern translations are no longer presented as
textual witnesses. Related lexical and theological rationales now explain the
provisional retention without unverified manuscript or translator-count claims.
Hebrew and marker-free main English are unchanged.
Old review objects are preserved verbatim under historical keys; the current
record is draft/needs-review, not an inherited approval of the new note.

`/root/ruth_subject_review` independently read the local Hebrew context and
Greek surface text, agreed with provisional retention and identified both
anchor defects. Its single candidate follow-up approved the proposed disclosure
on root's external-source observations; it did not independently inspect those
external sources or manuscript images. Final wording says “a published Greek
apparatus” to avoid misidentifying CATSS as Rahlfs's own apparatus. This is
scoped editorial review, not a vote establishing earliest wording.

## Access limits and stopping condition

The unversioned 2Q17 URL failed; search supplied the working versioned URL.
The Tully Peshitta paper returned a verification page, not its contents, and
the Sefaria opened page exposed only navigation. Neither was used as a read
paper or verified manuscript list; no repeated failed acquisition followed.
A local shell glob matched no tools and was abandoned for direct dataset
inspection. No image restoration, ImageGen, new schema or validator was needed.

Reopen source selection for a named Hebrew variant/hand or an actually consulted
critical apparatus that provides a discriminating transmission argument.
Direct Syriac/Latin consultation could refine the report but cannot by itself
turn contextual gender into preserved Hebrew. Do not repeat the bare Greek
gender check or treat 2Q17's verse-range coverage as preserved verb evidence.
The all-OT/NT objective remains unfinished; this is one newly examined unit.

## Executed verification

Verse schema, exact allowed record delta, unchanged source and marker-free
English, exact preservation of historical review objects, and the two new
anchor locations passed. Full before/after `export_book('RUT')` comparison
matched every canonical source identifier: four chapters, 85 verses. The only
reader-output changes were target text markers and note `b`; the baseline
export substituted the Git baseline target through the existing record loader.
Eight `tests.test_reader_footnote_export` tests and Git diff checks passed.
No new validation code was added. These checks establish scoped integration,
not earliest-text accuracy or approval of every Ruth verse.

- Applied verse SHA256:
  `3e5b9d185c1e660e409825f09ca6f6e45c119f01331ac13d0eb4049f4efad7c0`.
- Before full-book export SHA256:
  `aa752269f95cf0bf7f125573ab71197a805acff5824bc68b8f7aa16e78ab1702`.
- After full-book export SHA256:
  `4307336dfde5c3bb0d70daa2063fb25deb6deeea65907746e4735b2bdc441354`.
- Export hash serialization: UTF-8 JSON, sorted keys, compact separators,
  Unicode unescaped. No deployed-reader claim.
