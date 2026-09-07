# Nahash transition: 1 Samuel 10:27–11:1

Checked 2026-09-07. Outcome: qualified reader disclosure applied, not a
selection of the earliest Hebrew form. No new manuscript-image reading.

## Evidence actually compared

- Current WLC/POB 10:27 ends with Saul keeping silent; 11:1 begins the advance
  of Nahash. The longer background account is absent. POB 11:2 supplies the
  following threat to gouge out right eyes. The existing two lexical notes
  were attached to unrelated speech/name positions.
- [Qumran-Digital 4Q51, version 2025-03-11](https://lexicon.qumran-digital.org/transcriptions/4Q51/2025-03-11/index.html),
  section 10a, lines 5–10: substantial longer Hebrew narrative, including Gad,
  Reuben, right eyes, and seven thousand men. Line 8's `שבעת אלפים איש` is
  unbracketed; surrounding words/letters include supplies and uncertainty.
  Line 9 presents a superscripted transition clause; this pass does not
  settle its insertion placement or hand. It is not flattened into a newly
  reconstructed continuous Hebrew text.
- Pinned Rahlfs control: 10:27 ends with the gifts, while 11:1 begins
  `καὶ ἐγενήθη ὡς μετὰ μῆνα`, approximately a month later. These two edition
  verses do not contain the long background paragraph. This is not a claim
  about every Greek witness. Only `ref` and `words[].surface` were used from
  `lxx-morph` commit `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`,
  `db/seeds/lxx_morph/1-samuel.json`, SHA256
  `8bd1346509aaa9804a92a7ebc3c0f2812cb4fb35e61f2d41c14b482e95fd70c5`.
- Josephus, *Antiquities* 6.68–71 (= VI.5.1), checked by the separate
  `nahash_josephus_control` agent in the
  [Chicago-hosted Whiston edition](https://penelope.uchicago.edu/josephus/ant-6.html),
  with [section-number control](https://lexundria.com/j_aj/6.68-6.94/wst).
  Earlier oppression and eye mutilation precede Jabesh, but the named tribes
  and seven thousand are absent. Josephus adds a military explanation and
  places the month introduction before the retrospective narrative. This is
  related narrative evidence, not a verbatim Hebrew witness or demonstrated
  independent transmission.

## Decision and stopping point

Preserved longer narrative warrants disclosure even while priority is open.
Loss from a longer text and explanatory expansion of a shorter text remain
serious competing accounts. This pass does not establish either mechanism.
The shorter base is provisionally retained, not favored automatically because
it is Masoretic; older physical attestation alone does not decide literary
priority or authorize exact supplied wording.

The next source-selection gate is specific: read the DJD XVII pp. 65–67
reading notes and competing locus-level literary arguments, and compare the
Greek transition apparatus. These materials were located as leads, not read
in this pass. The month transition and the longer paragraph must be evaluated
separately. Do not reacquire the same Qumran or Josephus controls merely to
repeat agreement. ImageGen is not evidence and was not used.

## Application and verification

Root applied the new textual-variant note after 11:1's first sentence. The
existing covenant note now follows the covenant phrase; 10:27's deafness note
now follows the silence phrase. No words other than markers changed in main
English, and Hebrew is unchanged. Existing note bodies, lexical decisions,
theological decisions and draft provenance were preserved. Old cross-check
and revision objects were archived verbatim; active status is draft/needs-review.

The agent separately checked the proposed disclosure and anchors: scoped PASS,
with no correction required. It read the published Qumran transcription and
used root's supplied Greek control; no blind test, independent Greek
collation, whole-verse fidelity certification, or source-priority approval is
claimed. Root's application decision is limited to these notes and markers.

| Record | Before SHA256 | After SHA256 |
| --- | --- | --- |
| 1SA.10.27 | f05c30e47c4ea5c19630481ce1e3a3145f8a7a5bdb8a95c4f457ecb35ddc3294 | de03160e7d272eb8ee0b6d3921f398e5847b8476307379310ecf72dd3e937cc2 |
| 1SA.11.1 | db94206baeabe5b7fe3039a37189edf75e5315e9d0c08ae2779845628ad0dd80 | 9159fbb0b928d0acaa0a67ce3551b740f8dd668ba9fe127741b32e93ca1e41d0 |

Both edited records pass the verse schema. Full before/after 1 Samuel export
retains all 811 verse keys and changes only 10:27 and 11:1; the new note is
present in exported output. Source, marker-free English, existing notes and
archived review objects passed exact-equality checks. Eight existing reader
footnote tests and Git whitespace checks pass. No deployment occurred.
