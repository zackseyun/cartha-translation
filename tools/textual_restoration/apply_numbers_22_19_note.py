#!/usr/bin/env python3
"""Bounded Numbers 22:19 note package; no general-purpose canonical editor."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from unittest.mock import patch

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PACKAGE = ROOT / "sources/textual_restoration/applications"
TARGET_REL = "translation/ot/numbers/022/019.yaml"
BASELINE = PACKAGE / "numbers_22_19_note_baseline.v1.yaml"
CANDIDATE = PACKAGE / "numbers_22_19_note_candidate.v1.yaml"
PLAN = PACKAGE / "numbers_22_19_note_plan.v1.json"
JUDGMENT = PACKAGE / "numbers_22_19_note_judgment.v1.json"
INTENT = PACKAGE / "numbers_22_19_note_intent.v1.json"
APPLIED = PACKAGE / "numbers_22_19_note_application.v1.json"
BASELINE_SHA = "74348f325b3cfb563c42c4d5075985ce833193d906dfdfe51a0bcc5eb88ff246"
FROZEN_SELECTION_SHA = "c1ac793d6837896fb4fcd64e39adf4c70ea9527cae0bbced6036c5da8768074f"
FROZEN_REVIEW_SHA = "b124e7b20876ea771f75c0a9d7c91b34cd9782ab8412c440e092f2b73c65a3f6"
PACKAGE_ID = "NUM.22.19-note-anchor-name-2026-09-05-v1"
BEFORE_TEXT = "Now please stay here tonight[a], you also, so that I may know what more Yahweh will say to me."
AFTER_TEXT = "Now please stay here tonight, you also, so that I may know what more Yahweh will say to me[a]."
BEFORE_NOTE = "Or 'what else the LORD will speak to me.'"
AFTER_NOTE = "Or 'what else Yahweh will speak to me.'"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def compose(raw):
    if sha(raw) != BASELINE_SHA:
        raise ValueError("Exact Numbers baseline drift")
    before = yaml.safe_load(raw)
    text = raw.decode()
    for old, new in (("  text: " + BEFORE_TEXT, "  text: " + AFTER_TEXT),
                     ("    text: " + BEFORE_NOTE, "    text: " + AFTER_NOTE),
                     ("status: revised\n", "status: draft\n")):
        if text.count(old) != 1:
            raise ValueError("Bounded replacement not unique")
        text = text.replace(old, new)
    for field in ("revision_pass", "cross_check"):
        text, count = re.subn(r"(?ms)^" + field + r":\n.*?(?=^\S|\Z)", "", text)
        if count != 1:
            raise ValueError("Historical field not unique")
    history = [{"field": field, "value": before[field],
                "archived_from_baseline_sha256": BASELINE_SHA,
                "historical_review_input_binding": "not-verified",
                "certifies_this_candidate": False}
               for field in ("status", "revision_pass", "cross_check")]
    tail = {"cross_check": {"status": "needs_review"}, "review_history": history,
            "note_application": {"package_id": PACKAGE_ID,
                "scope": "sole footnote anchor and divine-name wording; no source or main-prose change",
                "baseline_sha256": BASELINE_SHA,
                "independent_note_review": str(JUDGMENT.relative_to(ROOT)),
                "application_receipt": str(APPLIED.relative_to(ROOT)),
                "whole_verse_reapproved": False,
                "ai_draft_metadata_role": "historical-original-draft; not current approval",
                "publication_approval": False}}
    candidate = (text.rstrip() + "\n" + yaml.safe_dump(tail, allow_unicode=True, sort_keys=False, width=1000)).encode()
    validate_scope(raw, candidate)
    return candidate


def validate_scope(raw, candidate_raw):
    before, after = yaml.safe_load(raw), yaml.safe_load(candidate_raw)
    if before["id"] != "NUM.22.19" or after["id"] != before["id"]:
        raise ValueError("Wrong verse")
    if after["translation"]["text"] != AFTER_TEXT or after["translation"]["text"].count("[a]") != 1:
        raise ValueError("Expected exact single final-clause note anchor")
    if after["translation"]["text"].replace("[a]", "") != before["translation"]["text"].replace("[a]", ""):
        raise ValueError("Main prose changed")
    expected_translation = copy.deepcopy(before["translation"])
    expected_translation["text"] = AFTER_TEXT
    expected_translation["footnotes"][0]["text"] = AFTER_NOTE
    if after["translation"] != expected_translation:
        raise ValueError("Unapproved translation/note edit")
    allowed = {"translation", "status", "revision_pass", "cross_check", "review_history", "note_application"}
    if set(after) != (set(before) - {"revision_pass"}) | {"review_history", "note_application"}:
        raise ValueError("Unexpected top-level fields")
    for field in set(before) - allowed:
        if before[field] != after[field]:
            raise ValueError(f"Unapproved component change: {field}")
    if after["status"] != "draft" or after["cross_check"] != {"status": "needs_review"}:
        raise ValueError("Historical certification reused")
    history = after["review_history"]
    if len(history) != 3:
        raise ValueError("Historical archive incomplete")
    for field in ("status", "revision_pass", "cross_check"):
        matches = [entry for entry in history if entry["field"] == field]
        if len(matches) != 1 or matches[0] != {"field": field, "value": before[field],
                "archived_from_baseline_sha256": BASELINE_SHA,
                "historical_review_input_binding": "not-verified", "certifies_this_candidate": False}:
            raise ValueError("Historical value or binding changed")


def verify_package(require_judgment=False):
    raw, candidate = BASELINE.read_bytes(), CANDIDATE.read_bytes()
    plan = json.loads(PLAN.read_text())
    if sha(raw) != BASELINE_SHA or compose(raw) != candidate:
        raise ValueError("Frozen baseline/candidate composition mismatch")
    if plan["package_id"] != PACKAGE_ID or plan["baseline_sha256"] != sha(raw) or plan["candidate_yaml_sha256"] != sha(candidate):
        raise ValueError("Plan binding mismatch")
    if require_judgment:
        verdict = json.loads(JUDGMENT.read_text())
        if (verdict.get("package_id") != PACKAGE_ID or verdict.get("baseline_sha256") != sha(raw)
                or verdict.get("candidate_yaml_sha256") != sha(candidate)
                or verdict.get("note_only_local_application_approved") is not True
                or verdict.get("whole_verse_reapproved") is not False
                or verdict.get("publication_approved") is not False):
            raise ValueError("Missing exact-byte, note-only independent approval")
    return raw, candidate, plan


def historical_bytes(path, current_reader=Path.read_bytes):
    """One pinned overlay; third states always fail, never silently pass drift."""
    current = current_reader(path)
    if path.resolve() != (ROOT / TARGET_REL).resolve():
        return current
    raw, candidate, _ = verify_package()
    if current == raw:
        return raw
    if current != candidate:
        raise ValueError("Unknown current Numbers state; historical overlay refused")
    verify_package(require_judgment=True)
    transaction = APPLIED if APPLIED.exists() else INTENT
    if not transaction.exists():
        raise ValueError("Candidate lacks application transaction provenance")
    verify_transaction_binding(json.loads(transaction.read_text()), raw, candidate)
    return raw


def historical_sample_probe():
    original_reader = Path.read_bytes
    # Resolve overlay before patching Path.read_bytes so package reads do not recurse.
    target = (ROOT / TARGET_REL).resolve()
    start = original_reader(target)
    overlay = historical_bytes(target, current_reader=original_reader)
    spec = importlib.util.spec_from_file_location("frozen_unflagged_selector", ROOT / "tools/textual_restoration/build_unflagged_english_sample.py")
    selector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(selector)
    selection_path = ROOT / "sources/textual_restoration/samples/unflagged_english_sample.selection.v1.json"
    review_path = ROOT / "sources/textual_restoration/samples/unflagged_english_sample.review.v1.json"
    if sha(selection_path.read_bytes()) != FROZEN_SELECTION_SHA or sha(review_path.read_bytes()) != FROZEN_REVIEW_SHA:
        raise ValueError("Frozen sample receipt bytes changed")
    saved, review = json.loads(selection_path.read_text()), json.loads(review_path.read_text())
    if sha(selection_path.read_bytes()) != review["selection_receipt_sha256"]:
        raise ValueError("Frozen sample selection binding changed")
    for rel, expected in saved["protocol_inputs"].items():
        if sha((ROOT / rel).read_bytes()) != expected:
            raise ValueError(f"Frozen protocol input changed: {rel}")
    current_rows = []
    def read_bytes(path):
        actual = original_reader(path)
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("translation/ot/") and path.suffix == ".yaml":
            current_rows.append((rel, sha(actual)))
        return overlay if path.resolve() == target else actual
    with patch.object(Path, "read_bytes", new=read_bytes):
        reconstructed = selector.build()
        if reconstructed != saved:
            raise ValueError("Historical sample mismatch, including complete protocol inputs/key set")
        current_corpus_digest = selector.digest_rows(current_rows)
        contexts = {path: digest for row in review["records"] for path, digest in row["context_files"].items()}
        for rel, digest in contexts.items():
            if sha((ROOT / rel).read_bytes()) != digest:
                raise ValueError(f"Historical context drift: {rel}")
    if original_reader(target) != start:
        raise ValueError("Canonical target changed during historical reconstruction")
    return {"historical_selection_reproduced": True, "context_files_verified": len(contexts),
            "overlay_paths": [TARGET_REL], "current_target_sha256": sha(start),
            "historical_target_sha256": sha(overlay), "current_target_differs": start != overlay,
            "frozen_selection_sha256": sha(selection_path.read_bytes()), "frozen_review_sha256": sha(review_path.read_bytes()),
            "historical_corpus_digest": saved["corpus_digest"],
            "current_corpus_digest": current_corpus_digest,
            "all_frozen_protocol_inputs_verified": len(saved["protocol_inputs"]),
            "current_corpus_matches_historical": start == overlay,
            "current_corpus_difference_scope": [] if start == overlay else [TARGET_REL]}


def export_probe(raw, candidate_raw):
    from tools import export_mobile_bible as exporter
    original = exporter.load_translation_record
    before, candidate = yaml.safe_load(raw), yaml.safe_load(candidate_raw)
    def export_with(record):
        def overlay(book, chapter, verse):
            return copy.deepcopy(record) if (book, chapter, verse) == ("NUM", 22, 19) else original(book, chapter, verse)
        with patch.object(exporter, "load_translation_record", side_effect=overlay):
            return exporter.export_book("NUM")
    baseline_book, candidate_book = export_with(before), export_with(candidate)
    def target(book):
        return next(v for c in book["chapters"] if c["chapter"] == 22 for v in c["verses"] if v["verse"] == 19)
    b, c = target(baseline_book), target(candidate_book)
    control = copy.deepcopy(candidate_book)
    control_target = target(control)
    control_target.clear()
    control_target.update(b)
    actual = exporter.export_book("NUM")
    return {"mode": "real full Numbers exporter with separately pinned single-record baseline/candidate loader overlays",
            "chapters": len(candidate_book["chapters"]), "verses": sum(len(c["verses"]) for c in candidate_book["chapters"]),
            "baseline_book_sha256": sha(json_bytes(baseline_book)), "candidate_book_sha256": sha(json_bytes(candidate_book)),
            "actual_current_book_sha256": sha(json_bytes(actual)),
            "actual_current_matches_baseline": actual == baseline_book,
            "actual_current_matches_candidate": actual == candidate_book,
            "baseline_verse": b, "candidate_verse": c,
            "all_other_book_content_unchanged": control == baseline_book,
            "single_final_anchor_preserved": c["text"] == AFTER_TEXT and c["text"].count("[a]") == 1,
            "note_body_preserved": c.get("footnotes") == candidate["translation"]["footnotes"],
            "research_history_exported": any(k in c for k in ("review_history", "note_application", "cross_check")),
            "source_object_exported": "source" in c,
            "deployed_reader_checked": False}


def preflight():
    raw, candidate_raw, plan = verify_package()
    current_start = (ROOT / TARGET_REL).read_bytes()
    if current_start not in (raw, candidate_raw):
        raise ValueError("Current target drift")
    schema_path = ROOT / "schema/verse.schema.json"
    validator = Draft202012Validator(json.loads(schema_path.read_text()))
    before, after = yaml.safe_load(raw), yaml.safe_load(candidate_raw)
    def errors(value):
        return [{"path": "/".join(map(str, e.absolute_path)), "message": e.message}
                for e in sorted(validator.iter_errors(value), key=lambda e: str(e.absolute_path))]
    exported = export_probe(raw, candidate_raw)
    historical = historical_sample_probe()
    if (ROOT / TARGET_REL).read_bytes() != current_start:
        raise ValueError("Current target changed during preflight")
    return {"package_id": PACKAGE_ID, "checked_date": "2026-09-05",
            "baseline_yaml_sha256": sha(raw), "candidate_yaml_sha256": sha(candidate_raw),
            "candidate_json_sha256": sha(json_bytes(after)), "plan_sha256": sha(PLAN.read_bytes()),
            "schema_sha256": sha(schema_path.read_bytes()),
            "exporter_sha256": sha((ROOT / "tools/export_mobile_bible.py").read_bytes()),
            "builder_sha256": sha(Path(__file__).read_bytes()),
            "components": {k: {"before_sha256": sha(json_bytes(before.get(k))), "after_sha256": sha(json_bytes(after.get(k))),
                               "changed": before.get(k) != after.get(k)} for k in sorted(set(before) | set(after))},
            "schema_check": {"baseline_errors": errors(before), "candidate_errors": errors(after)},
            "export_check": exported, "historical_sample_check": historical,
            "canonical_change_applied_by_this_preflight": False,
            "publication_ready": False,
            "publication_limits": ["Note-only local review is not a fresh whole-verse source/English approval.",
                "Website/CDN disclosure and production-publication gates remain unchecked or failed; no deployment is authorized."]}


def verify_transaction_binding(transaction, raw, candidate):
    expected = {"package_id": PACKAGE_ID, "baseline_sha256": sha(raw),
                "candidate_yaml_sha256": sha(candidate), "judgment_sha256": sha(JUDGMENT.read_bytes())}
    if any(transaction.get(key) != value for key, value in expected.items()):
        raise ValueError("Transaction provenance binding mismatch")


def require_checks(result):
    export = result["export_check"]
    if (result["schema_check"]["candidate_errors"] or not export["all_other_book_content_unchanged"]
            or not export["single_final_anchor_preserved"] or not export["note_body_preserved"]
            or export["research_history_exported"] or export["chapters"] != 36
            or export["verses"] != 1289
            or not result["historical_sample_check"]["historical_selection_reproduced"]
            or result["historical_sample_check"]["context_files_verified"] != 101):
        raise ValueError("Required local schema/export/historical checks failed")


def atomic_replace_expected(path, expected, replacement, before_swap=None):
    """Atomic single-file visibility, not a general concurrent-writer CAS."""
    if path.is_symlink() or path.resolve() != path.absolute():
        raise ValueError("Canonical target must not traverse symlinks")
    if path.read_bytes() != expected:
        raise ValueError("Canonical baseline drift before staging")
    mode = path.stat().st_mode & 0o777
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".num22-note-", delete=False) as stream:
            temporary = Path(stream.name)
            os.fchmod(stream.fileno(), mode)
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        if before_swap:
            before_swap()
        if path.is_symlink() or path.read_bytes() != expected:
            raise ValueError("Canonical baseline drift immediately before replacement")
        os.replace(temporary, path)
        temporary = None
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_once(path, document):
    """New ledger only; never overwrite an existing receipt or symlink."""
    if path.is_symlink() or path.parent.resolve() != path.parent.absolute():
        raise ValueError("Ledger output must not traverse symlinks")
    raw = json_bytes(document)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def apply_package():
    """Execute only this reviewed package; persist intent before atomic swap."""
    # Stable external advisory lock is intentionally not removed on unlock.
    # It coordinates this package's cooperating writers, not arbitrary editors.
    lock_name = "pob-num22-note-" + sha(str(ROOT.resolve()).encode())[:16] + ".lock"
    lock_path = Path(tempfile.gettempdir()) / lock_name
    if lock_path.is_symlink():
        raise ValueError("Lock must not be a symlink")
    lock_fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(lock_fd, "a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        raw, candidate, _ = verify_package(require_judgment=True)
        target = ROOT / TARGET_REL
        if target.is_symlink() or target.resolve() != target.absolute():
            raise ValueError("Canonical target must not traverse symlinks")
        current = target.read_bytes()
        if current not in (raw, candidate):
            raise ValueError("Unknown current target; application refused")
        if APPLIED.exists():
            completed = json.loads(APPLIED.read_text())
            verify_transaction_binding(completed, raw, candidate)
            if current != candidate or completed.get("status") != "applied-verified":
                raise ValueError("Recorded application no longer matches canonical target")
            return completed
        if current == candidate and not INTENT.exists():
            raise ValueError("Candidate state has no prepared transaction to resume")
        before = preflight()
        require_checks(before)
        bound = {"package_id": PACKAGE_ID, "baseline_sha256": sha(raw),
                 "candidate_yaml_sha256": sha(candidate), "judgment_sha256": sha(JUDGMENT.read_bytes())}
        if INTENT.exists():
            intent = json.loads(INTENT.read_text())
            verify_transaction_binding(intent, raw, candidate)
            if intent.get("preflight", {}).get("builder_sha256") != before["builder_sha256"]:
                raise ValueError("Executor changed since prepared intent")
            for key in ("schema_sha256", "exporter_sha256", "plan_sha256"):
                if intent["preflight"][key] != before[key]:
                    raise ValueError("Pinned application input changed since intent")
        else:
            intent = {**bound, "status": "prepared", "prepared_at": datetime.now(timezone.utc).isoformat(),
                      "preflight": before, "publication_ready": False}
            write_once(INTENT, intent)
        # Recheck approval and all data immediately before the single-file swap.
        raw_now, candidate_now, _ = verify_package(require_judgment=True)
        if (raw_now, candidate_now) != (raw, candidate) or sha(JUDGMENT.read_bytes()) != bound["judgment_sha256"]:
            raise ValueError("Approved bytes or judgment drifted after preparation")
        for path, key in ((ROOT / "schema/verse.schema.json", "schema_sha256"),
                          (ROOT / "tools/export_mobile_bible.py", "exporter_sha256"),
                          (Path(__file__), "builder_sha256"), (PLAN, "plan_sha256")):
            if sha(path.read_bytes()) != before[key]:
                raise ValueError("Application code/schema/plan drifted after preflight")
        if current == raw:
            atomic_replace_expected(target, raw, candidate)
        after = preflight()
        require_checks(after)
        if target.read_bytes() != candidate or not after["export_check"]["actual_current_matches_candidate"]:
            raise ValueError("Post-application target/export does not match approved candidate; inspect prepared intent")
        completed = {**bound, "status": "applied-verified", "applied_at": datetime.now(timezone.utc).isoformat(),
                     "intent_sha256": sha(INTENT.read_bytes()), "resulting_canonical_sha256": sha(target.read_bytes()),
                     "post_application": after, "canonical_note_change_applied": True,
                     "main_prose_changed": False, "source_changed": False, "publication_ready": False,
                     "scope": "exact reviewed Numbers22:19 note repair and archival review-state bookkeeping only"}
        write_once(APPLIED, completed)
        return completed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--compose", action="store_true")
    mode.add_argument("--apply", action="store_true", help="Apply only the fixed candidate after exact-byte independent judgment and all local checks")
    args = parser.parse_args()
    if args.compose:
        sys.stdout.buffer.write(compose((ROOT / TARGET_REL).read_bytes()))
    elif args.apply:
        print(json.dumps(apply_package(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(preflight(), ensure_ascii=False, indent=2))
