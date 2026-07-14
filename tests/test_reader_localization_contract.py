from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import sys
import threading
import time

import pytest
import yaml
from jsonschema import Draft202012Validator


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_catalog() -> dict:
    return json.loads(
        (ROOT / "localization_source" / "reader_catalog.v1.json").read_text(
            encoding="utf-8"
        )
    )


def reviewed_catalog(source: dict, module, code: str = "fr") -> dict:
    def localized(value: str) -> str:
        return f"[fr] {value}"

    strings = {
        group: {key: localized(value) for key, value in values.items()}
        for group, values in source["strings"].items()
    }
    books = {}
    for canonical_name, source_book in source["books"].items():
        book = {
            "display_name": localized(source_book["display_name"]),
            "author": localized(source_book["author"]),
            "audience": localized(source_book["audience"]),
            "date": localized(source_book["date"]),
        }
        if "summary" in source_book:
            book["summary"] = localized(source_book["summary"])
        book["chapters"] = {}
        for number, source_chapter in source_book["chapters"].items():
            chapter = {"title": localized(source_chapter["title"])}
            if "summary" in source_chapter:
                chapter["summary"] = localized(source_chapter["summary"])
            book["chapters"][number] = chapter
        books[canonical_name] = book

    chunks = module.localization_chunks(source, 100)
    reviews = [
        {
            "chunk_id": chunk["chunk_id"],
            "verdict": "approve",
            "review_summary": "Complete fixture review.",
            "issues": [],
            "draft_model_id": "gpt-5.6-sol",
            "draft_deployment": "gpt-5-6-sol-atlas",
            "draft_output_hash": "a" * 64,
            "review_model_id": "gpt-5.6-terra",
            "review_deployment": "gpt-5-6-terra-atlas",
            "review_output_hash": "b" * 64,
            "reviewed_at": "2026-07-14T00:00:00Z",
        }
        for chunk in chunks
    ]
    return {
        "contract_version": 1,
        "catalog_kind": "reviewed_locale",
        "catalog_id": "pob-reader-localization",
        "language": {
            "code": code,
            "name": "French",
            "native_name": "Français",
            "variant": "modern international French",
            "direction": "ltr",
        },
        "status": "reviewed",
        "counts": source["counts"],
        "source_catalog_sha256": module.source_catalog_hash(source),
        "strings": strings,
        "books": books,
        "review": {
            "verdict": "reviewed",
            "completed_at": "2026-07-14T00:00:00Z",
            "chunks": reviews,
        },
    }


def test_reader_localization_source_schema_and_counts() -> None:
    source = source_catalog()
    schema = json.loads(
        (ROOT / "schemas" / "reader_localization_catalog.v1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert list(Draft202012Validator(schema).iter_errors(source)) == []
    assert source["counts"] == {"books": 131, "chapter_titles": 2548}
    assert len(source["books"]) == 131
    assert sum(len(book["chapters"]) for book in source["books"].values()) == 2548
    assert set(source["strings"]) == {
        "reader_ui",
        "placeholders",
        "sections",
        "canon",
        "authority",
    }
    assert len(source["strings"]["reader_ui"]) == 132
    assert {
        "brandLead",
        "deleteAccountConfirm",
        "switchTheme",
        "spotlightNoResults",
        "introQuote",
        "authorLabel",
        "audienceLabel",
        "dateLabel",
        "bookSummaryLabel",
        "chapterSummaryLabel",
        "showChapterGrid",
        "showChapterSummaries",
        "openChapter",
        "openIncipit",
    } <= set(source["strings"]["reader_ui"])
    metadata = json.loads((ROOT / "book_metadata.json").read_text(encoding="utf-8"))[
        "books"
    ]
    assert list(source["books"]) == list(metadata)
    assert all(
        set((book[field] for field in ("display_name", "author", "audience", "date")))
        for book in source["books"].values()
    )


def test_localization_chunks_cover_every_contract_item_once() -> None:
    module = load_module(
        "reader_localization_chunks", "tools/multilingual_localization_pipeline.py"
    )
    source = source_catalog()
    chunks = module.localization_chunks(source, 100)
    string_chunks = [chunk for chunk in chunks if "strings" in chunk]
    book_chunks = [chunk for chunk in chunks if "strings" not in chunk]
    assert [chunk["chunk_id"] for chunk in string_chunks] == [
        "strings-001",
        "strings-002",
    ]
    assert [chunk["chunk_id"] for chunk in book_chunks] == [
        f"books-{number:03d}" for number in range(1, len(book_chunks) + 1)
    ]
    seen_strings = {
        group: {
            key: value
            for chunk in string_chunks
            for key, value in (chunk.get("strings") or {}).get(group, {}).items()
        }
        for group in source["strings"]
    }
    assert seen_strings == source["strings"]
    metadata_names = [
        name for chunk in chunks for name in (chunk.get("book_metadata") or {})
    ]
    assert metadata_names == list(source["books"])
    seen_chapters = []
    for chunk in chunks:
        unit_count = len(chunk.get("book_metadata") or {}) + sum(
            len(chapters) for chapters in (chunk.get("chapter_titles") or {}).values()
        ) + sum(len(values) for values in (chunk.get("strings") or {}).values())
        assert unit_count <= 100
        for book_name, chapters in (chunk.get("chapter_titles") or {}).items():
            seen_chapters.extend((book_name, chapter) for chapter in chapters)
    expected_chapters = [
        (book_name, chapter)
        for book_name, book in source["books"].items()
        for chapter in book["chapters"]
    ]
    assert seen_chapters == expected_chapters


def test_reviewed_catalog_schema_and_no_fallback_validation() -> None:
    module = load_module(
        "reader_localization_validation", "tools/multilingual_localization_pipeline.py"
    )
    source = source_catalog()
    catalog = reviewed_catalog(source, module)
    assert module.validate_locale_catalog(catalog, source, expected_locale="fr") == []

    missing_book = copy.deepcopy(catalog)
    del missing_book["books"]["Genesis"]
    assert "canonical book key set mismatch" in module.validate_locale_catalog(
        missing_book, source, expected_locale="fr"
    )

    missing_chapter = copy.deepcopy(catalog)
    del missing_chapter["books"]["John"]["chapters"]["1"]
    assert "chapter key set mismatch: John" in module.validate_locale_catalog(
        missing_chapter, source, expected_locale="fr"
    )

    broken_placeholder = copy.deepcopy(catalog)
    broken_placeholder["strings"]["placeholders"]["no_search_results"] = (
        "[fr] Aucun résultat."
    )
    assert "placeholder token mismatch: placeholders.no_search_results" in (
        module.validate_locale_catalog(broken_placeholder, source, expected_locale="fr")
    )

    incomplete_review = copy.deepcopy(catalog)
    incomplete_review["review"]["chunks"].pop()
    assert "review chunk manifest does not exactly cover the canonical source" in (
        module.validate_locale_catalog(incomplete_review, source, expected_locale="fr")
    )


def test_only_sol_and_terra_are_allowed_for_catalog_chunks() -> None:
    module = load_module(
        "reader_localization_models", "tools/multilingual_localization_pipeline.py"
    )
    config = module.load_contract_config()
    assert module.DRAFT_DEPLOYMENT == config["draft_deployment"] == "gpt-5-6-sol-atlas"
    assert module.REVIEW_DEPLOYMENT == config["review_deployment"] == (
        "gpt-5-6-terra-atlas"
    )
    source_text = (ROOT / "tools" / "multilingual_localization_pipeline.py").read_text(
        encoding="utf-8"
    ).lower()
    assert "gemini" not in source_text
    assert "vertex" not in source_text


def test_catalog_concurrency_parallelizes_chunks_for_one_language(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module(
        "reader_localization_chunk_concurrency",
        "tools/multilingual_localization_pipeline.py",
    )
    chunks = [{"chunk_id": f"books-{index:03d}"} for index in range(1, 5)]
    active = 0
    max_active = 0
    lock = threading.Lock()

    def fake_process(code, spec, chunk, **kwargs):
        nonlocal active, max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
        time.sleep(0.03)
        with lock:
            active -= 1
        return ({"chunk_id": chunk["chunk_id"], "status": "reviewed"}, {
            "prompt_tokens": 0,
            "completion_tokens": 0,
        }, False)

    monkeypatch.setattr(module, "load_contract_config", lambda: {
        "chunk_max_units": 100,
        "locale_catalog_pattern": "localization/{locale}/reader_catalog.v1.yaml",
        "chunk_pattern": "localization/{locale}/chunks/{chunk_id}.yaml",
    })
    monkeypatch.setattr(module, "load_source_catalog", lambda **kwargs: {})
    monkeypatch.setattr(module, "localization_chunks", lambda source, size: chunks)
    monkeypatch.setattr(module, "source_catalog_hash", lambda source: "a" * 64)
    monkeypatch.setattr(module, "language_selection", lambda values: [("pt", {})])
    monkeypatch.setattr(module, "configured_path", lambda *args, **kwargs: tmp_path / "catalog.yaml")
    monkeypatch.setattr(module, "azure_key", lambda: "test-key")
    monkeypatch.setattr(module, "process_chunk", fake_process)
    monkeypatch.setattr(module, "load_chunk_artifact", lambda *args, **kwargs: None)
    monkeypatch.setattr(sys, "argv", ["localizer", "--language", "pt", "--concurrency", "4"])

    assert module.main() == 0
    assert max_active == 4


def test_published_locale_without_reviewed_catalog_fails() -> None:
    builder = load_module(
        "reader_localization_builder_strict", "tools/build_multilingual_reader_assets.py"
    )
    config = builder.load_contract_config()
    config = copy.deepcopy(config)
    config["published_locales"] = ["fr"]
    spec = {
        "name": "French",
        "native_name": "Français",
        "variant": "modern international French",
    }
    with pytest.raises(builder.ReaderLocalizationError, match="English fallback is forbidden"):
        builder.load_reader_localization(
            "fr", spec, root=ROOT, contract_config=config, source=source_catalog()
        )


def test_requested_existing_revision_languages_are_included() -> None:
    builder = load_module(
        "reader_localization_builder_selection", "tools/build_multilingual_reader_assets.py"
    )
    config = builder.load_config()
    assert [code for code, _spec in builder.reader_asset_languages(config, ["es", "ko"])] == [
        "es",
        "ko",
    ]
    assert all(
        spec["status"] == "pilot"
        for _code, spec in builder.reader_asset_languages(config, [])
    )


def test_builder_emits_top_level_localization_and_projects_book_fields(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    localizer = load_module(
        "reader_localization_fixture", "tools/multilingual_localization_pipeline.py"
    )
    builder = load_module(
        "reader_localization_builder_projection", "tools/build_multilingual_reader_assets.py"
    )
    source = source_catalog()
    catalog = reviewed_catalog(source, localizer)
    catalog["books"]["Genesis"]["chapters"]["1"]["summary"] = (
        "[fr] Optional localized chapter summary."
    )
    verse_path = tmp_path / "translation_fr" / "ot" / "genesis" / "001" / "001.yaml"
    verse_path.parent.mkdir(parents=True)
    verse_path.write_text(
        yaml.safe_dump(
            {
                "reference": "Genesis 1:1",
                "language": {"code": "fr"},
                "translation": {"text": "Au commencement…", "footnotes": []},
                "review_pass": {"verdict": "approve"},
                "status": "reviewed",
            },
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(builder, "load_reader_localization", lambda *args, **kwargs: catalog)
    monkeypatch.setattr(builder, "validate_verse", lambda payload, code: [])
    spec = {
        "name": "French",
        "native_name": "Français",
        "variant": "modern international French",
    }
    payload = builder.compile_language(
        "fr",
        spec,
        root=tmp_path,
        contract_config=localizer.load_contract_config(),
        source=source,
    )
    assert payload["localization"] is catalog
    book = payload["books"][0]
    assert book["name"] == "Genesis"
    assert book["localized_name"] == catalog["books"]["Genesis"]["display_name"]
    assert book["metadata"] == {
        field: catalog["books"]["Genesis"][field]
        for field in ("author", "audience", "date")
    }
    assert book["summary"] == catalog["books"]["Genesis"]["summary"]
    assert book["chapters"][0]["title"] == catalog["books"]["Genesis"]["chapters"][
        "1"
    ]["title"]
    assert book["chapters"][0]["summary"] == "[fr] Optional localized chapter summary."


def test_builder_excludes_reviewed_but_parked_human_record(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    builder = load_module(
        "reader_localization_builder_human_parked",
        "tools/build_multilingual_reader_assets.py",
    )
    verse_path = tmp_path / "translation_fr" / "ot" / "genesis" / "001" / "001.yaml"
    verse_path.parent.mkdir(parents=True)
    verse_path.write_text(
        yaml.safe_dump(
            {
                "reference": "Genesis 1:1",
                "language": {"code": "fr"},
                "translation": {"text": "Au commencement…", "footnotes": []},
                "review_pass": {"verdict": "needs_human_review"},
                "status": "needs_human_review",
            },
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(builder, "validate_verse", lambda payload, code: [])
    spec = {
        "name": "French",
        "native_name": "Français",
        "variant": "modern international French",
    }
    payload = builder.compile_language(
        "fr",
        spec,
        root=tmp_path,
        contract_config=builder.load_contract_config(),
        source=source_catalog(),
    )
    assert payload["books"] == []
