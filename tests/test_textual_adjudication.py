import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "textual_adjudication", ROOT / "tools/textual_restoration/adjudication.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TextualAdjudicationTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(MODULE.DATA.read_text())

    def errors(self):
        return "\n".join(MODULE.validate(self.data))

    def test_pilot_integrity(self):
        self.assertEqual(MODULE.validate(self.data), [])
        self.assertEqual(len(self.data["units"]), 3)

    def test_age_is_not_an_override(self):
        self.data["policy"]["chronology"] = "oldest-wins"
        self.assertIn("modest preference", self.errors())

    def test_no_majority_vote_or_automatic_publication(self):
        self.data["policy"]["majority_vote"] = True
        self.data["policy"]["automatic_canonical_writes"] = True
        self.assertIn("majority_vote", self.errors())
        self.assertIn("automatic_canonical_writes", self.errors())

    def test_generated_pixels_are_not_evidence(self):
        self.data["units"][0]["generated_images_used"] = True
        self.assertIn("generated images", self.errors())

    def test_no_claim_of_unperformed_review(self):
        self.data["units"][0]["review_mode"] = "two-blinded-models"
        self.assertIn("unperformed second review", self.errors())

    def test_counterargument_required(self):
        self.data["units"][0]["decision"]["counterargument"] = ""
        self.assertIn("counterargument", self.errors())

    def test_model_probability_is_not_editorial_confidence(self):
        self.data["units"][0]["decision"]["priority_confidence"] = 0.99
        self.assertIn("qualitative", self.errors())

    def test_no_coverage_is_not_a_vote(self):
        witness = self.data["units"][0]["witnesses"][1]
        witness["coverage_confirmed"] = False
        witness["attestation"] = "no-coverage"
        self.assertIn("no coverage", self.errors())

    def test_sources_must_resolve(self):
        self.data["units"][0]["witnesses"][1]["source_refs"] = ["invented-source"]
        self.assertIn("source references", self.errors())

    def test_versions_are_not_direct_hebrew(self):
        self.data["units"][0]["witnesses"][2]["support_scope"] = "direct-wording"
        self.assertIn("not direct Hebrew", self.errors())

    def test_preference_requires_attestation(self):
        unit = self.data["units"][0]
        for witness in unit["witnesses"]:
            witness["supports"] = "six"
        self.assertIn("no cited attestation", self.errors())

    def test_unresolved_outcome_supported(self):
        decision = self.data["units"][0]["decision"]
        decision.update(status="unresolved", preferred=None, exact_wording_resolved=False)
        self.assertEqual(MODULE.validate(self.data), [])

    def test_report_is_reproducible(self):
        self.assertEqual(MODULE.REPORT.read_text(), MODULE.render(self.data))
        self.assertIn("not new image restorations", MODULE.render(self.data))


if __name__ == "__main__":
    unittest.main()
