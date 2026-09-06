import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("psalm145_check", ROOT / "tools/textual_restoration/build_psalm145_check.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class Psalm145Tests(unittest.TestCase):
    def test_real_wlc_acrostic_excludes_title_not_initial_aleph(self):
        verses = [v for v in ET.parse(ROOT / "sources/ot/wlc/Ps.xml").findall(".//o:verse", M.NS)
                  if v.get("osisID", "").startswith("Ps.145.")]
        result = M.acrostic(verses)
        self.assertEqual(result["stanza_count"], 21)
        self.assertEqual(result["opening_letters"], M.ALPHABET.replace("נ", ""))
        self.assertEqual(result["missing_alphabet_letters"], "נ")
        with self.assertRaisesRegex(ValueError, "unique and consecutive"):
            M.acrostic(verses[::-1])

    def test_title_boundary_must_be_explicit(self):
        verse = ET.fromstring(f'<verse xmlns="{M.NS["o"]}" osisID="Ps.145.1"><w>אחר</w><w>לדוד</w><w>ארוממך</w></verse>')
        with self.assertRaisesRegex(ValueError, "superscription boundary"):
            M.acrostic([verse])

    def test_witness_wording_is_not_harmonized(self):
        data = json.loads((ROOT / "sources/textual_restoration/comparisons/psalms_controls.v1.json").read_text())
        case = next(c for c in data["cases"] if c["id"] == "PSA.145.13.nun")
        readings = {r["source_ref"]: r for r in case["readings"]}
        self.assertEqual(readings["qumran-digital-psalms"]["text"], "נאמן אלוהים בדבריו וחסיד בכול מעשיו")
        self.assertIn("κύριος ἐν τοῖς λόγοις", readings["lxx-morph-rahlfs"]["text"])
        self.assertIn("ܘܙܕܝܩ", readings["cal-peshitta-psalms"]["text"])
        self.assertEqual(readings["pob-wlc"]["text"], "∅")
        self.assertIsNone(case["preferred_reading"])
        self.assertFalse(case["canonical_change_applied"])

    def test_saved_receipt_does_not_turn_index_or_acrostic_into_ink(self):
        data = json.loads(M.OUT.read_text())
        self.assertFalse(data["qdr_mapping"]["qdr_word_tags_alone_isolate_nun_line"])
        self.assertEqual(data["greek"]["reference"], "Ps 144:13a")
        self.assertTrue(all(v is False for v in data["policy"].values()))

    def test_latin_editions_remain_distinct_not_hebrew_votes(self):
        data = json.loads((ROOT / "sources/textual_restoration/comparisons/psalms_controls.v1.json").read_text())
        case = next(c for c in data["cases"] if c["id"] == "PSA.145.13.nun")
        readings = {r["source_ref"]: r for r in case["readings"]}
        sources = {s["id"]: s for s in data["sources"]}
        heb = "weber-gryson-psalter-hebrew"
        greek = "weber-gryson-psalter-greek"
        harden = "harden-hebrew-psalter-1922"
        self.assertEqual(readings[heb]["text"], "∅")
        self.assertIn("omnibus verbis", readings[greek]["text"])
        self.assertIn("omnibus uerbis", readings[harden]["text"])
        self.assertIn("operibus suis AHR", readings[harden]["locator"])
        self.assertIn("Ricemarch", sources[harden]["witness_basis"])
        self.assertIn("earlier published collations", sources[harden]["witness_basis"])
        for key in (heb, greek, harden):
            self.assertFalse(sources[key]["manuscript_level"])
            self.assertNotIn("witness_id", readings[key])

    def test_pilot_does_not_claim_uniform_jerome_absence(self):
        data = json.loads((ROOT / "sources/textual_restoration/decisions/hebrew_pilot.v1.json").read_text())
        unit = next(u for u in data["units"] if u["id"] == "PSA.145.13.nun")
        witnesses = {w["id"]: w for w in unit["witnesses"]}
        self.assertEqual(witnesses["jerome-hebrew"]["supports"], "absent")
        self.assertEqual(witnesses["jerome-hebrew-harden"]["supports"], "present")
        for key in ("gall", "jerome-hebrew", "jerome-hebrew-harden"):
            self.assertEqual(witnesses[key]["role"], "critical-edition")
            self.assertEqual(witnesses[key]["dating"]["kind"], "edition-publication")
            self.assertFalse(witnesses[key]["archival_image_checked"])
        self.assertFalse(unit["decision"]["exact_wording_resolved"])

    def test_note_preserves_witness_specific_gloss_and_unchanged_source(self):
        import yaml
        verse = yaml.safe_load((ROOT / "translation/ot/psalms/145/013.yaml").read_text())
        note = next(n for n in verse["translation"]["footnotes"] if n["marker"] == "b")
        self.assertIn("God is faithful in his words", note["text"])
        self.assertNotIn("faithful in all his words", note["text"])
        self.assertNotIn("נאמן", verse["source"]["text"])
        self.assertEqual(verse["translation"]["text"], "Your kingdom is a kingdom for all ages[a], and your dominion is throughout every generation.[b]")


if __name__ == "__main__":
    unittest.main()
