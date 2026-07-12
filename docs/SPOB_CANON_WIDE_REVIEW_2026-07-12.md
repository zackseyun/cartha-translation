# SPOB canon-wide grounding review — July 12, 2026

## Outcome

The current POB source tree contains **43,105 records** across canonical,
deuterocanonical, and extra-canonical collections. The SPOB tree now contains a
matching **43,105 records**, and the full validator reports **43,105 valid, 0
failed**.

Azure GPT-5.6 Terra produced substantive grounding verdicts for 43,065 records:

| Verdict | Records |
| --- | ---: |
| Approve | 25,928 |
| Revise | 17,100 |
| Block | 37 |
| **Substantive total** | **43,065** |

Every one of the 17,137 substantive `revise` or `block` recommendations has a
matching applied review hash in the SPOB revision history. GPT-5.6 Sol performed
the revision pass, and each corrected record was schema-validated before its
atomic replacement.

## Azure content-policy adjudication

Terra declined to inspect 40 passages under Azure's content policy. These are
policy-filter outcomes, not negative translation judgments. The pipeline records
them as `azure_content_filter_editorial_block`, prevents them from being treated
as substantive Terra recommendations, and requires explicit editorial handling.

For this completion pass, each blocked record was compared directly with its POB
base, footnote markers, simplification metadata, and interpretive-expansion
metadata. No unsupported named-interpreter doctrine was found, all records passed
the normal SPOB validator, and the current text was preserved. This avoids asking
another model to invent a correction for a review that never occurred.

The 40 adjudicated references are:

1. 1 Samuel 11:2
2. 1 Samuel 17:46
3. 2 Esdras 15:33
4. 2 Maccabees 7:4
5. 2 Maccabees 14:46
6. 2 Maccabees 15:35
7. 3 Maccabees 2:28
8. 4 Maccabees 11:10
9. 4 Maccabees 15:15
10. Acts of Paul and Thecla — Chapter IX
11. Acts of Paul and Thecla — Chapter X
12. Deuteronomy 13:11
13. Deuteronomy 28:31
14. Genesis 40:19
15. Gospel of Judas — Jesus Reveals Everything to Judas
16. Gospel of Philip — Adam, Eve, and the Bridal Chamber
17. Gospel of Philip — Overcoming the World
18. Gospel of Philip — Uprooting Evil
19. Gospel of the Egyptians — The Three Descents of Seth
20. Jubilees 16:9
21. Jubilees 30:10
22. Jubilees 43:5
23. Jubilees 47:11
24. Judges 20:6
25. Judith 7:27
26. Mark 6:27
27. Martyrdom of Polycarp — MartPol. 16
28. Micah 3:3
29. Testament of Gad 1
30. Testament of Issachar 1
31. Testament of Issachar 2
32. Testament of Joseph 5:1
33. Testament of Judah 8
34. Testament of Zebulun 1:6
35. Testament of Zebulun 4
36. Tripartite Tractate — Different Opinions
37. Tripartite Tractate — More about the Calling
38. Tripartite Tractate — The Aeon of the Word
39. Tripartite Tractate — The Mistake of the Last Aeon, the Word
40. Wisdom of Solomon 12:5

## Named-interpreter safeguard

A precise corpus scan found no use of `William Branham`, `Branham`, `serpent
seed`, or `Message church` in SPOB text or `SPOB_DOCTRINE.md`. This report names
the terms only to record the negative audit. Named teachers may be recorded only
as attributed external witnesses under the rules in `SPOB_DOCTRINE.md`; they
never control the main text.

## Reproducible checks

```bash
python3 tools/simplified_pob_pipeline.py validate --only-existing
python3 tests/test_simplified_pob_pipeline.py
python3 tests/test_translation_divergence.py
rg -n -i 'william[[:space:]]+branham|branham|serpent[[:space:]-]+seed|message[[:space:]]+church' \
  translation_simplified SPOB_DOCTRINE.md
```

Translation-divergence reports remain review-priority indicators rather than
doctrinal votes. Their regeneration compares POB and SPOB wording with the
public-domain reference panel and does not publish copyrighted NKJV, NIV, or NLT
text.
