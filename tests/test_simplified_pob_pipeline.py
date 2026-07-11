import importlib.util
import pathlib
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "simplified_pob_pipeline", ROOT / "tools" / "simplified_pob_pipeline.py"
)
assert SPEC and SPEC.loader
PIPELINE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PIPELINE
SPEC.loader.exec_module(PIPELINE)


class SpobDoctrinePromptTests(unittest.TestCase):
    def test_prompt_requires_auditable_interpretive_expansion(self):
        prompt = PIPELINE.DRAFT_SYSTEM_PROMPT
        self.assertIn("maximum warranted understanding", prompt)
        self.assertIn("interpretive_expansions", prompt)
        self.assertIn("William Branham", prompt)
        self.assertIn("Keep a clear mind and stay", prompt)

    def test_normalizes_interpretive_expansion(self):
        result = PIPELINE.normalize_interpretive_expansions(
            [
                {
                    "pob_phrase": "stay alert",
                    "rendering": "stay spiritually awake",
                    "claim": "The vigilance concerns spiritual attack.",
                    "evidence": ["Immediate devil and lion context"],
                    "confidence": "HIGH",
                    "alternatives_preserved": ["stay alert"],
                    "external_witnesses": [],
                }
            ]
        )
        self.assertEqual(result[0]["confidence"], "high")
        self.assertEqual(result[0]["rendering"], "stay spiritually awake")

    def test_validator_rejects_low_confidence_main_text_expansion(self):
        record = {
            "language": {"code": "en"},
            "base_translation": {"text": "Base text"},
            "translation": {
                "text": "A clear simplified sentence for the modern reader.",
                "philosophy": "optimal-equivalence",
            },
            "simplification_decisions": [{"rationale": "Clearer syntax"}],
            "interpretive_expansions": [
                {
                    "rendering": "teacher-specific claim",
                    "claim": "A disputed interpretation",
                    "evidence": ["One external teacher"],
                    "confidence": "low",
                }
            ],
            "ai_draft": {"prompt_sha256": "abc"},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "record.yaml"
            path.write_text(yaml.safe_dump(record), encoding="utf-8")
            errors = PIPELINE.validate_simplified_record(path)
        self.assertTrue(any("low-confidence expansion" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
