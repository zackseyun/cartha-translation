# Haggai: bounded Judean Desert comparison

## Result

Compared the Haggai portions of all three source records in the existing QDR
book map against POB: 4Q77, 4Q80 and Mur88. Found a source-relevant preposition
difference at 2:1 and added qualified disclosure. Hebrew and marker-free English
remain unchanged; historical priority is unresolved. This is not a complete
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
