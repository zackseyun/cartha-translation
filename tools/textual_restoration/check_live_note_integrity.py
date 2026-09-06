"""Retain live integrity of three completed notes after historical-test migration.

This does not approve another edit or validate the whole corpus. The trusted Git
checkpoint supplies expected package bytes; current manifests cannot repin them.
Only the three explicitly reviewed test replacements supersede snapshot bytes.
"""
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import tarfile

from tools.textual_restoration.replay_historical_tests import COMMIT, ROOT, git

PREFIX = "sources/textual_restoration/applications/"
TARGETS = (
    "translation/ot/numbers/022/019.yaml",
    "translation/ot/jeremiah/010/010.yaml",
    "translation/ot/genesis/004/008.yaml",
)
MIGRATED_TESTS = {
    "tests/test_genesis_note_transaction.py": "92dfae53301b45aa80ae773d149ca6e285c168fa44ec7495aef4249831779d6f",
    "tests/test_unflagged_english_sample.py": "45ec3ce7bf12671f58007b3218611c949f85ea6c51b89f2f6f7adca57194653b",
    "tests/test_ot_witness_registry.py": "07330a278b8c2ea826c727cb454f28ffc906a1dc6bf54334aac7f6e8782aecfd",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


@lru_cache(maxsize=1)
def expected_files():
    """Read only the fixed checkpoint; return immutable expected-hash pairs."""
    if git(ROOT, "rev-parse", "--verify", f"{COMMIT}^{{commit}}").decode().strip() != COMMIT:
        raise ValueError("Historical commit resolution mismatch")
    preflight = json.loads(git(ROOT, "show", f"{COMMIT}:{PREFIX}genesis_4_8_note_preflight.v1.json"))
    inputs = json.loads(git(ROOT, "show", f"{COMMIT}:{PREFIX}genesis4_8_newtransaction_inputs.v1.json"))
    pins = {**preflight["input_pins"], **inputs["prior_package_input_pins"],
            **inputs["unchanged_derivative_context_pins"]}
    genesis_records = [p for p in git(ROOT, "ls-tree", "-r", "--name-only", COMMIT, "--", PREFIX).decode().splitlines()
                       if Path(p).name.startswith("genesis")]
    paths = sorted(set(pins) | set(genesis_records) | set(TARGETS) |
                   {"tools/genesis_note_transaction.py", "METHODOLOGY.md", "REVISION_METHODOLOGY.md",
                    "docs/GENESIS_4_8_NOTE_APPLICATION_2026-09-06.md"})
    archive = git(ROOT, "archive", "--format=tar", COMMIT, "--", *paths)
    expected = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar.getmembers():
            if member.isdir():
                continue
            if not member.isfile() or member.name not in paths:
                raise ValueError("Unexpected historical integrity member")
            expected[member.name] = sha(tar.extractfile(member).read())
    if set(expected) != set(paths):
        raise ValueError("Missing historical integrity input")
    for path, digest in pins.items():
        if expected[path] != digest:
            raise ValueError(f"Checkpoint does not match frozen input: {path}")
    expected.update(MIGRATED_TESTS)
    return tuple(sorted(expected.items()))


def check_current(root: Path = ROOT):
    root = root.resolve()
    expected = expected_files()
    for relative, digest in expected:
        path = root / relative
        if path.is_symlink() or path.resolve() != path.absolute():
            raise ValueError(f"Live integrity symlink refused: {relative}")
        if sha(path.read_bytes()) != digest:
            raise ValueError(f"Live completed-note integrity drift: {relative}")
    return {"completed_note_targets": list(TARGETS), "files_verified": len(expected),
            "checkpoint": COMMIT, "migrated_test_paths": list(MIGRATED_TESTS),
            "current_completed_note_integrity_verified": True,
            "current_corpus_validated": False, "new_application_approved": False}


if __name__ == "__main__":
    print(json.dumps(check_current(), indent=2))
