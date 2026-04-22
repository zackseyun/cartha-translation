# Testaments of the Twelve Patriarchs source PDFs — manifest

Source scope: [`README.md`](README.md)

The local PDF scans are **not committed**. This file records the
expected files currently present in the workspace.

| Expected path | Edition | Year | Size (bytes) | SHA-256 | Role |
|---|---|---:|---:|---|---|
| `scans/charles_1908_greek_versions.pdf` | R. H. Charles, *The Greek Versions of the Testaments of the Twelve Patriarchs* | 1908 | 15,831,780 | `2309446584639013c6662d27a21a068439122d9a7b542ca2163f3822a2186a3d` | **Primary Greek drafting witness**; continuous Greek text with first Reuben OCR pilot now taken from pp. 66-79 |
| `scans/sinker_1879_testamenta_xii_patriarcharum.pdf` | Robert Sinker, *Testamenta XII patriarcharum* | 1879 | 4,123,483 | `6347ec554320801475023052eff672d458a7fb65b089dda54a90128bcd3120fe` | Appendix / collation witness only; useful for apparatus support, not the continuous drafting base text |
| `scans/charles_1908_testaments.pdf` | R. H. Charles, *The Testaments of the Twelve Patriarchs* | 1908 | 5,149,430 | `c1ec716dc0ae218452ecd26e658ef988fc9b6a7b538a677be0f6f32aa93b62f4` | English reference / structure aid |

## Verification

```bash
shasum -a 256 sources/testaments_twelve_patriarchs/scans/*.pdf
```
