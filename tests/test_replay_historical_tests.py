"""Runner isolation tests; synthetic passes are not research evidence."""
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from tools.textual_restoration import replay_historical_tests as module


class HistoricalTestRunnerTests(unittest.TestCase):
    def run_mocked(self, result=None, returncode=0, side_effect=None):
        payload = result or {"passed": True, "tests_run": 5, "skipped": 0, "expected_failures": 0}
        reply = subprocess.CompletedProcess([], returncode, json.dumps(payload), "child diagnostic")
        with patch.object(module, "git", side_effect=[module.COMMIT.encode(), b"archive"]), \
             patch.object(module, "_archive_paths", return_value=["tests"]), \
             patch.object(module, "extract_regular") as extract, \
             patch.object(module.subprocess, "run", return_value=reply, side_effect=side_effect) as child:
            try:
                actual = module.run_suite("registry_genesis")
                return actual, child.call_args
            finally:
                if extract.called:
                    self.assertFalse(extract.call_args.args[1].exists(), "private tree leaked")

    def test_unknown_suite_cannot_dispatch_arbitrary_code(self):
        with patch.object(module, "git") as git:
            with self.assertRaises(ValueError):
                module.run_suite("unittest.__main__")
            git.assert_not_called()

    def test_fixed_commit_resolution_required(self):
        with patch.object(module, "git", return_value=b"0" * 40):
            with self.assertRaisesRegex(ValueError, "resolution mismatch"):
                module.run_suite("genesis")

    def test_result_is_historical_and_child_is_isolated(self):
        result, call = self.run_mocked()
        self.assertEqual(result["commit"], module.COMMIT)
        self.assertFalse(result["current_corpus_validated"])
        self.assertFalse(result["application_approved"])
        self.assertEqual(call.args[0][:3], [module.sys.executable, "-I", "-c"])
        self.assertNotEqual(Path(call.kwargs["cwd"]), module.ROOT)
        self.assertFalse(Path(call.kwargs["cwd"]).exists())

    def test_child_failure_propagates_and_cleans_up(self):
        with self.assertRaisesRegex(RuntimeError, "child diagnostic"):
            self.run_mocked(returncode=1)

    def test_timeout_propagates_and_cleans_up(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            self.run_mocked(side_effect=subprocess.TimeoutExpired("child", 600))

    def test_missing_skipped_and_expected_failure_checks_cannot_pass(self):
        valid = {"passed": True, "tests_run": 5, "skipped": 0, "expected_failures": 0}
        for field, value in (("passed", False), ("tests_run", 0), ("skipped", 1), ("expected_failures", 1)):
            with self.subTest(field=field), self.assertRaisesRegex(RuntimeError, "coverage mismatch"):
                self.run_mocked({**valid, field: value})

    def test_derivative_paths_come_from_commit_and_cannot_escape(self):
        for path in ("../translation_es/a", "translation_es/../../outside", "translation_es/[ab]", "/translation_es/a"):
            manifest = {"unchanged_derivative_context_pins": {path: "0" * 64}}
            with self.subTest(path=path), patch.object(module, "git", return_value=json.dumps(manifest).encode()):
                with self.assertRaisesRegex(ValueError, "derivative path"):
                    module._archive_paths(module.ROOT)


if __name__ == "__main__":
    unittest.main()
