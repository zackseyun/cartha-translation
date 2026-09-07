#!/usr/bin/env python3
"""Run one blinded pilot provider through an already authenticated local CLI.

Never retries an authorization failure or substitutes a model. Raw CLI envelopes
stay gitignored because they can contain account/session metadata. Only the
sanitized proposal and provenance are candidates for version control.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from pilot import DEFAULT_PILOT, MODELS, digest, read_json, validate_result, write_json


def parse_claude(events: list[dict], exit_code: int) -> tuple[str, str | None, dict | None, str | None]:
    effective = next((event.get("model") for event in events
                      if event.get("type") == "system" and event.get("subtype") == "init"), None)
    final = next((event for event in reversed(events) if event.get("type") == "result"), {})
    # Claude can report subtype=success while is_error=true and process exit=1.
    if exit_code or final.get("is_error") or final.get("subtype") != "success":
        error = final.get("result") or "; ".join(final.get("errors") or []) or f"CLI exit {exit_code}"
        state = "blocked" if "disabled" in error or "authentication" in error.lower() else "failed"
        return state, effective, None, error
    result = final.get("structured_output")
    if not isinstance(result, dict):
        return "failed", effective, None, "No structured transcription returned"
    return "succeeded", effective, result, None


def json_events(path: Path) -> list[dict]:
    events = []
    for line in path.read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def run(pilot: Path, provider: str, executable: str, timeout: int, replace: bool,
        effort: str = "high") -> dict:
    output = pilot / "passes" / f"{provider}.json"
    if output.exists() and not replace:
        raise ValueError(f"Existing pass protected: {output}; use --replace explicitly after reviewing it")
    model = MODELS[provider]
    prompt = (pilot / "prompt.txt").read_text()
    regions = read_json(pilot / "regions.json")["regions"]
    crops = [pilot / "crops" / f"{region['id']}.png" for region in regions]
    schema = read_json(pilot / "response.schema.json")
    for path, region in zip(crops, regions):
        if digest(path) != region["crop_sha256"]:
            raise ValueError("Crop hash mismatch before model call")
    started = datetime.now(timezone.utc)
    raw = pilot / "raw" / (started.strftime("%Y%m%dT%H%M%S%fZ") + "-" + provider)
    raw.mkdir(parents=True)
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f"pob-dss-{provider}-") as temporary:
        if provider == "openai":
            command = [
                executable, "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
                "-s", "read-only", "-C", temporary, "-m", model,
                "-c", f'model_reasoning_effort="{effort}"',
                "-c", "project_doc_max_bytes=0", "-c", 'web_search="disabled"',
                "-c", 'developer_instructions="Read only the attached manuscript images. '
                'Do not call tools, read other files, or access memory. Return the requested JSON."',
                "--disable", "shell_tool", "--disable", "memories", "--disable", "multi_agent",
                "--disable", "browser_use", "--disable", "computer_use",
                "--disable", "image_generation", "--disable", "view_image",
                "--output-schema", str(pilot / "response.schema.json"),
                "--json", "-o", str(raw / "final.json"),
            ]
            for image in crops:
                command.extend(["-i", str(image)])
            command.append("-")
            stdin = prompt
        else:
            command = [
                executable, "-p", "--safe-mode", "--no-session-persistence", "--tools", "",
                "--model", model, "--effort", effort, "--input-format", "stream-json",
                "--output-format", "stream-json", "--verbose", "--json-schema", json.dumps(schema),
                "--system-prompt", "You are a manuscript image transcription model. Follow only the "
                "current user request. Never use external sources or other conversations.",
            ]
            content = [{"type": "text", "text": prompt}] + [
                {"type": "image", "source": {
                    "type": "base64", "media_type": "image/png",
                    "data": base64.b64encode(image.read_bytes()).decode(),
                }} for image in crops
            ]
            stdin = json.dumps({"type": "user", "message": {"role": "user", "content": content}}) + "\n"
        with (raw / "stdout.jsonl").open("w") as out, (raw / "stderr.log").open("w") as err:
            try:
                completed = subprocess.run(command, input=stdin, text=True, stdout=out, stderr=err,
                                           cwd=temporary, timeout=timeout)
                code = completed.returncode
            except subprocess.TimeoutExpired:
                code = 124
            except OSError as exc:
                err.write(str(exc))
                code = 127
    events = json_events(raw / "stdout.jsonl")
    tools = [event["item"]["type"] for event in events
             if event.get("type") == "item.started" and event.get("item", {}).get("type") != "agent_message"]
    if provider == "anthropic":
        status, effective, result, error = parse_claude(events, code)
        identity_basis = "CLI initialization event; inference only confirmed if a successful response exists"
    elif code == 0 and (raw / "final.json").exists():
        status, effective, error = "succeeded", model, None
        try:
            result = read_json(raw / "final.json")
        except json.JSONDecodeError:
            status, result, error = "failed", None, "CLI final response is not valid JSON"
        identity_basis = "Explicit --model selection; no fallback configured; successful CLI completion"
    else:
        status, effective, result, error = "failed", None, None, f"CLI exit {code}; inspect private raw logs"
        identity_basis = "No successful inference"
    if status == "succeeded":
        try:
            if effective != model:
                raise ValueError("Requested model was not the effective model")
            validate_result(result, [region["id"] for region in regions], response_schema=schema)
        except ValueError as exc:
            status, result, error = "failed", None, str(exc)
    record = {
        "schema_version": "1.0.0", "provider": provider, "requested_model": model,
        "reasoning_effort": effort,
        "effective_model": effective, "model_identity_basis": identity_basis,
        "status": status, "error": error, "started_at": started.isoformat(),
        "duration_seconds": round(time.monotonic() - start, 2), "exit_code": code,
        "prompt_sha256": digest(pilot / "prompt.txt"),
        "crop_sha256": [digest(image) for image in crops],
        "isolation": "Fresh process and empty temporary working directory; no other pass or edition supplied",
        "tool_events": tools, "raw_log_sha256": digest(raw / "stdout.jsonl"),
        "result": result, "publication_action": "none",
    }
    write_json(output, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--provider", choices=list(MODELS), required=True)
    parser.add_argument("--executable", help="Explicit CLI path; no software is installed or repaired")
    parser.add_argument("--timeout", type=int, default=480)
    parser.add_argument("--effort", choices=["low", "medium", "high"], default="high")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    executable = args.executable or os.environ.get("CODEX_CLI_PATH" if args.provider == "openai" else "CLAUDE_CLI_PATH")
    executable = executable or shutil.which("codex" if args.provider == "openai" else "claude")
    if not executable:
        parser.error("No CLI found; provide --executable")
    result = run(args.pilot.resolve(), args.provider, executable, args.timeout, args.replace, args.effort)
    print(f"{args.provider}: {result['status']}; {result.get('error') or 'proposal saved'}")
    return 0 if result["status"] == "succeeded" else 2


if __name__ == "__main__":
    raise SystemExit(main())
