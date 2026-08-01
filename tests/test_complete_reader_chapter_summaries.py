from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def load_module():
    sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(
        "complete_reader_chapter_summaries",
        TOOLS / "complete_reader_chapter_summaries.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_indexed_requires_every_requested_identity_exactly_once() -> None:
    module = load_module()

    assert module._indexed([{"id": "a"}, {"id": "b"}], {"a", "b"}, "draft") == {
        "a": {"id": "a"},
        "b": {"id": "b"},
    }
    with pytest.raises(RuntimeError, match="identity mismatch"):
        module._indexed([{"id": "a"}], {"a", "b"}, "draft")
    with pytest.raises(RuntimeError, match="duplicated id"):
        module._indexed([{"id": "a"}, {"id": "a"}], {"a"}, "draft")


def test_failed_packet_is_split_without_losing_tasks(monkeypatch) -> None:
    module = load_module()
    tasks = [
        {"language": "ko", "target_key": f"KPOB|{chapter}", "source": {}}
        for chapter in range(1, 5)
    ]
    calls: list[list[str]] = []

    def fake_translate(batch, _draft, _review):
        calls.append([task["target_key"] for task in batch])
        if len(batch) > 1:
            raise RuntimeError("model omitted an id")
        return [{"output": "translated"}]

    monkeypatch.setattr(module, "translate_batch", fake_translate)
    monkeypatch.setattr(
        module.base,
        "build_localized_item",
        lambda task, result, draft, review: {"summary_key": task["target_key"]},
    )
    monkeypatch.setattr(module.base, "put_localized_item", lambda *_args: True)

    statuses = module.localize_batch(None, "cache", tasks, "sol", "terra")

    assert statuses == [("written", task["target_key"]) for task in tasks]
    assert calls[0] == [task["target_key"] for task in tasks]
    assert {call[0] for call in calls if len(call) == 1} == {
        task["target_key"] for task in tasks
    }
