import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools/dss"))
from pilot import DEFAULT_PILOT, compare, normal, validate, validate_result
from run_pilot import parse_claude


def proposal(provider="openai", text="אלהים", certainty="clear"):
    return {
        "provider": provider,
        "effective_model": "gpt-5.6-sol" if provider == "openai" else "claude-opus-5",
        "status": "succeeded", "prompt_sha256": "a" * 64, "crop_sha256": ["b" * 64],
        "result": {"regions": [{"region_id": "region-a", "notes": "", "lines": [
            {"line_index": 1, "tokens": [{"text": text, "certainty": certainty}], "notes": ""}
        ]}]},
    }


class DssPilotTests(unittest.TestCase):
    def test_saved_pilot_hashes_and_comparison(self):
        validate(DEFAULT_PILOT)

    def test_success_subtype_does_not_hide_claude_access_error(self):
        events = [
            {"type": "system", "subtype": "init", "model": "claude-opus-5"},
            {"type": "result", "subtype": "success", "is_error": True,
             "result": "Your organization has disabled Claude subscription access for Claude Code"},
        ]
        status, model, result, error = parse_claude(events, 1)
        self.assertEqual(status, "blocked")
        self.assertEqual(model, "claude-opus-5")
        self.assertIsNone(result)
        self.assertIn("disabled", error)

    def test_missing_provider_never_creates_consensus(self):
        second = {"status": "blocked", "result": None}
        report = compare(proposal(), second)
        self.assertEqual(report["accepted_tokens"], 0)
        self.assertEqual(report["status"], "awaiting-two-successful-passes")

    def test_same_family_rejected(self):
        with self.assertRaises(ValueError):
            compare(proposal(), proposal())

    def test_input_mismatch_rejected(self):
        for field in ("prompt_sha256", "crop_sha256"):
            second = proposal("anthropic")
            second[field] = "changed"
            with self.assertRaises(ValueError):
                compare(proposal(), second)

    def test_wrong_model_rejected(self):
        second = proposal("anthropic")
        second["effective_model"] = "some-other-model"
        with self.assertRaises(ValueError):
            compare(proposal(), second)

    def test_additional_tool_access_requires_audit(self):
        second = proposal("anthropic")
        second["tool_events"] = ["command_execution"]
        with self.assertRaises(ValueError):
            compare(proposal(), second)

    def test_clear_exact_agreement_is_research_consensus(self):
        report = compare(proposal(), proposal("anthropic"))
        self.assertEqual(report["accepted_tokens"], 1)
        self.assertIn("research", report["publication_action"])

    def test_matching_uncertainty_is_not_visible_ink(self):
        for certainty in ("uncertain", "unreadable", "gap"):
            report = compare(proposal(certainty=certainty), proposal("anthropic", certainty=certainty))
            self.assertEqual(report["accepted_tokens"], 0)

    def test_markers_and_non_hebrew_never_promoted(self):
        for text in ("[אלהים]", "אל□ים", "אלהים?", "[—]", "123"):
            report = compare(proposal(text=text), proposal("anthropic", text=text))
            self.assertEqual(report["accepted_tokens"], 0)

    def test_final_letter_shapes_not_normalized_away(self):
        self.assertNotEqual(normal("מלך"), normal("מלכ"))
        report = compare(proposal(text="מלך"), proposal("anthropic", text="מלכ"))
        self.assertEqual(report["accepted_tokens"], 0)

    def test_segmentation_disagreement_is_not_positionally_aligned(self):
        second = proposal("anthropic")
        second["result"]["regions"][0]["lines"][0]["tokens"].append({"text": "אמר", "certainty": "clear"})
        report = compare(proposal(), second)
        self.assertEqual(report["accepted_tokens"], 0)
        self.assertEqual(report["unresolved_lines"][0]["reason"], "token-segmentation-disagreement")

    def test_line_count_disagreement_does_not_shift_rows(self):
        second = proposal("anthropic")
        lines = second["result"]["regions"][0]["lines"]
        lines.append(copy.deepcopy(lines[0]))
        lines[-1]["line_index"] = 2
        report = compare(proposal(), second)
        self.assertEqual(report["accepted_tokens"], 0)
        self.assertEqual(report["unresolved_lines"][0]["reason"], "line-count-disagreement")

    def test_success_without_structured_reading_is_failure(self):
        status, _, result, _ = parse_claude([
            {"type": "result", "subtype": "success", "is_error": False, "result": "Done"}
        ], 0)
        self.assertEqual(status, "failed")
        self.assertIsNone(result)

    def test_duplicate_region_and_empty_success_rejected(self):
        data = proposal()["result"]
        data["regions"].append(copy.deepcopy(data["regions"][0]))
        with self.assertRaises(ValueError):
            validate_result(data, ["region-a"])
        data["regions"] = data["regions"][:1]
        data["regions"][0]["lines"] = []
        with self.assertRaises(ValueError):
            validate_result(data, ["region-a"])


if __name__ == "__main__":
    unittest.main()
