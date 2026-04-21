#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${TARGET:-12}"
STOP_FLAG="/tmp/cob-phase9-stop"
LOG_DIR="/tmp/cob-phase9-workers"
CHECK_INTERVAL_SECONDS="${CHECK_INTERVAL_SECONDS:-20}"
SPAWN_STAGGER_SECONDS="${SPAWN_STAGGER_SECONDS:-2}"
PHASE="phase8"
MODEL="${MODEL:-gpt-5.4}"
PYTHON_BIN="${PYTHON_BIN:-$REPO_ROOT/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3)"
fi
mkdir -p "$LOG_DIR"
cd "$REPO_ROOT"
fetch_azure_key() {
  if [[ -z "${AZURE_OPENAI_API_KEY:-}" ]]; then
    AZURE_OPENAI_API_KEY="$(aws secretsmanager get-secret-value \
      --secret-id cartha-azure-openai-key --region us-west-2 \
      --query SecretString --output text \
      | python3 -c "import json,sys; print(json.load(sys.stdin)['api_key'])")"
    export AZURE_OPENAI_API_KEY
    export AZURE_OPENAI_ENDPOINT="https://eastus2.api.cognitive.microsoft.com"
    export AZURE_OPENAI_DEPLOYMENT_ID="gpt-5-4-deployment"
    export AZURE_OPENAI_API_VERSION="2025-04-01-preview"
  fi
}
declare -a SLOTS=(
  "phase9-wis-w1 /private/tmp/cartha-translation-phase9-wis-w1"
  "phase9-wis-w2 /private/tmp/cartha-translation-phase9-wis-w2"
  "phase9-wis-w3 /private/tmp/cartha-translation-phase9-wis-w3"
  "phase9-wis-w9 /private/tmp/cartha-translation-phase9-wis-w9"
  "phase9-wis-w10 /private/tmp/cartha-translation-phase9-wis-w10"
  "phase9-wis-w11 /private/tmp/cartha-translation-phase9-wis-w11"
  "phase9-deut-w4 /private/tmp/cartha-translation-phase9-deut-w4"
  "phase9-deut-w5 /private/tmp/cartha-translation-phase9-deut-w5"
  "phase9-deut-w6 /private/tmp/cartha-translation-phase9-deut-w6"
  "phase9-wis-w4 /private/tmp/cartha-translation-phase9-wis-w4"
  "phase9-wis-w5 /private/tmp/cartha-translation-phase9-wis-w5"
  "phase9-wis-w6 /private/tmp/cartha-translation-phase9-wis-w6"
  "phase9-wis-w7 /private/tmp/cartha-translation-phase9-wis-w7"
  "phase9-wis-w8 /private/tmp/cartha-translation-phase9-wis-w8"
  "phase9-wis-w12 /private/tmp/cartha-translation-phase9-wis-w12"
  "phase9-wis-w13 /private/tmp/cartha-translation-phase9-wis-w13"
  "phase9-wis-w14 /private/tmp/cartha-translation-phase9-wis-w14"
  "phase9-wis-w15 /private/tmp/cartha-translation-phase9-wis-w15"
)
is_alive() {
  local wid="$1"
  pgrep -f "tools/chapter_worker.py .*--worker-id $wid .*--phase $PHASE" >/dev/null 2>&1
}
count_alive() {
  pgrep -af "tools/chapter_worker.py .*--phase $PHASE" | wc -l | tr -d ' '
}
spawn_slot() {
  local wid="$1"
  local wt="$2"
  [[ -d "$wt" ]] || return 0
  fetch_azure_key
  nohup env \
    AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
    AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
    AZURE_OPENAI_DEPLOYMENT_ID="$AZURE_OPENAI_DEPLOYMENT_ID" \
    AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" \
    "$PYTHON_BIN" "$REPO_ROOT/tools/chapter_worker.py" \
      --coord-root "$REPO_ROOT" \
      --worker-id "$wid" \
      --phase "$PHASE" \
      --backend azure-openai \
      --model "$MODEL" \
      --max-jobs 100000 \
      --stop-when-empty \
    > "$LOG_DIR/$wid.log" 2>&1 &
  echo "[$(date +%H:%M:%S)] spawned $wid -> $wt"
}
echo "[$(date +%H:%M:%S)] supervise_phase9_workers starting; target=$TARGET phase=$PHASE"
echo " stop with: touch $STOP_FLAG"
while true; do
  if [[ -f "$STOP_FLAG" ]]; then
    echo "[$(date +%H:%M:%S)] stop flag present; exiting (existing workers keep running)"
    rm -f "$STOP_FLAG"
    exit 0
  fi
  alive="$(count_alive)"
  if (( alive < TARGET )); then
    need=$((TARGET - alive))
    echo "[$(date +%H:%M:%S)] alive=$alive target=$TARGET; need=$need"
    for slot in "${SLOTS[@]}"; do
      wid="${slot%% *}"
      wt="${slot#* }"
      if is_alive "$wid"; then
        continue
      fi
      spawn_slot "$wid" "$wt"
      need=$((need - 1))
      [[ $need -le 0 ]] && break
      sleep "$SPAWN_STAGGER_SECONDS"
    done
  fi
  sleep "$CHECK_INTERVAL_SECONDS"
done
