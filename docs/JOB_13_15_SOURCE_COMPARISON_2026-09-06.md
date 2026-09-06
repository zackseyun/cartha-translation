# Job 13:15 — written/read Hebrew and English impact

Checked 2026-09-06. Published/digital-source comparison, not fresh manuscript
transcription or an exhaustive Job apparatus. The scoped note/rationale
correction is now applied as recorded below; Hebrew and main English are
unchanged. Earlier research sections preserve their pre-application observations.

## Finding

POB's rationale incorrectly frames the choice as original-language primacy over
translation tradition. The alternative is recorded **inside the vendored Hebrew
source** as qere, not merely in English translations. Retaining the written text
is a defensible provisional policy, but that policy does not establish its
historical priority. Correcting the explanation is warranted; reversing the
source choice is not established by this pass.

## Actual evidence

| Control | Locally decisive evidence | What it establishes |
|---|---|---|
| [OSHB/WLC Job XML](../sources/ot/wlc/Job.xml), `Job.13.15` | Direct word `לא`, `type="x-ketiv"`, ID `184U9`; nested reading `ל֣/וֹ`, `type="x-qere"`, ID `18Vvg` | The digital Hebrew source preserves both written “not” and read “to him.” These are not two independently dated manuscripts. |
| [Current POB](../translation/ot/job/013/015.yaml) | “Though he slay me, I will not wait; yet I will argue my ways before him.” | It selects the ketiv and interprets the verb as waiting; the existing footnote discloses hope in him but obscures its source-local qere status. |
| [Pinned Greek control](https://github.com/OpenScriptorium/lxx-morph/blob/c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2/db/seeds/lxx_morph/job-lxx.json), `Job 13:15` | `ἐπεὶ καὶ ἦρκται` followed by `ἦ μὴν λαλήσω καὶ ἐλέγξω ἐναντίον αὐτοῦ` | The clause differs substantially from the Hebrew hope/wait alternatives. It does not supply a transparent word-for-word vote for either `לא` or `לו`. |

Only Greek `surface` fields were used, not this digital resource's generated
morphological confidence or reasoning. The Rahlfs-labeled edition control is
not a fresh collation of Greek manuscripts or their correction layers. Our
reading of the quoted Greek is “since he has already begun … surely I will
speak and argue before him”; this is an explanatory gloss, not proposed POB
English or a recovered Hebrew back-translation. In particular, `ἦ μὴν` is not
the Hebrew negation translated word-for-word.

The existing QDR screen records no index hit at this anchor. That is a dataset
query result, not proof that every Judean Desert Job witness lacks the passage.
No new physical-witness coverage, Aramaic Job transcription, Masoretic image,
Greek apparatus or Syriac/Latin comparison was acquired here.

## Keep the two English decisions separate

The same verb form `אֲיַחֵל` appears in local WLC Job 6:11, 13:15 and 14:14;
Job 32:11 supplies another form of the indexed lemma. The inspected contexts
concern endurance/expectation, waiting for a change, and waiting for speakers.
Our inference is that both waiting and hopeful expectation deserve contextual
testing. The project's own English choices at those loci are not independent
lexicographic evidence; no new HALOT consultation is claimed.

In Job 13:13–19, determination to present a case can support the current “I
will not wait,” while the prospect of death can support “I have no hope.” The
latter is not a necessary consequence of keeping `לא`. Likewise, choosing qere
does not by itself settle “Though” versus an emphatic opening, or every English
tense. This contextual assessment is not a blinded translation evaluation.

## Bounded outcome and proposed repair

Retain source and main English provisionally. Replace the misleading rationale
in a later reviewed application with: “The declared source follows the Hebrew
written form (ketiv), while the same source records the traditional reading
(qere). Retention is provisional, not proof that the written form is earlier;
the English sense of the verb requires separate contextual judgment.”

Initial prose note, superseded by the exact candidate below:

> The Hebrew written form (ketiv) has “not”; its traditional reading (qere)
> has “to him,” often rendered “I will hope in him.” The verb also involves
> waiting or expectation; “I have no hope” is another interpretation of the
> written form. Which reading is earlier remains uncertain.

This initial prose proposal was not a complete YAML application candidate.
The full-record candidate below now supersedes it for editorial preparation;
neither was applied at that preparation stage. Review the note, related
lexical/theological metadata and English alternatives together before applying
anything; preserve the historical reviews. To reopen historical selection,
obtain a discriminating manuscript/apparatus or versional argument and test
the competing transmission explanations. Do not equate qere with inferior
translation tradition, or take digital absence as an attested ancient omission.

## Published counterarguments and book-wide verb control — 2026-09-06

Question: does retaining `לא` establish POB's “I will not wait,” understood as
refusal to delay presenting a case? **No.** The negation, verb sense and implied
object of expectation need separate justification. This follow-up adds actual
published arguments and a reproducible lexical control, not a manuscript vote.

- The [NET notes, Job 13:15, notes 1–3](https://classic.net.bible.org/verse.php?book=Job&chapter=13&theme=false&verse=15)
  prefer the qere with hopeful expectation: Job risks death while anticipating
  vindication. They report Davidson's negative waiting interpretation as an
  alternative, not the NET conclusion. Their separate discussion allows an
  emphatic connective and defending one's case without emending the final verb.
- [Reyburn's *A Handbook on Job* (UBS, 1992), authorized excerpt at Job 13:15](https://tips.translation.bible/story/translation-commentary-on-job-1315/),
  acknowledges waiting as the verb's usual sense but recommends expressing
  absent hope/expectation in this context. Its strong rejection of the familiar
  trust rendering is an interpretive judgment, not an apparatus demonstration
  that the qere is historically secondary.
- The [Cambridge commentary, chapter 13, section 15](https://biblehub.com/commentaries/cambridge/job/13.htm)
  supplies the argument behind the negative waiting interpretation: Job does
  not postpone the fatal confrontation until death comes later. This is more
  specific than POB's explanation about ceasing to wait passively. The same
  commentary also discusses the qere as awaiting God's fatal action, rather
  than necessarily trusting for a favorable outcome. Read here as a digital
  reproduction of the commentary; no printed page or scan was verified.
  Its broad claims about ancient versions are not adopted as a collation.

### Local control and limits of the inference

In the unchanged OSHB/WLC `Job.xml`, enumerate direct `w` children of each
`verse` whose slash-delimited `lemma` ends in `3176`. This returns eight loci:
6:11, 13:15, 14:14, 29:21, 29:23, 30:26, 32:11 and 32:16. This is coverage of
the edition's annotation, not a claim to an independently re-lemmatized corpus.
The first three have the same pointed verb form; the other forms and speakers
must not be flattened into identical constructions.

The Hebrew of 29:21 and 32:11,16 connects waiting with speech. Conversely,
30:26 sets awaiting light alongside expecting good, each disappointed by its
opposite; 29:23 compares expectation to rain. Our inference: temporal waiting
can involve desired outcomes. These controls do not make “wait” mean impatience
by default, nor establish “hope” as the only English rendering. In 13:13–19,
readiness to speak despite danger supports the confrontation interpretation,
while anticipated vindication in 13:18 also explains the NET's counterargument.
The context constrains, but does not uniquely settle, either source choice.
Current POB translations were inspected only as implementation context, not
used to prove the Hebrew's meaning. No fresh HALOT consultation is claimed.

### Decision and concrete application implications

Retain source and main English provisionally; do not promote a new historical
reading. The published waiting argument supports plausibility, **not superiority
of POB's exact wording or explanation**. The proposed note above remains useful
but unapplied. A later scoped repair must cover not only `theological_decisions`
but the live `source_audit.review_summary`: its inference from WLC negation to
preferred “not wait” overstates what the consonants establish. Preserve the
past `revisions` entries as history, rather than silently rewriting their claims.
The lexical rationale should identify refusal to delay confrontation as an
interpretation and distinguish it from absence of hope. Review the opening
and connective with the whole sentence; changing ketiv/qere alone cannot settle
them. Do not append certainty percentages from agreement among commentators.

Stop this contextual pass here. Reopen main-English selection with a full
sentence-level comparison that explicitly weighs postponed confrontation,
lost expectation and waiting for God; reopen historical priority with actual
discriminating apparatus/versional evidence. No new image work or transaction
framework follows from this result. Local XML and target YAML hashes below
were rechecked unchanged at repository baseline `d73c9aecc4`.

## Exact disclosure candidate and editorial review — 2026-09-06

The [full-record candidate](../sources/textual_restoration/applications/job13_15_disclosure_candidate.v1.yaml)
turns the findings into an exact proposed correction, not another source search.
It identifies both Hebrew forms in the reader note, separates negation from
wait/hope semantics, and corrects the lexical, theological and live source-audit
explanations. It removes the unsupported “in him” from the negated lexical
alternative. The note makes no claim to establish the earlier reading.

Source, exact main English including its marker, philosophy, original AI draft,
historical revisions and unrelated lexical entries are unchanged. Old status,
revision-pass, cross-check and source-audit objects are archived intact with
their baseline provenance, without inventing original review-input bindings.
Current review fields require review; the modified lexical citation names the
published contextual comparison instead of implying a fresh HALOT consultation.

Candidate SHA256:
`5d32a6ef2913547460cacdc7e0192dfb6468c9c331af5325fee9f5f217ddc033`.
Baseline YAML and Hebrew XML hashes are the unchanged values below. Independent
agent `/root/job_disclosure_judge` checked this exact candidate, the XML, baseline
field preservation, archived reviews, NET notes and authorized Reyburn excerpt;
verdict **PASS — editorial candidate only**. This does not approve application,
historical priority, the full verse or publication.

Local preflight passed the verse JSON schema, exact source/English and historical
record preservation, single-marker/note correspondence and review-state checks.
The actual Job export contains 42 chapters and 1,070 verses. A separate simulated
export substituted this candidate only at `load_translation_record('JOB',13,15)`;
deep comparison found only footnote a changed. This is projected reader output,
not an applied or deployed export. Reproduce using `export_book('JOB')` normally,
then with that one loader override; compare all output after replacing only the
expected target note. Hash serialization is UTF-8 JSON, `ensure_ascii=False`,
`sort_keys=True`, separators `(',', ':')`:

- Actual export: `b7d20eb2076ab7755ff0b38fb883d8a6afcfe144e2121e24b05dd8202f59d56b`.
- Projected export: `84e15083b995f89b034e3fc69fa97c06e5b617258d401b298b4fa460c367e40f`.

**Preparation checkpoint, superseded by the application below:** the editorial
correction was ready but application was not yet approved. The existing
`tools/samuel_note_transaction.py` binds its current check to a fixed digest of
every OT canonical YAML, so even this disjoint Job edit would invalidate that
check. Do not repin its frozen receipt or build another per-verse transaction.
A separately reviewed successor-state mechanism must preserve verification of
the Samuel package while allowing explicitly authorized later corpus changes.
That is the concrete enabling issue before applying this candidate; new Job
image searches or more reviews of unchanged wording will not resolve it.
Schema/export preflight and editorial review do not waive this integration gate.
No canonical, executable, test or derivative file changed in this preparation.

## Scoped application verified — 2026-09-06

Applied the exact candidate above after resolving the integration gate through
the reusable [successor verifier](CORPUS_SUCCESSOR_VERIFICATION.md), not a Job
transaction executable. The [exact plan](../sources/textual_restoration/applications/job13_15_successor_plan.v1.json)
and [independent review](../sources/textual_restoration/applications/job13_15_successor_review.v1.json)
bind its source, candidate, implementation and checks. Review scope covers only
this disclosure/metadata application, not historical priority or the full verse.

Preserved the [actual baseline check](../sources/textual_restoration/applications/job13_15_successor_preflight.v1.json)
before the separate canonical edit. The [application record](../sources/textual_restoration/applications/job13_15_successor_application.v1.json)
records both actual states: all 23,264 OT YAML paths/bytes match the checkpoint
plus this one approved change. Actual Job export matches the previously projected
42-chapter/1,070-verse hash above; actual Samuel export remains unchanged at
`a434d6e5d515c8d1fd5135c07dd6d8e56ae12036d641d70a077895e5fc102289`.
This is no longer an in-memory candidate export. The separate application record
is current; the candidate's `note_proposal` block is historical preparation
metadata, including its earlier unapproved/unapplied labels.

For a read-only check of the applied state, use:

```sh
.venv/bin/python -m tools.textual_restoration.verify_corpus_successor \
  sources/textual_restoration/applications/job13_15_successor_plan.v1.json \
  sources/textual_restoration/applications/job13_15_successor_review.v1.json \
  --review-sha256 26e6e02bfe089a3eb448441b1bffefa0d9ce4029316397d419e245d8bc34c4f2 \
  --application sources/textual_restoration/applications/job13_15_successor_application.v1.json \
  --application-sha256 fb85aa879265820e344666e917bdbe0feea03bcc3252e65de09d639b90626803
```

The current source/English selection remains provisional. Review history is
preserved, current review flags require review, and no prior scores certify the
edited record. No derivative synchronization or reader deployment occurred.
Do not reopen this disclosure merely to obtain another passing review; historical
priority or main-English changes still require their stated new evidence.

## Reproduction and limits

Repository baseline: `276b39ce5c` (no Job changes during this pass).

- Job YAML SHA256: `111d4cebd2ee664ec2097a4fb21c92f54aba525b3ff0f30f0f35c769c3eebab4`.
- Job XML SHA256: `7db3311184122f37a8fd52f3c7c0c4a6d2da7b77ee82f4fdb26bcba9171d297f`.
- Greek JSON SHA256: `f58e3906448a5e892da5d8b6dcc01a732284c68985d926e2d1517e6eea61e837`;
  Git revision and path are fixed in the link above. Read verses 14–16;
  filter records by `ref`, then concatenate `words[].surface` in stored order.

Credit the Open Scriptures Hebrew Bible Project for its XML annotations;
its vendored README distinguishes CC BY 4.0 annotations from public-domain WLC
text. No full external corpus was vendored. An initial wrong XML selector and
guessed `job.json` URL failed; the OSIS namespace/verse ID and repository
directory listing supplied the successful locators. Inaccessible web pages and
irrelevant search results were not used as evidence. No image workflow or
ImageGen was needed for these published-source claims.
