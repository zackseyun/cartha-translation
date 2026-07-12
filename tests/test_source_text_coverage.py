import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.restore_missing_source_texts import has_source_text


class SourceTextCoverageTests(unittest.TestCase):
    def test_every_translation_record_publishes_nonempty_source_text(self):
        missing = [
            path.relative_to(ROOT).as_posix()
            for path in sorted((ROOT / "translation").rglob("*.yaml"))
            if not has_source_text(path)
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
