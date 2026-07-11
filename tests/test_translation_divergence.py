import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("build_translation_divergence", TOOLS / "build_translation_divergence.py")
assert SPEC and SPEC.loader
DIVERGENCE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DIVERGENCE
SPEC.loader.exec_module(DIVERGENCE)


class TranslationDivergenceTests(unittest.TestCase):
    def test_archaic_pronouns_are_normalized(self):
        score = DIVERGENCE.wording_similarity("Thou shalt love thy neighbour", "You will love your neighbor")
        self.assertGreater(score, 0.70)

    def test_substantively_different_renderings_score_lower(self):
        near = DIVERGENCE.wording_similarity("Everything is vapor", "All is vapor")
        far = DIVERGENCE.wording_similarity("Everything is vapor", "Nothing in life has any meaning")
        self.assertGreater(near, far)

    def test_pairwise_consensus_ignores_brenton_panel(self):
        base = {"bsb": "In the beginning God created", "web": "In the beginning God created", "asv": "In the beginning God created", "kjv": "In the beginning God created"}
        with_brenton = {**base, "brenton": "A completely different source-tradition wording"}
        self.assertEqual(DIVERGENCE.pairwise_consensus(base), DIVERGENCE.pairwise_consensus(with_brenton))

    def test_transliteration_variants_are_not_treated_as_totally_different(self):
        score = DIVERGENCE.wording_similarity("the Pathrusites and Casluhites", "Pathrusim and Casluhim")
        self.assertGreater(score, 0.50)

    def test_score_bands_are_stable(self):
        self.assertEqual(DIVERGENCE.score_band(24.99), "low")
        self.assertEqual(DIVERGENCE.score_band(40), "high")
        self.assertEqual(DIVERGENCE.score_band(55), "very_high")

    def test_licensed_bundle_emits_scores_but_never_source_text(self):
        secret_text = "Synthetic licensed wording that must not appear in output"
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "licensed.json"
            path.write_text(json.dumps({
                "translations": {
                    "nlt": {
                        "display_name": "NLT",
                        "provider": "test fixture",
                        "license_reference": "TEST-ONLY",
                        "verses": {"GEN.1.1": secret_text},
                    }
                }
            }))
            bundle = DIVERGENCE.load_licensed_references(path)
            comparisons = DIVERGENCE.licensed_comparisons(
                "GEN.1.1", "Synthetic wording", "Clear synthetic licensed wording", bundle
            )
            metadata = DIVERGENCE.licensed_reference_metadata(bundle)
        serialized = json.dumps({"comparisons": comparisons, "metadata": metadata})
        self.assertIn("nlt", comparisons)
        self.assertIsNotNone(comparisons["nlt"]["spob_similarity"])
        self.assertNotIn(secret_text, serialized)
        self.assertFalse(metadata["nlt"]["text_included_in_report"])

    def test_rejects_unapproved_licensed_translation_key(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "licensed.json"
            path.write_text(json.dumps({"translations": {"unknown": {"verses": {}}}}))
            with self.assertRaises(ValueError):
                DIVERGENCE.load_licensed_references(path)


if __name__ == "__main__":
    unittest.main()
