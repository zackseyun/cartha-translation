"""Synthetic approvals exercise mechanics; none is an application approval."""
import copy
from functools import lru_cache
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from tools.textual_restoration import verify_corpus_successor as m

TARGET = "translation/ot/job/013/015.yaml"
CANDIDATE = m.PREFIX + "job13_15_disclosure_candidate.v1.yaml"
PLAN = "synthetic-plan.json"
REVIEW = "synthetic-review.json"


def encode(value):
    return json.dumps(value, ensure_ascii=False).encode()


@lru_cache(maxsize=1)
def plan_fixture():
    return {"checkpoint": m.CHECKPOINT, "scope": "note-and-metadata-only",
            "input_pins": {"sources/ot/wlc/Job.xml": m.sha((m.ROOT / "sources/ot/wlc/Job.xml").read_bytes())},
            "changes": [{"target": TARGET, "candidate": CANDIDATE,
                         "before_sha256": "111d4cebd2ee664ec2097a4fb21c92f54aba525b3ff0f30f0f35c769c3eebab4",
                         "after_sha256": "5d32a6ef2913547460cacdc7e0192dfb6468c9c331af5325fee9f5f217ddc033"}],
            "books": {"JOB": {"chapters": 42, "verses": 1070,
                              "baseline_export_sha256": "b7d20eb2076ab7755ff0b38fb883d8a6afcfe144e2121e24b05dd8202f59d56b",
                              "candidate_export_sha256": "84e15083b995f89b034e3fc69fa97c06e5b617258d401b298b4fa460c367e40f"}}}


class CorpusSuccessorTests(unittest.TestCase):
    def exercise(self, *, plan=None, review_changes=None, overrides=None, trusted=None):
        plan = copy.deepcopy(plan if plan is not None else plan_fixture())
        review = {"plan_sha256": m.sha(encode(plan)), "scoped_application_approved": True,
                  "source_priority_approved": False, "whole_verse_reapproved": False, "publication_approved": False,
                  "implementation_pins": {p: m.sha((m.ROOT / p).read_bytes()) for p in m.BINDINGS}}
        review.update(review_changes or {})
        files = {PLAN: encode(plan), REVIEW: encode(review), **(overrides or {})}
        reader = m.safe_read
        with patch.object(m, "safe_read", lambda root, p: files[p] if p in files else reader(root, p)):
            return m.verify(PLAN, REVIEW, trusted or m.sha(files[REVIEW]))

    def test_actual_complete_current_exports_and_corpus(self):
        result = self.exercise()
        self.assertIn(result["state"], ("baseline", "candidate"))
        self.assertTrue(result["current_corpus_verified"])
        self.assertEqual(result["actual_exports"]["JOB"]["verses"], 1070)
        self.assertEqual(result["actual_exports"]["2SA"]["verses"], 695)
        self.assertFalse(result["canonical_files_written"])
        self.assertFalse(result["publication_approved"])

    def test_untrusted_review_plan_and_scope_fail(self):
        for changes in ({"plan_sha256": "0" * 64}, {"scoped_application_approved": False},
                        {"publication_approved": True}, {"implementation_pins": {}}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.exercise(review_changes=changes)
        with self.assertRaisesRegex(ValueError, "trusted review"):
            self.exercise(trusted="0" * 64)

    def test_each_reviewed_implementation_and_protected_input_rejects_drift(self):
        for path in [*m.BINDINGS, *m.protected()[0]]:
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "drift"):
                self.exercise(overrides={path: (m.ROOT / path).read_bytes() + b"\n"})

    def test_source_and_candidate_pins_reject_drift(self):
        for path in ("sources/ot/wlc/Job.xml", CANDIDATE):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "drift"):
                self.exercise(overrides={path: (m.ROOT / path).read_bytes() + b"\n"})

    def test_empty_duplicate_unknown_and_completed_targets_fail(self):
        for targets in ([], [TARGET, TARGET], ["translation/ot/job/999/999.yaml"],
                        ["translation/ot/2_samuel/013/037.yaml"], ["translation/ot/genesis/004/008.yaml"]):
            plan = copy.deepcopy(plan_fixture())
            plan["changes"] = [{**plan["changes"][0], "target": t} for t in targets]
            with self.subTest(targets=targets), self.assertRaises(ValueError):
                self.exercise(plan=plan)

    def test_changed_source_english_history_and_stale_review_rejected_even_if_repinned(self):
        original = yaml.safe_load((m.ROOT / CANDIDATE).read_bytes())
        mutations = [lambda c: c["source"].update(text="different"),
                     lambda c: c["translation"].update(text="different"),
                     lambda c: c.update(revisions=[]), lambda c: c.update(status="revised")]
        for mutate in mutations:
            candidate = copy.deepcopy(original)
            mutate(candidate)
            raw = yaml.safe_dump(candidate, allow_unicode=True).encode()
            plan = copy.deepcopy(plan_fixture())
            plan["changes"][0]["after_sha256"] = m.sha(raw)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                self.exercise(plan=plan, overrides={CANDIDATE: raw})

    def test_unapproved_added_deleted_or_changed_corpus_fails(self):
        baseline = dict(m.checkpoint())
        states = [{**baseline, "translation/ot/job/deeper/001/001.yaml": "x"},
                  {p: v for p, v in baseline.items() if p != TARGET},
                  {**baseline, "translation/ot/job/001/001.yaml": "x"}]
        for state in states:
            with self.subTest(), patch.object(m, "current_corpus", return_value=state), self.assertRaisesRegex(ValueError, "unapproved corpus"):
                self.exercise()

    def test_wrong_or_missing_book_export_expectation_fails(self):
        plan = copy.deepcopy(plan_fixture())
        plan["books"] = {}
        with self.assertRaisesRegex(ValueError, "coverage"):
            self.exercise(plan=plan)
        with patch.object(m.exporter, "export_book", return_value={"chapters": []}), self.assertRaisesRegex(ValueError, "export drift"):
            self.exercise()

    def test_partial_multi_target_application_fails(self):
        other = "translation/ot/job/013/016.yaml"
        before_raw = m.git(m.ROOT, "show", f"{m.CHECKPOINT}:{other}")
        after = yaml.safe_load(before_raw)
        after.update(status="draft", cross_check={"status": "needs_review"})
        after_raw = yaml.safe_dump(after, allow_unicode=True).encode()
        plan = copy.deepcopy(plan_fixture())
        plan["changes"].append({"target": other, "candidate": "synthetic-other.yaml",
                                "before_sha256": m.sha(before_raw), "after_sha256": m.sha(after_raw)})
        partial = {**m.checkpoint(), TARGET: m.blob((m.ROOT / CANDIDATE).read_bytes())}
        with patch.object(m, "current_corpus", return_value=partial), self.assertRaisesRegex(ValueError, "partial application"):
            self.exercise(plan=plan, overrides={"synthetic-other.yaml": after_raw})

    def test_mid_check_corpus_drift_fails(self):
        first = m.current_corpus(m.ROOT)
        changed = {**first, TARGET: "unexpected"}
        with patch.object(m, "current_corpus", side_effect=[first, changed]), self.assertRaisesRegex(ValueError, "changed during"):
            self.exercise()

    def test_inventory_includes_unexpected_depth_and_rejects_parent_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            nested = root / "translation/ot/job/deeper/001/001.yaml"
            nested.parent.mkdir(parents=True)
            nested.write_bytes(b"fixture")
            self.assertEqual(set(m.current_corpus(root)), {nested.relative_to(root).as_posix()})
            (root / "translation/ot/alias").symlink_to(nested.parent, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                m.current_corpus(root)
            with self.assertRaisesRegex(ValueError, "symlink"):
                m.safe_read(root, "translation/ot/alias/001.yaml")
        for path in ("../outside", "/outside", "a/../b", "a//b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                m.safe_read(m.ROOT, path)

    def test_application_receipt_rejects_rollback_stale_bytes_and_wrong_trust(self):
        actual = {"state": "candidate", "checkpoint": m.CHECKPOINT,
                  "review_sha256": "r", "plan_sha256": "p"}
        record = {"status": "applied-verified", "publication_approved": False,
                  "before": {**actual, "state": "baseline"}, "after": actual}
        raw = encode(record)
        with patch.object(m, "safe_read", return_value=raw), patch.object(m, "verify", return_value=actual):
            self.assertTrue(m.verify_applied(PLAN, REVIEW, "r", "application.json", m.sha(raw))["application_record_verified"])
            with self.assertRaisesRegex(ValueError, "trusted application"):
                m.verify_applied(PLAN, REVIEW, "r", "application.json", "0" * 64)
        for changed in ({**actual, "state": "baseline"}, {**actual, "plan_sha256": "changed"}):
            with patch.object(m, "safe_read", return_value=raw), patch.object(m, "verify", return_value=changed), self.assertRaisesRegex(ValueError, "rollback or stale"):
                m.verify_applied(PLAN, REVIEW, "r", "application.json", m.sha(raw))


if __name__ == "__main__":
    unittest.main()
