# 2 Samuel 13:37: Hebrew controls for Talmai's patronymic

Date: 2026-09-06. Research-only, held; no canonical change, source selection,
whole-verse approval, or new calibration result. Companion:
[factual receipt](../sources/textual_restoration/discovery/samuel13_37_hebrew_controls.v1.json).
The controlling method and the existing Leningrad image report were read in
full. This investigation adds a published DSS transcription check and an
independent medieval manuscript image, not another vote for each edition.

## Result

The evidence now supports a more precise hold. UXLC's final-dalet correction
can be a better transcription of **Leningrad** without making that spelling
the earliest recoverable patronymic. An accessible **Aleppo** photograph favors
written עמיחור, with marginal עמיהוד. The indexed **4Q51** passage does not
preserve the patronymic: its עמיחוד is supplied inside a gap. It cannot decide
any of the name's disputed letters. The present English “Ammihur” is therefore
not refuted simply by counting UXLC, a qere, and a completed DSS transcription.

The strongest contrary explanation to a final-dalet promotion is a genuine
resh-bearing written tradition, preserved in Aleppo, with a different reading
tradition beside it. A dalet spelling could be related to that reading tradition
without being the original body spelling. Conversely, resemblance between
resh and dalet permits corruption in either direction; a medieval resh does
not itself prove original resh. This report cannot determine direction or
establish the name's earliest form. Ancient-version comparisons belong to the
separate parent investigation; no unanimous versional support is claimed here.

## Separate the three questions

| Control | Written form / supplied form | Reading tradition | Evidentiary boundary |
| --- | --- | --- | --- |
| Vendored WLC at 2Sam.13.37 | עמיחור | עַמִּיה֖וּד | Two fields in one Leningrad-derived edition, not two manuscripts |
| Pinned UXLC 2.5 | עמיחוד, with `t` after the penultimate vav | עַמִּיה֖וּד | Same-codex transcription revision; `t` is metadata, not a consonant |
| Aleppo, publisher photograph examined here | Body appears עמיחור | Margin appears עמיהוד | A different physical codex; context-informed image reading, not a blind decipherment |
| Miqra'ot Gedolot Haketer online edition | Ketiv עמיחור | Qere עמיהוד | Aleppo-based editorial control, not an additional physical witness |
| QDR's 4Q51 transcription | Supplied עמיחוד | Not a Masoretic qere field | Entire name in brackets; no surviving name letters established by this transcription |

The ketiv's **het** and qere's **he** are a separate difference from final
**resh/dalet**. UXLC changes only the written form's last consonant relative to
WLC; it does not replace the ketiv with the qere. The preceding **vav/yod**
problem is yet another question: the Leningrad publisher explicitly flags it,
and the previous Leningrad image check leaves it unresolved. Neither the
Aleppo vav-looking stroke nor the qere settles what Leningrad's body stroke is.

## Exact local baseline

`translation/ot/2_samuel/013/037.yaml` has source edition WLC and unpointed
עמיחור in the source line. It prints “Talmai son of Ammihur[a], king of Geshur.”
The sole note is about the implicit subject of the later “he mourned,” understood
as David, not the patronymic. The marker after Ammihur therefore does not
disclose this variation and is poorly placed for its actual subject. This is
a separate, concrete reader-facing follow-up, not permission to change the name.
The record's HALOT-labelled lexical rationale and revision/cross-check metadata
are historical; HALOT was not freshly consulted or reapproved.

In `sources/ot/wlc/2Sam.xml`, locate `verse[@osisID='2Sam.13.37']`:
the `w[@type='x-ketiv']` has id `10tA2`, lemma `5991`, text עמיחור;
the variant note's `rdg[@type='x-qere']/w` has id `109ZJ`, lemma `5989`,
text עַמִּיה֖וּד. The pinned UXLC archive's member `Books/Samuel_2.xml`,
`c[@n='13']/v[@n='37']`, instead contains `<k>עמיחו<x>t</x>ד</k>` and
`<q>עַמִּיה֖וּד</q>`. All relevant file hashes are in the receipt.

## Leningrad and apparatus boundaries

The [UXLC publisher's change entry](https://tanach.us/Changes/2022.12.07%20-%20Changes/2022.12.07%20-%20Changes.html),
2022.08.30–23, locates word 2Sam13:37.7 at folio175B, column3, line19.
It changes final resh to dalet while retaining uncertainty over the preceding
stroke. It reports BHL's body as עמיחור and Appendix A's two question-marked
alternatives as עמיחיד (?) and עמיחוד (?). That is a publisher report **about**
BHL, not this investigation's direct consultation of Appendix A. Its reference
to Breuer likewise supplies no independently checked manuscript-by-manuscript
apparatus here. These publications concern Leningrad and cannot be counted as
additional ancient Hebrew witnesses.

The [published BHL foreword excerpts](https://tanach.us/Supplements/DotanForeword.html)
identify Aron Dotan's 2001 edition and explain why its edited body is not always
identical to the manuscript; Appendix A, “Manuscript Variants,” is listed at
pp.1229–1237. No actual Appendix A page, modern BHS/BHQ apparatus, or original
Breuer apparatus was inspected in this task. Those controls remain open.

The earlier [Leningrad image report](SAMUEL_EZEKIEL_CODEX_IMAGE_FOLLOWUP_2026-09-06.md)
favors final dalet in the color photograph while holding vav/yod. This task
does not claim a second independent inspection of those pixels. The Sefaria
API at [II Samuel13:37](https://www.sefaria.org/api/manuscripts/II_Samuel.13.37)
returned only `LC_Folio_175v`, range II Samuel13:18–14:1, on this retrieval.
One API result is not proof that other manuscripts lack the verse.

## Aleppo: actual image, not an edition substituted for ink

The [Haketer verse page](https://www.mgketer.org/tanach/9/13/37) gives the
ketiv/qere above and its Masorah discussion explicitly identifies het written,
he read. The project's [description](https://www.mgketer.org/home/index/)
identifies the edition as Aleppo-based but also describes reconstruction where
Aleppo is missing. Consequently that description alone cannot certify survival
of an individual word.

The [manuscript-image index](https://www.mgketer.org/kazms) led through
2 Samuel to [chapter13's reader](https://www.mgketer.org/mikra/9/13/1/mg/106).
Its actual script initializes `sefernum=8`, `prnum=13` and constructs the image
endpoint `/study/ketermsimage/` plus those values. The successful image is
[8_13](https://www.mgketer.org/study/ketermsimage/8_13), not `9_13`.
The latter, initially fetched by mistaking the public book number for the
script's zero-based index, proved to be **1 Kings13** and was rejected. Its
exploratory crops are not evidence for Samuel. No access control was bypassed.

The complete correct JPEG is 9,408×3,920, 16,392,104 bytes. Its leftmost panel
has a visible page numeral 63; the panel's rightmost column is headed by the
publisher's blue verse range לד–לט. No independent codicological folio/side
mapping is inferred from that numeral. The target is in the sequence of the
king's sons mourning, Absalom's flight, Talmai, Geshur, and David's mourning
(13:36–39). This context verifies the locus independently of the name.

Two local PNG rectangles were taken from the completed decoded JPEG, without
resizing, enhancement, rotation, thresholding, or generative processing. The
full-image display was reduced; the crops were viewed at native detail. In
the wider target crop `[2140,1130,3300,2050]` (top-left coordinates, right/bottom
exclusive), the body name after אל תלמי בן appears to have het, a vav-like
penultimate stroke, and final resh. The latter's shape is compatible with the
resh in following גשור and differs from the dalets of דוד in 13:39. The margin
at the same line reads עמיהוד with a qere indication: he, vav, final dalet.
This is a context-informed qualitative reading, not an independent certification
of every vowel/accent, a blinded comparison, or a finding about another codex's
hand. It is consistent with the published ketiv/qere control.

The publisher explicitly says it crops blank margins and performs some image
processing for legibility; these are **publisher-processed manuscript photos**,
not raw camera files. It credits Ben-Zvi Institute, Jerusalem, digital
photography Ardon Bar Hama, and directs readers to Ben-Zvi for originals.
The actual original photograph was not acquired. The project's
[rights page](https://www.mgketer.org/home/rights) is not permission to release
this image or its whole biblical edition under POB's license. Images and crops
remain private; the repository receives only observations, locators and hashes.

## DSS: a verse hit, but not a surviving patronymic

The actual [QDR biblical JSON at pinned commit f54f384](https://github.com/evenderekh/qdr/blob/f54f38464e18409eed8286fe24dd24f88d4735dd/data/qdr.1.1.biblical.json)
was retrieved and checked against SHA256 `3b90610a…`. The existing nested-word
extractor was called for the corpus's exact reference `2Sam 13:37`, with full
line context, and returns one manuscript record: **4Q51**, fragment identifier
`f102ii+103_106i+107_109a_b`, lines37–39. These identifiers are an editorial
fragment grouping and line coordinates, not additional witnesses.

Crucially, line38 contains the local sequence `תלמ[ י בן עמיחוד מ ]לך`.
The entire patronymic lies after that opening bracket and before its closing
bracket. The adjoining full lines37 and39 were inspected too; this conclusion
does not rely on a verse-only excerpt that may omit a bracket. On the published
transcription's restoration convention, **none of the patronymic's letters is
presented here as surviving**. Supplied עמיחוד also has het, not the qere's he.
It must not be silently relabelled either “DSS reads Ammihud” or “DSS agrees
with the qere.” This is a preservation judgment about a published transcription;
no 4Q51 photograph or DJD XVII plate/apparatus was freshly inspected.

The [QDR README](https://github.com/evenderekh/qdr/blob/f54f38464e18409eed8286fe24dd24f88d4735dd/README.md)
credits Michael Muzar's reader and Martin Abegg's transcriptions through
ETCBC/Naaijer. Its MIT code license does not cover the data: the latter are
CC BY-NC 4.0. Only the short bracket-boundary excerpt and factual metadata are
recorded, not the full corpus or full passage payload. The result is not a
negative DSS search; it is **positive indexed coverage / patronymic supplied**.
No other manuscript record is returned for this exact reference in this pinned
corpus. That is not an exhaustive claim about all physically extant DSS remains.

## Remaining control and next decision gate

The [ANU Codex Sassoon site](https://codexsassoon.org/) establishes a separate
early-medieval codex, not its reading at this locus. The attempted
[NLI manuscript viewer](https://www.nli.org.il/en/discover/manuscripts/hebrew-manuscripts/viewerpage?vid=MANUSCRIPTS&docid=PNX_MANUSCRIPTS990001349580205171-1)
returned HTTP403 by ordinary HTTPS; no alternate authority or bypass was used.
No Sassoon patronymic reading or locus-survival claim is assigned here.

Recommended outcome: **hold the source/name decision**, preserving the present
bytes. Review the separate version controls, acquire an actual accessible
critical-apparatus page if needed, and distinguish (1) a labelled Leningrad
transcription correction, (2) choosing a qere rendering, and (3) reconstructing
an earlier name. They require different justification. A small disclosure and
correction of the unrelated note's anchor can be proposed separately under the
editorial rules, but no exact note candidate is approved by this research.

Validation was limited to actual retrievals, local XML/JSON inspection, hashes,
and pixel-equality of the final crop. No canonical writer, registration,
historical snapshot rewrite, translation export, or regression run was needed.
