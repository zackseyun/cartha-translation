"""Current completed notes remain protected while historical tests use snapshots."""
from pathlib import Path
import json
import unittest
from unittest.mock import patch

from tools.textual_restoration import check_live_note_integrity as module


class LiveNoteIntegrityTests(unittest.TestCase):
    def test_current_completed_packages_and_explicit_migration_pass(self):
        result = module.check_current()
        self.assertTrue(result["current_completed_note_integrity_verified"])
        self.assertEqual(len(result["completed_note_targets"]), 3)
        self.assertFalse(result["current_corpus_validated"])
        self.assertFalse(result["new_application_approved"])

    def test_genesis_rollback_and_other_target_tampering_fail(self):
        reader = Path.read_bytes
        baseline = (module.ROOT / (module.PREFIX + "genesis_4_8_note_baseline.v1.yaml")).read_bytes()
        for relative in module.TARGETS:
            target = module.ROOT / relative
            changed = baseline if "genesis" in relative else reader(target) + b"\n"
            with self.subTest(path=relative), patch.object(Path, "read_bytes", lambda p: changed if p == target else reader(p)):
                with self.assertRaisesRegex(ValueError, "integrity drift"):
                    module.check_current()

    def test_receipt_source_executor_and_migrated_test_tampering_fail(self):
        reader = Path.read_bytes
        paths = [module.PREFIX + "genesis_4_8_note_application.v1.json",
                 module.PREFIX + "genesis4_8_newtransaction_review.v1.json",
                 "sources/ot/wlc/Gen.xml", "tools/genesis_note_transaction.py",
                 "docs/GENESIS_4_8_NOTE_APPLICATION_2026-09-06.md", *module.MIGRATED_TESTS]
        for relative in paths:
            target = module.ROOT / relative
            with self.subTest(path=relative), patch.object(Path, "read_bytes", lambda p: reader(p) + b"\n" if p == target else reader(p)):
                with self.assertRaisesRegex(ValueError, "integrity drift"):
                    module.check_current()

    def test_symlink_target_refused(self):
        target = module.ROOT / module.TARGETS[-1]
        original = Path.is_symlink
        with patch.object(Path, "is_symlink", lambda p: p == target or original(p)):
            with self.assertRaisesRegex(ValueError, "symlink"):
                module.check_current()

    def test_real_current_genesis_export_remains_checked(self):
        # Invoke only the unchanged export checker, not the historical package
        # entrypoint whose current-test bindings have explicitly been migrated.
        from tools import genesis_note_transaction as original

        module.check_current()
        result = original.current_export(
            original.BASELINE.read_bytes(), original.CANDIDATE.read_bytes(),
            json.loads(original.PREFLIGHT.read_text()))
        self.assertTrue(result["actual_export_outside_historical_overlays"])
        self.assertTrue(result["actual_matches_candidate"])
        self.assertTrue(result["all_other_content_unchanged"])
        self.assertEqual((result["chapters"], result["verses"]), (50, 1533))


if __name__ == "__main__":
    unittest.main()
