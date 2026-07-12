#!/usr/bin/env python3
"""Localize reader metadata and critical SPOB passages with Azure GPT-5.6.

This calibration layer proves more than verse transport: it localizes book
titles, short reader summaries, author/audience/date metadata, core picker UI,
and five high-impact SPOB passages. Sol drafts; Terra independently reviews.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import pathlib
from typing import Any

import yaml

from multilingual_pipeline import ROOT, call_tool, load_config, now, write_atomic

METADATA_BOOKS = ("Genesis", "John", "Gospel of Thomas")
BOOK_SUMMARIES = {
    "Genesis": (
        "Genesis tells of creation, humanity's rebellion and scattering, and the family of "
        "Abraham, Isaac, Jacob, and Joseph through whom God's covenant promises to Israel begin."
    ),
    "John": (
        "John presents Jesus as the eternal Word who reveals the Father, gives life through "
        "trust in him, and is glorified through his signs, death, and resurrection."
    ),
    "Gospel of Thomas": (
        "The Gospel of Thomas is a collection of sayings attributed to Jesus. It has no continuous "
        "story and repeatedly calls readers to discover the meaning of the sayings."
    ),
}
CRITICAL_SPOB = (
    "ot/genesis/001/001.yaml",
    "ot/ecclesiastes/001/002.yaml",
    "nt/john/001/001.yaml",
    "nt/romans/003/025.yaml",
    "nt/1_peter/001/013.yaml",
)

BOOK_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["source_title", "title", "author", "audience", "date", "summary"],
    "properties": {
        "source_title": {"type": "string"}, "title": {"type": "string"},
        "author": {"type": "string"}, "audience": {"type": "string"},
        "date": {"type": "string"}, "summary": {"type": "string"},
    },
}
PASSAGE_ITEM = {
    "type": "object", "additionalProperties": False,
    "required": ["source_path", "reference", "text", "translator_note"],
    "properties": {
        "source_path": {"type": "string"},
        "reference": {"type": "string"}, "text": {"type": "string"},
        "translator_note": {"type": "string"},
    },
}
UI_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["translations", "choose_language", "search_languages", "available_now", "translation_in_progress", "select"],
    "properties": {key: {"type": "string"} for key in (
        "translations", "choose_language", "search_languages", "available_now",
        "translation_in_progress", "select",
    )},
}


def payload_schema(*, review: bool) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "book_localizations": {"type": "array", "items": BOOK_ITEM},
        "spob_critical_passages": {"type": "array", "items": PASSAGE_ITEM},
        "reader_ui": UI_SCHEMA,
    }
    required = list(properties)
    if review:
        properties = {
            "verdict": {"type": "string", "enum": ["approve", "revise", "needs_human_review"]},
            "review_summary": {"type": "string"},
            "issues": {"type": "array", "items": {"type": "string"}},
            **properties,
        }
        required = list(properties)
    return {"type": "object", "additionalProperties": False, "required": required, "properties": properties}


def tool(name: str, *, review: bool) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name, "strict": True,
            "description": "Submit localized Bible metadata, reader UI, and critical SPOB passages.",
            "parameters": payload_schema(review=review),
        },
    }


def source_context() -> dict[str, Any]:
    metadata = json.loads((ROOT / "book_metadata.json").read_text(encoding="utf-8"))["books"]
    books = {
        name: {
            **{key: metadata[name][key] for key in ("author", "audience", "date")},
            "summary": BOOK_SUMMARIES[name],
        }
        for name in METADATA_BOOKS
    }
    passages = []
    for relative in CRITICAL_SPOB:
        record = yaml.safe_load((ROOT / "translation_simplified" / relative).read_text(encoding="utf-8"))
        passages.append({
            "source_path": relative,
            "reference": record.get("reference"),
            "spob_text": (record.get("translation") or {}).get("text"),
            "source": record.get("source") or {},
            "footnotes": (record.get("translation") or {}).get("footnotes") or [],
            "interpretive_expansions": record.get("interpretive_expansions") or [],
        })
    return {"books": books, "critical_spob_passages": passages}


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    books = payload.get("book_localizations") or []
    passages = payload.get("spob_critical_passages") or []
    if {item.get("source_title") for item in books} != set(METADATA_BOOKS):
        errors.append("book set mismatch")
    if {item.get("source_path") for item in passages} != set(CRITICAL_SPOB):
        errors.append("critical passage set mismatch")
    for item in books:
        if any(not str(item.get(key) or "").strip() for key in ("title", "author", "audience", "date", "summary")):
            errors.append(f"incomplete book localization: {item.get('source_title')}")
    for item in passages:
        if not str(item.get("text") or "").strip():
            errors.append(f"empty SPOB passage: {item.get('reference')}")
    return errors


def language_selection(values: list[str]) -> list[tuple[str, dict[str, Any]]]:
    languages = load_config()["languages"]
    if not values or "all" in values:
        return [(code, spec) for code, spec in languages.items() if code != "en"]
    unknown = [code for code in values if code not in languages or code == "en"]
    if unknown:
        raise SystemExit(f"unknown/non-target languages: {', '.join(unknown)}")
    return [(code, languages[code]) for code in values]


def run_language(code: str, spec: dict[str, Any], force: bool) -> tuple[str, dict[str, Any]]:
    target = ROOT / "localization" / code / "calibration.yaml"
    if target.exists() and not force:
        return "skip", {}
    context = source_context()
    system = f"""Localize Bible-reader content into {spec['name']} ({spec['native_name']}).
Target variant: {spec['variant']}.
Write natural, current, dignified language for ordinary readers. Translate the supplied titles and metadata, including each supplied summary, accurately without amplifying historical claims or inventing a replacement summary. The SPOB passages are understanding-first renderings: preserve their explanatory clarity while checking the supplied original-language source so the localization does not drift. Preserve disputed possibilities in the translator note. Do not import denominational or named-interpreter doctrine. Return every requested item exactly once."""
    system += """
Never leave a requested field blank. When the source metadata is genuinely unknown or disputed, say that plainly in the target language instead of returning an empty string."""
    draft, draft_usage, draft_hash = call_tool(
        deployment="gpt-5-6-sol-atlas", system=system,
        user=yaml.safe_dump(context, allow_unicode=True, sort_keys=False, width=1000),
        tool=tool("submit_localization_draft", review=False),
        name="submit_localization_draft", max_tokens=10000,
    )
    errors = validate(draft)
    if errors:
        raise RuntimeError(f"draft validation failed: {errors}")
    review_system = f"""You are the independent {spec['name']} localization reviewer.
Check every title, author/audience/date field, short summary, reader-UI label, and SPOB passage against the supplied source context. Prefer idiomatic modern {spec['name']} without losing source meaning. Return the complete corrected payload, even when approving. Do not add denominational or named-interpreter doctrine."""
    review_input = {"source_context": context, "draft": draft}
    reviewed, review_usage, review_hash = call_tool(
        deployment="gpt-5-6-terra-atlas", system=review_system,
        user=yaml.safe_dump(review_input, allow_unicode=True, sort_keys=False, width=1000),
        tool=tool("submit_localization_review", review=True),
        name="submit_localization_review", max_tokens=11000,
    )
    errors = validate(reviewed)
    if errors:
        raise RuntimeError(f"review validation failed: {errors}")
    output = {
        "language": {"code": code, **spec},
        "book_localizations": reviewed["book_localizations"],
        "spob_critical_passages": reviewed["spob_critical_passages"],
        "reader_ui": reviewed["reader_ui"],
        "review": {
            "verdict": reviewed["verdict"], "summary": reviewed["review_summary"],
            "issues": reviewed["issues"], "model_id": "gpt-5.6-terra",
            "azure_deployment": "gpt-5-6-terra-atlas", "timestamp": now(),
            "output_hash": review_hash, "usage": review_usage,
        },
        "draft_provenance": {
            "model_id": "gpt-5.6-sol", "azure_deployment": "gpt-5-6-sol-atlas",
            "timestamp": now(), "output_hash": draft_hash, "usage": draft_usage,
        },
        "status": "reviewed" if reviewed["verdict"] != "needs_human_review" else "needs_human_review",
    }
    write_atomic(target, output)
    return "reviewed", {
        "prompt_tokens": int(draft_usage.get("prompt_tokens") or 0) + int(review_usage.get("prompt_tokens") or 0),
        "completion_tokens": int(draft_usage.get("completion_tokens") or 0) + int(review_usage.get("completion_tokens") or 0),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", action="append", default=[])
    parser.add_argument("--concurrency", type=int, default=6)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    selected = language_selection(args.language)
    totals = {"reviewed": 0, "skip": 0, "error": 0, "prompt_tokens": 0, "completion_tokens": 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = {pool.submit(run_language, code, spec, args.force): code for code, spec in selected}
        for future in concurrent.futures.as_completed(futures):
            code = futures[future]
            try:
                status, usage = future.result()
                totals[status] += 1
                totals["prompt_tokens"] += usage.get("prompt_tokens", 0)
                totals["completion_tokens"] += usage.get("completion_tokens", 0)
                print(f"{status:8} {code}", flush=True)
            except Exception as exc:  # noqa: BLE001
                totals["error"] += 1
                print(f"ERROR    {code}: {exc}", flush=True)
    print(json.dumps(totals, indent=2))
    return 1 if totals["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
