# Amos 9:12 — Edom, humanity, and the quotation in Acts

Checked against repository baseline `0ab1c8cd75`. **Retain current Hebrew Amos
and both POB main translations.** The comparison adds manuscript-transcription
support for Edom, but not for the distinguishing letters of “possess.” It also
corrects a consequential error in our machine transcription of Greek apparatus.
No canonical change or new manuscript decipherment is made.

## Distinguish the actual evidence

| Source and exact locus | Observed published wording | Consequence and limit |
|---|---|---|
| [Local WLC](../sources/ot/wlc/Amos.xml), `Amos.9.12` | `יִירְשׁוּ אֶת שְׁאֵרִית אֱדוֹם` (accents omitted here) | Possessing the remnant of Edom; the remnant is the object, not the subject. No qere at this locus. |
| [Qumran-Digital Mur. 88, version 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/Mur._88/2026-05-21/index.html), 8,28 | `[ובניתיה כימי עולם למען ייר]שו את שארית אדום` | Edom is unbracketed. Only `שו` of the verb is outside restoration brackets; its missing beginning cannot independently decide `יירשו` versus `ידרשו`. This is a published transcription, not a fresh reading of ink. |
| [Swete vol. III, printed p. 27, scan n50](https://archive.org/download/theoldtestamenti03swetuoft_202003/theoldtestamenti03swetuoft/page/n50_w1500.jpg), main text 9:12 | `ὅπως ἐκζητήσωσιν οἱ κατάλοιποι τῶν ἀνθρώπων` | “So that the remnant of humanity may seek”; no explicit object after “seek” in this printed main text. The people are now the subject. |
| Same printed apparatus, 9:12, siglum A (Alexandrinus) | Addition `αν` after `οπως`; addition `τον κν` after `ανθρωπων` | Swete reports “the Lord” in this Greek witness, expanding the printed abbreviation `κν` as `κύριον`. The object is not absent from every Greek witness. No physical Alexandrinus leaf inspected. |
| [POB Acts source](../translation/nt/acts/015/017.yaml), SBLGNT Acts 15:17 | `ὅπως ἂν ἐκζητήσωσιν οἱ κατάλοιποι τῶν ἀνθρώπων τὸν κύριον` | Acts explicitly includes “the Lord.” This quotation is reception of Amos, not an additional independent Hebrew manuscript. Agreement in this clause does not establish which way Greek witnesses influenced one another. |

The [Qumran-Digital sigla](https://lexicon.qumran-digital.org/faq/v1/en/index.html)
define square brackets as restored text. Keep the two digital layers distinct:
the pinned QDR export has `א#ת#`, marking damage to the object marker; the current
primary display prints `את` without circelli. Do not silently upgrade the older
encoding or import the displayed Masoretic parallel as Mur. 88's own text.
There was no manuscript-image check of this locus.

A scan of all 266 records in the pinned biblical QDR dataset finds Amos 9:11–12
anchors only in Mur88, record 245, locator 8, lines 26–29. Record 138, 4Q82,
has chapter-9 anchors at 1, 5, 6, 14 and 15, not 11–12. This controls a specific
coverage claim; it is not proof of exhaustive coverage of discovered witnesses.
Related uses of 9:11 in 4Q174, 4Q266 and CD are not independent 9:12 noun/verb
witnesses. Their presence also warns against treating verse-anchor search alone
as a complete inventory of quotations.

## Printed apparatus versus our machine transcription

The original page image was inspected at full resolution and its hash matches
the existing provenance record. Our stored
[AI transcription](../sources/lxx/swete/transcribed/vol3_p0050.txt) renders the
9:12 apparatus additions incorrectly: `οπως] αν. A` loses the addition sign;
`ανθρωπων] + των αν A` corrupts the Lord-object reading. The page instead has
`οπως] + αν A` and `ανθρωπων] + τον κν A`. Use the inspected print for these
claims, not that OCR string. This erratum does not certify the rest of the page;
the original model output is preserved as provenance, not silently rewritten.

A previously pinned Rahlfs-labeled digital Amos control also lacks the explicit
object in its surface text. It was inspected only as a secondary control, not
counted as another independent witness or used to override Swete's apparatus.
No generated morphological reasoning or confidence scores were used.

## English impact and source-selection decision

POB Amos says “possess the remnant of Edom”; Acts says “the remnant of mankind
may seek the Lord.” Keep that difference rather than reconciling the two books
into identical words. The [authorized de Waard–Smalley commentary](https://tips.translation.bible/story/translation-commentary-on-amos-912/)
reads the Hebrew in terms of renewed territorial rule. That is a contextual
interpretation, not proof of historical priority. The Greek humanity/seeking
form changes both participants and action, not merely a place-name spelling.

Possible explanations include a different Hebrew exemplar, reading errors, or
interpretive translation. Reconstructing `ידרשו` and `אדם` from the Greek remains
a hypothesis: neither is supplied by the inspected Hebrew evidence. The retained
WLC has `אדום` with vav; explaining the full difference also requires accounting
for the object marker and subject/object syntax. “One letter changes everything”
is not an adequate account of this textual unit. Mur. 88's noun support does not
resolve its missing verb letters or establish the earliest form of the verse.

The existing Amos note explicitly refers to the form cited in Acts, so it is
not simply false. A future note refinement should distinguish Swete's main text,
its reported A addition, and Acts, instead of speaking of one uniform Greek
text. Any application must also review the misplaced name-idiom note anchor in
Amos and the nations/Gentiles note anchor in Acts. Those are identified editorial
issues, not new variant readings or approvals to edit either record here.

**Stop this pass at retain.** Reopen historical selection with discriminating
Greek apparatus/transmission evidence or additional direct Hebrew evidence.
The mapped Göttingen Twelve Prophets volume remains the modern apparatus route;
it was not acquired in this pass. Do not repeat the Mur. 88 verb restoration as
if its supplied letters were a new supporting witness. No ImageGen is needed:
generated letters cannot resolve a lacuna or validate an apparatus reading.

## Reproduction

- Mur. 88 primary HTML SHA256: `1d58fb5f18adeb57b429e7338d7148081965d4a2f8707d22bd6c261272007f3a`.
- QDR biblical JSON SHA256: `3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`; `data/qdr.1.1.biblical.json`, pinned QDR commit `f54f38464e18409eed8286fe24dd24f88d4735dd`.
- Swete original JPEG SHA256: `a2ca398a6cede8a0e82b21d4ea38757548213b81f0f94a9f2100f1ec849cac87`; actual 2534×4017 pixels despite the URL's `w1500` label. Printed page 27, not page 50.
- Stored Swete AI text SHA256: `ebb10d3ba573d63b73c8c67bcba92d11a4e449eb9eb10158390f2d4bc7caa159`.
- WLC Amos XML SHA256: `6ad94c6a18076762f1a458720c62156d354e5111ee25719b7792b70792d0084d`.
- Canonical Amos YAML SHA256: `558d10b077e7b02fd8957db2ae92ea33eb74eaa036a39309c737fbc68428212c`.
- Canonical Acts YAML SHA256: `3b51ec8b118d229af773bd3947b18b973feb8f6a16131125107bbfa7c4788154`.
- Secondary digital Greek: [pinned Amos JSON](https://github.com/OpenScriptorium/lxx-morph/blob/c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2/db/seeds/lxx_morph/amos.json), `ref == 'Amos 9:12'`, concatenate only `words[].surface`.

The versioned Mur. 88 page required direct HTTP retrieval after the web reader
failed. NET's Amos page was unavailable and contributes no evidence. An HTML
extraction attempt lacked BeautifulSoup; the standard HTML parser succeeded.
Unverified search summaries and broad claims about Greek unanimity were not used.
