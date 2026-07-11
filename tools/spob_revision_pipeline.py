#!/usr/bin/env python3
"""Revise SPOB drafts from an auditable reviewer verdict."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import pathlib
import sys
import tempfile
from typing import Any

import simplified_pob_pipeline as pipeline


ROOT = pathlib.Path(__file__).resolve().parent.parent
SIMPLIFIED_ROOT = ROOT / "translation_simplified"
REVIEW_ROOT = ROOT / "state" / "spob_reviews"

REVISION_SYSTEM_PROMPT = pipeline.DRAFT_SYSTEM_PROMPT + """

# Revision pass

You are revising an existing SPOB draft after an independent grounding review.
Resolve every valid issue in the review. Preserve good understanding-first
clarifications that the reviewer approved. Do not retreat toward POB merely for
verbal similarity, and do not blindly copy a recommendation when its footnotes or
format conflict with the structured schema. Return a complete replacement draft.
"""


def review_files(args: argparse.Namespace) -> list[pathlib.Path]:
    model_dir = args.review_model.replace("/", "_").replace(".", "_")
    paths = sorted((REVIEW_ROOT / model_dir).rglob("*.json"))
    selected: list[pathlib.Path] = []
    wanted_books = {b.lower().replace(" ", "_").replace("-", "_") for b in (args.book or [])}
    excluded_references = {str(ref).strip().lower() for ref in (args.exclude_reference or [])}
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if ((payload.get("review") or {}).get("verdict")) not in {"revise", "block"}:
            continue
        if str(payload.get("reference") or "").strip().lower() in excluded_references:
            continue
        spob_path = ROOT / str(payload.get("spob_path") or "")
        if not spob_path.exists():
            continue
        if wanted_books and spob_path.parents[1].name.lower() not in wanted_books:
            continue
        review_hash = str(payload.get("output_hash") or "")
        current = pipeline.safe_load_yaml(spob_path)
        applied = {
            str(item.get("review_output_hash") or "")
            for item in (current.get("spob_revision_history") or [])
            if isinstance(item, dict)
        }
        if review_hash in applied and not args.force:
            continue
        selected.append(path)
    return selected[: args.limit or None]


def revise_one(review_path: pathlib.Path, args: argparse.Namespace) -> dict[str, Any]:
    review_payload = json.loads(review_path.read_text(encoding="utf-8"))
    spob_path = ROOT / review_payload["spob_path"]
    existing = pipeline.safe_load_yaml(spob_path)
    source_path = ROOT / str(
        ((existing.get("source_grounding") or {}).get("pob_path"))
        or ((existing.get("base_translation") or {}).get("yaml_path"))
    )
    pob = pipeline.safe_load_yaml(source_path)
    base_prompt = pipeline.build_draft_user_prompt(source_path, pob)
    prompt = f"""{base_prompt}

# Existing SPOB draft

{pipeline.compact_yaml({
    "translation": existing.get("translation"),
    "simplification_decisions": existing.get("simplification_decisions") or [],
    "interpretive_expansions": existing.get("interpretive_expansions") or [],
    "translation_notes": existing.get("translation_notes") or {},
})}

# Independent grounding review

{pipeline.compact_yaml(review_payload.get("review") or {})}

Return a complete corrected submit_simplified_draft call. Fix the review issues
while retaining every warranted clarity improvement.
"""
    tool_input, model_version, usage, raw = pipeline.call_azure_tool(
        system_prompt=REVISION_SYSTEM_PROMPT,
        user_prompt=prompt,
        tool=pipeline.DRAFT_TOOL,
        tool_name="submit_simplified_draft",
        deployment=args.deployment,
        model_id=args.model,
        max_completion_tokens=args.max_completion_tokens,
        timeout_seconds=args.timeout_seconds,
        retries=args.retries,
    )
    new_record = pipeline.build_simplified_record(
        source_path=source_path,
        pob_record=pob,
        tool_input=tool_input,
        model_id=args.model,
        model_version=model_version,
        prompt_id="simplified_pob_grounding_revision_v1",
        prompt_sha=pipeline.sha256_text(REVISION_SYSTEM_PROMPT + "\n\n---\n\n" + prompt),
        raw_output_hash=pipeline.sha256_text(raw),
        usage=usage,
        deployment=args.deployment,
    )
    history = list(existing.get("spob_revision_history") or [])
    history.append(
        {
            "timestamp": pipeline.utc_now(),
            "previous_text": ((existing.get("translation") or {}).get("text")),
            "previous_model": ((existing.get("ai_draft") or {}).get("model_id")),
            "reviewer_model": ((review_payload.get("reviewer") or {}).get("model")),
            "review_verdict": ((review_payload.get("review") or {}).get("verdict")),
            "review_output_hash": review_payload.get("output_hash"),
            "review_summary": ((review_payload.get("review") or {}).get("review_summary")),
        }
    )
    new_record["spob_revision_history"] = history
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=spob_path.parent,
        prefix=f".{spob_path.name}.review-",
        suffix=".tmp",
        delete=False,
    ) as handle:
        yaml_text = pipeline.yaml.safe_dump(
            new_record,
            sort_keys=False,
            allow_unicode=True,
            width=1000,
        )
        handle.write(yaml_text)
        candidate_path = pathlib.Path(handle.name)
    errors = pipeline.validate_simplified_record(candidate_path)
    if errors:
        candidate_path.unlink(missing_ok=True)
        raise RuntimeError(f"revised record failed validation: {errors}")
    candidate_path.replace(spob_path)
    return {"reference": new_record.get("reference"), "path": str(spob_path), "text": ((new_record.get("translation") or {}).get("text"))}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", action="append")
    parser.add_argument("--exclude-reference", action="append")
    parser.add_argument("--review-model", default="gpt-5.6-terra")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--deployment", default="gpt-5-6-sol-atlas")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--max-completion-tokens", type=int, default=3000)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    paths = review_files(args)
    failures: list[str] = []
    revised = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_paths = {executor.submit(revise_one, path, args): path for path in paths}
        for future in concurrent.futures.as_completed(future_paths):
            path = future_paths[future]
            try:
                result = future.result()
                revised += 1
                print(f"revised {result['reference']}: {result['text']}", flush=True)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{path}: {type(exc).__name__}: {exc}")
                print(f"FAILED {path}: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
    print(json.dumps({"selected": len(paths), "revised": revised, "failed": len(failures)}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
