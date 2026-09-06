#!/usr/bin/env python3
"""Versioned whole-OT edition screen; no canonical writer or priority decision."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unicodedata as U
import xml.etree.ElementTree as E
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "sources/textual_restoration/discovery"
PROTOCOL = DIR / "uxlc_wlc_comparison_protocol.v1.json"
BOOKMAP = DIR / "hebrew_bible_book_map.v1.json"
OUTPUT = DIR / "uxlc_wlc_comparison.v1.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def tag(e):
    return e.tag.split("}")[-1]


def normalized(text, layer):
    text = U.normalize("NFD", text)
    if layer == "full":
        return U.normalize("NFD", "".join(c for c in text if not c.isspace() and c not in "/\u034f"))
    letters = lambda c: "\u05d0" <= c <= "\u05ea"
    points = lambda c: "\u05b0" <= c <= "\u05bc" or c in "\u05bf\u05c1\u05c2\u05c7"
    accents = lambda c: "\u0591" <= c <= "\u05af" or c == "\u05bd"
    if layer not in ("consonants", "pointing", "accents"):
        raise ValueError("unknown layer")
    return U.normalize("NFD", "".join(c for c in text if letters(c) or (layer != "consonants" and points(c)) or (layer == "accents" and accents(c))))


def mixed(e, annotations, position):
    text = e.text or ""
    for child in e:
        if tag(child) == "x":
            annotations.append({"position": position, "kind": "x", "attributes": child.attrib, "code": "".join(child.itertext())})
        elif tag(child) == "s":
            annotations.append({"position": position, "kind": "s", "attributes": child.attrib})
            text += mixed(child, annotations, position)
        else:
            raise ValueError("unexpected mixed word tag " + tag(child))
        text += child.tail or ""
    return text


def parse_uxlc(raw):
    root = E.fromstring(raw)
    versions = [e.text for e in root.findall(".//edition/version")]
    if versions != ["UXLC 2.5"]:
        raise ValueError("UXLC version mismatch")
    result = {}
    for chapter in root.findall(".//tanach/book/c"):
        for verse in chapter.findall("v"):
            key = (int(chapter.get("n")), int(verse.get("n")))
            row = {"written": [], "qere": [], "annotations": [], "other_note_types": {}}
            for i, child in enumerate(verse):
                name = tag(child)
                if name in ("w", "k", "q"):
                    value = {"kind": name, "position": i, "text": mixed(child, row["annotations"], i)}
                    row["qere" if name == "q" else "written"].append(value)
                elif name in ("pe", "samekh", "reversednun", "x"):
                    row["annotations"].append({"position": i, "kind": name, "attributes": child.attrib, "code": "".join(child.itertext())})
                else:
                    raise ValueError("unexpected UXLC verse tag " + name)
            if key in result:
                raise ValueError("duplicate UXLC verse")
            result[key] = row
    if not result:
        raise ValueError("no UXLC verses")
    return result


def parse_wlc(raw):
    result = {}
    for verse in E.fromstring(raw).iter():
        if tag(verse) != "verse":
            continue
        _, c, v = verse.get("osisID").split(".")
        row = {"written": [], "qere": [], "annotations": [], "other_note_types": {}}
        notes = Counter()
        for i, child in enumerate(verse):
            name = tag(child)
            if name == "w":
                row["written"].append({"kind": child.get("type", "w"), "position": i, "text": wlc_word(child, row["annotations"], i)})
            elif name == "seg":
                row["annotations"].append({"position": i, "kind": "seg", "attributes": child.attrib, "code": child.text or ""})
            elif name == "note":
                qeres = [r for r in child if tag(r) == "rdg" and r.get("type") == "x-qere"]
                if child.get("type") == "variant" and qeres:
                    for r in qeres:
                        words = [w for w in r if tag(w) == "w"]
                        row["qere"].append({"kind": "qere-group", "position": i,
                            "text": " ".join(wlc_word(w, row["annotations"], i) for w in words), "word_count": len(words),
                            "catchwords": [n.text or "" for n in child if tag(n) == "catchWord"]})
                else:
                    notes[child.get("type", "unspecified")] += 1
            else:
                raise ValueError("unexpected WLC verse child " + name)
        row["other_note_types"] = dict(notes)
        key = int(c), int(v)
        if key in result:
            raise ValueError("duplicate WLC verse")
        result[key] = row
    return result


def wlc_word(e, annotations, position):
    text = e.text or ""
    for child in e:
        if tag(child) != "seg" or child.get("type") not in ("x-large", "x-small", "x-suspended") or len(child):
            raise ValueError("unexpected nested WLC word")
        annotations.append({"position": position, "kind": "word-seg", "attributes": child.attrib})
        text += (child.text or "") + (child.tail or "")
    return text


def written_stream(row):
    # OSHB stores punctuation outside w; UXLC stores it within w/k.
    units = [(w["position"], w["text"]) for w in row["written"]]
    units += [(a["position"], a["code"]) for a in row["annotations"]
              if a["kind"] == "seg" and a["attributes"].get("type") in ("x-maqqef", "x-sof-pasuq", "x-paseq")]
    return "".join(text for _, text in sorted(units))


def comparison(a, b):
    aw, bw = (written_stream(r) for r in (a, b))
    kind = next((layer for layer in ("consonants", "pointing", "accents", "full")
                 if normalized(aw, layer) != normalized(bw, layer)), None)
    # Ordered payload, not a token-to-token or apparatus-unit alignment.
    # Qere punctuation placement differs by format; compare through accents.
    qere = normalized("".join(q["text"] for q in a["qere"]), "accents") != normalized("".join(q["text"] for q in b["qere"]), "accents")
    structure = (bool(a["qere"]), sum(q.get("word_count", bool(q["text"].strip())) for q in a["qere"])) != (bool(b["qere"]), sum(q.get("word_count", bool(q["text"].strip())) for q in b["qere"]))
    boundaries = [normalized(w["text"], "consonants") for w in a["written"]] != [normalized(w["text"], "consonants") for w in b["written"]]
    return {"written_difference": kind, "qere_payload_difference": qere,
            "qere_presence_or_word_count_difference": structure,
            "written_token_boundary_or_payload_difference": boundaries}


def member_name(book):
    if book.startswith(("1_", "2_")):
        digit, name = book.split("_", 1)
        return "Books/" + name.title() + "_" + digit + ".xml"
    return "Books/" + "_".join(w.title() if w != "of" else w for w in book.split("_")) + ".xml"


def build(archive):
    p = json.loads(PROTOCOL.read_text())
    raw = archive.read_bytes()
    if len(raw) != p["uxlc"]["bytes"] or digest(raw) != p["uxlc"]["sha256"]:
        raise ValueError("archive pin mismatch")
    catalog = json.loads(BOOKMAP.read_text())["books"]
    if len(catalog) != 39:
        raise ValueError("book count drift")
    inputs = {str(f.relative_to(ROOT)): digest(f.read_bytes()) for f in (PROTOCOL, BOOKMAP, Path(__file__))}
    books, differences, unmatched, joins = [], [], [], []
    with zipfile.ZipFile(archive) as z:
        members = [{"name": i.filename, "bytes": i.file_size} for i in z.infolist()]
        if sum(i["bytes"] for i in members) > p["acquisition"]["expanded_cap_bytes"] or len(z.namelist()) != len(set(z.namelist())):
            raise ValueError("archive expansion or duplicate member")
        expected = {member_name(row["book"]) for row in catalog}
        actual = {n for n in z.namelist() if n.startswith("Books/") and n.endswith(".xml") and not n.endswith(".DH.xml") and n not in ("Books/TanachHeader.xml", "Books/TanachIndex.xml")}
        if expected != actual:
            raise ValueError("ordinary-book member set mismatch")
        for item in catalog:
            book, short = item["book"], item["wlc_book"]
            wlc = ROOT / "sources/ot/wlc" / (short + ".xml")
            oldraw, newraw = wlc.read_bytes(), z.read(member_name(book))
            inputs[str(wlc.relative_to(ROOT))] = digest(oldraw)
            old, new = parse_wlc(oldraw), parse_uxlc(newraw)
            counts, ann_old, ann_new, excluded = Counter(), Counter(), Counter(), Counter()
            for key in sorted(set(old) | set(new)):
                if key not in old or key not in new:
                    unmatched.append({"book": book, "chapter": key[0], "verse": key[1], "present_in": "WLC" if key in old else "UXLC"})
                    continue
                a, b = old[key], new[key]
                for r, acc in ((a, ann_old), (b, ann_new)):
                    acc.update(x["kind"] for x in r["annotations"])
                excluded.update(a["other_note_types"])
                flags = comparison(a, b)
                counts[flags["written_difference"] or "written_equal"] += 1
                counts["qere_payload_difference"] += flags["qere_payload_difference"]
                counts["qere_presence_or_word_count_difference"] += flags["qere_presence_or_word_count_difference"]
                counts["written_token_boundary_or_payload_difference"] += flags["written_token_boundary_or_payload_difference"]
                if any(flags.values()):
                    differences.append({"book": book, "chapter": key[0], "verse": key[1], **flags, "wlc": a, "uxlc": b})
                if flags["written_difference"] == "consonants":
                    canonical = ROOT / f"translation/ot/{book}/{key[0]:03}/{key[1]:03}.yaml"
                    row = {"book": book, "chapter": key[0], "verse": key[1], "path": str(canonical.relative_to(ROOT))}
                    if canonical.exists():
                        cr = canonical.read_bytes()
                        inputs[row["path"]] = digest(cr)
                        record = yaml.safe_load(cr)
                        current = normalized(record["source"]["text"], "consonants")
                        row.update(source_edition=record["source"]["edition"], source_text=record["source"]["text"], english=record["translation"]["text"],
                            matches_wlc_written=current == normalized("".join(w["text"] for w in a["written"]), "consonants"),
                            matches_uxlc_written=current == normalized("".join(w["text"] for w in b["written"]), "consonants"))
                    else:
                        row["canonical_file_missing"] = True
                    joins.append(row)
            books.append({"book": book, "wlc_verses": len(old), "uxlc_verses": len(new), "shared_labels": len(set(old) & set(new)),
                          "uxlc_member": member_name(book), "uxlc_member_sha256": digest(newraw), "counts": dict(counts),
                          "wlc_annotation_kinds": dict(ann_old), "uxlc_annotation_kinds": dict(ann_new), "wlc_non_qere_note_types": dict(excluded)})
    totals = Counter()
    for book in books:
        totals.update(book["counts"])
    return {"schema_version": "1.0.0", "checked_date": p["declared_date"], "protocol": p, "inputs": inputs,
            "archive_members": members, "summary": {"books": len(books), "shared_verse_labels": sum(b["shared_labels"] for b in books),
               "unmatched_verse_labels": len(unmatched), "difference_rows": len(differences), "pob_consonant_difference_joins": len(joins), "counts": dict(totals)},
            "books": books, "unmatched_labels": unmatched, "differences": differences, "pob_joins": joins,
            "interpretation": "Different digital transcriptions of the same codex tradition; no independent witness count, restored ink, historical priority or English improvement established."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build(args.archive)
    if args.write:
        with OUTPUT.open("x") as out:
            out.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    elif result != json.loads(OUTPUT.read_text()):
        raise ValueError("saved comparison drift")
    print(json.dumps(result["summary"], indent=2))
