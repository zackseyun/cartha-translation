# Pentateuch source comparison — pass 2

Checked: 2026-09-04

Re-audit correction, 2026-09-04: the first version overstated three Exodus
attestations by treating supplied text or partial coverage as whole-reading
support. This revision supersedes those claims. No new manuscript was
deciphered and no main-text reading changed.

## Outcome

The three pilot passages now include individually identified Judean Desert
Hebrew manuscripts, not merely modern editions and daughter versions. This
changes the evidentiary picture without yet authorizing a new reconstructed
base text:

- Genesis 4:8: 4QGenb (4Q2) supports the shorter transition with no recorded
  invitation.
- Exodus 1:5: 4Q13 preserves seventy-five; 4Q1 preserves “and five” after
  supplied “seventy.” The numeral in 4Q11 is entirely supplied, not a preserved
  vote for seventy. The Joseph clause is a separate question.
- Exodus 12:40: the geography in 2Q2 is supplied. 4Q14 preserves a local
  Egypt-to-duration sequence, not enough to establish the whole Egypt-only form.

The English main text remains unchanged. The reader notes now disclose these
Hebrew witnesses and their preservation limits. Every source-text decision
remains `not-adjudicated` pending a reasoned dossier; image review is required
for new decipherment or an unresolved material claim, not universally for
every decision based on published scholarship.

## Discovery and verification method

The machine discovery pass scanned the nested word-level references in all 266
biblical scroll records in Qumran Digital Reader 1.1, pinned at git commit
`f54f38464e18409eed8286fe24dd24f88d4735dd`. A dedicated extractor now walks
every scroll, fragment, line, and word; it does not assume that a whole line has
one verse reference.

Each hit was then checked against a versioned Qumran-Digital scholarly
transcription and matched to its physical manuscript record in the Israel
Antiquities Authority's Leon Levy Digital Library. These are three different
layers:

1. QDR is a machine-readable discovery index derived from ETCBC/Abegg data.
2. Qumran-Digital supplies a versioned published transcription with editorial
   brackets and uncertainty marks.
3. The IAA record identifies the physical manuscript, script, period, material,
   bibliography, and available color/infrared photographs.

The platforms are not counted as witnesses. Each physical manuscript is
counted once, and text inside editorial brackets is not treated as visible ink.

Re-run the discovery query against a licensed local QDR snapshot with:

```bash
python3 tools/textual_restoration/extract_qdr_passages.py \
  /path/to/qdr.1.1.biblical.json \
  --reference 'Gen 4:8' \
  --reference 'Ex 1:5' \
  --reference 'Ex 12:40'
```

## Results

| Passage | Direct Hebrew manuscript | Published-transcription result | Evidentiary effect |
|---|---|---|---|
| Genesis 4:8 | 4QGenb (4Q2), fragment 3 i, lines 8–9 | After “his brother,” the text moves directly to “and it happened while they were in the field” | The short form is ancient and cannot be dismissed as a medieval Masoretic loss |
| Exodus 1:5 | 4QGen-Exoda (4Q1), fragment 17–18, lines 1–2 | “And five” preserved after supplied “seventy”; Joseph clause follows | Supports seventy-five with an explicit restoration boundary |
| Exodus 1:5 | 4QpaleoGen-Exodl (4Q11), fragment 1+39, lines 7–8 | Entire numeral supplied; Joseph clause partly visible after the gap | Indeterminate count; no preserved vote for seventy |
| Exodus 1:5 | 4QExodb (4Q13), fragment 1, lines 5–6 | Seventy-five; text proceeds to Joseph's death without the Joseph-in-Egypt clause | The count and Joseph-clause questions must be adjudicated separately |
| Exodus 12:40 | 2QExoda (2Q2), fragment 5, lines 8–9 | Geographical phrase and duration supplied | Indeterminate geography; passage coverage is not reading support |
| Exodus 12:40 | 4QExodc (4Q14), fragment 5, line 10 | Egypt partly preserved, immediately followed by duration | Excludes Canaan after Egypt locally; missing beginning cannot exclude Canaan before Egypt or “their fathers” |

## Passage assessments

### Genesis 4:8

4Q2 is especially important because enough of the transition is preserved to
exclude the invitation at that location: `אחיו` is followed by the conjunction
and damaged-but-identified `יהי`, then the field clause. The manuscript therefore
supports the same variation-unit class as the Masoretic control.

This does not by itself prove that the short form is earlier than the longer
Samaritan and Old Greek form. The longer form can represent an early Hebrew
Vorlage, while the shorter form is also demonstrably ancient. The best present
publication posture is the existing shorter main text plus a precise note.

### Exodus 1:5

This is no longer a simple Masoretic-versus-Greek count. 4Q13 preserves
`חמש ושבעים`; 4Q1 preserves the additional five after a restored seventy.
In contrast, 4Q11 has `[עקב שבעים]`: the entire word seventy is supplied.
The Old Greek reads seventy-five; Samaritan and Masoretic controls read seventy.
No two-against-one count of preserved Judean Desert numerals is justified.
Material reconstruction may constrain 4Q11, but that argument has not been
verified. Script differences do not prove genealogical independence.

The Joseph clause must be a separate variation unit. It follows the count in
the Masoretic, Samaritan, 4Q1, and 4Q11 forms; it precedes the total in the Old
Greek; and 4Q13 proceeds directly from the total to Joseph's death. No count
decision can silently choose the clause's wording or location.

### Exodus 12:40

In 2Q2, `[ו במצרים שלשים שנה וארבע מאות שנה]` is supplied: the visible
letters cannot establish the geographical scope. In 4Q14,
`ב֯ארץ מ[צר]ים שלשים` supports Egypt followed directly by the duration.
That excludes the Greek control's Canaan after Egypt at this location, but
the missing beginning cannot exclude the Samaritan order of Canaan before
Egypt or its fathers clause. Neither fragment alone establishes the entire
Masoretic form. Longer Samaritan and Old Greek forms remain distinct.

The controlling versioned transcriptions are
[4Q11 (2026-05-21)](https://lexicon.qumran-digital.org/transcriptions/4Q11/2026-05-21/index.html?v=2026-05-21),
[2Q2 (2025-03-11)](https://lexicon.qumran-digital.org/transcriptions/2Q2/2025-03-11/index.html),
and [4Q14 (2026-02-11)](https://lexicon.qumran-digital.org/transcriptions/4Q14/2026-02-11/index.html?v=2026-02-11).

## English POB impact

This pass makes note-level changes only:

- Genesis 4:8 now identifies 4Q2 as direct Hebrew support for the shorter form.
- Exodus 1:5 now has a distinct textual note for the divided count and the
  Joseph-clause variation; its lexical note is moved to the phrase it explains.
- Exodus 12:40 now states 2Q2's lacuna and 4Q14's limited local support before
  describing the two different longer traditions.

No main-text wording changed. The machine-readable comparison deliberately
forbids a preferred reading or canonical-change flag at this stage.

## Next gates

1. Identify the exact IAA color and infrared image for each listed fragment and
   record region coordinates and image provenance.
2. Re-read visible letters independently from the published transcriptions,
   keeping visible, damaged, and supplied characters separate.
3. Consult the cited DJD editions for material notes and competing
   reconstructions.
4. Split Exodus 1:5 into count and Joseph-clause variation units, then run the
   full internal/external adjudication method.
5. Expand the same extractor-driven coverage pass to every high-impact
   Pentateuch case in the variant queue.

The exact records are in
[`../sources/textual_restoration/coverage/pentateuch_pilot.v1.json`](../sources/textual_restoration/coverage/pentateuch_pilot.v1.json)
and
[`../sources/textual_restoration/comparisons/pentateuch_controls.v1.json`](../sources/textual_restoration/comparisons/pentateuch_controls.v1.json).
