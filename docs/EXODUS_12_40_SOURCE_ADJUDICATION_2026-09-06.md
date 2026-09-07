# Exodus 12:40: geographical scope and distinct Greek forms

Checked 2026-09-06 under [method 2.0](TEXTUAL_ADJUDICATION_METHOD.md).

Later application, also 2026-09-06: the scoped disclosure and related metadata
corrections identified below are now applied; see the
[application receipt](../sources/textual_restoration/applications/exodus12_40_disclosure.v1.json).
Hebrew, main English and note anchor remain unchanged. The research findings
and earlier unapplied-state statements below describe the preceding checkpoint.

## Decision

Provisionally retain the declared Hebrew base and current Egypt-only English.
Confidence in **earliest-wording priority is low**; this is not a finding that
the Masoretic form defeats the Samaritan Hebrew. The longer forms remain
serious alternatives. This closes the present research pass with a reasoned
hold, not source promotion or approval of the existing English rendering.

Baseline: `657b2b9ffd6e099b6abf2303999d3fa2b6045596`,
[`translation/ot/exodus/012/040.yaml`](../translation/ot/exodus/012/040.yaml),
SHA256 `e83843ea14e4c105449069f2a6fab7d6ef98e51f9f3193f6b6080be4997bd2a9`.
No canonical file changes in this pass.

## Evidence actually added

Brooke–McLean, *Exodus and Leviticus* (1909), printed pp. 194–195
(PDF 52–53), and preface v–vii (PDF 9–11), visually inspected in full.
[Source PDF](https://tmcdaniel.palmerseminary.edu/Brooke%26McLean/LXX_Brooke%26McLean_1-2.pdf),
SHA256 `8d63914f75fd1e4539fb953fa8ec50223be6b41e91509ea37c401e03d32d16c9`.

- Printed v40 has Egypt then Canaan, no fathers, and 430.
- The first apparatus at **both v40 and v41** reports
  `τριακοντα] + πεντε B* (om Bᵃ?)`: Vaticanus's first hand has the additional
  five; the corrector attribution carries a question mark. Do not flatten
  first hand and correction into a uniform 430 reading.
- The main v40 apparatus reports “they and their fathers” before the first
  locative phrase in one group and after Canaan in another. A (Alexandrinus)
  explicitly belongs to the latter group. These are not one uniform Greek
  form or a complete inventory of every Greek witness.
- The preface allows corrected B readings in the printed text for practical
  apparatus presentation. Printed text is not automatically B's first hand
  or the editors' reconstruction of earliest Greek.

General apparatus conventions were also checked in Brooke–McLean's *Genesis*
(1906), printed i–ii (PDF 9–10): marginal base, separate principal-manuscript
notes, `pr` versus `+`, and adjacent variation units.
[Conventions PDF](https://tmcdaniel.palmerseminary.edu/Brooke%26McLean/LXX_Brooke%26McLean_1-1.pdf),
SHA256 `c5031defb2e2f8de3e4db1f47244f0565ea001a529e3f924680e4f3c7ead1519`.
These are published reports, not inspection of ancient manuscript pixels.

## Existing evidence reused, not re-acquired

The [pass-2 dossier](PENTATEUCH_SOURCE_COMPARISON_PASS_2.md#exodus-1240)
and [pinned comparison](../sources/textual_restoration/comparisons/pentateuch_controls.v1.json)
preserve the relevant distinctions:

| Control | What it can establish here |
|---|---|
| WLC | Egypt-only, 430 in the declared base |
| Samaritan Hebrew digital control | Fathers; Canaan before Egypt; 430 |
| Rahlfs Greek digital control | Egypt before Canaan; no fathers; 430 in that edition |
| 2Q2 published transcription | Geography supplied in a gap; no geographical vote |
| 4Q14 published transcription | Partly preserved Egypt immediately before duration; missing beginning cannot exclude earlier Canaan or fathers |

The Samaritan dataset is based here on Chester Beatty 751, not the separately
mapped Rylands images. Modern editions and their source manuscripts are not
additional independent votes. The older comparison's `not-adjudicated` state
remains a historical checkpoint; this report supplies the later research hold.

## Competing explanations and chronological sensitivity

Adding Canaan and fathers can explain the duration as including patriarchal
residence. David A. Glatt-Gilad's
[2016 argument](https://www.thetorah.com/article/how-many-years-were-the-israelites-in-egypt)
was consulted for the genealogical tension and proposed harmonization. His
inference of independent solutions from differing geographical orders is not
adopted: reordering or shared ancestry remain possible. Biblical chronological
consistency is not a criterion that can by itself select the earlier wording.

The strongest counter-explanation is loss: in a hypothetical Canaan-first
Hebrew ancestor, repeated `בארץ` sequences could facilitate skipping part of
the geography. That would not by itself explain loss of fathers; another
change or a differently worded ancestor would be needed. This is a possible
transmission mechanism, not a newly attested exemplar. Conversely, expansion
is plausible, not an observed scribal intention. Neither “shorter” nor “more
difficult” decides the case.

Ancient Greek attestation makes the broader geography important, but the date
of a translation is not the date of each surviving reading. Early 4Q14 does
not preserve enough of the beginning to settle the scope. Removing the modest
age preference leaves the same low-confidence hold. The new Greek numeral
evidence also cannot recover a Hebrew 435 reading.

## Review, limits, and next action

One independent agent (`/root/exodus_sojourn_audit`) first audited local
evidence, then checked the new printed pages. It confirmed both numeral
entries, the uncertain corrector label and the two fathers positions, and
accepted provisional retention with low priority confidence. This was a
context-informed review, not blinded transcription or another historical vote.

The current note's blanket “The Septuagint reads” needs edition-specific
qualification. Its theological metadata also conflates the geographical orders
and inadequately accounts for Samaritan Hebrew as direct-language evidence.
The relative-clause rationale and English attachment differ; review that
separately rather than using a source decision to hide a rendering change.
These are identified issues, **not applied corrections**.

Reopen source selection when DJD material notes constrain 4Q14's missing
beginning, or a full modern Greek/Samaritan apparatus and local transmission
study discriminate expansion from loss. This pass did not consult those
materials or clear later errata; the 1909 preface itself anticipates later
corrections. Do not repeat this acquisition or initiate image calibration
without such a discriminating question. A scoped note/metadata correction can
use the evidence now available without waiting for source priority to be settled.

Both PDFs remain privately in the task's `research_sources/`; no PDF, manuscript
image or generated reconstruction is redistributed in Git. Documentation-only
checks verify links, baseline preservation and patch integrity, not textual truth.

## Scoped disclosure application

The subsequent application qualifies the edition/witness/hand attributions,
preserves the fragmentary Hebrew limits, separates the theological alternatives,
and states the existing relative-clause attachment without deciding the best
rendering. Old cross-check and revision-pass objects are archived verbatim;
the active verse remains draft/needs-review. One independent agent approved the
exact note and then confirmed the exact written metadata. That approval is
limited to disclosure, not earliest-source selection or whole-verse translation.

Verse-schema and exact structural-delta checks passed. Actual before/after EXO
exports both match every source chapter/verse identifier: 40 chapters and 1,213
verses. The only exported difference is the target footnote's text; source,
main English, marker and unrelated history remain unchanged. Eight reader-note
tests passed. The receipt records hashes and the actual exported target; it
pins this report's reviewed research version at the preceding Git checkpoint,
not this later application annotation. No deployment or corpus-wide validation.
