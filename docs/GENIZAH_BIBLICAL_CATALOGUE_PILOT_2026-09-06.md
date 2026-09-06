# Cairo Genizah biblical catalogue pilot — 2026-09-06

## Result and boundary

Actual Cambridge catalogue screening now covers **40 ordered search hits across Genesis and Psalms**, with complete institutional records and contextual manuscript-image inspection for **two shelfmarks**. This is a non-DSS coverage increment, not a complete Genizah census, a count of newly independent manuscripts, or a textual adjudication. No canonical text, English, registry, or frozen artifact was changed.

The principal result is an evidence crosswalk: T-S B6.24 digital canvas **1r** locally matches the catalogue's **fol. 2**; T-S A43.8's final canvas is a bifolium displaying nonadjacent Psalm contexts, not a reliable locator for the catalogue's final Psalm. Both records also contain structured/prose column-count conflicts. These hazards would matter in subsequent verse-level comparison.

The [JSON record](../sources/textual_restoration/discovery/genizah_biblical_catalogue_pilot.v1.json) preserves all 40 ordered shelfmarks, catalogue IDs, record URLs, screening classifications, the two complete-record crosswalks, and ten private-download hashes. This report follows the source-wording method and extends the coverage audit/Masoretic spine's still-open Genizah lane. Observations are agent-made, context-informed, and not a claimed human, specialist, blinded, or independent transcription pass.

## Executed query and denominators

Cambridge Digital Library's advanced search was run with Collection **Cairo Genizah**, Language **Hebrew**, keyword **Genesis**, then **Psalms**; author, title, subject, place, location and classmark were blank. Default displayed order was retained. Every description on page 1 was read, with no later pages sampled. Exact query URLs are in the JSON: [Genesis query](https://cudl.lib.cam.ac.uk/search?FacetCollection=Cairo%20Genizah&author=&keyword=Genesis&language=Hebrew&location=&page=1&place=&shelfLocator=&subject=&title=), [Psalms query](https://cudl.lib.cam.ac.uk/search?FacetCollection=Cairo%20Genizah&author=&keyword=Psalms&language=Hebrew&location=&page=1&place=&shelfLocator=&subject=&title=).

| Query | Displayed total | Screened | Description-based classification |
|---|---:|---:|---|
| Genesis | About 529 results; 27 pages | 20 | 2 Hebrew Bible/Onqelos; 2 shorthand; 13 commentary/translation; 1 masora; 1 writing exercise; 1 liturgy |
| Psalms | About 738 results; 37 pages | 20 | 1 mostly full text with occasional abbreviation; 19 shorthand |

These are **40 distinct shelfmarks in this convenience sample**, not 40 genealogically independent copies. Search totals are approximate, overlapping keyword-hit universes; do not sum them into a manuscript denominator. Hebrew-language filtering admits Judaeo-Arabic commentary and translations with Hebrew incipits as well as Hebrew/Aramaic bilingual text. The Genesis result T-S Misc.5.24 is principally commentary on Psalms citing Genesis. T-S A43.4's Genesis 4:8 range and T-S NS280.61's Psalm 22:17 range are shorthand locators, not proof of the complete disputed wording.

Three fuller-text targets were retained: Genesis results 17–18 (T-S B7.14 and T-S B6.24), and Psalms result 6 (T-S A43.8). The other 37 are held outside an automatic continuous full-word-copy lane, **not discarded as evidence for what they actually quote, abbreviate, translate or use liturgically**. No Sirach item was identified in these 40 descriptions; this is not an absence claim about the collection. Only two full records and two of their 12 canvases were inspected in depth.

## T-S B6.24: bilingual Genesis and a digital-label mismatch

The [institutional record](https://cudl.lib.cam.ac.uk/view/MS-TS-B-00006-00024/1), [TEI](https://services.cudl.lib.cam.ac.uk/v1/metadata/tei/MS-TS-B-00006-00024/) and [IIIF manifest](https://cudl.lib.cam.ac.uk/iiif/MS-TS-B-00006-00024) describe two mutilated parchment leaves containing Hebrew Bible and Targum Onqelos with Tiberian notation. The catalogue dates the Ashkenazi square script **probably to the thirteenth century**. This is the physical-copy estimate, not the date of Onqelos. Donation in 1898 and metadata revisions in 2024/2026 are separate events.

Catalogue fol. 1 covers Genesis 16:15–17:5, 17:9–10 and 17:15–21; fol. 2 covers 17:22–27 and 18:5–18. The manifest has four canvases labelled 1r, 1v, 2r, 2v. Actual image `MS-TS-B-00006-00024-000-00001.jp2`, labelled **1r**, shows a handwritten **2a**, tag **T-S B6.24 P1**, and the Genesis 17:24–26 context in its right column. A source-native region clearly preserves the Hebrew age phrase **בן תשעים ותשע שנה**, with surrounding Aramaic lines. The starts of damaged lines are not restored as visible ink.

The contextual sequence plus handwritten number support a **local alignment to catalogue fol. 2**, not catalogue fol. 1. This does not establish which numbering system is erroneous, revise Cambridge metadata, or resolve all four sides. The strongest mundane explanation is different physical/editorial versus digitization ordering; it is not a textual variant. Hebrew and Aramaic in one object must remain separate evidence lanes, not two independent Hebrew witnesses. Holes and discontiguous catalogue ranges cannot be converted into attested omissions.

## T-S A43.8: mostly full Psalms, four bifolia, eight canvases

The [record](https://cudl.lib.cam.ac.uk/view/MS-TS-A-00043-00008/1), [TEI](https://services.cudl.lib.cam.ac.uk/v1/metadata/tei/MS-TS-A-00043-00008/) and [manifest](https://cudl.lib.cam.ac.uk/iiif/MS-TS-A-00043-00008) describe Psalms 119:38–145:16, mainly written in full but occasionally shortened to lemma/serugin, with partial Tiberian notation and marginal masora. There are **eight leaves, four bifolia**, and eight digital canvases labelled 1r through 4v. No copy date is provided in the consulted record; 1898 is the donation date, not a manuscript date.

Canvas 8, labelled **4v**, image `MS-TS-A-00043-00008-000-00008.jp2`, shows tag **T-S A43.8 P4**, a bifolium with six columns, and substantial edge damage. Its right leaf contains the end of Psalm 119 and beginning of Psalm 120; the left has Psalm 135/136 context. The regional image confirms Psalm 119:176 followed by an abbreviated Psalm 120 heading and its opening context. This is context identification, not a diplomatic page transcription or certification of every letter. The abbreviated heading illustrates the catalogue's warning; it is not evidence for an accidentally lost heading.

The final canvas therefore **does not verify Psalm 145 or the nun-line question**. Mapping the other seven canvases is an explicit next task. Neither eight leaves nor eight canvases means eight manuscripts. No cross-shelfmark joins were asserted in either full record; absence of such a note does not establish that the shelfmarks have no joins or relationships elsewhere.

## Metadata, access and rights controls

Both TEIs encode `columns="1"` while their prose says two columns for Genesis and three for Psalms; the inspected images fit the prose locally. Do not silently select the structured attribute in a future parser. The TEI bodies contain page-break references rather than diplomatic transcriptions. Catalogue ranges and image availability are not surviving-letter inventories.

The web tool received a 403 at the collection landing page. Ordinary Chrome successfully displayed the collection, queries and records without login, an interstitial or bypass. Chrome's attempted content export was unsupported: the ordered search sample is agent-recorded from the displayed DOM, not a saved raw search-response file. Public record-linked TEI and IIIF requests worked. No PDF or paywalled edition was used.

The whole-image requests returned **server-limited derivatives**, not the native source rasters: Genesis 1365×2000 from advertised 6804×9972; Psalms 2000×895 from 6358×2845. Two documented IIIF regions, within the advertised 2000×2000 maximum, were inspected at source-native scale: Genesis `(3400,3400,2000,2000)` and Psalms `(3300,350,1500,2000)`. Coordinates are source-raster pixel x/y/width/height. They use full regional size, rotation zero and default JPEG; no local image transformation, enhancement, stitching, OCR, generated letters or ImageGen was used. Native-scale regional context does not make the whole-image derivative native resolution.

Cambridge's metadata is explicitly **CC0**. Its images are **not CC0**: the record permits fair-use/fair-dealing uses including research/teaching, and directs publication/public-web reproduction requests to `genizah@lib.cam.ac.uk`. All ten acquired files remain private under `/private/tmp/pob-genizah-pilot.T1D72w`; the JSON records URLs, bytes, SHA-256, actual dimensions and transformation descriptions. No manuscript images or full copyrighted transcriptions are vendored.

## Next bounded expansions and outcome

1. T-S B7.14: map P1/P2/P3 and the catalogue's five leaves against individual canvases before comparing its Genesis 42–43 Hebrew and Onqelos.
2. T-S AS67.19: the search description reports an abbreviated Tetragrammaton at Psalm 77:8 where MT has אדני. This is a **catalogue-reported lead only**; inspect its actual marks, abbreviation practice and neighbors before calling it a substantive variant.
3. T-S A43.8: map the remaining canvases and locate Psalm 145 explicitly; no present finding about the nun line.
4. Expand the dated sample to later result pages, other books and other institutional collections, preserving genre exclusions, physical joins and dependency holds. The present first-page order is not representative.

No source-wording or English change is proposed. Familiar contextual words were used as navigation anchors, not as a test that proves the current base correct. Reading priority, disputed-letter adjudication, apparatus consultation, and genuinely independent/blinded work remain separate later gates.
