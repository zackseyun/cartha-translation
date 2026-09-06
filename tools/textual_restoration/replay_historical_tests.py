"""Run receipt-bound historical tests against one trusted immutable Git snapshot.

Never validates or authorizes the current corpus. No current code is substituted
into the snapshot; current behavior needs separate tests. Requires local Git
history, Python's current installed dependencies, and temporary disk space.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from tools.textual_restoration.replay_unflagged_sample import extract_regular, git

ROOT = Path(__file__).resolve().parents[2]
COMMIT = "7637f998fd1edd9f7ab1acabf1e3037f2024b7e7"
_REGISTRY = "test_ot_witness_registry.OtWitnessRegistryTests."
SUITES = {
    "genesis": (["test_genesis_note_transaction"], 28),
    "unflagged": (["test_unflagged_english_sample"], 4),
    "registry_genesis": ([_REGISTRY + name for name in (
        "test_historical_pentateuch_comparison_with_named_genesis_baseline_view",
        "test_live_pentateuch_snapshot_reports_applied_genesis_note_drift",
        "test_historical_comparison_rejects_unknown_genesis_canonical_bytes",
        "test_historical_comparison_does_not_hide_unrelated_canonical_drift",
        "test_historical_control_comparison_detects_specific_mutated_baseline_hash",
    )], 5),
}
ARCHIVE_ROOTS = (
    "tools", "tests", "docs", "schema", "schemas", "translation/ot",
    "sources/ot", "sources/nt", "sources/lxx/swete",
    "sources/textual_restoration", "sources/dead_sea_scrolls",
    "sources/early_christian_texts/catalog.json",
    "METHODOLOGY.md", "REVISION_METHODOLOGY.md", "DOCTRINE.md",
)
_CHILD = """
import json, pathlib, sys, unittest
root = pathlib.Path.cwd()
sys.path[:0] = [str(root / 'tests'), str(root)]
suite = unittest.defaultTestLoader.loadTestsFromNames(json.loads(sys.argv[1]))
result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
print(json.dumps({'passed': result.wasSuccessful(), 'tests_run': result.testsRun,
                  'skipped': len(result.skipped),
                  'expected_failures': len(result.expectedFailures)}))
sys.exit(0 if result.wasSuccessful() else 1)
"""


def _archive_paths(repo):
    """Include exact derivative pins from the committed manifest, not live data."""
    rel = "sources/textual_restoration/applications/genesis4_8_newtransaction_inputs.v1.json"
    inputs = json.loads(git(repo, "show", f"{COMMIT}:{rel}"))
    extra = inputs["unchanged_derivative_context_pins"]
    # These are data only; refuse pathspec syntax, traversal and arbitrary roots.
    for path in extra:
        parts = Path(path).parts
        if (not path.startswith("translation_") or Path(path).is_absolute()
                or ".." in parts or any(c in path for c in "*?[:\\")):
            raise ValueError(f"Invalid historical derivative path: {path}")
    return [*ARCHIVE_ROOTS, *sorted(extra)]


def run_suite(name: str, *, repo: Path = ROOT):
    """A nonzero child, missing test, skipped check or wrong count is a failure."""
    if name not in SUITES:
        raise ValueError(f"Unknown historical suite: {name}")
    if sys.flags.optimize:
        raise ValueError("Historical replay requires non-optimized Python")
    resolved = git(repo, "rev-parse", "--verify", f"{COMMIT}^{{commit}}").decode().strip()
    if resolved != COMMIT:
        raise ValueError("Historical commit resolution mismatch")
    names, count = SUITES[name]
    archive = git(repo, "archive", "--format=tar", COMMIT, "--", *_archive_paths(repo))
    with tempfile.TemporaryDirectory(prefix="pob-historical-tests-") as directory:
        extract_regular(archive, Path(directory))
        del archive
        child = subprocess.run(
            [sys.executable, "-I", "-c", _CHILD, json.dumps(names)],
            cwd=directory, capture_output=True, text=True, timeout=600,
        )
    if child.returncode:
        raise RuntimeError(f"Historical {name} failed ({child.returncode}):\n{child.stderr}\n{child.stdout}")
    try:
        result = json.loads(child.stdout)
    except (ValueError, TypeError) as exc:
        raise RuntimeError("Historical child did not return its test result") from exc
    if (result.get("passed") is not True or result.get("tests_run") != count
            or result.get("skipped") != 0 or result.get("expected_failures") != 0):
        raise RuntimeError(f"Historical test coverage mismatch: {result}")
    return {**result, "suite": name, "commit": COMMIT,
            "current_corpus_validated": False, "application_approved": False}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", choices=tuple(SUITES))
    print(json.dumps(run_suite(parser.parse_args().suite), indent=2))
