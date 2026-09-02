import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    path = ROOT / "tools/dss/validate_project.py"
    spec = importlib.util.spec_from_file_location("dss_validate_project", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class DssProjectTest(unittest.TestCase):
    def test_dss_registry_rights_gates_and_hashes(self):
        validator = load_validator()
        self.assertEqual(validator.main(), 0)

    def test_permission_required_records_do_not_expose_downloads(self):
        registry = json.loads((ROOT / "sources/dead_sea_scrolls/registry.v1.json").read_text())
        for record in registry["records"]:
            for image in record.get("images", []):
                if image["rights"]["status"] == "permission-required":
                    self.assertNotIn("downloads", image)

    def test_transcription_schema_distinguishes_visible_and_supplied_text(self):
        schema = json.loads((ROOT / "schemas/dss-transcription.schema.json").read_text())
        token = schema["properties"]["lines"]["items"]["properties"]["tokens"]["items"]
        certainty = token["properties"]["certainty"]["enum"]
        source = token["properties"]["source"]["enum"]
        self.assertIn("visible", certainty)
        self.assertIn("supplied", certainty)
        self.assertIn("ink", source)
        self.assertIn("editorial-conjecture", source)

    def test_transcription_schema_supports_machine_only_corroboration(self):
        schema = json.loads((ROOT / "schemas/dss-transcription.schema.json").read_text())
        statuses = schema["properties"]["status"]["enum"]
        agent_types = schema["properties"]["passes"]["items"]["properties"]["agent_type"]["enum"]
        self.assertIn("machine-observed", statuses)
        self.assertIn("machine-consensus-accepted", statuses)
        self.assertIn("machine-consensus-restored", statuses)
        self.assertIn("machine-corroborated", statuses)
        self.assertIn("hypothesis-only", statuses)
        self.assertNotIn("human-review", statuses)
        self.assertNotIn("human", agent_types)
        self.assertIn("machine_corroboration", schema["properties"])
        self.assertIn("model_consensus", schema["properties"])
        consensus = schema["properties"]["model_consensus"]
        self.assertEqual(consensus["properties"]["different_model_families"]["const"], True)
        self.assertEqual(consensus["properties"]["pass_refs"]["minItems"], 2)
        accepted_rule = consensus["allOf"][0]
        self.assertEqual(
            accepted_rule["then"]["properties"]["exact_match"]["const"], True
        )
        restoration_statuses = (
            schema["properties"]["restoration_candidates"]["items"]
            ["properties"]["status"]["enum"]
        )
        self.assertIn("machine-consensus-restored", restoration_statuses)


if __name__ == "__main__":
    unittest.main()
