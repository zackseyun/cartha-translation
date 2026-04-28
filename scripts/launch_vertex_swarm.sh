#!/usr/bin/env bash
# launch_vertex_swarm.sh — fan out N gemini_review_workers all pointed at
# Gemini 3.1 Pro Preview via Vertex AI on the credit-funded project
# `cartha-bible-vertex`. Each worker claims jobs from the SQLite review
# queue (claim is row-level via the existing locking) and stops when the
# queue drains.
#
# Usage:
#   bash scripts/launch_vertex_swarm.sh                  # 8 workers, default strategy
#   N=16 bash scripts/launch_vertex_swarm.sh             # 16 workers
#   STRATEGY=vertex_gap_closure_2026_04 bash scripts/launch_vertex_swarm.sh
#
# Logs:    /tmp/vertex-swarm-vN.log per worker
# Stop:    pkill -f gemini_review_worker.py
# Status:  python3 tools/gemini_review_queue.py status

set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N="${N:-8}"
STRATEGY="${STRATEGY:-vertex_gap_closure_2026_04}"
SA="${GOOGLE_APPLICATION_CREDENTIALS:-/Users/zackseyun/.config/cartha/gemini-vertex-cbv.json}"
LOC="${GCP_LOCATION:-global}"
MODEL="${MODEL_OVERRIDE:-gemini-3.1-pro-preview}"

if [ ! -f "$SA" ]; then
  echo "ERROR: SA key not found at $SA" >&2
  exit 1
fi

cd "$REPO_ROOT"
echo "Launching $N parallel Vertex workers"
echo "  strategy: $STRATEGY"
echo "  model:    $MODEL"
echo "  project:  $(python3 -c "import json; print(json.load(open('$SA'))['project_id'])")"
echo "  endpoint: $LOC"

for i in $(seq 1 "$N"); do
  worker_id="v$i"
  log="/tmp/vertex-swarm-${worker_id}.log"
  GOOGLE_APPLICATION_CREDENTIALS="$SA" \
  GCP_LOCATION="$LOC" \
  nohup python3 tools/gemini_review_worker.py \
    --worker-id "$worker_id" \
    --strategy "$STRATEGY" \
    --model-override "$MODEL" \
    --stop-when-empty \
    --sleep 0.5 \
    > "$log" 2>&1 &
  pid=$!
  echo "  spawned $worker_id pid=$pid log=$log"
done

echo
echo "Watch combined progress:"
echo "  tail -f /tmp/vertex-swarm-v*.log"
echo "Queue status:"
echo "  python3 tools/gemini_review_queue.py status"
