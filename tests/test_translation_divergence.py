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
FETCH_SPEC = importlib.util.spec_from_file_location("fetch_api_bible_licensed_references", TOOLS / "fetch_api_bible_licensed_references.py")
assert FETCH_SPEC and FETCH_SPEC.loader
FETCH = importlib.util.module_from_spec(FETCH_SPEC)
sys.modules[FETCH_SPEC.name] = FETCH
FETCH_SPEC.loader.exec_module(FETCH)


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
        self.assertGreater(score, 0.45)

    def test_multitoken_superscription_marker_is_stripped(self):
        self.assertEqual(DIVERGENCE.normalize_tokens("[v1, includes superscription] Blessed is he"), ["blessed", "is", "he"])

    def test_tvtms_mapping_covers_known_offsets(self):
        expected = {("leviticus",6,2):(6,9),("exodus",22,9):(22,10),("genesis",32,1):(31,55),("joel",3,1):(2,28),("psalms",3,1):(3,1),("2_corinthians",13,13):(13,14),("philippians",1,16):(1,17)}
        for (book, chapter, verse), mapped in expected.items():
            with self.subTest(book=book): self.assertEqual(DIVERGENCE.refs.panel_reference(book,"bsb",chapter,verse), mapped)

    def test_api_bible_fetch_uses_standard_english_reference(self):
        self.assertEqual(FETCH.api_verse_id("leviticus", 6, 2), "LEV.6.9")
        self.assertEqual(FETCH.api_verse_id("joel", 3, 1), "JOE.2.28")

    def test_score_bands_are_stable(self):
        self.assertEqual(DIVERGENCE.score_band(24.99), "low")
        self.assertEqual(DIVERGENCE.score_band(40), "high")
        self.assertEqual(DIVERGENCE.score_band(55), "very_high")

    def test_reference_codes_match_ebible_vpl_codes(self):
        expected = {
            "song_of_songs": "SOL", "ezekiel": "EZE", "joel": "JOE",
            "nahum": "NAH", "mark": "MAR", "john": "JOH",
            "philippians": "PHI", "james": "JAM", "1_john": "1JO",
            "2_john": "2JO", "3_john": "3JO",
        }
        for book, code in expected.items():
            with self.subTest(book=book):
                self.assertEqual(DIVERGENCE.refs.BOOK_USFM_CODES[book], code)

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

    def test_short_fragment_is_excluded_from_public_ranking(self):
        alignment = DIVERGENCE.ranking_alignment(
            "known from of old",
            {
                "bsb": "that have been known for ages",
                "web": "All of God's works are known to him from eternity",
                "asv": "The Lord makes these things known from of old",
                "kjv": "Known unto God are all his works from the beginning of the world",
            },
        )
        self.assertFalse(alignment["ranking_eligible"])
        self.assertIn("pob_fragment_too_short", alignment["reasons"])

    def test_segmentation_merge_detects_aligned_plus_next_verse(self):
        panels = {
            name: {("LUK", 7, 18): "John's disciples told him all these things.", ("LUK", 7, 19): "John called two of his disciples."}
            for name in DIVERGENCE.CONSENSUS_PANELS
        }
        found = DIVERGENCE.surviving_segmentation_merge(
            "John's disciples told him all these things, and John called two of his disciples.", panels, "luke", 7, 18
        )
        self.assertEqual(found["direction"], "aligned+next")

    def test_targeted_metrics_compare_pob_to_niv_nkjv_and_spob_to_nlt(self):
        metrics = DIVERGENCE.licensed_target_metrics(
            {
                "niv": {"pob_similarity": 0.8, "spob_similarity": 0.7},
                "nkjv": {"pob_similarity": 0.6, "spob_similarity": 0.5},
                "nlt": {"pob_similarity": 0.5, "spob_similarity": 0.9},
            },
        )
        self.assertEqual(metrics["pob_niv_nkjv_similarity"], 0.7)
        self.assertEqual(metrics["pob_niv_nkjv_divergence"], 30.0)
        self.assertEqual(metrics["spob_nlt_similarity"], 0.9)
        self.assertEqual(metrics["spob_nlt_divergence"], 10.0)
        self.assertNotIn("targeted_review_priority", metrics)

    def test_public_headline_rewards_novelty_where_references_agree(self):
        refs = {"bsb":"The king entered the city","web":"The king entered the city","asv":"The king entered into the city","kjv":"The king entered into the city"}
        near = DIVERGENCE.public_headline_metrics("The king entered the city", refs)
        novel = DIVERGENCE.public_headline_metrics("A ruler secretly departed for the countryside", refs)
        self.assertGreater(novel["headline_divergence"], near["headline_divergence"])


if __name__ == "__main__":
    unittest.main()
