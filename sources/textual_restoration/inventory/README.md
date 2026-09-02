# Source-variant screening inventory

Generated with `python3 tools/textual_restoration/build_variant_inventory.py`.
This is a snapshot of canonical POB records and two source datasets, **not a
completed apparatus of all biblical manuscripts**. No canonical text is changed.

- `local_notes/`: typed textual notes or explicitly matched witness/reading
  terminology in POB footnotes. These are leads requiring verification.
- `hebrew_qere/`: written/read distinctions encoded in the WLC/OSHB XML.
  Qere/ketiv does not imply two independent manuscript witnesses.
- `hebrew_annotations/`: WLC editorial/transcription notes. Accent, vowel,
  consonant, and transcription observations are not all meaning-changing variants.
- `nt_editions/`: unmodified raw apparatus notes with added IDs, edition-label
  extraction, and same-reference POB pointers. Editions are not manuscript votes.
- `priority_cases.jsonl`: selected topics with local snapshots and apparatus
  entries at the anchor. Requested source families do not assert actual attestation.
- `summary.json`: counts, source and output hashes, and a canonical-snapshot
  digest. Layers overlap and must not be summed as unique variants.

Hebrew data retain WLC numbering; reference alignment, especially Psalms and
passage ranges, is still required. NT pointers are anchor-level, not token-level.
Absence of a local note or edition entry is not proof of no manuscript variants.

## Attribution

WLC underlying text: public domain. OSHB distribution: CC BY 4.0, see the
existing `sources/ot/wlc` notices. Hebrew inventory exports wording and notes,
not a new morphological corpus.

SBLGNT apparatus: © 2010 Society of Biblical Literature and Logos Bible
Software, edited by Michael W. Holmes; CC BY 4.0. Source:
[official publisher repository](https://github.com/Faithlife/SBLGNT).
The input is pinned with notices under `sources/nt/sblgnt_apparatus`; extraction
and screening fields were added by POB. No claim of publisher endorsement.

## Verify

```bash
python3 tools/textual_restoration/build_variant_inventory.py --verify-only
```

Offline verification checks saved artifact hashes, current WLC inputs, and
target definitions. Regenerate to refresh the canonical verse-file snapshot;
the verifier does not claim all current English verses remain unchanged.
