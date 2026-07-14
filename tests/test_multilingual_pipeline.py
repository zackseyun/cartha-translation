from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys

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
    assert len(languages) == 34
    assert sum(spec.get("status") == "pilot" for spec in languages.values()) == 31
    assert {"en", "es", "ko", "pt", "zh_hans", "de", "ar", "my"} <= set(languages)
    assert module.rollout_order(config)[:20] == [
        "en", "es", "pt", "zh_hans", "fr", "ko", "de", "ru", "hi", "id",
        "sw", "tl", "ta", "te", "ml", "vi", "ja", "ar", "yo", "ig",
    ]
    assert set(module.rollout_order(config)) == set(languages)


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
    assert "--draft-deployment gpt-5-6-sol-atlas" in result.stdout
    assert "-dz-" not in result.stdout


def test_rollout_language_lock_prevents_same_language_overlap(tmp_path, monkeypatch) -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module("multilingual_rollout_lock", "tools/multilingual_rollout.py")
    monkeypatch.setattr(module, "LOCK_ROOT", tmp_path)
    with module.language_lock("fr"):
        try:
            with module.language_lock("fr"):
                raise AssertionError("second language lane unexpectedly acquired the lock")
        except module.LanguageBusy:
            pass


def test_parallel_rollout_has_safe_stage_concurrency_defaults() -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout", "tools/multilingual_parallel_rollout.py"
    )
    parsed = module.parser().parse_args([])
    assert parsed.draft_total_concurrency == 32
    assert parsed.review_total_concurrency == 64
    assert parsed.stage == "both"
    assert module.lane_concurrency(32, 4) == 8
    assert module.lane_concurrency(64, 4) == 16
    assert parsed.draft_deployment == "gpt-5-6-sol-atlas"
    assert "dz" not in parsed.draft_deployment


def test_parallel_rollout_pins_top_priority_and_rotates_lower_lanes(monkeypatch) -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout_priority", "tools/multilingual_parallel_rollout.py"
    )
    monkeypatch.setattr(
        module,
        "language_state",
        lambda code, source=None: {
            "pending_review": 0,
            "pending_draft": 0 if code in {"es", "pt"} else 1,
        },
    )
    codes = module.rollout_codes([], module.load_config())
    tasks, cursor = module.choose_tasks(
        codes, 4, stage="draft", cursor=0, source=set()
    )
    assert [task["code"] for task in tasks] == [
        "zh_hans", "fr", "ko", "de"
    ]
    tasks, _cursor = module.choose_tasks(
        codes, 4, stage="draft", cursor=cursor, source=set()
    )
    assert [task["code"] for task in tasks] == ["zh_hans", "ru", "hi", "id"]
    assert tasks[0]["primary"] is True

    assert module.lane_concurrencies(32, 4) == [16, 6, 5, 5]


def test_parallel_rollout_deduplicates_language_lanes() -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout_unique", "tools/multilingual_parallel_rollout.py"
    )
    assert module.rollout_codes(["fr", "fr", "de"], module.load_config()) == ["fr", "de"]


def test_parallel_rollout_global_coordinator_lock(tmp_path, monkeypatch) -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout_lock", "tools/multilingual_parallel_rollout.py"
    )
    monkeypatch.setattr(module, "COORDINATOR_LOCK", tmp_path / "coordinator.lock")
    with module.coordinator_lock():
        try:
            with module.coordinator_lock():
                raise AssertionError("second coordinator unexpectedly acquired the global lock")
        except module.CoordinatorBusy:
            pass


def test_parallel_rollout_repeats_separate_fair_epochs(monkeypatch) -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout_epochs", "tools/multilingual_parallel_rollout.py"
    )
    monkeypatch.setattr(module, "source_relatives", lambda: ["record.yaml"])
    monkeypatch.setattr(
        module,
        "language_state",
        lambda code, source=None: {"pending_draft": 1, "pending_review": 1},
    )
    observed = []

    def fake_run_epoch(tasks, **kwargs):
        observed.append(
            (
                kwargs["epoch"],
                kwargs["stage"],
                kwargs["total_concurrency"],
                [task["code"] for task in tasks],
            )
        )
        return [
            {
                "code": task["code"],
                "stage": kwargs["stage"],
                "status": "dry_run",
            }
            for task in tasks
        ]

    monkeypatch.setattr(module, "run_epoch", fake_run_epoch)
    args = module.parser().parse_args(
        ["--languages", "fr", "de", "--workers", "1", "--epochs", "2", "--dry-run"]
    )
    assert module.coordinate(args) == 0
    assert observed == [
        (1, "draft", 32, ["fr"]),
        (1, "review", 64, ["fr"]),
        (2, "draft", 32, ["fr"]),
        (2, "review", 64, ["fr"]),
    ]


def test_parallel_rollout_can_run_review_only(monkeypatch) -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout_review_only",
        "tools/multilingual_parallel_rollout.py",
    )
    monkeypatch.setattr(module, "source_relatives", lambda: ["record.yaml"])
    monkeypatch.setattr(
        module,
        "language_state",
        lambda code, source=None: {"pending_draft": 10, "pending_review": 1},
    )
    observed = []

    def fake_run_epoch(tasks, **kwargs):
        observed.append(kwargs["stage"])
        return [{"code": tasks[0]["code"], "status": "complete"}]

    monkeypatch.setattr(module, "run_epoch", fake_run_epoch)
    args = module.parser().parse_args(
        ["--languages", "fr", "--stage", "review", "--epochs", "1", "--dry-run"]
    )
    assert module.coordinate(args) == 0
    assert observed == ["review"]


def test_parallel_rollout_reviews_successful_drafts_after_partial_failure(monkeypatch) -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout_partial",
        "tools/multilingual_parallel_rollout.py",
    )
    monkeypatch.setattr(module, "source_relatives", lambda: ["record.yaml"])
    monkeypatch.setattr(
        module,
        "language_state",
        lambda code, source=None: {"pending_draft": 1, "pending_review": 1},
    )
    observed = []

    def fake_run_epoch(tasks, **kwargs):
        observed.append(kwargs["stage"])
        return [
            {
                "code": tasks[0]["code"],
                "status": "failed" if kwargs["stage"] == "draft" else "complete",
            }
        ]

    monkeypatch.setattr(module, "run_epoch", fake_run_epoch)
    args = module.parser().parse_args(
        ["--languages", "fr", "--epochs", "1", "--dry-run"]
    )
    assert module.coordinate(args) == 1
    assert observed == ["draft", "review"]


def test_parallel_rollout_forwards_explicit_deployment_pools(tmp_path) -> None:
    sys.path.insert(0, str(ROOT / "tools"))
    module = load_module(
        "multilingual_parallel_rollout_pools", "tools/multilingual_parallel_rollout.py"
    )
    result = module.run_task(
        {"code": "fr", "stage": "draft"},
        epoch=1,
        limit_records=10,
        concurrency=8,
        draft_deployment="sol-global,sol-backup",
        review_deployment="terra-global,terra-backup",
        log_dir=tmp_path,
        env={},
        dry_run=True,
    )
    command = result["command"]
    assert command[command.index("--draft-deployment") + 1] == "sol-global,sol-backup"
    assert command[command.index("--review-deployment") + 1] == "terra-global,terra-backup"


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


def test_multilingual_pipeline_defaults_to_global_deployments() -> None:
    module = load_module(
        "multilingual_pipeline_global_defaults", "tools/multilingual_pipeline.py"
    )
    pilot = module.parser().parse_args(["pilot", "--language", "fr"])
    wave = module.parser().parse_args(["wave", "--language", "fr"])
    assert pilot.draft_deployment == "gpt-5-6-sol-atlas"
    assert wave.draft_deployment == "gpt-5-6-sol-atlas"
    assert pilot.review_deployment == "gpt-5-6-terra-atlas"
    assert "dz" not in pilot.draft_deployment


def test_multilingual_pipeline_honors_retry_after_with_jitter(monkeypatch) -> None:
    module = load_module(
        "multilingual_pipeline_retry_after", "tools/multilingual_pipeline.py"
    )
    monkeypatch.setattr(module.random, "uniform", lambda _low, _high: 0.75)
    assert module.retry_after_seconds({"Retry-After": "45"}) == 45
    assert module.retry_after_seconds({"x-ms-retry-after-ms": "2500"}) == 2.5
    assert module.retry_delay_seconds(0, 429, {"Retry-After": "45"}) == 45.75


def test_multilingual_both_stage_runs_distinct_draft_then_review_epochs(monkeypatch) -> None:
    module = load_module(
        "multilingual_pipeline_separate_epochs", "tools/multilingual_pipeline.py"
    )
    monkeypatch.setattr(module, "azure_key", lambda: "test-key")
    observed = []

    def fake_draft(code, _spec, verse, deployment, _force):
        observed.append(("draft", code, verse, deployment))
        return "drafted", verse, {}

    def fake_review(code, _spec, verse, deployment, _force):
        observed.append(("review", code, verse, deployment))
        return "reviewed", verse, {}

    monkeypatch.setattr(module, "draft_one", fake_draft)
    monkeypatch.setattr(module, "review_one", fake_review)
    args = module.parser().parse_args(
        [
            "pilot",
            "--language",
            "fr",
            "--verse",
            "first.yaml",
            "--verse",
            "second.yaml",
            "--stage",
            "both",
            "--limit-verses",
            "2",
            "--concurrency",
            "2",
        ]
    )
    assert module.command_pilot(args) == 0
    assert [item[0] for item in observed] == ["draft", "draft", "review", "review"]


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
    assert len(files) == 33
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
    assert len(index["languages"]) == 31
    assert all(item["verses"] >= 3 for item in index["languages"])
    assert (tmp_path / "multilingual" / "de.json").exists()
    assert (tmp_path / "multilingual" / "zh.json").exists()
    assert not (tmp_path / "multilingual" / "zh_hans.json").exists()
