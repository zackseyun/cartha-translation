from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess

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


def test_multilingual_payload_normalizes_bracketed_footnote_markers() -> None:
    module = load_module("multilingual_pipeline_footnotes", "tools/multilingual_pipeline.py")
    text, notes = module.normalize_translation_payload(
        "Texto[[a]]", [{"marker": "[a]", "text": "Nota", "reason": "Ambiguity"}]
    )
    assert text == "Texto[a]"
    assert notes[0]["marker"] == "a"
    record = {
        "language": {"code": "es"},
        "translation": {"text": text, "footnotes": notes},
    }
    assert module.validate(record, "es") == []


def test_multilingual_payload_discards_orphaned_model_footnotes() -> None:
    module = load_module("multilingual_pipeline_orphaned_footnotes", "tools/multilingual_pipeline.py")
    text, notes = module.normalize_translation_payload(
        "Texto[a]", [
            {"marker": "a", "text": "Anchored", "reason": "Ambiguity"},
            {"marker": "b", "text": "Orphaned", "reason": "Unused"},
        ]
    )
    assert text == "Texto[a]"
    assert [note["marker"] for note in notes] == ["a"]


def test_bounded_wave_command_is_available() -> None:
    module = load_module("multilingual_pipeline_wave", "tools/multilingual_pipeline.py")
    parsed = module.parser().parse_args(
        ["wave", "--language", "pt", "--limit-records", "25", "--pending-only"]
    )
    assert parsed.limit_records == 25
    assert parsed.language == ["pt"]
    assert parsed.pending_only is True


def test_rollout_can_direct_a_known_language_without_priority_rescan() -> None:
    result = subprocess.run(
        [
            "python3",
            "tools/multilingual_rollout.py",
            "--language",
            "ko",
            "--stage",
            "review",
            "--limit-records",
            "500",
            "--concurrency",
            "192",
            "--dry-run",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert '"selected_language": "ko"' in result.stdout
    assert '"directed": true' in result.stdout
    assert "--stage review" in result.stdout


def test_azure_key_is_cached_before_parallel_workers(monkeypatch) -> None:
    module = load_module("multilingual_pipeline_key_cache", "tools/multilingual_pipeline.py")
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)
    calls = 0

    def fake_check_output(*args, **kwargs):
        nonlocal calls
        calls += 1
        return '{"key1": "test-key"}'

    monkeypatch.setattr(module.subprocess, "check_output", fake_check_output)
    assert module.azure_key() == "test-key"
    assert module.azure_key() == "test-key"
    assert calls == 1


def test_weighted_azure_deployment_pool_is_deterministic() -> None:
    module = load_module("multilingual_pipeline_deployment_pool", "tools/multilingual_pipeline.py")
    value = "global*3,data-zone"
    assert module.deployment_pool(value) == ("global", "global", "global", "data-zone")
    assert module.choose_deployment(value, "pt:ot/genesis/001/001.yaml") == module.choose_deployment(
        value, "pt:ot/genesis/001/001.yaml"
    )
    observed = {
        module.choose_deployment(value, f"pt:ot/genesis/001/{verse:03}.yaml")
        for verse in range(1, 100)
    }
    assert observed == {"global", "data-zone"}


def test_multilingual_wave_uses_the_spob_publication_record_set() -> None:
    module = load_module("multilingual_pipeline_sources", "tools/multilingual_pipeline.py")
    relatives = module.source_relatives()
    assert len(relatives) == 43105
    assert len(relatives) == len(set(relatives))
    assert "extra_canonical/1_clement/001.yaml" not in relatives
    assert "extra_canonical/1_clement/001/001.yaml" in relatives
    assert "extra_canonical/testaments_twelve_patriarchs/asher/001.yaml" in relatives


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


def test_reader_asset_compiler_opens_every_pilot_language(tmp_path: pathlib.Path) -> None:
    subprocess.run(
        [
            "python3",
            "tools/build_multilingual_reader_assets.py",
            "--output-root",
            str(tmp_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    index = json.loads((tmp_path / "multilingual" / "index.json").read_text())
    assert len(index["languages"]) == 30
    assert all(item["verses"] >= 3 for item in index["languages"])
    assert (tmp_path / "multilingual" / "zh.json").exists()
    assert not (tmp_path / "multilingual" / "zh_hans.json").exists()
