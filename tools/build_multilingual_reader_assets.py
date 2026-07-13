#!/usr/bin/env python3
"""Compile every currently available multilingual POB record for readers.

The output is intentionally resumable and honest: a language can be opened as
soon as its first reviewed records exist, and the same stable URLs grow as the
Azure translation waves add more books.  No placeholder English verses are
inserted into a target-language corpus.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
from typing import Any

import yaml

from multilingual_pipeline import ROOT, load_config, validate


UI_CODE_OVERRIDES = {"zh_hans": "zh"}
REFERENCE_RE = re.compile(r"^(?P<book>.+?)\s+(?P<chapter>\d+):(?P<verse>\d+)$")


def ui_code(code: str) -> str:
    return UI_CODE_OVERRIDES.get(code, code)


def slugify_book(value: str) -> str:
    value = value.lower().replace("&", " and ").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def localized_titles(code: str) -> dict[str, str]:
    path = ROOT / "localization" / code / "calibration.yaml"
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {
        str(item.get("source_title")): str(item.get("title"))
        for item in payload.get("book_localizations") or []
        if isinstance(item, dict) and item.get("source_title") and item.get("title")
    }


def compile_language(code: str, spec: dict[str, Any]) -> dict[str, Any]:
    root = ROOT / f"translation_{code}"
    titles = localized_titles(code)
    books: dict[str, dict[int, list[dict[str, Any]]]] = {}
    book_paths: dict[str, str] = {}
    bad: list[str] = []
    if root.exists():
        for path in sorted(root.rglob("*.yaml")):
            try:
                payload = yaml.safe_load(path.read_text(encoding="utf-8"))
                if not isinstance(payload, dict):
                    continue
                if not payload.get("review_pass"):
                    continue
                errors = validate(payload, code)
                if errors:
                    bad.append(f"{path.relative_to(ROOT)}: {', '.join(errors)}")
                    continue
                match = REFERENCE_RE.match(str(payload.get("reference") or "").strip())
                if not match:
                    continue
                book = match.group("book")
                relative_parts = path.relative_to(root).parts
                book_paths.setdefault(book, "/".join(relative_parts[:-2]))
                chapter = int(match.group("chapter"))
                verse_number = int(match.group("verse"))
                translation = payload.get("translation") or {}
                verse: dict[str, Any] = {
                    "verse": verse_number,
                    "text": str(translation.get("text") or "").strip(),
                }
                footnotes = translation.get("footnotes") or []
                if footnotes:
                    verse["footnotes"] = footnotes
                books.setdefault(book, {}).setdefault(chapter, []).append(verse)
            except Exception as exc:  # noqa: BLE001
                bad.append(f"{path.relative_to(ROOT)}: {exc}")

    compiled_books = []
    testament_rank = {"ot": 0, "nt": 1, "deuterocanon": 2, "extra_canonical": 3}
    for book, chapters in sorted(
        books.items(),
        key=lambda item: (
            testament_rank.get(book_paths.get(item[0], "").split("/", 1)[0], 9),
            book_paths.get(item[0], item[0]),
        ),
    ):
        compiled_books.append(
            {
                "name": book,
                "localized_name": titles.get(book, book),
                "slug": slugify_book(book),
                "chapters": [
                    {
                        "chapter": chapter,
                        "verses": sorted(verses, key=lambda verse: verse["verse"]),
                    }
                    for chapter, verses in sorted(chapters.items())
                ],
            }
        )

    target_code = ui_code(code)
    full_name = f"{spec['name']} People's Open Bible (Preview)"
    meta = {
        "translation": f"POB: {full_name}",
        "translation_id": f"pob_{target_code}_preview",
        "short_name": "POB",
        "full_name": full_name,
        "language": target_code,
        "native_language": spec["native_name"],
        "variant": spec["variant"],
    }
    return {**meta, "meta": meta, "books": compiled_books, "validation_warnings": bad}


def git_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=pathlib.Path, required=True)
    parser.add_argument("--language", action="append", default=[])
    parser.add_argument(
        "--full-only",
        action="store_true",
        help="Write only the compact full preview assets (for bundled mobile seeds)",
    )
    args = parser.parse_args()

    config = load_config()
    requested = set(args.language or [])
    languages = [
        (code, spec)
        for code, spec in config["languages"].items()
        if spec.get("status") == "pilot" and (not requested or "all" in requested or code in requested)
    ]
    sha = git_sha()
    index = []
    for code, spec in languages:
        payload = compile_language(code, spec)
        target_code = ui_code(code)
        asset_path = args.output_root / "multilingual" / f"{target_code}.json"
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        version = f"{sha[:12]}-{hashlib.sha256(serialized).hexdigest()[:12]}"
        books = len(payload["books"])
        chapters = sum(len(book["chapters"]) for book in payload["books"])
        verses = sum(len(chapter["verses"]) for book in payload["books"] for chapter in book["chapters"])
        manifest = {
            "version": version,
            "commit_sha": sha,
            "language": target_code,
            "books": books,
            "chapters": chapters,
            "verses": verses,
            "bible_url": f"/bibles/multilingual/{target_code}.json",
        }
        write_json(asset_path, payload)
        language_root = args.output_root / "multilingual" / target_code
        shutil.rmtree(language_root, ignore_errors=True)
        if args.full_only:
            index.append({**manifest, "name": spec["name"], "native_name": spec["native_name"]})
            print(f"{target_code:8} books={books:3} chapters={chapters:4} verses={verses:6} -> {asset_path}")
            continue
        write_json(
            language_root / "nav.json",
            {
                **payload["meta"],
                "books": [
                    {
                        "name": book["name"],
                        "localized_name": book["localized_name"],
                        "slug": book["slug"],
                        "chapterCount": max(
                            (chapter["chapter"] for chapter in book["chapters"]),
                            default=0,
                        ),
                    }
                    for book in payload["books"]
                ],
            },
        )
        for book in payload["books"]:
            write_json(language_root / "books" / f"{book['slug']}.json", book)
        write_json(language_root / "manifest.json", manifest)
        index.append({**manifest, "name": spec["name"], "native_name": spec["native_name"]})
        print(f"{target_code:8} books={books:3} chapters={chapters:4} verses={verses:6} -> {asset_path}")

    write_json(args.output_root / "multilingual" / "index.json", {"commit_sha": sha, "languages": index})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
