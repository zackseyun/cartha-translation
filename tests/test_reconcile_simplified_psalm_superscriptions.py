from __future__ import annotations

import importlib.util
import pathlib
import sys
import tempfile
import unittest

from ruamel.yaml import YAML


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location(
    "reconcile_simplified_psalm_superscriptions",
    ROOT / "tools" / "reconcile_simplified_psalm_superscriptions.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReconcileSimplifiedPsalmSuperscriptionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.width = 4096

    def write(self, path: pathlib.Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            self.yaml.dump(data, handle)

    def read(self, path: pathlib.Path) -> dict:
        return self.yaml.load(path.read_text(encoding="utf-8"))

    def test_preserves_slot_wording_instead_of_choosing_by_similarity(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            sp0 = root / "translation_simplified/ot/psalms/023/000.yaml"
            sp1 = root / "translation_simplified/ot/psalms/023/001.yaml"
            pob0 = root / "translation/ot/psalms/023/000.yaml"
            pob1 = root / "translation/ot/psalms/023/001.yaml"
            source = {"edition": "WLC", "text": "same combined source"}
            self.write(
                sp0,
                {
                    "id": "PSA.23.0",
                    "source": source,
                    "translation": {
                        "text": (
                            "A psalm of David[a]. Yahweh[b] is my shepherd; "
                            "I will not be in need."
                        ),
                        "footnotes": [
                            {"marker": "a", "text": "heading note"},
                            {"marker": "b", "text": "content note"},
                        ],
                    },
                },
            )
            self.write(
                sp1,
                {
                    "id": "PSA.23.1",
                    "source": source,
                    "translation": {
                        "text": (
                            "A psalm of David[a].\n\nYahweh[b] is my shepherd. "
                            "I will have everything I need."
                        ),
                        "footnotes": [
                            {"marker": "a", "text": "heading note"},
                            {"marker": "b", "text": "content note"},
                        ],
                    },
                },
            )
            self.write(
                pob0,
                {
                    "id": "PSA.23.0",
                    "source": source,
                    "translation": {"text": "A psalm of David[a]."},
                    "is_superscription": True,
                },
            )
            self.write(
                pob1,
                {
                    "id": "PSA.23.1",
                    "source": source,
                    "translation": {
                        "text": "Yahweh is my shepherd; I will not lack."
                    },
                },
            )

            MODULE.reconcile_pair(
                "023",
                sp0,
                sp1,
                pob0,
                pob1,
                canonical_commit="abc123",
                yaml=self.yaml,
                apply=True,
                repo_root=root,
            )
            zero = self.read(sp0)
            one = self.read(sp1)
            self.assertEqual(
                zero["translation"]["text"], "A psalm of David[a]."
            )
            self.assertEqual(
                one["translation"]["text"],
                "Yahweh[b] is my shepherd. I will have everything I need.",
            )
            self.assertTrue(zero["is_superscription"])
            self.assertEqual(
                [item["marker"] for item in zero["translation"]["footnotes"]],
                ["a"],
            )
            self.assertEqual(
                [item["marker"] for item in one["translation"]["footnotes"]],
                ["b"],
            )
            self.assertEqual(
                one["base_translation"]["text"],
                "Yahweh is my shepherd; I will not lack.",
            )

    def test_exact_prefix_handles_grammatically_ambiguous_psalm_87(self) -> None:
        heading, content = MODULE.split_existing_text(
            (
                "A psalm and a song of the sons of Korah.[a] "
                "His[b] foundation is in the holy mountains."
            ),
            "087",
            1,
        )
        self.assertEqual(
            heading, "A psalm and a song of the sons of Korah.[a]"
        )
        self.assertEqual(
            content, "His[b] foundation is in the holy mountains."
        )

    def test_removes_only_duplicated_terminal_punctuation(self) -> None:
        self.assertEqual(
            MODULE.clean_structural_punctuation(
                "A song of ascents. Of David.[a]."
            ),
            "A song of ascents. Of David.[a]",
        )
        self.assertEqual(
            MODULE.clean_structural_punctuation("A psalm of David.[a]"),
            "A psalm of David.[a]",
        )


if __name__ == "__main__":
    unittest.main()
