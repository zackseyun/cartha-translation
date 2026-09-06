"""Exact scope, lifecycle, drift and real-export checks for the note package."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml
from jsonschema import Draft202012Validator
from tools.textual_restoration import apply_numbers_22_19_note as module


class NumbersNoteApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw, cls.candidate, cls.plan = module.verify_package()
        cls.before, cls.after = yaml.safe_load(cls.raw), yaml.safe_load(cls.candidate)

    def test_byte_exact_baseline_candidate_and_plan_bindings(self):
        self.assertEqual(module.sha(self.raw), module.BASELINE_SHA)
        self.assertEqual(module.compose(self.raw), self.candidate)
        self.assertEqual(module.sha(self.candidate), self.plan["candidate_yaml_sha256"])

    def test_exhaustive_content_scope_and_single_correct_anchor(self):
        module.validate_scope(self.raw, self.candidate)
        self.assertEqual(self.before["source"], self.after["source"])
        for key in ("lexical_decisions", "theological_decisions", "ai_draft"):
            self.assertEqual(self.before[key], self.after[key])
        text = self.after["translation"]["text"]
        self.assertNotIn("tonight[a]", text)
        self.assertTrue(text.endswith("me[a]."))
        self.assertEqual(text.count("[a]"), 1)
        self.assertEqual(text.replace("[a]", ""), self.before["translation"]["text"].replace("[a]", ""))

    def test_old_states_are_archived_without_reapproval(self):
        self.assertEqual(self.after["cross_check"], {"status": "needs_review"})
        self.assertEqual(self.after["status"], "draft")
        self.assertNotIn("revision_pass", self.after)
        for entry in self.after["review_history"]:
            self.assertEqual(entry["value"], self.before[entry["field"]])
            self.assertEqual(entry["historical_review_input_binding"], "not-verified")
            self.assertFalse(entry["certifies_this_candidate"])
        self.assertFalse(self.after["note_application"]["whole_verse_reapproved"])
        self.assertFalse(self.after["note_application"]["publication_approval"])

    def test_unchanged_schema_accepts_candidate_and_exposes_old_status(self):
        validator = Draft202012Validator(json.loads((module.ROOT / "schema/verse.schema.json").read_text()))
        self.assertEqual([list(e.absolute_path) for e in validator.iter_errors(self.before)], [["status"]])
        self.assertEqual(list(validator.iter_errors(self.after)), [])

    def test_repeated_or_moved_wrong_anchor_cannot_pass_set_equality(self):
        for text in (module.AFTER_TEXT.replace("tonight", "tonight[a]"), module.BEFORE_TEXT):
            candidate = copy.deepcopy(self.after)
            candidate["translation"]["text"] = text
            with self.assertRaisesRegex(ValueError, "single final-clause"):
                module.validate_scope(self.raw, yaml.safe_dump(candidate).encode())

    def test_unrelated_lexical_edit_is_rejected(self):
        candidate = copy.deepcopy(self.after)
        candidate["lexical_decisions"][0]["chosen"] = "Something else"
        with self.assertRaisesRegex(ValueError, "Unapproved component"):
            module.validate_scope(self.raw, yaml.safe_dump(candidate).encode())

    def test_baseline_drift_and_unknown_historical_overlay_state_fail(self):
        with self.assertRaisesRegex(ValueError, "baseline drift"):
            module.compose(self.raw + b"\n")
        with self.assertRaisesRegex(ValueError, "Unknown current"):
            module.historical_bytes(module.ROOT / module.TARGET_REL, current_reader=lambda p: self.raw + b"\n")
        self.assertEqual(module.historical_bytes(module.ROOT / module.TARGET_REL, current_reader=lambda p: self.raw), self.raw)

    def test_all_six_frozen_protocol_inputs_reject_drift(self):
        selection = json.loads((module.ROOT / "sources/textual_restoration/samples/unflagged_english_sample.selection.v1.json").read_text())
        self.assertEqual(len(selection["protocol_inputs"]), 6)
        original_read = Path.read_bytes
        for relative in selection["protocol_inputs"]:
            with self.subTest(path=relative):
                changed = module.ROOT / relative
                def read_bytes(path):
                    raw = original_read(path)
                    return raw + b"\n# simulated criteria drift\n" if path == changed else raw
                with patch.object(Path, "read_bytes", new=read_bytes):
                    with self.assertRaisesRegex(ValueError, "Frozen protocol input changed"):
                        module.historical_sample_probe()

    def test_exact_byte_review_cannot_be_replaced_by_unbound_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "review.json"
            fake.write_text(json.dumps({"note_only_local_application_approved": True}))
            # Keep composition's canonical receipt locator stable; alter only read bytes.
            original_read = Path.read_text
            def read_text(path, *args, **kwargs):
                return original_read(fake) if path == module.JUDGMENT else original_read(path, *args, **kwargs)
            with patch.object(Path, "read_text", new=read_text):
                with self.assertRaisesRegex(ValueError, "exact-byte"):
                    module.verify_package(require_judgment=True)

    def test_atomic_swap_preserves_bytes_and_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory).resolve() / "verse.yaml"
            path.write_bytes(self.raw)
            path.chmod(0o640)
            module.atomic_replace_expected(path, self.raw, self.candidate)
            self.assertEqual(path.read_bytes(), self.candidate)
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            self.assertEqual(list(path.parent.glob(".num22-note-*")), [])

    def test_drift_between_staging_and_swap_preserves_intervening_write(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory).resolve() / "verse.yaml"
            path.write_bytes(self.raw)
            with self.assertRaisesRegex(ValueError, "immediately before"):
                module.atomic_replace_expected(path, self.raw, self.candidate, before_swap=lambda: path.write_bytes(b"intervening edit\n"))
            self.assertEqual(path.read_bytes(), b"intervening edit\n")
            self.assertEqual(list(path.parent.glob(".num22-note-*")), [])

    def test_symlink_target_and_existing_ledger_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory).resolve() / "verse.yaml"
            path.write_bytes(self.raw)
            alias = path.parent / "alias.yaml"
            alias.symlink_to(path)
            with self.assertRaisesRegex(ValueError, "symlinks"):
                module.atomic_replace_expected(alias, self.raw, self.candidate)
            with self.assertRaises(FileExistsError):
                module.write_once(path, {"unapproved": True})
            self.assertEqual(path.read_bytes(), self.raw)

    def test_real_complete_numbers_export(self):
        result = module.export_probe(self.raw, self.candidate)
        self.assertEqual((result["chapters"], result["verses"]), (36, 1289))
        self.assertTrue(result["single_final_anchor_preserved"])
        self.assertTrue(result["note_body_preserved"])
        self.assertTrue(result["all_other_book_content_unchanged"])
        self.assertFalse(result["research_history_exported"])
        self.assertFalse(result["source_object_exported"])
        self.assertFalse(result["deployed_reader_checked"])


if __name__ == "__main__":
    unittest.main()
