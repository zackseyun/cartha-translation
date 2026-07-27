import importlib.util
import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_derived_coverage", ROOT / "tools" / "check_derived_coverage.py"
)
assert SPEC and SPEC.loader
COVERAGE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = COVERAGE
SPEC.loader.exec_module(COVERAGE)


class DerivedTranslationCoverageTests(unittest.TestCase):
    def test_current_canonical_corpus_has_no_derived_gaps(self):
        report = COVERAGE.build_report(ROOT)
        missing = {
            name: result["missing"]
            for name, result in report["derived"].items()
            if result["missing"]
        }
        self.assertEqual(missing, {})

    def test_reports_missing_base_verse_but_does_not_count_extra_as_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            base = root / "translation/ot/psalms/119/001.yaml"
            base.parent.mkdir(parents=True)
            base.write_text("translation:\n  text: Base\n", encoding="utf-8")
            for derived_root in COVERAGE.DERIVED_ROOTS.values():
                extra = root / derived_root / "ot/psalms/118/999.yaml"
                extra.parent.mkdir(parents=True)
                extra.write_text("translation:\n  text: Extra\n", encoding="utf-8")

            report = COVERAGE.build_report(root)

        for result in report["derived"].values():
            self.assertEqual(result["missing"], ["ot/psalms/119/001.yaml"])
            self.assertEqual(result["extra"], ["ot/psalms/118/999.yaml"])


if __name__ == "__main__":
    unittest.main()
