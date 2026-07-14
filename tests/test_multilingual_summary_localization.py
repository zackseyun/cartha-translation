from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def load_module():
    sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(
        "multilingual_summary_localization",
        TOOLS / "multilingual_summary_localization.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_row(index: int, output: str = "English summary") -> dict[str, Any]:
    chapter = index + 1
    model = "gpt-5.4-2026-03-05"
    return {
        "summary_key": (
            f"POB|unspecified|chapter|JOHN.{chapter:03d}|simplify|"
            f"bible_shared_summary_v1|{model}"
        ),
        "translation": "POB",
        "translation_version": "unspecified",
        "scope": "chapter",
        "book": "JOHN",
        "chapter": chapter,
        "tool": "simplify",
        "output": output,
        "prompt_version": "bible_shared_summary_v1",
        "model_version": model,
        "source_hash": f"source-{index}",
        "verse_count": 10 + index,
        "generated_at": "2026-07-14T00:00:00Z",
        "updated_at": "2026-07-14T00:00:00Z",
    }


def task(module, source: dict[str, Any], code: str = "fr") -> dict[str, Any]:
    return module.task_for(
        source,
        code,
        {"name": "French", "native_name": "Français", "variant": "modern French"},
    )


def matching_target(module, pending: dict[str, Any]) -> dict[str, Any]:
    source = pending["source"]
    return {
        "summary_key": pending["target_key"],
        "translation": module.language_translation(pending["language"]),
        "language": pending["language"],
        "source_hash": source["source_hash"],
        "localized_from_summary_key": source["summary_key"],
        "localized_from_output_hash": pending["source_output_hash"],
        "localization_pipeline_version": module.PIPELINE_VERSION,
    }


class FakeDynamo:
    def __init__(self, module, source_pages=None, existing=None):
        self.module = module
        self.source_pages = list(source_pages or [])
        self.existing = dict(existing or {})
        self.scan_index = 0
        self.put_calls: list[dict[str, Any]] = []

    def scan(self, **kwargs):
        page = self.source_pages[self.scan_index]
        self.scan_index += 1
        response = {"Items": [self.module.serialize_item(item) for item in page]}
        if self.scan_index < len(self.source_pages):
            response["LastEvaluatedKey"] = {"summary_key": {"S": f"cursor-{self.scan_index}"}}
        return response

    def batch_get_item(self, RequestItems):
        table, request = next(iter(RequestItems.items()))
        keys = [item["summary_key"]["S"] for item in request["Keys"]]
        items = [self.module.serialize_item(self.existing[key]) for key in keys if key in self.existing]
        return {"Responses": {table: items}, "UnprocessedKeys": {}}

    def put_item(self, **kwargs):
        self.put_calls.append(kwargs)
        return {}


def test_identity_changes_only_to_language_scoped_pob_token() -> None:
    module = load_module()
    source = source_row(0)
    localized = module.localized_summary_key(source["summary_key"], "zh_hans")
    assert module.language_translation("zh_hans") == "POB-ZH"
    assert localized == source["summary_key"].replace("POB|", "POB-ZH|", 1)
    assert localized.split("|")[1:] == source["summary_key"].split("|")[1:]
    assert module.deserialize_item(module.serialize_item(source))["chapter"] == 1


def test_pending_collection_skips_matching_rows_and_scans_forward() -> None:
    module = load_module()
    sources = [source_row(index, f"English summary {index}") for index in range(3)]
    first_task = task(module, sources[0])
    fake = FakeDynamo(
        module,
        source_pages=[sources[:2], sources[2:]],
        existing={first_task["target_key"]: matching_target(module, first_task)},
    )
    pending, stats = module.collect_pending_tasks(
        fake,
        "BibleSummaryCache-alpha",
        [("fr", first_task["language_spec"])],
        limit=2,
    )
    assert [item["source"]["chapter"] for item in pending] == [2, 3]
    assert stats == {"english_rows_scanned": 3, "matching_rows_skipped": 1}
    assert fake.scan_index == 2


def test_existing_match_requires_exact_source_output_and_pipeline() -> None:
    module = load_module()
    pending = task(module, source_row(0))
    existing = matching_target(module, pending)
    assert module.existing_matches(existing, pending)
    existing["localized_from_output_hash"] = "stale"
    assert not module.existing_matches(existing, pending)
    existing = matching_target(module, pending)
    existing["localization_pipeline_version"] = "old"
    assert not module.existing_matches(existing, pending)


def test_sol_draft_is_independently_corrected_by_terra_and_written(monkeypatch) -> None:
    module = load_module()
    pending = task(module, source_row(0, "Jesus addresses the gathered disciples."))
    calls: list[dict[str, Any]] = []

    def fake_call_tool(**kwargs):
        calls.append(kwargs)
        if kwargs["name"] == "submit_summary_translation":
            return {"translation": "Brouillon français."}, {"prompt_tokens": 10}, "draft-call"
        return (
            {
                "verdict": "revise",
                "final_translation": "Jésus s’adresse aux disciples réunis.",
                "issues": ["Corrected register."],
                "review_summary": "Faithful after correction.",
                "safe_to_publish": True,
            },
            {"prompt_tokens": 12},
            "review-call",
        )

    monkeypatch.setattr(module, "call_tool", fake_call_tool)
    monkeypatch.setattr(module, "now", lambda: "2026-07-14T12:00:00Z")
    fake = FakeDynamo(module)
    status, key = module.localize_one(
        fake,
        "BibleSummaryCache-alpha",
        pending,
        "gpt-5-6-sol-atlas",
        "gpt-5-6-terra-atlas",
    )

    assert status == "written"
    assert key.startswith("POB-FR|")
    assert [call["deployment"] for call in calls] == [
        "gpt-5-6-sol-atlas",
        "gpt-5-6-terra-atlas",
    ]
    assert calls[0]["name"] == "submit_summary_translation"
    assert calls[1]["name"] == "submit_summary_translation_review"

    put = fake.put_calls[0]
    item = module.deserialize_item(put["Item"])
    source = pending["source"]
    assert item["output"] == "Jésus s’adresse aux disciples réunis."
    assert item["translation"] == "POB-FR"
    assert item["language"] == "fr"
    assert item["scope"] == source["scope"]
    assert item["book"] == source["book"]
    assert item["chapter"] == source["chapter"]
    assert item["tool"] == source["tool"]
    assert item["source_hash"] == source["source_hash"]
    assert item["verse_count"] == source["verse_count"]
    assert item["model_version"] == source["model_version"]
    assert item["localization_provider"] == "azure_openai"
    assert item["localization_draft_model"] == "gpt-5.6-sol"
    assert item["localization_review_model"] == "gpt-5.6-terra"
    assert "attribute_not_exists" in put["ConditionExpression"]
    assert put["ExpressionAttributeValues"][":source_hash"]["S"] == source["source_hash"]


def test_cli_supports_bounded_dry_run_controls() -> None:
    module = load_module()
    args = module.parser().parse_args(
        [
            "--language",
            "fr",
            "--limit",
            "7",
            "--concurrency",
            "3",
            "--dry-run",
        ]
    )
    assert args.language == ["fr"]
    assert args.limit == 7
    assert args.concurrency == 3
    assert args.dry_run is True
