# Isaiah 53:11 — should POB include “light”?

Research baseline: `8fd27c83d7`; checked 2026-09-06. **Provisionally favor the
attested addition אור, “light,” for a proposed critical source reading.** This
is a source-unit recommendation, not a completed verse replacement or an applied
change. The existing Hebrew/English files remain unchanged.

## Actual Hebrew evidence

The exact anchor in the [pinned QDR biblical data](https://github.com/evenderekh/qdr/blob/f54f38464e18409eed8286fe24dd24f88d4735dd/data/qdr.1.1.biblical.json)
is `Is 53:11`. It returns seven line records across four scroll IDs, not seven
independent witnesses. The primary transcriptions below are version 2026-05-21.

| Witness and locus | Published target text | Evidentiary weight at this unit |
|---|---|---|
| [1QIsaᵃ, 44:19](https://lexicon.qumran-digital.org/transcriptions/1QIsa%5Ea%5E/2026-05-21/index.html#c9525-i41754) | `יראה אור וישבע` | “See light” printed without restoration/uncertainty marks; conjunction before the next verb. |
| [1Q8 = 1QIsaᵇ, 23:22](https://lexicon.qumran-digital.org/transcriptions/1Q8/2026-05-21/index.html#c9565-i42420) | `יראה אור יש[בע]` | “See light” fully printed; end of the following verb restored. QDR flags uncertainty in that following verb which the newer display does not mark. |
| [4Q58 = 4QIsaᵈ, 8:20](https://lexicon.qumran-digital.org/transcriptions/4Q58/2026-05-21/index.html#c337257-i337301) | `יראה או֯[ר ]ושבע֯` | Partial support: aleph unmarked, vav uncertain, resh supplied. Following form is `ושבע`, not `וישבע`. |
| [4Q56 = 4QIsaᵇ, fragment 39:1](https://lexicon.qumran-digital.org/transcriptions/4Q56/2026-05-21/index.html#c10589-i48990) | Later clause beginning with `עבדי` | Verse overlap, not preservation or omission of the light clause. Do not confuse 4QIsaᵇ with 1QIsaᵇ. |
| [Retained WLC, Isa.53.11](../sources/ot/wlc/Isa.xml) | `יִרְאֶה יִשְׂבָּע` | No explicit object “light”; a genuine shorter reading, not missing digital coverage. |

These are published transcription findings, not fresh observations of parchment.
The [project sigla](https://lexicon.qumran-digital.org/faq/v1/en/index.html#sigla)
distinguish restored letters from uncertain remains. Related QDR and primary
website representations do not create additional ancient witnesses. In
particular, “three fully preserved identical Hebrew phrases” would overstate
both survival and agreement. No new date, scribal hand or genealogy is assigned.

## Greek support and the shorter-reading counterevidence

The [pinned Greek digital control](https://github.com/OpenScriptorium/lxx-morph/blob/c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2/db/seeds/lxx_morph/isaiah.json),
`Isa 53:10–12`, has `δεῖξαι αὐτῷ φῶς`, “to show him light,” within a different
syntactic construction. It supports light, not an identical Hebrew vocalization
or the complete English sentence. Only `words[].surface` was consulted; this
Rahlfs-labeled derivative is not a new manuscript or full Greek apparatus.

[John Meade's 2020 textual discussion](https://evangelicaltextualcriticism.blogspot.com/2020/04/he-will-see-light-in-isaiah-5311.html)
also identifies light in the Old Greek and reports the shorter form through
Aquila, Symmachus and Theodotion. He explains that Ziegler's split apparatus
entries obscure a continuous marginal quotation in Ra 86. The reproduced
Ziegler excerpt was visually checked: it splits the seeing and following-verb
entries. The continuous manuscript note itself was not inspected here; its
reading remains Meade's report, not our independent transcription. These later
Greek translations must not be collapsed into a single undifferentiated LXX.

Meade favors light partly because 1QIsaᵇ, despite its generally close relation
to proto-MT, agrees here with other Hebrew and Greek witnesses. That relationship
assessment is his published argument, not a new measured genealogy in POB.
His proposed copying omission is plausible, not an observed copying event.

## Decision, contrary explanation and English effect

Our evaluation favors inclusion because the full Hebrew object is attested in
two distinct manuscript transcriptions, with qualified additional Hebrew and
Greek support. This is stronger than supplying a word solely by retroverting
Greek or filling a damaged image. It is not a simple four-to-one witness vote:
relationships, partial survival and the different Greek syntax remain relevant.

The strongest counter-explanation is that an originally objectless “see” was
clarified by adding the familiar light idiom, with that expansion subsequently
shared in transmission. Conversely, the shorter text may reflect loss of the
object. The exact omission mechanism and branching history are not established.
The shorter reading's difficulty does not automatically make it original, and
the longer reading's fluency does not automatically make it secondary. The
cross-witness support tips this bounded recommendation toward light, with
historical priority still provisional.

Proposed consonantal unit, **not an applied WLC correction**:

```text
Retained:  יראה ישבע
Proposed:  יראה אור ישבע
```

This isolates the object decision; it does not import all 1QIsaᵃ conjunctions,
4Q58 verb forms or Greek syntax. Any pointed critical text must identify its
editorial vocalization and retain the exact base separately. It may not call a
modified line verbatim WLC.

POB currently begins: “From the anguish of his soul he will see and be satisfied.”
The minimal candidate is: **“From the anguish of his soul he will see light and
be satisfied.”** This is not a blinded full-sentence translation winner.
Keep the metaphor “light,” not an unmarked expansion to “light of life” or
“rise from the dead.” Local WLC Job 3:16 uses seeing light of infants, while
33:28,30 connect light with deliverance and life. Those usage controls do not
add the word “life” to the Isaiah witnesses or identify the servant. Meade's
[theological application](https://textandcanon.org/recovering-the-resurrection-textual-criticism-and-easter/)
is separate from our source selection; doctrinal desirability is not evidence
that one reading is earlier.

## Application boundary and stop condition

The [current verse](../translation/ot/isaiah/053/011.yaml) already mentions light,
but only as “some ancient witnesses.” Its two note anchors are misplaced:
the knowledge note follows “satisfied,” and the light note follows “many.” A
future full-record candidate must fix those anchors, name support accurately,
update the source label/apparatus and connected rationales, and archive stale
review scores. The unchanged 0.95 model-agreement score is not approval of this
proposal. The knowledge construction and rest of the verse require their own
English review; this object decision does not settle them.

Stop at **propose a source-changing candidate**, not “recovered autograph” or
“applied translation.” This case needs source-selection and full-verse English
review before promotion. The current successor verifier permits note/metadata
changes only and cannot authorize this Hebrew/main-English change. Do not evade
that scope by treating light as a footnote-only edit or silently changing WLC.
No new image restoration or ImageGen experiment is required to establish the
already attested word. Further source work should address transmission or
contrary evidence, not repeat the same four verse-anchor hits.

## Reproduction and access limits

- QDR JSON SHA256: `3b90610ab70a737aeb329b3d35af0d941b354d374503866d3dd8b30b914c8295`.
- Versioned primary HTML (retrieved with `?v=2026-05-21`): 1QIsaᵃ `4af5795fda749af47afa896fe985d78c5dfde3e9ea60bd17a445096f68741a32`; 1Q8 `e8d8da5b2a63c28c90eb6ae97d0a739cc20ea86b4a9396a2ec0666269b148d44`; 4Q58 `f226461e9fcb83cad0691ba54c6cc0640df2af5a30bba32151d8de33d0e3deb6`.
- WLC Isa.xml SHA256: `0807678de609bdef284bed5400b94ddab570d101b593c7f59ae1939015572fa2`.
- Canonical Isaiah YAML SHA256: `ba43727be38285048f014f05f8b8eb853faa058a7f6c5561de3f5ed0212c09d8`.
- Greek JSON SHA256: `c60980806a91bfde385004f5bbc030268f95803503527224ba760330390bed56`; note its reference prefix is `Isa`, not `Isaiah`.
- Meade's reproduced Ziegler apparatus image SHA256: `6626a2297f1e97b70ac43f8cab57778fe1d0bcd5ff8b5eae90e9a02e5dd6ee92`; `Isa53.11_Edition.JPG`, linked through his 2020 post. This is a cropped excerpt, not a consulted complete modern apparatus.

NET and the authorized UBS commentary pages were unavailable in this pass;
neither was used as evidence. Large primary transcription pages were retrieved
through ordinary public HTTP after web-reader failures. No canonical, source-data,
executable or test file changed; no deployment or generated reconstruction.
