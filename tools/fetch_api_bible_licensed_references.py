#!/usr/bin/env python3
"""Fetch privately licensed NKJV/NIV/NLT verses from API.Bible.

This tool deliberately writes only beneath a caller-selected private path. The
output is an input to build_translation_divergence.py and must remain gitignored.
Use it only when Cartha's API.Bible plan/license expressly covers the requested
commercial and AI-assisted evaluation use.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import tempfile
import urllib.error
import urllib.parse
import urllib.request

import build_translation_divergence as divergence


API_ROOT = "https://rest.api.bible/v1"


def load_config(path: pathlib.Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    translations = payload.get("translations") if isinstance(payload, dict) else None
    if not isinstance(translations, dict) or not translations:
        raise ValueError("config must contain a non-empty translations object")
    for name, entry in translations.items():
        if name.lower() not in divergence.LICENSED_TARGETS:
            raise ValueError(f"unsupported translation {name}; use NKJV, NIV, or NLT")
        if not isinstance(entry, dict) or not entry.get("bible_id") or not entry.get("license_reference"):
            raise ValueError(f"{name} requires bible_id and license_reference")
    return payload


def fetch_verse(api_key: str, bible_id: str, verse_id: str) -> str:
    query = urllib.parse.urlencode({
        "content-type": "text",
        "include-notes": "false",
        "include-titles": "false",
        "include-chapter-numbers": "false",
        "include-verse-numbers": "false",
    })
    url = f"{API_ROOT}/bibles/{urllib.parse.quote(bible_id)}/verses/{urllib.parse.quote(verse_id)}?{query}"
    request = urllib.request.Request(url, headers={"api-key": api_key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"API.Bible returned HTTP {exc.code} for {verse_id}") from exc
    content = str(((payload.get("data") or {}).get("content") or "")).strip()
    if not content:
        raise RuntimeError(f"API.Bible returned no content for {verse_id}")
    return content


def verse_ids(books: list[str]) -> list[str]:
    ids: list[str] = []
    for book in books:
        for path in divergence.verse_paths(book):
            import yaml
            record = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if record.get("id"):
                ids.append(str(record["id"]).upper())
    return ids


def atomic_write(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = pathlib.Path(handle.name)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--books", nargs="+", default=["genesis", "luke"])
    parser.add_argument("--api-key-env", default="API_BIBLE_KEY")
    parser.add_argument(
        "--acknowledge-license",
        action="store_true",
        help="confirm the configured licenses cover this commercial/AI-assisted comparison",
    )
    args = parser.parse_args()
    if not args.acknowledge_license:
        raise SystemExit("Refusing fetch without --acknowledge-license")
    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        raise SystemExit(f"Missing API key environment variable: {args.api_key_env}")
    config = load_config(args.config)
    ids = verse_ids(args.books)
    output = {"schema_version": 1, "translations": {}}
    for raw_name, entry in config["translations"].items():
        name = raw_name.lower()
        verses: dict[str, str] = {}
        for index, verse_id in enumerate(ids, start=1):
            verses[verse_id] = fetch_verse(api_key, str(entry["bible_id"]), verse_id)
            if index % 100 == 0:
                print(f"{name}: fetched {index}/{len(ids)} verses")
        output["translations"][name] = {
            "display_name": str(entry.get("display_name") or name.upper()),
            "provider": "API.Bible",
            "license_reference": str(entry["license_reference"]),
            "verses": verses,
        }
        print(f"{name}: fetched {len(verses)} verses")
    atomic_write(args.output, output)
    print(f"private licensed bundle -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
