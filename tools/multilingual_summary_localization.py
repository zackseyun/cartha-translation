#!/usr/bin/env python3
"""Localize existing English POB summary-cache output with Azure GPT-5.6.

The English cache row is the closed source for this pipeline: Sol translates
that prose, then Terra independently compares the draft with the same English
prose and returns the corrected publication text. The tool never generates a
new Bible summary or consults source verses.

Writes are language-scoped siblings of the English row. Only the translation
component of the seven-part cache identity changes, for example::

    POB|unspecified|chapter|JOHN.001|simplify|...|gpt-5.4-...
    POB-FR|unspecified|chapter|JOHN.001|simplify|...|gpt-5.4-...

The source model version remains in the identity because the localized output
is a derivative of that exact English row. Separate localization fields record
the Azure Sol and Terra models and deployments.

Examples::

    python3 tools/multilingual_summary_localization.py --language fr --limit 25 --dry-run
    python3 tools/multilingual_summary_localization.py --language fr --limit 25 --concurrency 4

The bounded default and required explicit language prevent accidental corpus-
wide work. Re-running is safe: rows matching the source output hash and
pipeline version are skipped, stale rows are refreshed, and writes use a
conditional expression to avoid racing another runner.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import pathlib
import re
import sys
import time
from decimal import Decimal
from typing import Any, Iterable, Iterator

import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from multilingual_pipeline import ROOT, azure_key, call_tool, load_config, now, write_atomic


DEFAULT_REGION = "us-west-2"
DEFAULT_TABLE = "BibleSummaryCache-alpha"
DEFAULT_LIMIT = 25
DEFAULT_CONCURRENCY = 4
SCAN_PAGE_SIZE = 100

SOURCE_TRANSLATION = "POB"
PIPELINE_VERSION = "azure_summary_localization_v1"
DRAFT_MODEL = "gpt-5.6-sol"
REVIEW_MODEL = "gpt-5.6-terra"
DRAFT_PROMPT_ID = "summary_translation_closed_source_v1"
REVIEW_PROMPT_ID = "summary_translation_review_closed_source_v1"

_DESERIALIZER = TypeDeserializer()
_SERIALIZER = TypeSerializer()
_LANGUAGE_CODE = re.compile(r"^[a-z][a-z0-9_]*$")
CACHE_CODE_OVERRIDES = {"zh_hans": "zh"}
BLOCK_ROOT = ROOT / "state" / "multilingual_summary_localization" / "blocked"


DRAFT_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_summary_translation",
        "strict": True,
        "description": "Submit a faithful translation of the supplied English summary.",
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "required": ["translation"],
            "properties": {"translation": {"type": "string"}},
        },
    },
}

REVIEW_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_summary_translation_review",
        "strict": True,
        "description": "Submit an independent review and corrected final translation.",
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "verdict",
                "final_translation",
                "issues",
                "review_summary",
                "safe_to_publish",
            ],
            "properties": {
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
    },
}


def output_hash(value: str) -> str:
    """Return the stable hash used to decide whether a target row is current."""

    return hashlib.sha256(value.strip().encode("utf-8")).hexdigest()


def language_translation(code: str) -> str:
    """Return the established language-scoped POB translation identity."""

    normalized = str(code or "").strip().lower().replace("-", "_")
    if not _LANGUAGE_CODE.fullmatch(normalized):
        raise ValueError(f"invalid language code: {code!r}")
    normalized = CACHE_CODE_OVERRIDES.get(normalized, normalized)
    return f"POB-{normalized.upper()}"


def localized_summary_key(source_key: str, language: str) -> str:
    """Clone an English cache identity with only its translation token changed."""

    parts = str(source_key or "").split("|")
    if len(parts) != 7 or parts[0].strip().upper() != SOURCE_TRANSLATION:
        raise ValueError(f"invalid English POB summary key: {source_key!r}")
    parts[0] = language_translation(language)
    return "|".join(parts)


def _plain_dynamodb_value(value: Any) -> Any:
    """Convert TypeDeserializer's Decimals into JSON-safe Python values."""

    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else str(value)
    if isinstance(value, dict):
        return {key: _plain_dynamodb_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain_dynamodb_value(item) for item in value]
    return value


def deserialize_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        key: _plain_dynamodb_value(_DESERIALIZER.deserialize(value))
        for key, value in item.items()
    }


def _dynamodb_value(value: Any) -> Any:
    """Convert API-derived numbers into values accepted by TypeSerializer."""

    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, dict):
        return {key: _dynamodb_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_dynamodb_value(item) for item in value]
    return value


def serialize_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        key: _SERIALIZER.serialize(_dynamodb_value(value))
        for key, value in item.items()
    }


def configured_languages(values: Iterable[str]) -> list[tuple[str, dict[str, Any]]]:
    """Resolve explicit target codes against multilingual_languages.yaml."""

    requested: list[str] = []
    for value in values:
        for raw_code in str(value).split(","):
            code = raw_code.strip().lower().replace("-", "_")
            if code and code not in requested:
                requested.append(code)
    if not requested:
        raise ValueError("at least one explicit --language is required")
    if "all" in requested:
        raise ValueError("--language all is intentionally unsupported; select bounded lanes")

    languages = load_config()["languages"]
    invalid = [code for code in requested if code == "en" or code not in languages]
    if invalid:
        raise ValueError(f"unknown/non-target languages: {', '.join(invalid)}")
    return [(code, dict(languages[code])) for code in requested]


def _source_row_valid(row: dict[str, Any]) -> bool:
    if str(row.get("translation") or "").upper() != SOURCE_TRANSLATION:
        return False
    if not str(row.get("output") or "").strip():
        return False
    try:
        localized_summary_key(str(row.get("summary_key") or ""), "fr")
    except ValueError:
        return False
    return True


def scan_english_pages(ddb: Any, table: str) -> Iterator[list[dict[str, Any]]]:
    """Yield filtered, deserialized English POB rows one scan page at a time."""

    request: dict[str, Any] = {
        "TableName": table,
        "FilterExpression": "#translation = :source AND attribute_exists(#output)",
        "ExpressionAttributeNames": {
            "#translation": "translation",
            "#scope": "scope",
            "#book": "book",
            "#tool": "tool",
            "#output": "output",
        },
        "ExpressionAttributeValues": {":source": {"S": SOURCE_TRANSLATION}},
        "ProjectionExpression": (
            "summary_key,#translation,translation_version,#scope,#book,chapter,"
            "#tool,#output,prompt_version,model_version,source_hash,verse_count,"
            "generated_at,updated_at"
        ),
        "Limit": SCAN_PAGE_SIZE,
    }
    while True:
        response = ddb.scan(**request)
        rows = [deserialize_item(item) for item in response.get("Items", [])]
        yield [row for row in rows if _source_row_valid(row)]
        cursor = response.get("LastEvaluatedKey")
        if not cursor:
            return
        request["ExclusiveStartKey"] = cursor


def task_for(
    source: dict[str, Any], language: str, language_spec: dict[str, Any]
) -> dict[str, Any]:
    source_text = str(source["output"]).strip()
    return {
        "source": source,
        "language": language,
        "language_spec": language_spec,
        "target_key": localized_summary_key(str(source["summary_key"]), language),
        "source_output_hash": output_hash(source_text),
    }


def block_path(task: dict[str, Any]) -> pathlib.Path:
    """Return a stable local marker for one source-version/language pair."""

    identity = f"{task['target_key']}|{task['source_output_hash']}"
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return BLOCK_ROOT / str(task["language"]) / f"{digest}.yaml"


def task_is_blocked(task: dict[str, Any]) -> bool:
    return block_path(task).exists()


def is_content_filter_error(exc: Exception) -> bool:
    rendered = str(exc).lower()
    return "content_filter" in rendered or "responsibleaipolicyviolation" in rendered


def park_content_filter_block(task: dict[str, Any], exc: Exception) -> None:
    path = block_path(task)
    write_atomic(
        path,
        {
            "status": "content_filter_blocked",
            "target_key": task["target_key"],
            "source_key": task["source"]["summary_key"],
            "language": task["language"],
            "source_output_hash": task["source_output_hash"],
            "blocked_at": now(),
            "error": str(exc)[:1000],
        },
    )


def batch_get_targets(ddb: Any, table: str, keys: Iterable[str]) -> dict[str, dict[str, Any]]:
    """Fetch target rows in batches, retrying DynamoDB's unprocessed keys."""

    ordered_keys = list(dict.fromkeys(keys))
    found: dict[str, dict[str, Any]] = {}
    for offset in range(0, len(ordered_keys), 100):
        pending = [{"summary_key": {"S": key}} for key in ordered_keys[offset : offset + 100]]
        attempts = 0
        while pending:
            response = ddb.batch_get_item(
                RequestItems={
                    table: {
                        "Keys": pending,
                        "ConsistentRead": True,
                        "ProjectionExpression": (
                            "summary_key,#translation,#language,source_hash,"
                            "localized_from_summary_key,localized_from_output_hash,"
                            "localization_pipeline_version"
                        ),
                        "ExpressionAttributeNames": {
                            "#translation": "translation",
                            "#language": "language",
                        },
                    }
                }
            )
            for raw_item in response.get("Responses", {}).get(table, []):
                item = deserialize_item(raw_item)
                found[str(item["summary_key"])] = item
            pending = (
                response.get("UnprocessedKeys", {})
                .get(table, {})
                .get("Keys", [])
            )
            if pending:
                attempts += 1
                if attempts >= 7:
                    raise RuntimeError("DynamoDB left target cache keys unprocessed")
                time.sleep(min(1.0, 0.05 * (2**attempts)))
    return found


def existing_matches(existing: dict[str, Any] | None, task: dict[str, Any]) -> bool:
    """True only when a target row derives from this exact English output."""

    if not existing:
        return False
    source = task["source"]
    return all(
        (
            str(existing.get("translation") or "")
            == language_translation(str(task["language"])),
            str(existing.get("language") or "") == str(task["language"]),
            str(existing.get("source_hash") or "")
            == str(source.get("source_hash") or ""),
            str(existing.get("localized_from_summary_key") or "")
            == str(source.get("summary_key") or ""),
            str(existing.get("localized_from_output_hash") or "")
            == str(task["source_output_hash"]),
            str(existing.get("localization_pipeline_version") or "")
            == PIPELINE_VERSION,
        )
    )


def collect_pending_tasks(
    ddb: Any,
    table: str,
    languages: list[tuple[str, dict[str, Any]]],
    limit: int,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Scan past completed rows until `limit` resumable work items are found."""

    if limit < 1:
        raise ValueError("--limit must be at least 1")
    tasks: list[dict[str, Any]] = []
    stats = {
        "english_rows_scanned": 0,
        "matching_rows_skipped": 0,
        "content_filter_blocks_skipped": 0,
    }
    for page in scan_english_pages(ddb, table):
        stats["english_rows_scanned"] += len(page)
        candidates = [
            task_for(source, code, spec)
            for source in page
            for code, spec in languages
        ]
        existing = batch_get_targets(
            ddb, table, (task["target_key"] for task in candidates)
        )
        for task in candidates:
            if task_is_blocked(task):
                stats["content_filter_blocks_skipped"] += 1
                continue
            if existing_matches(existing.get(task["target_key"]), task):
                stats["matching_rows_skipped"] += 1
                continue
            tasks.append(task)
            if len(tasks) >= limit:
                return tasks, stats
    return tasks, stats


def _draft_system(task: dict[str, Any]) -> str:
    spec = task["language_spec"]
    return f"""You are an exacting professional translator into {spec['name']} ({spec['native_name']}).
Target variant: {spec['variant']}.

Translate only the supplied English POB summary. The English summary is a closed and authoritative source for this task. Preserve every claim, qualification, relationship, citation, and degree of certainty already present. Do not consult, reconstruct, explain, improve, harmonize, or expand the underlying biblical or historical passage. Do not add exegesis, devotional application, background knowledge, headings, notes, or facts. Do not remove difficult or disputed claims. Use natural, dignified, current target-language prose while keeping the same paragraph structure when practical. Return the complete translation through the required tool."""


def _review_system(task: dict[str, Any]) -> str:
    spec = task["language_spec"]
    return f"""You are the independent senior {spec['name']} ({spec['native_name']}) translation reviewer.
Target variant: {spec['variant']}.

Compare the candidate translation sentence by sentence with the supplied English POB summary. The English prose is the only source of truth. Correct omissions, additions, altered certainty, mistranslations, awkward language, names, and references. Do not use outside Bible knowledge and do not introduce new exegesis, interpretation, historical detail, devotional application, headings, or notes. Always return the complete corrected target-language summary, even when approving the draft. Set safe_to_publish=false only when a faithful correction cannot be completed from the supplied English prose."""


def translate_and_review(
    task: dict[str, Any], draft_deployment: str, review_deployment: str
) -> dict[str, Any]:
    """Run the closed-source Sol draft and independent Terra correction."""

    source = task["source"]
    source_payload = {
        "language": task["language"],
        "book": source.get("book"),
        "scope": source.get("scope"),
        "chapter": source.get("chapter"),
        "tool": source.get("tool"),
        "english_summary": str(source["output"]).strip(),
    }
    draft, draft_usage, draft_call_hash = call_tool(
        deployment=draft_deployment,
        system=_draft_system(task),
        user=json.dumps(source_payload, ensure_ascii=False),
        tool=DRAFT_TOOL,
        name="submit_summary_translation",
        max_tokens=5000,
    )
    draft_text = str(draft.get("translation") or "").strip()
    if not draft_text:
        raise RuntimeError("Sol returned an empty summary translation")

    review_payload = {
        **source_payload,
        "candidate_translation": draft_text,
    }
    review, review_usage, review_call_hash = call_tool(
        deployment=review_deployment,
        system=_review_system(task),
        user=json.dumps(review_payload, ensure_ascii=False),
        tool=REVIEW_TOOL,
        name="submit_summary_translation_review",
        max_tokens=6000,
    )
    final_text = str(review.get("final_translation") or "").strip()
    if not final_text:
        raise RuntimeError("Terra returned an empty final summary translation")
    if not review.get("safe_to_publish") or review.get("verdict") == "reject":
        raise RuntimeError(
            "Terra rejected the localization: "
            + str(review.get("review_summary") or "no review summary")
        )
    return {
        "output": final_text,
        "draft": draft,
        "draft_usage": draft_usage,
        "draft_call_hash": draft_call_hash,
        "review": review,
        "review_usage": review_usage,
        "review_call_hash": review_call_hash,
    }


def build_localized_item(
    task: dict[str, Any],
    result: dict[str, Any],
    draft_deployment: str,
    review_deployment: str,
) -> dict[str, Any]:
    """Build a target row while preserving the source summary cache contract."""

    source = task["source"]
    review = result["review"]
    timestamp = now()
    item: dict[str, Any] = {
        "summary_key": task["target_key"],
        "translation": language_translation(str(task["language"])),
        "translation_version": str(source.get("translation_version") or "unspecified"),
        "scope": str(source.get("scope") or "book"),
        "book": str(source.get("book") or ""),
        "tool": str(source.get("tool") or ""),
        "output": result["output"],
        "prompt_version": str(source.get("prompt_version") or "bible_shared_summary_v1"),
        "model_version": str(source.get("model_version") or "unspecified"),
        "source_hash": str(source.get("source_hash") or ""),
        "verse_count": int(source.get("verse_count") or 0),
        "generated_at": timestamp,
        "updated_at": timestamp,
        "language": task["language"],
        "language_name": str(task["language_spec"].get("name") or task["language"]),
        "localized_from_summary_key": str(source["summary_key"]),
        "localized_from_translation": SOURCE_TRANSLATION,
        "localized_from_model_version": str(source.get("model_version") or ""),
        "localized_from_output_hash": task["source_output_hash"],
        "localized_from_generated_at": str(source.get("generated_at") or ""),
        "localized_output_hash": output_hash(result["output"]),
        "localization_provider": "azure_openai",
        "localization_pipeline_version": PIPELINE_VERSION,
        "localization_draft_model": DRAFT_MODEL,
        "localization_draft_deployment": draft_deployment,
        "localization_draft_prompt_id": DRAFT_PROMPT_ID,
        "localization_draft_call_hash": result["draft_call_hash"],
        "localization_draft_usage": result.get("draft_usage") or {},
        "localization_review_model": REVIEW_MODEL,
        "localization_review_deployment": review_deployment,
        "localization_review_prompt_id": REVIEW_PROMPT_ID,
        "localization_review_call_hash": result["review_call_hash"],
        "localization_review_usage": result.get("review_usage") or {},
        "localization_review_verdict": str(review.get("verdict") or ""),
        "localization_review_summary": str(review.get("review_summary") or ""),
        "localization_review_issues": [str(issue) for issue in review.get("issues") or []],
    }
    if source.get("chapter") is not None:
        item["chapter"] = int(source["chapter"])
    return item


def put_localized_item(ddb: Any, table: str, item: dict[str, Any]) -> bool:
    """Conditionally write a stale/missing target; return False on a race."""

    try:
        ddb.put_item(
            TableName=table,
            Item=serialize_item(item),
            ConditionExpression=(
                "attribute_not_exists(#key) OR "
                "attribute_not_exists(#language) OR #language <> :language OR "
                "attribute_not_exists(#source_hash) OR #source_hash <> :source_hash OR "
                "attribute_not_exists(#source_key) OR #source_key <> :source_key OR "
                "attribute_not_exists(#source_output_hash) OR "
                "#source_output_hash <> :source_output_hash OR "
                "attribute_not_exists(#pipeline) OR #pipeline <> :pipeline"
            ),
            ExpressionAttributeNames={
                "#key": "summary_key",
                "#language": "language",
                "#source_hash": "source_hash",
                "#source_key": "localized_from_summary_key",
                "#source_output_hash": "localized_from_output_hash",
                "#pipeline": "localization_pipeline_version",
            },
            ExpressionAttributeValues={
                ":language": {"S": item["language"]},
                ":source_hash": {"S": item["source_hash"]},
                ":source_key": {"S": item["localized_from_summary_key"]},
                ":source_output_hash": {"S": item["localized_from_output_hash"]},
                ":pipeline": {"S": PIPELINE_VERSION},
            },
        )
        return True
    except Exception as exc:  # botocore errors expose a stable response code
        code = getattr(exc, "response", {}).get("Error", {}).get("Code")
        if code == "ConditionalCheckFailedException":
            return False
        raise


def localize_one(
    ddb: Any,
    table: str,
    task: dict[str, Any],
    draft_deployment: str,
    review_deployment: str,
) -> tuple[str, str]:
    result = translate_and_review(task, draft_deployment, review_deployment)
    item = build_localized_item(task, result, draft_deployment, review_deployment)
    if put_localized_item(ddb, table, item):
        return "written", str(task["target_key"])
    return "race_skipped", str(task["target_key"])


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--language",
        action="append",
        required=True,
        help="Configured target language code; repeat or comma-separate for bounded lanes.",
    )
    result.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum localization tasks this run (default: {DEFAULT_LIMIT}).",
    )
    result.add_argument(
        "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        help=f"Parallel Sol/Terra task pairs (default: {DEFAULT_CONCURRENCY}).",
    )
    result.add_argument(
        "--dry-run",
        action="store_true",
        help="Read cache state and print pending identities without Azure calls or writes.",
    )
    result.add_argument(
        "--table",
        default=os.environ.get("CARTHA_SUMMARY_CACHE_TABLE", DEFAULT_TABLE),
    )
    result.add_argument(
        "--region",
        default=os.environ.get("AWS_REGION", DEFAULT_REGION),
    )
    return result


def run(args: argparse.Namespace, ddb: Any | None = None) -> int:
    if args.limit < 1:
        raise ValueError("--limit must be at least 1")
    if args.concurrency < 1:
        raise ValueError("--concurrency must be at least 1")
    languages = configured_languages(args.language)
    config = load_config()
    draft_deployment = str(config.get("draft_deployment") or "gpt-5-6-sol-atlas")
    review_deployment = str(config.get("review_deployment") or "gpt-5-6-terra-atlas")
    ddb = ddb or boto3.client("dynamodb", region_name=args.region)

    tasks, discovery = collect_pending_tasks(ddb, args.table, languages, args.limit)
    print(
        json.dumps(
            {
                "table": args.table,
                "region": args.region,
                "languages": [code for code, _ in languages],
                "limit": args.limit,
                "pending": len(tasks),
                **discovery,
                "dry_run": bool(args.dry_run),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    if args.dry_run:
        for task in tasks:
            source = task["source"]
            print(
                json.dumps(
                    {
                        "target_key": task["target_key"],
                        "source_key": source["summary_key"],
                        "language": task["language"],
                        "scope": source.get("scope"),
                        "book": source.get("book"),
                        "chapter": source.get("chapter"),
                        "tool": source.get("tool"),
                    },
                    ensure_ascii=False,
                )
            )
        return 0
    if not tasks:
        return 0

    # Resolve and cache Azure credentials before worker threads begin.
    azure_key()
    totals = {"written": 0, "race_skipped": 0, "blocked": 0, "error": 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = {
            pool.submit(
                localize_one,
                ddb,
                args.table,
                task,
                draft_deployment,
                review_deployment,
            ): task
            for task in tasks
        }
        for future in concurrent.futures.as_completed(futures):
            task = futures[future]
            try:
                status, key = future.result()
                totals[status] += 1
                print(f"{status:12} {key}", flush=True)
            except Exception as exc:  # noqa: BLE001
                if is_content_filter_error(exc):
                    park_content_filter_block(task, exc)
                    totals["blocked"] += 1
                    print(
                        f"blocked      {task['target_key']}",
                        file=sys.stderr,
                        flush=True,
                    )
                    continue
                totals["error"] += 1
                print(f"ERROR        {task['target_key']}: {exc}", file=sys.stderr, flush=True)
    print(json.dumps(totals, sort_keys=True), flush=True)
    return 1 if totals["error"] else 0


def main() -> int:
    args = parser().parse_args()
    try:
        return run(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
