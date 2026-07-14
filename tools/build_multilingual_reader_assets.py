#!/usr/bin/env python3
"""Compile reviewed multilingual POB verses and reader-localization assets.

Complete v1 catalogs are emitted as the top-level ``localization`` object and
are also projected into existing book/chapter records. Legacy calibration data
remains available for preview locales during migration. A published locale is
strict: a missing, incomplete, stale, or unreviewed catalog fails the build.
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

from multilingual_localization_pipeline import (
    load_contract_config,
    load_source_catalog,
    validate_locale_catalog,
)
from multilingual_pipeline import ROOT, load_config, validate as validate_verse


UI_CODE_OVERRIDES = {"zh_hans": "zh"}
REFERENCE_RE = re.compile(r"^(?P<book>.+?)\s+(?P<chapter>\d+):(?P<verse>\d+)$")


class ReaderLocalizationError(RuntimeError):
    """A locale cannot be emitted without violating its localization contract."""


def ui_code(code: str) -> str:
    return UI_CODE_OVERRIDES.get(code, code)


def slugify_book(value: str) -> str:
    value = value.lower().replace("&", " and ").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def localized_titles(code: str, *, root: pathlib.Path = ROOT) -> dict[str, str]:
    """Read the legacy three-book calibration map during the v1 migration."""
    path = root / "localization" / code / "calibration.yaml"
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {
        str(item.get("source_title")): str(item.get("title"))
        for item in payload.get("book_localizations") or []
        if isinstance(item, dict) and item.get("source_title") and item.get("title")
    }


def _legacy_localization(
    code: str,
    spec: dict[str, Any],
    *,
    root: pathlib.Path,
    contract_config: dict[str, Any],
) -> dict[str, Any]:
    pattern = (contract_config.get("compatibility") or {}).get(
        "calibration_pattern", "localization/{locale}/calibration.yaml"
    )
    path = root / pattern.format(locale=code)
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    payload = payload or {}
    books: dict[str, Any] = {}
    for item in payload.get("book_localizations") or []:
        if not isinstance(item, dict) or not item.get("source_title"):
            continue
        value: dict[str, Any] = {"display_name": str(item.get("title") or "").strip()}
        metadata = {
            key: str(item.get(key) or "").strip()
            for key in ("author", "audience", "date")
            if str(item.get(key) or "").strip()
        }
        if metadata:
            value.update(metadata)
        if str(item.get("summary") or "").strip():
            value["summary"] = str(item["summary"]).strip()
        books[str(item["source_title"])] = value
    return {
        "contract_version": 0,
        "catalog_kind": "legacy_calibration",
        "catalog_id": "pob-reader-localization",
        "language": {
            "code": code,
            "name": spec["name"],
            "native_name": spec["native_name"],
            "variant": spec["variant"],
            "direction": spec.get("direction", "ltr"),
        },
        "status": "legacy_calibration",
        "strings": {"reader_ui": payload.get("reader_ui") or {}},
        "books": books,
    }


def locale_is_published(
    code: str, spec: dict[str, Any], contract_config: dict[str, Any]
) -> bool:
    explicit_status = str(spec.get("reader_localization_status") or "").lower()
    return code in set(contract_config.get("published_locales") or []) or explicit_status in {
        "published",
        "strict",
    }


def load_reader_localization(
    code: str,
    spec: dict[str, Any],
    *,
    root: pathlib.Path = ROOT,
    contract_config: dict[str, Any] | None = None,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Load one reviewed catalog, or a clearly marked legacy preview adapter."""
    contract_config = contract_config or load_contract_config(root)
    published = locale_is_published(code, spec, contract_config)
    catalog_path = root / contract_config["locale_catalog_pattern"].format(locale=code)
    if catalog_path.exists():
        catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
        source = source or load_source_catalog(root, contract_config)
        errors = validate_locale_catalog(
            catalog, source, expected_locale=code, root=root
        )
        if errors:
            raise ReaderLocalizationError(
                f"locale {code} has an invalid reviewed reader catalog: " + "; ".join(errors)
            )
        return catalog
    if published:
        raise ReaderLocalizationError(
            f"published locale {code} requires a complete reviewed v1 reader catalog at "
            f"{catalog_path.relative_to(root)}; English fallback is forbidden"
        )
    compatibility = contract_config.get("compatibility") or {}
    if not compatibility.get("allow_legacy_calibration", False):
        raise ReaderLocalizationError(f"locale {code} has no reviewed reader catalog")
    return _legacy_localization(
        code, spec, root=root, contract_config=contract_config
    )


def _localized_book_projection(
    localization: dict[str, Any], canonical_name: str
) -> dict[str, Any] | None:
    book = (localization.get("books") or {}).get(canonical_name)
    if localization.get("status") == "reviewed" and not isinstance(book, dict):
        raise ReaderLocalizationError(
            f"reviewed locale catalog is missing canonical book {canonical_name}"
        )
    return book if isinstance(book, dict) else None


def compile_language(
    code: str,
    spec: dict[str, Any],
    *,
    root: pathlib.Path = ROOT,
    contract_config: dict[str, Any] | None = None,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    translation_root = root / f"translation_{code}"
    contract_config = contract_config or load_contract_config(root)
    localization = load_reader_localization(
        code,
        spec,
        root=root,
        contract_config=contract_config,
        source=source,
    )
    reviewed_localization = localization.get("status") == "reviewed"
    books: dict[str, dict[int, list[dict[str, Any]]]] = {}
    book_paths: dict[str, str] = {}
    bad: list[str] = []
    if translation_root.exists():
        for path in sorted(translation_root.rglob("*.yaml")):
            try:
                payload = yaml.safe_load(path.read_text(encoding="utf-8"))
                if not isinstance(payload, dict):
                    continue
                # Only Terra-approved or safely applied Terra revisions are
                # publishable. A review_pass can also exist on records that
                # were deliberately parked for human review; those must never
                # leak into reader assets merely because the review ran.
                if not payload.get("review_pass") or payload.get("status") != "reviewed":
                    continue
                errors = validate_verse(payload, code)
                if errors:
                    bad.append(f"{path.relative_to(root)}: {', '.join(errors)}")
                    continue
                match = REFERENCE_RE.match(str(payload.get("reference") or "").strip())
                if not match:
                    continue
                book = match.group("book")
                relative_parts = path.relative_to(translation_root).parts
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
                bad.append(f"{path.relative_to(root)}: {exc}")

    compiled_books = []
    testament_rank = {"ot": 0, "nt": 1, "deuterocanon": 2, "extra_canonical": 3}
    for canonical_name, chapters in sorted(
        books.items(),
        key=lambda item: (
            testament_rank.get(book_paths.get(item[0], "").split("/", 1)[0], 9),
            book_paths.get(item[0], item[0]),
        ),
    ):
        localized_book = _localized_book_projection(localization, canonical_name)
        if reviewed_localization:
            assert localized_book is not None
            localized_name = str(localized_book["display_name"])
        else:
            localized_name = str((localized_book or {}).get("display_name") or canonical_name)

        compiled_chapters = []
        for chapter_number, verses in sorted(chapters.items()):
            chapter_record: dict[str, Any] = {
                "chapter": chapter_number,
                "verses": sorted(verses, key=lambda verse: verse["verse"]),
            }
            localized_chapter = ((localized_book or {}).get("chapters") or {}).get(
                str(chapter_number)
            )
            if reviewed_localization:
                if not isinstance(localized_chapter, dict):
                    raise ReaderLocalizationError(
                        f"reviewed locale {code} is missing {canonical_name} chapter {chapter_number}"
                    )
                chapter_record["title"] = str(localized_chapter["title"])
                if localized_chapter.get("summary"):
                    chapter_record["summary"] = str(localized_chapter["summary"])
            elif isinstance(localized_chapter, dict):
                if localized_chapter.get("title"):
                    chapter_record["title"] = str(localized_chapter["title"])
                if localized_chapter.get("summary"):
                    chapter_record["summary"] = str(localized_chapter["summary"])
            compiled_chapters.append(chapter_record)

        compiled_book: dict[str, Any] = {
            "name": canonical_name,
            "localized_name": localized_name,
            "slug": slugify_book(canonical_name),
            "chapters": compiled_chapters,
        }
        if localized_book:
            metadata = {
                field: str(localized_book[field])
                for field in ("author", "audience", "date")
                if localized_book.get(field)
            }
            if reviewed_localization and set(metadata) != {"author", "audience", "date"}:
                raise ReaderLocalizationError(
                    f"reviewed locale {code} has incomplete metadata for {canonical_name}"
                )
            if metadata:
                compiled_book["metadata"] = metadata
            if localized_book.get("summary"):
                compiled_book["summary"] = str(localized_book["summary"])
        compiled_books.append(compiled_book)

    if bad and locale_is_published(code, spec, contract_config):
        preview = "; ".join(bad[:5])
        raise ReaderLocalizationError(
            f"published locale {code} has {len(bad)} invalid reviewed records: {preview}"
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
        "localization_contract_version": localization["contract_version"],
        "localization_status": localization["status"],
    }
    return {
        **meta,
        "meta": meta,
        "localization": localization,
        "books": compiled_books,
        "validation_warnings": bad,
    }


def git_sha(*, root: pathlib.Path = ROOT) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )


def reader_asset_languages(
    config: dict[str, Any], requested_values: list[str]
) -> list[tuple[str, dict[str, Any]]]:
    """Keep default bulk builds on pilots, but honor named existing revisions."""
    requested = set(requested_values)
    explicitly_named = bool(requested) and "all" not in requested
    eligible_statuses = {"pilot", "existing_revision"} if explicitly_named else {"pilot"}
    return [
        (code, spec)
        for code, spec in config["languages"].items()
        if spec.get("status") in eligible_statuses
        and (not explicitly_named or code in requested)
    ]


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
    contract_config = load_contract_config()
    source = load_source_catalog(config=contract_config)
    languages = reader_asset_languages(config, args.language)
    sha = git_sha()
    index = []
    for code, spec in languages:
        payload = compile_language(
            code,
            spec,
            contract_config=contract_config,
            source=source,
        )
        target_code = ui_code(code)
        asset_path = args.output_root / "multilingual" / f"{target_code}.json"
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode(
            "utf-8"
        )
        version = f"{sha[:12]}-{hashlib.sha256(serialized).hexdigest()[:12]}"
        books = len(payload["books"])
        chapters = sum(len(book["chapters"]) for book in payload["books"])
        verses = sum(
            len(chapter["verses"])
            for book in payload["books"]
            for chapter in book["chapters"]
        )
        localization = payload["localization"]
        manifest = {
            "version": version,
            "commit_sha": sha,
            "language": target_code,
            "books": books,
            "chapters": chapters,
            "verses": verses,
            "localization_contract_version": localization["contract_version"],
            "localization_status": localization["status"],
            "bible_url": f"/bibles/multilingual/{target_code}.json",
        }
        if localization.get("status") == "reviewed" and not args.full_only:
            manifest["localization_url"] = (
                f"/bibles/multilingual/{target_code}/localization.json"
            )
        write_json(asset_path, payload)
        language_root = args.output_root / "multilingual" / target_code
        shutil.rmtree(language_root, ignore_errors=True)
        if args.full_only:
            index.append(
                {**manifest, "name": spec["name"], "native_name": spec["native_name"]}
            )
            print(
                f"{target_code:8} books={books:3} chapters={chapters:4} "
                f"verses={verses:6} localization={localization['status']} -> {asset_path}"
            )
            continue
        write_json(
            language_root / "nav.json",
            {
                **payload["meta"],
                "localization": localization,
                "books": [
                    {
                        "name": book["name"],
                        "localized_name": book["localized_name"],
                        "slug": book["slug"],
                        **({"metadata": book["metadata"]} if "metadata" in book else {}),
                        **({"summary": book["summary"]} if "summary" in book else {}),
                        "chapterCount": max(
                            (chapter["chapter"] for chapter in book["chapters"]), default=0
                        ),
                    }
                    for book in payload["books"]
                ],
            },
        )
        for book in payload["books"]:
            write_json(language_root / "books" / f"{book['slug']}.json", book)
        if localization.get("status") == "reviewed":
            write_json(language_root / "localization.json", localization)
        write_json(language_root / "manifest.json", manifest)
        index.append(
            {**manifest, "name": spec["name"], "native_name": spec["native_name"]}
        )
        print(
            f"{target_code:8} books={books:3} chapters={chapters:4} "
            f"verses={verses:6} localization={localization['status']} -> {asset_path}"
        )

    write_json(
        args.output_root / "multilingual" / "index.json",
        {"commit_sha": sha, "languages": index},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
