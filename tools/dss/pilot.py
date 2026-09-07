#!/usr/bin/env python3
"""Reproduce evidence crops and compare independent manuscript proposals.

No OCR/model calls occur here. Agreement is a research status, not a measured
accuracy claim, and this module never writes to translation/ or reader exports.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PILOT = ROOT / "sources/dead_sea_scrolls/pilots/2026-09-02-dual-vision"
MODELS = {"openai": "gpt-5.6-sol", "anthropic": "claude-opus-5"}
CERTAINTIES = {"clear", "uncertain", "unreadable", "gap"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def repo_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("Evidence path escapes repository")
    return path


def prepare(pilot: Path) -> None:
    from PIL import Image

    for region in read_json(pilot / "regions.json")["regions"]:
        source = repo_path(region["source_path"])
        if digest(source) != region["source_sha256"]:
            raise ValueError(f"Master hash mismatch: {region['id']}")
        x, y, width, height = region["bbox_xywh"]
        with Image.open(source) as image:
            if min(x, y) < 0 or min(width, height) <= 0:
                raise ValueError("Invalid region dimensions")
            if x + width > image.width or y + height > image.height:
                raise ValueError("Region outside image bounds")
            output = repo_path(region["crop_path"])
            output.parent.mkdir(parents=True, exist_ok=True)
            image.crop((x, y, x + width, y + height)).convert("RGB").save(output)
        if digest(output) != region["crop_sha256"]:
            raise ValueError(f"Crop hash mismatch: {region['id']}")


def validate_result(result: dict, region_ids: list[str]) -> None:
    regions = result.get("regions")
    if not isinstance(regions, list):
        raise ValueError("Response has no region list")
    if [region.get("region_id") for region in regions] != region_ids:
        raise ValueError("Missing, duplicate, or reordered regions")
    for region in regions:
        lines = region.get("lines")
        if not isinstance(lines, list) or not lines:
            raise ValueError("Empty transcription is not a successful response")
        if [line.get("line_index") for line in lines] != list(range(1, len(lines) + 1)):
            raise ValueError("Line indices must be consecutive and top-to-bottom")
        for line in lines:
            if not isinstance(line.get("tokens"), list) or not line["tokens"]:
                raise ValueError("Every line needs tokens or explicit gaps")
            for token in line["tokens"]:
                if not isinstance(token.get("text"), str) or not token["text"].strip():
                    raise ValueError("Empty token")
                if token.get("certainty") not in CERTAINTIES:
                    raise ValueError("Invalid certainty label")


def normal(text: str) -> str:
    # Do not erase consonants, final forms, matres, diacritics, or gap markers.
    return unicodedata.normalize("NFC", text).strip()


def plain_hebrew_token(text: str) -> bool:
    """Conservative eligibility, not proof that any glyph is actually visible.

    Keep Hebrew vowel/cantillation marks, but refuse editorial brackets,
    generic combining uncertainty dots, prose and other annotation syntax.
    Such tokens remain in the report for adjudication rather than being
    automatically counted as clear agreement.
    """
    return any("\u05d0" <= c <= "\u05ea" for c in text) and all(
        "\u05d0" <= c <= "\u05ea"
        or ("\u0591" <= c <= "\u05c7" and unicodedata.category(c).startswith("M"))
        for c in text
    )


def compare(left: dict, right: dict) -> dict:
    report = {
        "schema_version": "1.0.0",
        "status": "awaiting-two-successful-passes",
        "interpretation": "Model agreement is not an independently measured accuracy rate.",
        "publication_action": "none; research artifacts only",
        "accepted_tokens": 0,
        "compared_tokens": 0,
        "unresolved_lines": [],
        "tokens": [],
    }
    if any(run.get("status") != "succeeded" for run in (left, right)):
        report["reason"] = "At least one provider has no successful transcription."
        return report
    if left["provider"] == right["provider"] or left["effective_model"] == right["effective_model"]:
        raise ValueError("Two independent model families are required")
    for run in (left, right):
        if run["effective_model"] != MODELS.get(run["provider"]):
            raise ValueError("Model identity does not match the requested pilot pair")
        if run.get("tool_events"):
            raise ValueError("Image-only pass used tools; inspect its input independence before comparing")
    if left["prompt_sha256"] != right["prompt_sha256"]:
        raise ValueError("Blinded inputs have different prompts")
    if left["crop_sha256"] != right["crop_sha256"]:
        raise ValueError("Blinded inputs have different image crops")
    region_ids = [region["region_id"] for region in left["result"]["regions"]]
    validate_result(left["result"], region_ids)
    validate_result(right["result"], region_ids)
    report["status"] = "compared"
    for a, b in zip(left["result"]["regions"], right["result"]["regions"]):
        rid = a["region_id"]
        if len(a["lines"]) != len(b["lines"]):
            report["unresolved_lines"].append({"region_id": rid, "reason": "line-count-disagreement"})
            continue
        for la, lb in zip(a["lines"], b["lines"]):
            if len(la["tokens"]) != len(lb["tokens"]):
                report["unresolved_lines"].append({
                    "region_id": rid, "line_index": la["line_index"],
                    "reason": "token-segmentation-disagreement",
                })
                continue
            for index, (ta, tb) in enumerate(zip(la["tokens"], lb["tokens"]), 1):
                text = normal(ta["text"])
                accepted = (
                    text == normal(tb["text"])
                    and ta["certainty"] == tb["certainty"] == "clear"
                    and plain_hebrew_token(text)
                )
                report["tokens"].append({
                    "region_id": rid, "line_index": la["line_index"], "token_index": index,
                    "left": ta, "right": tb,
                    "status": "machine-consensus-accepted" if accepted else "unresolved",
                })
                report["compared_tokens"] += 1
                report["accepted_tokens"] += int(accepted)
    return report


def validate(pilot: Path) -> None:
    regions = read_json(pilot / "regions.json")["regions"]
    ids = [region["id"] for region in regions]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate region IDs")
    registry = read_json(ROOT / "sources/dead_sea_scrolls/registry.v1.json")
    masters = {
        image["id"]: image["downloads"]["master"]
        for record in registry["records"] for image in record.get("images", [])
        if "master" in image.get("downloads", {})
    }
    for region in regions:
        master = masters[region["registry_image_id"]]
        if master["sha256"] != region["source_sha256"] or master["local_path"] != region["source_path"]:
            raise ValueError("Region is not tied to the registered master")
        if digest(repo_path(region["crop_path"])) != region["crop_sha256"]:
            raise ValueError("Crop bytes changed")
    for path in sorted((pilot / "passes").glob("*.json")):
        run = read_json(path)
        if run.get("requested_model") != MODELS.get(run.get("provider")):
            raise ValueError("Unexpected provider or requested model")
        if run["prompt_sha256"] != digest(pilot / "prompt.txt"):
            raise ValueError("Pass prompt mismatch")
        if run["crop_sha256"] != [region["crop_sha256"] for region in regions]:
            raise ValueError("Pass crop mismatch")
        if run["status"] == "succeeded":
            if run.get("effective_model") != run["requested_model"]:
                raise ValueError("Effective model mismatch")
            validate_result(run["result"], ids)
        elif run.get("result") is not None:
            raise ValueError("Failed provider must not contain a usable result")
    comparison = pilot / "comparison.json"
    if comparison.exists():
        runs = [read_json(pilot / "passes" / f"{provider}.json") for provider in MODELS]
        if read_json(comparison) != compare(*runs):
            raise ValueError("Comparison report does not match the saved passes")
    print(f"Pilot validation passed: {len(regions)} pixel-exact source crops")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "compare", "validate"])
    parser.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    args = parser.parse_args()
    if args.action == "prepare":
        prepare(args.pilot)
    elif args.action == "validate":
        validate(args.pilot)
    else:
        runs = [read_json(args.pilot / "passes" / f"{provider}.json") for provider in MODELS]
        write_json(args.pilot / "comparison.json", compare(*runs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
