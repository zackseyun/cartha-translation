"""Fail-closed note provenance and historical overlays; never write canonical data."""
from contextlib import contextmanager
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.textual_restoration import jeremiah_note_transaction as module


class JeremiahNoteTransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = module.BASELINE.read_bytes()
        cls.candidate = module.CANDIDATE.read_bytes()

    def setUp(self):
        self.review = {**module.binding(), "scoped_transaction_approved": True}
        self.review_raw = module.jbytes(self.review)
        self.intent = {**module.binding(), "status": "prepared",
                       "transaction_review_sha256": module.sha(self.review_raw)}
        self.intent_raw = module.jbytes(self.intent)
        self.application = {**module.binding(), "status": "applied-verified",
                            "transaction_review_sha256": module.sha(self.review_raw),
                            "intent_sha256": module.sha(self.intent_raw)}
        self.files = {module.REVIEW: self.review_raw, module.INTENT: self.intent_raw,
                      module.APPLICATION: None, module.TARGET: self.raw}

    @contextmanager
    def virtual_files(self, changes=None):
        """Overlay exact requested reads/existence; None means absent, no writes."""
        files = {**self.files, **(changes or {})}
        original_bytes, original_text, original_exists = Path.read_bytes, Path.read_text, Path.exists
        def read_bytes(path):
            if path not in files:
                return original_bytes(path)
            if files[path] is None:
                raise FileNotFoundError(path)
            return files[path]
        def read_text(path, *args, **kwargs):
            if path not in files:
                return original_text(path, *args, **kwargs)
            return read_bytes(path).decode("utf-8")
        def exists(path):
            return files[path] is not None if path in files else original_exists(path)
        with patch.object(Path, "read_bytes", read_bytes), patch.object(Path, "read_text", read_text), patch.object(Path, "exists", exists):
            yield files

    def test_actual_package_bytes_and_all_pins_are_valid(self):
        raw, candidate, _ = module.package()
        self.assertEqual((raw, candidate), (self.raw, self.candidate))

    def test_baseline_replay_does_not_require_candidate_transaction(self):
        with self.virtual_files({module.REVIEW: None, module.INTENT: None}):
            with module.historical_view():
                self.assertEqual(module.TARGET.read_bytes(), self.raw)
                self.assertEqual(module.TARGET.read_text(), self.raw.decode())

    def test_approved_candidate_replays_baseline_and_restores_current_reader(self):
        with self.virtual_files({module.TARGET: self.candidate}):
            with module.historical_view():
                self.assertEqual(module.TARGET.read_bytes(), self.raw)
                self.assertEqual(module.TARGET.read_text(), self.raw.decode())
            self.assertEqual(module.TARGET.read_bytes(), self.candidate)

    def test_unknown_canonical_state_is_rejected(self):
        with self.virtual_files({module.TARGET: self.candidate + b"\n"}):
            with self.assertRaisesRegex(ValueError, "unknown Jeremiah state"):
                with module.historical_view():
                    self.fail("Unknown bytes were exposed as historical baseline")

    def test_applied_ledger_rejects_canonical_rollback_to_baseline(self):
        with self.virtual_files({module.APPLICATION: module.jbytes(self.application)}):
            with self.assertRaisesRegex(ValueError, "baseline|rollback"):
                with module.historical_view():
                    self.fail("Applied ledger accepted canonical rollback")

    def test_baseline_with_pending_intent_requires_current_review(self):
        with self.virtual_files({module.REVIEW: None}):
            with self.assertRaises(FileNotFoundError):
                with module.historical_view():
                    self.fail("Pending intent bypassed review at baseline")
        stale = {**self.review, "executor_sha256": "stale"}
        with self.virtual_files({module.REVIEW: module.jbytes(stale)}):
            with self.assertRaisesRegex(ValueError, "missing or stale transaction review"):
                with module.historical_view():
                    self.fail("Pending intent accepted stale review")

    def test_baseline_with_pending_intent_requires_valid_intent_status(self):
        with self.virtual_files({module.INTENT: module.jbytes({**self.intent, "status": "failed"})}):
            with self.assertRaisesRegex(ValueError, "invalid transaction state"):
                with module.historical_view():
                    self.fail("Pending failed intent was ignored")

    def test_candidate_without_review_or_intent_is_rejected(self):
        for missing in (module.REVIEW, module.INTENT):
            with self.subTest(path=missing), self.virtual_files({module.TARGET: self.candidate, missing: None}):
                with self.assertRaises(FileNotFoundError):
                    with module.historical_view():
                        self.fail("Candidate accepted without provenance")

    def test_review_requires_explicit_approval_and_every_current_binding(self):
        mutations = [("scoped_transaction_approved", False)]
        mutations += [(key, "stale") for key in module.binding()]
        for key, value in mutations:
            review = {**self.review, key: value}
            with self.subTest(field=key), self.virtual_files({module.REVIEW: module.jbytes(review)}):
                with self.assertRaisesRegex(ValueError, "missing or stale transaction review"):
                    module.require_review()

    def test_prepared_intent_and_verified_application_are_both_accepted(self):
        with self.virtual_files():
            module.require_transaction()
        with self.virtual_files({module.APPLICATION: module.jbytes(self.application)}):
            module.require_transaction()

    def test_application_does_not_substitute_for_missing_intent(self):
        with self.virtual_files({module.INTENT: None, module.APPLICATION: module.jbytes(self.application)}):
            with self.assertRaises(FileNotFoundError):
                module.require_transaction()

    def test_each_ledger_requires_its_own_status(self):
        for path, original, wrong in (
            (module.INTENT, self.intent, "applied-verified"),
            (module.INTENT, self.intent, "failed"),
            (module.APPLICATION, self.application, "prepared"),
            (module.APPLICATION, self.application, "failed"),
        ):
            with self.subTest(path=path, status=wrong), self.virtual_files({path: module.jbytes({**original, "status": wrong})}):
                with self.assertRaisesRegex(ValueError, "invalid transaction state"):
                    module.require_transaction()

    def test_each_ledger_rejects_every_stale_binding_including_review_bytes(self):
        for path, original in ((module.INTENT, self.intent), (module.APPLICATION, self.application)):
            for key in (*module.binding(), "transaction_review_sha256"):
                with self.subTest(path=path, field=key), self.virtual_files({path: module.jbytes({**original, key: "stale"})}):
                    with self.assertRaisesRegex(ValueError, "transaction provenance drift"):
                        module.require_transaction()

    def test_application_requires_exact_intent_bytes(self):
        for value in ("stale", None):
            record = {**self.application, "intent_sha256": value}
            with self.subTest(value=value), self.virtual_files({module.APPLICATION: module.jbytes(record)}):
                with self.assertRaisesRegex(ValueError, "application intent binding drift"):
                    module.require_transaction()
        # Semantically equivalent JSON still has different receipt bytes.
        with self.virtual_files({module.INTENT: self.intent_raw + b"\n", module.APPLICATION: module.jbytes(self.application)}):
            with self.assertRaisesRegex(ValueError, "application intent binding drift"):
                module.require_transaction()

    def test_candidate_baseline_and_independent_judgment_byte_drift_fail(self):
        for path in (module.BASELINE, module.CANDIDATE, module.JUDGMENT):
            changed = path.read_bytes() + b"\n"
            with self.subTest(path=path), self.virtual_files({path: changed}):
                with self.assertRaisesRegex(ValueError, "drift"):
                    module.package()

    def test_every_bound_input_rejects_drift(self):
        pins = {}
        for path in (module.JUDGMENT, module.PREFLIGHT):
            pins.update(json.loads(path.read_text())["input_pins"])
        for relative in pins:
            path = module.ROOT / relative
            with self.subTest(path=relative), self.virtual_files({path: path.read_bytes() + b"\n"}):
                with self.assertRaisesRegex(ValueError, "drift"):
                    module.package()

    def test_baseline_view_rejects_concurrent_target_change(self):
        with self.virtual_files() as files:
            with self.assertRaisesRegex(ValueError, "canonical changed during historical replay"):
                with module.historical_view():
                    files[module.TARGET] = b"intervening edit\n"

    def test_prepare_never_overwrites_an_existing_ledger(self):
        for path in (module.INTENT, module.APPLICATION):
            with self.subTest(path=path), self.virtual_files({module.INTENT: None, module.APPLICATION: None, path: b"existing\n"}):
                with patch.object(module.numbers, "write_once") as write:
                    with self.assertRaises(ValueError):
                        module.prepare()
                    write.assert_not_called()

    def test_complete_never_overwrites_an_existing_application(self):
        with self.virtual_files({module.APPLICATION: module.jbytes(self.application)}):
            with patch.object(module.numbers, "write_once") as write:
                with self.assertRaisesRegex(ValueError, "application already exists"):
                    module.complete()
                write.assert_not_called()

    def test_complete_rejects_baseline_before_validation_or_write(self):
        with self.virtual_files():
            with patch.object(module, "check") as check, patch.object(module.numbers, "write_once") as write:
                with self.assertRaisesRegex(ValueError, "exact applied candidate"):
                    module.complete()
                check.assert_not_called()
                write.assert_not_called()

    def test_failed_post_application_export_cannot_write_completion(self):
        with self.virtual_files({module.TARGET: self.candidate}):
            with patch.object(module, "check", return_value={"current_export": {"actual_matches_candidate": False}}):
                with patch.object(module.numbers, "write_once") as write:
                    with self.assertRaisesRegex(ValueError, "actual canonical export differs"):
                        module.complete()
                    write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
