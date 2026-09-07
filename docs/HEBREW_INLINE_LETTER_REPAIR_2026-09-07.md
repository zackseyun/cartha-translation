# Hebrew inline-letter extraction repair — 2026-09-07

## Result

Fixed a production XML extraction defect and repaired 11 truncated Hebrew words
in 10 canonical source records. The words already exist in the vendored XML;
this is neither restored manuscript ink nor a new historical reading. Main
English is unchanged. A Hebrew quotation in Isaiah 44:14's footnote and four
connected lexical citations are corrected. Independent inspection corroborated
all affected XML words and identified the Judges qualification below.

| POB record | Complete XML word(s) |
|---|---|
| Leviticus 11:42 | גָּח֜וֹן |
| Numbers 27:5 | מִשְׁפָּטָ֖/ן |
| Deuteronomy 6:4 | שְׁמַ֖ע; אֶחָֽד |
| Judges 18:30 | מְנַשֶּׁ֜ה |
| Job 38:13 | רְשָׁעִ֣ים |
| Job 38:15 | מֵ/רְשָׁעִ֣ים |
| Psalms 80:13 | מִ/יָּ֑עַר |
| Proverbs 16:28 | וְ֝/נִרְגָּ֗ן |
| Isaiah 44:14 | אֹ֖רֶן |
| Jeremiah 39:13 | וּ/נְבֽוּשַׁזְבָּן֙ |

The [repair receipt](../sources/textual_restoration/applications/hebrew_inline_letter_repair.v1.json)
pins the original canonical records and XML files, gives before/after Hebrew,
and identifies each word and inline annotation. Psalm 80:13 maps to XML Ps.80.14;
the XML itself supplies the KJV:Ps.80.13 mapping. No new source acquisition.

## Cause and repair boundary

`tools/wlc.py` read only a word element's leading `.text`, omitting nested
`seg` content and its following tail. This dropped both the specially formatted
letter and, in several words, ordinary letters after it. The parser now assembles
the whole word, retains annotation type/text/code-point offset, and rejects
unexpected inline markup. Only x-large, x-small and x-suspended segments are
accepted. Qere/reading-note words remain outside the written-word stream.
The original XML retains the full note apparatus; this patch does not newly
implement that apparatus in the prompt or reader. Existing punctuation rendering
and paragraph-marker handling are unchanged, not certified as exact XML layout.

All ten sources continue to identify WLC. Old review objects are preserved as
historical and current records are draft/needs-review, not automatically fully
approved translations. The Lev/Isa/Jer lexical repairs only restore truncated
citations. In Judges, the malformed citation is replaced by the complete base
spelling and its rationale now explicitly separates that spelling from POB's
existing “Moses” choice. WLC has Manasseh with a suspended nun; English Moses
and its existing alternative note are retained. This parser repair does not
adjudicate which name is earlier. Isaiah's existing tree-species uncertainty is
also retained; only the missing nun in its quoted Hebrew is supplied from XML.

## Whole-OT screen and what it does not establish

The preceding pass was verified progress on NT attribution. This pass reused
the existing WLC/UXLC parsing and normalization functions for a local base screen:
23,264 canonical OT records, with 23,262 WLC labels and two explicit POB-critical
records (1 Samuel 17:4 and Isaiah 53:11). Those editorial texts were not reverted.
The pre-edit path/hash manifest was
`856668006a8a8f681d8629f1e0f01c587a66367e1ae02e0eb9684a6d2c154b54`.

Outside Psalms, 17,546 records matched the full written consonant stream and
3,138 matched the legacy parser instead; two had explicit critical labels.
The 3,138 are **not manuscript variants or 3,138 damaged words**: the initial
comparison excludes paragraph signs that the legacy representation appends as
Hebrew letters, and also exposes the small inline-letter defect isolated here.
Inspecting every direct XML word found exactly 11 annotated words in 10 verses.
No unexplained non-Psalm consonant difference outside those initial categories
was found by this screen; this is not a pointing, qere, punctuation or English audit.

Psalms was screened by chapter concatenation to avoid assuming identical verse
numbering: 97 chapters matched and 53 differed. That is not a valid universal
corpus reconstruction: Psalm 11's heading and body records, for example, both
retain the same full source verse as context. Do not treat these flags as 53
textual variants or automatically delete duplicate-looking Hebrew. Explicit
source-span alignment is required before claiming full Psalms source coverage.

## Verification

Regression tests cover all direct written words in all 39 vendored XML books,
the complete 11-word annotation inventory, all ten canonical repair strings,
loaded morphology, tail/initial/multiple segments, unexpected markup and qere
exclusion. Before/source hashes match, main English is identical, all historical
objects are preserved, and no new verse-schema errors are introduced. Among the
ten reader verse objects, only Isaiah 44:14 changes, solely in its Hebrew note
quotation. This is not a fresh deployment or full-book translation review.

The combined 36-test run had 35 passes and one stale-snapshot failure in the
preexisting UXLC/WLC receipt test, first reported at untouched 2 Samuel 13:37.
That failure is not repaired by repinning historical inputs. The focused current
parser/reader results and drift diagnosis are recorded at closeout below.

Closeout: all **22 focused parser/reader tests pass**. Checking every pin in the
older comparison receipt found only the 2 Samuel 13:37 drift; its current bytes
equal HEAD before this task's changes. Thus the broader failure is confirmed
preexisting, not attributed merely by assumption. Historical pins are unchanged.

Repair receipt SHA-256:
`ac93e8e00bb0a4db92c79c2522c9d35e0e2d120c766aa58235c421c3bbca2042`.
