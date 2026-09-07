# Haggai: bounded Judean Desert comparison

## Result

Compared the Haggai portions of all three source records in the existing QDR
book map against POB: 4Q77, 4Q80 and Mur88. Found a source-relevant preposition
difference at 2:1 and added qualified disclosure. Hebrew and marker-free English
were unchanged in that source pass; historical priority is unresolved. The
separate 2:22 English-number correction below subsequently changes one word.
This is not a complete
Haggai manuscript census, all-version collation or new manuscript transcription.

The [receipt](../sources/textual_restoration/comparisons/haggai_dss_screen.v1.json)
pins the local navigation data, 38 canonical records and selected Greek control.
Its 87 indexed physical-line records carry 36 Haggai reference tags, including
supplied material; they do **not** establish 36 preserved verses. Haggai 2:9
and 2:11 have no tags in this three-record index, not proven manuscript omissions.
Legacy labels and numbering are navigation coordinates, not physical identity
proof. No new extractor or validation infrastructure was built.

## Published text consulted

- [4Q77, 2026-05-21](https://lexicon.qumran-digital.org/transcriptions/4Q77/2026-05-21/index.html?v=2026-05-21): fragment 3 lines 6–9; fragments 4–5 lines 1–3. Adjacent 3:1–4 and 6:1–3 checked for boundaries. Darius has a spelling difference, `לדריהש` versus WLC `לדריוש`, with no English consequence. The people's complaint at 1:2 is supplied, not independently preserved wording. Fragment 6 has no Haggai identification on this page.
- [4Q80, same version](https://lexicon.qumran-digital.org/transcriptions/4Q80/2026-05-21/index.html?v=2026-05-21): fragments 1–2, three lines each, with the next fragment's transition checked. Sparse day/storehouse/bearing/date/governor fragments give no consequential change. The negative before “borne” and the blessing promise are supplied; fragment 2 line 3 is wholly supplied, not an attested earth clause.
- [Mur.88, same version](https://lexicon.qumran-digital.org/transcriptions/Mur._88/2026-05-21/index.html?v=2026-05-21): Haggai material in columns 21–23, using complete indexed lines and published neighboring context. At 22:15, `אל חגי` is unbracketed and unmarked as uncertain, against WLC's `ביד חגי`. At 22:20 the pronoun is displayed above the line; preserve that correction layer. The key 2:7 treasure wording at 22:31 is supplied and cannot settle its interpretation.

Root read all 38 canonical Hebrew/English records and the Mur88 comparison;
one agent handled the two Qumran records. This is divided labor, not independent
replication of the entire screen. No new image reading was attempted.

## Haggai 2:1: source and English consequence

Mur88's wording addresses the prophet; WLC explicitly expresses mediation by
his hand. Both formulas occur in the book. The local Greek selected text has
`ἐν χειρὶ` here and at 1:1,3, but `πρὸς` at 2:10,20. It distinguishes the
formulas, yet its 2:1 opening verb also differs: it does not prove every Hebrew
word by retroversion. Only its reference labels and surface tokens were used,
not generated morphology/confidence; no Greek manuscript unanimity is claimed.

Either Hebrew formula could have assimilated to another occurrence. This
screen supplies no decisive direction or independently verified object date;
do not turn a modest age preference into a source change. Keep the declared
base provisionally and expose the difference, without erasing “hand” from its
English. The decision is not proof that WLC is the earlier reading.

```json
{
  "source_distinction_checks": [{
    "candidate_id": "hag21-prophetic-formula",
    "disposition": "retain_after_comparison",
    "source_evidence": "WLC בְּיַד חַגַּי; published Mur.88 22:15 אל חגי; local Greek selected text ἐν χειρὶ Αγγαιου.",
    "proposed_text": "On the twenty-first day of the seventh month, the word of Yahweh came by the hand of Haggai[a] the prophet[b], saying,",
    "alternative_text": "On the twenty-first day of the seventh month, the word of Yahweh came to Haggai the prophet[b], saying,",
    "rationale": "The alternative illustrates the attested Mur88 relation, not an English synonym for ביד. Retain the source's explicit mediation and distinguish it from the book's recipient formulas while disclosing the rival reading. This is provisional source retention pending discriminating transmission evidence. The hypothetical alternative omits the agency-note anchor because that explanation would no longer attach to its main wording."
  }]
}
```

Applied note b and moved the unchanged agency note a from the month to Haggai.
One bounded independent check of Mur88 22:14–16 and the exact note/anchors
passed; it does not approve historical priority or all English choices. Archived
old review objects verbatim; current status is draft/needs-review. Stop this
screen here. Reopen 2:1 for a locus apparatus or local transmission analysis
that distinguishes the competing histories, not another transcription download.
Other versional and catalogue gaps remain open; no deployment occurred.

Verification: schema and exact source/marker-free-English/history preservation
passed; all 38 full-book export keys retained, sole output delta at 2:1, both
notes exported intact. Checked receipt input hashes, all 38 baseline hashes and
the exact full-verse comparison JSON. Eight reader-footnote tests pass. Canonical
2:1 SHA256 before `afde1f231b25cd676bc0d75663a3f278f71583d573b26e087d355123b7b3eb3a`,
after `cc6ec19b5402c3594fb8a3104143b2f9cfd21aefc83548dd7a2fbb068ab5fa4a`.

## English consequence: plural riders at 2:22 — 2026-09-07

Changed **“the chariot and its rider” → “the chariot and its riders.”**
The source has singular `מֶרְכָּבָה` but plural `רֹכְבֶיהָ`, followed by
another plural rider form, `רֹכְבֵיהֶם`. Canonical Hebrew and the vendored
WLC/OSHB XML agree; both participles have `Vqrmpc` morphology, with different
possessive suffixes. The [publisher's BHS text](https://www.die-bibel.de/bibel/BHS/HAG.2)
was also consulted at 2:22; this is another edition control, not an independent
ancient witness. Mur88's supplied word does not corroborate the plural as ink.

The old rationale acknowledged the plural but imposed singular occupants for
“paired singular imagery,” then claimed a broadening in the following clause.
That number contrast is not in the Hebrew. The revised wording retains the
singular chariot image and plural occupants/repetition in intelligible English.
The strongest alternative, “the chariots and their riders,” makes a plausible
collective referent explicit but loses the singular vehicle image. The objection
that one chariot may sound overly specific is real; the kingdom/military context
supports generic “the chariot” without requiring one occupant.

One independent agent selected among three anonymized phrase alternatives
in the same full-verse frame before reading the existing draft/rationale,
then reviewed that rationale. Its scoped pass favored the plural correction;
this was one candidate order, not a randomized benchmark or full-verse scholarly
approval. Root read 2:20–23 and made the separate application decision. Existing
source-distinction and doctrine files retain their previously verified hashes.

```json
{
  "source_distinction_checks": [{
    "candidate_id": "HAG.2.22-chariot-riders",
    "disposition": "propose",
    "source_evidence": "מֶרְכָּבָה וְרֹכְבֶיהָ … סוּסִים וְרֹכְבֵיהֶם: singular chariot; both rider forms plural.",
    "proposed_text": "I will overturn the throne of kingdoms[a], and I will destroy the strength of the kingdoms of the nations. I will overturn the chariot and its riders, and horses and their riders will go down[b], each by the sword of his brother.",
    "alternative_text": "",
    "rationale": "Preserve singular chariot, plural occupants and repeated plural riders. The previous singular rider introduces a number contrast not expressed by the source. All other words and note anchors remain unchanged."
  }]
}
```

Applied the proposal to canonical YAML after review, without deploying it.
Updated only the connected lexical choice/rationale and review status; archived
the exact old lexical decision and review objects. Source, notes/anchors,
draft provenance and theological decisions are unchanged. The earlier source
screen's baseline manifest is historical and was not repinned for this edit.

Checks passed: one-word text delta, one lexical-entry delta, exact source/note/
historical preservation, schema, all 38 exported verse keys, only 2:22 changed,
unchanged exported notes, eight reader-footnote tests. An initial one-off XML
lookup missed the OSIS namespace; the corrected namespace-aware check verified
both source forms. No parser change was necessary. Record SHA256 before
`0ef541736dbe460fcacb55ca7469bf1ffd7220a59fb21c0fdd0f2146debf5846`, after
`bca88068dc771fbe981c396c16c986b478fa052d9e92389374a6c9d1f187e69a`.
This is an English fidelity repair, not a new Hebrew restoration or a general
rule that every collective expression must be translated mechanically.

### Related-form batch check — 2026-09-07

After the correction, screened all 39 vendored WLC/OSHB XML books for lemma
7392 with masculine-plural active-participle morphology (`Vqrmp`). Found 17
forms in 16 verses: Judges 5:10; 10:4; 12:14; 2 Kings 9:25; 18:23;
Esther 8:10,14; Isaiah 36:8; Jeremiah 17:25; 22:4; Ezekiel 23:6,12,23;
38:15; Haggai 2:22; Zechariah 10:5. Checked the corresponding POB English.
No further explicit singular “rider” rendering was found: other expressions
use riders/horsemen, plural subjects with riding/mounted, or “you who ride.”
English “you” does not overtly mark number; this is not a claim that every
grammatical distinction is explicit or every rendering optimal.

The initial source-form search traversed all 23,264 OT records; the follow-up
used book/chapter references. Esther's repeated form matches both verses, so
word-string matches are navigation, not unique verse alignment. This check
excludes singular participles, other verb stems/forms and other Hebrew lemmas.
It closes the analogous explicit singular-rider issue in this bounded set;
no extra canonical edits, agent review, infrastructure or runtime tests were
needed. Reopen only for a specific counterexample, not another identical scan.
