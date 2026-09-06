#!/usr/bin/env python3
"""Replay a committed sample in a private Git archive, never the live corpus.

This verifies historical reproducibility only. It authorizes no current edit,
accepts no current drift and does not replace existing transaction guards.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
import tempfile

from tools.textual_restoration import build_unflagged_english_sample as selector

BASE_COMMIT = "574f204de77e89c8abba04c72209bdf5efb317f9"
RECEIPT = "sources/textual_restoration/samples/unflagged_english_sample.selection.v1.json"
NUMBERS_TARGET = "translation/ot/numbers/022/019.yaml"
NUMBERS_BASELINE = "sources/textual_restoration/applications/numbers_22_19_note_baseline.v1.yaml"
NUMBERS_BASELINE_SHA = "74348f325b3cfb563c42c4d5075985ce833193d906dfdfe51a0bcc5eb88ff246"
NUMBERS_COMMITTED_SHA = "eee7a776befc2a210c8f5ca9e2a35cda3c93ae1ed7a4d90436dfe8ce5b608a77"
ROOT = Path(__file__).resolve().parents[2]


def git(repo, *args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(repo), *args])


def extract_regular(archive: bytes, destination: Path):
    """Validate every member before extracting; refuse links and special files."""
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        members = tar.getmembers()
        names = set()
        for member in members:
            name = PurePosixPath(member.name)
            if (name.is_absolute() or ".." in name.parts or not name.parts
                    or member.name in names or not (member.isfile() or member.isdir())):
                raise ValueError(f"Unsafe archive member: {member.name}")
            names.add(member.name)
        for member in members:
            target = destination / member.name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source, target.open("xb") as output:
                    shutil.copyfileobj(source, output)


def replay(repo: Path = ROOT, commit: str = BASE_COMMIT):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use a full immutable Git commit ID")
    resolved = git(repo, "rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()
    if resolved != commit:
        raise ValueError("Commit resolution mismatch")
    raw_receipt = git(repo, "show", f"{commit}:{RECEIPT}")
    expected = json.loads(raw_receipt)
    paths = ["sources/ot/wlc", "translation/ot", NUMBERS_BASELINE, *expected["protocol_inputs"]]
    # Execute only the installed selector, after verifying its two code inputs.
    # No code from the archive is imported or executed.
    for rel in ("tools/textual_restoration/build_unflagged_english_sample.py",
                "tools/textual_restoration/build_variant_inventory.py"):
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != expected["protocol_inputs"][rel]:
            raise ValueError(f"Installed selector dependency differs: {rel}")
    archive = git(repo, "archive", "--format=tar", commit, "--", *paths)
    with tempfile.TemporaryDirectory(prefix="pob-historical-sample-") as folder:
        extract_regular(archive, Path(folder))
        # The receipt was generated before NUM.22.19 changed in the same commit.
        # Its independently preserved application baseline is the sole substitution.
        baseline = (Path(folder) / NUMBERS_BASELINE).read_bytes()
        target = Path(folder) / NUMBERS_TARGET
        selected = expected["strata"]["torah"]["selected"]
        if (hashlib.sha256(baseline).hexdigest() != NUMBERS_BASELINE_SHA
                or hashlib.sha256(target.read_bytes()).hexdigest() != NUMBERS_COMMITTED_SHA
                or selected["path"] != NUMBERS_TARGET
                or selected["yaml_sha256"] != NUMBERS_BASELINE_SHA):
            raise ValueError("Historical Numbers baseline provenance mismatch")
        target.write_bytes(baseline)  # Private extracted tree only, never repo.
        actual = selector.build(Path(folder))
    if actual != expected:
        raise ValueError("Historical receipt mismatch")
    return {"commit": commit, "receipt_sha256": hashlib.sha256(raw_receipt).hexdigest(),
            "complete_receipt_equal": True, "corpus_files": actual["corpus_files"],
            "historical_corpus_digest": actual["corpus_digest"],
            "private_tree_substitutions": {NUMBERS_TARGET: NUMBERS_BASELINE_SHA},
            "current_corpus_validated": False, "application_approved": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", default=BASE_COMMIT)
    args = parser.parse_args()
    print(json.dumps(replay(commit=args.commit), indent=2))
