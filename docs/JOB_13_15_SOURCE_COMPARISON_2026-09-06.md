# Job 13:15 — written/read Hebrew and English impact

Checked 2026-09-06. Published/digital-source comparison, not fresh manuscript
transcription or an exhaustive Job apparatus. No canonical change applied.

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

Proposed reader note, **research-only, unapplied**:

> The Hebrew written form (ketiv) has “not”; its traditional reading (qere)
> has “to him,” often rendered “I will hope in him.” The verb also involves
> waiting or expectation; “I have no hope” is another interpretation of the
> written form. Which reading is earlier remains uncertain.

This is not a complete YAML application candidate. Review the note, related
lexical/theological metadata and English alternatives together before applying
anything; preserve the historical reviews. To reopen historical selection,
obtain a discriminating manuscript/apparatus or versional argument and test
the competing transmission explanations. Do not equate qere with inferior
translation tradition, or take digital absence as an attested ancient omission.

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
