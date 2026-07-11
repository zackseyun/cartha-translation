#!/usr/bin/env python3
"""Prepare and draft the 23-work early-Christian expansion.

Every record remains explicitly provisional: the drafting basis is an
explicit-public-domain English witness (or Lightfoot's public-domain
translation), while direct source-language review remains a release gate.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("pd_bridge", pathlib.Path(__file__).with_name("draft_public_domain_witness.py"))
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(bridge)

LUM = "https://www.luminescence-llc.net"
CCEL = "https://ccel.org/ccel/lightfoot/fathers"


def cfg(title, code, url, collection, manuscript, language, author, strategy, start=None, urls=None):
    return dict(title=title, code=code, url=url, urls=urls or [url], collection=collection,
                manuscript=manuscript, source_language=language, witness_author=author,
                witness_license="Public domain witness", unit="editorial_section",
                strategy=strategy, start_heading=start)


TEXTS = {
    "treatise_on_the_resurrection": cfg("Treatise on the Resurrection", "TRES", f"{LUM}/resurrection", "nag_hammadi", "Nag Hammadi Codex I,4", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "Introduction"),
    "dialogue_of_the_savior": cfg("Dialogue of the Savior", "DSAV", f"{LUM}/dialogue-of-the-savior", "nag_hammadi", "Nag Hammadi Codex III,5", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "Introduction"),
    "exegesis_on_the_soul": cfg("Exegesis on the Soul", "EXSO", f"{LUM}/the-exegesis-on-the-soul", "nag_hammadi", "Nag Hammadi Codex II,6", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "The Fall of the Soul"),
    "book_of_thomas_the_contender": cfg("Book of Thomas the Contender", "BTHC", f"{LUM}/thomas-the-contender", "nag_hammadi", "Nag Hammadi Codex II,7", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "Incipit"),
    "tripartite_tractate": cfg("Tripartite Tractate", "TRIP", f"{LUM}/tripartate-tractate", "nag_hammadi", "Nag Hammadi Codex I,5", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "Part 1: Cosmology"),
    "apocryphon_of_john": cfg("Apocryphon of John", "APOJ", "https://othergospels.com/john/zinner.json", "nag_hammadi", "Nag Hammadi Codices II,1; III,1; IV,1 and Berlin Codex 8502,2", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison / Rachel Bousfield", "othergospels_json"),
    "hypostasis_of_the_archons": cfg("Hypostasis of the Archons", "HARCH", f"{LUM}/the-substance-of-the-archons", "nag_hammadi", "Nag Hammadi Codex II,4", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "Introduction"),
    "on_the_origin_of_the_world": cfg("On the Origin of the World", "ORIGW", f"{LUM}/on-the-origin-of-the-world", "nag_hammadi", "Nag Hammadi Codex II,5 and related witnesses", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "Introduction"),
    "sophia_of_jesus_christ": cfg("Sophia of Jesus Christ", "SOJC", f"{LUM}/sophia-of-jesus-christ", "nag_hammadi", "Nag Hammadi Codex III,4 and Berlin Codex 8502,3", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "The Savior Appears to His Disciples"),
    "gospel_of_the_egyptians": cfg("Gospel of the Egyptians", "GEGYP", f"{LUM}/the-sacred-book-of-the-great-unseen-spirit", "nag_hammadi", "Nag Hammadi Codices III,2 and IV,2", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "The Sacred Book"),
    "letter_of_peter_to_philip": cfg("Letter of Peter to Philip", "LPPH", f"{LUM}/the-letter-of-peter-to-philip", "nag_hammadi", "Nag Hammadi Codex VIII,2 and Codex Tchacos", "Coptic (source-language review pending)", "Samuel Zinner / Mark M. Mattison", "strong_p", "Introduction"),
    "gospel_of_judas": cfg("Gospel of Judas", "GJUD", "https://www.gospels.net/judas", "early_christian_apocrypha", "Codex Tchacos 3", "Coptic (source-language review pending)", "Mark M. Mattison", "centered_p", "Introduction"),
    "protoevangelium_of_james": cfg("Protoevangelium of James", "PROJ", "https://www.gospels.net/infancyjames", "early_christian_apocrypha", "Greek manuscript tradition", "Greek (source-language review pending)", "Mark M. Mattison", "centered_p", "Chapter 1: Joachim’s Plight"),
    "infancy_gospel_of_thomas": cfg("Infancy Gospel of Thomas", "IGTH", "https://www.gospels.net/infancythomas", "early_christian_apocrypha", "Greek manuscript tradition", "Greek (source-language review pending)", "Mark M. Mattison", "centered_p", "Chapter 1: Prologue"),
    "acts_of_paul_and_thecla": cfg("Acts of Paul and Thecla", "APTH", "https://en.wikisource.org/wiki/Acts_of_Paul_and_Thecla_(Jeremiah_Jones_translation)?printable=yes", "early_christian_apocrypha", "Greek and versional manuscript tradition", "Greek (source-language review pending)", "Jeremiah Jones (1820 edition)", "html_headings", "CHAPTER I"),
    "gospel_of_peter": cfg("Gospel of Peter", "GPET", "https://www.gospels.net/peter", "early_christian_apocrypha", "Akhmim Codex, P.Cair. 10759", "Greek (source-language review pending)", "Mark M. Mattison", "centered_p", "Pilate and Herod"),
    "2_clement": cfg("2 Clement", "2CLEM", f"{CCEL}/fathers.ii.ii.html", "apostolic_fathers", "Greek manuscript tradition", "Greek (source-language review pending)", "J. B. Lightfoot", "ccel", "2 Clem. 1"),
    "epistle_of_barnabas": cfg("Epistle of Barnabas", "BARN", f"{CCEL}/fathers.ii.xiii.html", "apostolic_fathers", "Codex Sinaiticus and related Greek/Latin witnesses", "Greek/Latin (source-language review pending)", "J. B. Lightfoot", "ccel", "Barn. 1"),
    "letters_of_ignatius": cfg("Letters of Ignatius", "IGN", f"{CCEL}/fathers.ii.iii.html", "apostolic_fathers", "Middle-recension Greek manuscript tradition", "Greek (source-language review pending)", "J. B. Lightfoot", "ccel", "IgnEph. Prologue", urls=[f"{CCEL}/fathers.ii.{x}.html" for x in ("iii", "iv", "v", "vi", "vii", "viii", "ix")]),
    "polycarp_to_the_philippians": cfg("Polycarp to the Philippians", "POLY", f"{CCEL}/fathers.ii.x.html", "apostolic_fathers", "Greek and Latin manuscript tradition", "Greek/Latin (source-language review pending)", "J. B. Lightfoot", "ccel", "PolPhil. Prologue"),
    "martyrdom_of_polycarp": cfg("Martyrdom of Polycarp", "MPOL", f"{CCEL}/fathers.ii.xi.html", "apostolic_fathers", "Greek manuscript tradition", "Greek (source-language review pending)", "J. B. Lightfoot", "ccel", "MartPol. Prologue"),
    "epistle_to_diognetus": cfg("Epistle to Diognetus", "DIOG", f"{CCEL}/fathers.ii.xv.html", "apostolic_fathers", "Codex Argentoratensis (lost; known through copies)", "Greek (source-language review pending)", "J. B. Lightfoot", "ccel", "Diogn. 1"),
    "fragments_of_papias": cfg("Fragments of Papias", "PAPI", "https://archive.org/details/apostolicfathers00lighuoft", "apostolic_fathers", "Fragments preserved in Eusebius and later witnesses", "Greek/Latin (source-language review pending)", "J. B. Lightfoot", "papias_pdf"),
}

for _chapter_work in (
    "protoevangelium_of_james", "infancy_gospel_of_thomas",
    "acts_of_paul_and_thecla", "2_clement", "epistle_of_barnabas",
    "polycarp_to_the_philippians", "martyrdom_of_polycarp",
    "epistle_to_diognetus",
):
    TEXTS[_chapter_work]["unit"] = "chapter"
TEXTS["fragments_of_papias"]["unit"] = "fragment"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Cartha-POB/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8", "ignore")


def clean(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<sup\b[^>]*>.*?</sup>", "", fragment, flags=re.I | re.S)
    return bridge.clean_html(fragment)


def parse_paragraph_headings(raw: str, start: str, whole_strong: bool) -> list[dict]:
    items = []
    for m in re.finditer(r"<p\b([^>]*)>(.*?)</p>", raw, re.I | re.S):
        attrs, body = m.groups()
        body = re.sub(r"(?:<a\b[^>]*>)?\s*<strong\b[^>]*>\s*\d{1,3}\s*</strong>\s*(?:</a>)?(?:\s|&nbsp;)*", "", body, flags=re.I)
        text = clean(body)
        if not text:
            continue
        centered = "text-align:center" in attrs.replace(" ", "").lower() and "<strong" in body.lower()
        strong = bool(re.fullmatch(r"\s*<strong\b[^>]*>.*?</strong>\s*", body, re.I | re.S))
        items.append(("heading" if centered or (whole_strong and strong) else "paragraph", text))
    return collect(items, start)


def parse_heading_html(raw: str, start: str, ccel: bool = False) -> list[dict]:
    items = []
    for m in re.finditer(r"<(h[2-4]|p)\b[^>]*>(.*?)</\1>", raw, re.I | re.S):
        tag, body = m.groups()
        text = clean(body)
        if not text:
            continue
        kind = "heading" if tag.lower().startswith("h") else "paragraph"
        if ccel and kind == "heading" and not re.match(r"(?:2 Clem\.|Barn\.|Ign|PolPhil\.|MartPol\.|Diogn\.)", text):
            continue
        items.append((kind, text))
    return collect(items, start)


def collect(items, start):
    out, current, started = [], None, False
    for kind, text in items:
        if kind == "heading":
            if text == start:
                started = True
            if not started:
                continue
            if text.strip().lower() in {"notes", "references", "bibliography"} or text.lower().startswith("notes on translation"):
                break
            current = {"heading": text, "paragraphs": []}
            out.append(current)
        elif started and current is not None:
            current["paragraphs"].append(text)
    return [x for x in out if x["paragraphs"]]


def parse_othergospels_json(raw: str) -> list[dict]:
    data = json.loads(raw)
    result = []
    for i, chapter in enumerate(data.get("chapters", []), 1):
        title = chapter.get("title") or chapter.get("section") or f"Section {i}"
        body = chapter.get("body") or []
        if not body and chapter.get("bodies"):
            choices = chapter["bodies"]
            choice = next((x for x in choices if "codex-iv" in (x.get("classes") or [])), choices[0])
            body = choice.get("body") or []
        paragraphs = [re.sub(r"\*\*(\d+)\.\*\*", r"\1.", str(x)).strip() for x in body if str(x).strip()]
        if paragraphs:
            result.append({"heading": title, "paragraphs": paragraphs})
    return result


def parse_papias() -> tuple[str, list[dict]]:
    pdf = ROOT / "sources/shepherd_of_hermas/scans/lightfoot_1891_apostolic_fathers.pdf"
    raw = subprocess.check_output(["pdftotext", "-layout", "-f", "543", "-l", "551", str(pdf), "-"]).decode("utf-8", "ignore")
    matches = list(re.finditer(r"(?m)^\s*([IVXLCDM]+)\.\s*$", raw))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(raw)
        body = re.sub(r"(?m)^\s*(?:\d+\s+)?THE\s+FRAGMENTS\s+OF\s+PAPIAS.*$", "", raw[match.end():end])
        body = re.sub(r"\n\s*\n+", "\n\n", body).strip()
        if len(body) > 30:
            sections.append({"heading": f"Fragment {match.group(1)}", "paragraphs": [body]})
    return raw, sections


def prepare(text_id: str):
    config = TEXTS[text_id]
    if config["strategy"] == "papias_pdf":
        raw, sections = parse_papias()
    else:
        raws = [fetch(url) for url in config["urls"]]
        raw = "\n<!-- NEXT SOURCE PAGE -->\n".join(raws)
        if config["strategy"] == "strong_p":
            sections = parse_paragraph_headings(raw, config["start_heading"], True)
        elif config["strategy"] == "centered_p":
            sections = parse_paragraph_headings(raw, config["start_heading"], False)
        elif config["strategy"] == "html_headings":
            sections = parse_heading_html(raw, config["start_heading"])
        elif config["strategy"] == "ccel":
            sections = []
            for page in raws:
                headings = [clean(x) for x in re.findall(r"<h[2-4][^>]*>(.*?)</h[2-4]>", page, re.I | re.S)]
                first_unit = next((x for x in headings if re.match(r"(?:2 Clem\.|Barn\.|Ign|PolPhil\.|MartPol\.|Diogn\.)", x)), "")
                candidates = parse_heading_html(page, config["start_heading"] if not sections else first_unit, True)
                sections.extend(candidates)
        else:
            sections = parse_othergospels_json(raw)
    if not sections:
        raise RuntimeError(f"No sections parsed for {text_id}")
    target = bridge.SOURCE_ROOT / text_id
    target.mkdir(parents=True, exist_ok=True)
    suffix = "json" if config["strategy"] == "othergospels_json" else ("txt" if config["strategy"] == "papias_pdf" else "html")
    raw_path = target / f"witness.{suffix}"
    raw_path.write_text(raw)
    bridge.write_manifest(text_id, config, sections, raw_path)
    return sections


def credentials():
    if not os.environ.get("AZURE_OPENAI_API_KEY"):
        os.environ["AZURE_OPENAI_API_KEY"] = subprocess.check_output(["az", "cognitiveservices", "account", "keys", "list", "-g", "rg-cartha-truth-openai", "-n", "cartha-aoai-truth-1c9177c8", "--query", "key1", "-o", "tsv"], text=True).strip()
    if not os.environ.get("AZURE_OPENAI_ENDPOINT"):
        os.environ["AZURE_OPENAI_ENDPOINT"] = subprocess.check_output(["az", "cognitiveservices", "account", "show", "-g", "rg-cartha-truth-openai", "-n", "cartha-aoai-truth-1c9177c8", "--query", "properties.endpoint", "-o", "tsv"], text=True).strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", action="append", choices=sorted(TEXTS))
    p.add_argument("--all", action="store_true")
    p.add_argument("--workers", type=int, default=24)
    p.add_argument("--review", action="store_true")
    p.add_argument("--prepare-only", action="store_true")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()
    selected = sorted(TEXTS) if args.all else (args.text or [])
    if not selected:
        p.error("use --all or --text")
    bridge.TEXTS = TEXTS
    jobs = []
    for text_id in selected:
        sections = prepare(text_id)
        print(f"prepared {text_id}: {len(sections)} sections", flush=True)
        jobs.extend((text_id, i, s) for i, s in enumerate(sections, 1))
    if args.prepare_only:
        return 0
    credentials()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(bridge.process_one, tid, n, section, args.review, args.force) for tid, n, section in jobs]
        for f in concurrent.futures.as_completed(futures):
            print(f.result(), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
