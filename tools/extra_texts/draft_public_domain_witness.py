#!/usr/bin/env python3
"""Draft provisional POB extra-canonical texts from explicit-PD witnesses.

This bridge exists for works whose source-language critical editions are not
yet openly licensed.  It never presents the result as a direct Coptic/Greek
translation: every YAML records the public-domain English witness and keeps a
source-language review gate open.

Supported sources are selected from ``sources/early_christian_texts/catalog.json``.
This bridge currently accepts catalog entries using the
``gospels_net_centered_paragraphs`` parser strategy.

Azure GPT-5.6 Sol produces the provisional rendering.  GPT-5.6 Terra may be
used as a grounding reviewer with ``--review``.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import html
import json
import os
import pathlib
import re
import time
import urllib.request
from typing import Any

import yaml

try:
    from tools.extra_texts.catalog import load_entries
except ModuleNotFoundError:  # Executed as a file from this directory.
    from catalog import load_entries


ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "sources" / "early_christian_texts"
TRANSLATION_ROOT = ROOT / "translation" / "extra_canonical"
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
SOL_DEPLOYMENT = os.environ.get("AZURE_OPENAI_SOL_DEPLOYMENT_ID", "gpt-5-6-sol-atlas")
TERRA_DEPLOYMENT = os.environ.get("AZURE_OPENAI_TERRA_DEPLOYMENT_ID", "gpt-5-6-terra-atlas")


def bridge_texts() -> dict[str, dict[str, Any]]:
    texts: dict[str, dict[str, Any]] = {}
    for entry in load_entries():
        source = entry["source"]
        if source.get("strategy") != "gospels_net_centered_paragraphs":
            continue
        required = ("url", "witness_author", "start_heading")
        if any(not source.get(field) for field in required):
            continue
        texts[entry["id"]] = {
            "title": entry["title"],
            "code": entry["code"],
            "url": source["url"],
            "collection": entry["category"],
            "manuscript": source["manuscript"],
            "source_language": source["source_language"],
            "witness_author": source["witness_author"],
            "witness_license": source["license"],
            "start_heading": source["start_heading"],
            "unit": entry["unit"],
        }
    return texts


TEXTS = bridge_texts()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Cartha-POB-Extra-Texts/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", "ignore")


def clean_html(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    fragment = html.unescape(fragment).replace("\xa0", " ")
    fragment = re.sub(r"[ \t\r\f\v]+", " ", fragment)
    fragment = re.sub(r" *\n *", "\n", fragment)
    return fragment.strip()


def parse_sections(raw: str, start_heading: str) -> list[dict[str, Any]]:
    items: list[tuple[str, str]] = []
    for match in re.finditer(r"<p\b([^>]*)>(.*?)</p>", raw, re.I | re.S):
        attrs, body = match.groups()
        # Gospels.net embeds manuscript page folio markers as numeric-only
        # ``<strong>`` spans inside prose. They belong in provenance, not in
        # the reader sentence (otherwise readers see "Christ came 53 to...").
        body = re.sub(
            r"<strong\b[^>]*>\s*\d{1,3}\s*</strong>(?:\s|&nbsp;)*",
            "",
            body,
            flags=re.I,
        )
        text = clean_html(body)
        if not text:
            continue
        centered = "text-align:center" in attrs.replace(" ", "").lower()
        kind = "heading" if centered and "<strong" in body.lower() else "paragraph"
        items.append((kind, text))

    started = False
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for kind, text in items:
        if kind == "heading":
            if text == start_heading:
                started = True
            if not started:
                continue
            if text.lower().startswith("notes on translation"):
                break
            current = {"heading": text, "paragraphs": []}
            sections.append(current)
            continue
        if started and current is not None:
            current["paragraphs"].append(text)

    return [section for section in sections if section["paragraphs"]]


def azure_call(deployment: str, messages: list[dict[str, str]], max_tokens: int = 9000) -> dict[str, Any]:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_OPENAI_API_KEY"]
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={API_VERSION}"
    payload = {
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "api-key": key},
    )
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                result = json.load(response)
            content = result["choices"][0]["message"]["content"]
            return {"payload": json.loads(content), "model": result.get("model", deployment)}
        except Exception as exc:  # network/rate-limit/json retry boundary
            last_error = exc
            time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"Azure request failed after retries: {last_error}")


def draft_prompt(config: dict[str, Any], section: dict[str, Any]) -> list[dict[str, str]]:
    witness = "\n\n".join(section["paragraphs"])
    system = """You are drafting a provisional People's Open Bible rendering of an early Christian text.
The supplied English witness is explicitly public domain and itself translates an ancient source-language manuscript.
This is an interim bridge, not a substitute for future direct source-language review.

Rules:
- Preserve every claim, image, argument, quotation, ambiguity, and paragraph in order.
- Preserve square brackets and ellipses as manuscript-damage/restoration signals.
- Do not harmonize with the canonical Bible or normalize disputed theology.
- Use clear modern English without adding interpretation to the main text.
- Do not summarize, omit, preach, defend, or refute the text.
- Remove bare manuscript page numbers only when they interrupt a sentence.
- Return JSON with exactly: text (string, paragraphs separated by two newlines), notes (array of short strings).
"""
    user = f"""Work: {config['title']}
Editorial section: {section['heading']}
Manuscript: {config['manuscript']}

PUBLIC-DOMAIN ENGLISH WITNESS:
{witness}

Produce the provisional POB rendering now."""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def review_prompt(config: dict[str, Any], section: dict[str, Any], draft: str) -> list[dict[str, str]]:
    witness = "\n\n".join(section["paragraphs"])
    system = """You are the independent grounding reviewer for a provisional early-Christian-text rendering.
Compare the draft only against the supplied public-domain witness. Do not import a preferred theology.
Return JSON with: verdict ('accept' or 'revise'), issues (array), revised_text (string; empty when accepted).
Require all lacunae/restoration signals and all substantive claims to remain visible."""
    user = f"""Work: {config['title']}
Section: {section['heading']}

WITNESS:
{witness}

DRAFT:
{draft}"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def write_manifest(text_id: str, config: dict[str, Any], sections: list[dict[str, Any]], raw_path: pathlib.Path) -> None:
    target = SOURCE_ROOT / text_id
    target.mkdir(parents=True, exist_ok=True)
    manifest = {
        "text_id": text_id,
        "title": config["title"],
        "collection": config["collection"],
        "manuscript": config["manuscript"],
        "source_language": config["source_language"],
        "current_drafting_basis": {
            "kind": "public_domain_english_translation_witness",
            "url": config["url"],
            "translator": config["witness_author"],
            "license": config["witness_license"],
            "raw_snapshot": str(raw_path.relative_to(ROOT)),
        },
        "direct_source_language_review": "required_before_final",
        "unit": config["unit"],
        "expected_units": len(sections),
        "generated_at": now(),
    }
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (target / "sections.json").write_text(json.dumps(sections, indent=2, ensure_ascii=False) + "\n")


def render_record(
    text_id: str,
    config: dict[str, Any],
    section_num: int,
    section: dict[str, Any],
    draft_result: dict[str, Any],
    review_result: dict[str, Any] | None,
) -> dict[str, Any]:
    draft = draft_result["payload"]
    text = str(draft["text"]).strip()
    review_meta: dict[str, Any] | None = None
    if review_result:
        review = review_result["payload"]
        if review.get("verdict") == "revise" and str(review.get("revised_text", "")).strip():
            text = str(review["revised_text"]).strip()
        review_meta = {
            "model": review_result["model"],
            "deployment": TERRA_DEPLOYMENT,
            "verdict": review.get("verdict"),
            "issues": review.get("issues") or [],
            "reviewed_at": now(),
        }
    witness = "\n\n".join(section["paragraphs"])
    prompt = draft_prompt(config, section)
    prompt_hash = hashlib.sha256(json.dumps(prompt, ensure_ascii=False).encode()).hexdigest()
    record: dict[str, Any] = {
        "id": f"{config['code']}.{section_num:03d}",
        "reference": f"{config['title']} — {section['heading']}",
        "unit": config["unit"],
        "book": config["title"],
        "reader_navigation": {
            "division_kind": config["unit"],
            "order": section_num,
            "heading": section["heading"],
            "authoritative_division": False,
            "note": "Heading and section break are modern navigation aids, not ancient verse divisions.",
        },
        "source": {
            "manuscript": config["manuscript"],
            "ancient_language": config["source_language"],
            "drafting_basis": "Public-domain English translation witness; direct source-language review pending",
            "witness_url": config["url"],
            "witness_translator": config["witness_author"],
            "witness_license": config["witness_license"],
            "english_witness": witness,
        },
        "translation": {
            "text": text,
            "philosophy": "provisional optimal-equivalence bridge",
            "translator_notes": draft.get("notes") or [],
        },
        "ai_draft": {
            "model_id": draft_result["model"],
            "deployment": SOL_DEPLOYMENT,
            "prompt_id": "extra_text_pd_witness_v1",
            "prompt_sha256": prompt_hash,
            "timestamp": now(),
        },
        "status": "provisional_source_bridge",
        "source_language_review": "pending",
    }
    if review_meta:
        record["grounding_review"] = review_meta
    return record


def process_one(text_id: str, section_num: int, section: dict[str, Any], review: bool, force: bool) -> str:
    config = TEXTS[text_id]
    out_dir = TRANSLATION_ROOT / text_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{section_num:03d}.yaml"
    if out_path.exists() and not force:
        return f"cached {text_id} {section_num:03d}"
    drafted = azure_call(SOL_DEPLOYMENT, draft_prompt(config, section))
    reviewed = None
    if review:
        reviewed = azure_call(TERRA_DEPLOYMENT, review_prompt(config, section, drafted["payload"]["text"]))
    record = render_record(text_id, config, section_num, section, drafted, reviewed)
    out_path.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=1000))
    return f"wrote {out_path.relative_to(ROOT)}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", action="append", choices=sorted(TEXTS), required=True)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--review", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not os.environ.get("AZURE_OPENAI_ENDPOINT") or not os.environ.get("AZURE_OPENAI_API_KEY"):
        raise SystemExit("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required")

    jobs: list[tuple[str, int, dict[str, Any]]] = []
    for text_id in args.text:
        config = TEXTS[text_id]
        raw = fetch(config["url"])
        raw_dir = SOURCE_ROOT / text_id
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / "witness.html"
        raw_path.write_text(raw)
        sections = parse_sections(raw, config["start_heading"])
        if not sections:
            raise RuntimeError(f"No sections parsed for {text_id}")
        write_manifest(text_id, config, sections, raw_path)
        for index, section in enumerate(sections, start=1):
            jobs.append((text_id, index, section))

    if args.limit:
        jobs = jobs[: args.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(process_one, text_id, num, section, args.review, args.force) for text_id, num, section in jobs]
        for future in concurrent.futures.as_completed(futures):
            print(future.result(), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
