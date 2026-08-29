#!/usr/bin/env python3
"""Coverage and caution checks for the catalog-backed book metadata."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EarlyChristianMetadataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(
            (ROOT / "sources/early_christian_texts/catalog.json").read_text()
        )
        cls.metadata = json.loads((ROOT / "book_metadata.json").read_text())["books"]
        cls.entries = [
            entry
            for group in (
                "nag_hammadi_order",
                "early_christian_apocrypha_order",
                "apostolic_fathers_completion_order",
            )
            for entry in cls.catalog[group]
        ]

    def test_all_catalog_titles_have_complete_english_and_spanish_metadata(self):
        for entry in self.entries:
            with self.subTest(title=entry["title"]):
                record = self.metadata[entry["title"]]
                for field in ("author", "audience", "date"):
                    self.assertGreaterEqual(len(record[field].strip()), 40)
                    self.assertGreaterEqual(
                        len(record["localized"]["es"][field].strip()), 40
                    )

    def test_expansion_contains_23_prior_titles_plus_four_church_orders(self):
        existing_bridges = {"gospel_of_philip", "gospel_of_mary"}
        expansion = [e for e in self.entries if e["id"] not in existing_bridges]
        self.assertEqual(len(expansion), 27)
        self.assertEqual(
            [e["id"] for e in expansion[-4:]],
            [
                "didascalia_apostolorum",
                "apostolic_tradition",
                "apostolic_church_order",
                "apostolic_constitutions",
            ],
        )

    def test_traditional_titles_do_not_create_false_authorship_claims(self):
        anonymous_titles = {
            "Gospel of Judas",
            "Protoevangelium of James",
            "Infancy Gospel of Thomas",
            "Gospel of Peter",
            "2 Clement",
            "Epistle of Barnabas",
            "Epistle to Diognetus",
        }
        for title in anonymous_titles:
            with self.subTest(title=title):
                self.assertTrue(self.metadata[title]["author"].startswith("Anonymous"))

    def test_dates_express_uncertainty_or_manuscript_transmission(self):
        for entry in self.entries:
            if entry["id"] in {"gospel_of_philip", "gospel_of_mary"}:
                continue
            with self.subTest(title=entry["title"]):
                date = self.metadata[entry["title"]]["date"].lower()
                self.assertTrue(
                    any(
                        token in date
                        for token in (
                            "usually",
                            "commonly",
                            "often",
                            "generally",
                            "dated",
                            "century",
                        )
                    ),
                    date,
                )


if __name__ == "__main__":
    unittest.main()
