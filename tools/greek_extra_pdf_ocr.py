#!/usr/bin/env python3
"""greek_extra_pdf_ocr.py — shared OCR for local Greek extra-canonical PDFs.

This is the Group A companion to:

- `tools/transcribe_source.py` (Swete pages fetched from archive.org)
- `tools/2esdras/ocr_pipeline.py` (local PDFs, source-config driven)

Unlike those, this tool is intentionally generic: it OCRs *any* local
Greek PDF page range into `.txt` + `.meta.json` files using the shared
extra-canonical Greek prompt.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPT_PATH = REPO_ROOT / "tools" / "prompts" / "transcribe_greek_extra_generic.md"
PROMPT_VERSION = "greek_extra_generic_v1_2026-04-21"


def azure_endpoint() -> str:
    return os.environ.get(
        "AZURE_OPENAI_ENDPOINT",
        "https://eastus2.api.cognitive.microsoft.com",
    ).rstrip("/")


def azure_deployment() -> str:
    return os.environ.get(
        "AZURE_OPENAI_VISION_DEPLOYMENT_ID",
        "gpt-5-4-deployment",
    )


def azure_api_version() -> str:
    return os.environ.get(
        "AZURE_OPENAI_API_VERSION",
        "2025-04-01-preview",
    )


def parse_pages(page_arg: int | None, pages_arg: str | None) -> list[int]:
    if page_arg is not None:
        return [page_arg]
    if not pages_arg:
        raise ValueError("pass --page or --pages")
    pages: list[int] = []
    for chunk in pages_arg.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            start = int(a)
            end = int(b)
            if end < start:
                raise ValueError(f"descending page range: {chunk}")
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(chunk))
    return sorted(dict.fromkeys(pages))


def render_pdf_page(pdf_path: pathlib.Path, page: int, dpi: int) -> bytes:
    with tempfile.TemporaryDirectory(prefix="greek_extra_ocr_") as tmpdir:
        out_prefix = pathlib.Path(tmpdir) / f"page_{page}"
        cmd = [
            "pdftocairo",
            "-jpeg",
            "-jpegopt",
            "quality=95",
            "-r",
            str(dpi),
            "-f",
            str(page),
            "-l",
            str(page),
            "-singlefile",
            str(pdf_path),
            str(out_prefix),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return pathlib.Path(f"{out_prefix}.jpg").read_bytes()


def call_azure_vision(image_bytes: bytes, system_prompt: str, *, max_tokens: int) -> tuple[str, str]:
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("AZURE_OPENAI_API_KEY not set")

    b64 = base64.b64encode(image_bytes).decode("ascii")
    url = (
        f"{azure_endpoint()}/openai/deployments/{azure_deployment()}/chat/completions"
        f"?api-version={azure_api_version()}"
    )
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Transcribe this page following the instructions exactly."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ],
            },
        ],
        "temperature": 0.0,
        "max_completion_tokens": max_tokens,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            body = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Azure HTTP {exc.code}: {detail[:500]}") from exc
    return body["choices"][0]["message"]["content"], body.get("model", azure_deployment())


def output_stem(prefix: str, page: int) -> str:
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in prefix).strip("_")
    return f"{safe or 'greek_extra'}_p{page:04d}"


def process_page(
    *,
    pdf_path: pathlib.Path,
    page: int,
    out_dir: pathlib.Path,
    prompt: str,
    dpi: int,
    max_tokens: int,
    stem_prefix: str,
    book_hint: str,
) -> dict:
    image_bytes = render_pdf_page(pdf_path, page, dpi=dpi)
    image_sha = hashlib.sha256(image_bytes).hexdigest()
    started = time.time()
    text, model_id = call_azure_vision(image_bytes, prompt, max_tokens=max_tokens)
    duration = round(time.time() - started, 2)

    stem = output_stem(stem_prefix, page)
    (out_dir / f"{stem}.txt").write_text(text, encoding="utf-8")
    meta = {
        "source": "greek_extra_pdf",
        "book_hint": book_hint,
        "pdf_path": str(pdf_path),
        "page": page,
        "render_dpi": dpi,
        "image_sha256": image_sha,
        "image_bytes": len(image_bytes),
        "provenance_url": f"file://{pdf_path}#page={page}",
        "model": model_id,
        "deployment": azure_deployment(),
        "prompt_version": PROMPT_VERSION,
        "transcribed_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_seconds": duration,
        "output_chars": len(text),
    }
    (out_dir / f"{stem}.meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return meta


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pdf", required=True, help="Local PDF path")
    p.add_argument("--page", type=int, help="Single PDF page number")
    p.add_argument("--pages", help="Ranges, e.g. '120-125' or '120,132,140-142'")
    p.add_argument("--out-dir", required=True, help="Output directory for .txt/.meta.json files")
    p.add_argument("--book-hint", required=True, help="Human-readable source hint")
    p.add_argument("--stem-prefix", default="greek_extra", help="Output filename prefix")
    p.add_argument("--dpi", type=int, default=300, help="Render DPI (default 300)")
    p.add_argument("--concurrency", type=int, default=1)
    p.add_argument("--max-completion-tokens", type=int, default=7000)
    p.add_argument("--skip-existing", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    pdf_path = pathlib.Path(args.pdf).resolve()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    try:
        pages = parse_pages(args.page, args.pages)
    except ValueError as exc:
        p.error(str(exc))

    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    out_dir = pathlib.Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    def already_done(page: int) -> bool:
        stem = output_stem(args.stem_prefix, page)
        return (out_dir / f"{stem}.txt").exists() and (out_dir / f"{stem}.meta.json").exists()

    todo = [pg for pg in pages if not (args.skip_existing and already_done(pg))]
    skipped = len(pages) - len(todo)

    print(f"📘 book:   {args.book_hint}")
    print(f"📄 pdf:    {pdf_path}")
    print(f"📂 out:    {out_dir}")
    print(f"📑 pages:  {', '.join(str(pg) for pg in pages)}")
    if skipped:
        print(f"↷ skipping {skipped} page(s) already on disk")
    if args.dry_run:
        print("🧪 dry run only — no OCR requests will be sent")
        return 0

    results: dict[int, tuple[dict | None, str | None]] = {}

    def worker(page: int):
        try:
            meta = process_page(
                pdf_path=pdf_path,
                page=page,
                out_dir=out_dir,
                prompt=prompt,
                dpi=args.dpi,
                max_tokens=args.max_completion_tokens,
                stem_prefix=args.stem_prefix,
                book_hint=args.book_hint,
            )
            return page, meta, None
        except Exception as exc:  # noqa: BLE001
            return page, None, f"{type(exc).__name__}: {exc}"

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as ex:
        futs = [ex.submit(worker, pg) for pg in todo]
        for fut in as_completed(futs):
            page, meta, err = fut.result()
            results[page] = (meta, err)
            if err:
                print(f"  FAIL p{page}: {err[:300]}", flush=True)
            else:
                print(
                    f"  OK   p{page:>4d}  {meta['duration_seconds']:>5.1f}s  "
                    f"{meta['output_chars']:>6d} chars",
                    flush=True,
                )

    n_ok = sum(1 for meta, err in results.values() if err is None)
    n_fail = len(results) - n_ok
    print(f"\ndone: {n_ok} ok, {n_fail} failed, {skipped} skipped; output in {out_dir}", flush=True)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
