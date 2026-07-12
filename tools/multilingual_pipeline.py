#!/usr/bin/env python3
"""Azure-only source-grounded POB translation pipeline for new languages.

The pipeline starts with small calibration pilots. GPT-5.6 Sol drafts from the
original-language source packet and English POB audit trail; GPT-5.6 Terra
independently reviews and may apply a bounded revision. No Vertex/Gemini path
exists in this tool.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "multilingual_languages.yaml"
SOURCE_ROOT = ROOT / "translation"
DEFAULT_PILOT = (
    "ot/genesis/001/001.yaml",
    "nt/john/001/001.yaml",
    "ot/ecclesiastes/001/002.yaml",
)
ENDPOINT = os.environ.get(
    "AZURE_OPENAI_ENDPOINT", "https://cartha-aoai-truth-1c9177c8.openai.azure.com"
).rstrip("/")
RESOURCE_GROUP = "rg-cartha-truth-openai"
ACCOUNT = "cartha-aoai-truth-1c9177c8"
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_config() -> dict[str, Any]:
    data = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("languages"), dict):
        raise RuntimeError("invalid multilingual language config")
    return data


def azure_key() -> str:
    key = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
    if key:
        return key
    raw = subprocess.check_output(
        [
            "az", "cognitiveservices", "account", "keys", "list",
            "--resource-group", RESOURCE_GROUP, "--name", ACCOUNT, "-o", "json",
        ],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    payload = json.loads(raw)
    key = str(payload.get("key1") or payload.get("key2") or "").strip()
    if not key:
        raise RuntimeError("Azure OpenAI key unavailable from the logged-in Azure CLI")
    return key


def call_tool(
    *, deployment: str, system: str, user: str, tool: dict[str, Any], name: str,
    max_tokens: int = 7000, retries: int = 6,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    body = {
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_completion_tokens": max_tokens,
        "parallel_tool_calls": False,
        "tool_choice": {"type": "function", "function": {"name": name}},
        "tools": [tool],
    }
    encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
    url = f"{ENDPOINT}/openai/deployments/{deployment}/chat/completions?api-version={API_VERSION}"
    last: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url, data=encoded,
            headers={"Content-Type": "application/json", "api-key": azure_key()}, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                response_body = json.loads(response.read().decode("utf-8"))
            message = response_body["choices"][0]["message"]
            calls = message.get("tool_calls") or []
            if len(calls) != 1 or (calls[0].get("function") or {}).get("name") != name:
                raise RuntimeError("model did not return the required single tool call")
            raw = (calls[0].get("function") or {}).get("arguments") or "{}"
            return json.loads(raw), response_body.get("usage") or {}, hashlib.sha256(raw.encode()).hexdigest()
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            last = RuntimeError(f"Azure HTTP {exc.code}: {error_body[:600]}")
            if exc.code not in {408, 429, 500, 502, 503, 504}:
                break
        except Exception as exc:  # noqa: BLE001
            last = exc
        if attempt < retries:
            time.sleep(min(30, 2 ** attempt))
    raise last or RuntimeError("Azure request failed")


DRAFT_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_translation_draft", "strict": True,
        "description": "Submit a source-grounded publication draft.",
        "parameters": {
            "type": "object", "additionalProperties": False,
            "required": ["text", "philosophy", "lexical_decisions", "theological_decisions", "footnotes", "register_notes"],
            "properties": {
                "text": {"type": "string"},
                "philosophy": {"type": "string", "enum": ["formal", "dynamic", "optimal-equivalence"]},
                "lexical_decisions": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["source_word", "choice", "rationale"], "properties": {"source_word": {"type": "string"}, "choice": {"type": "string"}, "rationale": {"type": "string"}}}},
                "theological_decisions": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["issue", "choice", "alternative", "rationale"], "properties": {"issue": {"type": "string"}, "choice": {"type": "string"}, "alternative": {"type": "string"}, "rationale": {"type": "string"}}}},
                "footnotes": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["marker", "text", "reason"], "properties": {"marker": {"type": "string"}, "text": {"type": "string"}, "reason": {"type": "string"}}}},
                "register_notes": {"type": "string"},
            },
        },
    },
}

REVIEW_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_translation_review", "strict": True,
        "description": "Independently review and, when safe, revise a translation draft.",
        "parameters": {
            "type": "object", "additionalProperties": False,
            "required": ["verdict", "source_fidelity", "naturalness", "terminology", "issues", "revised_text", "revised_footnotes", "revision_rationale", "requires_human_review"],
            "properties": {
                "verdict": {"type": "string", "enum": ["approve", "revise", "reject"]},
                "source_fidelity": {"type": "string"}, "naturalness": {"type": "string"}, "terminology": {"type": "string"},
                "issues": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["severity", "issue", "rationale"], "properties": {"severity": {"type": "string", "enum": ["low", "medium", "high"]}, "issue": {"type": "string"}, "rationale": {"type": "string"}}}},
                "revised_text": {"type": "string"},
                "revised_footnotes": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["marker", "text", "reason"], "properties": {"marker": {"type": "string"}, "text": {"type": "string"}, "reason": {"type": "string"}}}},
                "revision_rationale": {"type": "string"}, "requires_human_review": {"type": "boolean"},
            },
        },
    },
}


def source_record(relative: str) -> tuple[pathlib.Path, dict[str, Any]]:
    path = SOURCE_ROOT / relative
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"invalid source record {path}")
    return path, data


def target_path(code: str, source_path: pathlib.Path) -> pathlib.Path:
    return ROOT / f"translation_{code}" / source_path.relative_to(SOURCE_ROOT)


def context_for(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record.get("id"), "reference": record.get("reference"),
        "original_language_source": record.get("source") or {},
        "english_pob": record.get("translation") or {},
        "english_lexical_decisions": (record.get("lexical_decisions") or [])[:12],
        "english_theological_decisions": (record.get("theological_decisions") or [])[:8],
        "latest_revisions": (record.get("revisions") or [])[-3:],
    }


def validate(data: dict[str, Any], code: str) -> list[str]:
    errors: list[str] = []
    if (data.get("language") or {}).get("code") != code:
        errors.append("language.code mismatch")
    translation = data.get("translation") or {}
    text = str(translation.get("text") or "").strip()
    if not text:
        errors.append("translation.text missing")
    notes = translation.get("footnotes") or []
    markers = [str(x.get("marker") or "") for x in notes if isinstance(x, dict)]
    if len(markers) != len(set(markers)):
        errors.append("duplicate footnote markers")
    for marker in markers:
        if marker and f"[{marker}]" not in text:
            errors.append(f"unanchored footnote [{marker}]")
    return errors


def write_atomic(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(rendered)
        temporary = pathlib.Path(handle.name)
    temporary.replace(path)


def draft_one(code: str, spec: dict[str, Any], relative: str, deployment: str, force: bool) -> tuple[str, str, dict[str, Any]]:
    path, english = source_record(relative)
    destination = target_path(code, path)
    if destination.exists() and not force:
        return "skip", str(destination.relative_to(ROOT)), {}
    system = f"""You are drafting the People's Open Bible in {spec['name']} ({spec['native_name']}).
Target variant: {spec['variant']}.
Translate from the original-language source evidence first. The English POB is an audited consultation layer, not an opaque base text. Preserve genuine ambiguity and theological tension instead of silently resolving it. Use natural, current, dignified language understandable to ordinary modern readers. Do not import denominational distinctives or any named interpreter's private doctrine. Every footnote marker must appear in the main text as [a], [b], etc. Call submit_translation_draft exactly once."""
    user = yaml.safe_dump(context_for(english), allow_unicode=True, sort_keys=False, width=1000)
    result, usage, output_hash = call_tool(deployment=deployment, system=system, user=user, tool=DRAFT_TOOL, name="submit_translation_draft")
    translation = {"language": code, "text": result["text"], "philosophy": result["philosophy"]}
    if result.get("footnotes"):
        translation["footnotes"] = result["footnotes"]
    record = {
        "id": english.get("id"), "reference": english.get("reference"),
        "language": {"code": code, "name": spec["name"], "native_name": spec["native_name"], "variant": spec["variant"]},
        "source": english.get("source") or {},
        "base_translation": {"language": "en", "yaml_path": str(path.relative_to(ROOT)), "text": (english.get("translation") or {}).get("text")},
        "translation": translation,
        "lexical_decisions": result.get("lexical_decisions") or [],
        "theological_decisions": result.get("theological_decisions") or [],
        "translation_notes": {"register": result.get("register_notes")},
        "source_grounding": {"english_pob_role": "consult_only"},
        "ai_draft": {"model_id": "gpt-5.6-sol", "azure_deployment": deployment, "prompt_id": "multilingual_source_draft_v1", "timestamp": now(), "output_hash": output_hash, "usage": usage},
        "status": "draft",
    }
    errors = validate(record, code)
    if errors:
        raise RuntimeError(f"validation failed: {errors}")
    write_atomic(destination, record)
    return "drafted", str(destination.relative_to(ROOT)), usage


def review_one(code: str, spec: dict[str, Any], relative: str, deployment: str, force: bool) -> tuple[str, str, dict[str, Any]]:
    path, english = source_record(relative)
    destination = target_path(code, path)
    if not destination.exists():
        return "missing", str(destination.relative_to(ROOT)), {}
    record = yaml.safe_load(destination.read_text(encoding="utf-8"))
    if record.get("review_pass") and not force:
        return "skip", str(destination.relative_to(ROOT)), {}
    system = f"""You are the independent {spec['name']} reviewer for the People's Open Bible.
Target variant: {spec['variant']}. Review against the original-language source first, then the English POB audit trail. Check source fidelity, natural modern usage, register, names, key theological terms, and footnote anchors. Preserve ambiguity when the source is disputed. Do not impose denominational or named-interpreter doctrine. Provide a complete revised text only when a safe correction is needed. Call submit_translation_review exactly once."""
    user_payload = {"source_context": context_for(english), "draft": record}
    result, usage, output_hash = call_tool(deployment=deployment, system=system, user=yaml.safe_dump(user_payload, allow_unicode=True, sort_keys=False, width=1000), tool=REVIEW_TOOL, name="submit_translation_review")
    old_text = str((record.get("translation") or {}).get("text") or "")
    old_footnotes = list((record.get("translation") or {}).get("footnotes") or [])
    revised = str(result.get("revised_text") or "").strip()
    revised_footnotes = result.get("revised_footnotes") if isinstance(result.get("revised_footnotes"), list) else old_footnotes
    text_changed = bool(revised and revised != old_text)
    footnotes_changed = revised_footnotes != old_footnotes
    apply = result.get("verdict") == "revise" and (text_changed or footnotes_changed) and not result.get("requires_human_review")
    auto_apply_blocked_errors: list[str] = []
    if apply:
        candidate = json.loads(json.dumps(record, ensure_ascii=False))
        candidate["translation"]["text"] = revised if revised else old_text
        if revised_footnotes:
            candidate["translation"]["footnotes"] = revised_footnotes
        else:
            candidate["translation"].pop("footnotes", None)
        auto_apply_blocked_errors = validate(candidate, code)
        if auto_apply_blocked_errors:
            apply = False
    if apply:
        record.setdefault("revisions", []).append({"from": old_text, "to": revised, "rationale": result.get("revision_rationale"), "reviewer_model": "gpt-5.6-terra", "timestamp": now()})
        record["translation"]["text"] = revised if revised else old_text
        if revised_footnotes:
            record["translation"]["footnotes"] = revised_footnotes
        else:
            record["translation"].pop("footnotes", None)
    record["review_pass"] = {**result, "model_id": "gpt-5.6-terra", "azure_deployment": deployment, "prompt_id": "multilingual_source_review_v1", "timestamp": now(), "output_hash": output_hash, "usage": usage, "applied_revision": apply, "auto_apply_blocked_errors": auto_apply_blocked_errors}
    record["status"] = "reviewed" if result.get("verdict") == "approve" or apply else "needs_human_review"
    errors = validate(record, code)
    if errors:
        raise RuntimeError(f"reviewed record validation failed: {errors}")
    write_atomic(destination, record)
    return "reviewed", str(destination.relative_to(ROOT)), usage


def selected_languages(config: dict[str, Any], values: list[str]) -> list[tuple[str, dict[str, Any]]]:
    languages = config["languages"]
    if not values or "all" in values:
        return [(code, spec) for code, spec in languages.items() if spec.get("status") == "pilot"]
    unknown = [code for code in values if code not in languages]
    if unknown:
        raise SystemExit(f"unknown language codes: {', '.join(unknown)}")
    return [(code, languages[code]) for code in values]


def command_status(args: argparse.Namespace) -> int:
    config = load_config()
    rows = []
    for code, spec in config["languages"].items():
        root = SOURCE_ROOT if code == "en" else ROOT / f"translation_{code}"
        files = list(root.rglob("*.yaml")) if root.exists() else []
        reviewed = 0
        if files:
            probe = subprocess.run(
                ["rg", "-l", "^review_pass:", str(root)],
                text=True, capture_output=True, check=False,
            )
            reviewed = len([line for line in probe.stdout.splitlines() if line.strip()])
        rows.append({"code": code, "language": spec["name"], "project_status": spec["status"], "files": len(files), "reviewed": reviewed})
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


def command_pilot(args: argparse.Namespace) -> int:
    config = load_config()
    languages = selected_languages(config, args.language)
    verses = list(args.verse or DEFAULT_PILOT)[: args.limit_verses or None]
    jobs = [(code, spec, verse) for code, spec in languages for verse in verses]
    print(f"Azure-only multilingual pilot: languages={len(languages)} verses_each={len(verses)} jobs={len(jobs)} stage={args.stage}")
    azure_key()  # fail before launching workers
    totals = {"drafted": 0, "reviewed": 0, "skip": 0, "error": 0, "prompt_tokens": 0, "completion_tokens": 0}

    def run(job: tuple[str, dict[str, Any], str]) -> list[tuple[str, str, dict[str, Any]]]:
        code, spec, verse = job
        output = []
        if args.stage in {"draft", "both"}:
            output.append(draft_one(code, spec, verse, args.draft_deployment, args.force))
        if args.stage in {"review", "both"}:
            output.append(review_one(code, spec, verse, args.review_deployment, args.force))
        return output

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = {pool.submit(run, job): job for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            code, _spec, verse = futures[future]
            try:
                for status, path, usage in future.result():
                    totals[status if status in totals else "skip"] += 1
                    totals["prompt_tokens"] += int(usage.get("prompt_tokens") or 0)
                    totals["completion_tokens"] += int(usage.get("completion_tokens") or 0)
                    print(f"{status:8} {code:8} {verse} -> {path}", flush=True)
            except Exception as exc:  # noqa: BLE001
                totals["error"] += 1
                print(f"ERROR    {code:8} {verse}: {exc}", flush=True)
    print(json.dumps(totals, indent=2))
    return 1 if totals["error"] else 0


def command_wave(args: argparse.Namespace) -> int:
    sources = sorted(SOURCE_ROOT.rglob("*.yaml"))
    relatives = [str(path.relative_to(SOURCE_ROOT)) for path in sources]
    if args.testament:
        relatives = [value for value in relatives if value.split("/", 1)[0] == args.testament]
    if args.book:
        relatives = [value for value in relatives if len(value.split("/")) > 1 and value.split("/")[1] == args.book]
    relatives = relatives[args.offset : args.offset + args.limit_records]
    if not relatives:
        print("No source records matched this bounded wave.")
        return 0
    args.verse = relatives
    args.limit_verses = 0
    return command_pilot(args)


def command_validate(args: argparse.Namespace) -> int:
    config = load_config()
    bad = checked = 0
    for code, _spec in selected_languages(config, args.language):
        root = ROOT / f"translation_{code}"
        for path in root.rglob("*.yaml") if root.exists() else []:
            checked += 1
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                errors = validate(data, code)
            except Exception as exc:  # noqa: BLE001
                errors = [str(exc)]
            if errors:
                bad += 1
                print(f"BAD {path.relative_to(ROOT)}: {errors}")
    print(f"checked={checked} bad={bad}")
    return 1 if bad else 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status")
    status.set_defaults(func=command_status)
    pilot = sub.add_parser("pilot")
    pilot.add_argument("--language", action="append", default=[])
    pilot.add_argument("--verse", action="append")
    pilot.add_argument("--limit-verses", type=int, default=1)
    pilot.add_argument("--stage", choices=["draft", "review", "both"], default="both")
    pilot.add_argument("--concurrency", type=int, default=8)
    pilot.add_argument("--draft-deployment", default="gpt-5-6-sol-atlas")
    pilot.add_argument("--review-deployment", default="gpt-5-6-terra-atlas")
    pilot.add_argument("--force", action="store_true")
    pilot.set_defaults(func=command_pilot)
    wave = sub.add_parser("wave", help="Run a bounded, resumable source-tree wave")
    wave.add_argument("--language", action="append", required=True)
    wave.add_argument("--limit-records", type=int, default=100)
    wave.add_argument("--offset", type=int, default=0)
    wave.add_argument("--testament", choices=["ot", "nt", "deuterocanon", "extra_canonical"])
    wave.add_argument("--book")
    wave.add_argument("--stage", choices=["draft", "review", "both"], default="both")
    wave.add_argument("--concurrency", type=int, default=8)
    wave.add_argument("--draft-deployment", default="gpt-5-6-sol-atlas")
    wave.add_argument("--review-deployment", default="gpt-5-6-terra-atlas")
    wave.add_argument("--force", action="store_true")
    wave.set_defaults(func=command_wave)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--language", action="append", default=[])
    validate_parser.set_defaults(func=command_validate)
    return root


def main() -> int:
    args = parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
