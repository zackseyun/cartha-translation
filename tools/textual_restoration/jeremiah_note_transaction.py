#!/usr/bin/env python3
"""Fixed note-package ledgers/checks; canonical editing is a separate apply_patch.

Historical readers accept only exact baseline or approved candidate plus a
bound intent/application. They never rewrite old experiments to absorb drift.
"""
import argparse
from contextlib import contextmanager
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.textual_restoration import check_jeremiah_10_10_note_candidate_v2 as candidate_check
from tools.textual_restoration import apply_numbers_22_19_note as numbers
from tools.textual_restoration import check_jeremiah10_literary_forms as dossier
from tools import export_mobile_bible as exporter

PREFIX = ROOT / "sources/textual_restoration/applications"
TARGET = ROOT / candidate_check.v1.TARGET
BASELINE = PREFIX / "jeremiah_10_10_note_baseline.v1.yaml"
CANDIDATE = PREFIX / "jeremiah_10_10_note_candidate.v2.yaml"
PREFLIGHT = PREFIX / "jeremiah_10_10_note_preflight.v2.json"
JUDGMENT = PREFIX / "jeremiah_10_10_note_judgment.v2.json"
REVIEW = PREFIX / "jeremiah_10_10_note_transaction_review.v2.json"
INTENT = PREFIX / "jeremiah_10_10_note_intent.v2.json"
APPLICATION = PREFIX / "jeremiah_10_10_note_application.v2.json"
JUDGMENT_SHA = "121b89d7959a0b5506fc75e7515cfb1c86ec644a6f4c000c2b7c6ee73e8f027f"
PACKAGE_ID = "JER.10.10-literary-form-disclosure-2026-09-05-v2"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jbytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def package():
    if not __debug__:
        raise ValueError("frozen preflight assertions require non-optimized Python")
    raw, candidate = BASELINE.read_bytes(), CANDIDATE.read_bytes()
    if sha(raw) != candidate_check.v1.BASELINE_SHA or sha(candidate) != candidate_check.CANDIDATE_SHA:
        raise ValueError("baseline/candidate drift")
    if sha(JUDGMENT.read_bytes()) != JUDGMENT_SHA:
        raise ValueError("independent judgment drift")
    judgment = json.loads(JUDGMENT.read_text())
    if judgment["decision"] != "APPROVE" or judgment["bounded_note_application_approved"] is not True:
        raise ValueError("missing bounded approval")
    if any(judgment[k] is not False for k in ("whole_verse_reapproved", "publication_approved", "earliest_source_form_promoted")):
        raise ValueError("approval scope drift")
    frozen = json.loads(PREFLIGHT.read_text())
    for pins in (judgment["input_pins"], frozen["input_pins"]):
        for relative, expected in pins.items():
            if sha((ROOT / relative).read_bytes()) != expected:
                raise ValueError(f"bound input drift: {relative}")
    return raw, candidate, frozen


def binding():
    return {"package_id": PACKAGE_ID, "baseline_sha256": candidate_check.v1.BASELINE_SHA,
            "candidate_yaml_sha256": candidate_check.CANDIDATE_SHA,
            "judgment_sha256": JUDGMENT_SHA, "executor_sha256": sha(Path(__file__).read_bytes())}


def require_review():
    review = json.loads(REVIEW.read_text())
    if review.get("scoped_transaction_approved") is not True or any(review.get(k) != v for k, v in binding().items()):
        raise ValueError("missing or stale transaction review")


def require_transaction():
    require_review()
    def validate(path, status):
        record = json.loads(path.read_text())
        if any(record.get(k) != v for k, v in binding().items()) or record.get("transaction_review_sha256") != sha(REVIEW.read_bytes()):
            raise ValueError("transaction provenance drift")
        if record.get("status") != status:
            raise ValueError("invalid transaction state")
        return record
    validate(INTENT, "prepared")
    if APPLICATION.exists():
        record = validate(APPLICATION, "applied-verified")
        if record.get("intent_sha256") != sha(INTENT.read_bytes()):
            raise ValueError("application intent binding drift")


@contextmanager
def historical_view():
    raw, candidate, _ = package()
    if TARGET.is_symlink() or TARGET.resolve() != TARGET.absolute():
        raise ValueError("canonical target must not traverse symlinks")
    reader, text_reader = Path.read_bytes, Path.read_text
    start = reader(TARGET)
    if start not in (raw, candidate):
        raise ValueError("unknown Jeremiah state; historical overlay refused")
    if start == raw and APPLICATION.exists():
        raise ValueError("baseline contradicts completed application; rollback requires a new record")
    if start == candidate or INTENT.exists():
        require_transaction()
    def read_bytes(path):
        return raw if path == TARGET else reader(path)
    def read_text(path, *args, **kwargs):
        return raw.decode("utf-8") if path == TARGET else text_reader(path, *args, **kwargs)
    with patch.object(Path, "read_bytes", read_bytes), patch.object(Path, "read_text", read_text):
        yield
    if reader(TARGET) != start:
        raise ValueError("canonical changed during historical replay")


def historical_sample_probe():
    with historical_view():
        result = numbers.historical_sample_probe()
    # The inner digest intentionally describes the Jeremiah-baseline view.
    rows = [(p.relative_to(ROOT).as_posix(), sha(p.read_bytes()))
            for p in sorted((ROOT / "translation/ot").glob("*/*/*.yaml"))]
    digest = sha("".join(f"{p}\0{h}\n" for p, h in sorted(rows)).encode())
    return {"historical_selection_reproduced": result["historical_selection_reproduced"],
            "historical_corpus_digest": result["historical_corpus_digest"],
            "current_corpus_digest": digest, "context_files_verified": result["context_files_verified"],
            "overlay_paths": [numbers.TARGET_REL, candidate_check.v1.TARGET],
            "jeremiah_current_sha256": sha(TARGET.read_bytes()),
            "numbers_probe_under_jeremiah_baseline_view": result}


def current_export(raw, candidate):
    actual = exporter.export_book("JER")
    original = exporter.load_translation_record
    def with_target(record):
        def loader(book, chapter, verse):
            return copy.deepcopy(record) if (book, chapter, verse) == ("JER", 10, 10) else original(book, chapter, verse)
        with patch.object(exporter, "load_translation_record", side_effect=loader):
            return exporter.export_book("JER")
    before, after = with_target(yaml.safe_load(raw)), with_target(yaml.safe_load(candidate))
    def locate(book):
        return next(v for c in book["chapters"] if c["chapter"] == 10 for v in c["verses"] if v["verse"] == 10)
    patched = copy.deepcopy(after)
    row = locate(patched)
    row.clear()
    row.update(locate(before))
    if patched != before or locate(after) != json.loads(PREFLIGHT.read_text())["mobile_probe"]["draft_verse"]:
        raise ValueError("current export scope drift")
    return {"chapters": len(actual["chapters"]), "verses": sum(len(c["verses"]) for c in actual["chapters"]),
            "baseline_book_sha256": sha(jbytes(before)), "candidate_book_sha256": sha(jbytes(after)),
            "actual_book_sha256": sha(jbytes(actual)), "actual_matches_baseline": actual == before,
            "actual_matches_candidate": actual == after, "all_other_content_unchanged": True,
            "actual_verse": locate(actual), "deployed_reader_checked": False}


def check():
    raw, candidate, frozen = package()
    start = TARGET.read_bytes()
    with historical_view():
        if candidate_check.run(2) != frozen:
            raise ValueError("historical candidate preflight mismatch")
        dossier.check()
    historical = historical_sample_probe()
    exported = current_export(raw, candidate)
    if TARGET.read_bytes() != start:
        raise ValueError("canonical changed during check")
    return {**binding(), "current_target_sha256": sha(start), "candidate_preflight_reproduced": True,
            "dossier_contexts_reproduced": 11, "historical_sample": historical,
            "current_export": exported, "source_changed": False, "main_prose_changed": False,
            "whole_verse_reapproved": False, "publication_ready": False}


def prepare():
    if INTENT.exists() or APPLICATION.exists():
        raise ValueError("transaction already exists")
    require_review()
    result = check()
    if TARGET.read_bytes() != BASELINE.read_bytes():
        raise ValueError("prepare requires exact canonical baseline")
    record = {**binding(), "status": "prepared", "prepared_at": datetime.now(timezone.utc).isoformat(),
              "transaction_review_sha256": sha(REVIEW.read_bytes()), "preflight": result,
              "canonical_edit_mechanism": "Separate apply_patch of exact baseline to approved candidate; no canonical writer in this tool"}
    numbers.write_once(INTENT, record)
    return record


def complete():
    if APPLICATION.exists():
        raise ValueError("application already exists")
    require_transaction()
    if TARGET.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError("completion requires exact applied candidate")
    result = check()
    if not result["current_export"]["actual_matches_candidate"]:
        raise ValueError("actual canonical export differs from candidate")
    record = {**binding(), "status": "applied-verified", "completed_at": datetime.now(timezone.utc).isoformat(),
              "transaction_review_sha256": sha(REVIEW.read_bytes()), "intent_sha256": sha(INTENT.read_bytes()),
              "post_application": result, "canonical_note_change_applied": True,
              "source_changed": False, "main_prose_changed": False, "publication_ready": False}
    numbers.write_once(APPLICATION, record)
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--prepare", action="store_true")
    group.add_argument("--complete", action="store_true")
    args = parser.parse_args()
    print(json.dumps(prepare() if args.prepare else complete() if args.complete else check(), indent=2))
