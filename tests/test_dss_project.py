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


if __name__ == "__main__":
    unittest.main()
