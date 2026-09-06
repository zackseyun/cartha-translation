"""Genesis transaction guards with virtual reads; no canonical or ledger writes."""
from contextlib import contextmanager
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools import genesis_note_transaction as module


class GenesisNoteTransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = module.BASELINE.read_bytes()
        cls.candidate = module.CANDIDATE.read_bytes()

    def setUp(self):
        self.review = {**module.binding(), 'scoped_transaction_approved': True}
        self.review_raw = module.jbytes(self.review)
        self.intent = {**module.binding(), 'status': 'prepared',
                       'transaction_review_sha256': module.sha(self.review_raw)}
        self.intent_raw = module.jbytes(self.intent)
        self.application = {**module.binding(), 'status': 'applied-verified',
                            'transaction_review_sha256': module.sha(self.review_raw),
                            'intent_sha256': module.sha(self.intent_raw)}
        self.files = {module.REVIEW: self.review_raw, module.INTENT: self.intent_raw,
                      module.APPLICATION: None, module.TARGET: self.raw}

    @contextmanager
    def virtual_files(self, changes=None):
        files = {**self.files, **(changes or {})}
        read, read_text, exists = Path.read_bytes, Path.read_text, Path.exists
        def virtual_read(path):
            if path not in files:
                return read(path)
            if files[path] is None:
                raise FileNotFoundError(path)
            return files[path]
        def virtual_text(path, *args, **kwargs):
            return virtual_read(path).decode('utf-8') if path in files else read_text(path, *args, **kwargs)
        def virtual_exists(path):
            return files[path] is not None if path in files else exists(path)
        with patch.object(Path, 'read_bytes', virtual_read), patch.object(Path, 'read_text', virtual_text), \
                patch.object(Path, 'exists', virtual_exists):
            yield files

    def test_actual_pinned_package(self):
        raw, candidate, _ = module.package()
        self.assertEqual((raw, candidate), (self.raw, self.candidate))

    def test_each_fixed_file_and_input_pin_rejects_drift(self):
        paths = {module.BASELINE, module.CANDIDATE, module.PREFLIGHT, module.JUDGMENT, module.INPUTS}
        for path in json.loads(module.PREFLIGHT.read_text())['input_pins']:
            paths.add(module.ROOT / path)
        for key in ('prior_package_input_pins', 'unchanged_derivative_context_pins'):
            paths.update(module.ROOT / path for path in json.loads(module.INPUTS.read_text())[key])
        for path in paths:
            with self.subTest(path=path), self.virtual_files({path: path.read_bytes() + b'\n'}):
                with self.assertRaisesRegex(ValueError, 'drift'):
                    module.package()

    def test_prior_completed_canonical_candidates_cannot_roll_back(self):
        for path, baseline in ((module.jeremiah.TARGET, module.jeremiah.BASELINE),
                               (module.numbers.ROOT / module.numbers.TARGET_REL, module.numbers.BASELINE)):
            with self.subTest(path=path), self.virtual_files({path: baseline.read_bytes()}):
                with self.assertRaisesRegex(ValueError, 'prior applied canonical state drift'):
                    module.package()

    def test_baseline_without_intent_or_review_replays(self):
        with self.virtual_files({module.INTENT: None, module.REVIEW: None}), module.historical_view():
            self.assertEqual(module.TARGET.read_bytes(), self.raw)

    def test_candidate_replays_only_target_and_restores_readers(self):
        other = module.ROOT / 'translation/ot/genesis/004/009.yaml'
        original = other.read_bytes()
        with self.virtual_files({module.TARGET: self.candidate}):
            with module.historical_view():
                self.assertEqual(module.TARGET.read_bytes(), self.raw)
                self.assertEqual(module.TARGET.read_text(), self.raw.decode())
                self.assertEqual(other.read_bytes(), original)
            self.assertEqual(module.TARGET.read_bytes(), self.candidate)

    def test_unknown_target_bytes_rejected(self):
        with self.virtual_files({module.TARGET: self.candidate + b'\n'}):
            with self.assertRaisesRegex(ValueError, 'unknown Genesis state'), module.historical_view():
                self.fail('unknown candidate accepted')

    def test_completed_application_rejects_baseline_rollback(self):
        with self.virtual_files({module.APPLICATION: module.jbytes(self.application)}):
            with self.assertRaisesRegex(ValueError, 'rollback'), module.historical_view():
                self.fail('unrecorded rollback accepted')

    def test_pending_baseline_intent_validates_review_and_intent(self):
        changes = [{module.REVIEW: None}, {module.INTENT: module.jbytes({**self.intent, 'status': 'failed'})},
                   {module.REVIEW: module.jbytes({**self.review, 'executor_sha256': 'stale'})}]
        for change in changes:
            with self.subTest(change=change), self.virtual_files(change):
                with self.assertRaises((ValueError, FileNotFoundError)), module.historical_view():
                    self.fail('pending intent bypassed validation')

    def test_candidate_missing_review_or_intent_rejected_even_with_application(self):
        for missing in (module.REVIEW, module.INTENT):
            with self.subTest(missing=missing), self.virtual_files({module.TARGET: self.candidate,
                    module.APPLICATION: module.jbytes(self.application), missing: None}):
                with self.assertRaises(FileNotFoundError), module.historical_view():
                    self.fail('application replaced required provenance')

    def test_review_requires_explicit_approval_and_every_binding(self):
        for key in ('scoped_transaction_approved', *module.binding()):
            with self.subTest(key=key), self.virtual_files({module.REVIEW: module.jbytes({**self.review, key: 'stale'})}):
                with self.assertRaisesRegex(ValueError, 'missing or stale transaction review'):
                    module.require_review()

    def test_mutated_executor_tests_doc_and_migration_invalidate_review(self):
        for path in (Path(module.__file__), module.TESTS, module.DOC, module.MIGRATION,
                     module.METHOD, module.REVISION_METHOD):
            with self.subTest(path=path), self.virtual_files({path: path.read_bytes() + b'\n'}):
                with self.assertRaisesRegex(ValueError, 'missing or stale transaction review'):
                    module.require_review()

    def test_ledger_status_and_every_binding_and_review_bytes(self):
        for path, record in ((module.INTENT, self.intent), (module.APPLICATION, self.application)):
            for key in ('status', 'transaction_review_sha256', *module.binding()):
                with self.subTest(path=path, key=key), self.virtual_files({path: module.jbytes({**record, key: 'stale'})}):
                    with self.assertRaisesRegex(ValueError, 'invalid transaction state|transaction provenance drift'):
                        module.require_transaction()

    def test_application_binds_exact_intent_bytes(self):
        with self.virtual_files({module.INTENT: self.intent_raw + b'\n', module.APPLICATION: module.jbytes(self.application)}):
            with self.assertRaisesRegex(ValueError, 'application intent binding drift'):
                module.require_transaction()

    def test_both_valid_ledger_states_accepted(self):
        with self.virtual_files():
            module.require_transaction()
        with self.virtual_files({module.APPLICATION: module.jbytes(self.application)}):
            module.require_transaction()

    def test_target_changed_during_overlay_fails(self):
        with self.virtual_files() as files:
            with self.assertRaisesRegex(ValueError, 'canonical changed during historical replay'):
                with module.historical_view():
                    files[module.TARGET] = b'concurrent change'

    def test_symlink_target_refused(self):
        original = Path.is_symlink
        with self.virtual_files(), patch.object(Path, 'is_symlink', lambda p: p == module.TARGET or original(p)):
            with self.assertRaisesRegex(ValueError, 'symlink'), module.historical_view():
                self.fail('symlink accepted')

    def test_prepare_and_complete_never_overwrite_ledgers(self):
        for path in (module.INTENT, module.APPLICATION):
            with self.subTest(path=path), self.virtual_files({module.INTENT: None, path: b'exists'}):
                with patch.object(module.numbers, 'write_once') as write:
                    with self.assertRaisesRegex(ValueError, 'transaction already exists'):
                        module.prepare()
                    write.assert_not_called()
        with self.virtual_files({module.APPLICATION: module.jbytes(self.application)}):
            with patch.object(module.numbers, 'write_once') as write:
                with self.assertRaisesRegex(ValueError, 'application already exists'):
                    module.complete()
                write.assert_not_called()

    def test_completion_requires_candidate_and_postcheck_requires_application(self):
        with self.virtual_files(), patch.object(module.numbers, 'write_once') as write:
            with self.assertRaisesRegex(ValueError, 'exact applied candidate'):
                module.complete()
            with self.assertRaisesRegex(ValueError, 'completed application'):
                module.post_check()
            write.assert_not_called()

    def test_failed_post_export_writes_no_completion(self):
        with self.virtual_files({module.TARGET: self.candidate}), patch.object(module, 'check', return_value={
                'current_export': {'actual_matches_candidate': False}}), patch.object(module.numbers, 'write_once') as write:
            with self.assertRaisesRegex(ValueError, 'actual canonical export differs'):
                module.complete()
            write.assert_not_called()

    def test_provenance_change_during_completion_writes_no_receipt(self):
        with self.virtual_files({module.TARGET: self.candidate}) as files:
            def changing_check():
                files[module.INTENT] += b'\n'
                return {'current_export': {'actual_matches_candidate': True}}
            with patch.object(module, 'check', side_effect=changing_check), patch.object(module.numbers, 'write_once') as write:
                with self.assertRaisesRegex(ValueError, 'provenance changed during completion'):
                    module.complete()
                write.assert_not_called()

    def test_postcheck_requires_stable_application_bytes_through_check(self):
        for change in (None, module.jbytes(self.application) + b'\n'):
            with self.subTest(change=change), self.virtual_files({module.TARGET: self.candidate,
                    module.APPLICATION: module.jbytes(self.application)}) as files:
                def changing_check():
                    files[module.APPLICATION] = change
                    return {'checked': True}
                with patch.object(module, 'check', side_effect=changing_check):
                    with self.assertRaises((ValueError, FileNotFoundError)):
                        module.post_check()

    def test_successful_confirmation_and_postcheck_never_write_canonical(self):
        result = {'current_export': {'actual_matches_candidate': True}}
        with self.virtual_files({module.TARGET: self.candidate}), patch.object(module, 'check', return_value=result), \
                patch.object(module.numbers, 'write_once') as write:
            record = module.complete()
            write.assert_called_once_with(module.APPLICATION, record)
            self.assertEqual(record['intent_sha256'], module.sha(self.intent_raw))
            self.assertEqual(module.TARGET.read_bytes(), self.candidate)
        with self.virtual_files({module.TARGET: self.candidate, module.APPLICATION: module.jbytes(self.application)}), \
                patch.object(module, 'check', return_value=result), patch.object(module.numbers, 'write_once') as write:
            self.assertEqual(module.post_check(), result)
            write.assert_not_called()

    def test_current_test_guard_accepts_only_exact_declared_migration(self):
        plan = json.loads(module.MIGRATION.read_text())
        raw = module.CURRENT_TEST.read_text()
        if module.sha(raw.encode()) == plan['baseline_sha256']:
            after = raw
            for edit in plan['edits']:
                after = after.replace(edit['from'], edit['to'])
        else:
            after = raw
        with self.virtual_files({module.CURRENT_TEST: after.encode()}):
            self.assertEqual(module.migration_state(), 'candidate')
        with self.virtual_files({module.CURRENT_TEST: after.encode() + b'\n'}):
            with self.assertRaisesRegex(ValueError, 'unknown current-test migration state'):
                module.package()

    def test_preparation_has_no_canonical_writer_and_binds_preflight(self):
        with self.virtual_files({module.INTENT: None}), patch.object(module, 'check', return_value={'checked': True}), \
                patch.object(module.numbers, 'write_once') as write:
            record = module.prepare()
            self.assertEqual(record['preflight'], {'checked': True})
            write.assert_called_once_with(module.INTENT, record)
            self.assertEqual(module.TARGET.read_bytes(), self.raw)

    def test_full_read_only_check_baseline_and_virtual_applied_candidate(self):
        digests = []
        for raw in (self.raw, self.candidate):
            with self.subTest(state=module.sha(raw)), self.virtual_files({module.TARGET: raw}):
                result = module.check()
                self.assertTrue(result['candidate_preflight_reproduced_under_explicit_genesis_baseline_overlay'])
                sample = result['historical_sample']
                self.assertEqual(sample['overlay_paths'], [module.numbers.TARGET_REL,
                    module.jeremiah.candidate_check.v1.TARGET, module.candidate_check.TARGET])
                self.assertEqual(sample['context_files_verified'], 101)
                self.assertTrue(sample['current_digest_computed_outside_all_overlays'])
                self.assertEqual(sample['current_corpus_digest'], module.corpus_digest())
                digests.append(sample['current_corpus_digest'])
                export = result['current_export']
                self.assertEqual((export['chapters'], export['verses']), (50, 1533))
                self.assertEqual(export['actual_matches_candidate'], raw == self.candidate)
                self.assertEqual(export['actual_matches_baseline'], raw == self.raw)
                self.assertEqual(result['unchanged_derivative_records_pinned'], 17)
        self.assertNotEqual(*digests)

    def test_unrelated_corpus_drift_not_absorbed_by_historical_replay(self):
        other = module.ROOT / 'translation/ot/obadiah/001/001.yaml'
        with self.virtual_files({other: other.read_bytes() + b'\n'}):
            with self.assertRaisesRegex(ValueError, 'Historical sample mismatch'):
                module.historical_sample_probe()

    def test_actual_export_is_not_the_baseline_overlay_in_candidate_state(self):
        raw, candidate, frozen = module.package()
        with self.virtual_files({module.TARGET: self.candidate}):
            result = module.current_export(raw, candidate, frozen)
            self.assertTrue(result['actual_matches_candidate'])
            self.assertFalse(result['actual_matches_baseline'])
            self.assertEqual(result['actual_verse'], frozen['mobile_probe']['draft_verse'])

    def test_exact_current_test_migration_is_unambiguous_and_compiles(self):
        plan = json.loads(module.MIGRATION.read_text())
        current = (module.ROOT / plan['target']).read_bytes()
        self.assertIn(module.sha(current), (plan['baseline_sha256'], plan['candidate_sha256']))
        if module.sha(current) == plan['baseline_sha256']:
            text = current.decode()
            for edit in plan['edits']:
                self.assertEqual(text.count(edit['from']), 1)
                text = text.replace(edit['from'], edit['to'])
            self.assertEqual(module.sha(text.encode()), plan['candidate_sha256'])
        else:
            text = current.decode()
        compile(text, plan['target'], 'exec')


if __name__ == '__main__':
    unittest.main()
