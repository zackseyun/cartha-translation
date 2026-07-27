#!/usr/bin/env python3
"""Reconcile Simplified POB Psalm 0/1 records with canonical POB numbering.

The original Simplified POB pass was generated while 52 POB psalms still had
the Masoretic superscription and verse 1 fused in both ``000.yaml`` and
``001.yaml``.  That produced two competing simplified renderings of the same
source verse.  POB commit 38d5b36 fixed the canonical records: ``000.yaml`` is
now the heading and ``001.yaml`` is the first content verse.

This tool applies the same *structural* split to the derivative without making
an editorial choice between verse translations:

* keep the existing Simplified POB heading from ``000.yaml``;
* keep the existing Simplified POB content rendering from ``001.yaml``;
* refresh each record's ``base_translation`` from the corresponding canonical
  POB record; and
* record the repair so subsequent checks are idempotent.

No Scripture wording is synthesized and no similarity score chooses a winner.

Usage:
  python3 tools/reconcile_simplified_psalm_superscriptions.py --check
  python3 tools/reconcile_simplified_psalm_superscriptions.py --apply
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import pathlib
import re
import subprocess
import sys
from typing import Any

from ruamel.yaml import YAML

from psalm_numbering import split_fused


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
POB_PSALMS = REPO_ROOT / "translation" / "ot" / "psalms"
SIMPLIFIED_PSALMS = REPO_ROOT / "translation_simplified" / "ot" / "psalms"
REPAIR_METHOD = "canonical-slot-preservation-v1"

# A few one-line records are grammatically ambiguous to the generic Psalm
# superscription classifier.  These are exact, existing prefixes—not authored
# replacement wording.
EXACT_HEADER_PREFIXES: dict[tuple[str, int], str] = {
    ("087", 0): "A psalm of the sons of Korah; a song.[a]",
    ("087", 1): "A psalm and a song of the sons of Korah.[a]",
    ("120", 0): "A Song of Ascents.[a]",
    ("120", 1): "A Song of Ascents.[a]",
    ("121", 0): "A song for going up.[a]",
    ("134", 1): "A Song of Ascents.[a]",
}


def load_yaml(path: pathlib.Path, yaml: YAML) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def translation_text(record: dict[str, Any]) -> str:
    return str((record.get("translation") or {}).get("text") or "").strip()


def source_text(record: dict[str, Any]) -> str:
    return str((record.get("source") or {}).get("text") or "").strip()


def split_existing_text(text: str, psalm: str, slot: int) -> tuple[str, str]:
    """Return the existing (heading, content) without rewriting either."""
    text = text.strip()
    if "\n\n" in text:
        heading, content = text.split("\n\n", 1)
        return heading.strip(), content.strip()

    exact = EXACT_HEADER_PREFIXES.get((psalm, slot))
    if exact:
        if not text.startswith(exact):
            raise ValueError(
                f"Psalm {psalm} slot {slot}: expected prefix {exact!r}, "
                f"found {text[:100]!r}"
            )
        return exact, text[len(exact) :].strip()

    heading, content = split_fused(text)
    return heading.strip(), content.strip()


def clean_structural_punctuation(text: str) -> str:
    """Remove only a duplicated terminal mark around a footnote marker."""
    return re.sub(
        r"([.!?])(\[[a-z0-9]+\])[.!?]$",
        r"\1\2",
        text.strip(),
        flags=re.I,
    )


def referenced_markers(text: str) -> set[str]:
    return set(re.findall(r"\[([a-z0-9]+)\]", text, flags=re.I))


def filter_footnotes(record: dict[str, Any], new_text: str) -> None:
    translation = record.setdefault("translation", {})
    footnotes = translation.get("footnotes")
    if not isinstance(footnotes, list):
        return
    markers = referenced_markers(new_text)
    kept = [
        item
        for item in footnotes
        if isinstance(item, dict) and str(item.get("marker") or "") in markers
    ]
    if kept:
        translation["footnotes"] = kept
    else:
        translation.pop("footnotes", None)


def normalized_words(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def phrase_is_relevant(item: Any, new_text: str, new_base_text: str) -> bool:
    if not isinstance(item, dict):
        return False
    haystacks = (normalized_words(new_text), normalized_words(new_base_text))
    for key in ("simplified_phrase", "rendering", "pob_phrase", "term"):
        needle = normalized_words(item.get(key))
        if len(needle) >= 4 and any(needle in haystack for haystack in haystacks):
            return True
    return False


def filter_explanatory_metadata(
    record: dict[str, Any], new_text: str, new_base_text: str, *, slot: int
) -> None:
    for key in ("simplification_decisions", "interpretive_expansions", "retained_terms"):
        value = record.get(key)
        if not isinstance(value, list):
            continue
        kept = [
            item
            for item in value
            if phrase_is_relevant(item, new_text, new_base_text)
        ]
        if kept:
            record[key] = kept
        else:
            record.pop(key, None)

    # Verse-0 notes in the corrupt records commonly explain the removed verse-1
    # wording ("need", "justice", etc.). Replace those notes with the precise
    # mechanical repair statement. Verse 1 keeps its content-facing notes.
    if slot == 0:
        record["translation_notes"] = {
            "source_alignment_notes": (
                "Structural repair only: retained this record's existing "
                "simplified superscription and removed the duplicated verse 1 "
                "content after canonical POB numbering was corrected."
            )
        }


def refresh_base_translation(
    simplified: dict[str, Any],
    canonical: dict[str, Any],
    canonical_path: pathlib.Path,
    canonical_commit: str,
    repo_root: pathlib.Path,
) -> None:
    canonical_translation = canonical.get("translation") or {}
    relative_path = canonical_path.relative_to(repo_root).as_posix()
    base: dict[str, Any] = {
        "language": "en",
        "edition": "POB",
        "yaml_path": relative_path,
        "text": canonical_translation.get("text"),
        "footnotes": copy.deepcopy(canonical_translation.get("footnotes") or []),
    }
    for key in ("ai_draft", "revision_pass"):
        if canonical.get(key):
            base[key] = copy.deepcopy(canonical[key])
    simplified["base_translation"] = base

    grounding = simplified.setdefault("source_grounding", {})
    grounding["pob_path"] = relative_path
    grounding["pob_commit_sha"] = canonical_commit


def record_repair(
    record: dict[str, Any],
    *,
    old_text: str,
    kept_text: str,
    canonical_commit: str,
    slot: int,
) -> None:
    record["spob_structural_repair"] = {
        "method": REPAIR_METHOD,
        "canonical_pob_commit": canonical_commit,
        "slot": "superscription" if slot == 0 else "verse_1",
        "previous_text_sha256": hashlib.sha256(old_text.encode("utf-8")).hexdigest(),
        "wording_policy": (
            "preserved existing simplified slot wording; no similarity-based "
            "or model-authored replacement"
        ),
    }
    if slot == 0:
        record["is_superscription"] = True
    else:
        record.pop("is_superscription", None)
    record.setdefault("translation", {})["text"] = kept_text


def current_commit(repo_root: pathlib.Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True
    ).strip()


def candidate_pairs(
    simplified_root: pathlib.Path,
    pob_root: pathlib.Path,
    yaml: YAML,
) -> list[tuple[str, pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path]]:
    pairs = []
    for psalm_dir in sorted(simplified_root.iterdir()):
        if not psalm_dir.is_dir() or not psalm_dir.name.isdigit():
            continue
        sp0, sp1 = psalm_dir / "000.yaml", psalm_dir / "001.yaml"
        pob0 = pob_root / psalm_dir.name / "000.yaml"
        pob1 = pob_root / psalm_dir.name / "001.yaml"
        if not all(path.exists() for path in (sp0, sp1, pob0, pob1)):
            continue
        simplified_zero = load_yaml(sp0, yaml)
        simplified_one = load_yaml(sp1, yaml)
        if source_text(simplified_zero) != source_text(simplified_one):
            continue
        repaired_zero = simplified_zero.get("spob_structural_repair") or {}
        repaired_one = simplified_one.get("spob_structural_repair") or {}
        if (
            repaired_zero.get("method") == REPAIR_METHOD
            and repaired_one.get("method") == REPAIR_METHOD
        ):
            continue
        pairs.append((psalm_dir.name, sp0, sp1, pob0, pob1))
    return pairs


def reconcile_pair(
    psalm: str,
    sp0_path: pathlib.Path,
    sp1_path: pathlib.Path,
    pob0_path: pathlib.Path,
    pob1_path: pathlib.Path,
    *,
    canonical_commit: str,
    yaml: YAML,
    apply: bool,
    repo_root: pathlib.Path = REPO_ROOT,
) -> None:
    sp0 = load_yaml(sp0_path, yaml)
    sp1 = load_yaml(sp1_path, yaml)
    pob0 = load_yaml(pob0_path, yaml)
    pob1 = load_yaml(pob1_path, yaml)

    old_zero = translation_text(sp0)
    old_one = translation_text(sp1)
    heading_zero, _discarded_zero_content = split_existing_text(old_zero, psalm, 0)
    _discarded_one_heading, content_one = split_existing_text(old_one, psalm, 1)

    # Psalm 131's verse-0 record was already heading-only; its verse-1 record
    # still needed the split.
    if psalm == "131" and not heading_zero:
        heading_zero = old_zero
    heading_zero = clean_structural_punctuation(heading_zero)
    if not heading_zero:
        raise ValueError(f"Psalm {psalm}: could not isolate the existing heading")
    if not content_one:
        raise ValueError(f"Psalm {psalm}: could not isolate existing verse-1 content")

    if not apply:
        return

    canonical_zero_text = translation_text(pob0)
    canonical_one_text = translation_text(pob1)
    refresh_base_translation(sp0, pob0, pob0_path, canonical_commit, repo_root)
    refresh_base_translation(sp1, pob1, pob1_path, canonical_commit, repo_root)
    record_repair(
        sp0,
        old_text=old_zero,
        kept_text=heading_zero,
        canonical_commit=canonical_commit,
        slot=0,
    )
    record_repair(
        sp1,
        old_text=old_one,
        kept_text=content_one,
        canonical_commit=canonical_commit,
        slot=1,
    )
    filter_footnotes(sp0, heading_zero)
    filter_footnotes(sp1, content_one)
    filter_explanatory_metadata(
        sp0, heading_zero, canonical_zero_text, slot=0
    )
    filter_explanatory_metadata(
        sp1, content_one, canonical_one_text, slot=1
    )

    for path, record in ((sp0_path, sp0), (sp1_path, sp1)):
        with path.open("w", encoding="utf-8") as handle:
            yaml.dump(record, handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    commit = current_commit(REPO_ROOT)
    pairs = candidate_pairs(SIMPLIFIED_PSALMS, POB_PSALMS, yaml)

    for psalm, sp0, sp1, pob0, pob1 in pairs:
        reconcile_pair(
            psalm,
            sp0,
            sp1,
            pob0,
            pob1,
            canonical_commit=commit,
            yaml=yaml,
            apply=args.apply,
        )

    if args.check:
        if pairs:
            print(
                f"ERROR: {len(pairs)} Simplified POB psalms still duplicate "
                "the superscription and verse 1:"
            )
            print("  " + ", ".join(psalm for psalm, *_ in pairs))
            return 1
        print("Simplified POB Psalm superscription/verse-1 alignment: ok")
        return 0

    print(f"Reconciled {len(pairs)} Simplified POB psalms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
