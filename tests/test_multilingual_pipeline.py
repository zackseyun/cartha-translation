from __future__ import annotations

import importlib.util
import pathlib

import yaml


ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_language_program_is_deduplicated_and_complete() -> None:
    module = load_module("multilingual_pipeline", "tools/multilingual_pipeline.py")
    config = module.load_config()
    languages = config["languages"]
    assert len(languages) == 33
    assert sum(spec.get("status") == "pilot" for spec in languages.values()) == 30
    assert {"en", "es", "ko", "pt", "zh_hans", "ar", "my"} <= set(languages)


def test_multilingual_validator_requires_anchored_footnotes() -> None:
    module = load_module("multilingual_pipeline_validation", "tools/multilingual_pipeline.py")
    record = {
        "language": {"code": "fr"},
        "translation": {"text": "Texte", "footnotes": [{"marker": "a", "text": "Note"}]},
    }
    assert module.validate(record, "fr") == ["unanchored footnote [a]"]
    record["translation"]["text"] = "Texte[a]"
    assert module.validate(record, "fr") == []


def test_bounded_wave_command_is_available() -> None:
    module = load_module("multilingual_pipeline_wave", "tools/multilingual_pipeline.py")
    parsed = module.parser().parse_args(["wave", "--language", "pt", "--limit-records", "25"])
    assert parsed.limit_records == 25
    assert parsed.language == ["pt"]


def test_spanish_repair_extracts_publication_text_from_curly_quotes() -> None:
    module = load_module("repair_spanish_yaml", "tools/repair_spanish_yaml.py")
    raw = """translation:\n  language: es\n  text: ‘Jesús dijo: «Vengan».’\nreview_pass:\n  rationale: roto: sin comillas\n"""
    assert module.extract_translation_text(raw) == "Jesús dijo: «Vengan»."


def test_localization_calibration_covers_every_target_language() -> None:
    files = sorted((ROOT / "localization").glob("*/calibration.yaml"))
    assert len(files) == 32
    expected_passages = {
        "ot/genesis/001/001.yaml",
        "ot/ecclesiastes/001/002.yaml",
        "nt/john/001/001.yaml",
        "nt/romans/003/025.yaml",
        "nt/1_peter/001/013.yaml",
    }
    for path in files:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        books = payload["book_localizations"]
        assert {item["source_title"] for item in books} == {
            "Genesis",
            "John",
            "Gospel of Thomas",
        }
        assert all(item["title"] and item["summary"] for item in books)
        assert {
            item["source_path"] for item in payload["spob_critical_passages"]
        } == expected_passages
        assert payload["reader_ui"]["translation_in_progress"]
