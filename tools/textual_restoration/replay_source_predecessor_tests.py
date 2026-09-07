"""Replay exactly 19 unchanged predecessor tests once per process.

Tests, verifiers and data come entirely from the fixed checkpoint. Its trusted
code uses local Git history for read-only checkpoint queries. The two current
wrappers share this cached result; it does not validate today's corpus or
approve source changes. Requires local history and installed Python dependencies.
"""
from functools import lru_cache
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from tools.textual_restoration.replay_historical_tests import _archive_paths, _CHILD
from tools.textual_restoration.replay_unflagged_sample import extract_regular, git

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT = "783e61ec70c5a152468f5cbe619656e0857182d4"
SUITES = {
    "corpus_successor": ("test_corpus_successor.CorpusSuccessorTests.", (
        "test_actual_complete_current_exports_and_corpus",
        "test_untrusted_review_plan_and_scope_fail",
        "test_each_reviewed_implementation_and_protected_input_rejects_drift",
        "test_source_and_candidate_pins_reject_drift",
        "test_empty_duplicate_unknown_and_completed_targets_fail",
        "test_changed_source_english_history_and_stale_review_rejected_even_if_repinned",
        "test_unapproved_added_deleted_or_changed_corpus_fails",
        "test_wrong_or_missing_book_export_expectation_fails",
        "test_partial_multi_target_application_fails",
        "test_mid_check_corpus_drift_fails",
        "test_inventory_includes_unexpected_depth_and_rejects_parent_symlink",
        "test_application_receipt_rejects_rollback_stale_bytes_and_wrong_trust",
    )),
    "source_composition": ("test_source_composition.SourceCompositionTests.", (
        "test_both_real_candidates_without_promotion",
        "test_normalization_preserves_consonants_and_punctuation",
        "test_unchanged_base_coordinates_for_multiple_patches",
        "test_overlap_wrong_unit_and_missing_evidence_fail",
        "test_drift_unsafe_path_duplicate_and_extra_field_fail",
        "test_repinning_candidate_does_not_hide_extra_source_change_or_approval",
        "test_symlink_evidence_rejected",
    )),
}


@lru_cache(maxsize=1)
def replay():
    """One shared real child execution; no skips, expected failures or repins."""
    if sys.flags.optimize:
        raise ValueError("Historical replay requires non-optimized Python")
    if git(ROOT, "rev-parse", "--verify", CHECKPOINT + "^{commit}").decode().strip() != CHECKPOINT:
        raise ValueError("Historical checkpoint resolution mismatch")
    names = [prefix + name for prefix, methods in SUITES.values() for name in methods]
    counts = {name: len(methods) for name, (_, methods) in SUITES.items()}
    if counts != {"corpus_successor": 12, "source_composition": 7} or len(set(names)) != 19:
        raise ValueError("Historical suite selection mismatch")
    package_path = "sources/textual_restoration/applications/samuel13_37_disclosure_candidate.v1.json"
    package = json.loads(git(ROOT, "show", f"{CHECKPOINT}:{package_path}"))
    paths = [*_archive_paths(ROOT), *package["derivative_context"]["pinned_paths_sha256"]]
    archive = git(ROOT, "archive", "--format=tar", CHECKPOINT, "--", *paths)
    with tempfile.TemporaryDirectory(prefix="pob-source-predecessor-") as directory:
        extract_regular(archive, Path(directory))
        del archive
        env = dict(os.environ, GIT_DIR=git(ROOT, "rev-parse", "--absolute-git-dir").decode().strip(),
                   GIT_WORK_TREE=directory, GIT_OPTIONAL_LOCKS="0")
        child = subprocess.run([sys.executable, "-I", "-B", "-c", _CHILD, json.dumps(names)],
                               cwd=directory, env=env, capture_output=True, text=True, timeout=600)
    if child.returncode:
        raise RuntimeError("Historical source predecessor tests failed:\n" + child.stderr + child.stdout)
    try:
        result = json.loads(child.stdout)
    except (ValueError, TypeError) as exc:
        raise RuntimeError("Historical child did not return its test result") from exc
    if result != {"passed": True, "tests_run": 19, "skipped": 0, "expected_failures": 0}:
        raise RuntimeError(f"Historical test coverage mismatch: {result}")
    return {**result, "checkpoint": CHECKPOINT, "suite_test_counts": counts,
            "shared_replay_cached_per_process": True,
            "current_corpus_validated": False, "application_approved": False}


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2))
