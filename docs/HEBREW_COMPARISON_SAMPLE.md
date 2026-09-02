# Hebrew witnesses: a three-passage English comparison

Checked: 2026-09-02. Scope: a source-comparison demonstration, not a new
manuscript discovery, image-restoration result, or approved translation change.

## What is possible now

We can compare POB's local Masoretic Hebrew source with documented readings from
other Hebrew manuscripts, identify changes of wording, number, or passage
length, and show the resulting English alternatives. This does not require
ImageGen or a newly commissioned human transcription.

The Qumran readings below were checked in published scholarly discussions. They
are printed here in modern Hebrew type, without vocalization, and are not fresh
image-addressable diplomatic transcriptions by Codex. Full fragment boundaries,
damaged-letter marks, and surrounding lacunae are not reproduced. No missing
letters have been generated or newly recovered in this sample.

The dataset is
[`../sources/textual_restoration/samples/hebrew_comparison.v1.json`](../sources/textual_restoration/samples/hebrew_comparison.v1.json).
It records the local source snapshot, hashes, reported witness readings,
English effects, citations, and non-promotion status.

## 1. A changed number: Goliath's height — 1 Samuel 17:4

| Hebrew witness | Changed Hebrew word | English effect |
|---|---|---|
| Masoretic Text, represented by POB's WLC source | שש — six | His height was **six cubits and a span**. |
| 4QSam-a / 4Q51, reported Qumran reading | ארבע — four | His height was **four cubits and a span**. |

Only the numerical word is displayed so that surrounding reconstructed words
are not mistaken for fully surviving manuscript ink. This is a Hebrew textual
variant, not two possible translations of the same Hebrew word. Greek evidence
also supports four, but the Qumran manuscript gives us Hebrew evidence for it.
Choosing the earlier reading still requires textual-critical judgment; the age
of a surviving copy alone does not settle that judgment.

The current local [POB verse](../translation/ot/1_samuel/017/004.yaml) uses six.
Its footnotes explain the champion idiom and approximate height, but do not
mention the four-cubit Hebrew variant. This is an apparatus-coverage finding,
not a claim that the current main text has already been proven wrong. Retain
ancient units in the comparison because modern cubit conversions are uncertain.

Evidence: J. Daniel Hays, [The Height of Goliath: A Response to Clyde Billington](https://etsjets.org/wp-content/uploads/2010/06/files_JETS-PDFs_50_50-3_JETS_50-3_509-516_Hays.pdf),
JETS 50/3 (2007), especially p. 513; the Hebrew numerical variant is also set out
in this [University of Helsinki text-critical study of Samuel](https://helda.helsinki.fi/server/api/core/bitstreams/6e381d49-3bc5-4e67-a8d2-b2afa567a1a2/content),
under 1 Samuel 17:4.

## 2. A changed referent: nations and inheritance — Deuteronomy 32:8

| Hebrew witness | Key phrase | English effect in the final clause |
|---|---|---|
| Masoretic Text, represented by POB's WLC source | בני ישראל | according to the number of the **sons of Israel** |
| 4QDeut-j / 4Q37, reported Qumran reading | בני אלוהים | according to the number of the **sons of God** |

The difference changes who is being counted. The second wording is commonly
understood as referring to divine beings; that interpretation should remain
separate from the literal rendering. Greek witnesses with sons or angels of
God provide versional support, not another Hebrew manuscript.

The current local [POB verse](../translation/ot/deuteronomy/032/008.yaml) uses
sons of Israel and already includes a footnote about the Qumran/Greek
alternative. The next improvement would be precise manuscript attribution,
not claiming this as a newly discovered variant. This sample does not establish
the motive of any ancient scribe or settle the passage's theology.

Evidence: Emanuel Tov, [The Sons of Israel or God? — Deuteronomy 32:8](https://www.thetorah.com/article/the-sons-of-israel-or-god-deuteronomy-32-8),
especially the witness table. Tov supplies the reported Qumran spelling used
here; a later image-first audit must separately preserve damaged-letter marks.

## 3. An additional line: Psalm 145 after verse 13

| Hebrew witness | Evidence at the nun-line position | English effect |
|---|---|---|
| Leningrad/Masoretic base used by POB | No corresponding line; the acrostic proceeds from mem to samekh | No extra sentence after verse 13. |
| 11QPs-a / 11Q5, column XVII, lines 2–3 | נאמן אלוהים בדבריו וחסיד בכול מעשיו | **God is faithful in his words and loyal in all his deeds.** |

The sample English is a direct illustrative rendering. The Qumran text uses
God, while the corresponding Greek line uses Lord; these must not be silently
conflated. The scroll's recurring refrain is outside this excerpt.

The acrostic structure and other ancient versions make the additional line
important evidence. They do not, by themselves, prove whether it was omitted
from one tradition or supplied in another. That direction-of-change question
remains distinct from the secure observation that the witnesses differ.

The current local [POB verse](../translation/ot/psalms/145/013.yaml) contains
only the kingdom/dominion sentence and a lexical footnote; it does not disclose
this additional Hebrew line. Nothing in the canonical YAML was changed for
this demonstration.

Evidence: Peter W. Flint, [The Significance of the Biblical Dead Sea Scrolls](https://swbtsv7.s3.amazonaws.com/media/Theology_Journal/53.1/53.1_Flint.pdf),
Southwestern Journal of Theology 53/1 (2010), pp. 19–21; the Hebrew excerpt and
manuscript location are on p. 20. This citation is used for this specific
excavated witness, not as an endorsement of every historical claim or later
private-market fragment mentioned elsewhere in the article.

## What the sample demonstrates — and what it does not

- **Demonstrated:** real Hebrew variants can change an English number, the
  referent of a phrase, or whether an entire sentence is included.
- **Demonstrated:** POB's existing footnotes already disclose some variants,
  while these local Samuel and Psalms records have disclosure gaps.
- **Not demonstrated:** a new decipherment, recovery of invisible ink, complete
  comparison of every witness, or certainty about the lost original wording.
- **Not done:** canonical edits, translation publication, deployment, or
  ImageGen reconstruction.

The next useful implementation is a verse-level apparatus with both readings,
witness IDs, source links, a clear English difference, and a separate adoption
decision. Image-first transcription can follow for selected fragments. Codex
can process existing lawful captures, but cannot create genuine spectral data
that was never captured. ImageGen can illustrate a reconstruction; it cannot
supply evidence for the Hebrew.
