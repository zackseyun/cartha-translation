#!/usr/bin/env python3
"""Finish the reviewed chapter-summary layer for every published reader language.

This is the catalog-scale companion to ``multilingual_summary_localization``.
It selects the canonical GPT-5.4 English Quick Study rows that the readers
request, translates them in bounded same-language packets with Sol, has Terra
independently correct every packet, and writes each localized row under the
reader's established summary namespace.

The English summary is closed source. This pipeline translates it; it never
re-summarizes Scripture or adds interpretation. Runs are resumable and safe to
repeat because exact current derivatives are skipped before any model call.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import sys
from collections import defaultdict
from typing import Any, Iterable

import boto3

import multilingual_summary_localization as base
from multilingual_pipeline import azure_key, call_tool, load_config


DEFAULT_MODEL_VERSION = "gpt-5.4-2026-03-05"
DEFAULT_BATCH_SIZE = 20
DEFAULT_CONCURRENCY = 8


TRANSLATE_BATCH_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_summary_translation_batch",
        "strict": True,
        "description": "Submit every requested closed-source summary translation.",
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "required": ["translations"],
            "properties": {
                "translations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["id", "translation"],
                        "properties": {
                            "id": {"type": "string"},
                            "translation": {"type": "string"},
                        },
                    },
                }
            },
        },
    },
}


REVIEW_BATCH_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_summary_translation_review_batch",
        "strict": True,
        "description": "Independently review and correct every summary translation.",
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "required": ["items"],
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "verdict",
                            "final_translation",
                            "issues",
                            "review_summary",
                            "safe_to_publish",
                        ],
                        "properties": {
                            "id": {"type": "string"},
                            "verdict": {
                                "type": "string",
                                "enum": ["approve", "revise", "reject"],
                            },
                            "final_translation": {"type": "string"},
                            "issues": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "review_summary": {"type": "string"},
                            "safe_to_publish": {"type": "boolean"},
                        },
                    },
                }
            },
        },
    },
}


def task_id(task: dict[str, Any]) -> str:
    return hashlib.sha256(str(task["target_key"]).encode()).hexdigest()[:20]


def _indexed(items: Any, expected: set[str], label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        raise RuntimeError(f"{label} did not return an item list")
    indexed: dict[str, dict[str, Any]] = {}
    for raw in items:
        if not isinstance(raw, dict) or not str(raw.get("id") or ""):
            raise RuntimeError(f"{label} returned an invalid item")
        identity = str(raw["id"])
        if identity in indexed:
            raise RuntimeError(f"{label} duplicated id {identity}")
        indexed[identity] = raw
    if set(indexed) != expected:
        missing = sorted(expected - set(indexed))
        extra = sorted(set(indexed) - expected)
        raise RuntimeError(f"{label} identity mismatch: missing={missing} extra={extra}")
    return indexed


def scan_sources(
    ddb: Any,
    table: str,
    model_version: str,
    book: str = "",
) -> list[dict[str, Any]]:
    request: dict[str, Any] = {
        "TableName": table,
        "FilterExpression": (
            "#translation = :source AND #scope = :chapter AND #tool = :simplify "
            "AND #model = :model AND attribute_exists(#output)"
        ),
        "ExpressionAttributeNames": {
            "#translation": "translation",
            "#scope": "scope",
            "#tool": "tool",
            "#model": "model_version",
            "#book": "book",
            "#output": "output",
        },
        "ExpressionAttributeValues": {
            ":source": {"S": base.SOURCE_TRANSLATION},
            ":chapter": {"S": "chapter"},
            ":simplify": {"S": "simplify"},
            ":model": {"S": model_version},
        },
        "ProjectionExpression": (
            "summary_key,#translation,translation_version,#scope,#book,chapter,"
            "#tool,#output,prompt_version,model_version,source_hash,verse_count,"
            "generated_at,updated_at"
        ),
    }
    if book.strip():
        request["FilterExpression"] += " AND #book = :book"
        request["ExpressionAttributeValues"][":book"] = {"S": book.strip().upper()}
    sources: list[dict[str, Any]] = []
    while True:
        response = ddb.scan(**request)
        sources.extend(
            row
            for row in (
                base.deserialize_item(item) for item in response.get("Items", [])
            )
            if base._source_row_valid(row)
        )
        cursor = response.get("LastEvaluatedKey")
        if not cursor:
            break
        request["ExclusiveStartKey"] = cursor
    return sorted(
        sources,
        key=lambda row: (
            str(row.get("book") or ""),
            int(row.get("chapter") or 0),
            str(row.get("prompt_version") or ""),
        ),
    )


def resolve_languages(values: Iterable[str]) -> list[tuple[str, dict[str, Any]]]:
    requested = [part.strip() for value in values for part in value.split(",") if part.strip()]
    config = load_config()
    if requested == ["all"] or not requested:
        requested = [code for code in config["rollout_priority"] if code != "en"]
    return base.configured_languages(requested)


def collect_tasks(
    ddb: Any,
    table: str,
    sources: list[dict[str, Any]],
    languages: list[tuple[str, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], int]:
    candidates = [
        base.task_for(source, code, spec)
        for code, spec in languages
        for source in sources
    ]
    existing = base.batch_get_targets(
        ddb, table, (task["target_key"] for task in candidates)
    )
    tasks = [
        task
        for task in candidates
        if not base.existing_matches(existing.get(task["target_key"]), task)
        and not base.task_is_blocked(task)
    ]
    return tasks, len(candidates) - len(tasks)


def _draft_system(task: dict[str, Any]) -> str:
    spec = task["language_spec"]
    return f"""You are an exacting professional translator into {spec['name']} ({spec['native_name']}).
Target variant: {spec['variant']}.

Translate every supplied English POB chapter summary. Each English summary is a closed and authoritative source. Preserve every claim, qualification, relationship, citation, name, and degree of certainty. Do not consult, reconstruct, explain, improve, harmonize, or expand the underlying passage. Do not add exegesis, devotional application, headings, notes, or facts. Do not remove difficult or disputed claims. Use natural, dignified, current target-language prose. Return exactly one complete translation for every supplied id through the required tool."""


def _review_system(task: dict[str, Any]) -> str:
    spec = task["language_spec"]
    return f"""You are the independent senior {spec['name']} ({spec['native_name']}) translation reviewer.
Target variant: {spec['variant']}.

For every id, compare the candidate translation sentence by sentence with its English POB summary. The English prose is the only source of truth. Correct omissions, additions, altered certainty, mistranslations, awkward language, names, and references. Do not use outside Bible knowledge and do not add exegesis, interpretation, historical detail, devotional application, headings, or notes. Return every id and its complete corrected target-language summary. Set safe_to_publish=false only when a faithful correction cannot be completed from the supplied English prose."""


def translate_batch(
    tasks: list[dict[str, Any]], draft_deployment: str, review_deployment: str
) -> list[dict[str, Any]]:
    if not tasks or len({task["language"] for task in tasks}) != 1:
        raise ValueError("a batch must contain one language")
    ids = {task_id(task) for task in tasks}
    source_payload = [
        {
            "id": task_id(task),
            "book": task["source"].get("book"),
            "chapter": task["source"].get("chapter"),
            "english_summary": str(task["source"]["output"]).strip(),
        }
        for task in tasks
    ]
    draft, draft_usage, draft_hash = call_tool(
        deployment=draft_deployment,
        system=_draft_system(tasks[0]),
        user=json.dumps({"summaries": source_payload}, ensure_ascii=False),
        tool=TRANSLATE_BATCH_TOOL,
        name="submit_summary_translation_batch",
        max_tokens=18000,
        retries=4,
    )
    drafts = _indexed(draft.get("translations"), ids, "Sol draft")
    review_payload = [
        {
            **source,
            "candidate_translation": str(drafts[source["id"]]["translation"]).strip(),
        }
        for source in source_payload
    ]
    review, review_usage, review_hash = call_tool(
        deployment=review_deployment,
        system=_review_system(tasks[0]),
        user=json.dumps({"summaries": review_payload}, ensure_ascii=False),
        tool=REVIEW_BATCH_TOOL,
        name="submit_summary_translation_review_batch",
        max_tokens=20000,
        retries=4,
    )
    reviewed = _indexed(review.get("items"), ids, "Terra review")
    results: list[dict[str, Any]] = []
    for task in tasks:
        identity = task_id(task)
        item = reviewed[identity]
        final = str(item.get("final_translation") or "").strip()
        if not final or not item.get("safe_to_publish") or item.get("verdict") == "reject":
            raise RuntimeError(f"Terra rejected batch item {identity}")
        results.append(
            {
                "output": final,
                "draft": drafts[identity],
                "draft_usage": draft_usage,
                "draft_call_hash": draft_hash,
                "review": item,
                "review_usage": review_usage,
                "review_call_hash": review_hash,
            }
        )
    return results


def localize_batch(
    ddb: Any,
    table: str,
    tasks: list[dict[str, Any]],
    draft_deployment: str,
    review_deployment: str,
) -> list[tuple[str, str]]:
    try:
        results = translate_batch(tasks, draft_deployment, review_deployment)
    except Exception:
        # Large structured packets occasionally come back with one omitted id,
        # especially in lower-resource languages. Split rather than discarding
        # translations for the rest of the packet; a single-row leaf reuses the
        # established individually reviewed path and preserves block markers.
        if len(tasks) == 1:
            return [
                base.localize_one(
                    ddb,
                    table,
                    tasks[0],
                    draft_deployment,
                    review_deployment,
                )
            ]
        midpoint = len(tasks) // 2
        return localize_batch(
            ddb,
            table,
            tasks[:midpoint],
            draft_deployment,
            review_deployment,
        ) + localize_batch(
            ddb,
            table,
            tasks[midpoint:],
            draft_deployment,
            review_deployment,
        )
    statuses: list[tuple[str, str]] = []
    for task, result in zip(tasks, results, strict=True):
        item = base.build_localized_item(
            task, result, draft_deployment, review_deployment
        )
        written = base.put_localized_item(ddb, table, item)
        statuses.append(("written" if written else "race_skipped", task["target_key"]))
    return statuses


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--language", action="append", default=[])
    result.add_argument("--table", default=os.getenv("CARTHA_SUMMARY_CACHE_TABLE", base.DEFAULT_TABLE))
    result.add_argument("--region", default=os.getenv("AWS_REGION", base.DEFAULT_REGION))
    result.add_argument("--model-version", default=DEFAULT_MODEL_VERSION)
    result.add_argument("--book", default="", help="Optional canonical book lane")
    result.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    result.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    result.add_argument("--limit", type=int, default=0, help="Optional task cap for smoke runs")
    result.add_argument("--dry-run", action="store_true")
    return result


def run(args: argparse.Namespace, ddb: Any | None = None) -> int:
    if args.batch_size < 1 or args.batch_size > 30:
        raise ValueError("--batch-size must be between 1 and 30")
    if args.concurrency < 1:
        raise ValueError("--concurrency must be positive")
    languages = resolve_languages(args.language)
    config = load_config()
    draft_deployment = str(config.get("draft_deployment") or "gpt-5-6-sol-atlas")
    review_deployment = str(config.get("review_deployment") or "gpt-5-6-terra-atlas")
    ddb = ddb or boto3.client("dynamodb", region_name=args.region)
    sources = scan_sources(ddb, args.table, args.model_version, args.book)
    tasks, skipped = collect_tasks(ddb, args.table, sources, languages)
    if args.limit:
        tasks = tasks[: args.limit]
    print(json.dumps({
        "table": args.table,
        "languages": [code for code, _ in languages],
        "canonical_english_rows": len(sources),
        "pending": len(tasks),
        "current_or_blocked": skipped,
        "batch_size": args.batch_size,
        "dry_run": args.dry_run,
    }), flush=True)
    if args.dry_run or not tasks:
        return 0

    azure_key()
    by_language: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in tasks:
        by_language[str(task["language"])].append(task)
    batches = [
        language_tasks[offset : offset + args.batch_size]
        for language_tasks in by_language.values()
        for offset in range(0, len(language_tasks), args.batch_size)
    ]
    totals = {"written": 0, "race_skipped": 0, "error": 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        future_map = {
            pool.submit(
                localize_batch,
                ddb,
                args.table,
                batch,
                draft_deployment,
                review_deployment,
            ): batch
            for batch in batches
        }
        for index, future in enumerate(concurrent.futures.as_completed(future_map), 1):
            batch = future_map[future]
            try:
                for status, _ in future.result():
                    totals[status] += 1
            except Exception as exc:  # noqa: BLE001
                totals["error"] += len(batch)
                print(
                    f"ERROR language={batch[0]['language']} size={len(batch)} "
                    f"first={batch[0]['target_key']}: {exc}",
                    file=sys.stderr,
                    flush=True,
                )
            if index % 10 == 0 or index == len(batches):
                print(json.dumps({"batches": f"{index}/{len(batches)}", **totals}), flush=True)
    return 1 if totals["error"] else 0


def main() -> int:
    try:
        return run(parser().parse_args())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
