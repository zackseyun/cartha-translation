import importlib.util
import pathlib
import sys
import tempfile
import types
import unittest
import json

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "simplified_pob_pipeline", ROOT / "tools" / "simplified_pob_pipeline.py"
)
assert SPEC and SPEC.loader
PIPELINE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PIPELINE
SPEC.loader.exec_module(PIPELINE)
sys.path.insert(0, str(ROOT / "tools"))
REVISION_SPEC = importlib.util.spec_from_file_location(
    "spob_revision_pipeline", ROOT / "tools" / "spob_revision_pipeline.py"
)
assert REVISION_SPEC and REVISION_SPEC.loader
REVISION = importlib.util.module_from_spec(REVISION_SPEC)
sys.modules[REVISION_SPEC.name] = REVISION
REVISION_SPEC.loader.exec_module(REVISION)


class SpobDoctrinePromptTests(unittest.TestCase):
    def test_prompt_requires_auditable_interpretive_expansion(self):
        prompt = PIPELINE.DRAFT_SYSTEM_PROMPT
        self.assertIn("maximum warranted understanding", prompt)
        self.assertIn("interpretive_expansions", prompt)
        self.assertIn("They never control the main text", prompt)
        self.assertIn("Vapor of", prompt)

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

    def test_revision_selection_preserves_editorial_adjudication_without_override(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            spob = root / "translation_simplified/nt/test_book/001/001.yaml"
            spob.parent.mkdir(parents=True)
            spob.write_text(yaml.safe_dump({
                "editorial_adjudications": [{"status": "retain"}],
                "spob_revision_history": [],
            }))
            review = root / "state/spob_reviews/gpt-5_6-terra/nt/test_book/001/001.json"
            review.parent.mkdir(parents=True)
            review.write_text(json.dumps({
                "reference": "Test 1:1",
                "spob_path": str(spob.relative_to(root)),
                "output_hash": "review-hash",
                "review": {"verdict": "revise"},
            }))
            original_root, original_review_root = REVISION.ROOT, REVISION.REVIEW_ROOT
            REVISION.ROOT = root
            REVISION.REVIEW_ROOT = root / "state/spob_reviews"
            try:
                args = types.SimpleNamespace(
                    review_model="gpt-5.6-terra", book=None, chapter=None,
                    exclude_reference=None, force=False, limit=0,
                    override_editorial_adjudications=False,
                )
                self.assertEqual(REVISION.review_files(args), [])
                args.override_editorial_adjudications = True
                self.assertEqual(REVISION.review_files(args), [review])
            finally:
                REVISION.ROOT, REVISION.REVIEW_ROOT = original_root, original_review_root


if __name__ == "__main__":
    unittest.main()
