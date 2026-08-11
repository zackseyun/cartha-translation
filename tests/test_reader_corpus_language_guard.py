import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location(
    "validate_reader_corpus", ROOT / "tools" / "validate_reader_corpus.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class EnglishReaderLanguageGuardTests(unittest.TestCase):
    def record(self, text: str):
        return VALIDATOR.CorpusRecord(
            path=ROOT / "translation" / "nt" / "matthew" / "013" / "022.yaml",
            text=text,
            normalized_text=VALIDATOR.normalize_text(text),
            note="",
            unit="",
            reference="Matthew 13:22",
            yaml_kind="reader_verse",
        )

    def test_rejects_devanagari_inside_english_translation(self):
        record = self.record("The चिंता of this age chokes the word.")
        issues = VALIDATOR.check_english_script_contamination({record.path: record})
        self.assertEqual(["devanagari-in-english-reader"], [issue.rule for issue in issues])

    def test_accepts_audited_english_rendering(self):
        record = self.record("The worries of this age choke the word.")
        self.assertEqual([], VALIDATOR.check_english_script_contamination({record.path: record}))


if __name__ == "__main__":
    unittest.main()
