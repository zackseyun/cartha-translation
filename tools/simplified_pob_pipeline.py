#!/usr/bin/env python3
"""simplified_pob_pipeline.py — draft the Simplified People's Open Bible (SPOB).

SPOB is an English derivative of the People's Open Bible for modern common
readers. It is not a replacement source translation: each record is simplified
from the audited English POB text while using the original source payload,
lexical decisions, theological decisions, footnotes, revision history, and
cross-check summaries as guardrails.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANSLATION_ROOT = REPO_ROOT / "translation"
SIMPLIFIED_ROOT = REPO_ROOT / "translation_simplified"
STATUS_PATH = REPO_ROOT / "status.json"

DEFAULT_DRAFT_MODEL_ID = os.environ.get("CARTHA_SIMPLIFIED_DRAFT_MODEL", "gpt-5-mini")
DEFAULT_DRAFT_DEPLOYMENT = os.environ.get(
    "AZURE_OPENAI_MINI_DEPLOYMENT_ID",
    os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID", "gpt-5-mini-atlas"),
)
DEFAULT_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
DEFAULT_TEMPERATURE = 1.0
DEFAULT_TIMEOUT_SECONDS = 240
DEFAULT_BACKEND = os.environ.get("CARTHA_SIMPLIFIED_BACKEND", "auto")
DEFAULT_GEMINI_MODEL = os.environ.get("CARTHA_SIMPLIFIED_GEMINI_MODEL", "gemini-3.5-flash")
DEFAULT_VERTEX_MODEL = os.environ.get("CARTHA_SIMPLIFIED_VERTEX_MODEL", "gemini-3.5-flash")
DEFAULT_VERTEX_LOCATION = os.environ.get("CARTHA_SIMPLIFIED_VERTEX_LOCATION", "global")

MODEL_PRICES_USD_PER_MTOK = {
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50, "cached_input": 0.075},
    "gpt-5.4": {"input": 2.50, "output": 15.00, "cached_input": 0.25},
}

SPOB_STYLE_GUIDE = """
# Simplified POB target style

Audience: a modern, common English reader who may be new to biblical language.
Use clear, natural English. Prefer short sentences when the POB sentence is hard
to follow. Keep the gravity of Scripture; do not make it casual, cute, or vague.
This is a readability translation, not a conservative copyedit. If the draft
mostly preserves POB's wording and sentence structure, it has failed.

Relationship to POB:
- POB is the controlling base text and audit trail.
- The original source payload, lexical decisions, theological decisions,
  footnotes, revisions, and cross-check summaries are guardrails.
- Compression is allowed, but only when it does not erase the central meaning,
  a documented ambiguity, or a theologically important source-language pressure.
- Preserve the main POB decision even when simplifying the wording.
- Prefer explaining difficult terms through clearer wording, but retain a term
  when replacing it would hide a key biblical concept.

Default simplification rules:
- Replace academic or archaic phrasing with common wording.
- Replace opaque historical, legal, ritual, currency, measure, and idiomatic
  terms with understandable modern wording in the main text. Keep the original
  term only in a footnote or retained-term note when needed for auditability.
- Break dense clauses into simpler sentences when helpful.
- Recast awkward participles and literal clause order into ordinary English
  when that makes the same meaning easier to understand.
- Keep names, divine names, and major theological titles stable unless POB's own
  rationale permits a clearer equivalent.
- Keep footnotes only when they help a normal reader understand an important
  alternate reading, textual issue, cross-reference, or translation choice.
- Do not harmonize, doctrinally smooth, or over-resolve tension that POB keeps.

Understanding-first interpretation:
- Target maximum warranted understanding, not maximum verbal similarity.
- You may express contextual meaning more directly than POB when source, immediate
  context, and POB reasoning strongly support it.
- Use a bounded clarifier such as "spiritually" when it prevents a likely modern
  misunderstanding and the context clearly supplies that domain.
- Preserve distinct source ideas. Do not merge two meaningful commands or images
  into one generalized paraphrase.
- Record every meaning made more explicit in `interpretive_expansions`, including
  evidence, confidence, alternatives preserved, and any external witnesses.
- Historical or modern teachers (including William Branham), denominations, and
  traditions may be treated only as interpretive witnesses. They never control the
  main text. A teacher-specific conclusion belongs outside the translation unless
  source, context, and POB reasoning independently establish it.

Examples of the kind of main-text simplification expected:
- "quadrans" -> "smallest coin" / "last small coin"
- "alms" -> "charity" / "help for the poor"
- "having come under confinement" -> "when he is put in prison/custody"
- "examined concerning the things he did" -> "questioned about what he did"
- "not having need" -> "when he does not need help"
- 1 Peter 5:8 "Be clear-minded; stay alert" -> "Keep a clear mind and stay
  spiritually awake" (preserve both commands; make the spiritual-attack context
  explicit rather than replacing both ideas with a vague paraphrase)
""".strip()

DRAFT_SYSTEM_PROMPT = f"""You are drafting the Simplified People's Open Bible (SPOB).

SPOB is an English derivative of the People's Open Bible for modern common
readers. Your task is to simplify one POB verse/section while preserving the POB
meaning and its audited reasoning layers.

The output should read like a real plain-language edition. Do not merely polish
POB with a few synonym swaps. Actively rewrite difficult wording into a clearer
representation a normal reader can understand on the first read.

You must call `submit_simplified_draft` exactly once and output no other text.

Keep the audit compact. Use no more than three simplification decisions, two
interpretive expansions, and two risk flags. Each rationale and evidence item
should be one short, non-repetitive sentence.

Never:
- ignore the POB lexical/theological decisions;
- flatten a documented ambiguity into a confident claim;
- remove the force of a source-language image unless you preserve it another way;
- turn translation into devotional commentary;
- invent source evidence or lexicon claims;
- make the text sound childish or slangy.

{SPOB_STYLE_GUIDE}
"""

DRAFT_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "submit_simplified_draft",
        "description": "Submit a plain-language English derivative draft with traceable simplification choices.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "simplified_text",
                "translation_philosophy",
                "footnotes",
                "simplification_decisions",
                "interpretive_expansions",
                "risk_flags",
            ],
            "properties": {
                "simplified_text": {"type": "string"},
                "translation_philosophy": {"type": "string", "enum": ["formal", "dynamic", "optimal-equivalence"]},
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
                                    "source_note",
                                    "simplification_note",
                                ],
                            },
                        },
                        "additionalProperties": False,
                    },
                },
                "simplification_decisions": {
                    "type": "array",
                    "maxItems": 3,
                    "items": {
                        "type": "object",
                        "required": ["pob_phrase", "simplified_phrase", "preserved_meaning", "reasoning_layer_used", "rationale"],
                        "properties": {
                            "pob_phrase": {"type": "string"},
                            "simplified_phrase": {"type": "string"},
                            "preserved_meaning": {"type": "string"},
                            "reasoning_layer_used": {"type": "string"},
                            "rationale": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                },
                "interpretive_expansions": {
                    "type": "array",
                    "maxItems": 2,
                    "description": "Meanings stated more explicitly than POB. Use an empty array when none are added.",
                    "items": {
                        "type": "object",
                        "required": [
                            "pob_phrase",
                            "rendering",
                            "claim",
                            "evidence",
                            "confidence",
                            "alternatives_preserved",
                            "external_witnesses",
                        ],
                        "properties": {
                            "pob_phrase": {"type": "string"},
                            "rendering": {"type": "string"},
                            "claim": {"type": "string"},
                            "evidence": {"type": "array", "maxItems": 3, "items": {"type": "string"}},
                            "confidence": {"type": "string", "enum": ["high", "moderate", "low"]},
                            "alternatives_preserved": {"type": "array", "maxItems": 3, "items": {"type": "string"}},
                            "external_witnesses": {"type": "array", "maxItems": 3, "items": {"type": "string"}},
                        },
                        "additionalProperties": False,
                    },
                },
                "risk_flags": {
                    "type": "array",
                    "maxItems": 2,
                    "items": {
                        "type": "object",
                        "required": ["risk", "mitigation"],
                        "properties": {
                            "risk": {"type": "string"},
                            "mitigation": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                },
            },
            "additionalProperties": False,
        },
    },
}


@dataclass(frozen=True)
class SourceRecord:
    source_path: pathlib.Path
    target_path: pathlib.Path
    testament: str
    book: str
    slug: str
    index: int


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def current_git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    except Exception:
        return ""


def prune_empty(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: prune_empty(v) for k, v in value.items() if v not in (None, "", [], {})}
    if isinstance(value, list):
        return [prune_empty(v) for v in value if v not in (None, "", [], {})]
    return value


def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def safe_load_yaml(path: pathlib.Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML object")
    return data


def write_yaml_atomic(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), delete=False) as tmp:
        tmp.write(rendered)
        tmp_path = pathlib.Path(tmp.name)
    tmp_path.replace(path)


def acquire_lock(path: pathlib.Path, worker_id: str) -> pathlib.Path | None:
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return None
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps({"worker_id": worker_id, "locked_at": utc_now()}) + "\n")
    return lock_path


def release_lock(lock_path: pathlib.Path | None) -> None:
    if lock_path and lock_path.exists():
        lock_path.unlink()


def choose_source_files(book_dir: pathlib.Path) -> list[pathlib.Path]:
    if book_dir.name == "testaments_twelve_patriarchs":
        return sorted(book_dir.rglob("*.yaml"))
    nested = sorted(book_dir.glob("*/*.yaml"))
    if nested:
        return nested
    return sorted(book_dir.glob("*.yaml"))


def iter_status_records(*, book_filter: set[str] | None = None, testament_filter: set[str] | None = None) -> list[SourceRecord]:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    records: list[SourceRecord] = []
    idx = 0
    for book in status.get("books", []):
        testament = str(book.get("testament"))
        slug = str(book.get("slug"))
        name = str(book.get("book"))
        normalized_name = name.lower().replace(" ", "_").replace("-", "_")
        if book_filter and slug not in book_filter and normalized_name not in book_filter:
            continue
        if testament_filter and testament not in testament_filter:
            continue
        book_dir = TRANSLATION_ROOT / testament / slug
        for source_path in choose_source_files(book_dir):
            idx += 1
            target_path = SIMPLIFIED_ROOT / source_path.relative_to(TRANSLATION_ROOT)
            records.append(SourceRecord(source_path, target_path, testament, name, slug, idx))
    return records


def compact_yaml(obj: Any) -> str:
    return yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=1000).strip()


def parse_json_object(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S).strip()
    start = text.find("{")
    if start > 0:
        text = text[start:]
    decoder = json.JSONDecoder()
    parsed, _ = decoder.raw_decode(text)
    if not isinstance(parsed, dict):
        raise RuntimeError("JSON response was not an object")
    return parsed


def summarize_cross_check(cross_check: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(cross_check, dict):
        return {}
    keep = {
        "status": cross_check.get("status"),
        "verdict": cross_check.get("verdict"),
        "agreement": cross_check.get("agreement"),
        "agreement_score": cross_check.get("agreement_score"),
        "reviewer_model": cross_check.get("reviewer_model"),
        "pass_count": cross_check.get("pass_count"),
        "passes_with_issues": cross_check.get("passes_with_issues"),
        "verdict_counts": cross_check.get("verdict_counts"),
    }
    return prune_empty(keep)


def build_draft_user_prompt(source_path: pathlib.Path, record: dict[str, Any]) -> str:
    translation = record.get("translation") or {}
    context = {
        "source_yaml_path": rel(source_path),
        "id": record.get("id"),
        "reference": record.get("reference"),
        "source_payload": record.get("source") or {},
        "pob_translation": {
            "text": translation.get("text"),
            "footnotes": translation.get("footnotes") or [],
            "philosophy": translation.get("philosophy"),
        },
        "pob_lexical_decisions": record.get("lexical_decisions") or [],
        "pob_theological_decisions": record.get("theological_decisions") or [],
        "applied_revisions": record.get("revisions") or [],
        "latest_revision_pass": record.get("revision_pass") or {},
        "cross_check_summary": summarize_cross_check(record.get("cross_check") or {}),
    }
    return f"""# SPOB simplification task

Simplify this People's Open Bible record for a modern common English reader.

## Full POB source + reasoning context

{compact_yaml(context)}

## Task

Return exactly one `submit_simplified_draft` function call.

The main `simplified_text` should be clear, publication-readable English. Keep
POB's source-driven choice as the controlling meaning. Explain the major
simplification choices in `simplification_decisions` so a reviewer can see what
was compressed and what reasoning layer protected the meaning.
""".strip()


def fetch_azure_env() -> None:
    if os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_ENDPOINT"):
        return
    try:
        raw = subprocess.check_output(
            [
                "aws",
                "secretsmanager",
                "get-secret-value",
                "--secret-id",
                "cartha-azure-openai-key",
                "--region",
                "us-west-2",
                "--query",
                "SecretString",
                "--output",
                "text",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        try:
            account = os.environ.get("AZURE_OPENAI_ACCOUNT", "cartha-aoai-truth-1c9177c8")
            resource_group = os.environ.get("AZURE_OPENAI_RESOURCE_GROUP", "rg-cartha-truth-openai")
            key = subprocess.check_output(
                [
                    "az",
                    "cognitiveservices",
                    "account",
                    "keys",
                    "list",
                    "--resource-group",
                    resource_group,
                    "--name",
                    account,
                    "--query",
                    "key1",
                    "--output",
                    "tsv",
                ],
                text=True,
            ).strip()
            endpoint = subprocess.check_output(
                [
                    "az",
                    "cognitiveservices",
                    "account",
                    "show",
                    "--resource-group",
                    resource_group,
                    "--name",
                    account,
                    "--query",
                    "properties.endpoint",
                    "--output",
                    "tsv",
                ],
                text=True,
            ).strip()
        except Exception as az_exc:
            raise RuntimeError(
                "AZURE_OPENAI_API_KEY/AZURE_OPENAI_ENDPOINT are not set; AWS secret is deleted/unavailable and Azure CLI key fetch failed"
            ) from az_exc
        os.environ["AZURE_OPENAI_API_KEY"] = key
        os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint
        os.environ.setdefault("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)
        return
    secret = json.loads(raw)
    os.environ["AZURE_OPENAI_API_KEY"] = secret["api_key"]
    os.environ["AZURE_OPENAI_ENDPOINT"] = secret.get("endpoint") or "https://eastus2.api.cognitive.microsoft.com"
    os.environ.setdefault("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)


def model_prices(model_id: str) -> dict[str, float]:
    normalized = model_id.lower()
    if "gemini" in normalized:
        # Gemini pricing is not kept here yet; keep usage tokens but avoid fake
        # cost precision until we add a current price table.
        return {"input": 0.0, "output": 0.0, "cached_input": 0.0}
    if "gpt-5.6" in normalized:
        # Do not attribute GPT-5.4 prices to the GPT-5.6 variants. Add official
        # Azure prices here once they are published for this subscription/region.
        return {"input": 0.0, "output": 0.0, "cached_input": 0.0}
    if "mini" in normalized:
        return MODEL_PRICES_USD_PER_MTOK["gpt-5.4-mini"]
    return MODEL_PRICES_USD_PER_MTOK["gpt-5.4"]


def usage_cost_usd(usage: dict[str, Any], model_id: str) -> float:
    prices = model_prices(model_id)
    prompt = int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
    completion = int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
    return (prompt / 1_000_000 * prices["input"]) + (completion / 1_000_000 * prices["output"])


def normalize_usage(usage: dict[str, Any], model_id: str) -> dict[str, Any]:
    usage = dict(usage or {})
    details = usage.get("completion_tokens_details") or {}
    return {
        "prompt_tokens": int(usage.get("prompt_tokens") or 0),
        "completion_tokens": int(usage.get("completion_tokens") or 0),
        "total_tokens": int(usage.get("total_tokens") or 0),
        "reasoning_tokens": int(details.get("reasoning_tokens") or 0),
        "estimated_cost_usd": round(usage_cost_usd(usage, model_id), 6),
    }


def call_azure_tool(
    *,
    system_prompt: str,
    user_prompt: str,
    tool: dict[str, Any],
    tool_name: str,
    deployment: str,
    model_id: str,
    max_completion_tokens: int,
    temperature: float = DEFAULT_TEMPERATURE,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    retries: int = 2,
) -> tuple[dict[str, Any], str, dict[str, Any], str]:
    fetch_azure_env()
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)
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
    if temperature != 1.0:
        payload["temperature"] = temperature

    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        retry_after_seconds = 0.0
        req = urllib.request.Request(
            url,
            data=encoded,
            headers={"Content-Type": "application/json", "api-key": api_key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
            choices = body.get("choices") or []
            if not choices:
                raise RuntimeError(f"Azure response had no choices: {body}")
            message = choices[0].get("message") or {}
            tool_calls = message.get("tool_calls") or []
            if len(tool_calls) != 1:
                raise RuntimeError(f"Expected exactly one tool call; got {len(tool_calls)}: {body}")
            fn = (tool_calls[0].get("function") or {})
            if fn.get("name") != tool_name:
                raise RuntimeError(f"Expected tool {tool_name}; got {fn.get('name')}")
            raw_args = fn.get("arguments") or "{}"
            parsed = json.loads(raw_args)
            if not isinstance(parsed, dict):
                raise RuntimeError("Tool arguments were not an object")
            return prune_empty(parsed), str(body.get("model") or model_id), body.get("usage") or {}, raw_args
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {exc.code}: {detail[:1200]}")
            if exc.code == 429:
                try:
                    retry_after_seconds = float(exc.headers.get("Retry-After") or 0)
                except (TypeError, ValueError):
                    retry_after_seconds = 0.0
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        if attempt < retries:
            # Azure commonly applies a one-minute rolling window. A short fixed
            # retry loop only repeats the same 429, so honor Retry-After when it
            # is present and otherwise back off far enough for that window.
            fallback_delay = 2 + attempt * 5
            if "HTTP 429" in str(last_error):
                fallback_delay = max(fallback_delay, 20 * (attempt + 1))
            time.sleep(max(fallback_delay, retry_after_seconds))
    assert last_error is not None
    raise last_error


def fetch_gemini_api_key() -> str:
    if os.environ.get("GOOGLE_API_KEY"):
        return str(os.environ["GOOGLE_API_KEY"])
    try:
        raw = subprocess.check_output(
            [
                "aws",
                "secretsmanager",
                "get-secret-value",
                "--secret-id",
                "/cartha/openclaw/gemini_api_key",
                "--region",
                "us-west-2",
                "--query",
                "SecretString",
                "--output",
                "text",
            ],
            text=True,
        ).strip()
    except Exception as exc:
        raise RuntimeError("GOOGLE_API_KEY is not set and Gemini secret fetch failed") from exc
    try:
        payload = json.loads(raw)
        if payload.get("api_key"):
            return str(payload["api_key"])
        keys = payload.get("api_keys")
        if isinstance(keys, list) and keys:
            return str(keys[0])
    except Exception:
        pass
    if raw:
        return raw
    raise RuntimeError("Gemini secret was empty")


def call_gemini_json(
    *,
    system_prompt: str,
    user_prompt: str,
    model_id: str,
    temperature: float = DEFAULT_TEMPERATURE,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    retries: int = 2,
) -> tuple[dict[str, Any], str, dict[str, Any], str]:
    api_key = fetch_gemini_api_key()
    model_path = model_id if model_id.startswith("models/") else f"models/{model_id}"
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={api_key}"
    json_prompt = (
        f"{system_prompt}\n\n---\n\n{user_prompt}\n\n"
        "Return only a JSON object matching this schema shape. Do not wrap in Markdown. "
        "The JSON object keys must be: simplified_text, translation_philosophy, footnotes, "
        "simplification_decisions, retained_terms, source_alignment_notes, readability_notes, "
        "compression_notes, risk_flags."
    )
    payload: dict[str, Any] = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": json_prompt}],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            data=encoded,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
            candidates = body.get("candidates") or []
            if not candidates:
                raise RuntimeError(f"Gemini response had no candidates: {body}")
            parts = ((candidates[0].get("content") or {}).get("parts") or [])
            raw_text = "".join(str(part.get("text") or "") for part in parts).strip()
            parsed = parse_json_object(raw_text)
            usage_meta = body.get("usageMetadata") or {}
            usage = {
                "prompt_tokens": int(usage_meta.get("promptTokenCount") or 0),
                "completion_tokens": int(usage_meta.get("candidatesTokenCount") or 0),
                "total_tokens": int(usage_meta.get("totalTokenCount") or 0),
            }
            return prune_empty(parsed), model_path.replace("models/", ""), usage, raw_text
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {exc.code}: {detail[:1200]}")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        if attempt < retries:
            time.sleep(2 + attempt * 5)
    assert last_error is not None
    raise last_error


def fetch_vertex_oauth() -> tuple[str, str]:
    """Return (access_token, project_id) for Vertex Gemini via stored refresh-token credentials."""
    if os.environ.get("VERTEX_ACCESS_TOKEN") and os.environ.get("VERTEX_PROJECT_ID"):
        return os.environ["VERTEX_ACCESS_TOKEN"], os.environ["VERTEX_PROJECT_ID"]
    try:
        raw = subprocess.check_output(
            [
                "aws",
                "secretsmanager",
                "get-secret-value",
                "--secret-id",
                "/cartha/verification/gemini_credentials",
                "--region",
                "us-west-2",
                "--query",
                "SecretString",
                "--output",
                "text",
            ],
            text=True,
        ).strip()
        creds = json.loads(raw)
        encoded = urllib.parse.urlencode(
            {
                "client_id": creds["client_id"],
                "client_secret": creds["client_secret"],
                "refresh_token": creds["refresh_token"],
                "grant_type": "refresh_token",
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            "https://oauth2.googleapis.com/token",
            data=encoded,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            token_payload = json.loads(response.read().decode("utf-8"))
        return str(token_payload["access_token"]), str(creds.get("quota_project_id") or creds.get("project_id"))
    except Exception as exc:
        raise RuntimeError("Vertex OAuth credential fetch failed") from exc


def call_vertex_json(
    *,
    system_prompt: str,
    user_prompt: str,
    model_id: str,
    location: str,
    temperature: float = DEFAULT_TEMPERATURE,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    retries: int = 2,
) -> tuple[dict[str, Any], str, dict[str, Any], str]:
    token, project = fetch_vertex_oauth()
    model_path = model_id if model_id.startswith("publishers/") else f"publishers/google/models/{model_id}"
    if location == "global":
        url = f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/{model_path}:generateContent"
    else:
        url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/{model_path}:generateContent"
    json_prompt = (
        f"{system_prompt}\n\n---\n\n{user_prompt}\n\n"
        "Return only a JSON object matching this schema shape. Do not wrap in Markdown. "
        "The JSON object keys must be: simplified_text, translation_philosophy, footnotes, "
        "simplification_decisions, retained_terms, source_alignment_notes, readability_notes, "
        "compression_notes, risk_flags."
    )
    payload: dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": json_prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            data=encoded,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "x-goog-user-project": project,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
            candidates = body.get("candidates") or []
            if not candidates:
                raise RuntimeError(f"Vertex response had no candidates: {body}")
            parts = ((candidates[0].get("content") or {}).get("parts") or [])
            raw_text = "".join(str(part.get("text") or "") for part in parts).strip()
            parsed = parse_json_object(raw_text)
            usage_meta = body.get("usageMetadata") or {}
            usage = {
                "prompt_tokens": int(usage_meta.get("promptTokenCount") or 0),
                "completion_tokens": int(usage_meta.get("candidatesTokenCount") or 0),
                "total_tokens": int(usage_meta.get("totalTokenCount") or 0),
            }
            return prune_empty(parsed), model_id, usage, raw_text
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {exc.code}: {detail[:1200]}")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        if attempt < retries:
            time.sleep(2 + attempt * 5)
    assert last_error is not None
    raise last_error


def build_simplified_record(
    *,
    source_path: pathlib.Path,
    pob_record: dict[str, Any],
    tool_input: dict[str, Any],
    model_id: str,
    model_version: str,
    prompt_id: str,
    prompt_sha: str,
    raw_output_hash: str,
    usage: dict[str, Any],
    deployment: str,
) -> dict[str, Any]:
    footnotes = normalize_footnotes(tool_input.get("footnotes") or [])
    simplification_decisions = normalize_simplification_decisions(
        tool_input.get("simplification_decisions") or []
    )
    interpretive_expansions = normalize_interpretive_expansions(
        tool_input.get("interpretive_expansions") or []
    )
    retained_terms = normalize_retained_terms(tool_input.get("retained_terms") or [])
    translation_block: dict[str, Any] = {
        "language": "en",
        "text": str(tool_input["simplified_text"]).strip(),
        "philosophy": normalize_philosophy(tool_input.get("translation_philosophy")),
    }
    if footnotes:
        translation_block["footnotes"] = footnotes
    pob_translation = pob_record.get("translation") or {}
    record = {
        "id": pob_record.get("id"),
        "reference": pob_record.get("reference"),
        "language": {
            "code": "en",
            "name": "English",
            "variant": "simplified modern common English",
        },
        "source": pob_record.get("source") or {},
        "base_translation": {
            "language": "en",
            "edition": "POB",
            "yaml_path": rel(source_path),
            "text": pob_translation.get("text"),
            "footnotes": pob_translation.get("footnotes") or [],
            "ai_draft": pob_record.get("ai_draft") or {},
            "revision_pass": pob_record.get("revision_pass") or {},
        },
        "translation": translation_block,
        "simplification_decisions": simplification_decisions,
        "interpretive_expansions": interpretive_expansions,
        "retained_terms": retained_terms,
        "translation_notes": {
            "source_alignment_notes": tool_input.get("source_alignment_notes"),
            "readability_notes": normalize_string_list(tool_input.get("readability_notes") or []),
            "compression_notes": normalize_string_list(tool_input.get("compression_notes") or []),
            "risk_flags": normalize_risk_flags(tool_input.get("risk_flags") or []),
        },
        "source_grounding": {
            "pob_role": "primary_derivative_base",
            "source_payload_role": "audit_guardrail",
            "pob_path": rel(source_path),
            "source_text_sha256": sha256_text(compact_yaml(pob_record.get("source") or {})),
            "pob_commit_sha": current_git_sha(),
        },
        "ai_draft": {
            "model_id": model_id,
            "model_version": model_version,
            "azure_deployment": deployment,
            "prompt_id": prompt_id,
            "prompt_sha256": prompt_sha,
            "timestamp": utc_now(),
            "output_hash": raw_output_hash,
            "usage": normalize_usage(usage, model_id),
        },
        "status": "simplified_draft",
    }
    return prune_empty(record)


def normalize_footnotes(raw: list[Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        marker = str(item.get("marker") or "").strip().strip("[]")
        text = str(item.get("text") or "").strip()
        if not marker or not text:
            continue
        out.append(
            {
                "marker": marker,
                "text": text,
                "reason": str(item.get("reason") or "simplification_note").strip(),
            }
        )
    return out


def normalize_philosophy(raw: Any) -> str:
    value = str(raw or "").strip()
    allowed = {"formal", "dynamic", "optimal-equivalence"}
    return value if value in allowed else "optimal-equivalence"


def normalize_string_list(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item or "").strip()]
    text = str(raw or "").strip()
    return [text] if text else []


def normalize_risk_flags(raw: Any) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    items = raw if isinstance(raw, list) else ([raw] if raw else [])
    for item in items:
        if isinstance(item, dict):
            risk = str(item.get("risk") or item.get("issue") or item.get("flag") or "").strip()
            mitigation = str(item.get("mitigation") or item.get("rationale") or "Flag retained for reviewer attention.").strip()
        else:
            risk = str(item or "").strip()
            mitigation = "Flag retained for reviewer attention."
        if risk:
            out.append({"risk": risk, "mitigation": mitigation})
    return out


def normalize_simplification_decisions(raw: list[Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in raw:
        if isinstance(item, dict):
            rationale = str(item.get("rationale") or item.get("preserved_meaning") or "").strip()
            out.append(
                {
                    "pob_phrase": str(item.get("pob_phrase") or "").strip(),
                    "simplified_phrase": str(item.get("simplified_phrase") or "").strip(),
                    "preserved_meaning": str(item.get("preserved_meaning") or rationale).strip(),
                    "reasoning_layer_used": str(item.get("reasoning_layer_used") or "POB audit trail").strip(),
                    "rationale": rationale,
                }
            )
        elif isinstance(item, str) and item.strip():
            text = item.strip()
            out.append(
                {
                    "pob_phrase": "",
                    "simplified_phrase": "",
                    "preserved_meaning": text,
                    "reasoning_layer_used": "POB audit trail",
                    "rationale": text,
                }
            )
    return prune_empty(out)


def normalize_retained_terms(raw: list[Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in raw:
        if isinstance(item, dict):
            term = str(item.get("term") or "").strip()
            reason = str(item.get("reason") or "Retained to preserve POB's source-grounded terminology.").strip()
        else:
            term = str(item or "").strip()
            reason = "Retained to preserve POB's source-grounded terminology."
        if term:
            out.append({"term": term, "reason": reason})
    return out


def normalize_interpretive_expansions(raw: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    items = raw if isinstance(raw, list) else []
    for item in items:
        if not isinstance(item, dict):
            continue
        claim = str(item.get("claim") or "").strip()
        rendering = str(item.get("rendering") or "").strip()
        if not claim or not rendering:
            continue
        confidence = str(item.get("confidence") or "moderate").strip().lower()
        if confidence not in {"high", "moderate", "low"}:
            confidence = "moderate"
        out.append(
            {
                "pob_phrase": str(item.get("pob_phrase") or "").strip(),
                "rendering": rendering,
                "claim": claim,
                "evidence": normalize_string_list(item.get("evidence") or []),
                "confidence": confidence,
                "alternatives_preserved": normalize_string_list(item.get("alternatives_preserved") or []),
                "external_witnesses": normalize_string_list(item.get("external_witnesses") or []),
            }
        )
    return prune_empty(out)


def validate_simplified_record(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    try:
        record = safe_load_yaml(path)
    except Exception as exc:
        return [f"{type(exc).__name__}: {exc}"]
    text = str(((record.get("translation") or {}).get("text") or "")).strip()
    base_text = str(((record.get("base_translation") or {}).get("text") or "")).strip()
    if not text:
        errors.append("translation.text missing")
    if ((record.get("translation") or {}).get("philosophy")) not in {"formal", "dynamic", "optimal-equivalence"}:
        errors.append("translation.philosophy invalid")
    if (record.get("language") or {}).get("code") != "en":
        errors.append("language.code is not en")
    if not base_text:
        errors.append("base_translation.text missing")
    if not isinstance(record.get("simplification_decisions"), list):
        errors.append("simplification_decisions missing/non-list")
    elif len(text.split()) >= 5 and not record.get("simplification_decisions"):
        errors.append("simplification_decisions empty for non-trivial text")
    expansions = record.get("interpretive_expansions")
    if expansions is not None and not isinstance(expansions, list):
        errors.append("interpretive_expansions non-list")
    for index, expansion in enumerate(expansions or []):
        if not isinstance(expansion, dict):
            errors.append(f"interpretive_expansions[{index}] non-object")
            continue
        if not expansion.get("evidence"):
            errors.append(f"interpretive_expansions[{index}] evidence missing")
        if expansion.get("confidence") == "low":
            errors.append(f"interpretive_expansions[{index}] low-confidence expansion cannot enter main text")
    footnotes = ((record.get("translation") or {}).get("footnotes") or [])
    markers = [str(note.get("marker") or "").strip().strip("[]") for note in footnotes if isinstance(note, dict)]
    if len(markers) != len(set(markers)):
        errors.append("duplicate footnote markers")
    for marker in markers:
        if marker and f"[{marker}]" not in text:
            errors.append(f"footnote marker [{marker}] not present in translation text")
    if not (record.get("ai_draft") or {}).get("prompt_sha256"):
        errors.append("ai_draft.prompt_sha256 missing")
    return errors


def draft_one(src: SourceRecord, *, args: argparse.Namespace) -> bool:
    if src.target_path.exists() and not args.force:
        return False
    lock = acquire_lock(src.target_path, args.worker_id)
    if lock is None:
        return False
    try:
        pob_record = safe_load_yaml(src.source_path)
        user_prompt = build_draft_user_prompt(src.source_path, pob_record)
        if args.dry_run_prompt:
            print(user_prompt)
            return True
        validation_note = ""
        last_errors: list[str] = []
        for validation_attempt in range(args.validation_retries + 1):
            attempt_prompt = user_prompt + validation_note
            attempt_prompt_sha = sha256_text(DRAFT_SYSTEM_PROMPT + "\n\n---\n\n" + attempt_prompt)
            backend = args.backend
            if backend == "gemini":
                tool_input, model_version, usage, raw_args = call_gemini_json(
                    system_prompt=DRAFT_SYSTEM_PROMPT,
                    user_prompt=attempt_prompt,
                    model_id=args.gemini_model,
                    temperature=args.temperature,
                    timeout_seconds=args.timeout_seconds,
                    retries=args.retries,
                )
                model_id = args.gemini_model
                deployment = "gemini-api"
            elif backend == "vertex":
                tool_input, model_version, usage, raw_args = call_vertex_json(
                    system_prompt=DRAFT_SYSTEM_PROMPT,
                    user_prompt=attempt_prompt,
                    model_id=args.vertex_model,
                    location=args.vertex_location,
                    temperature=args.temperature,
                    timeout_seconds=args.timeout_seconds,
                    retries=args.retries,
                )
                model_id = args.vertex_model
                deployment = f"vertex:{args.vertex_location}"
            else:
                try:
                    tool_input, model_version, usage, raw_args = call_azure_tool(
                        system_prompt=DRAFT_SYSTEM_PROMPT,
                        user_prompt=attempt_prompt,
                        tool=DRAFT_TOOL,
                        tool_name="submit_simplified_draft",
                        deployment=args.deployment,
                        model_id=args.model,
                        max_completion_tokens=args.max_completion_tokens,
                        temperature=args.temperature,
                        timeout_seconds=args.timeout_seconds,
                        retries=args.retries,
                    )
                    model_id = args.model
                    deployment = args.deployment
                except Exception as azure_exc:
                    if backend == "azure":
                        raise
                    print(f"[simplified] Azure unavailable; falling back to Vertex ({type(azure_exc).__name__}: {azure_exc})", file=sys.stderr)
                    tool_input, model_version, usage, raw_args = call_vertex_json(
                        system_prompt=DRAFT_SYSTEM_PROMPT,
                        user_prompt=attempt_prompt,
                        model_id=args.vertex_model,
                        location=args.vertex_location,
                        temperature=args.temperature,
                        timeout_seconds=args.timeout_seconds,
                        retries=args.retries,
                    )
                    model_id = args.vertex_model
                    deployment = f"vertex:{args.vertex_location}"
            if not str(tool_input.get("simplified_text") or "").strip():
                last_errors = ["model response missing simplified_text"]
                validation_note = (
                    "\n\n# Previous output failed validation\n"
                    "Errors: model response missing simplified_text\n"
                    "Return a complete corrected JSON/function payload with a non-empty simplified_text.\n"
                )
                continue
            out_record = build_simplified_record(
                source_path=src.source_path,
                pob_record=pob_record,
                tool_input=tool_input,
                model_id=model_id,
                model_version=model_version,
                prompt_id=args.prompt_id,
                prompt_sha=attempt_prompt_sha,
                raw_output_hash=sha256_text(raw_args),
                usage=usage,
                deployment=deployment,
            )
            write_yaml_atomic(src.target_path, out_record)
            errors = validate_simplified_record(src.target_path)
            if not errors:
                print(
                    f"drafted {rel(src.target_path)} cost=${out_record['ai_draft']['usage']['estimated_cost_usd']:.4f}",
                    flush=True,
                )
                return True
            last_errors = errors
            invalid_path = src.target_path.with_suffix(src.target_path.suffix + f".invalid-{int(time.time())}-{validation_attempt}")
            src.target_path.replace(invalid_path)
            validation_note = (
                "\n\n# Previous output failed validation\n"
                f"Errors: {errors}\n"
                "Return a corrected function call. Footnotes are allowed only when every marker appears exactly in simplified_text, e.g. [a]. "
                "Use unique markers and include no unanchored footnotes.\n"
            )
        raise RuntimeError(f"validation failed for {rel(src.target_path)} after retries: {last_errors}")
    finally:
        release_lock(lock)


def selected_records(args: argparse.Namespace) -> list[SourceRecord]:
    books = {b.lower().replace(" ", "_").replace("-", "_") for b in (args.book or [])} or None
    tests = set(args.testament or []) or None
    records = iter_status_records(book_filter=books, testament_filter=tests)
    if getattr(args, "chapter", None):
        wanted = {int(ch) for ch in args.chapter}
        records = [
            r
            for r in records
            if r.source_path.parent.name.isdigit() and int(r.source_path.parent.name) in wanted
        ]
    if getattr(args, "verse", None):
        wanted = {int(vs) for vs in args.verse}
        records = [
            r
            for r in records
            if r.source_path.stem.isdigit() and int(r.source_path.stem) in wanted
        ]
    if getattr(args, "verse_start", None) is not None:
        records = [
            r
            for r in records
            if r.source_path.stem.isdigit() and int(r.source_path.stem) >= int(args.verse_start)
        ]
    if getattr(args, "verse_end", None) is not None:
        records = [
            r
            for r in records
            if r.source_path.stem.isdigit() and int(r.source_path.stem) <= int(args.verse_end)
        ]
    if args.shard_count > 1:
        records = [r for i, r in enumerate(records) if i % args.shard_count == args.shard_index]
    return records


def command_draft(args: argparse.Namespace) -> int:
    records = selected_records(args)
    done = 0
    for src in records:
        if done >= args.limit > 0:
            break
        try:
            if draft_one(src, args=args):
                done += 1
        except Exception as exc:  # noqa: BLE001
            print(f"FAILED draft {rel(src.source_path)}: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
            if not args.keep_going:
                return 1
    print(f"draft command completed: wrote_or_processed={done}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    records = selected_records(args)
    checked = failed = 0
    for src in records:
        if args.only_existing and not src.target_path.exists():
            continue
        if checked >= args.limit > 0:
            break
        checked += 1
        errors = validate_simplified_record(src.target_path) if src.target_path.exists() else ["missing simplified YAML"]
        if errors:
            failed += 1
            print(f"{rel(src.target_path)}: {errors}")
    print(f"validated={checked} failed={failed}")
    return 1 if failed else 0


def collect_usage() -> dict[str, Any]:
    totals = {
        "draft_prompt_tokens": 0,
        "draft_completion_tokens": 0,
        "draft_cost_usd": 0.0,
        "files": 0,
        "invalid_files": 0,
    }
    by_status: dict[str, int] = {}
    for path in sorted(SIMPLIFIED_ROOT.glob("**/*.yaml*")):
        if path.name.endswith(".lock"):
            continue
        record = safe_load_yaml(path)
        is_invalid = ".invalid-" in path.name
        if is_invalid:
            totals["invalid_files"] += 1
        else:
            totals["files"] += 1
            status = str(record.get("status") or "unknown")
            by_status[status] = by_status.get(status, 0) + 1
        usage = ((record.get("ai_draft") or {}).get("usage") or {})
        totals["draft_prompt_tokens"] += int(usage.get("prompt_tokens") or 0)
        totals["draft_completion_tokens"] += int(usage.get("completion_tokens") or 0)
        totals["draft_cost_usd"] += float(usage.get("estimated_cost_usd") or 0)
    totals["draft_cost_usd"] = round(totals["draft_cost_usd"], 6)
    totals["by_status"] = by_status
    return totals


def command_summary(args: argparse.Namespace) -> int:
    records = selected_records(args)
    expected = len(records)
    existing = sum(1 for r in records if r.target_path.exists())
    status_counts: dict[str, int] = {}
    for r in records:
        if not r.target_path.exists():
            continue
        record = safe_load_yaml(r.target_path)
        status = str(record.get("status") or "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    payload = {
        "expected_records": expected,
        "simplified_files": existing,
        "pending_draft": expected - existing,
        "status_counts": status_counts,
        "usage": collect_usage(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def estimate_tokens_for_text(text: str) -> int:
    try:
        import tiktoken  # type: ignore

        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, int(len(text) / 3.2))


def command_estimate(args: argparse.Namespace) -> int:
    records = selected_records(args)
    sampled_records = records[: args.limit if args.limit > 0 else len(records)]
    draft_prompt_tokens = 0
    for src in sampled_records:
        record = safe_load_yaml(src.source_path)
        draft_prompt_tokens += estimate_tokens_for_text(DRAFT_SYSTEM_PROMPT) + estimate_tokens_for_text(build_draft_user_prompt(src.source_path, record))
    sampled = len(sampled_records)
    avg = draft_prompt_tokens / sampled if sampled else 0
    projected_input = int(avg * len(records))
    projected_output = int(len(records) * args.output_tokens_per_record)
    prices = model_prices(args.model)
    cost = projected_input / 1_000_000 * prices["input"] + projected_output / 1_000_000 * prices["output"]
    print(json.dumps({
        "records": len(records),
        "sampled_records": sampled,
        "avg_estimated_input_tokens_per_record": round(avg, 1),
        "projected_input_tokens": projected_input,
        "projected_output_tokens": projected_output,
        "model": args.model,
        "estimated_draft_cost_usd": round(cost, 2),
    }, indent=2))
    return 0


def add_common_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--book", action="append", help="Book slug/name filter, repeatable")
    parser.add_argument("--testament", action="append", choices=["ot", "nt", "deuterocanon", "extra_canonical"])
    parser.add_argument("--chapter", action="append", type=int, help="Chapter number filter, repeatable")
    parser.add_argument("--verse", action="append", type=int, help="Verse number filter, repeatable")
    parser.add_argument("--verse-start", type=int, help="Minimum verse number filter")
    parser.add_argument("--verse-end", type=int, help="Maximum verse number filter")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("draft", help="Draft Simplified POB YAML records")
    add_common_filters(p)
    p.add_argument("--limit", type=int, default=1, help="0 = no limit")
    p.add_argument("--worker-id", default=f"simplified-draft-{os.getpid()}")
    p.add_argument("--backend", choices=["auto", "azure", "gemini", "vertex"], default=DEFAULT_BACKEND)
    p.add_argument("--model", default=DEFAULT_DRAFT_MODEL_ID)
    p.add_argument("--deployment", default=DEFAULT_DRAFT_DEPLOYMENT)
    p.add_argument("--gemini-model", default=DEFAULT_GEMINI_MODEL)
    p.add_argument("--vertex-model", default=DEFAULT_VERTEX_MODEL)
    p.add_argument("--vertex-location", default=DEFAULT_VERTEX_LOCATION)
    p.add_argument("--prompt-id", default="simplified_pob_understanding_first_compact_v3")
    p.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    p.add_argument("--max-completion-tokens", type=int, default=3000)
    p.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    p.add_argument("--retries", type=int, default=2)
    p.add_argument("--validation-retries", type=int, default=1)
    p.add_argument("--force", action="store_true")
    p.add_argument("--keep-going", action="store_true")
    p.add_argument("--dry-run-prompt", action="store_true")
    p.set_defaults(func=command_draft)

    p = sub.add_parser("validate", help="Validate Simplified POB YAML records")
    add_common_filters(p)
    p.add_argument("--limit", type=int, default=0, help="0 = no limit")
    p.add_argument("--only-existing", action="store_true")
    p.set_defaults(func=command_validate)

    p = sub.add_parser("summary", help="Summarize Simplified POB progress and observed API costs")
    add_common_filters(p)
    p.set_defaults(func=command_summary)

    p = sub.add_parser("estimate", help="Estimate draft cost for selected records")
    add_common_filters(p)
    p.add_argument("--limit", type=int, default=250, help="sample records for input estimate; 0 = all")
    p.add_argument("--model", default=DEFAULT_DRAFT_MODEL_ID)
    p.add_argument("--output-tokens-per-record", type=int, default=900)
    p.set_defaults(func=command_estimate)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.shard_index < 0 or args.shard_count < 1 or args.shard_index >= args.shard_count:
        parser.error("shard-index must be in [0, shard-count)")
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
