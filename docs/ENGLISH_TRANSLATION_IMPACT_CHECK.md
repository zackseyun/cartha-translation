# Does the additional source evidence change POB English?

Checked: 2026-09-02. **Yes, selectively — but none of these research choices has yet changed the canonical English.**

This checks ten selected current local POB verse records. It is not a whole-Bible change estimate, fresh manuscript decipherment, or live-site audit. The three proposed replacements follow the existing provisional adjudications; the check does not upgrade their confidence or complete their outstanding review.

## Three concrete draft changes

Footnote markers are removed for readability. Only the source-dependent phrase changes; the rest of each current sentence is preserved.

### 1 Samuel 17:4

**Current:** Then a champion came out from the camps of the Philistines; his name was Goliath, from Gath. His height was six cubits and a span.

**Draft if the working source choice is adopted:** Then a champion came out from the camps of the Philistines; his name was Goliath, from Gath. His height was four cubits and a span.

- Difference: **six cubits and a span → four cubits and a span**.
- Source decision: `1SA.17.4.height` in [sources/textual_restoration/decisions/hebrew_pilot.v1.json](../sources/textual_restoration/decisions/hebrew_pilot.v1.json); confidence moderate.
- [Current canonical record](../translation/ot/1_samuel/017/004.yaml); unchanged by this check.

### Deuteronomy 32:8

**Current:** When the Most High gave the nations their inheritance, when he separated the sons of man, he fixed the boundaries of the peoples according to the number of the sons of Israel.

**Draft if the working source choice is adopted:** When the Most High gave the nations their inheritance, when he separated the sons of man, he fixed the boundaries of the peoples according to the number of the sons of God.

- Difference: **sons of Israel → sons of God**.
- Source decision: `DEU.32.8.referent` in [sources/textual_restoration/decisions/hebrew_pilot.v1.json](../sources/textual_restoration/decisions/hebrew_pilot.v1.json); confidence moderate.
- [Current canonical record](../translation/ot/deuteronomy/032/008.yaml); unchanged by this check.

### Mark 1:41

**Current:** And being angry, he stretched out his hand, touched him, and said to him, “I am willing; be cleansed.”

**Draft if the working source choice is adopted:** And moved with compassion, he stretched out his hand, touched him, and said to him, “I am willing; be cleansed.”

- Difference: **being angry → moved with compassion**.
- Source decision: `MRK.1.41.emotion` in [sources/textual_restoration/decisions/nt_pilot.v1.json](../sources/textual_restoration/decisions/nt_pilot.v1.json); confidence moderate.
- [Current canonical record](../translation/nt/mark/001/041.yaml); unchanged by this check.

## One possible added line: Psalm 145 after verse 13

The present verse ends with the kingdom/dominion sentence. The working source assessment tentatively favors a nun line. A Qumran-based English example is:

> God is faithful in his words and loyal in all his deeds.

This is **not finalized wording**. The earlier divine designation and some wording details remain unresolved, so no ready-to-publish verse replacement is supplied.

## Other passages checked

| Passage | Current English excerpt | Impact of this check |
|---|---|---|
| [John 1:18](../translation/nt/john/001/018.yaml) | the one and only God | God is already in POB; the alternative Son is already footnoted. The pinned SBLGNT apparatus also assigns the God reading to WH, Treg, and NA28. This is edition-level corroboration, not a completed manuscript adjudication. |
| [Jude 1:5](../translation/nt/jude/001/005.yaml) | that Jesus | Jesus is already in POB and alternatives are footnoted. The pinned apparatus lists NA28 with this name; comparison does not create a new English change here. |
| [Revelation 13:18](../translation/nt/revelation/013/018.yaml) | six hundred sixty-six | 616 is already footnoted. Its existence alone does not establish that POB should replace 666. |
| [Isaiah 53:11](../translation/ot/isaiah/053/011.yaml) | he will see and be satisfied | The existing note records the light variant; the expanded queue has not yet made an adopted source-choice decision for this verse. |
| [Psalms 100:3](../translation/ot/psalms/100/003.yaml) | we did not make ourselves | We are his is already footnoted. This is a written/read tradition issue; the inventory is not yet a decision to switch readings. |
| [Job 13:15](../translation/ot/job/013/015.yaml) | I will not wait | Hope in him is already footnoted. The consonantal written/read difference and the English rendering of the verb both require judgment. |

## What changes before publication

- A source-choice change must be recorded as a departure from the retained base edition. Do not silently relabel a modified Hebrew line WLC or a modified Greek line SBLGNT.
- Update the corresponding English, source-selection rationale, lexical decisions, alternate-reading footnote, and reference markers together.
- In 1 Samuel 17:4 the current height-conversion note would also need revision if four is adopted.
- Keep the rejected but material readings visible. Psalm 145 needs an explicit variant note even while exact-wording selection is held.
- Complete the outstanding evidence/review gates before canonical promotion; then synchronize POB/SPOB and reader exports separately. This check does not deploy anything.

## Result

- **3** provisional main-text replacements.
- **1** possible additional line with exact wording unresolved.
- **2** passages already express one of the supported edited readings.
- **4** further variants noted but not yet adjudicated.
- **0** canonical changes applied.

The 6,934 NT apparatus entries and 1,260 Hebrew written/read records are **not** counts of required English revisions. Some source differences leave English unchanged; some affect only notes, spelling, word order, or placement. No defensible corpus-wide revision percentage has been calculated.

[Machine-readable impact check](../sources/textual_restoration/decisions/english_impact_check.v1.json) · [Hebrew evidence report](HEBREW_PILOT_ADJUDICATION.md) · [NT evidence report](NT_PILOT_ADJUDICATION.md)
