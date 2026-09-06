# Leviticus 2:8–9: direct Greek and Syriac controls

Date: 2026-09-05. The earlier selective report is supported at the opening
verb by direct consultation of the publisher's Greek chapter and CAL's Syriac
chapter. The Syriac delivery clause also exposes a distinction that opening-verb
agreement does not cover. No canonical text, lexical rationale, reader note,
registry, or frozen receipt was changed. Earliest Hebrew and best English
remain unresolved.

## Sources actually read

The [Deutsche Bibelgesellschaft chapter](https://www.die-bibel.de/bibel/LXX/LEV.2)
identifies its text as Rahlfs–Hanhart's second improved edition (2006).
The full chapter, including the continuous 2:8–9 sentence, was read through
the web extractor. This improves the earlier OpenScriptorium derivative
control to direct publisher-text consultation. The displayed chapter does
not supply the full Greek critical apparatus; that remains open. Two digital
presentations of this edition family do not become two physical witnesses.

The current [CAL chapter browser](https://cal.huc.edu/get_a_chapter.php?file=62003&sub=02&cset=S)
was read with manuscript variants displayed, with special attention to 2:7–10
and the same aroma expression in 2:2/12. Its [file information](https://cal.huc.edu/get_file_info.php?coord=62003&return=/ot_peshitta.html)
attributes P Lv, file 62003, to the Leiden critical edition with some corrections
from manuscript 7a1, provided through the Peshitta Institute. This is an
edition-derived, selectively corrected text, not a fresh reading of 7a1 or
a complete collation of every Syriac manuscript. The metadata page oddly heads
the information with “chapter 2 verse 2”; its description names Peshitta
Leviticus. No claim that a particular 2:8 word is a correction from 7a1 follows.

The new [machine receipt](../sources/textual_restoration/discovery/lev2_version_controls.v1.json)
pins current POB 2:1–10 files, the local Hebrew morphology source, and the
three preceding reports and twelve-unit specification. It also pins two
private **selected observation transcripts**. Those transcripts preserve
literal excerpts manually from the actual tool-visible pages; their hashes
are not raw HTTP hashes, full-chapter hashes, or edition-file hashes. This
limitation is explicit because publisher curl returned 403, CAL's obsolete
URL returned 404, and Chrome content export was unsupported. CAL's direct
curl response displayed a no-scraping notice; automated CAL downloading was
not continued. Normal navigation through its current Syriac category and
OT Peshitta index succeeded. No authentication or access restriction was bypassed.

## Person and agency

| Clause | Publisher Greek | CAL Syriac | Current POB Hebrew/English consequence |
|---|---|---|---|
| Opening, 2:8 | προσοίσει: future active indicative, third singular | ܘܬܝܬܐ: second masculine singular in this instructional context | POB retains second-person והבאת, “you shall bring.” |
| Relative clause | ποιῇ: present active subjunctive, third singular | ܕܡܬܥܒܕ: Ethpeel masculine singular participle, “that is made” | Stored Hebrew has Niphal imperfect 3ms; Greek active wording is a versional distinction. |
| Delivery to priest | Same third-singular Greek verb as opening | ܘܬܩܪܒܝܘܗܝ: second masculine singular in context, masculine singular object | Stored pointed והקריבהּ is 3ms + 3fs object; Syriac is not evidence that the current Hebrew pointing is 2ms. |
| Altar action | προσεγγίσας: aorist active masculine nominative singular participle | ܘܢܣܩܝܘܗܝ: third masculine singular, masculine singular object | Stored pointed והגישהּ remains 3ms + 3fs object; priestly agency is contextual. |
| Continuation, 2:9 | ἀφελεῖ ὁ ἱερεὺς supplies explicit priest subject | Removal clause explicitly names the priest | Compare across the Greek verse boundary before assigning the participle's subject. |

The Syriac [opening](https://cal.huc.edu/getlex.php?coord=620030208&word=0&hasvariant=0),
[relative](https://cal.huc.edu/getlex.php?coord=620030208&word=2&hasvariant=0),
[delivery](https://cal.huc.edu/getlex.php?coord=620030208&word=6&hasvariant=0), and
[altar](https://cal.huc.edu/getlex.php?coord=620030208&word=8&hasvariant=0)
lexical pages tag the roots/stems as respectively `)ty C`, `(bd Gt`, `qrb D`,
and `slq C`. These are the directly consulted CAL metadata. The person,
number, participle and suffix analyses above are our analyses of the displayed
Syriac, **not full person tags returned by CAL**. The t-prefixed imperfect has
2ms/3fs syncretism; second-person address is selected contextually here, with
masculine grain-offering wording and the surrounding instructions. Finite
Greek third singular itself does not encode masculine gender.

This directly supports the earlier En-Gedi edition's local classification
of Syriac with the second-person opening and Greek with the third-person
alternative reported for 4Q24. It does not independently re-read the En-Gedi
PDF's footnote 19 or verify every selective alignment at other loci. The
earlier report's selective-apparatus warning remains in force. In particular,
Syriac second-person delivery differs from POB's stored third-person delivery,
although its opening agrees in contextual person. Whole-verse agreement
cannot be inferred from the opening comparison.

Greek naturally links the approach participle to the explicit priest in
2:9. In Syriac the third-person altar clause follows second-person delivery
to the priest; the receiving priest is a natural inferred subject, not a
newly supplied explicit noun in that clause. Neither version requires us to
declare the priest the subject of the preceding delivery *to* the priest.
POB's two later 3ms forms are retained. The [prior agency review](LEVITICUS_2_8_AGENCY_REVIEW_2026-09-05.md)
already corrected its rationale to distinguish grammatical person from
contextual agent. These versional controls strengthen that distinction;
they do not choose between retained English, explicit agents, or a reader note.

## Aroma and the limits of retroversion

The Greek aroma expression is ὀσμὴ εὐωδίας. CAL's 2:9 display explicitly
includes `ܣܘܬܐ/ܢܝܚܐ#2#/`. Its [lexical page](https://cal.huc.edu/getlex.php?coord=620030209&word=10&hasvariant=1)
warns that parsing is shared across the main and variant readings. It links
the main noun to the sweet-smell entry and the alternative to rest/comfort.
Do not collapse this into one word's two simultaneous parses. The identity of
CAL's `#2#` siglum was not established; the opened 2:9 comment page concerned
remembrance and supplied no siglum key. The visible variant is not a consulted
full Leiden apparatus. Its spelling must not be silently promoted to a
named manuscript reading.

POB's Hebrew ניחח and the previously reported QDR ניחוח differ in plene
spelling. Greek aroma semantics and Syriac's lexical alternative do not
recover the presence or absence of that Hebrew waw. The Syriac alternative
is also not merely the same Hebrew plene/defective contrast written in another
alphabet. No changed English aroma follows from the Hebrew spelling alone.
No HALOT entry was consulted in this pass.

At the opening, a Greek third-person rendering is compatible with a Hebrew
third-person Vorlage, but does not uniquely prove it: translation practice
and contextual adjustment remain live explanations. Syriac contextual second
person likewise is not direct evidence for particular Hebrew vowels. These
are language-specific grammatical observations and bounded edition-family
comparisons, with no new independently inspected physical witness or target
pixels. The [4Q24 primary follow-up](4Q24_LEVITICUS_2_PRIMARY_FOLLOWUP_2026-09-05.md)
retains its separate transcription/plate/fragment gates.

## Verification and next gate

```bash
.venv/bin/python tools/textual_restoration/check_lev2_version_controls.py /path/to/private/observation-directory
.venv/bin/python -m unittest tests.test_lev2_version_controls
```

The checker requires both private observation transcripts and rejects missing
or altered inputs; it also checks all 15 current local hashes and the stored
Hebrew person morphology. Tests cover drift, missing evidence, altered private
bytes, absent excerpts, and interpretation boundaries. They check receipt
faithfulness, not earliest reading or best English. Full Greek/Leiden apparatus,
CAL variant-siglum identity, source priority and comparative English selection
remain open. This report does not claim a judge-approved reading or completed
textual adjudication.
