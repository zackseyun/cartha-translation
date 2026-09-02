# SBLGNT edition-comparison apparatus

The unmodified upstream XML for all 27 New Testament books is pinned to
Faithlife/SBLGNT commit `c4d241a9c1c479a55b989ba35a4976c1d0b8052c`.
The publisher's license, README, and About files accompany it; hashes and source
URLs are in `manifest.json`.

**Attribution:** SBL Greek New Testament, edited by Michael W. Holmes.
Copyright 2010 Society of Biblical Literature and Logos Bible Software.
Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Source: [official publisher repository](https://github.com/Faithlife/SBLGNT).

These are differences between **edited Greek texts**, not a list of independent
manuscript attestations. WH, Treg, RP, NIV, NA27, NA28, and Holmes are editorial
labels; preserve the labels actually present in each entry. The upstream files
do not provide the complete ECM/UBS6 apparatus. Their older introduction and
current files do not necessarily have identical totals or labels.

This source is separate from POB's existing SBLGNT/MorphGNT base and its
morphological licensing. No canonical Greek or English text is replaced by the
import. Generated inventory records identify their transformation and retain
the original apparatus note verbatim under the same attribution.

```bash
python3 tools/textual_restoration/fetch_sblgnt_apparatus.py
python3 tools/textual_restoration/fetch_sblgnt_apparatus.py --verify-only
```

The [publisher's explanation](https://sblgnt.com/about/introduction/apparatus/)
describes the apparatus as a guide to further textual research. Agreement of
these editions is not proof of the original text; absence of an entry does not
prove absence of manuscript variation.
