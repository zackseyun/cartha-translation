# Dead Sea Scrolls and Ancient Witness Backlog

This is the implementation backlog for the
[POB Dead Sea Scrolls and Ancient Witness Project](DSS_TEXTUAL_WITNESS_PROJECT.md).
Checkboxes mean repository evidence exists; they do not imply scholarly
acceptance or live-reader publication.

## Foundation

- [x] Create the project charter and evidence-lane rules.
- [x] Create a machine-readable initial scroll registry.
- [x] Create a broader Hebrew/Aramaic/Greek comparison-witness registry.
- [x] Create a schema for image-addressable diplomatic transcription and
  restoration candidates.
- [x] Add a validator that enforces hashes and blocks vendoring
  permission-required images.
- [x] Add deterministic image enhancement with provenance sidecars.
- [x] Retrieve four lawful LOC pilot images (two War Scroll, two Pesher
  Habakkuk previews) and verify SHA-256 hashes.
- [x] Retrieve the four corresponding LOC TIFF masters locally and record their
  hashes; keep the 145 MB rehydratable masters outside normal Git history.
- [ ] Publish a Codex-only adjudication guide and blinded-pass agreement
  procedure.
- [ ] Add machine-corroboration states that distinguish visible ink,
  independently supported readings, hypotheses, and physical loss.

## Rights and acquisition

- [ ] Ask the IAA for written permission covering bulk research access,
  redistribution, crops, non-generative derivatives, and public display.
- [ ] Ask the Israel Museum separately about Great Isaiah, Community Rule,
  Temple, War, and Habakkuk high-resolution assets.
- [ ] Record the response, exact license, attribution, expiry, and allowed
  downstream uses per image—not as a collection-wide assumption.
- [ ] Inventory every target plate/image before any bulk retrieval.
- [ ] Add a takedown/correction contact and source-provider change monitor.
- [ ] Reject sources whose terms prohibit the intended open POB distribution;
  keep them in the private consultation lane only.

## Dead Sea Scrolls priority queue

### Wave 1 — pipeline and comparison anchors

- [ ] 1QIsa-a — Great Isaiah Scroll.
- [ ] 1QS / 4Q255–264 — Community Rule witnesses.
- [ ] 1QM / related 4Q witnesses — War Scroll/War Rule.
- [ ] 1QpHab — Pesher Habakkuk.
- [ ] 1QH-a / 4QHodayot — Thanksgiving Hymns.
- [ ] 11Q19, 11Q20, 4Q524 — Temple Scroll witnesses.
- [ ] 4Q266–273 plus Cairo witnesses — Damascus Document.
- [ ] 1QapGen — Genesis Apocryphon (Aramaic).
- [ ] 4Q394–399 — Miqsat Ma'aseh ha-Torah (4QMMT).
- [ ] 4Q400–407, 11Q17, Mas1k — Songs of the Sabbath Sacrifice.

### Wave 2 — known works outside the Leningrad corpus

- [ ] 4Q201–212 — Aramaic 1 Enoch witnesses.
- [ ] 4Q216–224 and related fragments — Hebrew Jubilees witnesses.
- [ ] 4Q196–200 — Aramaic/Hebrew Tobit witnesses.
- [ ] 2Q18 and 11Q5 — Hebrew Sirach material.
- [ ] 7Q2 — Greek Letter of Jeremiah fragment.
- [ ] 11Q5 — Hebrew Psalm 151 / Psalms Scroll material.
- [ ] Aramaic Levi witnesses and later Genizah parallels.

### Wave 3 — biblical textual forms

- [ ] Isaiah witness family, beginning with 1QIsa-a and 1QIsa-b.
- [ ] Samuel witnesses, including major readings in 4QSam-a.
- [ ] Jeremiah witnesses representing shorter and longer textual forms.
- [ ] Deuteronomy witnesses with meaningful Septuagint/Samaritan/MT overlap.
- [ ] Psalms witnesses and non-Masoretic ordering/composition evidence.
- [ ] Daniel and the Twelve in Hebrew/Aramaic/Greek comparison.
- [ ] Genesis and Exodus sampling before full-book expansion.

## Other ancient witnesses worth comparing

- [ ] Samaritan Pentateuch: locate an open, independently verifiable Hebrew
  transcription and manuscript-image path.
- [ ] Nash Papyrus: inventory rights-safe images and freshly transcribe the
  Decalogue/Shema material.
- [ ] Ketef Hinnom: preserve epigraphic lineation and distinguish inscriptional
  reconstruction from Numbers 6 parallels.
- [ ] Masada: biblical scrolls and Ben Sira, subject to image rights.
- [ ] Wadi Murabba'at: biblical scrolls plus dated documentary Hebrew/Aramaic.
- [ ] Nahal Hever: Greek Minor Prophets plus Hebrew/Aramaic documentary corpus.
- [ ] Cairo Genizah: biblical manuscripts, Hebrew Ben Sira, and Aramaic Levi.
- [ ] Aleppo Codex and other Masoretic codices alongside the existing WLC/UHB.
- [ ] Targums: Onkelos, Jonathan, and selected Palestinian witnesses.
- [ ] Syriac Peshitta witnesses for Semitic cross-checking.
- [ ] Septuagint/Old Greek manuscripts and public-domain editions.
- [ ] Greek New Testament papyri and major codices for New Testament work.
- [ ] Latin, Coptic, Ge'ez, Armenian, Georgian, and other daughter versions only
  where they can preserve a lost earlier reading.

## Transcription and restoration

- [x] Produce deterministic grayscale/contrast derivatives for the four pilot
  images without adding or replacing strokes.
- [x] Document the initial OCR feasibility result: previews are insufficient
  for accepted independent transcription, and no guessed words were promoted.
- [ ] Run two blinded vision passes from different model families on each
  full-resolution pilot region.
  - [x] Prepare neutral-labeled, pixel-exact 1QM and 1QpHab master-image crops,
    shared prompt/schema, provider runner, and fail-closed comparison tests.
  - [x] Save a real GPT-5.6 Sol image-only structured proposal and its provenance;
    this is a single-model proposal, not two-model acceptance.
  - [x] Prepare `docs/CLAUDE_CODE_DSS_HANDOFF.md` for Zack's independent Claude
    session, with a blind input allowlist, exact hashes, and frozen deliverables.
  - [ ] Restore authorized Claude inference access; the service currently
    reports that the organization disabled Claude Code subscription access.
  - [ ] Complete both successful responses; pilot configuration is not proof
    that either model returned a transcription.
- [ ] Reconcile at glyph level and calculate exact character/token agreement.
- [ ] Promote exact visible-text agreement to `machine-consensus-accepted`.
- [ ] Promote matching supplied-text restorations to
  `machine-consensus-restored`, retaining brackets and both rationales.
- [ ] Keep disagreements as hypotheses until another independent model pass
  resolves them.
- [ ] Add multispectral channel support when licensed data is available.
- [ ] Add fragment-joint proposals as annotations, never destructive image edits.
- [ ] Add a benchmark set of independently attested control lines to measure
  the real error rate of the two-model rule while scaling automation.

## Collation, translation, and reader delivery

- [ ] Build the reference/fragment mapping layer.
- [ ] Emit machine-readable variant units and a human-readable apparatus.
- [ ] Add source-weight rationale instead of simple majority voting.
- [ ] Draft English only from machine-corroborated source units; keep novel
  Codex-only restorations out of the main text.
- [ ] Show alternate English renderings for materially uncertain variants.
- [ ] Preserve canonical/tradition labels for every composition.
- [ ] Add source-image regions to POB reader citations where redistribution is
  allowed.
- [ ] Add explicit “image unavailable” and “educational reconstruction” labels.
- [ ] Run blinded Codex reconciliation, cross-witness corroboration, schema
  validation, reader QA, and public revision review before any release.
- [ ] Create optional ImageGen reconstructions only after textual adjudication;
  watermark and exclude them from all OCR and translation inputs.
