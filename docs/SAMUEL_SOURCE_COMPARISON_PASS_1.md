# Samuel source comparison — pass 1

Checked: 2026-09-04

## Outcome

The existing 1 Samuel 17:4 pilot has been upgraded from secondary-report-only
evidence to a pinned source comparison. The result strengthens, but does not
canonically promote, the working preference for four cubits and a span:

- WLC reads `שש אמות וזרת`, “six cubits and a span.”
- 4QSama (4Q51), fragments 12–14, line 3, reads
  `]א֯רבע[ א]מות וזרת`, supporting “four cubits and a span.”
- The pinned Rahlfs Greek control reads
  `τεσσάρων πήχεων καὶ σπιθαμῆς`, “four cubits and a span.”

The POB main text still reads six because its declared source remains WLC. Its
measurement footnote is now attached to the measurement rather than to “Gath,”
and it discloses the direct Hebrew and Greek four-cubit reading.

## Evidentiary boundary

The Qumran-Digital transcription places most of the surrounding clause inside
editorial brackets. Within the numeral, the alef is dotted as uncertain while
resh-bet-ayin are preserved. Part of `אמות`, “cubits,” is also supplied. This is
adequate published-transcription support for the numeral four; it is not a
claim that the whole reconstructed line is visible on the leather.

The physical manuscript is counted once. Qumran-Digital is its transcription
layer, the IAA record is its institutional identity and image-access layer, and
the Rahlfs reading is daughter-version evidence. Those access and edition
layers are not additional Hebrew witnesses.

## Reproducible controls

The Greek text was extracted from OpenScriptorium `lxx-morph` at commit
`c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`. During this pass, the earlier
Pentateuch record's upstream commit object was found to be unavailable. All six
stored Pentateuch Greek verses were compared byte-for-byte with the current
resolvable commit and were identical, so their snapshot metadata was refreshed
without changing any reading.

The 4Q51 transcript is pinned to its 2025-03-11 version. The IAA manuscript page
provides the institutional image inventory, but the exact fragments 12–14 image
region has not yet been crosswalked or independently read.

## Adjudication effect

The earlier moderate working preference for four remains appropriately
moderate. Direct early Hebrew and the Greek control converge on four, but the
six reading is also ancient in versional evidence, and the broader short/long
literary forms of the David–Goliath narrative must not be reduced to a single
number substitution.

No main-text change has been made. Before promotion, the passage still requires
image verification, the DJD XVII material and reading notes, individual Greek
manuscript collation beyond an edited Rahlfs control, broader Samuel literary-
form review, an independent editorial pass, and an atomic critical-Hebrew plus
English selection bundle.

## Next Samuel cases

1. 1 Samuel 10:27–11:1 — the Nahash narrative material in 4Q51 and its relation
   to Josephus and the shorter Masoretic transition.
2. 1 Samuel 14:41 — the shorter prayer and longer Urim–Thummim form, while
   keeping Greek retroversion distinct from surviving Hebrew ink.
3. 1 Samuel 1:24 — three bulls versus a three-year-old bull.
4. 1 Samuel 13:1 — a conjecture-control case in which missing numbers must not
   be silently supplied as recovered text.

Machine-readable evidence is in
[`../sources/textual_restoration/coverage/samuel_pilot.v1.json`](../sources/textual_restoration/coverage/samuel_pilot.v1.json)
and
[`../sources/textual_restoration/comparisons/samuel_controls.v1.json`](../sources/textual_restoration/comparisons/samuel_controls.v1.json).

Primary access points:

- [Qumran-Digital 4Q51 versioned transcription](https://lexicon.qumran-digital.org/transcriptions/4Q51/2025-03-11/index.html)
- [IAA Leon Levy Digital Library 4Q51 record](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q51-2?locale=en_US)
- [OpenScriptorium lxx-morph](https://github.com/OpenScriptorium/lxx-morph)
