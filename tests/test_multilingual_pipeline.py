from __future__ import annotations

import importlib.util
import pathlib


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
