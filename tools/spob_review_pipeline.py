#!/usr/bin/env python3
"""Review SPOB drafts for clarity, faithfulness, and interpretive overreach."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import pathlib
import sys
from typing import Any

import yaml

import simplified_pob_pipeline as draft_pipeline


ROOT = pathlib.Path(__file__).resolve().parent.parent
SIMPLIFIED_ROOT = ROOT / "translation_simplified"
REVIEW_ROOT = ROOT / "state" / "spob_reviews"

REVIEW_SYSTEM_PROMPT = """You are reviewing a Simplified People's Open Bible (SPOB) draft.

SPOB is an understanding-first derivative of POB. Do not reject a draft merely
because it is less literal or more explicit than POB. Approve a contextual
clarification when source text, immediate context, and POB's reasoning establish
it. Reject or revise it when it inserts a teacher's doctrine, collapses a live
ambiguity, merges distinct source ideas, weakens the passage, or states a merely
possible application as the text's meaning.

Use this authority order: source/textual evidence; immediate context; POB audit
trail; broader canonical usage; external interpreters only as non-controlling
witnesses. No named teacher or interpretive tradition can control the main text.

Judge both sides: flag unsupported expansion, but also flag under-simplification
that leaves modern readers unable to understand the actual meaning.

Call submit_spob_review exactly once and output nothing else.
"""

REVIEW_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "submit_spob_review",
        "description": "Submit an auditable SPOB doctrine and readability review.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "verdict",
                "faithfulness_score",
                "clarity_score",
                "doctrine_score",
                "issues",
                "recommended_text",
                "review_summary",
            ],
            "properties": {
                "verdict": {"type": "string", "enum": ["approve", "revise", "block"]},
                "faithfulness_score": {"type": "integer", "minimum": 1, "maximum": 5},
                "clarity_score": {"type": "integer", "minimum": 1, "maximum": 5},
                "doctrine_score": {"type": "integer", "minimum": 1, "maximum": 5},
                "issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["type", "severity", "description", "evidence"],
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": [
                                    "meaning_change",
                                    "unsupported_expansion",
                                    "under_simplified",
                                    "lost_ambiguity",
                                    "merged_ideas",
                                    "named_interpreter_reliance",
                                    "style",
                                    "footnote",
                                ],
                            },
                            "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                            "description": {"type": "string"},
                            "evidence": {"type": "array", "items": {"type": "string"}},
                        },
                        "additionalProperties": False,
                    },
                },
                "recommended_text": {"type": "string"},
                "review_summary": {"type": "string"},
            },
            "additionalProperties": False,
        },
    },
}


def source_path_for(record: dict[str, Any]) -> pathlib.Path:
    rel = ((record.get("source_grounding") or {}).get("pob_path") or
           (record.get("base_translation") or {}).get("yaml_path"))
    if not rel:
        raise ValueError("SPOB record has no POB path")
    return ROOT / str(rel)


def review_prompt(spob_path: pathlib.Path, spob_record: dict[str, Any]) -> str:
    pob_path = source_path_for(spob_record)
    pob = draft_pipeline.safe_load_yaml(pob_path)
    context = {
        "reference": spob_record.get("reference"),
        "pob": {
            "text": ((pob.get("translation") or {}).get("text")),
            "footnotes": ((pob.get("translation") or {}).get("footnotes") or []),
            "lexical_decisions": pob.get("lexical_decisions") or [],
            "theological_decisions": pob.get("theological_decisions") or [],
        },
        "spob": {
            "text": ((spob_record.get("translation") or {}).get("text")),
            "footnotes": ((spob_record.get("translation") or {}).get("footnotes") or []),
            "simplification_decisions": spob_record.get("simplification_decisions") or [],
            "interpretive_expansions": spob_record.get("interpretive_expansions") or [],
            "retained_terms": spob_record.get("retained_terms") or [],
            "risk_flags": ((spob_record.get("translation_notes") or {}).get("risk_flags") or []),
        },
    }
    return f"""Review this SPOB draft under SPOB_DOCTRINE.md.

{draft_pipeline.compact_yaml(context)}

Approve only if the text is both meaningfully clearer than POB and warranted by
the source/context/audit trail. If revision is needed, recommended_text must be a
complete publication-ready replacement. If approved, repeat the current SPOB text
as recommended_text.
"""


def review_path_for(spob_path: pathlib.Path, model: str) -> pathlib.Path:
    model_dir = model.replace("/", "_").replace(".", "_")
    return REVIEW_ROOT / model_dir / spob_path.relative_to(SIMPLIFIED_ROOT).with_suffix(".json")


def review_one(spob_path: pathlib.Path, args: argparse.Namespace) -> dict[str, Any]:
    record = draft_pipeline.safe_load_yaml(spob_path)
    out_path = review_path_for(spob_path, args.model)
    if out_path.exists() and not args.force:
        return json.loads(out_path.read_text(encoding="utf-8"))
    result, model_version, usage, raw = draft_pipeline.call_azure_tool(
        system_prompt=REVIEW_SYSTEM_PROMPT,
        user_prompt=review_prompt(spob_path, record),
        tool=REVIEW_TOOL,
        tool_name="submit_spob_review",
        deployment=args.deployment,
        model_id=args.model,
        max_completion_tokens=args.max_completion_tokens,
        timeout_seconds=args.timeout_seconds,
        retries=args.retries,
    )
    output = {
        "reference": record.get("reference"),
        "spob_path": str(spob_path.relative_to(ROOT)),
        "reviewer": {"model": args.model, "model_version": model_version, "deployment": args.deployment},
        "review": result,
        "usage": draft_pipeline.normalize_usage(usage, args.model),
        "output_hash": draft_pipeline.sha256_text(raw),
        "timestamp": draft_pipeline.utc_now(),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def write_content_filter_block(
    spob_path: pathlib.Path,
    args: argparse.Namespace,
    error: Exception,
) -> dict[str, Any]:
    """Record a non-substantive block when Azure cannot inspect a passage."""
    record = draft_pipeline.safe_load_yaml(spob_path)
    current_text = str(((record.get("translation") or {}).get("text")) or "")
    out_path = review_path_for(spob_path, args.model)
    output = {
        "reference": record.get("reference"),
        "spob_path": str(spob_path.relative_to(ROOT)),
        "reviewer": {
            "model": args.model,
            "model_version": "azure-content-policy-fallback",
            "deployment": args.deployment,
        },
        "review": {
            "verdict": "block",
            "faithfulness_score": 1,
            "clarity_score": 1,
            "doctrine_score": 1,
            "issues": [
                {
                    "type": "meaning_change",
                    "severity": "high",
                    "description": (
                        "Azure content policy prevented Terra from reviewing this passage; "
                        "the current SPOB text requires explicit editorial adjudication."
                    ),
                    "evidence": ["ResponsibleAIPolicyViolation", str(error)[:500]],
                }
            ],
            "recommended_text": current_text,
            "review_summary": (
                "No substantive automated verdict was produced. Preserve the current text "
                "unchanged until a human/editorial grounding review resolves this block."
            ),
        },
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "reasoning_tokens": 0,
            "estimated_cost_usd": 0.0,
        },
        "output_hash": draft_pipeline.sha256_text(str(error)),
        "timestamp": draft_pipeline.utc_now(),
        "review_status": "azure_content_filter_editorial_block",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def selected_paths(args: argparse.Namespace) -> list[pathlib.Path]:
    paths = sorted(SIMPLIFIED_ROOT.rglob("*.yaml"))
    if args.book:
        wanted = {b.lower().replace(" ", "_").replace("-", "_") for b in args.book}
        paths = [p for p in paths if p.parents[1].name.lower() in wanted]
    if args.chapter:
        wanted_chapters = {f"{chapter:03}" for chapter in args.chapter}
        paths = [p for p in paths if p.parent.name in wanted_chapters]
    if args.only_expansions:
        paths = [p for p in paths if (draft_pipeline.safe_load_yaml(p).get("interpretive_expansions") or [])]
    if args.revised_after:
        paths = [
            p for p in paths
            if any(
                str(entry.get("timestamp") or "") >= args.revised_after
                for entry in (draft_pipeline.safe_load_yaml(p).get("spob_revision_history") or [])
                if isinstance(entry, dict)
            )
        ]
    # Apply the wave limit to records that still need this model's review.
    # Previously, an existing reviewed prefix consumed every limited wave,
    # preventing later records from ever being selected unless the full corpus
    # was queued at once.
    if not args.force:
        paths = [p for p in paths if not review_path_for(p, args.model).exists()]
    return paths[: args.limit or None]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", action="append")
    parser.add_argument("--chapter", action="append", type=int)
    parser.add_argument("--only-expansions", action="store_true")
    parser.add_argument(
        "--revised-after",
        help="review only records with an SPOB revision-history timestamp at or after this ISO-8601 value",
    )
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--deployment", default="gpt-5-6-terra-atlas")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-completion-tokens", type=int, default=1800)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    paths = selected_paths(args)
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_paths = {executor.submit(review_one, path, args): path for path in paths}
        for future in concurrent.futures.as_completed(future_paths):
            path = future_paths[future]
            try:
                result = future.result()
                results.append(result)
                print(f"reviewed {result['reference']}: {result['review']['verdict']}", flush=True)
            except Exception as exc:  # noqa: BLE001
                if "content_filter" in str(exc) or "ResponsibleAIPolicyViolation" in str(exc):
                    result = write_content_filter_block(path, args, exc)
                    results.append(result)
                    print(f"reviewed {result['reference']}: block (content policy)", flush=True)
                    continue
                failures.append(f"{path}: {type(exc).__name__}: {exc}")
                print(f"FAILED {path}: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)

    counts = {"approve": 0, "revise": 0, "block": 0}
    for result in results:
        verdict = ((result.get("review") or {}).get("verdict"))
        if verdict in counts:
            counts[verdict] += 1
    print(json.dumps({"selected": len(paths), "reviewed": len(results), "failed": len(failures), "verdicts": counts}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
