#!/usr/bin/env python3
"""Validate the OT witness registry's evidence boundaries and local references."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "sources/textual_restoration/ot_witness_registry.v1.json"
COVERAGE = ROOT / "sources/textual_restoration/coverage/pentateuch_pilot.v1.json"
COMPARISON = ROOT / "sources/textual_restoration/comparisons/pentateuch_controls.v1.json"
SAMUEL_COVERAGE = ROOT / "sources/textual_restoration/coverage/samuel_pilot.v1.json"
SAMUEL_COMPARISON = ROOT / "sources/textual_restoration/comparisons/samuel_controls.v1.json"
PSALMS_COVERAGE = ROOT / "sources/textual_restoration/coverage/psalms_pilot.v1.json"
PSALMS_COMPARISON = ROOT / "sources/textual_restoration/comparisons/psalms_controls.v1.json"
SELECTIONS = ROOT / "sources/textual_restoration/selections/ot_critical_source_pilot.v1.json"
ADJUDICATION = ROOT / "sources/textual_restoration/decisions/hebrew_pilot.v1.json"


def comparison_text(value: str) -> str:
    """Strip Hebrew pointing and source-token separators for phrase checks."""
    return "".join(
        char for char in unicodedata.normalize("NFD", value)
        if unicodedata.category(char) != "Mn" and char != "/"
    )


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    policy = data.get("policy", {})
    if policy.get("target") != "earliest-attainable-text":
        errors.append("policy target must remain earliest-attainable-text")
    if policy.get("imagegen_is_evidence") is not False:
        errors.append("ImageGen must never be evidence")
    if policy.get("automatic_translation_changes") is not False:
        errors.append("registry discovery cannot automatically change translation")

    witnesses = data.get("witnesses", [])
    ids = [w.get("id") for w in witnesses]
    if not witnesses or None in ids or len(ids) != len(set(ids)):
        errors.append("witness IDs must be nonempty and unique")

    allowed_classes = {
        "direct-hebrew-aramaic-manuscript", "direct-hebrew-inscription",
        "ancient-daughter-version", "masoretic-control", "modern-transcription",
        "critical-edition", "critical-apparatus",
    }
    for witness in witnesses:
        wid = witness.get("id", "<missing>")
        if witness.get("witness_class") not in allowed_classes:
            errors.append(f"{wid}: invalid witness class")
        if not witness.get("languages") or not witness.get("corpus_coverage"):
            errors.append(f"{wid}: language and corpus coverage are required")
        if not witness.get("relationship_group"):
            errors.append(f"{wid}: relationship group is required before counting support")
        if not witness.get("next_action"):
            errors.append(f"{wid}: next discovery or collation action is required")
        if witness.get("restoration_suitability") == "none" and "restore" in witness.get("next_action", "").lower():
            errors.append(f"{wid}: non-restorable source has a restoration action")

        repo_path = witness.get("repo_path")
        if repo_path:
            resolved = (ROOT / repo_path).resolve()
            if not resolved.is_relative_to(ROOT / "sources") or not resolved.exists():
                errors.append(f"{wid}: repo_path is missing or outside sources")

        access = witness.get("access", [])
        if not access:
            errors.append(f"{wid}: at least one access record is required")
        for index, item in enumerate(access):
            url = urlparse(item.get("url", ""))
            if url.scheme != "https" or not url.netloc:
                errors.append(f"{wid}/access/{index}: stable HTTPS URL required")
            if item.get("availability") == "local" and not repo_path:
                errors.append(f"{wid}/access/{index}: local access requires repo_path")
            if item.get("rights_status") == "unknown" and not witness.get("next_action"):
                errors.append(f"{wid}/access/{index}: unknown rights require a next action")
    return errors


def summarize(data: dict) -> dict:
    witnesses = data["witnesses"]
    return {
        "registered_witnesses_or_families": len(witnesses),
        "vendored": sum(w["source_state"] == "vendored" for w in witnesses),
        "image_or_multispectral_access": sum(
            any(a["kind"] in {"images", "multispectral-images"} for a in w["access"])
            for w in witnesses
        ),
        "restoration_candidates": sum(w["restoration_suitability"] != "none" for w in witnesses),
        "coverage_mapped": sum(w.get("coverage_status") == "mapped" for w in witnesses),
        "coverage_partial": sum(w.get("coverage_status") == "partial-map" for w in witnesses),
        "coverage_unmapped": sum(w.get("coverage_status") == "unmapped" for w in witnesses),
    }


def validate_coverage(coverage: dict, registry: dict) -> list[str]:
    errors: list[str] = []
    witness_ids = {w["id"] for w in registry["witnesses"]}
    records = coverage.get("records", [])
    record_ids = [record.get("id") for record in records]
    if not records or None in record_ids or len(record_ids) != len(set(record_ids)):
        errors.append("coverage record IDs must be nonempty and unique")
    for record in records:
        rid = record.get("id", "<missing>")
        if record.get("witness_id") not in witness_ids:
            errors.append(f"{rid}: coverage references an unknown witness")
        if record.get("coverage_status") == "present" and not record.get("passage_span"):
            errors.append(f"{rid}: present coverage requires an observed page span")
        basis = record.get("coverage_basis")
        if record.get("pixels_acquired") is True:
            inspection = record.get("image_inspection", {})
            if not inspection or not record.get("official_image_record"):
                errors.append(f"{rid}: acquired pixels require an image inspection manifest")
            if record.get("image_rights_status") != "study-only":
                errors.append(f"{rid}: current image pilot permits private study only")
            if any(inspection.get(key) is not False for key in (
                "generated_images_used", "publication_authorized", "complete_image_verification"
            )):
                errors.append(f"{rid}: image pilot cannot claim generated evidence, publication, or complete verification")
            if inspection.get("mode") != "single-editor-context-informed":
                errors.append(f"{rid}: image pilot must disclose its context-informed review")
        elif record.get("pixels_acquired") is not False or record.get("image_inspection"):
            errors.append(f"{rid}: pixels acquisition and inspection manifest disagree")
        if basis == "institutional-image-map":
            if record.get("transcription_collated") is not False:
                errors.append(f"{rid}: an image locator cannot claim a completed transcription")
            required_urls = ("canvas_id", "image_service_id", "mapping_source", "holding_source")
        elif basis == "published-transcription-index":
            if record.get("transcription_collated") is not True:
                errors.append(f"{rid}: published transcription coverage must record a completed collation")
            if not all(record.get(key) for key in ("manuscript_id", "standard_siglum", "source_snapshot", "transcription_locators")):
                errors.append(f"{rid}: manuscript identity, snapshot, and transcript locators are required")
            if record.get("reading_support_status") not in {
                "supports-reading", "indeterminate-lacuna", "coverage-only",
            }:
                errors.append(f"{rid}: published transcription requires a reading support status")
            required_urls = ("transcription_source", "mapping_source", "holding_source")
        else:
            errors.append(f"{rid}: invalid coverage basis")
            required_urls = ("mapping_source", "holding_source")
        for field in required_urls:
            parsed = urlparse(record.get(field, ""))
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{rid}: {field} requires a stable HTTPS URL")
    return errors


def verify_private_images(coverage: dict, private_root: Path) -> list[str]:
    """Verify private bytes only when the caller explicitly supplies their root.

    Normal repository validation checks metadata, not inaccessible image files
    or the correctness of the editorial reading.
    """
    errors = []
    root = private_root.resolve()
    for record in coverage.get("records", []):
        inspection = record.get("image_inspection")
        if not inspection:
            continue
        rid = record.get("id", "<missing>")
        if not isinstance(inspection, dict):
            errors.append(f"{rid}: invalid private image manifest")
            continue
        key = inspection.get("private_copy_key")
        assets = inspection.get("assets")
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9-]+", key) or not isinstance(assets, list) or not assets:
            errors.append(f"{rid}: invalid private image manifest")
            continue
        for asset in assets:
            if not isinstance(asset, dict) or not all(
                isinstance(asset.get(field), str) and re.fullmatch(pattern, asset[field])
                for field, pattern in (("file_name", r"[0-9a-f]{16}"), ("sha256", r"[0-9a-f]{64}"))
            ):
                errors.append(f"{rid}: invalid private image asset metadata")
                continue
            path = (root / key / asset["file_name"]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                errors.append(f"{rid}: private image missing or outside supplied root")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != asset["sha256"]:
                errors.append(f"{rid}: private image hash mismatch")
    return errors


def validate_comparison(comparison: dict) -> list[str]:
    errors: list[str] = []
    policy = comparison.get("policy", {})
    for key in (
        "controls_are_manuscript_votes", "reference_text_is_rylands_transcription",
        "automatic_text_selection", "automatic_english_change",
    ):
        if policy.get(key) is not False:
            errors.append(f"comparison policy {key} must be false")
    sources = comparison.get("sources", [])
    source_ids = [source.get("id") for source in sources]
    if None in source_ids or not source_ids or len(source_ids) != len(set(source_ids)):
        errors.append("comparison sources require IDs")
    sources_by_id = {source.get("id"): source for source in sources}
    case_ids: set[str] = set()
    for case in comparison.get("cases", []):
        cid = case.get("id", "<missing>")
        if cid in case_ids:
            errors.append(f"{cid}: duplicate comparison case")
        case_ids.add(cid)
        if case.get("decision_status") != "not-adjudicated" or case.get("preferred_reading") is not None:
            errors.append(f"{cid}: control comparison cannot select a reading")
        if case.get("canonical_change_applied") is not False:
            errors.append(f"{cid}: control comparison cannot claim a canonical change")
        readings = case.get("readings", [])
        if len(readings) < 2:
            errors.append(f"{cid}: at least two controls are required")
        physical_manuscripts: set[str] = set()
        for reading in readings:
            source_ref = reading.get("source_ref")
            if source_ref not in sources_by_id:
                errors.append(f"{cid}: unknown source reference")
            if not reading.get("text") or not reading.get("relationship_group"):
                errors.append(f"{cid}: readings require text and relationship group")
            support_status = reading.get("support_status")
            if support_status not in {"supports-reading", "indeterminate-lacuna", "coverage-only"}:
                errors.append(f"{cid}: readings require a valid support status")
            indeterminate_class = reading.get("reading_class", "").startswith("indeterminate-")
            if indeterminate_class != (support_status == "indeterminate-lacuna"):
                errors.append(f"{cid}: an indeterminate lacuna cannot be counted as reading support")
            coverage_only_class = reading.get("reading_class", "").startswith("coverage-only-")
            if coverage_only_class != (support_status == "coverage-only"):
                errors.append(f"{cid}: coverage-only material cannot be counted as reading support")
            source = sources_by_id.get(source_ref, {})
            if source.get("manuscript_level") is True:
                manuscript_id = reading.get("witness_id")
                if not all((manuscript_id, reading.get("standard_siglum"), reading.get("locator"))):
                    errors.append(f"{cid}: direct transcription requires physical manuscript identity and locator")
                parsed = urlparse(reading.get("locator_url", ""))
                if parsed.scheme != "https" or not parsed.netloc:
                    errors.append(f"{cid}: direct transcription requires a stable locator URL")
                if manuscript_id in physical_manuscripts:
                    errors.append(f"{cid}: physical manuscript counted more than once")
                physical_manuscripts.add(manuscript_id)
        baseline = case.get("baseline", {})
        path = (ROOT / baseline.get("repo_path", "")).resolve()
        if not path.is_relative_to(ROOT / "translation") or not path.is_file():
            errors.append(f"{cid}: invalid canonical baseline path")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != baseline.get("sha256"):
            errors.append(f"{cid}: canonical baseline drift")
    return errors


def validate_selections(selections: dict, comparison: dict, adjudication: dict) -> list[str]:
    """Validate atomic source/English bundles and their evidence cross-links."""
    errors: list[str] = []
    policy = selections.get("policy", {})
    if policy.get("source_and_english_promote_atomically") is not True:
        errors.append("selection policy must promote source and English atomically")
    if policy.get("imagegen_is_evidence") is not False:
        errors.append("ImageGen must never be selection evidence")
    if policy.get("automatic_canonical_writes") is not False:
        errors.append("critical-source selection cannot automatically write canonical text")

    comparison_cases = {case["id"]: case for case in comparison.get("cases", [])}
    decision_units = {unit["id"]: unit for unit in adjudication.get("units", [])}
    records = selections.get("selections", [])
    record_ids = [record.get("id") for record in records]
    if not records or None in record_ids or len(record_ids) != len(set(record_ids)):
        errors.append("selection IDs must be nonempty and unique")

    for record in records:
        sid = record.get("id", "<missing>")
        if record.get("generated_images_used") is not False:
            errors.append(f"{sid}: generated images cannot support a source selection")

        case = comparison_cases.get(record.get("comparison_case_id"))
        unit = decision_units.get(record.get("adjudication_unit_id"))
        if case is None:
            errors.append(f"{sid}: unknown comparison case")
        if unit is None:
            errors.append(f"{sid}: unknown adjudication unit")
        if case is not None and case.get("reference") != record.get("reference"):
            errors.append(f"{sid}: comparison reference mismatch")
        if unit is not None and unit.get("reference") != record.get("reference"):
            errors.append(f"{sid}: adjudication reference mismatch")

        baseline = record.get("baseline", {})
        path = (ROOT / baseline.get("repo_path", "")).resolve()
        if not path.is_relative_to(ROOT / "translation/ot") or not path.is_file():
            errors.append(f"{sid}: invalid canonical baseline path")
        else:
            canonical = yaml.safe_load(path.read_text())
            if hashlib.sha256(path.read_bytes()).hexdigest() != baseline.get("sha256"):
                errors.append(f"{sid}: canonical baseline drift")
            if not baseline.get("declared_source_edition") or baseline.get("declared_source_edition") != canonical.get("source", {}).get("edition"):
                errors.append(f"{sid}: declared source edition is not present in the baseline")
            if not baseline.get("declared_source_text") or baseline.get("declared_source_text") != canonical.get("source", {}).get("text"):
                errors.append(f"{sid}: declared source text is not present in the baseline")
            if not baseline.get("english_text") or baseline.get("english_text") != canonical.get("translation", {}).get("text"):
                errors.append(f"{sid}: baseline English is not present in the canonical record")
        if case is not None and baseline.get("repo_path") != case.get("baseline", {}).get("repo_path"):
            errors.append(f"{sid}: selection and comparison baseline paths differ")
        if unit is not None and baseline.get("repo_path") != unit.get("baseline", {}).get("repo_path"):
            errors.append(f"{sid}: selection and adjudication baseline paths differ")

        critical = record.get("critical_source", {})
        english = record.get("english_candidate", {})
        evidence = record.get("evidence_links", {})
        if critical.get("reading_class") != evidence.get("comparison_reading_class"):
            errors.append(f"{sid}: selection reading class differs from its evidence link")
        if english.get("source_phrase") != critical.get("normalized_variation_unit"):
            errors.append(f"{sid}: English candidate is not bound to the selected Hebrew phrase")
        if english.get("rendering", "") not in english.get("full_verse_text", ""):
            errors.append(f"{sid}: full English candidate does not contain its selected rendering")

        if case is not None:
            matched_readings = [
                reading for reading in case.get("readings", [])
                if reading.get("reading_class") == evidence.get("comparison_reading_class")
                and reading.get("support_status") == "supports-reading"
            ]
            source_manuscripts = set(critical.get("source_manuscripts", []))
            direct_matches = [
                reading for reading in matched_readings
                if reading.get("witness_id") in source_manuscripts
            ]
            if not matched_readings or not source_manuscripts or len(direct_matches) != len(source_manuscripts):
                errors.append(f"{sid}: selected reading lacks direct comparison support")
            elif any(
                comparison_text(critical.get("normalized_variation_unit", "")) not in comparison_text(reading.get("text", ""))
                or critical.get("diplomatic_anchor", "") not in reading.get("text", "")
                for reading in direct_matches
            ):
                errors.append(f"{sid}: selected Hebrew is not anchored in the diplomatic comparison")
            for reading in direct_matches:
                visible = re.sub(r"\[[^\]]*\]", " | ", reading.get("text", ""))
                if not critical.get("normalized_variation_unit") or comparison_text(critical["normalized_variation_unit"]) not in comparison_text(visible):
                    errors.append(f"{sid}: selected phrase must survive outside editorial reconstruction")
            comparison_sources = {source["id"] for source in comparison.get("sources", [])}
            for retained in record.get("retained_readings", []):
                match = next((
                    reading for reading in case.get("readings", [])
                    if reading.get("source_ref") == retained.get("source_ref")
                    and reading.get("reading_class") == retained.get("reading_class")
                ), None)
                if retained.get("source_ref") not in comparison_sources or match is None:
                    errors.append(f"{sid}: retained reading does not resolve to the comparison")
                elif comparison_text(retained.get("text", "")) not in comparison_text(match.get("text", "")):
                    errors.append(f"{sid}: retained reading text is not present in its comparison control")

        if unit is not None:
            candidate = next((
                candidate for candidate in unit.get("candidates", [])
                if candidate.get("id") == evidence.get("adjudication_candidate_id")
            ), None)
            decision = unit.get("decision", {})
            if candidate is None or decision.get("preferred") != evidence.get("adjudication_candidate_id"):
                errors.append(f"{sid}: selection does not resolve to the preferred adjudication candidate")
            else:
                if candidate.get("hebrew") != critical.get("normalized_variation_unit"):
                    errors.append(f"{sid}: selected Hebrew differs from the adjudication candidate")
                if english.get("rendering", "") not in candidate.get("english", ""):
                    errors.append(f"{sid}: selected English differs from the adjudication candidate")
            if critical.get("priority_confidence") != decision.get("priority_confidence"):
                errors.append(f"{sid}: confidence differs from the adjudication")
            if critical.get("exact_wording_resolved") != decision.get("exact_wording_resolved"):
                errors.append(f"{sid}: wording-resolution state differs from the adjudication")

        required_gates = {
            "image_verification", "djd_material_review", "independent_editorial_review",
            "full_verse_critical_source", "english_review", "export_sync",
        }
        gates = record.get("review_gates", {})
        if set(gates) != required_gates:
            errors.append(f"{sid}: required review gates are missing or unknown")
        gate_values = [gates.get(key) for key in required_gates]
        promotion = record.get("promotion_status")
        canonical_applied = record.get("canonical_change_applied")
        if promotion != "not-promoted":
            errors.append(f"{sid}: this pilot cannot certify promotion; reviewed application receipts are not implemented")
        if promotion in {"ready-for-promotion", "promoted"} and any(
            value != "complete" for value in gate_values
        ):
            errors.append(f"{sid}: selection cannot advance while review gates remain open")
        if promotion == "promoted":
            if canonical_applied is not True:
                errors.append(f"{sid}: promoted selection must record the canonical change")
            if critical.get("status") != "approved-selection" or critical.get("scope") != "full-verse":
                errors.append(f"{sid}: promotion requires an approved full-verse critical source")
            if critical.get("exact_wording_resolved") is not True or not critical.get("full_verse_text"):
                errors.append(f"{sid}: promotion requires resolved full-verse Hebrew wording")
        elif canonical_applied is not False:
            errors.append(f"{sid}: unpromoted selection cannot claim a canonical change")
        if critical.get("exact_wording_resolved") is False and not record.get("open_questions"):
            errors.append(f"{sid}: unresolved wording requires open questions")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--private-image-root", type=Path,
                        help="optionally verify private image hashes; never downloads or publishes")
    args = parser.parse_args()
    data = json.loads(REGISTRY.read_text())
    errors = validate(data)
    coverage_sets = [json.loads(path.read_text()) for path in (COVERAGE, SAMUEL_COVERAGE, PSALMS_COVERAGE)]
    for coverage in coverage_sets:
        errors += validate_coverage(coverage, data)
        if args.private_image_root:
            errors += verify_private_images(coverage, args.private_image_root)
    comparison_sets = [json.loads(path.read_text()) for path in (COMPARISON, SAMUEL_COMPARISON, PSALMS_COMPARISON)]
    for comparison in comparison_sets:
        errors += validate_comparison(comparison)
    selections = json.loads(SELECTIONS.read_text())
    adjudication = json.loads(ADJUDICATION.read_text())
    schema_pairs = [
        ("ot-witness-registry", data),
        *[("ot-passage-coverage", item) for item in coverage_sets],
        *[("ot-source-comparison", item) for item in comparison_sets],
        ("ot-critical-source-selection", selections),
    ]
    for name, document in schema_pairs:
        schema = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())
        errors += [f"{name}: {error.message}" for error in Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(document)]
    combined_comparison = {
        "sources": [source for item in comparison_sets for source in item["sources"]],
        "cases": [case for item in comparison_sets for case in item["cases"]],
    }
    errors += validate_selections(selections, combined_comparison, adjudication)
    if errors:
        for error in errors:
            print(error)
        return 1
    if args.report:
        print(json.dumps(summarize(data), indent=2))
    else:
        print(
            f"Validated {len(data['witnesses'])} OT witnesses or source families "
            f"and {sum(len(item['records']) for item in coverage_sets)} passage coverage records and "
            f"{sum(len(item['cases']) for item in comparison_sets)} source-control comparisons and "
            f"{len(selections['selections'])} atomic source/English selections."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
