#!/usr/bin/env python3
"""Write SPOB records from Codex/manual JSON drafts without calling external LLM APIs.

Input JSON format:
[
  {
    "source_path": "translation/nt/matthew/011/001.yaml",
    "simplified_text": "...",
    "translation_philosophy": "optimal-equivalence",
    "footnotes": [{"marker":"a", "text":"...", "reason":"simplification_note"}],
    "simplification_decisions": [{"pob_phrase":"...", "simplified_phrase":"...", "preserved_meaning":"...", "rationale":"..."}],
    "retained_terms": [{"term":"Messiah", "reason":"..."}],
    "source_alignment_notes": "...",
    "readability_notes": ["..."],
    "compression_notes": ["..."],
    "risk_flags": [{"risk":"...", "mitigation":"..."}]
  }
]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any

# Make sibling pipeline importable when run as a script.
TOOLS_DIR = pathlib.Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import simplified_pob_pipeline as spob  # noqa: E402

DEFAULT_PROMPT_ID = "simplified_pob_codex_manual_v1"
DEFAULT_PROMPT_SHA = spob.sha256_text(
    "Codex manual SPOB drafting: simplify POB into modern common English while preserving POB audit-layer decisions."
)


def target_for_source(source_path: pathlib.Path) -> pathlib.Path:
    return spob.SIMPLIFIED_ROOT / source_path.relative_to(spob.TRANSLATION_ROOT)


def normalize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    text = str(entry.get("simplified_text") or entry.get("text") or "").strip()
    if not text:
        raise ValueError("entry missing simplified_text")
    return {
        "simplified_text": text,
        "translation_philosophy": entry.get("translation_philosophy") or "optimal-equivalence",
        "footnotes": entry.get("footnotes") or [],
        "simplification_decisions": entry.get("simplification_decisions") or [
            {
                "preserved_meaning": "Codex manual SPOB draft preserves the controlling POB meaning while simplifying wording for modern common English.",
                "reasoning_layer_used": "POB audit trail",
                "rationale": "Manual Codex drafting pass; see base_translation and source_grounding for the controlling POB record.",
            }
        ],
        "retained_terms": entry.get("retained_terms") or [],
        "source_alignment_notes": entry.get("source_alignment_notes") or "Preserves the POB source-grounded meaning while simplifying syntax and wording.",
        "readability_notes": entry.get("readability_notes") or ["Uses clearer modern common English than the base POB wording."],
        "compression_notes": entry.get("compression_notes") or ["No central meaning is intentionally removed."],
        "risk_flags": entry.get("risk_flags") or [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON file containing an array of manual SPOB draft entries")
    parser.add_argument("--force", action="store_true", help="Overwrite existing target records")
    parser.add_argument("--model-id", default="codex-gpt-5.5-manual")
    parser.add_argument("--model-version", default="codex-gpt-5.5-codex-session")
    parser.add_argument("--deployment", default="codex-session")
    parser.add_argument("--prompt-id", default=DEFAULT_PROMPT_ID)
    args = parser.parse_args()

    input_path = pathlib.Path(args.input)
    raw_text = input_path.read_text(encoding="utf-8")
    entries = json.loads(raw_text)
    if not isinstance(entries, list):
        raise ValueError("input JSON must be an array")

    written = 0
    skipped = 0
    for i, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"entry {i}: expected object")
        rel_source = entry.get("source_path")
        if not rel_source:
            raise ValueError(f"entry {i}: missing source_path")
        source_path = (spob.REPO_ROOT / str(rel_source)).resolve()
        try:
            source_path.relative_to(spob.TRANSLATION_ROOT)
        except ValueError as exc:
            raise ValueError(f"entry {i}: source_path must be under translation/: {source_path}") from exc
        target_path = target_for_source(source_path)
        if target_path.exists() and not args.force:
            skipped += 1
            continue
        pob_record = spob.safe_load_yaml(source_path)
        tool_input = normalize_entry(entry)
        raw_entry = json.dumps(tool_input, sort_keys=True, ensure_ascii=False)
        out = spob.build_simplified_record(
            source_path=source_path,
            pob_record=pob_record,
            tool_input=tool_input,
            model_id=args.model_id,
            model_version=args.model_version,
            prompt_id=args.prompt_id,
            prompt_sha=DEFAULT_PROMPT_SHA,
            raw_output_hash=hashlib.sha256(raw_entry.encode("utf-8")).hexdigest(),
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "reasoning_tokens": 0, "estimated_cost_usd": 0.0},
            deployment=args.deployment,
        )
        spob.write_yaml_atomic(target_path, out)
        errors = spob.validate_simplified_record(target_path)
        if errors:
            raise RuntimeError(f"validation failed for {spob.rel(target_path)}: {errors}")
        print(f"wrote {spob.rel(target_path)}")
        written += 1
    print(f"manual writer complete: written={written} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
