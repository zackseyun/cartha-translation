"""Exact transaction guards; all application/ledger simulations are in memory."""
from contextlib import contextmanager
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools import samuel_note_transaction as module


class SamuelNoteTransactionTests(unittest.TestCase):
    def setUp(self):
        self.p = module.package()
        self.raw = self.p["baseline"]["yaml_utf8"].encode()
        self.candidate = self.p["candidate"]["yaml_utf8"].encode()
        self.review = {"scoped_application_approved": True, "binding": module.binding(),
                       "source_priority_approved": False, "whole_verse_reapproved": False, "publication_approved": False}
        self.review_bytes = self.encode(self.review)
        self.live = module.check_current()
        self.intent = {"status": "prepared", "binding": module.binding(),
                       "review_sha256": module.sha(self.review_bytes),
                       "verification": module.verification(self.p, "baseline", "unprepared", self.live)}
        self.intent_bytes = self.encode(self.intent)
        self.application = {"status": "applied-verified", "binding": module.binding(),
                            "review_sha256": module.sha(self.review_bytes),
                            "intent_sha256": module.sha(self.intent_bytes),
                            "verification": module.verification(self.p, "candidate", "awaiting-confirmation", self.live),
                            "note_proposal_role": "historical-preparation-metadata-not-current-status",
                            "publication_approved": False}

    @staticmethod
    def encode(value):
        return json.dumps(value, ensure_ascii=False).encode()

    @contextmanager
    def virtual(self, **states):
        files = {module.TARGET: self.raw, module.REVIEW: self.review_bytes,
                 module.INTENT: None, module.APPLICATION: None}
        files.update({getattr(module, key): value for key, value in states.items()})
        reader, text_reader, exists = Path.read_bytes, Path.read_text, Path.exists
        def read(path):
            if path not in files:
                return reader(path)
            if files[path] is None:
                raise FileNotFoundError(path)
            return files[path]
        with patch.object(Path, "read_bytes", read), \
             patch.object(Path, "read_text", lambda p,*a,**k: read(p).decode() if p in files else text_reader(p,*a,**k)), \
             patch.object(Path, "exists", lambda p: files[p] is not None if p in files else exists(p)):
            yield files

    def test_actual_full_book_and_corpus_baseline_and_candidate(self):
        for state, data in (("baseline", self.raw), ("candidate", self.candidate)):
            with self.subTest(state=state), self.virtual(TARGET=data, INTENT=self.intent_bytes):
                result = module.check()
                self.assertEqual(result["state"], state)
                self.assertEqual(result["current_corpus_digest"], module.CORPUS[state])
                self.assertTrue(result["export_outside_historical_overlays"])
                self.assertFalse(result["source_changed"])

    def test_unknown_bytes_and_symlink_rejected(self):
        with self.virtual(TARGET=self.candidate+b"\n"):
            with self.assertRaisesRegex(ValueError, "unknown canonical"):
                module.check()
        with self.virtual(), patch.object(Path,"is_symlink",lambda p:p==module.TARGET):
            with self.assertRaisesRegex(ValueError,"symlink"):
                module.check()

    def test_package_source_and_derivative_pins_reject_tampering(self):
        paths = {module.PACKAGE, module.CANDIDATE_REVIEW}
        paths.update(module.ROOT / p for p in self.p["input_pins"])
        paths.update(module.ROOT / p for p in self.p["derivative_context"]["pinned_paths_sha256"])
        paths.discard(module.TARGET)  # Exact target states are checked separately.
        reader = Path.read_bytes
        for target in paths:
            with self.subTest(path=target),patch.object(Path,"read_bytes",lambda p:reader(p)+b"\n" if p==target else reader(p)):
                with self.assertRaisesRegex(ValueError,"drift"):
                    module.package()

    def test_each_implementation_binding_rejects_changed_current_bytes(self):
        reader = Path.read_bytes
        for relative in module.BINDING_PATHS:
            target=module.ROOT/relative
            with self.subTest(path=relative),self.virtual(),patch.object(Path,"read_bytes",lambda p:reader(p)+b"\n" if p==target else (self.review_bytes if p==module.REVIEW else reader(p))):
                with self.assertRaisesRegex(ValueError,"stale transaction review"):
                    module.require_review()

    def test_unrelated_corpus_and_actual_export_drift_rejected(self):
        with self.virtual(), patch.object(module,"corpus_digest",return_value="0"*64):
            with self.assertRaisesRegex(ValueError,"unrelated current corpus"):
                module.check()
        fake={"chapters":[{"verses":[{}]*29} for _ in range(23)]+[{"verses":[{}]*28}]}
        with self.virtual(), patch.object(module.exporter,"export_book",return_value=fake):
            with self.assertRaisesRegex(ValueError,"export drift"):
                module.check()

    def test_partial_ledgers_and_rollback_rejected(self):
        for state,changes in (("candidate",{}),("baseline",{"APPLICATION":self.encode(self.application)}),
                             ("baseline",{"INTENT":self.intent_bytes,"APPLICATION":self.encode(self.application)})):
            with self.subTest(state=state,changes=changes),self.virtual(**changes):
                with self.assertRaises(ValueError):
                    module.ledger_state(state)

    def test_valid_prepared_pending_and_completed_states(self):
        with self.virtual(): self.assertEqual(module.ledger_state("baseline"),"unprepared")
        with self.virtual(INTENT=self.intent_bytes):
            self.assertEqual(module.ledger_state("baseline"),"prepared")
            self.assertEqual(module.ledger_state("candidate"),"awaiting-confirmation")
        with self.virtual(INTENT=self.intent_bytes,APPLICATION=self.encode(self.application)):
            self.assertEqual(module.ledger_state("candidate"),"applied-verified")

    def test_review_and_each_binding_cannot_drift(self):
        changes=[{**self.review,"scoped_application_approved":False},
                 {**self.review,"publication_approved":True}]
        for key in self.review['binding']:
            changed=copy.deepcopy(self.review); changed['binding'][key]='stale'; changes.append(changed)
        for changed in changes:
            with self.subTest(changed=changed),self.virtual(REVIEW=self.encode(changed)):
                with self.assertRaisesRegex(ValueError,"review|scope"):
                    module.require_review()

    def test_intent_and_application_tamper_rejected(self):
        for which,original in (("INTENT",self.intent),("APPLICATION",self.application)):
            for field in original:
                changed=copy.deepcopy(original); changed[field]='tampered'
                states={"INTENT":self.intent_bytes,"APPLICATION":self.encode(self.application),which:self.encode(changed)}
                with self.subTest(which=which,field=field),self.virtual(**states):
                    with self.assertRaises(ValueError): module.ledger_state("candidate")

    def test_prepare_and_confirm_never_overwrite_existing_ledgers(self):
        for states in ({"INTENT":self.intent_bytes},{"APPLICATION":self.encode(self.application)}):
            with self.virtual(**states),patch.object(module,"write_once") as write:
                with self.assertRaises(ValueError): module.prepare()
                write.assert_not_called()
        with self.virtual(INTENT=self.intent_bytes,APPLICATION=self.encode(self.application)),patch.object(module,"write_once") as write:
            with self.assertRaises(ValueError): module.confirm()
            write.assert_not_called()

    def test_failed_check_writes_no_intent_or_application(self):
        for action in (module.prepare,module.confirm):
            states={} if action==module.prepare else {"INTENT":self.intent_bytes}
            with self.virtual(**states),patch.object(module,"check",side_effect=ValueError("failed validation")),patch.object(module,"write_once") as write:
                with self.assertRaisesRegex(ValueError,"failed validation"): action()
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
