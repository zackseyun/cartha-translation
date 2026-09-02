#!/usr/bin/env python3
"""Index three distinct evidence layers; never treat triage as adjudication."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_sblgnt_apparatus import verify as verify_apparatus

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources/textual_restoration/inventory"
REPORT = ROOT / "docs/HEBREW_AND_NT_VARIANT_MAP.md"
NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
NT_MAP = dict(zip(
    "Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev".split(),
    "matthew mark luke john acts romans 1_corinthians 2_corinthians galatians ephesians philippians colossians 1_thessalonians 2_thessalonians 1_timothy 2_timothy titus philemon hebrews james 1_peter 2_peter 1_john 2_john 3_john jude revelation".split()))
OT_MAP = dict(zip(
    "Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal".split(),
    "genesis exodus leviticus numbers deuteronomy joshua judges ruth 1_samuel 2_samuel 1_kings 2_kings 1_chronicles 2_chronicles ezra nehemiah esther job psalms proverbs ecclesiastes song_of_songs isaiah jeremiah lamentations ezekiel daniel hosea joel amos obadiah jonah micah nahum habakkuk zephaniah haggai zechariah malachi".split()))
WITNESS_RE = re.compile(r"manuscripts?|masoretic|septuagint|qumran|dead sea|samaritan|peshitta|vulgate|old (?:greek|latin|syriac)|textual variant|qere|keti[bv]|codex|papyri|papyrus|\bNA2[789]\b|SBLGNT|\bWLC\b|marginal reading|traditional (?:alternative )?reading", re.I)
EDITION_RE = re.compile(r"(?<![A-Za-z])(?:WHmarg|WHapp|Tregmarg|Treg|NIV|RP|NA2[78]|Holmes|WH|TR|Greeven)(?![A-Za-z])")
TYPED = {"textual_variant", "textual_critical", "textual_alternative"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def footnote_signals(record: dict) -> list[dict]:
    result = []
    for n, note in enumerate(record.get("translation", {}).get("footnotes", []) or []):
        if not isinstance(note, dict):
            continue
        reason, text = str(note.get("reason", "")), str(note.get("text", ""))
        typed = reason in TYPED or reason.startswith("textual_")
        mentioned = sorted(set(m.group(0).lower() for m in WITNESS_RE.finditer(text)))
        if typed or mentioned:
            result.append({"footnote_index": n, "marker": note.get("marker"), "reason": reason,
                           "text": text, "signal": "typed-textual-note" if typed else "witness-mention-screen",
                           "matched_terms": mentioned})
    return result


def scan_pob(root: Path = ROOT):
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    index, grouped, stats = {}, defaultdict(list), {}
    corpus_digest = hashlib.sha256()
    errors = []
    for testament in ("ot", "nt"):
        for book in sorted((root / "translation" / testament).iterdir()):
            if not book.is_dir():
                continue
            key = f"{testament}/{book.name}"
            stat = stats.setdefault(key, {"files_scanned": 0, "flagged_passages": 0, "typed_notes": 0,
                                          "mention_notes": 0, "source_marker_passages": 0})
            grouped[key] = []
            for path in sorted(book.glob("*/*.yaml")):
                raw = path.read_bytes()
                if len(raw) > 2_000_000:
                    errors.append(f"oversize file: {path}")
                    continue
                relative = path.relative_to(root).as_posix()
                file_hash = sha(raw)
                corpus_digest.update(f"{relative}\0{file_hash}\n".encode())
                try:
                    data = yaml.load(raw, Loader=loader)
                    if not isinstance(data, dict) or not isinstance(data.get("translation"), dict):
                        raise ValueError("not a verse record")
                    chapter, verse = int(path.parent.name), int(path.stem)
                except (ValueError, yaml.YAMLError) as exc:
                    errors.append(f"{relative}: {exc}")
                    continue
                stat["files_scanned"] += 1
                signals = footnote_signals(data)
                source = data.get("source") or {}
                if re.search("[⸀⸁⸂⸃⸄⸅]", str(source.get("text", ""))):
                    stat["source_marker_passages"] += 1
                row = {"id": data.get("id"), "reference": data.get("reference"),
                       "testament": testament, "book": book.name, "chapter": chapter, "verse": verse,
                       "repo_path": relative, "sha256": file_hash, "source_edition": source.get("edition"),
                       "source_text": source.get("text"), "english_snapshot": data["translation"].get("text"),
                       "signals": signals, "evidence_type": "local-editorial-note-screen",
                       "reference_system": "POB", "adjudicated": False}
                index[(testament, book.name, chapter, verse)] = row
                if signals:
                    grouped[key].append(row)
                    stat["flagged_passages"] += 1
                    for signal in signals:
                        stat["typed_notes" if signal["signal"] == "typed-textual-note" else "mention_notes"] += 1
    if errors:
        raise ValueError("Corpus scan incomplete:\n" + "\n".join(errors[:30]))
    return index, grouped, stats, corpus_digest.hexdigest()


def parse_wlc(path: Path):
    qere, annotations = [], []
    tree = ET.parse(path)
    for verse in tree.findall(".//o:verse", NS):
        reference = verse.get("osisID")
        for n, note in enumerate(verse.findall("o:note", NS)):
            if note.get("type") == "variant":
                readings = note.findall("o:rdg[@type='x-qere']", NS)
                if not readings:
                    raise ValueError(f"Unknown WLC variant structure: {path}:{reference}")
                qere.append({"id": f"{reference}.qere.{n}", "reference": reference,
                             "reference_system": "WLC/OSHB, not automatically POB-aligned",
                             "ketiv": note.findtext("o:catchWord", default="", namespaces=NS),
                             "qere": [" ".join("".join(w.itertext()) for w in r.findall("o:w", NS)) for r in readings],
                             "evidence_type": "masoretic-written-read-tradition",
                             "independent_manuscript_variant": False, "adjudicated": False})
            elif note.get("n"):
                annotations.append({"id": f"{reference}.annotation.{n}", "reference": reference,
                                    "reference_system": "WLC/OSHB", "code": note.get("n"),
                                    "text": "".join(note.itertext()).strip(),
                                    "evidence_type": "edition-transcription-annotation",
                                    "independent_manuscript_variant": False})
    return qere, annotations


def parse_apparatus(path: Path, local_index: dict):
    book = NT_MAP[path.stem]
    ref, chapter, verse, ordinal = None, None, None, 0
    rows = []
    for element in ET.parse(path).getroot():
        if element.tag == "verse":
            ref = "".join(element.itertext()).strip()
            match = re.fullmatch(r".+? (\d+):(\d+)", ref)
            if not match:
                raise ValueError(f"Unparsed SBLGNT reference: {ref}")
            chapter, verse = map(int, match.groups())
            ordinal = 0
        elif element.tag == "note":
            if ref is None:
                raise ValueError(f"Unanchored apparatus note: {path}")
            ordinal += 1
            raw = "".join(element.itertext()).strip()
            local = local_index.get(("nt", book, chapter, verse))
            # Notes can span verses or contain ellipses: do not invent a full aligned text.
            span = bool(re.search(r"^\d+(?::\d+)?[–-]\d+|\.\.\.|…|⟦", raw))
            rows.append({"id": f"SBLAPP.{path.stem}.{chapter}.{verse}.{ordinal}", "reference": ref,
                         "testament": "nt", "book": book, "chapter": chapter, "verse": verse,
                         "reference_system": "publisher SBLGNT apparatus anchor",
                         "raw_note": raw, "edition_labels": sorted(set(EDITION_RE.findall(raw))),
                         "evidence_type": "critical-edition-comparison-not-manuscript-collation",
                         "requires_span_or_bracket_review": span,
                         "local_reference_match": None if local is None else local["repo_path"],
                         "local_textual_note_detected": bool(local and local["signals"]),
                         "alignment_status": "reference-anchor-only-not-token-aligned",
                         "adjudicated": False})
    return rows


def write_jsonl(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))


def casebook(index: dict, nt_rows: list[dict]) -> list[dict]:
    targets = json.loads((ROOT / "sources/textual_restoration/casebook_targets.v1.json").read_text())["records"]
    by_anchor = defaultdict(list)
    for row in nt_rows:
        by_anchor[(row["book"], row["chapter"], row["verse"])].append(row)
    result = []
    for target in targets:
        key = (target["testament"], target["book"], target["chapter"], target["verse"])
        local = index.get(key)
        entries = by_anchor[(target["book"], target["chapter"], target["verse"])] if target["testament"] == "nt" else []
        result.append({**target, "local_snapshot": local,
                       "edition_anchor_entries": entries,
                       "edition_entries_are_topic_specific": False,
                       "canonical_promotion_approved": False,
                       "image_restoration_performed": False})
    lines = ["# Priority source-variant casebook", "",
             f"**{len(result)} targeted cases:** Hebrew/Aramaic and Greek New Testament. This is a purposeful shortlist beside the [corpus-wide map](HEBREW_AND_NT_VARIANT_MAP.md), not an exhaustive list of manuscript differences.", "",
             "The source lists are **what to collate**, not claims that every named source attests a particular reading. Some cases are controls: a translation question, literary parallel, or scribal-correction tradition must not be misreported as a surviving manuscript variant.", "",
             "Three Hebrew cases have the earlier [provisional adjudication](HEBREW_PILOT_ADJUDICATION.md), and [Mark 1:41 has an initial published-witness review](NT_PILOT_ADJUDICATION.md). Other entries await passage-level evidence review. No case here was automatically promoted into POB.", ""]
    for testament in ("ot", "nt"):
        lines += ["## " + ("Hebrew and Aramaic" if testament == "ot" else "Greek New Testament"), "",
                  "| Passage / issue | Evidence question | Existing POB source-note signals | Edition entries at anchor | Sources to collate |",
                  "|---|---|---:|---:|---|"]
        for row in result:
            if row["testament"] != testament:
                continue
            local = row["local_snapshot"]
            ref = row["reference_label"]
            if local:
                ref = f"[{ref}](../{local['repo_path']})"
            signals = len(local["signals"]) if local else "no local match"
            values = [ref + " — " + row["topic"], row["category"], str(signals),
                      str(len(row["edition_anchor_entries"])) if testament == "nt" else "not applicable",
                      "; ".join(row["sources_to_collate"])]
            lines.append("| " + " | ".join(v.replace("|", "\\|") for v in values) + " |")
        lines.append("")
    lines += ["## Reading this map", "",
              "- A zero edition-entry count does not exclude manuscript variation. A nonzero count does not guarantee completeness either: the Revelation 13:18 entries do not cover the 616 reading.",
              "- Counts are at the reference anchor, not a claim that every entry addresses the named issue or is consequential in English.",
              "- Ranges and alternate locations require explicit span mapping. Hebrew verse numbering is not silently joined to POB numbering.",
              "- Existing POB notes are editorial leads, not independent manuscript evidence. Notes may need correction themselves.",
              "- Qere/ketiv data are already extracted separately. For example, Psalm 100:3 and Job 13:15 preserve a not/to-him-or-his distinction in the written/read traditions; this is not proof of two independent manuscripts.", "",
              "## Data", "",
              "- [Target definitions](../sources/textual_restoration/casebook_targets.v1.json)",
              "- [Cases with local source snapshots and edition entries](../sources/textual_restoration/inventory/priority_cases.jsonl)",
              "- [NT source-wording workflow and examples](NT_TEXTUAL_WITNESS_METHOD.md)", ""]
    (ROOT / "docs/TEXTUAL_VARIANT_CASEBOOK.md").write_text("\n".join(lines))
    return result


def build() -> dict:
    manifest = verify_apparatus()
    index, notes, stats, snapshot = scan_pob()
    outputs, wlc_sources, qere_counts, annotation_counts, nt_counts = [], [], {}, {}, {}
    def emit(relative, rows):
        path = OUT / relative
        write_jsonl(path, rows)
        outputs.append({"path": relative, "records": len(rows), "sha256": sha(path.read_bytes())})
    for key, rows in notes.items():
        emit(f"local_notes/{key}.jsonl", rows)
    for path in sorted((ROOT / "sources/ot/wlc").glob("*.xml")):
        if path.stem not in OT_MAP:
            continue
        qere, annotations = parse_wlc(path)
        key = f"ot/{OT_MAP[path.stem]}"
        qere_counts[key], annotation_counts[key] = len(qere), len(annotations)
        wlc_sources.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path.read_bytes())})
        emit(f"hebrew_qere/{path.stem}.jsonl", qere)
        emit(f"hebrew_annotations/{path.stem}.jsonl", annotations)
    nt_rows = []
    for path in sorted((ROOT / "sources/nt/sblgnt_apparatus/xml").glob("*.xml")):
        rows = parse_apparatus(path, index)
        nt_rows.extend(rows)
        key = f"nt/{NT_MAP[path.stem]}"
        nt_counts[key] = len(rows)
        emit(f"nt_editions/{path.stem}.jsonl", rows)
    cases = casebook(index, nt_rows)
    emit("priority_cases.jsonl", cases)
    for key, stat in stats.items():
        stat.update(qere_records=qere_counts.get(key, 0), hebrew_annotations=annotation_counts.get(key, 0),
                    nt_apparatus_entries=nt_counts.get(key, 0))
    summary = {"schema_version": "1.0.0", "scope": "66-book POB canonical records plus WLC and 27-book SBLGNT edition apparatus",
               "not_exhaustive_manuscript_apparatus": True, "canonical_text_modified": False,
               "corpus_snapshot_sha256": snapshot, "apparatus_commit": manifest["commit"],
               "casebook_targets_sha256": sha((ROOT / "sources/textual_restoration/casebook_targets.v1.json").read_bytes()),
               "books": stats, "wlc_sources": wlc_sources, "outputs": outputs,
               "totals": {"books_scanned": len(stats), "verse_files_scanned": sum(s["files_scanned"] for s in stats.values()),
                          "local_note_flagged_passages": sum(s["flagged_passages"] for s in stats.values()),
                          "hebrew_qere_records": sum(qere_counts.values()), "hebrew_editorial_annotations": sum(annotation_counts.values()),
                          "nt_edition_apparatus_entries": len(nt_rows),
                          "priority_cases": len(cases),
                          "nt_apparatus_anchor_passages": len({x["reference"] for x in nt_rows}),
                          "nt_unmatched_reference_anchors": len({x["reference"] for x in nt_rows if not x["local_reference_match"]}),
                          "nt_anchor_passages_without_detected_textual_note": len({x["reference"] for x in nt_rows if x["local_reference_match"] and not x["local_textual_note_detected"]})}}
    expected_books = {"ot/" + x for x in OT_MAP.values()} | {"nt/" + x for x in NT_MAP.values()}
    if set(stats) != expected_books or any(s["files_scanned"] == 0 for s in stats.values()) or len(qere_counts) != 39 or len(nt_counts) != 27:
        raise ValueError(f"Unexpected book coverage: POB={len(stats)}, WLC={len(qere_counts)}, NT={len(nt_counts)}")
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    REPORT.write_text(render(summary))
    return summary


def verify_inventory() -> dict:
    verify_apparatus()
    summary = json.loads((OUT / "summary.json").read_text())
    if summary["not_exhaustive_manuscript_apparatus"] is not True or summary["canonical_text_modified"] is not False:
        raise ValueError("Inventory must not claim exhaustive collation or canonical modification")
    expected_books = {"ot/" + x for x in OT_MAP.values()} | {"nt/" + x for x in NT_MAP.values()}
    if set(summary["books"]) != expected_books:
        raise ValueError("Incomplete canonical book coverage")
    for source in summary["wlc_sources"]:
        if sha((ROOT / source["path"]).read_bytes()) != source["sha256"]:
            raise ValueError(f"WLC source drift: {source['path']}")
    if sha((ROOT / "sources/textual_restoration/casebook_targets.v1.json").read_bytes()) != summary["casebook_targets_sha256"]:
        raise ValueError("Casebook definitions changed; regenerate inventory")
    for item in summary["outputs"]:
        raw = (OUT / item["path"]).read_bytes()
        if sha(raw) != item["sha256"] or len(raw.splitlines()) != item["records"]:
            raise ValueError(f"Inventory output drift: {item['path']}")
        for line in raw.splitlines():
            json.loads(line)
    if REPORT.read_text() != render(summary):
        raise ValueError("Summary report drift; regenerate inventory")
    return summary


def render(summary: dict) -> str:
    t = summary["totals"]
    lines = ["# Hebrew and New Testament source-variant map", "",
             "This is a corpus-wide **screening map**, not a completed manuscript apparatus or a list of proven errors.", "",
             f"Scanned **{t['verse_files_scanned']:,} canonical verse files across {t['books_scanned']} books**.", "",
             f"- Local POB footnote signals: **{t['local_note_flagged_passages']:,} passages**. Some are lexical or interpretive false positives requiring review.",
             f"- WLC written/read variants: **{t['hebrew_qere_records']:,} qere/ketiv records**. These are Masoretic reading traditions, not that many independent manuscript disagreements.",
             f"- WLC editorial/transcription annotations: **{t['hebrew_editorial_annotations']:,} records**. Accent, vowel, consonant, and other editorial notes remain a separate layer.",
             f"- NT edition apparatus: **{t['nt_edition_apparatus_entries']:,} entries at {t['nt_apparatus_anchor_passages']:,} reference anchors**, across all 27 NT books.", "",
             "These layers overlap and must not be added together as a total of unique variants. Counts refer to repository records, not a reconstructed total of unique biblical verses. A book with zero detected footnotes is not a book with no variants.", "",
             "## Coverage and its limits", "",
             "The NT data come from the pinned, licensed SBLGNT publisher apparatus, which compares edited Greek texts. Edition labels are not manuscript IDs, votes, or the latest ECM/UBS6 apparatus. Raw notes are retained; ranges, brackets, and ellipses need manual/machine adjudication before token alignment.", "",
             f"There are **{t['nt_anchor_passages_without_detected_textual_note']:,} matched NT reference anchors without a detected textual footnote**. This is a triage list, not a requirement to footnote every spelling or word-order difference. **{t['nt_unmatched_reference_anchors']} anchors** have no same-numbered local verse file; omitted verses and numbering must be checked before calling these data loss.", "",
             "Hebrew XML references retain WLC numbering. POB numbering, especially Psalms, must be mapped explicitly before joining records. The Hebrew side is not yet a complete MT–DSS–Samaritan–Greek collation.", "",
             "## Book map", "",
             "| Testament / book | Verse files | POB note leads | Qere / ketiv | Hebrew annotations | NT edition entries |",
             "|---|---:|---:|---:|---:|---:|"]
    for key, stat in summary["books"].items():
        lines.append(f"| {key.replace('_', ' ')} | {stat['files_scanned']} | {stat['flagged_passages']} | {stat['qere_records']} | {stat['hebrew_annotations']} | {stat['nt_apparatus_entries']} |")
    lines += ["", "## Next comparison targets", "",
              "Use the [priority casebook](TEXTUAL_VARIANT_CASEBOOK.md) for meaning-changing examples and the [source-wording method](TEXTUAL_ADJUDICATION_METHOD.md) for adjudication. The [NT workflow](NT_TEXTUAL_WITNESS_METHOD.md) keeps Greek manuscript evidence separate from editorial comparisons.", "",
              "## Reproduce and inspect", "",
              "- [Inventory manifest and totals](../sources/textual_restoration/inventory/summary.json)",
              "- [Local POB note leads](../sources/textual_restoration/inventory/local_notes/)",
              "- [Hebrew written/read records](../sources/textual_restoration/inventory/hebrew_qere/)",
              "- [Hebrew editorial annotations](../sources/textual_restoration/inventory/hebrew_annotations/)",
              "- [NT edition comparison records](../sources/textual_restoration/inventory/nt_editions/)",
              "- [SBLGNT source provenance and license](../sources/nt/sblgnt_apparatus/README.md)", "",
              "```bash", "python3 tools/textual_restoration/build_variant_inventory.py", "```", "",
              "Derived SBLGNT apparatus records: CC BY 4.0; original edition © 2010 Society of Biblical Literature and Logos Bible Software, edited by Michael W. Holmes. Extraction and POB reference-screen fields were added by this project; upstream raw notes were not rewritten.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="verify snapshot artifacts without rescanning canonical source files")
    args = parser.parse_args()
    summary = verify_inventory() if args.verify_only else build()
    print(json.dumps(summary["totals"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
