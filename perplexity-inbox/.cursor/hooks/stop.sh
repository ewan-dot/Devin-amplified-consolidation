#!/usr/bin/env bash
# stop — compact nudge + self-compound SSOT check + seat-close log
set -euo pipefail

LOG="${HOME}/.vellum/stop.log"
mkdir -p "$(dirname "$LOG")"
echo "stop $(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"$LOG"

DIR="$(dirname "$0")"
INPUT=$(cat)

compact=$(echo "$INPUT" | python3 "$DIR/stop-compact-nudge.py")
compound=$(echo "$INPUT" | python3 "$DIR/stop-self-compound-check.py")
vellum=$(echo "$INPUT" | python3 "$DIR/stop-vellum-actual.py")
chase=$(python3 "$DIR/fork-checkpoint-chase.py" || echo '{}')

python3 - "$compact" "$compound" "$vellum" "$chase" <<'PY'
import json, sys
msgs = []
for raw in sys.argv[1:]:
    try:
        m = json.loads(raw).get("followup_message")
        if m:
            msgs.append(m)
    except Exception:
        pass
print(json.dumps({"followup_message": " ".join(msgs)}) if msgs else "{}")
PY
