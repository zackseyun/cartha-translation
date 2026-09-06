# Masoretic controls: a version-aware all-book coverage spine

Checked 2026-09-06. The executed [spine](../sources/textual_restoration/discovery/masoretic_codex_spine.v1.json)
connects all 39 POB OT books to three named codex targets and preserves the
24 Tanakh navigation groupings. It is not an all-Masoretic-manuscript census,
complete image inventory, verse-level collation or count of independent textual
branches. No source, English, note, registry or frozen prior experiment changes.

## What the new source checks establish

| Control | Actual source basis | What comparison must still establish |
|---|---|---|
| Leningrad | NLI's exact EVR I B 19a record, dated 1008–1009; NLR institutional index describes a complete codex | Page/verse/hand mapping and fidelity of each digital layer; complete codex does not mean every expected textual unit or vowel occurs |
| Aleppo | Project's loss list and separate parchment/photo/testimony categories | Source-specific gap endpoints, individual marks, old photographs and documentary evidence; unlisted gaps do not certify completeness |
| Sassoon 1053 | ANU Hebrew collection description and dated Sotheby's account | Passage-level losses and corrections; all 24 books represented does not allocate ~92% survival uniformly across books |

The [NLI record](https://www.nli.org.il/en/discover/manuscripts/hebrew-manuscripts/itempage?SearchTxt=Leningrad+codex&docId=PNX_MANUSCRIPTS990001516230205171&scope=PNX_MANUSCRIPTS&vid=MANUSCRIPTS)
identifies film representations separately; its PH2301 note concerns selected
Jeremiah/Isaiah pages. Those copies do not multiply the ancient witness. Its
upload date is not the manuscript's date. The
[NLR index](https://expositions.nlr.ru/eng/ex_manus/firkovich/sobr_prim.php)
uses 1008–1010 in its caption and 1010 in prose. That dating discrepancy is
retained, not settled by rounding or a new colophon reading.

The [Aleppo project](https://www.aleppocodex.org/links/9.html), sections 3.1–3.4,
reports an Exodus 8 scrap, a returned Chronicles leaf and old photographs of
Genesis 27 and the Deuteronomy Decalogue. The spine preserves those evidence
types even where the main body is missing. Testimony and reconstructed editions
remain separate. Its English page has editorial placeholders and source-specific
gap endpoints, so this is not a certified exact-word loss map. Chronicles must
not be placed after Ezra/Nehemiah and incorrectly lost merely because that is
POB's book order.

[ANU's Hebrew account](https://anumuseum.org.il/he/codex-sassoon/) reports 792
pages, about 12 wholly missing leaves and additional local losses. Its two
successive Masorah hands and later corrections require separate comparison
layers; dependence of a note on Aleppo does not prove dependence of every
biblical reading. The [2023 Sotheby's article](https://www.sothebys.com/en/articles/sassoon-codex-oldest-most-complete-hebrew-bible)
is a dated object description, not current custody authority or a replacement
for a passage/hand apparatus.

## Digital editions are not the manuscripts themselves

Actual headers were inspected across all 39 local WLC XML files and their
individual hashes are saved. The records retain their revision histories,
including the WLC 4.20 update and OSHB morphology release. The local UHB
manifest identifies version 2.1.32, issued 2026-04-12, with an OSHB 2.1.31 source
declaration. These are digital-edition metadata, not ancient witness dates.

The editor's [UXLC description](https://www.tanach.us/Pages/About.html) identifies
a distinct fork of WLC 4.20. Its [change log](https://www.tanach.us/Pages/Changes.html)
currently lists UXLC 2.5, 2026-04-01. A present-day tanach.us link in an older
header must not silently upgrade that local file to UXLC. The all-book comparison
should pin and collate the actual different releases, then investigate decisive
differences against codex evidence. A later release is neither a new manuscript
nor automatically the preferable critical reading.

Two source-reported exceptions expose why that distinction matters:

| Actual local probe | WLC word elements / vowel codepoints | Interpretation boundary |
|---|---:|---|
| Joshua 21:36 | 10 / 27 | Digital text exists although UXLC's editor reports the two-verse unit absent in LC |
| Joshua 21:37 | 10 / 28 | Same distinction; retaining it requires textual comparison, not false direct LC attestation |
| Numbers 7:13 | 20 / 56 | First-offering vocalized control |
| Numbers 7:19 | 22 / 59 | Repeated-offering lead: editor reports supplied vowels in repeated sections |

The canonical source fields also contain those vowel-codepoint totals. These
are direct measurements of stored encoding only. The physical omission and
supplied-vowel claims come from the editor's cited account; no fresh LC pixels
were inspected here. Neither exception warrants deleting verses, unpointing
the POB source or altering English without a separate case review. Existing
Joshua disclosure remains unchanged. A complete book can omit a textual unit;
an extant word can lack points present in its digital edition.

## Reproducibility, rights and next work

The [observation record](../sources/textual_restoration/discovery/masoretic_codex_sources.v1.json)
contains consulted URLs, section locators, limitations and conservative rules.
Its hash identifies our manually recorded observations, not the websites'
original responses. No full web-page snapshot or new manuscript pixels are
vendored. English ANU requests timed out; its Hebrew page succeeded. Aleppo's
reading link returned 404; NLI Aleppo and a linked USC route returned 403;
the Leningrad manifest returned cache miss. No access restrictions were bypassed.

The [builder](../tools/textual_restoration/build_masoretic_codex_spine.py) hashes
the observations, frozen QDR book-map receipt, 39 WLC files, UHB manifest and
four canonical probe files. It retains the QDR zero-hit books—1 Chronicles,
Nehemiah, Esther—without removing their Masoretic comparison targets. All rows
remain explicitly uncollated at verse/hand level.

```sh
.venv/bin/python tools/textual_restoration/build_masoretic_codex_spine.py
.venv/bin/python -m unittest tests.test_masoretic_codex_spine
```

Eight tests pass for current reproduction, 39/24 accounting, zero-hit retention,
loss/surrogate separation, order-independent Chronicles handling, no false
completeness, invalid assignment rejection and the actual encoding probes.
They verify those invariants, not scholarly truth. Next acquire the precise
surrogates and passage/hand maps, and compare pinned UXLC corrections against
images and POB. Other early codices, Genizah fragments, book apparatuses and
versional controls remain required; this three-codex spine does not close them.
