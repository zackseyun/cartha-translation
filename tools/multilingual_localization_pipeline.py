#!/usr/bin/env python3
"""Build complete, reviewed v1 reader-localization catalogs with Azure GPT-5.6.

Canonical English book names and chapter numbers are immutable identifiers.
Azure GPT-5.6 Sol drafts bounded catalog chunks; Azure GPT-5.6 Terra reviews
each complete chunk. A locale catalog is assembled only after every chunk has
passed validation and independent review.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import string
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from multilingual_pipeline import ROOT, azure_key, call_tool, load_config, now, write_atomic


CONTRACT_CONFIG_PATH = pathlib.Path("config/reader_localization.yaml")
DRAFT_DEPLOYMENT = "gpt-5-6-sol-atlas"
REVIEW_DEPLOYMENT = "gpt-5-6-terra-atlas"
DRAFT_MODEL_ID = "gpt-5.6-sol"
REVIEW_MODEL_ID = "gpt-5.6-terra"
CONTENT_KEYS = ("strings", "book_metadata", "chapter_titles")
STRING_GROUPS = ("reader_ui", "placeholders", "sections", "canon", "authority")


def load_contract_config(root: pathlib.Path = ROOT) -> dict[str, Any]:
    payload = yaml.safe_load((root / CONTRACT_CONFIG_PATH).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("contract_version") != 1:
        raise RuntimeError("reader localization config must use contract_version: 1")
    if payload.get("draft_deployment") != DRAFT_DEPLOYMENT:
        raise RuntimeError(f"reader localization drafts must use {DRAFT_DEPLOYMENT}")
    if payload.get("review_deployment") != REVIEW_DEPLOYMENT:
        raise RuntimeError(f"reader localization reviews must use {REVIEW_DEPLOYMENT}")
    return payload


def configured_path(root: pathlib.Path, pattern: str, **values: str) -> pathlib.Path:
    return root / pattern.format(**values)


def canonical_hash(payload: Any) -> str:
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def schema_errors(payload: dict[str, Any], *, root: pathlib.Path = ROOT) -> list[str]:
    config = load_contract_config(root)
    schema = json.loads((root / config["schema"]).read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: tuple(str(item) for item in error.absolute_path),
    )
    rendered: list[str] = []
    for error in errors:
        path = ".".join(str(item) for item in error.absolute_path) or "$"
        rendered.append(f"{path}: {error.message}")
    return rendered


def _format_tokens(value: str) -> set[str]:
    try:
        return {
            field_name
            for _literal, field_name, _format_spec, _conversion in string.Formatter().parse(value)
            if field_name
        }
    except ValueError:
        return {"<invalid-format-string>"}


def validate_source_catalog(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    books = payload.get("books") or {}
    counts = payload.get("counts") or {}
    if payload.get("catalog_kind") != "source":
        errors.append("catalog_kind must be source")
    if (payload.get("language") or {}).get("code") != "en":
        errors.append("source catalog language must be en")
    if len(books) != counts.get("books"):
        errors.append(f"book count mismatch: expected {counts.get('books')}, found {len(books)}")
    chapter_count = sum(len((book or {}).get("chapters") or {}) for book in books.values())
    if chapter_count != counts.get("chapter_titles"):
        errors.append(
            f"chapter title count mismatch: expected {counts.get('chapter_titles')}, found {chapter_count}"
        )
    for canonical_name, book in books.items():
        if (book or {}).get("display_name") != canonical_name:
            errors.append(f"source display_name must equal canonical key: {canonical_name}")
    return errors


def load_source_catalog(
    root: pathlib.Path = ROOT, config: dict[str, Any] | None = None
) -> dict[str, Any]:
    config = config or load_contract_config(root)
    payload = json.loads((root / config["source_catalog"]).read_text(encoding="utf-8"))
    errors = schema_errors(payload, root=root) + validate_source_catalog(payload)
    if errors:
        raise RuntimeError("invalid reader localization source catalog: " + "; ".join(errors))
    return payload


def source_catalog_hash(source: dict[str, Any]) -> str:
    return canonical_hash(source)


def source_chunk_hash(source_chunk: dict[str, Any]) -> str:
    """Hash only the bounded source chunk that a localized artifact covers.

    A global catalog hash still protects assembled reader assets, but it should
    not invalidate and retranslate all 29 reviewed chunks when one title in one
    chunk changes. New artifacts therefore carry both hashes.
    """
    return canonical_hash(source_chunk)


def validate_locale_catalog(
    payload: dict[str, Any],
    source: dict[str, Any],
    *,
    expected_locale: str | None = None,
    root: pathlib.Path = ROOT,
) -> list[str]:
    """Validate schema plus exact source-key coverage and placeholder contracts."""
    errors = schema_errors(payload, root=root)
    language = payload.get("language") or {}
    if expected_locale and language.get("code") != expected_locale:
        errors.append(
            f"locale mismatch: expected {expected_locale}, found {language.get('code')}"
        )
    expected_hash = source_catalog_hash(source)
    if payload.get("source_catalog_sha256") != expected_hash:
        errors.append("source_catalog_sha256 does not match the canonical v1 source")
    if payload.get("counts") != source.get("counts"):
        errors.append("catalog counts do not match the canonical v1 source")
    review_chunks = ((payload.get("review") or {}).get("chunks") or [])
    expected_chunk_ids = [
        chunk["chunk_id"]
        for chunk in localization_chunks(
            source, int(load_contract_config(root)["chunk_max_units"])
        )
    ]
    actual_chunk_ids = [
        str(chunk.get("chunk_id") or "")
        for chunk in review_chunks
        if isinstance(chunk, dict)
    ]
    if actual_chunk_ids != expected_chunk_ids:
        errors.append("review chunk manifest does not exactly cover the canonical source")

    source_strings = source.get("strings") or {}
    localized_strings = payload.get("strings") or {}
    if set(localized_strings) != set(source_strings):
        errors.append("localized string group set mismatch")
    for group_name, source_group in source_strings.items():
        localized_group = localized_strings.get(group_name) or {}
        if set(localized_group) != set(source_group):
            errors.append(f"localized string key set mismatch: {group_name}")
            continue
        for key, source_value in source_group.items():
            target_value = str(localized_group.get(key) or "")
            if str(source_value).strip() and not target_value.strip():
                errors.append(f"empty localized string: {group_name}.{key}")
            if _format_tokens(target_value) != _format_tokens(str(source_value)):
                errors.append(f"placeholder token mismatch: {group_name}.{key}")

    source_books = source.get("books") or {}
    localized_books = payload.get("books") or {}
    if set(localized_books) != set(source_books):
        errors.append("canonical book key set mismatch")
        return errors
    for canonical_name, source_book in source_books.items():
        target_book = localized_books.get(canonical_name) or {}
        for field in ("display_name", "author", "audience", "date"):
            if not str(target_book.get(field) or "").strip():
                errors.append(f"empty book localization: {canonical_name}.{field}")
        if ("summary" in source_book) != ("summary" in target_book):
            errors.append(f"book summary presence mismatch: {canonical_name}")
        elif "summary" in source_book and not str(target_book.get("summary") or "").strip():
            errors.append(f"empty book summary: {canonical_name}")
        source_chapters = source_book.get("chapters") or {}
        target_chapters = target_book.get("chapters") or {}
        if set(target_chapters) != set(source_chapters):
            errors.append(f"chapter key set mismatch: {canonical_name}")
            continue
        for chapter_number, source_chapter in source_chapters.items():
            target_chapter = target_chapters.get(chapter_number) or {}
            if not str(target_chapter.get("title") or "").strip():
                errors.append(f"empty chapter title: {canonical_name} {chapter_number}")
            if ("summary" in source_chapter) != ("summary" in target_chapter):
                errors.append(f"chapter summary presence mismatch: {canonical_name} {chapter_number}")
            elif "summary" in source_chapter and not str(target_chapter.get("summary") or "").strip():
                errors.append(f"empty chapter summary: {canonical_name} {chapter_number}")
    return errors


def localization_chunks(source: dict[str, Any], max_units: int) -> list[dict[str, Any]]:
    """Partition strings, metadata, and chapter titles without splitting an item."""
    if max_units < 2:
        raise ValueError("max_units must be at least 2")
    chunks: list[dict[str, Any]] = []
    string_packet: dict[str, dict[str, str]] = {}
    string_units = 0
    string_sequence = 1

    def flush_strings() -> None:
        nonlocal string_packet, string_units, string_sequence
        if not string_packet:
            return
        chunks.append(
            {"chunk_id": f"strings-{string_sequence:03d}", "strings": string_packet}
        )
        string_packet = {}
        string_units = 0
        string_sequence += 1

    for group, values in source["strings"].items():
        for key, value in values.items():
            if string_units >= max_units:
                flush_strings()
            string_packet.setdefault(group, {})[key] = value
            string_units += 1
    flush_strings()
    packet: dict[str, Any] = {"book_metadata": {}, "chapter_titles": {}}
    units = 0
    sequence = 1

    def flush() -> None:
        nonlocal packet, units, sequence
        if not packet["book_metadata"] and not packet["chapter_titles"]:
            return
        content = {key: value for key, value in packet.items() if value}
        chunks.append({"chunk_id": f"books-{sequence:03d}", **content})
        packet = {"book_metadata": {}, "chapter_titles": {}}
        units = 0
        sequence += 1

    for canonical_name, book in source["books"].items():
        if units >= max_units:
            flush()
        metadata = {key: book[key] for key in ("display_name", "author", "audience", "date")}
        if "summary" in book:
            metadata["summary"] = book["summary"]
        packet["book_metadata"][canonical_name] = metadata
        units += 1
        for chapter_number, chapter in book["chapters"].items():
            if units >= max_units:
                flush()
            packet["chapter_titles"].setdefault(canonical_name, {})[chapter_number] = chapter
            units += 1
    flush()
    return chunks


def _string_schema(value: dict[str, Any]) -> dict[str, Any]:
    properties = {key: {"type": "string"} for key in value}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(properties),
        "properties": properties,
    }


def _metadata_schema(value: dict[str, Any]) -> dict[str, Any]:
    properties = {key: {"type": "string"} for key in value}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(properties),
        "properties": properties,
    }


def _chapter_schema(value: dict[str, Any]) -> dict[str, Any]:
    return _metadata_schema(value)


def chunk_payload_schema(chunk: dict[str, Any], *, review: bool) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "chunk_id": {"type": "string", "enum": [chunk["chunk_id"]]},
    }
    if "strings" in chunk:
        properties["strings"] = {
            "type": "object",
            "additionalProperties": False,
            "required": list(chunk["strings"]),
            "properties": {
                group: _string_schema(values) for group, values in chunk["strings"].items()
            },
        }
    if "book_metadata" in chunk:
        properties["book_metadata"] = {
            "type": "object",
            "additionalProperties": False,
            "required": list(chunk["book_metadata"]),
            "properties": {
                name: _metadata_schema(values)
                for name, values in chunk["book_metadata"].items()
            },
        }
    if "chapter_titles" in chunk:
        properties["chapter_titles"] = {
            "type": "object",
            "additionalProperties": False,
            "required": list(chunk["chapter_titles"]),
            "properties": {
                name: {
                    "type": "object",
                    "additionalProperties": False,
                    "required": list(chapters),
                    "properties": {
                        number: _chapter_schema(chapter)
                        for number, chapter in chapters.items()
                    },
                }
                for name, chapters in chunk["chapter_titles"].items()
            },
        }
    if review:
        properties = {
            "verdict": {
                "type": "string",
                "enum": ["approve", "revise", "needs_human_review"],
            },
            "review_summary": {"type": "string"},
            "issues": {"type": "array", "items": {"type": "string"}},
            **properties,
        }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(properties),
        "properties": properties,
    }


def localization_tool(name: str, chunk: dict[str, Any], *, review: bool) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "strict": True,
            "description": "Submit one complete, keyed POB reader-localization catalog chunk.",
            "parameters": chunk_payload_schema(chunk, review=review),
        },
    }


def chunk_content(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: payload[key] for key in CONTENT_KEYS if key in payload}


def validate_chunk_payload(payload: dict[str, Any], source_chunk: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_keys = {key for key in CONTENT_KEYS if key in source_chunk}
    if payload.get("chunk_id") != source_chunk.get("chunk_id"):
        errors.append("chunk_id mismatch")
    if set(chunk_content(payload)) != expected_keys:
        errors.append("chunk content section mismatch")
        return errors

    if "strings" in source_chunk:
        source_strings = source_chunk["strings"]
        target_strings = payload.get("strings") or {}
        if set(target_strings) != set(source_strings):
            errors.append("string group set mismatch")
        for group, values in source_strings.items():
            target_values = target_strings.get(group) or {}
            if set(target_values) != set(values):
                errors.append(f"string key set mismatch: {group}")
                continue
            for key, source_value in values.items():
                target_value = str(target_values.get(key) or "")
                if str(source_value).strip() and not target_value.strip():
                    errors.append(f"empty localized string: {group}.{key}")
                if _format_tokens(target_value) != _format_tokens(str(source_value)):
                    errors.append(f"placeholder token mismatch: {group}.{key}")

    for section in ("book_metadata", "chapter_titles"):
        if section not in source_chunk:
            continue
        source_values = source_chunk[section]
        target_values = payload.get(section) or {}
        if set(target_values) != set(source_values):
            errors.append(f"{section} book key set mismatch")
            continue
        for book_name, source_value in source_values.items():
            target_value = target_values.get(book_name) or {}
            if set(target_value) != set(source_value):
                errors.append(f"{section} key set mismatch: {book_name}")
                continue
            if section == "book_metadata":
                for field in source_value:
                    if not str(target_value.get(field) or "").strip():
                        errors.append(f"empty book metadata: {book_name}.{field}")
            else:
                for chapter_number, source_chapter in source_value.items():
                    target_chapter = target_value.get(chapter_number) or {}
                    if set(target_chapter) != set(source_chapter):
                        errors.append(f"chapter field set mismatch: {book_name} {chapter_number}")
                    for field in source_chapter:
                        if not str(target_chapter.get(field) or "").strip():
                            errors.append(
                                f"empty chapter localization: {book_name} {chapter_number}.{field}"
                            )
    return errors


def chunk_artifact_path(
    code: str, chunk_id: str, *, root: pathlib.Path, config: dict[str, Any]
) -> pathlib.Path:
    return configured_path(root, config["chunk_pattern"], locale=code, chunk_id=chunk_id)


def load_chunk_artifact(
    path: pathlib.Path,
    source_chunk: dict[str, Any],
    *,
    code: str,
    expected_source_hash: str,
) -> dict[str, Any] | None:
    if not path.exists():
        return None
    artifact = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(artifact, dict):
        return None
    if artifact.get("contract_version") != 1 or artifact.get("locale") != code:
        return None
    expected_chunk_hash = source_chunk_hash(source_chunk)
    artifact_chunk_hash = artifact.get("source_chunk_sha256")
    if artifact_chunk_hash:
        if artifact_chunk_hash != expected_chunk_hash:
            return None
    elif artifact.get("source_catalog_sha256") != expected_source_hash:
        # Backward compatibility for v1 artifacts created before chunk hashes
        # were introduced. They remain reusable while the full source catalog
        # is unchanged and are upgraded the next time the chunk is regenerated.
        return None
    if artifact.get("chunk_id") != source_chunk["chunk_id"]:
        return None
    payload = {"chunk_id": artifact.get("chunk_id"), **(artifact.get("payload") or {})}
    if validate_chunk_payload(payload, source_chunk):
        return None
    draft = artifact.get("draft_provenance") or {}
    review = artifact.get("review") or {}
    if draft.get("model_id") != DRAFT_MODEL_ID or draft.get("azure_deployment") != DRAFT_DEPLOYMENT:
        return None
    if review.get("model_id") != REVIEW_MODEL_ID or review.get("azure_deployment") != REVIEW_DEPLOYMENT:
        return None
    return artifact


def process_chunk(
    code: str,
    spec: dict[str, Any],
    source_chunk: dict[str, Any],
    *,
    source_hash: str,
    root: pathlib.Path,
    config: dict[str, Any],
    force: bool,
) -> tuple[dict[str, Any], dict[str, int], bool]:
    path = chunk_artifact_path(code, source_chunk["chunk_id"], root=root, config=config)
    existing = load_chunk_artifact(
        path, source_chunk, code=code, expected_source_hash=source_hash
    )
    if existing and existing.get("status") == "reviewed" and not force:
        return existing, {"prompt_tokens": 0, "completion_tokens": 0}, True

    system = f"""You are Azure GPT-5.6 Sol, drafting one bounded People's Open Bible reader-localization catalog chunk into {spec['name']} ({spec['native_name']}).
Target variant: {spec['variant']}.
Translate every supplied value naturally and accurately for ordinary readers. Never translate, rename, add, or remove JSON object keys: canonical English book names, chapter-number keys, string IDs, and chunk_id are immutable identifiers. Preserve every {{placeholder}} token exactly. Author, audience, and date metadata must preserve uncertainty and must not amplify historical claims. Optional summaries appear only when supplied and must not be invented. Return every requested value exactly once. Never use denominational advocacy or named-interpreter doctrine."""
    draft, draft_usage, draft_hash = call_tool(
        deployment=DRAFT_DEPLOYMENT,
        system=system,
        user=json.dumps(source_chunk, ensure_ascii=False, indent=2),
        tool=localization_tool("submit_reader_localization_draft", source_chunk, review=False),
        name="submit_reader_localization_draft",
        max_tokens=24000,
    )
    errors = validate_chunk_payload(draft, source_chunk)
    if errors:
        raise RuntimeError(f"draft chunk {source_chunk['chunk_id']} failed validation: {errors}")

    review_system = f"""You are Azure GPT-5.6 Terra, the independent {spec['name']} reviewer for one bounded People's Open Bible reader-localization catalog chunk.
Check every localized value against the supplied canonical English source. Correct the draft directly and return the complete chunk even when approving. Keep all canonical English book-name keys, chapter-number keys, string IDs, chunk_id, and {{placeholder}} tokens unchanged. Reject missing fields, English fallback caused by omission, invented summaries, historical overstatement, and denominational advocacy. Use needs_human_review only when a faithful complete correction cannot be made."""
    review_input = {"source_chunk": source_chunk, "sol_draft": draft}
    reviewed, review_usage, review_hash = call_tool(
        deployment=REVIEW_DEPLOYMENT,
        system=review_system,
        user=json.dumps(review_input, ensure_ascii=False, indent=2),
        tool=localization_tool("submit_reader_localization_review", source_chunk, review=True),
        name="submit_reader_localization_review",
        max_tokens=26000,
    )
    errors = validate_chunk_payload(reviewed, source_chunk)
    if not str(reviewed.get("review_summary") or "").strip():
        errors.append("review_summary is empty")
    if errors:
        raise RuntimeError(f"review chunk {source_chunk['chunk_id']} failed validation: {errors}")
    verdict = reviewed["verdict"]
    status = "needs_human_review" if verdict == "needs_human_review" else "reviewed"
    artifact = {
        "contract_version": 1,
        "locale": code,
        "source_catalog_sha256": source_hash,
        "source_chunk_sha256": source_chunk_hash(source_chunk),
        "chunk_id": source_chunk["chunk_id"],
        "status": status,
        "payload": chunk_content(reviewed),
        "review": {
            "verdict": verdict,
            "review_summary": reviewed["review_summary"],
            "issues": reviewed["issues"],
            "model_id": REVIEW_MODEL_ID,
            "azure_deployment": REVIEW_DEPLOYMENT,
            "timestamp": now(),
            "output_hash": review_hash,
            "usage": review_usage,
        },
        "draft_provenance": {
            "model_id": DRAFT_MODEL_ID,
            "azure_deployment": DRAFT_DEPLOYMENT,
            "timestamp": now(),
            "output_hash": draft_hash,
            "usage": draft_usage,
        },
    }
    write_atomic(path, artifact)
    usage = {
        "prompt_tokens": int(draft_usage.get("prompt_tokens") or 0)
        + int(review_usage.get("prompt_tokens") or 0),
        "completion_tokens": int(draft_usage.get("completion_tokens") or 0)
        + int(review_usage.get("completion_tokens") or 0),
    }
    return artifact, usage, False


def assemble_locale_catalog(
    code: str,
    spec: dict[str, Any],
    source: dict[str, Any],
    chunks: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    *,
    root: pathlib.Path = ROOT,
) -> dict[str, Any]:
    by_id = {artifact["chunk_id"]: artifact for artifact in artifacts}
    expected_ids = [chunk["chunk_id"] for chunk in chunks]
    if set(by_id) != set(expected_ids):
        missing = sorted(set(expected_ids) - set(by_id))
        raise RuntimeError(f"locale {code} is missing reviewed chunks: {', '.join(missing)}")
    strings_payload: dict[str, dict[str, str]] = {}
    metadata: dict[str, Any] = {}
    chapter_titles: dict[str, dict[str, Any]] = {}
    review_chunks: list[dict[str, Any]] = []
    for chunk_id in expected_ids:
        artifact = by_id[chunk_id]
        if artifact.get("status") != "reviewed":
            raise RuntimeError(f"locale {code} chunk {chunk_id} is not reviewed")
        payload = artifact["payload"]
        if "strings" in payload:
            for group, values in payload["strings"].items():
                target = strings_payload.setdefault(group, {})
                overlap = set(target) & set(values)
                if overlap:
                    raise RuntimeError(
                        f"duplicate localized reader strings: {group} {sorted(overlap)}"
                    )
                target.update(values)
        for name, value in (payload.get("book_metadata") or {}).items():
            if name in metadata:
                raise RuntimeError(f"duplicate localized book metadata: {name}")
            metadata[name] = value
        for name, chapters in (payload.get("chapter_titles") or {}).items():
            target = chapter_titles.setdefault(name, {})
            overlap = set(target) & set(chapters)
            if overlap:
                raise RuntimeError(f"duplicate localized chapter titles: {name} {sorted(overlap)}")
            target.update(chapters)
        review = artifact["review"]
        draft = artifact["draft_provenance"]
        review_chunks.append(
            {
                "chunk_id": chunk_id,
                "verdict": review["verdict"],
                "review_summary": review["review_summary"],
                "issues": review["issues"],
                "draft_model_id": draft["model_id"],
                "draft_deployment": draft["azure_deployment"],
                "draft_output_hash": draft["output_hash"],
                "review_model_id": review["model_id"],
                "review_deployment": review["azure_deployment"],
                "review_output_hash": review["output_hash"],
                "reviewed_at": review["timestamp"],
            }
        )
    books: dict[str, Any] = {}
    for canonical_name in source["books"]:
        if canonical_name not in metadata:
            raise RuntimeError(f"missing localized book metadata: {canonical_name}")
        books[canonical_name] = {
            **metadata[canonical_name],
            "chapters": chapter_titles.get(canonical_name) or {},
        }
    direction = spec.get("direction", "ltr")
    catalog = {
        "contract_version": 1,
        "catalog_kind": "reviewed_locale",
        "catalog_id": source["catalog_id"],
        "language": {
            "code": code,
            "name": spec["name"],
            "native_name": spec["native_name"],
            "variant": spec["variant"],
            "direction": direction,
        },
        "status": "reviewed",
        "counts": source["counts"],
        "source_catalog_sha256": source_catalog_hash(source),
        "strings": strings_payload,
        "books": books,
        "review": {
            "verdict": "reviewed",
            "completed_at": now(),
            "chunks": review_chunks,
        },
    }
    errors = validate_locale_catalog(catalog, source, expected_locale=code, root=root)
    if errors:
        raise RuntimeError("assembled locale catalog failed validation: " + "; ".join(errors))
    return catalog


def language_selection(values: list[str]) -> list[tuple[str, dict[str, Any]]]:
    languages = load_config()["languages"]
    if not values or "all" in values:
        return [(code, spec) for code, spec in languages.items() if code != "en"]
    unknown = [code for code in values if code not in languages or code == "en"]
    if unknown:
        raise SystemExit(f"unknown/non-target languages: {', '.join(unknown)}")
    return [(code, languages[code]) for code in values]


def run_language(
    code: str,
    spec: dict[str, Any],
    force: bool,
    selected_chunk_ids: set[str] | None = None,
) -> tuple[str, dict[str, int]]:
    config = load_contract_config()
    source = load_source_catalog(config=config)
    source_hash = source_catalog_hash(source)
    chunks = localization_chunks(source, int(config["chunk_max_units"]))
    target = configured_path(ROOT, config["locale_catalog_pattern"], locale=code)
    if target.exists() and not force and not selected_chunk_ids:
        existing = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
        if not validate_locale_catalog(existing, source, expected_locale=code):
            return "skip", {"prompt_tokens": 0, "completion_tokens": 0}

    known_ids = {chunk["chunk_id"] for chunk in chunks}
    if selected_chunk_ids:
        unknown = sorted(selected_chunk_ids - known_ids)
        if unknown:
            raise RuntimeError(f"unknown chunk id(s): {', '.join(unknown)}")
        work_chunks = [chunk for chunk in chunks if chunk["chunk_id"] in selected_chunk_ids]
    else:
        work_chunks = chunks

    totals = {"prompt_tokens": 0, "completion_tokens": 0}
    needs_human = False
    for chunk in work_chunks:
        artifact, usage, was_cached = process_chunk(
            code,
            spec,
            chunk,
            source_hash=source_hash,
            root=ROOT,
            config=config,
            force=force,
        )
        totals["prompt_tokens"] += usage["prompt_tokens"]
        totals["completion_tokens"] += usage["completion_tokens"]
        needs_human = needs_human or artifact.get("status") == "needs_human_review"
        cache_label = "cached" if was_cached else artifact.get("status")
        print(f"{code:8} {chunk['chunk_id']:10} {cache_label}", flush=True)

    artifacts: list[dict[str, Any]] = []
    for chunk in chunks:
        artifact = load_chunk_artifact(
            chunk_artifact_path(code, chunk["chunk_id"], root=ROOT, config=config),
            chunk,
            code=code,
            expected_source_hash=source_hash,
        )
        if artifact is not None:
            artifacts.append(artifact)
    if len(artifacts) == len(chunks) and all(item.get("status") == "reviewed" for item in artifacts):
        catalog = assemble_locale_catalog(code, spec, source, chunks, artifacts)
        write_atomic(target, catalog)
        return "reviewed", totals
    if needs_human:
        return "needs_human_review", totals
    return "partial", totals


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--language", action="append", default=[])
    result.add_argument("--chunk-id", action="append", default=[])
    result.add_argument("--concurrency", type=int, default=2)
    result.add_argument("--force", action="store_true")
    result.add_argument(
        "--list-chunks",
        action="store_true",
        help="Print the bounded v1 chunk manifest without calling Azure",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    config = load_contract_config()
    source = load_source_catalog(config=config)
    chunks = localization_chunks(source, int(config["chunk_max_units"]))
    if args.list_chunks:
        print(
            json.dumps(
                {
                    "source_catalog_sha256": source_catalog_hash(source),
                    "chunks": [
                        {
                            "chunk_id": chunk["chunk_id"],
                            "book_metadata": len(chunk.get("book_metadata") or {}),
                            "chapter_titles": sum(
                                len(value) for value in (chunk.get("chapter_titles") or {}).values()
                            ),
                            "string_count": sum(
                                len(value) for value in (chunk.get("strings") or {}).values()
                            ),
                        }
                        for chunk in chunks
                    ],
                },
                indent=2,
            )
        )
        return 0

    selected = language_selection(args.language)
    selected_chunks = set(args.chunk_id) or None
    known_ids = {chunk["chunk_id"] for chunk in chunks}
    if selected_chunks:
        unknown = sorted(selected_chunks - known_ids)
        if unknown:
            raise SystemExit(f"unknown chunk id(s): {', '.join(unknown)}")
    totals = {
        "reviewed": 0,
        "partial": 0,
        "needs_human_review": 0,
        "skip": 0,
        "error": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
    }
    source_hash = source_catalog_hash(source)
    language_states: dict[str, dict[str, Any]] = {}
    tasks: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for code, spec in selected:
        target = configured_path(ROOT, config["locale_catalog_pattern"], locale=code)
        if target.exists() and not args.force and not selected_chunks:
            existing = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
            if not validate_locale_catalog(existing, source, expected_locale=code):
                language_states[code] = {
                    "spec": spec,
                    "target": target,
                    "status": "skip",
                    "needs_human": False,
                    "error": False,
                }
                continue
        work_chunks = [
            chunk
            for chunk in chunks
            if selected_chunks is None or chunk["chunk_id"] in selected_chunks
        ]
        language_states[code] = {
            "spec": spec,
            "target": target,
            "status": None,
            "needs_human": False,
            "error": False,
        }
        tasks.extend((code, spec, chunk) for chunk in work_chunks)

    # Resolve and cache the Azure key before worker threads start. More
    # importantly, concurrency now applies to independent catalog chunks, not
    # merely to the number of selected languages. A one-language rollout can
    # therefore use all requested workers instead of processing 29 chunks
    # serially.
    if tasks:
        azure_key()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max(1, args.concurrency)
    ) as pool:
        futures = {
            pool.submit(
                process_chunk,
                code,
                spec,
                chunk,
                source_hash=source_hash,
                root=ROOT,
                config=config,
                force=args.force,
            ): (code, chunk)
            for code, spec, chunk in tasks
        }
        for future in concurrent.futures.as_completed(futures):
            code, chunk = futures[future]
            try:
                artifact, usage, was_cached = future.result()
                totals["prompt_tokens"] += usage.get("prompt_tokens", 0)
                totals["completion_tokens"] += usage.get("completion_tokens", 0)
                state = language_states[code]
                state["needs_human"] = state["needs_human"] or (
                    artifact.get("status") == "needs_human_review"
                )
                cache_label = "cached" if was_cached else artifact.get("status")
                print(f"{code:8} {chunk['chunk_id']:10} {cache_label}", flush=True)
            except Exception as exc:  # noqa: BLE001
                language_states[code]["error"] = True
                print(f"ERROR              {code} {chunk['chunk_id']}: {exc}", flush=True)

    for code, _spec in selected:
        state = language_states[code]
        status = state["status"]
        if status == "skip":
            totals["skip"] += 1
            print(f"{'skip':18} {code}", flush=True)
            continue
        if state["error"]:
            totals["error"] += 1
            print(f"{'error':18} {code}", flush=True)
            continue
        artifacts: list[dict[str, Any]] = []
        for chunk in chunks:
            artifact = load_chunk_artifact(
                chunk_artifact_path(code, chunk["chunk_id"], root=ROOT, config=config),
                chunk,
                code=code,
                expected_source_hash=source_hash,
            )
            if artifact is not None:
                artifacts.append(artifact)
        if len(artifacts) == len(chunks) and all(
            item.get("status") == "reviewed" for item in artifacts
        ):
            catalog = assemble_locale_catalog(
                code, state["spec"], source, chunks, artifacts
            )
            write_atomic(state["target"], catalog)
            status = "reviewed"
        elif state["needs_human"]:
            status = "needs_human_review"
        else:
            status = "partial"
        totals[status] += 1
        print(f"{status:18} {code}", flush=True)
    print(json.dumps(totals, indent=2))
    return 1 if totals["error"] or totals["needs_human_review"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
