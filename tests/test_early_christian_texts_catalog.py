import pathlib
import unittest

from tools import build_status
from tools import export_extra_canonical_chapter_books as chapter_export
from tools import export_mobile_bible as mobile_export
from tools.extra_texts import draft_public_domain_witness as witness_bridge
from tools.extra_texts.catalog import (
    expected_units,
    flat_export_entries,
    load_entries,
    published_entries,
)
from tools.extra_texts.validate_catalog import validate_catalog


ROOT = pathlib.Path(__file__).resolve().parents[1]


class EarlyChristianTextsCatalogTests(unittest.TestCase):
    def test_catalog_contains_all_25_ordered_works_with_stable_codes(self):
        entries = load_entries()
        self.assertEqual(len(entries), 25)
        self.assertEqual(
            {entry["id"]: entry["code"] for entry in entries},
            {
                "gospel_of_philip": "GPHIL",
                "treatise_on_the_resurrection": "TRES",
                "dialogue_of_the_savior": "DSAV",
                "exegesis_on_the_soul": "EXSO",
                "book_of_thomas_the_contender": "BTHC",
                "tripartite_tractate": "TRIP",
                "apocryphon_of_john": "APOJ",
                "hypostasis_of_the_archons": "HARCH",
                "on_the_origin_of_the_world": "ORIGW",
                "sophia_of_jesus_christ": "SOJC",
                "gospel_of_the_egyptians": "GEGYP",
                "letter_of_peter_to_philip": "LPPH",
                "gospel_of_mary": "GMARY",
                "gospel_of_judas": "GJUD",
                "protoevangelium_of_james": "PROJ",
                "infancy_gospel_of_thomas": "IGTH",
                "acts_of_paul_and_thecla": "APTH",
                "gospel_of_peter": "GPET",
                "2_clement": "2CLEM",
                "epistle_of_barnabas": "BARN",
                "letters_of_ignatius": "IGN",
                "polycarp_to_the_philippians": "POLY",
                "martyrdom_of_polycarp": "MPOL",
                "epistle_to_diognetus": "DIOG",
                "fragments_of_papias": "PAPI",
            },
        )
        for entry in entries:
            self.assertIn("source", entry)
            self.assertTrue(entry["source"]["strategy"])
            self.assertTrue(entry["source"]["license"])

    def test_all_artifact_complete_entries_are_published(self):
        self.assertEqual(len(published_entries()), 25)
        self.assertEqual(len(flat_export_entries()), 25)
        self.assertTrue(all(expected_units(entry) > 0 for entry in flat_export_entries()))
        self.assertEqual(witness_bridge.TEXTS["gospel_of_judas"]["code"], "GJUD")
        self.assertEqual(witness_bridge.TEXTS["protoevangelium_of_james"]["unit"], "chapter")

    def test_shared_catalog_drives_all_three_export_registries(self):
        self.assertIn(("Didache", "DID", 16, 100, "didache"), build_status.EXTRA_CANONICAL_BOOKS)
        self.assertIn(("Gospel of Philip", "GPHIL", 18, 18, "gospel_of_philip"), build_status.EXTRA_CANONICAL_BOOKS)
        self.assertEqual(chapter_export.BOOKS["gospel_of_mary"]["id"], "GMARY")
        self.assertEqual(mobile_export.EXTRA_CANONICAL_BOOK_SLUGS["GPHIL"], "gospel_of_philip")
        self.assertIn("GPHIL", mobile_export.EXTRA_CANONICAL_CHAPTER_LEVEL)
        self.assertIn("DID", mobile_export.EXTRA_CANONICAL_BOOK_ORDER)

        rows = build_status.build_extra_canonical_books(
            build_status.EXTRA_CANONICAL_BOOKS
        )
        self.assertTrue(
            all(row["verses_drafted"] <= row["verses_total"] for row in rows)
        )

    def test_published_catalog_artifacts_pass_schema_and_cross_file_validation(self):
        self.assertEqual(validate_catalog(), [])

    def test_catalog_books_export_with_existing_reader_shape(self):
        payload = chapter_export.build_payload([entry["id"] for entry in published_entries()])
        self.assertEqual(len(payload["books"]), 25)
        self.assertTrue(all(book["chapters"] for book in payload["books"]))
        philip = mobile_export.export_extra_canonical_book("GPHIL")
        mary = mobile_export.export_extra_canonical_book("GMARY")
        self.assertEqual(philip["name"], "Gospel of Philip")
        self.assertEqual(len(philip["chapters"]), 18)
        self.assertEqual(mary["name"], "Gospel of Mary")
        self.assertEqual(len(mary["chapters"]), 5)

    def test_acts_of_paul_and_thecla_exports_real_verse_rows(self):
        book = mobile_export.export_extra_canonical_book("APTH")
        self.assertIsNotNone(book)
        chapter_one = next(
            chapter for chapter in book["chapters"] if chapter["chapter"] == 1
        )

        self.assertEqual(len(chapter_one["verses"]), 22)
        self.assertEqual(chapter_one["verses"][0]["verse"], 1)
        self.assertTrue(
            chapter_one["verses"][0]["text"].startswith("When Paul went up to Iconium")
        )
        self.assertFalse(chapter_one["verses"][0]["text"].startswith("1:1 "))
        self.assertFalse(chapter_one["verses"][1]["text"].startswith("1:2 "))


if __name__ == "__main__":
    unittest.main()
