import importlib.util
import pathlib
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_regressions", ROOT / "tools" / "check_regressions.py"
)
assert SPEC and SPEC.loader
REGRESSIONS = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REGRESSIONS
SPEC.loader.exec_module(REGRESSIONS)


class DivineNameRegressionTests(unittest.TestCase):
    def check_record(self, source_text: str, translation_text: str) -> list[dict]:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "translation" / "ot" / "test" / "001" / "001.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(
                yaml.safe_dump({
                    "source": {"text": source_text},
                    "translation": {"text": translation_text},
                }, allow_unicode=True),
                encoding="utf-8",
            )
            original_root = REGRESSIONS.REPO_ROOT
            REGRESSIONS.REPO_ROOT = root
            try:
                return REGRESSIONS.check_file(path)
            finally:
                REGRESSIONS.REPO_ROOT = original_root

    def test_rejects_lord_when_source_uses_yhwh(self):
        violations = self.check_record("וַיֹּאמֶר יְהוָה", "The LORD said.")
        self.assertIn("yhwh-as-lord", [item["rule"] for item in violations])

    def test_accepts_yahweh_when_source_uses_yhwh(self):
        violations = self.check_record("וַיֹּאמֶר יְהוָה", "Yahweh said.")
        self.assertNotIn("yhwh-as-lord", [item["rule"] for item in violations])

    def test_does_not_apply_yhwh_rule_to_adonai(self):
        violations = self.check_record("אֲדֹנָי", "The LORD said.")
        self.assertNotIn("yhwh-as-lord", [item["rule"] for item in violations])


class ServantTerminologyRegressionTests(unittest.TestCase):
    def check_record(self, translation_text: str) -> list[dict]:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "translation" / "nt" / "test" / "001" / "001.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(
                yaml.safe_dump({
                    "source": {"text": "δοῦλος"},
                    "translation": {"text": translation_text},
                }, allow_unicode=True),
                encoding="utf-8",
            )
            original_root = REGRESSIONS.REPO_ROOT
            REGRESSIONS.REPO_ROOT = root
            try:
                return REGRESSIONS.check_file(path)
            finally:
                REGRESSIONS.REPO_ROOT = original_root

    def test_rejects_slave_in_translation_text(self):
        violations = self.check_record("To show his slaves through his slave John.")
        self.assertIn("slave-as-servant", [item["rule"] for item in violations])

    def test_accepts_servant_in_translation_text(self):
        violations = self.check_record("To show his servants through his servant John.")
        self.assertNotIn("slave-as-servant", [item["rule"] for item in violations])


class EnglishPersonalNameRegressionTests(unittest.TestCase):
    def check_record(self, translation_text: str) -> list[dict]:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "translation" / "ot" / "test" / "001" / "001.yaml"
            path.parent.mkdir(parents=True)
            path.write_text(
                yaml.safe_dump({
                    "source": {"text": "יוֹסֵף יַעֲקֹב"},
                    "translation": {"text": translation_text},
                }, allow_unicode=True),
                encoding="utf-8",
            )
            original_root = REGRESSIONS.REPO_ROOT
            REGRESSIONS.REPO_ROOT = root
            try:
                return REGRESSIONS.check_file(path)
            finally:
                REGRESSIONS.REPO_ROOT = original_root

    def test_rejects_closer_hebrew_forms_in_base_english_text(self):
        violations = self.check_record("Yosef spoke to his father Yaakov.")
        rules = [item["rule"] for item in violations]
        self.assertEqual(2, rules.count("hebrew-name-form-in-english-reader"))

    def test_accepts_stable_english_name_forms(self):
        violations = self.check_record("Joseph spoke to his father Jacob.")
        self.assertNotIn(
            "hebrew-name-form-in-english-reader",
            [item["rule"] for item in violations],
        )


if __name__ == "__main__":
    unittest.main()
