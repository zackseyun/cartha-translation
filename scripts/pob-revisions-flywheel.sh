#!/usr/bin/env bash
# Compatibility entry point: explicit/batch-triggered only; no launchd timer.
# Default: request one refresh, skip unchanged inputs, publish only on clean main.
# --background returns immediately after queuing a completed batch.
# On battery requests remain pending until another batch or a manual AC retry.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="${POB_REVISIONS_REPO:-$(cd "$SCRIPT_DIR/.." && pwd)}"
PYTHON="${POB_REVISIONS_PYTHON:-python3}"
if [[ -z "${POB_REVISIONS_PYTHON:-}" && -x /opt/homebrew/bin/python3 ]]; then
  PYTHON=/opt/homebrew/bin/python3
fi
exec "$PYTHON" "$REPO/tools/revisions_refresh.py" --repo "$REPO" --request --publish "$@"
