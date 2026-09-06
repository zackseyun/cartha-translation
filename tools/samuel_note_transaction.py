"""Exact Samuel disclosure transaction; canonical writes are separate apply_patch.

Default checks are read-only. Prepare/confirm exclusively create bound ledgers.
The candidate's entire note_proposal block remains historical preparation data;
the application ledger, not that old status string, records the actual state.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import yaml
from jsonschema import Draft202012Validator

from tools import export_mobile_bible as exporter
from tools.textual_restoration.check_live_note_integrity import check_current
from tools.textual_restoration.apply_numbers_22_19_note import write_once

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "sources/textual_restoration/applications"
PACKAGE = PREFIX / "samuel13_37_disclosure_candidate.v1.json"
CANDIDATE_REVIEW = PREFIX / "samuel13_37_disclosure_candidate_review.v1.json"
REVIEW = PREFIX / "samuel13_37_transaction_review.v1.json"
INTENT = PREFIX / "samuel13_37_application_intent.v1.json"
APPLICATION = PREFIX / "samuel13_37_application.v1.json"
TARGET = ROOT / "translation/ot/2_samuel/013/037.yaml"
PACKAGE_SHA = "55465d593a81c4d02dec1990d321e95784e0266d75e8f400c236a52ea6a47bfc"
CANDIDATE_REVIEW_SHA = "6242b086569b9c736997738f7b3c2b24bd9cc7ba508e4fdee3e22ccda1336e7f"
CORPUS = {
    "baseline": "89d6910840ac91c621fe2c929edd8add3eebb17e2229831a7a12ca253c936ec0",
    "candidate": "ebc5a784b4f4dc8773c6818297fb2d5e531329a685ab016171c6ee6f2df496c4",
}
BINDING_PATHS = (
    "tools/samuel_note_transaction.py", "tests/test_samuel_note_transaction.py",
    "docs/SAMUEL_13_37_NOTE_APPLICATION_2026-09-06.md",
    "tools/textual_restoration/check_live_note_integrity.py",
    "tools/textual_restoration/replay_historical_tests.py",
    "tools/textual_restoration/replay_unflagged_sample.py",
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def binding():
    return {"candidate_package_sha256": PACKAGE_SHA,
            "candidate_review_sha256": CANDIDATE_REVIEW_SHA,
            "implementation_pins": {p: sha((ROOT / p).read_bytes()) for p in BINDING_PATHS}}


def corpus_digest():
    files = sorted((ROOT / "translation/ot").glob("*/*/*.yaml"))
    return sha("".join(f"{p.relative_to(ROOT).as_posix()}\0{sha(p.read_bytes())}\n" for p in files).encode())


def package():
    require(sha(PACKAGE.read_bytes()) == PACKAGE_SHA, "candidate package drift")
    require(sha(CANDIDATE_REVIEW.read_bytes()) == CANDIDATE_REVIEW_SHA, "candidate review drift")
    p = json.loads(PACKAGE.read_text())
    r = json.loads(CANDIDATE_REVIEW.read_text())
    require(r["verdict"] == "APPROVE_EXACT_CANDIDATE_ONLY", "candidate approval scope drift")
    require(p["target"] == TARGET.relative_to(ROOT).as_posix(), "candidate target drift")
    for role in ("baseline", "candidate"):
        require(sha(p[role]["yaml_utf8"].encode()) == p[role]["sha256"], "embedded YAML drift")
    for rel, digest in {**p["input_pins"], **p["derivative_context"]["pinned_paths_sha256"], **r["bindings"]}.items():
        if ROOT / rel != TARGET:
            require(sha((ROOT / rel).read_bytes()) == digest, f"bound input drift: {rel}")
    before, after = (yaml.safe_load(p[role]["yaml_utf8"]) for role in ("baseline", "candidate"))
    for field in ("source", "lexical_decisions", "ai_draft"):
        require(before[field] == after[field], f"unapproved {field} change")
    plain = lambda text: re.sub(r"\[[a-z]+\]", "", text)
    require(plain(before["translation"]["text"]) == plain(after["translation"]["text"]), "main English changed")
    validator = Draft202012Validator(json.loads((ROOT / "schema/verse.schema.json").read_text()))
    require(not list(validator.iter_errors(after)), "candidate schema failure")
    return p


def require_review():
    r = json.loads(REVIEW.read_text())
    require(r.get("scoped_application_approved") is True and r.get("binding") == binding(), "missing or stale transaction review")
    require(all(r.get(k) is False for k in ("source_priority_approved", "whole_verse_reapproved", "publication_approved")), "transaction approval scope drift")
    return sha(REVIEW.read_bytes())


def verification(p, state, lifecycle, live):
    return {"state": state, "lifecycle": lifecycle, "yaml_sha256": p[state]["sha256"],
            "current_corpus_digest": CORPUS[state],
            "actual_full_2SA_export_sha256": p["preflight"][state + "_export"]["json_sha256"],
            "export_outside_historical_overlays": True, "chapters": 24, "verses": 695,
            "prior_completed_note_integrity": live, "source_changed": False,
            "main_english_changed": False, "whole_verse_reapproved": False,
            "deployed_reader_checked": False, "derivative_contexts_synchronized": False}


def ledger_state(state):
    if not INTENT.exists():
        require(state == "baseline" and not APPLICATION.exists(), "candidate or partial application lacks intent")
        return "unprepared"
    review_sha = require_review()
    intent = json.loads(INTENT.read_text())
    require(intent.get("status") == "prepared" and intent.get("binding") == binding()
            and intent.get("review_sha256") == review_sha, "intent binding or status drift")
    p, live = package(), check_current()
    require(intent.get("verification") == verification(p, "baseline", "unprepared", live), "intent baseline verification drift")
    if not APPLICATION.exists():
        return "prepared" if state == "baseline" else "awaiting-confirmation"
    record = json.loads(APPLICATION.read_text())
    require(state == "candidate", "applied ledger contradicts baseline rollback")
    require(record.get("status") == "applied-verified" and record.get("binding") == binding()
            and record.get("review_sha256") == review_sha
            and record.get("intent_sha256") == sha(INTENT.read_bytes()), "application binding or status drift")
    require(record.get("verification") == verification(p, "candidate", "awaiting-confirmation", live), "application verification drift")
    require(record.get("note_proposal_role") == "historical-preparation-metadata-not-current-status", "proposal lifecycle ambiguity")
    require(record.get("publication_approved") is False, "application publication scope drift")
    return "applied-verified"


def check():
    p = package()
    require(not TARGET.is_symlink() and TARGET.resolve() == TARGET.absolute(), "canonical symlink refused")
    raw = TARGET.read_bytes()
    states = {p[role]["yaml_utf8"].encode(): role for role in ("baseline", "candidate")}
    require(raw in states, "unknown canonical bytes")
    state = states[raw]
    initial_binding = binding()
    lifecycle = ledger_state(state)
    live = check_current()
    start = corpus_digest()
    require(start == CORPUS[state], "unrelated current corpus drift")
    book = exporter.export_book("2SA")
    require(len(book["chapters"]) == 24 and sum(len(c["verses"]) for c in book["chapters"]) == 695, "incomplete 2SA export")
    export_sha = sha(json.dumps(book, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())
    require(export_sha == p["preflight"][state + "_export"]["json_sha256"], "actual full-book export drift")
    package()
    require(binding() == initial_binding and TARGET.read_bytes() == raw and corpus_digest() == start, "inputs changed during check")
    require(ledger_state(state) == lifecycle, "ledger changed during check")
    return verification(p, state, lifecycle, live)


def prepare():
    require(not INTENT.exists() and not APPLICATION.exists(), "transaction already exists")
    review_sha = require_review()
    result = check()
    require(result["state"] == "baseline", "prepare requires baseline")
    require(require_review() == review_sha, "review changed during prepare")
    record = {"status": "prepared", "created": datetime.now(timezone.utc).isoformat(),
              "binding": binding(), "review_sha256": review_sha, "verification": result}
    write_once(INTENT, record)
    return record


def confirm():
    require(INTENT.exists() and not APPLICATION.exists(), "confirmation requires intent and no application")
    review_sha, intent_sha = require_review(), sha(INTENT.read_bytes())
    result = check()
    require(result["state"] == "candidate", "confirmation requires exact candidate")
    require(require_review() == review_sha and sha(INTENT.read_bytes()) == intent_sha, "review or intent changed during confirmation")
    record = {"status": "applied-verified", "created": datetime.now(timezone.utc).isoformat(),
              "binding": binding(), "review_sha256": review_sha, "intent_sha256": intent_sha,
              "note_proposal_role": "historical-preparation-metadata-not-current-status",
              "verification": result, "publication_approved": False}
    write_once(APPLICATION, record)
    return record


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "prepare", "confirm"), default="check", nargs="?")
    print(json.dumps({"check": check, "prepare": prepare, "confirm": confirm}[parser.parse_args().mode](), indent=2))
