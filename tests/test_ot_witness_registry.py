import copy
import importlib.util
import json
import unittest
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_ot_witness_registry",
    ROOT / "tools/textual_restoration/validate_ot_witness_registry.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)

EXTRACT_SPEC = importlib.util.spec_from_file_location(
    "extract_qdr_passages",
    ROOT / "tools/textual_restoration/extract_qdr_passages.py",
)
EXTRACT_MODULE = importlib.util.module_from_spec(EXTRACT_SPEC)
assert EXTRACT_SPEC.loader
EXTRACT_SPEC.loader.exec_module(EXTRACT_MODULE)


class OtWitnessRegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(MODULE.REGISTRY.read_text())
        self.coverage = json.loads(MODULE.COVERAGE.read_text())
        self.comparison = json.loads(MODULE.COMPARISON.read_text())
        self.samuel_coverage = json.loads(MODULE.SAMUEL_COVERAGE.read_text())
        self.samuel_comparison = json.loads(MODULE.SAMUEL_COMPARISON.read_text())
        self.selections = json.loads(MODULE.SELECTIONS.read_text())
        self.adjudication = json.loads(MODULE.ADJUDICATION.read_text())

    def test_current_registry(self):
        self.assertEqual(MODULE.validate(self.data), [])
        self.assertEqual(MODULE.validate_coverage(self.coverage, self.data), [])
        self.assertEqual(MODULE.validate_comparison(self.comparison), [])
        self.assertEqual(MODULE.validate_coverage(self.samuel_coverage, self.data), [])
        self.assertEqual(MODULE.validate_comparison(self.samuel_comparison), [])
        self.assertEqual(
            MODULE.validate_selections(self.selections, self.comparison, self.adjudication), []
        )
        summary = MODULE.summarize(self.data)
        self.assertGreaterEqual(summary["registered_witnesses_or_families"], 10)
        self.assertGreater(summary["restoration_candidates"], 0)

    def test_psalms_case_and_coverage_validate(self):
        comparison = json.loads(MODULE.PSALMS_COMPARISON.read_text())
        coverage = json.loads(MODULE.PSALMS_COVERAGE.read_text())
        self.assertEqual(MODULE.validate_comparison(comparison), [])
        self.assertEqual(MODULE.validate_coverage(coverage, self.data), [])
        self.assertEqual(len(coverage["records"]), 3)

    def test_psalm_22_4q88_supplied_waw_cannot_be_promoted(self):
        comparison = json.loads(MODULE.PSALMS_COMPARISON.read_text())
        case = next(c for c in comparison["cases"] if c["id"] == "PSA.22.16.hands-feet")
        reading = next(r for r in case["readings"] if r.get("witness_id") == "4q88")
        self.assertIn("כ֯ר֯[ו ]", reading["text"])
        self.assertEqual(reading["support_status"], "indeterminate-lacuna")
        reading["support_status"] = "supports-reading"
        self.assertTrue(any("indeterminate lacuna" in e for e in MODULE.validate_comparison(comparison)))

    def test_psalm_22_preserves_published_spelling_not_normalized_verb(self):
        comparison = json.loads(MODULE.PSALMS_COMPARISON.read_text())
        case = next(c for c in comparison["cases"] if c["id"] == "PSA.22.16.hands-feet")
        reading = next(r for r in case["readings"] if r.get("witness_id") == "5-6hev1b")
        self.assertEqual(reading["text"], "כארו ידיה֯")
        self.assertIn("meaning-unresolved", reading["reading_class"])
        self.assertIsNone(case["preferred_reading"])
        self.assertFalse(case["canonical_change_applied"])

    def test_psalm_22_numbering_and_main_text_remain_explicit(self):
        import yaml
        verse = yaml.safe_load((ROOT / "translation/ot/psalms/022/016.yaml").read_text())
        self.assertEqual(verse["translation"]["text"], "For dogs have surrounded me; a company of evildoers has encircled me; like a lion—my hands and my feet.[a]")
        self.assertIn("כָּ֝/אֲרִ֗י", verse["source"]["text"])
        comparison = json.loads(MODULE.PSALMS_COMPARISON.read_text())
        self.assertIn("21:17", comparison["scope"])
        self.assertIn("22:17", comparison["scope"])
        self.assertTrue(all(r["pixels_acquired"] is False for r in json.loads(MODULE.PSALMS_COVERAGE.read_text())["records"]))

    def test_psalm_22_versions_remain_edition_controls_in_their_own_languages(self):
        comparison = json.loads(MODULE.PSALMS_COMPARISON.read_text())
        sources = {s["id"]: s for s in comparison["sources"]}
        case = next(c for c in comparison["cases"] if c["id"] == "PSA.22.16.hands-feet")
        readings = {r["source_ref"]: r for r in case["readings"]}
        for source_id, language in (("cal-peshitta-psalms", "Syriac"),
                                    ("cal-targum-psalms", "Aramaic")):
            with self.subTest(source_id=source_id):
                self.assertFalse(sources[source_id]["manuscript_level"])
                self.assertEqual(readings[source_id]["language"], language)
                self.assertNotIn("witness_id", readings[source_id])
                self.assertIn("022:017", readings[source_id]["locator"])
                self.assertEqual(readings[source_id]["support_status"], "supports-reading")

    def test_psalm_22_targum_action_does_not_erase_lion_or_become_syriac_verb(self):
        comparison = json.loads(MODULE.PSALMS_COMPARISON.read_text())
        case = next(c for c in comparison["cases"] if c["id"] == "PSA.22.16.hands-feet")
        readings = {r["source_ref"]: r for r in case["readings"]}
        targum = readings["cal-targum-psalms"]
        syriac = readings["cal-peshitta-psalms"]
        self.assertEqual(targum["text"], "נכתין היך כאריא אידי ורגלי")
        self.assertEqual(targum["reading_class"], "aramaic-lion-with-biting-expansion")
        self.assertEqual(syriac["text"], "ܒܙܥܘ ܐ̈ܝܕܝ ܘܪ̈ܓܠܝ")
        self.assertNotEqual(targum["relationship_group"], syriac["relationship_group"])
        self.assertIsNone(case["preferred_reading"])

    def test_cal_psalms_registry_is_not_a_new_ancient_manuscript_count(self):
        entries = {w["id"]: w for w in self.data["witnesses"]}
        for source_id, language in (("cal-peshitta-ot", "Syriac"),
                                    ("cal-targum-psalms", "Aramaic")):
            with self.subTest(source_id=source_id):
                entry = entries[source_id]
                self.assertEqual(entry["witness_class"], "modern-transcription")
                self.assertEqual(entry["date_basis"]["kind"], "edition-publication")
                self.assertEqual(entry["languages"], [language])
                self.assertEqual(entry["coverage_status"], "partial-map")
                self.assertIn("22:17", entry["corpus_coverage"])

    def test_imagegen_cannot_be_promoted_to_evidence(self):
        data = copy.deepcopy(self.data)
        data["policy"]["imagegen_is_evidence"] = True
        self.assertTrue(any("ImageGen" in e for e in MODULE.validate(data)))

    def test_duplicate_ids_are_rejected(self):
        data = copy.deepcopy(self.data)
        data["witnesses"].append(copy.deepcopy(data["witnesses"][0]))
        self.assertTrue(any("unique" in e for e in MODULE.validate(data)))

    def test_relationship_group_is_required(self):
        data = copy.deepcopy(self.data)
        data["witnesses"][0]["relationship_group"] = ""
        self.assertTrue(any("relationship group" in e for e in MODULE.validate(data)))

    def test_local_sources_must_resolve(self):
        data = copy.deepcopy(self.data)
        data["witnesses"][0]["repo_path"] = "sources/not-present"
        self.assertTrue(any("repo_path" in e for e in MODULE.validate(data)))

    def test_summary_partitions_coverage(self):
        summary = MODULE.summarize(self.data)
        self.assertEqual(
            summary["registered_witnesses_or_families"],
            summary["coverage_mapped"] + summary["coverage_partial"] + summary["coverage_unmapped"],
        )

    def test_coverage_must_resolve_to_registered_witness(self):
        data = copy.deepcopy(self.coverage)
        data["records"][0]["witness_id"] = "invented-witness"
        self.assertTrue(any("unknown witness" in e for e in MODULE.validate_coverage(data, self.data)))

    def test_coverage_does_not_smuggle_in_unmanifested_pixels(self):
        data = copy.deepcopy(self.coverage)
        data["records"][0]["pixels_acquired"] = True
        self.assertTrue(any("pixels" in e for e in MODULE.validate_coverage(data, self.data)))

    def test_published_transcription_requires_physical_manuscript_identity(self):
        data = copy.deepcopy(self.coverage)
        record = next(r for r in data["records"] if r["coverage_basis"] == "published-transcription-index")
        record["manuscript_id"] = ""
        self.assertTrue(any("manuscript identity" in e for e in MODULE.validate_coverage(data, self.data)))

    def test_published_transcription_requires_reading_support_status(self):
        data = copy.deepcopy(self.coverage)
        record = next(r for r in data["records"] if r["coverage_basis"] == "published-transcription-index")
        record.pop("reading_support_status", None)
        self.assertTrue(any("reading support status" in e for e in MODULE.validate_coverage(data, self.data)))

    def test_control_comparison_cannot_select_a_reading(self):
        data = copy.deepcopy(self.comparison)
        data["cases"][0]["decision_status"] = "preferred"
        data["cases"][0]["preferred_reading"] = "longer"
        self.assertTrue(any("cannot select" in e for e in MODULE.validate_comparison(data)))

    def test_control_comparison_detects_baseline_drift(self):
        data = copy.deepcopy(self.comparison)
        data["cases"][0]["baseline"]["sha256"] = "0" * 64
        self.assertTrue(any("baseline drift" in e for e in MODULE.validate_comparison(data)))

    def test_direct_transcription_requires_a_locator(self):
        data = copy.deepcopy(self.comparison)
        reading = next(
            r for c in data["cases"] for r in c["readings"]
            if r["source_ref"] == "qumran-digital-dss"
        )
        reading["locator"] = ""
        self.assertTrue(any("physical manuscript identity" in e for e in MODULE.validate_comparison(data)))

    def test_physical_manuscript_cannot_be_counted_twice(self):
        data = copy.deepcopy(self.comparison)
        direct = next(r for r in data["cases"][0]["readings"] if r["source_ref"] == "qumran-digital-dss")
        data["cases"][0]["readings"].append(copy.deepcopy(direct))
        self.assertTrue(any("counted more than once" in e for e in MODULE.validate_comparison(data)))

    def test_lacuna_cannot_be_promoted_to_reading_support(self):
        data = copy.deepcopy(self.comparison)
        case = next(c for c in data["cases"] if c["id"] == "DEU.27.4.mountain")
        direct = next(r for r in case["readings"] if r["source_ref"] == "qumran-digital-dss")
        direct["support_status"] = "supports-reading"
        self.assertTrue(any("indeterminate lacuna" in e for e in MODULE.validate_comparison(data)))

    def test_partial_verse_coverage_cannot_be_promoted_to_reading_support(self):
        data = copy.deepcopy(self.comparison)
        case = next(c for c in data["cases"] if c["id"] == "DEU.32.8.referent")
        direct = next(r for r in case["readings"] if r.get("witness_id") == "4q45")
        direct["support_status"] = "supports-reading"
        self.assertTrue(any("coverage-only material" in e for e in MODULE.validate_comparison(data)))

    def test_exodus_supplied_words_cannot_be_promoted_to_preserved_support(self):
        for witness_id in ("4q11", "2q2"):
            with self.subTest(witness_id=witness_id):
                data = copy.deepcopy(self.comparison)
                reading = next(r for c in data["cases"] for r in c["readings"]
                               if r.get("witness_id") == witness_id)
                self.assertEqual(reading["support_status"], "indeterminate-lacuna")
                reading["support_status"] = "supports-reading"
                self.assertTrue(any("indeterminate lacuna" in e
                                    for e in MODULE.validate_comparison(data)))

    def test_4q14_support_is_local_not_whole_verse_geography(self):
        reading = next(r for c in self.comparison["cases"] for r in c["readings"]
                       if r.get("witness_id") == "4q14")
        self.assertEqual(reading["reading_class"], "egypt-followed-directly-by-duration")

    def test_samuel_disputed_or_unassigned_traces_cannot_become_support(self):
        for witness_id in ("4q52", "1q7"):
            with self.subTest(witness_id=witness_id):
                data = copy.deepcopy(self.samuel_comparison)
                reading = next(r for c in data["cases"] for r in c["readings"]
                               if r.get("witness_id") == witness_id)
                self.assertEqual(reading["support_status"], "coverage-only")
                reading["support_status"] = "supports-reading"
                self.assertTrue(any("coverage-only material" in e
                                    for e in MODULE.validate_comparison(data)))
                coverage = next(r for r in self.samuel_coverage["records"]
                                if r.get("manuscript_id") == witness_id)
                self.assertEqual(coverage["coverage_status"], "uncertain")

    def test_chronicles_is_a_parallel_composition_not_a_samuel_manuscript(self):
        source = next(s for s in self.samuel_comparison["sources"]
                      if s["id"] == "pob-wlc-chronicles-parallel")
        self.assertEqual(source["role"], "parallel-literary-account-not-samuel-manuscript")
        self.assertFalse(source.get("manuscript_level", False))

    def test_samuel_offering_preserves_age_word_but_not_supplied_animal_phrase(self):
        case = next(c for c in self.samuel_comparison["cases"]
                    if c["id"] == "1SA.1.24.offering")
        reading = next(r for r in case["readings"] if r.get("witness_id") == "4q51")
        self.assertEqual(reading["text"], "[בפר בן ]בקר משלש ולחם")
        self.assertEqual(reading["support_status"], "supports-reading")
        self.assertEqual(reading["reading_class"], "preserved-age-related-meshullash-and-bread")
        self.assertIsNone(case["preferred_reading"])
        self.assertFalse(case["canonical_change_applied"])
        coverage = next(r for r in self.samuel_coverage["records"]
                        if r["id"] == "1SA.1.24@4q51")
        self.assertTrue(coverage["pixels_acquired"])
        self.assertFalse(coverage["image_inspection"]["complete_image_verification"])
        self.assertEqual(coverage["next_gate"], "image-verification")

    def test_private_image_check_does_not_claim_blind_or_complete_review(self):
        data = copy.deepcopy(self.samuel_coverage)
        r = next(r for r in data["records"] if r["id"] == "1SA.1.24@4q51")
        r["image_inspection"]["complete_image_verification"] = True
        self.assertTrue(any("complete verification" in e
                            for e in MODULE.validate_coverage(data, self.data)))
        r["image_inspection"]["mode"] = "blind-independent"
        self.assertTrue(any("context-informed" in e
                            for e in MODULE.validate_coverage(data, self.data)))

    def test_samuel_peshitta_support_does_not_import_bread(self):
        case = next(c for c in self.samuel_comparison["cases"] if c["id"] == "1SA.1.24.offering")
        reading = next(r for r in case["readings"] if r["source_ref"] == "cal-peshitta-samuel")
        self.assertEqual(reading["language"], "Syriac")
        self.assertEqual(reading["text"], "ܒܬܘܪܐ ܬܘܠܬܐ܂ ܘܣܐܬܐ ܚܕܐ ܕܩܡܚܐ܂")
        self.assertEqual(reading["reading_class"], "age-related-bull-without-bread")
        self.assertEqual(reading["relationship_group"], "syriac-peshitta")
        source = next(s for s in self.samuel_comparison["sources"] if s["id"] == reading["source_ref"])
        self.assertFalse(source["manuscript_level"])
        self.assertIn("not text snapshots", source["snapshot"])

    def test_samuel_symmachus_is_marginal_not_continuous_lxx(self):
        case = next(c for c in self.samuel_comparison["cases"] if c["id"] == "1SA.1.24.offering")
        readings = [r for r in case["readings"] if r["source_ref"] == "cambridge-samuel-1927"]
        self.assertEqual(len(readings), 2)
        marginal = next(r for r in readings if r["relationship_group"] == "hexaplaric-symmachus")
        self.assertEqual(marginal["text"], "μετὰ ταύρων τριῶν")
        self.assertIn("not its continuous text", marginal["locator"])
        self.assertNotIn("witness_id", marginal)
        base = next(r for r in readings if r["relationship_group"] == "greek-edition-control")
        rahlfs = next(r for r in case["readings"] if r["source_ref"] == "lxx-morph-rahlfs")
        self.assertEqual(base["relationship_group"], rahlfs["relationship_group"])
        self.assertIsNone(case["preferred_reading"])
        self.assertFalse(case["canonical_change_applied"])

    def test_new_versional_access_entries_are_not_manuscript_counts(self):
        entries = {w["id"]: w for w in self.data["witnesses"]}
        self.assertEqual(entries["cal-peshitta-ot"]["witness_class"], "modern-transcription")
        self.assertEqual(entries["cambridge-lxx-samuel-1927"]["witness_class"], "critical-apparatus")
        for key in ("cal-peshitta-ot", "cambridge-lxx-samuel-1927"):
            self.assertEqual(entries[key]["coverage_status"], "partial-map")
            self.assertEqual(entries[key]["restoration_suitability"], "none")

    def test_private_image_hash_verification_reports_missing_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = MODULE.verify_private_images(self.samuel_coverage, Path(directory))
            self.assertEqual(len(errors), 2)
            self.assertTrue(all("private image missing" in e for e in errors))

    def selection_errors(self, data):
        return MODULE.validate_selections(data, self.comparison, self.adjudication)

    def test_private_image_hash_match_and_mismatch(self):
        data = copy.deepcopy(self.samuel_coverage)
        receipt = next(r["image_inspection"] for r in data["records"] if r.get("image_inspection"))
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / receipt["private_copy_key"]
            folder.mkdir()
            for asset in receipt["assets"]:
                (folder / asset["file_name"]).write_bytes(b"synthetic test bytes, not manuscript evidence")
                asset["sha256"] = MODULE.hashlib.sha256((folder / asset["file_name"]).read_bytes()).hexdigest()
            self.assertEqual(MODULE.verify_private_images(data, Path(directory)), [])
            receipt["assets"][0]["sha256"] = "0" * 64
            self.assertTrue(any("hash mismatch" in e for e in MODULE.verify_private_images(data, Path(directory))))

    def test_private_image_malformed_metadata_is_reported(self):
        for field, value in (("private_copy_key", "../outside"), ("assets", []), ("assets", [{}])):
            data = copy.deepcopy(self.samuel_coverage)
            receipt = next(r["image_inspection"] for r in data["records"] if r.get("image_inspection"))
            receipt[field] = value
            with tempfile.TemporaryDirectory() as directory:
                self.assertTrue(any("invalid private image" in e for e in MODULE.verify_private_images(data, Path(directory))))

    def test_private_image_symlink_cannot_escape_root(self):
        data = copy.deepcopy(self.samuel_coverage)
        receipt = next(r["image_inspection"] for r in data["records"] if r.get("image_inspection"))
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            (Path(directory) / receipt["private_copy_key"]).symlink_to(Path(outside), target_is_directory=True)
            errors = MODULE.verify_private_images(data, Path(directory))
            self.assertEqual(len(errors), 2)
            self.assertTrue(all("outside supplied root" in e for e in errors))

    def test_selection_imagegen_cannot_be_evidence(self):
        data = copy.deepcopy(self.selections)
        data["selections"][0]["generated_images_used"] = True
        self.assertTrue(any("generated images" in e for e in self.selection_errors(data)))

    def test_selection_detects_baseline_drift(self):
        data = copy.deepcopy(self.selections)
        data["selections"][0]["baseline"]["sha256"] = "0" * 64
        self.assertTrue(any("baseline drift" in e for e in self.selection_errors(data)))

    def test_selection_requires_direct_supported_reading(self):
        data = copy.deepcopy(self.selections)
        data["selections"][0]["critical_source"]["source_manuscripts"] = ["4q45"]
        self.assertTrue(any("direct comparison support" in e for e in self.selection_errors(data)))

    def test_selection_cannot_advance_with_pending_gates(self):
        data = copy.deepcopy(self.selections)
        data["selections"][0]["promotion_status"] = "ready-for-promotion"
        self.assertTrue(any("review gates" in e for e in self.selection_errors(data)))

    def test_selection_requires_atomic_policy(self):
        data = copy.deepcopy(self.selections)
        data["policy"]["source_and_english_promote_atomically"] = False
        self.assertTrue(any("atomically" in e for e in self.selection_errors(data)))

    def test_empty_gates_cannot_bypass_review(self):
        data = copy.deepcopy(self.selections)
        data["selections"][0]["review_gates"] = {}
        self.assertTrue(any("required review gates" in e for e in self.selection_errors(data)))

    def test_pilot_cannot_certify_promotion_even_with_completed_flags(self):
        data = copy.deepcopy(self.selections)
        record = data["selections"][0]
        record["review_gates"] = {key: "complete" for key in record["review_gates"]}
        record["promotion_status"] = "ready-for-promotion"
        self.assertTrue(any("cannot certify promotion" in e for e in self.selection_errors(data)))

    def test_baseline_phrase_in_a_note_is_not_the_source_field(self):
        data = copy.deepcopy(self.selections)
        data["selections"][0]["baseline"]["declared_source_text"] = "בני אלוהים"
        self.assertTrue(any("declared source text" in e for e in self.selection_errors(data)))

    def test_reconstructed_selected_phrase_is_not_visible_support(self):
        comparison = copy.deepcopy(self.comparison)
        case = next(c for c in comparison["cases"] if c["id"] == "DEU.32.8.referent")
        reading = next(r for r in case["readings"] if r.get("witness_id") == "4q37")
        reading["text"] = "[בני אלוהים]"
        errors = MODULE.validate_selections(self.selections, comparison, self.adjudication)
        self.assertTrue(any("outside editorial reconstruction" in e for e in errors))

    def test_selection_cannot_promote_without_full_hebrew_source(self):
        data = copy.deepcopy(self.selections)
        record = data["selections"][0]
        record["review_gates"] = {key: "complete" for key in record["review_gates"]}
        record["promotion_status"] = "promoted"
        record["canonical_change_applied"] = True
        self.assertTrue(any("full-verse" in e for e in self.selection_errors(data)))

    def test_qdr_extraction_finds_references_at_word_level(self):
        corpus = [{
            "scroll": "4Q-test",
            "fragments": [{
                "id": "f1",
                "lines": [{
                    "n": "7",
                    "words": [
                        ["prior", "prior", "", "", "", "Ex 1:4"],
                        ["seventy", "seventy", "", "", "", "Ex 1:5"],
                        ["five", "five", "", "", "", "Ex 1:5"],
                    ],
                }],
            }],
        }]
        result = EXTRACT_MODULE.extract_passages(corpus, {"Ex 1:5", "Ex 12:40"})
        self.assertEqual(result["Ex 1:5"][0]["manuscript_id"], "4Q-test")
        self.assertEqual(result["Ex 1:5"][0]["lines"][0]["diplomatic_text"], "seventy five")
        self.assertEqual(result["Ex 12:40"], [])


if __name__ == "__main__":
    unittest.main()
