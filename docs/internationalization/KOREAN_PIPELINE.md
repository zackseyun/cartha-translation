# Korean source-grounded POB pipeline

Korean ("translation_ko") is a source-grounded drafting track that mirrors the
Spanish pipeline (`SPANISH_PIPELINE.md`). It is **not** an English-to-Korean
localization. Each Korean record is drafted from the original Greek (SBLGNT) or
Hebrew (WLC/UHB, etc.) source, with the English POB rendering, lexical
decisions, theological decisions, footnotes, and revisions as **consult-only**
audit context. The English POB exists to expose translation policy already
adjudicated by the project; it does not override the Korean rendering when the
source warrants something different.

## North-star principle (binding)

> "Maintain what the author meant for the audience to understand, and represent
> true and powerful meaning. Render as close to the original scribe as
> possible."

When a traditional Korean ecclesial rendering would soften or domesticate the
source, prefer the source-direct rendering and explain the choice in
`lexical_decisions` / `theological_decisions`. This applies in particular to
divine names, titles, and bonded-status language (see Glossary).

## Output layout

```text
translation_ko/<testament>/<book>/<chapter>/<verse>.yaml
```

`<book>` slugs and chapter/verse zero-padding match the English tree exactly
(e.g. `translation_ko/nt/philippians/001/001.yaml` ↔
`translation/nt/philippians/001/001.yaml`).

## Language target

- **Code**: `ko`
- **Variant**: 표준어 (Standard Korean), modern.
- **Register**: 합쇼체 (formal-polite, contemporary). Modern but dignified —
  comparable to 새번역 / 우리말성경 register, not the archaic 하옵나이다 of
  개역개정. Direct addresses to God use 합쇼체 honorific verb endings
  (-십니다, -십시오); narrative voice uses plain 합쇼체 (-ㅂ니다 / -습니다).
- **Punctuation**: standard Korean punctuation. Use 「」 or "" for quoted
  speech; em-dashes ( — ) for parenthetical breaks; ellipsis as "…" not "...".
- **Names**: transliterate proper names per modern 외래어 표기법 unless an
  established biblical Korean form is overwhelmingly recognized
  (예: 바울, 베드로, 요한, 빌립보, 예루살렘). Document carve-outs in
  `lexical_decisions`.

## Glossary — project-level defaults

Defaults, not blind replacements. Always preserve context-sensitive nuance and
explain deviations.

| Source              | Default Korean   | Alternatives           | Notes |
|---------------------|------------------|------------------------|-------|
| יהוה / YHWH         | **야훼**         | 여호와 (traditional)   | Academic transliteration closer to the original tetragrammaton; avoid 주(主)/주님 as a masking convention. If the immediate source is Greek κύριος quoting or alluding to YHWH, note the call in `theological_decisions`. |
| Χριστός (titular)   | **메시아**       | 그리스도               | Mirrors EN POB "Messiah". Use 메시아 when functioning as a title (overwhelmingly the case in Paul); reserve 그리스도 only for fixed liturgical/name-form carve-outs that the EN record itself documents. |
| Χριστός (name-form) | 그리스도         | 메시아                 | Rare; only when EN POB already treats it as a fixed name. |
| δοῦλος / δοῦλη      | **종**           | 노예, 하인             | Default 종 carries the bonded-service nuance in modern Korean. Use **노예** specifically where EN POB chose "slave(s)" to flag bonded status (e.g. Philippians 1:1 per DOCTRINE.md §1) — note this in `lexical_decisions`. Avoid 하인 (mere domestic servant). |
| ἅγιοι (Pauline)     | **성도**         | 거룩한 자들            | "성도" is the natural Pauline address-formula equivalent in Korean. |
| ἀγάπη                | **사랑**         | (none)                 | Reserve 자비 for ἔλεος. |
| πνεῦμα (divine)     | **영** / **성령**| (none)                 | "성령" only where the source explicitly carries divine-Spirit force (πνεῦμα ἅγιον, or contextually unambiguous Pauline reference); otherwise "영". Do **not** capitalize-by-default in 1st-century Jewish-Christian texts (see DOCTRINE.md / north-star). |
| ἐκκλησία            | **회중** / **교회** | 교회는 첫 선택지가 아님 | Prefer **회중** ("assembly") when the source clearly means a gathered group of believers (Pauline usage). Use **교회** only where the EN POB explicitly chose "church" with institutional force. |
| ἐπίσκοπος           | **감독**         | 주교                   | Avoid 주교 (later ecclesial office). |
| διάκονος            | **집사**         | 봉사자, 일꾼           | In paired church-office contexts (e.g. Php 1:1), use 집사. Use 봉사자/일꾼 only where source clearly means generic service. |
| Θεός                | **하나님**       | 하느님 (Catholic)      | Default 하나님 (Protestant convention) for broad readability. Document if Catholic 하느님 is more faithful in a specific context. |
| κύριος (of Jesus)   | **주(主)** / **주님** | (none)            | Standard. |
| κύριος (= YHWH)     | **야훼**         | 주                     | When κύριος in NT clearly quotes/alludes to יהוה (e.g. LXX citations), render 야훼 and note in `theological_decisions`. |
| πίστις              | **믿음**         | 신실함                 | Use 신실함 only where the source clearly means "faithfulness" rather than "faith". |
| δικαιοσύνη          | **의**           | 정의                   | Default 의 in soteriological/Pauline contexts; 정의 only where the source clearly means social/forensic justice. |
| νόμος (Torah)       | **율법**         | 토라                   | 율법 is the established term; 토라 acceptable only in scholarly carve-out. |

For Hebrew OT specifics (e.g. אלהים, רוח, חסד, ברית), extend this table when
OT drafting begins.

## YAML record shape

Per-verse Korean records follow the same envelope as Spanish records. Required
top-level fields:

```yaml
id: PHP.1.1
reference: Philippians 1:1
language:
  code: ko
  name: Korean
  variant: 표준어 / modern formal-polite (합쇼체)
source:
  edition: SBLGNT          # copied verbatim from the EN record
  text: Παῦλος καὶ ...
base_translation:
  language: en
  yaml_path: translation/nt/philippians/001/001.yaml
  text: 'Paul and Timothy[a], slaves of Messiah Jesus, ...'
  footnotes: [ ... ]       # copied from EN; consult-only
translation:
  language: ko
  text: '바울과 디모데, ...'
  philosophy: optimal-equivalence
  footnotes:
    - marker: a
      text: 한국어 각주 ...
      reason: lexical_alternative | alternative_reading | textual_variant | ...
lexical_decisions:
  - source_word: δοῦλοι
    english_pob_choice: slaves
    chosen_korean: 노예
    alternatives_korean: [종, 하인]
    lexicon: BDAG
    rationale: '...'
theological_decisions:
  - issue: '...'
    chosen_reading: '...'
    alternative_readings: ['...']
    rationale: '...'
    doctrine_reference: 'DOCTRINE.md: ...'
ai_draft:
  model_id: claude-opus-4-7
  model_version: claude-opus-4-7-1m
  prompt_id: korean_source_grounded_draft_inline_v1
  timestamp: '2026-05-18T00:00:00Z'
source_grounding:
  english_pob_role: consult_only
```

`base_translation.footnotes` and `base_translation.ai_draft` may be omitted on
the Korean side if the corresponding EN record didn't populate them.

`status: draft` is implied for first-pass records; reviewers may add
`status: revised` later, parallel to the EN / ES flow.

## Drafting process (Phase 1 — inline via Claude Code session)

Phase 1 drafting runs through Claude Opus inside the Zack-owned Claude Code
session (no Azure cost; throughput bounded by Max-plan usage limits). Process:

1. Read the EN source YAML.
2. Apply the north-star principle + glossary defaults to produce Korean text.
3. Surface every lexical/theological decision where the Korean choice diverges
   from a default, deviates from the EN POB choice, or merits a footnote.
4. Write `translation_ko/<...>.yaml` conforming to the schema above.
5. Validate with `python3 -c 'import yaml; yaml.safe_load(open(p))'` (full
   schema validation will land with `tools/korean_pipeline.py` later).
6. Commit per book/chapter with no Claude trailer (repo policy).

## Drafting process (Phase 2 — Azure mini + review layer)

`tools/korean_pipeline.py` is the durable Azure path for finishing the remaining
New Testament coverage and adding a second-pass review layer. It builds
per-verse drafting/review briefs from the original source payload plus the
English POB audit trail, writes `translation_ko/...` YAML records, validates
footnote anchors, and records token usage.

Default Azure target:

- Resource: `cartha-aoai-truth-1c9177c8`
- Resource group: `rg-cartha-truth-openai`
- Deployment: `gpt-5-mini-atlas`
- Model label: `gpt-5-mini`

The script reads `AZURE_OPENAI_API_KEY` first. If not set, it can fetch a key
from the logged-in Azure CLI for the resource above; `CARTHA_KO_KEY_FILE` is
available as an explicit override.

Useful commands:

```bash
# Coverage/review status
python3 tools/korean_pipeline.py summary nt

# Validate existing Korean YAMLs without failing on the remaining missing scope
python3 tools/korean_pipeline.py validate nt --only-existing

# Draft a small pilot / continuation batch
python3 tools/korean_pipeline.py draft nt/john/001 --limit 5 --concurrency 2

# Review existing records and apply only low-risk model-proposed fixes
python3 tools/korean_pipeline.py review nt/jude --limit 5 --concurrency 2 --apply-revisions --keep-going
```

For broad scale-out, prefer chapter/book shards first (e.g. John 1-14, John
19-21, Luke 7-8, Luke 23-24, Matthew 17-21) and keep review running as a
separate lane. If Azure returns 429s, reduce review concurrency before reducing
draft throughput.

## Status reporting

After each batch:

```bash
python3 tools/build_status.py
git add status.json
git commit -m "status: regenerate snapshot"
git push
```

`status.json` walks `translation/` only today; once `translation_ko/` coverage
is meaningful, extend the script (or add a sibling `korean_status.json`) so
the public dashboard can render Korean coverage alongside English and Spanish.

## Commit style

- No `Co-Authored-By: Claude` trailer (repo-wide policy).
- Subjects: `ko: draft Philippians 1`, `ko: glossary update — δοῦλος`, etc.
- Revision-pass commits (later phases) start with `revise:` / `polish:` /
  `normalize:` so the dashboard filter works.
