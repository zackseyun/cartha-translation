#!/usr/bin/env python3
"""korean_pipeline.py — source-grounded Korean POB drafting/review pipeline.

Like spanish_pipeline.py: drafts each Korean record from the original
Greek/Hebrew source with the English POB rendering as consult-only audit
context. Targets the current Azure OpenAI gpt-5-mini deployment on
cartha-aoai-truth-1c9177c8 (rg-cartha-truth-openai, eastus2).

Authoritative style + glossary lives in
docs/internationalization/KOREAN_PIPELINE.md. A condensed inline version is
embedded below as the system prompt so the model is fully briefed without
having to read the doc.

Output schema mirrors the existing translation_ko/ files written earlier in
the project (see translation_ko/nt/philippians/001/001.yaml for the canonical
example).
"""
from __future__ import annotations

import argparse
import copy
import concurrent.futures
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Iterable

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANSLATION_ROOT = REPO_ROOT / "translation"
KOREAN_ROOT = REPO_ROOT / "translation_ko"

DEFAULT_MODEL_ID = os.environ.get("CARTHA_KO_MODEL", "gpt-5-mini")
DEFAULT_AZURE_RESOURCE_GROUP = os.environ.get(
    "CARTHA_KO_AZURE_RESOURCE_GROUP", "rg-cartha-truth-openai"
)
DEFAULT_AZURE_ACCOUNT = os.environ.get(
    "CARTHA_KO_AZURE_ACCOUNT", "cartha-aoai-truth-1c9177c8"
)
DEFAULT_DEPLOYMENT = os.environ.get("CARTHA_KO_DEPLOYMENT", "gpt-5-mini-atlas")
DEFAULT_API_VERSION = os.environ.get(
    "AZURE_OPENAI_API_VERSION", "2025-04-01-preview"
)
DEFAULT_ENDPOINT = os.environ.get(
    "AZURE_OPENAI_ENDPOINT", "https://cartha-aoai-truth-1c9177c8.openai.azure.com"
)
DEFAULT_KEY_FILE = (
    pathlib.Path(os.environ["CARTHA_KO_KEY_FILE"])
    if os.environ.get("CARTHA_KO_KEY_FILE")
    else None
)
LEGACY_KEY_FILE = pathlib.Path("/tmp/aoai_key.txt")
DEFAULT_MAX_COMPLETION = 8000
DEFAULT_TIMEOUT = 180

PROMPT_ID = "korean_source_grounded_draft_azure_v1"
REVIEW_PROMPT_ID = "korean_source_review_azure_v1"

KOREAN_STYLE_AND_GLOSSARY = """
# Korean target style

Language target: Standard Korean (표준어), modern formal-polite (합쇼체) —
comparable to 새번역 / 우리말성경, not the archaic 하옵나이다 of 개역개정.
Narrative voice uses 합쇼체 (-ㅂ니다 / -습니다). Direct address to God uses
honorific verb endings (-십니다, -십시오). Inside quoted divine or
prophetic speech, register may shift (반말 to disciples, 합쇼체 to crowds,
imperative -옵소서 inside prayer formulas) — document any deliberate
register shift in `theological_decisions`.

Use standard Korean punctuation. 「」 or "" for quoted speech; em-dashes
( — ) for parenthetical breaks; ellipsis "…" not "...".

# North-star principle (binding)

"Maintain what the author meant for the audience to understand, and
represent true and powerful meaning. Render as close to the original
scribe as possible."

When a traditional Korean ecclesial rendering would soften or domesticate
the source, prefer the source-direct rendering and explain in
`lexical_decisions` / `theological_decisions`.

# Glossary — project defaults (defaults, not blind replacements)

| Source              | Default Korean           | Notes |
|---------------------|--------------------------|-------|
| יהוה / YHWH         | **야훼**                 | Academic transliteration, not 여호와. When NT κύριος cites/alludes to יהוה (LXX quotation), render 야훼 in main text + ot_citation footnote. |
| Χριστός (titular)   | **메시아**               | Mirror EN POB "Messiah". Reserve **그리스도** only for documented name-form carve-outs. |
| δοῦλος / δοῦλη      | **종** (default) / **노예** | Use **노예** specifically where the EN POB chose "slave(s)" to flag bonded status (Phil 1:1, Rom 6, Gal 4 Hagar allegory, Col 3:11, 1 Cor 7:23 etc.). |
| ἅγιοι (Pauline)     | **성도**                 | |
| ἀγάπη                | **사랑**                 | |
| πνεῦμα (divine)     | **영** / **성령**        | Use 성령 only where the source explicitly carries divine-Spirit force (πνεῦμα ἅγιον or contextually unambiguous Pauline reference); otherwise 영. Don't capitalize-by-default in 1st-century texts. |
| ἐκκλησία            | **회중** (gathered) / **교회** (institutional) | Case-by-case; document carve-outs. |
| ἐπίσκοπος           | **감독**                 | Not 주교. |
| διάκονος            | **집사** (office) / **일꾼** (general service) | Case-by-case. |
| Θεός                | **하나님**               | (Protestant convention.) |
| κύριος (of Jesus)   | **주(主)** / **주님**    | |
| πίστις              | **믿음**                 | Use 신실함 only where source clearly means "faithfulness". |
| δικαιοσύνη          | **의**                   | 정의 only for social/forensic justice senses. |
| νόμος (Torah)       | **율법**                 | Use **법/원리** when the source clearly means a different "law" (e.g. Rom 7:21, 8:2). |
| εὐαγγέλιον          | **복음**                 | |
| χάρις               | **은혜**                 | |
| εἰρήνη              | **평강**                 | |
| υἱὸς τοῦ ἀνθρώπου   | **인자**                 | |
| βασιλεία τοῦ θεοῦ / τῶν οὐρανῶν | **하나님의 나라 / 하늘 나라** | Matt uses 하늘 나라 (preserve). |
| παράκλητος (John 14-16, divine Spirit) | **보혜사** | Korean ecclesial tradition. |
| παράκλητος (1 Jn 2:1, of Jesus advocating) | **대언자** | Carve-out from 보혜사 (which is reserved for Spirit). |
| ἱλασμός / ἱλαστήριον | **화목제물** / **속죄소** | Render 1 Jn / Heb / Rom 3:25 distinctly per context. |

Proper nouns: transliterate per modern 외래어 표기법 unless an established
Korean biblical form is overwhelmingly recognized (예: 바울, 베드로, 요한,
빌립보, 예루살렘). Document carve-outs.

# Output discipline

Work from the original source evidence (`source.text`) first. Use the
English POB rendering, lexical/theological decisions, footnotes, and
revisions as audited context, not as the text to translate from
mechanically.

For every significant source-language choice, produce a Korean lexical
decision explaining the Korean rendering. Footnote markers in `korean_text`
must align with footnotes in the `footnotes` array (markers a, b, c, ...,
never reused). If no anchor belongs in the text for a footnote, don't
create that footnote.
""".strip()

DRAFT_SYSTEM_PROMPT = f"""You are producing a source-grounded Korean draft for the People's Open Bible.

The People's Open Bible (Cartha Open Bible) is transparent, CC-BY 4.0, and
translated directly from original-language sources (SBLGNT Greek, WLC/UHB
Hebrew, etc.) with auditable reasoning. Your task is not ordinary
localization. You draft one Korean verse using the original source text
plus the existing English POB audit trail.

You must call `submit_korean_draft` exactly once and output no other text.

Never:
- translate mechanically from English while ignoring the original source;
- paraphrase beyond what the source warrants;
- erase a documented lexical/theological tension;
- replace documented POB terminology with traditional church wording
  without a source-based rationale;
- invent lexicon entry numbers.

{KOREAN_STYLE_AND_GLOSSARY}
"""

DRAFT_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "submit_korean_draft",
        "description": "Submit a source-grounded Korean draft with auditable lexical/theological decisions.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "korean_text",
                "translation_philosophy",
                "lexical_decisions",
                "theological_decisions",
                "footnotes",
            ],
            "properties": {
                "korean_text": {"type": "string"},
                "translation_philosophy": {
                    "type": "string",
                    "enum": ["formal", "dynamic", "optimal-equivalence"],
                },
                "lexical_decisions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "source_word",
                            "english_pob_choice",
                            "chosen_korean",
                            "alternatives_korean",
                            "lexicon",
                            "rationale",
                        ],
                        "properties": {
                            "source_word": {"type": "string"},
                            "english_pob_choice": {"type": "string"},
                            "chosen_korean": {"type": "string"},
                            "alternatives_korean": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "lexicon": {"type": "string"},
                            "rationale": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                },
                "theological_decisions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "issue",
                            "chosen_reading",
                            "alternative_readings",
                            "rationale",
                            "doctrine_reference",
                        ],
                        "properties": {
                            "issue": {"type": "string"},
                            "chosen_reading": {"type": "string"},
                            "alternative_readings": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "rationale": {"type": "string"},
                            "doctrine_reference": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                },
                "footnotes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["marker", "text", "reason"],
                        "properties": {
                            "marker": {"type": "string"},
                            "text": {"type": "string"},
                            "reason": {
                                "type": "string",
                                "enum": [
                                    "alternative_reading",
                                    "lexical_alternative",
                                    "textual_variant",
                                    "cultural_note",
                                    "cross_reference",
                                    "theological_note",
                                    "source_note",
                                    "ot_citation",
                                    "previous_rendering",
                                    "korean_style_note",
                                ],
                            },
                        },
                        "additionalProperties": False,
                    },
                },
            },
            "additionalProperties": False,
        },
    },
}

REVIEW_SYSTEM_PROMPT = f"""You are an independent source-facing reviewer for the Korean People's Open Bible.

Read the original source evidence, the English POB audit trail, and the Korean
draft. Decide whether the Korean draft faithfully preserves the source meaning,
POB terminology, Korean readability, and documented lexical/theological
rationale.

You must call `submit_korean_review` exactly once and output no other text.

If a small repair is needed, provide a complete revised Korean text and complete
footnote array. Do not auto-domesticate source-sharp renderings merely because
traditional Korean Bible style would sound smoother.

{KOREAN_STYLE_AND_GLOSSARY}
"""

REVIEW_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "submit_korean_review",
        "description": "Review a Korean POB draft against source evidence and project terminology.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "verdict",
                "source_alignment_summary",
                "korean_quality_summary",
                "glossary_alignment",
                "issues",
                "revised_korean_text",
                "revised_footnotes",
                "revision_rationale",
                "requires_full_adjudication",
            ],
            "properties": {
                "verdict": {"type": "string", "enum": ["approve", "revise", "reject"]},
                "source_alignment_summary": {"type": "string"},
                "korean_quality_summary": {"type": "string"},
                "glossary_alignment": {"type": "string"},
                "issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["severity", "issue", "rationale"],
                        "properties": {
                            "severity": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                            "issue": {"type": "string"},
                            "rationale": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                },
                "revised_korean_text": {"type": "string"},
                "revised_footnotes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["marker", "text", "reason"],
                        "properties": {
                            "marker": {"type": "string"},
                            "text": {"type": "string"},
                            "reason": {
                                "type": "string",
                                "enum": [
                                    "alternative_reading",
                                    "lexical_alternative",
                                    "textual_variant",
                                    "cultural_note",
                                    "cross_reference",
                                    "theological_note",
                                    "source_note",
                                    "ot_citation",
                                    "previous_rendering",
                                    "korean_style_note",
                                ],
                            },
                        },
                        "additionalProperties": False,
                    },
                },
                "revision_rationale": {"type": "string"},
                "requires_full_adjudication": {"type": "boolean"},
            },
            "additionalProperties": False,
        },
    },
}


def rel(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def source_to_korean_path(source_path: pathlib.Path) -> pathlib.Path:
    return KOREAN_ROOT / source_path.relative_to(TRANSLATION_ROOT)


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def compact_yaml(obj: Any) -> str:
    return yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=1000).strip()


def prune_empty(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: v for k, v in ((k, prune_empty(v)) for k, v in obj.items()) if v not in (None, "", [], {})}
    if isinstance(obj, list):
        return [prune_empty(v) for v in obj]
    return obj


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_user_prompt(source_path: pathlib.Path, record: dict[str, Any]) -> str:
    translation = record.get("translation") or {}
    context = {
        "source_yaml_path": rel(source_path),
        "id": record.get("id"),
        "reference": record.get("reference"),
        "source_payload": record.get("source") or {},
        "english_pob_translation": {
            "text": translation.get("text"),
            "footnotes": translation.get("footnotes") or [],
            "philosophy": translation.get("philosophy"),
        },
        "english_lexical_decisions": record.get("lexical_decisions") or [],
        "english_theological_decisions": record.get("theological_decisions") or [],
        "applied_revisions": (record.get("revisions") or [])[-3:],
        "latest_revision_pass": record.get("revision_pass") or {},
    }
    return f"""# Korean source-grounded draft task

Draft a Korean POB record for this one verse.

## Full source + English audit context

{compact_yaml(prune_empty(context))}

## Task

Return exactly one `submit_korean_draft` function call.

The main `korean_text` should be publication-readable modern formal-polite
Korean (합쇼체). Lexical and theological decisions should explain Korean
choices from the original source, using the English POB audit trail as
context.
""".strip()


def build_review_user_prompt(
    source_path: pathlib.Path,
    en_record: dict[str, Any],
    korean_record: dict[str, Any],
) -> str:
    translation = korean_record.get("translation") or {}
    context = {
        "source_yaml_path": rel(source_path),
        "korean_yaml_path": rel(source_to_korean_path(source_path)),
        "id": en_record.get("id"),
        "reference": en_record.get("reference"),
        "source_payload": en_record.get("source") or {},
        "english_pob_translation": en_record.get("translation") or {},
        "english_lexical_decisions": en_record.get("lexical_decisions") or [],
        "english_theological_decisions": en_record.get("theological_decisions") or [],
        "english_applied_revisions": en_record.get("revisions") or [],
        "korean_draft": {
            "text": translation.get("text"),
            "footnotes": translation.get("footnotes") or [],
            "lexical_decisions": korean_record.get("lexical_decisions") or [],
            "theological_decisions": korean_record.get("theological_decisions") or [],
            "status": korean_record.get("status"),
        },
    }
    return f"""# Korean source-grounded review task

Review this Korean draft against the source and the English POB audit trail.

{compact_yaml(prune_empty(context))}

## Task

Return exactly one `submit_korean_review` function call. If the text needs a
small repair, set verdict `revise` and provide `revised_korean_text` plus a
complete `revised_footnotes` array whose markers exactly match the revised text.
If you approve without changes, set `revised_korean_text` and
`revision_rationale` to empty strings and `revised_footnotes` to an empty array.
Set `requires_full_adjudication` true only when the issue is genuinely hard,
doctrinally sensitive, source-uncertain, or too risky for automatic application.
""".strip()


def fetch_azure_key_from_cli() -> str | None:
    """Fetch an Azure OpenAI key from the logged-in Azure CLI, if available."""
    try:
        raw = subprocess.check_output(
            [
                "az",
                "cognitiveservices",
                "account",
                "keys",
                "list",
                "--resource-group",
                DEFAULT_AZURE_RESOURCE_GROUP,
                "--name",
                DEFAULT_AZURE_ACCOUNT,
                "-o",
                "json",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        keys = json.loads(raw)
        key = str(keys.get("key1") or keys.get("key2") or "").strip()
        if key:
            os.environ["AZURE_OPENAI_API_KEY"] = key
            return key
    except Exception:
        return None
    return None


def fetch_azure_key() -> str:
    if "AZURE_OPENAI_API_KEY" in os.environ and os.environ["AZURE_OPENAI_API_KEY"].strip():
        return os.environ["AZURE_OPENAI_API_KEY"].strip()
    if DEFAULT_KEY_FILE and DEFAULT_KEY_FILE.exists():
        return DEFAULT_KEY_FILE.read_text(encoding="utf-8").strip()
    cli_key = fetch_azure_key_from_cli()
    if cli_key:
        return cli_key
    if LEGACY_KEY_FILE.exists():
        return LEGACY_KEY_FILE.read_text(encoding="utf-8").strip()
    raise RuntimeError(
        "Azure OpenAI key not found. Set AZURE_OPENAI_API_KEY, set "
        "CARTHA_KO_KEY_FILE, or log in with Azure CLI for "
        f"{DEFAULT_AZURE_ACCOUNT}."
    )


def call_azure(
    *,
    system_prompt: str,
    user_prompt: str,
    deployment: str,
    tool: dict[str, Any] = DRAFT_TOOL,
    tool_name: str = "submit_korean_draft",
    api_version: str = DEFAULT_API_VERSION,
    endpoint: str = DEFAULT_ENDPOINT,
    max_completion_tokens: int = DEFAULT_MAX_COMPLETION,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = 2,
) -> tuple[dict[str, Any], dict[str, Any]]:
    api_key = fetch_azure_key()
    endpoint = endpoint.rstrip("/")
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    payload: dict[str, Any] = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_completion_tokens": max_completion_tokens,
        "parallel_tool_calls": False,
        "tool_choice": {"type": "function", "function": {"name": tool_name}},
        "tools": [tool],
    }
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            data=encoded,
            headers={"Content-Type": "application/json", "api-key": api_key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            choices = body.get("choices") or []
            if not choices:
                raise RuntimeError(f"Azure response had no choices: {body}")
            message = choices[0].get("message") or {}
            tool_calls = message.get("tool_calls") or []
            if len(tool_calls) != 1:
                raise RuntimeError(f"Expected 1 tool call, got {len(tool_calls)}: {body}")
            fn = tool_calls[0].get("function") or {}
            if fn.get("name") != tool_name:
                raise RuntimeError(f"Unexpected tool name: {fn.get('name')}")
            arguments = json.loads(fn.get("arguments") or "{}")
            usage = body.get("usage") or {}
            return arguments, usage
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {exc.code} from Azure: {body[:500]}")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
            last_error = exc
        time.sleep(2 ** attempt)
    raise last_error if last_error else RuntimeError("Azure call failed without specific error")


def normalize_usage(usage: dict[str, Any]) -> dict[str, Any]:
    details = usage.get("completion_tokens_details") or {}
    return {
        "prompt_tokens": int(usage.get("prompt_tokens") or 0),
        "completion_tokens": int(usage.get("completion_tokens") or 0),
        "total_tokens": int(usage.get("total_tokens") or 0),
        "reasoning_tokens": int(details.get("reasoning_tokens") or 0),
    }


def build_record(
    *,
    source_path: pathlib.Path,
    en_record: dict[str, Any],
    draft: dict[str, Any],
    model_id: str,
    deployment: str,
    usage: dict[str, Any],
) -> dict[str, Any]:
    en_translation = en_record.get("translation") or {}
    base_translation: dict[str, Any] = {
        "language": "en",
        "yaml_path": rel(source_path),
        "text": en_translation.get("text"),
    }
    if en_translation.get("footnotes"):
        base_translation["footnotes"] = en_translation["footnotes"]

    translation_block: dict[str, Any] = {
        "language": "ko",
        "text": draft["korean_text"],
        "philosophy": draft.get("translation_philosophy") or "optimal-equivalence",
    }
    if draft.get("footnotes"):
        translation_block["footnotes"] = draft["footnotes"]

    record: dict[str, Any] = {
        "id": en_record.get("id"),
        "reference": en_record.get("reference"),
        "language": {
            "code": "ko",
            "name": "Korean",
            "variant": "표준어 / modern formal-polite (합쇼체)",
        },
        "source": en_record.get("source") or {},
        "base_translation": base_translation,
        "translation": translation_block,
    }
    if draft.get("lexical_decisions"):
        record["lexical_decisions"] = draft["lexical_decisions"]
    if draft.get("theological_decisions"):
        record["theological_decisions"] = draft["theological_decisions"]
    record["ai_draft"] = {
        "model_id": model_id,
        "azure_deployment": deployment,
        "prompt_id": PROMPT_ID,
        "timestamp": utc_now(),
        "usage": normalize_usage(usage),
    }
    record["source_grounding"] = {"english_pob_role": "consult_only"}
    record["status"] = "draft"
    return record


def write_korean_yaml(target_path: pathlib.Path, record: dict[str, Any]) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )


def validate_korean_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["record is not a YAML object"]
    if (data.get("language") or {}).get("code") != "ko":
        errors.append("language.code is not ko")
    translation = data.get("translation") or {}
    text = str(translation.get("text") or "").strip()
    if translation.get("language") != "ko":
        errors.append("translation.language is not ko")
    if not text:
        errors.append("translation.text missing")
    footnotes = translation.get("footnotes") or []
    if not isinstance(footnotes, list):
        errors.append("translation.footnotes is not a list")
        footnotes = []
    markers = [str(note.get("marker") or "") for note in footnotes if isinstance(note, dict)]
    if len(markers) != len(set(markers)):
        errors.append("duplicate footnote markers")
    for marker in markers:
        if marker and f"[{marker}]" not in text:
            errors.append(f"footnote marker [{marker}] not present in translation text")
    if "Messiah Jesus" in text or "Jesus Christ" in text:
        errors.append("possible untranslated English residue in Korean text")
    return errors


def validate_korean_record(path: pathlib.Path) -> list[str]:
    try:
        data = load_yaml(path)
    except Exception as exc:  # noqa: BLE001
        return [f"{type(exc).__name__}: {exc}"]
    return validate_korean_data(data)


def iter_missing(source_paths: Iterable[pathlib.Path], overwrite: bool) -> list[pathlib.Path]:
    out = []
    for sp in source_paths:
        tp = source_to_korean_path(sp)
        if overwrite or not tp.exists():
            out.append(sp)
    return out


def expand_scope(scope: str) -> list[pathlib.Path]:
    """Expand a `book` or `book/chap` or explicit path into source EN yaml paths.

    Examples:
      'nt/john'           -> all chapters of John
      'nt/john/001'       -> just John 1
      'translation/nt/john/001/001.yaml' -> single verse
    """
    s = scope.strip()
    # Normalize: strip leading "translation/" so all scopes are relative to TRANSLATION_ROOT.
    if s.startswith("translation/"):
        s = s[len("translation/"):]
    if s.endswith(".yaml") or s.endswith(".yml"):
        candidate = TRANSLATION_ROOT / s
        if not candidate.exists():
            raise SystemExit(f"Scope file not found: {candidate}")
        return [candidate]
    candidate = TRANSLATION_ROOT / s
    if not candidate.exists():
        raise SystemExit(f"Scope path not found: {candidate}")
    return sorted(candidate.rglob("*.yaml"))


def draft_one(
    source_path: pathlib.Path,
    *,
    deployment: str,
    model_id: str,
    overwrite: bool,
    max_completion: int,
    validation_retries: int,
) -> tuple[str, str]:
    target_path = source_to_korean_path(source_path)
    if target_path.exists() and not overwrite:
        return ("skip", rel(target_path))
    try:
        en_record = load_yaml(source_path)
        if not en_record.get("source", {}).get("text"):
            return ("error", f"{rel(source_path)} missing source.text")
        user_prompt = build_user_prompt(source_path, en_record)
        validation_note = ""
        last_errors: list[str] = []
        for attempt in range(validation_retries + 1):
            draft, usage = call_azure(
                system_prompt=DRAFT_SYSTEM_PROMPT,
                user_prompt=user_prompt + validation_note,
                deployment=deployment,
                max_completion_tokens=max_completion,
            )
            record = build_record(
                source_path=source_path,
                en_record=en_record,
                draft=draft,
                model_id=model_id,
                deployment=deployment,
                usage=usage,
            )
            write_korean_yaml(target_path, record)
            errors = validate_korean_record(target_path)
            if not errors:
                return ("ok", rel(target_path))
            last_errors = errors
            invalid_path = target_path.with_suffix(
                target_path.suffix + f".invalid-{int(time.time())}-{attempt}"
            )
            target_path.replace(invalid_path)
            validation_note = (
                "\n\n# Previous output failed validation\n"
                f"Errors: {errors}\n"
                "Return a corrected function call. Footnotes are allowed only "
                "when every marker appears exactly in korean_text, e.g. [a]. "
                "Use unique markers and include no unanchored footnotes.\n"
            )
        return ("error", f"{rel(source_path)} validation failed after retries: {last_errors}")
    except Exception as exc:  # noqa: BLE001
        return ("error", f"{rel(source_path)}: {exc}")


def cmd_draft(args: argparse.Namespace) -> int:
    sources = []
    for scope in args.scope:
        sources.extend(expand_scope(scope))
    if not args.overwrite:
        sources = iter_missing(sources, overwrite=False)
    if args.limit:
        sources = sources[: args.limit]
    if not sources:
        print("[ko-draft] nothing to do — all targets already have Korean files.")
        return 0
    print(
        f"[ko-draft] {len(sources)} verses to draft via {args.deployment} "
        f"(concurrency={args.concurrency}, overwrite={args.overwrite})"
    )
    # Resolve credentials once before worker threads start so they do not all
    # race the Azure CLI key lookup.
    fetch_azure_key()
    start = time.time()
    ok = err = skip = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {
            ex.submit(
                draft_one,
                sp,
                deployment=args.deployment,
                model_id=args.model_id,
                overwrite=args.overwrite,
                max_completion=args.max_completion,
                validation_retries=args.validation_retries,
            ): sp
            for sp in sources
        }
        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            status, msg = fut.result()
            if status == "ok":
                ok += 1
            elif status == "skip":
                skip += 1
            else:
                err += 1
                print(f"  ERR [{i}/{len(sources)}] {msg}")
            if i % 10 == 0 or i == len(sources):
                elapsed = time.time() - start
                rate = i / max(elapsed, 1e-6)
                eta = (len(sources) - i) / max(rate, 1e-6)
                print(
                    f"  progress: {i}/{len(sources)} ok={ok} err={err} skip={skip} "
                    f"({rate:.2f} v/s, eta {eta/60:.1f}m)"
                )
    elapsed = time.time() - start
    print(f"[ko-draft] done in {elapsed/60:.1f}m. ok={ok} err={err} skip={skip}")
    return 0 if err == 0 else 1


def cmd_validate(args: argparse.Namespace) -> int:
    sources = []
    for scope in args.scope:
        sources.extend(expand_scope(scope))
    if args.limit:
        sources = sources[: args.limit]
    ok = bad = missing = 0
    for sp in sources:
        tp = source_to_korean_path(sp)
        if not tp.exists():
            missing += 1
            if not args.only_existing:
                print(f"  MISSING {rel(tp)}")
            continue
        errors = validate_korean_record(tp)
        if errors:
            bad += 1
            print(f"  BAD {rel(tp)}: {errors}")
        else:
            ok += 1
    print(f"[ko-validate] ok={ok} bad={bad} missing={missing} (of {len(sources)})")
    return 0 if bad == 0 and (args.only_existing or missing == 0) else 1


def review_one(
    source_path: pathlib.Path,
    *,
    deployment: str,
    model_id: str,
    apply_revisions: bool,
    force: bool,
    max_completion: int,
) -> tuple[str, str]:
    target_path = source_to_korean_path(source_path)
    if not target_path.exists():
        return ("skip", rel(target_path))
    try:
        en_record = load_yaml(source_path)
        korean_record = load_yaml(target_path)
        if korean_record.get("review_pass") and not force:
            return ("skip", rel(target_path))
        user_prompt = build_review_user_prompt(source_path, en_record, korean_record)
        review, usage = call_azure(
            system_prompt=REVIEW_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            deployment=deployment,
            tool=REVIEW_TOOL,
            tool_name="submit_korean_review",
            max_completion_tokens=max_completion,
        )
        translation = korean_record.setdefault("translation", {})
        old_text = str(translation.get("text") or "").strip()
        old_footnotes = list(translation.get("footnotes") or [])
        revised = str(review.get("revised_korean_text") or "").strip()
        revised_footnotes = (
            review.get("revised_footnotes")
            if isinstance(review.get("revised_footnotes"), list)
            else old_footnotes
        )

        apply_revision = (
            apply_revisions
            and review.get("verdict") == "revise"
            and revised
            and revised != old_text
            and not bool(review.get("requires_full_adjudication"))
        )
        auto_apply_blocked_errors: list[str] = []
        if apply_revision:
            candidate = copy.deepcopy(korean_record)
            candidate_translation = candidate.setdefault("translation", {})
            candidate_translation["text"] = revised
            if revised_footnotes:
                candidate_translation["footnotes"] = revised_footnotes
            else:
                candidate_translation.pop("footnotes", None)
            auto_apply_blocked_errors = validate_korean_data(candidate)
            if auto_apply_blocked_errors:
                apply_revision = False

        if apply_revision:
            korean_record.setdefault("revisions", []).append(
                {
                    "from": old_text,
                    "to": revised,
                    "rationale": review.get("revision_rationale")
                    or review.get("source_alignment_summary"),
                    "reviewer_model": model_id,
                    "timestamp": utc_now(),
                }
            )
            translation["text"] = revised
            if revised_footnotes:
                translation["footnotes"] = revised_footnotes
            else:
                translation.pop("footnotes", None)
            korean_record["status"] = "korean_reviewed"
        elif review.get("verdict") == "approve":
            korean_record["status"] = "korean_reviewed"
        else:
            korean_record["status"] = (
                "korean_needs_adjudication"
                if review.get("requires_full_adjudication")
                else "korean_needs_revision"
            )

        korean_record["review_pass"] = prune_empty(
            {
                **review,
                "model_id": model_id,
                "azure_deployment": deployment,
                "prompt_id": REVIEW_PROMPT_ID,
                "timestamp": utc_now(),
                "usage": normalize_usage(usage),
                "applied_revision": apply_revision,
                "auto_apply_blocked_errors": auto_apply_blocked_errors,
            }
        )
        write_korean_yaml(target_path, korean_record)
        return ("ok", f"{rel(target_path)} verdict={review.get('verdict')}")
    except Exception as exc:  # noqa: BLE001
        return ("error", f"{rel(source_path)}: {exc}")


def cmd_review(args: argparse.Namespace) -> int:
    sources = []
    for scope in args.scope:
        sources.extend(expand_scope(scope))
    if args.limit:
        sources = sources[: args.limit]
    if not sources:
        print("[ko-review] nothing to review.")
        return 0
    print(
        f"[ko-review] reviewing up to {len(sources)} verses via {args.deployment} "
        f"(concurrency={args.concurrency}, apply_revisions={args.apply_revisions}, force={args.force})"
    )
    fetch_azure_key()
    ok = err = skip = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {
            ex.submit(
                review_one,
                sp,
                deployment=args.deployment,
                model_id=args.model_id,
                apply_revisions=args.apply_revisions,
                force=args.force,
                max_completion=args.max_completion,
            ): sp
            for sp in sources
        }
        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            status, msg = fut.result()
            if status == "ok":
                ok += 1
                print(f"  OK [{i}/{len(sources)}] {msg}")
            elif status == "skip":
                skip += 1
            else:
                err += 1
                print(f"  ERR [{i}/{len(sources)}] {msg}")
                if not args.keep_going:
                    break
    print(f"[ko-review] done. ok={ok} err={err} skip={skip}")
    return 0 if err == 0 else 1


def cmd_summary(args: argparse.Namespace) -> int:
    sources = []
    for scope in args.scope:
        sources.extend(expand_scope(scope))
    existing = reviewed = pending_review = 0
    status_counts: dict[str, int] = {}
    usage = {
        "draft_prompt_tokens": 0,
        "draft_completion_tokens": 0,
        "review_prompt_tokens": 0,
        "review_completion_tokens": 0,
    }
    by_book: dict[str, dict[str, int]] = {}
    for sp in sources:
        parts = sp.relative_to(TRANSLATION_ROOT).parts
        book = f"{parts[0]}/{parts[1]}" if len(parts) >= 2 else rel(sp)
        by_book.setdefault(book, {"expected": 0, "existing": 0, "reviewed": 0})
        by_book[book]["expected"] += 1
        tp = source_to_korean_path(sp)
        if not tp.exists():
            continue
        existing += 1
        by_book[book]["existing"] += 1
        record = load_yaml(tp)
        status = str(record.get("status") or "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        draft_usage = (record.get("ai_draft") or {}).get("usage") or {}
        usage["draft_prompt_tokens"] += int(draft_usage.get("prompt_tokens") or 0)
        usage["draft_completion_tokens"] += int(draft_usage.get("completion_tokens") or 0)
        review_usage = (record.get("review_pass") or {}).get("usage") or {}
        if record.get("review_pass"):
            reviewed += 1
            by_book[book]["reviewed"] += 1
        usage["review_prompt_tokens"] += int(review_usage.get("prompt_tokens") or 0)
        usage["review_completion_tokens"] += int(review_usage.get("completion_tokens") or 0)
    pending_review = existing - reviewed
    payload = {
        "expected_records": len(sources),
        "korean_files": existing,
        "pending_draft": len(sources) - existing,
        "reviewed": reviewed,
        "pending_review": pending_review,
        "status_counts": status_counts,
        "usage": usage,
        "by_book": by_book,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Korean POB drafting via Azure GPT-5 mini")
    sub = p.add_subparsers(dest="cmd", required=True)

    pd = sub.add_parser("draft", help="Draft missing Korean YAMLs for the given scope")
    pd.add_argument("scope", nargs="+", help="Book / chapter / verse path (e.g. nt/john)")
    pd.add_argument("--deployment", default=DEFAULT_DEPLOYMENT)
    pd.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    pd.add_argument("--concurrency", type=int, default=6)
    pd.add_argument("--limit", type=int, default=0, help="0 = no limit")
    pd.add_argument("--overwrite", action="store_true")
    pd.add_argument("--max-completion", type=int, default=DEFAULT_MAX_COMPLETION)
    pd.add_argument("--validation-retries", type=int, default=1)
    pd.set_defaults(func=cmd_draft)

    pr = sub.add_parser("review", help="Review existing Korean YAMLs and optionally apply small revisions")
    pr.add_argument("scope", nargs="+", help="Book / chapter / verse path (e.g. nt/john)")
    pr.add_argument("--deployment", default=DEFAULT_DEPLOYMENT)
    pr.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    pr.add_argument("--concurrency", type=int, default=2)
    pr.add_argument("--limit", type=int, default=1, help="0 = no limit")
    pr.add_argument("--force", action="store_true")
    pr.add_argument("--apply-revisions", action="store_true")
    pr.add_argument("--keep-going", action="store_true")
    pr.add_argument("--max-completion", type=int, default=DEFAULT_MAX_COMPLETION)
    pr.set_defaults(func=cmd_review)

    pv = sub.add_parser("validate", help="Validate Korean YAMLs in scope vs EN tree")
    pv.add_argument("scope", nargs="+")
    pv.add_argument("--limit", type=int, default=0, help="0 = no limit")
    pv.add_argument("--only-existing", action="store_true")
    pv.set_defaults(func=cmd_validate)

    ps = sub.add_parser("summary", help="Summarize Korean coverage/review state")
    ps.add_argument("scope", nargs="+")
    ps.set_defaults(func=cmd_summary)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
