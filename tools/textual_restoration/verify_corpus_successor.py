"""Read-only verification of explicitly reviewed note/metadata successor states.

The caller supplies a trusted review SHA, not a hash discovered from the plan.
This validates stated scope/bytes; it cannot authenticate scholarly judgment.
Canonical edits and application records are separate authorized operations.
"""
from functools import lru_cache
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

import yaml
from jsonschema import Draft202012Validator

from tools import export_mobile_bible as exporter
from tools.textual_restoration.check_live_note_integrity import check_current
from tools.textual_restoration.replay_historical_tests import _archive_paths, _CHILD
from tools.textual_restoration.replay_unflagged_sample import extract_regular, git

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT = "9af0a131c7f6368217cf1c33a3d7f4bf3c231de1"
PREFIX = "sources/textual_restoration/applications/"
WRAPPER = "tests/test_samuel_note_transaction.py"
BINDINGS = ("tools/textual_restoration/verify_corpus_successor.py", WRAPPER,
            "tests/test_corpus_successor.py", "docs/CORPUS_SUCCESSOR_VERIFICATION.md")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def json_sha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def safe_read(root, relative):
    path = Path(relative)
    require(not path.is_absolute() and path.as_posix() == relative
            and path.parts and ".." not in path.parts, "unsafe relative path")
    target = root / path
    require(target.resolve() == target.absolute() and not target.is_symlink(), "symlink refused")
    return target.read_bytes()


@lru_cache(maxsize=1)
def checkpoint():
    require(git(ROOT, "rev-parse", "--verify", CHECKPOINT + "^{commit}").decode().strip() == CHECKPOINT,
            "checkpoint mismatch")
    require(git(ROOT, "rev-parse", "--show-object-format").decode().strip() == "sha1", "unsupported Git object format")
    tree = {}
    for entry in git(ROOT, "ls-tree", "-rz", CHECKPOINT, "--", "translation/ot").split(b"\0"):
        if not entry:
            continue
        meta, path = entry.decode().split("\t", 1)
        mode, kind, oid = meta.split()
        require(mode == "100644" and kind == "blob", "nonregular checkpoint corpus entry")
        if path.endswith(".yaml"):
            tree[path] = oid
    require(bool(tree), "empty checkpoint corpus")
    return tree


@lru_cache(maxsize=1)
def protected():
    """Frozen Samuel and transitive completed-note obligations; never live repins."""
    def read(name):
        return json.loads(git(ROOT, "show", f"{CHECKPOINT}:{PREFIX}{name}"))
    package = read("samuel13_37_disclosure_candidate.v1.json")
    review = read("samuel13_37_disclosure_candidate_review.v1.json")
    transaction = read("samuel13_37_transaction_review.v1.json")
    pins = {**package["input_pins"], **package["derivative_context"]["pinned_paths_sha256"],
            **review["bindings"], **transaction["binding"]["implementation_pins"]}
    # The old package pins its pre-application target; current checkpoint has the applied note.
    pins.pop(package["target"])
    paths = set(pins) | {package["target"]}
    paths.update(PREFIX + name for name in (
        "samuel13_37_disclosure_candidate.v1.json", "samuel13_37_disclosure_candidate_review.v1.json",
        "samuel13_37_transaction_review.v1.json", "samuel13_37_application_intent.v1.json",
        "samuel13_37_application.v1.json"))
    expected = {}
    raw = git(ROOT, "archive", "--format=tar", CHECKPOINT, "--", *sorted(paths))
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        for member in archive.getmembers():
            if member.isdir():
                continue
            require(member.isfile() and member.name in paths, "unexpected protected input")
            expected[member.name] = sha(archive.extractfile(member).read())
    require(set(expected) == paths, "missing protected input")
    for path, digest in pins.items():
        require(expected[path] == digest, "checkpoint contradicts frozen binding")
    expected.pop(WRAPPER)  # Only this migrated consumer is superseded by reviewed current bytes.
    return expected, package["preflight"]["candidate_export"]["json_sha256"]


def current_corpus(root):
    base = root / "translation/ot"
    require(base.resolve() == base.absolute() and base.is_dir(), "corpus directory symlink or missing")
    result = {}
    for directory, directories, files in os.walk(base, followlinks=False):
        for name in directories + files:
            require(not (Path(directory) / name).is_symlink(), "corpus symlink refused")
        for name in files:
            if name.endswith(".yaml"):
                path = Path(directory) / name
                result[path.relative_to(root).as_posix()] = blob(path.read_bytes())
    return result


def verify(plan_path, review_path, review_sha256, *, root=ROOT):
    """Both exact baseline and complete candidate are valid observations, not writes."""
    root = root.resolve()
    review_raw = safe_read(root, review_path)
    require(sha(review_raw) == review_sha256, "trusted review hash mismatch")
    review = json.loads(review_raw)
    plan_raw = safe_read(root, plan_path)
    require(review.get("plan_sha256") == sha(plan_raw), "plan review binding mismatch")
    require(review.get("scoped_application_approved") is True
            and all(review.get(k) is False for k in ("source_priority_approved", "whole_verse_reapproved", "publication_approved")),
            "review scope mismatch")
    require(set(review.get("implementation_pins", {})) == set(BINDINGS), "missing implementation bindings")
    for path, digest in review["implementation_pins"].items():
        require(sha(safe_read(root, path)) == digest, "implementation drift")
    plan = json.loads(plan_raw)
    require(plan.get("checkpoint") == CHECKPOINT and plan.get("scope") == "note-and-metadata-only", "unsupported plan scope")
    expected = dict(checkpoint())
    pins, samuel_export = protected()
    for path, digest in pins.items():
        require(sha(safe_read(root, path)) == digest, "protected package drift: " + path)
    live = check_current(root)
    protected_targets = set(live["completed_note_targets"]) | {"translation/ot/2_samuel/013/037.yaml"}
    require(isinstance(plan.get("input_pins"), dict) and plan["input_pins"], "missing source inputs")
    for path, digest in plan["input_pins"].items():
        require(sha(safe_read(root, path)) == digest, "plan input drift")
    require(isinstance(plan.get("changes"), list) and plan["changes"], "empty successor plan")
    validator = Draft202012Validator(json.loads(safe_read(root, "schema/verse.schema.json")))
    affected, seen, candidate_tree = set(), set(), dict(expected)
    for change in plan["changes"]:
        target = change["target"]
        require(target in expected and target not in seen and target not in protected_targets, "unknown, duplicate or protected target")
        seen.add(target)
        before_raw = git(ROOT, "show", f"{CHECKPOINT}:{target}")
        after_raw = safe_read(root, change["candidate"])
        require(sha(before_raw) == change["before_sha256"] and sha(after_raw) == change["after_sha256"], "candidate/baseline drift")
        before, after = yaml.safe_load(before_raw), yaml.safe_load(after_raw)
        require(not list(validator.iter_errors(after)), "candidate schema failure")
        for key in ("id", "reference", "source", "ai_draft", "revisions"):
            require(before.get(key) == after.get(key), "unauthorized source/history change")
        require(before["translation"]["text"] == after["translation"]["text"]
                and before["translation"]["philosophy"] == after["translation"]["philosophy"], "main English change")
        require(after.get("status") == "draft" and after.get("cross_check", {}).get("status") == "needs_review", "stale review status")
        affected.add(before["id"].split(".")[0])
        candidate_tree[target] = blob(after_raw)
    start = current_corpus(root)
    require(start == expected or start == candidate_tree, "unapproved corpus state (including partial application)")
    state = "baseline" if start == expected else "candidate"
    require(set(plan.get("books", {})) == affected, "affected-book coverage mismatch")
    exports = {}
    # The normal exporter is used only on its real repository, never on an in-memory overlay.
    require(root == ROOT, "actual export requires repository root")
    for code in sorted(affected | {"2SA"}):
        book = exporter.export_book(code)
        chapters = len(book["chapters"])
        verses = sum(len(ch["verses"]) for ch in book["chapters"])
        digest = json_sha(book)
        if code == "2SA":
            require((chapters, verses, digest) == (24, 695, samuel_export), "protected Samuel export drift")
        if code in affected:
            spec = plan["books"][code]
            require((chapters, verses, digest) == (spec["chapters"], spec["verses"], spec[state + "_export_sha256"]), "affected-book export drift")
        exports[code] = {"chapters": chapters, "verses": verses, "sha256": digest}
    require(current_corpus(root) == start, "corpus changed during verification")
    require(safe_read(root, review_path) == review_raw and safe_read(root, plan_path) == plan_raw, "review/plan changed during verification")
    for path, digest in {**pins, **review["implementation_pins"], **plan["input_pins"]}.items():
        require(sha(safe_read(root, path)) == digest, "bound input changed during verification")
    for change in plan["changes"]:
        require(sha(safe_read(root, change["candidate"])) == change["after_sha256"], "candidate changed during verification")
    require(check_current(root) == live, "prior integrity changed during verification")
    return {"state": state, "checkpoint": CHECKPOINT, "review_sha256": review_sha256,
            "plan_sha256": sha(plan_raw), "canonical_yaml_count": len(start), "actual_exports": exports,
            "current_corpus_verified": True, "canonical_files_written": False,
            "publication_approved": False, "whole_verse_reapproved": False}


def verify_applied(plan_path, review_path, review_sha256, application_path, application_sha256):
    """Check a previously recorded application using an externally trusted digest."""
    raw = safe_read(ROOT, application_path)
    require(sha(raw) == application_sha256, "trusted application hash mismatch")
    record = json.loads(raw)
    require(record.get("status") == "applied-verified" and record.get("publication_approved") is False,
            "application record scope mismatch")
    actual = verify(plan_path, review_path, review_sha256)
    require(actual["state"] == "candidate" and record.get("after") == actual, "application rollback or stale record")
    before = record.get("before", {})
    require(before.get("state") == "baseline" and before.get("checkpoint") == CHECKPOINT
            and before.get("review_sha256") == review_sha256 and before.get("plan_sha256") == actual["plan_sha256"],
            "application baseline binding mismatch")
    require(safe_read(ROOT, application_path) == raw, "application changed during verification")
    return {**actual, "application_record_verified": True, "application_sha256": application_sha256}


def historical_samuel_tests():
    """Legacy adapter only: original 11 tests/code/data, plus read-only Git history."""
    checkpoint()
    package = json.loads(git(ROOT, "show", f"{CHECKPOINT}:{PREFIX}samuel13_37_disclosure_candidate.v1.json"))
    paths = [*_archive_paths(ROOT), *package["derivative_context"]["pinned_paths_sha256"]]
    raw = git(ROOT, "archive", "--format=tar", CHECKPOINT, "--", *paths)
    with tempfile.TemporaryDirectory(prefix="pob-samuel-history-") as directory:
        extract_regular(raw, Path(directory))
        del raw
        env = dict(os.environ, GIT_DIR=git(ROOT, "rev-parse", "--absolute-git-dir").decode().strip(), GIT_WORK_TREE=directory)
        child = subprocess.run([sys.executable, "-I", "-c", _CHILD, '["test_samuel_note_transaction"]'],
                               cwd=directory, env=env, capture_output=True, text=True, timeout=600)
    require(child.returncode == 0, "historical Samuel failed: " + child.stderr + child.stdout)
    result = json.loads(child.stdout)
    require(result == {"passed": True, "tests_run": 11, "skipped": 0, "expected_failures": 0}, "historical coverage mismatch")
    return {**result, "checkpoint": CHECKPOINT, "current_corpus_validated": False}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan")
    parser.add_argument("review")
    parser.add_argument("--review-sha256", required=True, help="Trusted independent review digest; do not calculate from untrusted input")
    parser.add_argument("--application")
    parser.add_argument("--application-sha256")
    args = parser.parse_args()
    require(bool(args.application) == bool(args.application_sha256), "application path and trusted hash required together")
    result = (verify_applied(args.plan, args.review, args.review_sha256, args.application, args.application_sha256)
              if args.application else verify(args.plan, args.review, args.review_sha256))
    print(json.dumps(result, indent=2))
