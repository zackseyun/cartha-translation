import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('revisions_refresh', ROOT/'tools/revisions_refresh.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        for name in ['tools','translation/nt/john/001','state/reviews/test']:
            (self.repo/name).mkdir(parents=True)
        self.verse = self.repo/'translation/nt/john/001/001.yaml'
        self.verse.write_text('text: fixture\n')
        self.review = self.repo/'state/reviews/test/001.json'
        self.review.write_text('{"verdict":"agree"}\n')
        (self.repo/'tools/build_revisions_index.py').write_text('''from pathlib import Path
p=Path('build-count')
p.write_text(str(int(p.read_text())+1) if p.exists() else '1')
Path('revisions.json').write_text('{}')
Path('revisions-summary.json').write_text('{}')
''')
        self.ac = patch.object(r, 'on_ac_power', return_value=True)
        self.ac.start()
        self.addCleanup(self.ac.stop)

    def request(self):
        r.request_refresh(self.repo, background=False)

    def run_pending(self, **kwargs):
        return r.run_pending(self.repo, quiet_seconds=0, **kwargs)

    def builds(self):
        p = self.repo/'build-count'
        return int(p.read_text()) if p.exists() else 0

    def test_idle_does_not_probe_power_scan_or_build(self):
        with patch.object(r, 'source_fingerprint', side_effect=AssertionError('scan')), \
             patch.object(r, 'on_ac_power', side_effect=AssertionError('power')):
            self.assertEqual(self.run_pending(), 0)
        self.assertEqual(self.builds(), 0)

    def test_battery_retains_pending_without_scanning(self):
        self.request()
        with patch.object(r, 'on_ac_power', return_value=False), \
             patch.object(r, 'source_fingerprint', side_effect=AssertionError('scan')):
            self.assertEqual(self.run_pending(), 0)
        self.assertFalse((r.state_dir(self.repo)/'completed.json').exists())
        self.assertEqual(self.run_pending(), 0)
        self.assertEqual(self.builds(), 1)

    def test_manual_battery_override(self):
        self.request()
        with patch.object(r, 'on_ac_power', return_value=False):
            self.assertEqual(self.run_pending(allow_battery=True), 0)
        self.assertEqual(self.builds(), 1)

    def test_repeated_batch_and_idle_skip_unchanged_inputs(self):
        self.request(); self.run_pending()
        self.request(); self.run_pending()
        self.run_pending()
        self.assertEqual(self.builds(), 1)

    def test_review_edit_without_file_count_change_rebuilds(self):
        self.request(); self.run_pending()
        self.review.write_text('{"verdict":"needs-revision"}\n')
        self.request(); self.run_pending()
        self.assertEqual(self.builds(), 2)

    def test_translation_edit_rebuilds(self):
        self.request(); self.run_pending()
        self.verse.write_text('text: changed fixture\n')
        self.request(); self.run_pending()
        self.assertEqual(self.builds(), 2)

    def test_review_deletion_rebuilds(self):
        self.request(); self.run_pending()
        self.review.unlink()
        self.request(); self.run_pending()
        self.assertEqual(self.builds(), 2)

    def test_missing_output_rebuilds(self):
        self.request(); self.run_pending()
        (self.repo/'revisions-summary.json').unlink()
        self.request(); self.run_pending()
        self.assertEqual(self.builds(), 2)

    def test_failed_builder_retains_pending(self):
        self.request()
        with patch.object(r.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'fixture')):
            self.assertEqual(self.run_pending(), 1)
        self.assertFalse((r.state_dir(self.repo)/'completed.json').exists())
        self.assertEqual(self.run_pending(), 0)
        self.assertEqual(self.builds(), 1)

    def test_failed_push_retries_without_rebuilding(self):
        self.request()
        with patch.object(r, 'prepare_publish'), patch.object(r, 'publish', side_effect=RuntimeError('fixture push failure')):
            self.assertEqual(self.run_pending(publish_changes=True), 1)
        with patch.object(r, 'prepare_publish'), patch.object(r, 'publish') as publish:
            self.assertEqual(self.run_pending(publish_changes=True), 0)
            publish.assert_called_once()
        self.assertEqual(self.builds(), 1)

    def test_concurrent_request_during_build_is_consumed_without_duplicate_build(self):
        self.request()
        real_run = r.subprocess.run
        started = threading.Event()
        def slow_run(*args, **kwargs):
            started.set(); time.sleep(.05)
            return real_run(*args, **kwargs)
        with patch.object(r.subprocess, 'run', side_effect=slow_run):
            first = threading.Thread(target=self.run_pending)
            first.start(); self.assertTrue(started.wait(2))
            self.request()
            second = threading.Thread(target=self.run_pending)
            second.start(); first.join(5); second.join(5)
            self.assertFalse(first.is_alive()); self.assertFalse(second.is_alive())
        self.assertEqual(self.builds(), 1)
        state = r.state_dir(self.repo)
        self.assertEqual(r.read_json(state/'request.json')['id'], r.read_json(state/'completed.json')['id'])

    def test_inputs_changed_during_build_not_published_or_cached(self):
        self.request()
        real_run = r.subprocess.run
        def changing_run(*args, **kwargs):
            result = real_run(*args, **kwargs)
            self.verse.write_text('text: concurrent batch\n')
            return result
        with patch.object(r.subprocess, 'run', side_effect=changing_run), \
             patch.object(r, 'prepare_publish'), patch.object(r, 'publish') as publish:
            self.assertEqual(self.run_pending(publish_changes=True), 0)
            publish.assert_not_called()
        self.assertFalse((r.state_dir(self.repo)/'built.json').exists())
        self.assertFalse((r.state_dir(self.repo)/'completed.json').exists())

    def test_dirty_or_nonmain_checkout_is_not_modified(self):
        for branch, staged, dirty in [('feature','', ''), ('main','unrelated.py',''), ('main','','translation/nt/john/001/001.yaml')]:
            with self.subTest(branch=branch, staged=staged, dirty=dirty):
                values = iter([branch, staged, dirty])
                with patch.object(r, 'git', side_effect=lambda *a: next(values)) as git:
                    with self.assertRaises(RuntimeError): r.prepare_publish(self.repo)
                    self.assertFalse(any('merge' in call.args for call in git.call_args_list))

    def test_changed_or_truncated_output_is_rebuilt(self):
        self.request(); self.run_pending()
        (self.repo/'revisions-summary.json').write_text('{truncated')
        self.request(); self.run_pending()
        self.assertEqual(self.builds(), 2)
        self.assertEqual(json.loads((self.repo/'revisions-summary.json').read_text()), {})

    def test_invalid_builder_output_is_not_completed(self):
        (self.repo/'tools/build_revisions_index.py').write_text(
            "from pathlib import Path\nPath('revisions.json').write_text('{bad')\nPath('revisions-summary.json').write_text('{}')\n")
        self.request()
        self.assertEqual(self.run_pending(), 1)
        self.assertFalse((r.state_dir(self.repo)/'completed.json').exists())

    def test_real_local_git_publish_includes_new_snapshots_and_preserves_other_files(self):
        remote = self.repo/'remote.git'
        def command(*args):
            return subprocess.run(args, cwd=self.repo, capture_output=True, text=True, check=True)
        command('git','init','-b','main')
        command('git','config','user.name','Fixture')
        command('git','config','user.email','fixture@example.invalid')
        (self.repo/'.gitignore').write_text('state/\nbuild-count\nremote.git/\n')
        command('git','add','.gitignore','tools','translation')
        command('git','commit','-m','fixture source')
        command('git','init','--bare',str(remote))
        command('git','remote','add','origin',str(remote))
        command('git','push','-u','origin','main')
        (self.repo/'unrelated.txt').write_text('leave this local file alone')
        self.request()
        self.assertEqual(self.run_pending(publish_changes=True), 0)
        self.assertEqual(command('git','show','origin/main:revisions.json').stdout, '{}')
        self.assertEqual(command('git','show','origin/main:revisions-summary.json').stdout, '{}')
        self.assertNotIn('unrelated.txt',command('git','ls-tree','--name-only','HEAD').stdout)
        self.assertEqual(self.builds(), 1)
        self.request(); self.assertEqual(self.run_pending(publish_changes=True), 0)
        self.assertEqual(self.builds(), 1)

    def test_no_periodic_revisions_template_remains(self):
        self.assertFalse((ROOT/'scripts/com.cartha.pob-revisions-flywheel.plist').exists())
        self.assertIn('--background', (ROOT/'scripts/sync_pob.sh').read_text())
        self.assertNotIn('timeout=120', (ROOT/'tools/auto_apply_gemini.py').read_text())


if __name__ == '__main__':
    unittest.main()
