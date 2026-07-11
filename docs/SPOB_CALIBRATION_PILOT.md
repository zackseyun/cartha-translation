# SPOB calibration pilot

Generated: 2026-05-27 22:48 UTC

This pilot calibrates the Simplified People's Open Bible style before scaling to the full corpus.

> **2026-07-10 update:** The understanding-first doctrine and GPT-5.6
> Sol/Terra/Luna comparison are documented in
> [SPOB_GPT56_CALIBRATION.md](SPOB_GPT56_CALIBRATION.md). Sol is the calibrated
> primary drafter; Terra and Luna serve distinct review roles.

## Scope

- Records generated: **36**
- Sections covered:
  - Genesis 1:1-5
  - Ecclesiastes 1:1-5
  - Psalm 23 superscription + 23:1-6
  - Isaiah 53:1-5
  - John 1:1-5
  - Romans 3:21-25
  - Revelation 21:1-4

## Calibration questions

Review this pilot for:

1. Is the text easier than POB without becoming casual or childish?
2. Did SPOB keep the same source-grounded decisions POB made?
3. Did it preserve important footnotes and remove only unnecessary friction?
4. Are there places where SPOB should be bolder about simplifying the main sentence?
5. Are there places where it should stay closer to POB?

## Sample excerpts

### Genesis 1:1

`translation_simplified/ot/genesis/001/001.yaml`

> In the beginning, when God created the heavens and the earth[a]—

### John 1:1

`translation_simplified/nt/john/001/001.yaml`

> In the beginning was the Word[a], and the Word was with God[b], and the Word was God.

### Ecclesiastes 1:2

`translation_simplified/ot/ecclesiastes/001/002.yaml`

> Breath of breaths[a], says Qoheleth[b]; breath of breaths, all is mere breath.

### Psalms 23:1

`translation_simplified/ot/psalms/023/001.yaml`

> A psalm of David[a]. Yahweh[b] is my shepherd; I will not lack.

### Romans 3:23

`translation_simplified/nt/romans/003/023.yaml`

> For everyone has sinned and falls short of the glory of God[a][b].

### Isaiah 53:5

`translation_simplified/ot/isaiah/053/005.yaml`

> But he was pierced[a] because of our rebellion, he was crushed because of our sins. The punishment that brought us peace[b] was upon him, and by his wound[c] we are healed.

### Revelation 21:4

`translation_simplified/nt/revelation/021/004.yaml`

> He will wipe away every tear from their eyes. Death will be no more. There will be no more mourning, crying, or pain, for the former things have passed away.

## Validation

```bash
python3 tools/simplified_pob_pipeline.py validate --only-existing
# validated=36 failed=0
```
