# Leviticus 2:8: grammatical person, inferred agents and pointing

Date: 2026-09-05. Outcome: two lexical rationales corrected; Hebrew source,
main English, reader notes and old review state unchanged. No source selection,
fresh manuscript reading, reader-text promotion or deployment occurred.
The [bounded repair record](../sources/textual_restoration/decisions/leviticus_2_8_agency_review.v1.json)
preserves before/after hashes, exact changed lines, unchanged-component hashes,
source pins and unpromoted alternatives.

## Hebrew and English are different questions

The stored WLC forms change grammatical person. The local unfoldingWord Hebrew
Bible morphology independently checks our parsing of the same Masoretic
tradition; it is not an independent ancient witness. Its full Leviticus file
is hash-pinned in the repair record. The relevant sequence is:

| Form, consonants shown | Stored-pointing analysis | Close English gloss |
|---|---|---|
| והבאת | Hiphil perfect 2ms | and you shall bring |
| יעשה | Niphal imperfect 3ms | which shall be made |
| והקריבה | Hiphil perfect 3ms + 3fs object | and he shall present it |
| והגישה | Hiphil perfect 3ms + 3fs object | and he shall bring it near |

POB retains these person forms. That is not an accidental English pronoun
substitution. It can still leave readers unsure who acts. The delivery clause
directs the offering **to the priest**; identifying that clause's agent as the
priest is not established by the verb. The offerer is the natural contextual
agent for delivery, with the receiving priest the natural agent of the later
altar action. These are contextual interpretations, not two explicitly named
Hebrew subjects in the clauses themselves.

The old first rationale prematurely assigned priestly handling to delivery.
The second rationale reinforced that assignment backward. Both now distinguish
grammatical form from inferred agent. This is a local syntactic correction,
not a new HALOT consultation; the existing lexical-reference fields do not
certify new source research. Other unrelated metadata was left untouched.

## Greek comparison crosses a verse boundary

The consulted OpenScriptorium Rahlfs-derived Leviticus snapshot has SHA256
`1d8804b122df867eede51dee6086b1f4d36b7f43b0b11b77a6bffa6d3753a57c`.
Its provenance identifies an Eliran Wong digital text and CC BY 4.0 morphology;
only bounded forms are recorded here. The dataset's automated parse-confidence
fields are not historical-reading probabilities.
[Pinned repository](https://github.com/OpenScriptorium/lxx-morph/tree/c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2).

Greek 2:8 has third-singular προσοίσει in both bringing clauses and active ποιῇ
in the relative clause. At its end, προσεγγίσας is a masculine nominative
singular participle. Greek 2:9 continues with ἀφελεῖ ὁ ἱερεὺς: the explicit
priest subject supplies the natural subject for the preceding participle.
Do not force that participle into a self-contained finite clause merely because
it is tagged 2:8. This analysis supports the Greek ritual sequence; it does
not prove a unique Hebrew Vorlage or adjudicate all Greek manuscript readings.
The full Leviticus Greek critical apparatus remains unconsulted.

## A proposed imperative is a source-pointing question

The publisher's NET PDF, printed p. 230 / PDF page 4, note 3, was inspected
visually. It describes a tentative imperative repointing attributed to BHS,
notes that consonants need not change, and acknowledges unresolved grammatical
difficulties. This establishes what NET's translators proposed, not direct
inspection of BHS or the cited Hartley/Milgrom discussions.
[Publisher's notes](https://bible.org/sites/bible.org/resources/download/netbible/ondemand/bybook/lev.pdf).

Thus an imperative adopted *as a different Hebrew analysis* must not be labeled
an English-only repair just because consonants match. Conversely, an English
imperative used only to restate the current legal injunction pragmatically is
a translation choice; its rationale must not falsely claim to preserve the
same grammatical form. Record which operation is intended. Neither has been
promoted here. Earlier En-Gedi/4Q24 checks do not recover lost Masoretic pointing.

## Alternatives and current decision

1. Retain formal person shifts with a clearer explanation. This preserves the
   declared source and avoids new explicit agents, but leaves English ambiguity.
2. Name contextual agents or add a reader note. This can clarify the handoff
   without changing Hebrew, but must disclose supplied English referents and
   preserve uncertainty where warranted.
3. Adopt the proposed imperative analysis. This may smooth the person sequence,
   but is a pointing decision and does not resolve all grammatical questions.

Only the two incorrect/overconfident rationale lines were repaired. No blind
candidate comparison is claimed; main-text choices remain open under the
[English-review method](TEXTUAL_ADJUDICATION_METHOD.md#english-review-and-application).
The prior review flag and timestamp are preserved as historical state, not
reused as approval. Its referenced review JSON was unavailable in the preceding
pass. No new review score has been invented.

The apparatus receipt was regenerated solely to refresh the current Lev 2:8
file binding after the metadata change. Its twelve source comparisons, English
excerpts and results are unchanged. The repair record retains the prior verse
hash, and tests reconstruct the entire pre-edit byte stream by reversing the
two exact line substitutions. They separately prove unchanged source,
translation/footnotes and cross-check components.

## Access and next gates

The first NET HTML route failed, the classic notes route could not be opened,
and the modern reader returned unrelated passage content. None was used as
Leviticus evidence. The publisher's PDF supplied the relevant note; the PDF
skill's visual-review workflow verified its full page and footnote placement.
Initial local Greek path and Hebrew grep assumptions also failed; locating the
actual private Greek snapshot and chapter/verse USFM blocks resolved them.

Next: directly inspect the cited critical apparatus, evaluate explicit-agent
and reader-note candidates in the full offering paragraph, and record a
source/English application package only if warranted. Do not force person,
voice or gender uniformity merely to make a sentence smoother. The broader
OT/NT source discovery and physical-restoration work remains incomplete.

Tests: `.venv/bin/python -m unittest tests.test_leviticus_agency`.
The [research log](TEXTUAL_RESTORATION_RESEARCH_LOG.md) records this pass.
