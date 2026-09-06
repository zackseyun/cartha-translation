# Pentateuch source comparison — pass 3

Checked: 2026-09-04

## Outcome

The direct-Hebrew pass now reaches Deuteronomy 27:4 and 32:43. It also adds an
explicit distinction between a manuscript that supports a reading and a
manuscript that merely covers the verse while the decisive letters are lost.

- **Deuteronomy 27:4:** the Masoretic and Old Greek controls read Mount Ebal;
  the Samaritan Pentateuch reads Mount Gerizim. 4QDeutf (4Q33) contains the
  verse, but the whole mountain-name phrase is supplied inside a bracketed
  lacuna. It supports neither name.
- **Deuteronomy 32:43:** 4QDeutq (4Q44) preserves an unambiguously longer Hebrew
  form. The Old Greek is related but longer still, while the Masoretic and
  Samaritan controls preserve the shorter form.

No English main-text wording has been changed. Both cases remain
`not-adjudicated`; their POB notes now state the evidence more accurately.

## Pinned controls

The same reproducible controls used in the earlier passes were queried at their
pinned snapshots:

- the local POB WLC source field;
- DT-UCPH Samaritan Pentateuch 7.1.3 at commit
  `2f2120286ac48d4ff3d04e0107e33efd864aa9e1`;
- OpenScriptorium's Rahlfs LXX data at commit
  `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2` (the six stored Greek verses
  were rechecked byte-for-byte after the earlier recorded upstream object
  became unavailable); and
- QDR 1.1 at commit `f54f38464e18409eed8286fe24dd24f88d4735dd`,
  checked against versioned Qumran-Digital transcriptions and IAA manuscript
  identities.

The modern editions and transcription platforms are controls, not additional
physical manuscripts.

## Deuteronomy 27:4

| Evidence | Reading | Status |
|---|---|---|
| WLC/MT | `בהר עיבל` — Mount Ebal | supports Ebal control |
| Samaritan Pentateuch | `בהרגריזים` — Mount Gerizim | supports Gerizim control |
| Rahlfs LXX | `ἐν ὄρει Γαιβαλ` — on Mount Ebal | supports an Ebal Hebrew Vorlage as daughter-version evidence |
| 4QDeutf (4Q33), fragment 32–35, lines 6–7 | `ה[יום בהר עיבל ושדת או]תם` | **indeterminate lacuna** |

The brackets are decisive. They mark editorial reconstruction, not visible
letters. The record therefore says that 4Q33 covers the verse but cannot vote
for Ebal or Gerizim. This corrects a common methodological error: a supplied
word in a published transcript must not be converted into manuscript support.

Reports based on unprovenanced or private-market fragments are excluded until
an authenticated object and a stable scholarly publication clear the normal
evidence gates.

## Deuteronomy 32:43

4Q44, fragment 5 ii, lines 6–11, reads:

```text
הרנינו שמים עמו
והשתחוו לו כל אלהים
כי דם בניו יקום
ונקם ישיב לצריו
ולמשנאיו ישלם
ויכפר אדמת עמו
```

A close English rendering is: “Rejoice, heavens, with him; bow down to him, all
gods; for he will avenge the blood of his sons; he will return vengeance to his
adversaries and repay those who hate him; and he will atone for the land of his
people.”

This is direct Hebrew evidence for a longer ancient form. It differs from the
shorter MT/Samaritan form in at least five linked features: heavens rather than
nations in the opening, the command to all gods, sons rather than servants, the
repayment of those who hate him, and the closing construction “land of his
people.”

The Old Greek contains those broad features but is not identical. It adds
separate calls to the nations and to all angels of God. It is therefore wrong
to merge “4Q44 + LXX” into a single longer reading or count them as two copies
of one Hebrew manuscript.

The relevant fragment is visibly located on IAA image record B-280818, PAM
M42.164 (scanned infrared negative, recto). This is a plate-level locator, not a
stored image derivative or a measured region. It narrows the next verification
step without overstating what has been completed.

## English POB impact

- The marker on Deuteronomy 27:4 now sits at “Mount Ebal,” and its note explains
  both the Samaritan reading and 4Q33's evidentiary limit.
- The markers on Deuteronomy 32:43 now sit at the phrases they explain. Its
  textual note quotes the 4Q44 form and distinguishes the still-longer Greek.

The longer 32:43 form deserves formal adjudication and an English candidate,
but the current comparison package deliberately forbids a preferred reading or
canonical-change flag. Image verification and internal/external evaluation
come first.

## Next gates

1. Map the exact IAA image plate for 4Q33 and measured regions for 4Q33 and 4Q44.
2. Independently verify the visible letters, especially the joins and damaged
   characters in 4Q44, without treating supplied characters as ink.
3. Consult DJD XIV for the material reconstruction and editorial rationale.
4. Split Deuteronomy 32:43 into aligned variation units and test whether the
   shorter or longer forms better explain the multiple ancient editions.
5. Continue to Deuteronomy 32:8, then expand beyond the Pentateuch to Samuel,
   Jeremiah, Isaiah, and Psalms.

Machine-readable records are in
[`../sources/textual_restoration/coverage/pentateuch_pilot.v1.json`](../sources/textual_restoration/coverage/pentateuch_pilot.v1.json)
and
[`../sources/textual_restoration/comparisons/pentateuch_controls.v1.json`](../sources/textual_restoration/comparisons/pentateuch_controls.v1.json).
