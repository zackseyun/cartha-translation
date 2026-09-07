import copy
import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import validate as validate_schema
from tests.test_dss_pilot import proposal
from pilot import compare, validate_result


def observation(provider="openai", status="no-visible-text"):
    run = proposal(provider)
    run["result"]["observation_protocol"] = "2.0"
    region = run["result"]["regions"][0]
    region["observation"] = status
    region["notes"] = "Image-only observation; no inferred missing wording."
    if status != "text-present":
        region["lines"] = []
    return run


class ObservationProtocolTests(unittest.TestCase):
    def test_frozen_development_control_inputs(self):
        root = Path(__file__).resolve().parents[1]
        directory = root / "sources/dead_sea_scrolls/pilots/2026-09-06-observation-development"
        freeze = json.loads((directory / "freeze.json").read_text())
        for path, digest in freeze["sha256"].items():
            self.assertEqual(hashlib.sha256((directory / path).read_bytes()).hexdigest(), digest, path)
        labels = json.loads((directory / "reference-labels.json").read_text())["labels"]
        regions = json.loads((directory / "regions.json").read_text())["regions"]
        self.assertEqual([r["id"] for r in regions], [r["region_id"] for r in labels])
        self.assertEqual(sum(r["expected_observation"] == "text-present" for r in labels), 2)
        self.assertEqual(sum(r["expected_observation"] == "no-visible-text" for r in labels), 2)
        self.assertFalse(freeze["held_out"])
        self.assertFalse(freeze["glyph_accuracy_evaluation"])

    def test_all_explicit_observations_validate(self):
        schema = json.loads((Path(__file__).resolve().parents[1] /
                             "sources/dead_sea_scrolls/protocols/observation-v2.schema.json").read_text())
        for status in ("text-present", "no-visible-text", "unassessable"):
            result = observation(status=status)["result"]
            validate_schema(result, schema)
            validate_result(result, ["region-a"])

    def test_matching_empty_observations_are_not_accepted_letters(self):
        report = compare(observation(), observation("anthropic"))
        self.assertEqual(report["schema_version"], "2.0.0")
        self.assertEqual(report["accepted_tokens"], 0)
        self.assertEqual(report["compared_tokens"], 0)
        self.assertEqual(report["tokens"], [])
        self.assertEqual(report["region_observations"][0]["status"], "matching-observations")

    def test_unassessable_is_not_blank_success(self):
        report = compare(observation(status="unassessable"),
                         observation("anthropic", "unassessable"))
        self.assertEqual(report["region_observations"][0]["status"], "unassessable")
        self.assertTrue(report["unresolved_lines"])
        self.assertEqual(report["accepted_tokens"], 0)

    def test_different_observations_remain_unresolved(self):
        for other in ("text-present", "unassessable"):
            report = compare(observation(), observation("anthropic", other))
            self.assertTrue(report["unresolved_lines"])
            self.assertEqual(report["accepted_tokens"], 0)

    def test_v2_text_still_uses_existing_token_comparison(self):
        report = compare(observation(status="text-present"),
                         observation("anthropic", "text-present"))
        self.assertEqual(report["accepted_tokens"], 1)

    def test_invalid_or_contradictory_observations_fail(self):
        base = observation()["result"]
        mutations = [
            lambda r: r.pop("observation_protocol"),
            lambda r: r.update(observation_protocol="3.0"),
            lambda r: r["regions"][0].pop("observation"),
            lambda r: r["regions"][0].update(observation="blank"),
            lambda r: r["regions"][0].update(observation="text-present"),
            lambda r: r["regions"][0].update(notes=" "),
            lambda r: r["regions"][0].update(lines=proposal()["result"]["regions"][0]["lines"]),
        ]
        for mutate in mutations:
            result = copy.deepcopy(base)
            mutate(result)
            with self.assertRaises(ValueError):
                validate_result(result, ["region-a"])

    def test_mixed_protocols_fail(self):
        with self.assertRaises(ValueError):
            compare(proposal(), observation("anthropic", "text-present"))

    def test_no_regions_does_not_become_success(self):
        with self.assertRaises(ValueError):
            validate_result({"regions": []}, [])

    def test_frozen_schema_is_enforced_when_supplied(self):
        schema = json.loads((Path(__file__).resolve().parents[1] /
                             "sources/dead_sea_scrolls/protocols/observation-v2.schema.json").read_text())
        result = observation()["result"]
        validate_result(result, ["region-a"], response_schema=schema)
        result["extra"] = "unexpected field"
        with self.assertRaises(ValueError):
            validate_result(result, ["region-a"], response_schema=schema)

    def test_text_present_requires_notes_before_comparison(self):
        run = observation(status="text-present")
        del run["result"]["regions"][0]["notes"]
        with self.assertRaises(ValueError):
            compare(run, observation("anthropic", "text-present"))


if __name__ == "__main__":
    unittest.main()
