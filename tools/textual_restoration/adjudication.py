#!/usr/bin/env python3
"""Validate editorial records and render an apparatus; never select or publish text."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "sources/textual_restoration/decisions/hebrew_pilot.v1.json"
REPORT = ROOT / "docs/HEBREW_PILOT_ADJUDICATION.md"
NT_DATA = ROOT / "sources/textual_restoration/decisions/nt_pilot.v1.json"
NT_REPORT = ROOT / "docs/NT_PILOT_ADJUDICATION.md"


def validate(data: dict, check_current_baseline: bool = False) -> list[str]:
    """Structural/evidence-boundary checks, not a scholarly correctness score."""
    errors: list[str] = []
    policy = data.get("policy", {})
    if policy.get("chronology") != "modest-preference":
        errors.append("chronology must be a modest preference, not an override")
    for key in ("majority_vote", "model_agreement_is_historical_independence",
                "automatic_canonical_writes"):
        if policy.get(key) is not False:
            errors.append(f"policy.{key} must be false")
    sources = data.get("sources", [])
    source_ids = [s.get("id") for s in sources]
    if not source_ids or None in source_ids or len(set(source_ids)) != len(source_ids):
        errors.append("source IDs must be nonempty and unique")
    for source in sources:
        url = urlparse(source.get("url", ""))
        if url.scheme not in ("http", "https") or not url.netloc:
            errors.append(f"{source.get('id')}: missing source URL")
        if not source.get("locator"):
            errors.append(f"{source.get('id')}: missing source locator")
    units = data.get("units", [])
    unit_ids = [u.get("id") for u in units]
    if not units or None in unit_ids or len(set(unit_ids)) != len(unit_ids):
        errors.append("unit IDs must be nonempty and unique")
    for unit in units:
        uid = unit.get("id")
        if unit.get("generated_images_used") is not False:
            errors.append(f"{uid}: generated images cannot support adjudication")
        if unit.get("fresh_restoration") is not False or unit.get("evidence_mode") != "published-witness-comparison":
            errors.append(f"{uid}: this pilot must not claim fresh image restoration")
        if unit.get("review_mode") != "single-Codex-editorial-pass":
            errors.append(f"{uid}: pilot may not claim an unperformed second review")
        if unit.get("publication_status") != "not-promoted":
            errors.append(f"{uid}: research pilot must remain separate from publication")
        candidates = unit.get("candidates", [])
        cids = [c.get("id") for c in candidates]
        if len(cids) < 2 or None in cids or len(set(cids)) != len(cids):
            errors.append(f"{uid}: at least two unique alternatives are required")
        witnesses = unit.get("witnesses", [])
        wids = [w.get("id") for w in witnesses]
        if not wids or None in wids or len(set(wids)) != len(wids):
            errors.append(f"{uid}: witness IDs must be nonempty and unique")
        for witness in witnesses:
            wid = f"{uid}/{witness.get('id')}"
            reading = witness.get("supports")
            if reading is not None and reading not in cids:
                errors.append(f"{wid}: unknown candidate")
            if reading is not None and (
                witness.get("coverage_confirmed") is not True or
                witness.get("attestation") not in ("present", "attested-absence")
            ):
                errors.append(f"{wid}: no coverage or unclear text cannot support a reading")
            if not witness.get("relationship_group"):
                errors.append(f"{wid}: missing relationship group")
            refs = witness.get("source_refs", [])
            if not refs or any(r not in source_ids + ["local-baseline"] for r in refs):
                errors.append(f"{wid}: missing or unknown source references")
            if witness.get("evidence_basis") not in ("local-text", "published-report"):
                errors.append(f"{wid}: unsupported evidence basis")
            if witness.get("archival_image_checked") is not False:
                errors.append(f"{wid}: no archival-image check was performed in this pilot")
            if witness.get("dating", {}).get("kind") not in (
                "physical-copy", "work-composition", "translation-tradition", "textual-tradition", "edition-publication"
            ):
                errors.append(f"{wid}: distinguish object dates from tradition or work dates")
            if witness.get("role") in ("ancient-version", "retelling") and witness.get("support_scope") == "direct-wording":
                errors.append(f"{wid}: translation or retelling is not direct source-language wording")
        decision = unit.get("decision", {})
        preferred = decision.get("preferred")
        if decision.get("status") == "working-preference":
            if preferred not in cids:
                errors.append(f"{uid}: preferred candidate does not exist")
            elif not any(w.get("supports") == preferred for w in witnesses):
                errors.append(f"{uid}: preferred candidate has no cited attestation")
            elif all(w.get("role") == "critical-edition" for w in witnesses if w.get("supports") == preferred):
                errors.append(f"{uid}: edition choices alone are not manuscript corroboration")
        elif decision.get("status") != "unresolved" or preferred is not None:
            errors.append(f"{uid}: invalid decision status or unresolved preference")
        if decision.get("priority_confidence") not in ("low", "moderate", "strong"):
            errors.append(f"{uid}: confidence must be qualitative, not a model probability")
        for key in ("summary", "reason_for", "counterargument", "transmission_explanation",
                    "chronological_effect", "independence_effect", "publication_action"):
            if not decision.get(key):
                errors.append(f"{uid}: decision requires {key}")
        if not isinstance(decision.get("exact_wording_resolved"), bool):
            errors.append(f"{uid}: exact-wording decision must be explicit")
        if decision.get("exact_wording_resolved") is False and not decision.get("open_questions"):
            errors.append(f"{uid}: unresolved wording requires open questions")
        baseline = unit.get("baseline", {})
        digest = baseline.get("sha256", "")
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            errors.append(f"{uid}: invalid baseline hash")
        path = (ROOT / baseline.get("repo_path", "")).resolve()
        if not path.is_relative_to(ROOT / "translation"):
            errors.append(f"{uid}: baseline must name a canonical translation file")
        elif check_current_baseline:
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f"{uid}: baseline drift; refresh the comparison before promotion")
    return errors


def cell(value: str | None) -> str:
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


def render(data: dict) -> str:
    title = data.get("title", "Hebrew pilot: applied multi-witness adjudication")
    dataset = data.get("dataset_path", "sources/textual_restoration/decisions/hebrew_pilot.v1.json")
    language = data.get("source_language", "Hebrew")
    lines = [f"# {title}", "",
             f"Checked: {data['checked_date']} · Method {data['method_version']}", "",
             f"Generated from the [decision dataset](../{dataset}). "
             "These are working editorial choices from published readings, not new image restorations, "
             "cross-model-reviewed decisions, or published POB changes.", "",
             "Older witnesses receive a modest preference; no numerical vote or authenticity percentage is used.", ""]
    for unit in data["units"]:
        decision = unit["decision"]
        lines += [f"## {unit['reference']}", "",
                  f"**Working preference:** {decision['summary']}",
                  f"**Priority confidence:** {decision['priority_confidence']} (editorial judgment, not a probability).",
                  f"**Wording-level outcome:** {'provisional selection within this unit' if decision['exact_wording_resolved'] else 'exact earlier form unresolved'}.", "",
                  f"| Candidate | {language} excerpt | English effect |", "|---|---|---|"]
        for candidate in unit["candidates"]:
            lines.append(f"| {cell(candidate['id'])} | {cell(candidate.get('source_text', candidate.get('hebrew')))} | {cell(candidate['english'])} |")
            if candidate.get("display_note"):
                lines.append("")
                lines.append(candidate["display_note"])
        lines += ["", "### Witness matrix", "",
                  "Every non-local row below is a published report; archival pixels were not independently re-read in this pass.", "",
                  "| Witness | Language / role | Reported reading | Date basis | Related evidence group | Source |",
                  "|---|---|---|---|---|---|"]
        for witness in unit["witnesses"]:
            refs = ", ".join(witness["source_refs"])
            lines.append("| " + " | ".join(cell(v) for v in (
                witness["label"], witness["language"] + " / " + witness["role"],
                witness["reported_reading"], witness["dating"]["kind"] + ": " + witness["dating"]["description"],
                witness["relationship_group"], refs)) + " |")
        lines += ["", f"Baseline: [{unit['baseline']['repo_path']}](../{unit['baseline']['repo_path']}).", ""]
        for label, key in (("Why prefer it", "reason_for"), ("Strongest objection", "counterargument"),
                           ("Transmission explanation", "transmission_explanation"),
                           ("Effect of age", "chronological_effect"), ("Independence caution", "independence_effect"),
                           ("Publication decision", "publication_action")):
            lines.append(f"- **{label}:** {decision[key]}")
        lines += ["", "Still unresolved:"] + [f"- {q}" for q in decision["open_questions"]]
        lines += ["", "Not used to force a result:"] + [f"- {q}" for q in decision["excluded_evidence"]] + [""]
    lines += ["## Sources", ""]
    for source in data["sources"]:
        lines.append(f"- **{source['id']}:** [{source['title']}]({source['url']}) — {source['locator']}.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-current-baseline", action="store_true")
    parser.add_argument("--report", action="store_true", help="regenerate the fixed Markdown report")
    parser.add_argument("--track", choices=("hebrew", "nt"), default="hebrew")
    args = parser.parse_args()
    source_path, report_path = (NT_DATA, NT_REPORT) if args.track == "nt" else (DATA, REPORT)
    data = json.loads(source_path.read_text())
    errors = validate(data, args.check_current_baseline)
    if errors:
        print("\n".join("FAIL: " + error for error in errors))
        return 1
    if args.report:
        report_path.write_text(render(data))
        print(f"Report written: {report_path}")
    print(f"Validated {len(data['units'])} decisions; "
          f"{sum(len(u['witnesses']) for u in data['units'])} passage-level witness rows. "
          "Canonical text was not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
