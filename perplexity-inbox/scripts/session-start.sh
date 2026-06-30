#!/usr/bin/env bash
# session-start.sh — deterministic fleet session opening (no LLM).
# Exit: 0=proceed, 1=warn, 2=halt (matches unified_sensor.signal_reader)
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PERMS="skip"
SENSOR_CMD=""
FINAL_EXIT=0

echo "session-start: root=$ROOT"

# 1. Optional standing-grants self-test
if [[ -f "$ROOT/amplified_permissions.py" ]]; then
  echo "--- amplified_permissions (self-test) ---"
  if python3 "$ROOT/amplified_permissions.py"; then
    PERMS="pass"
  else
    PERMS="fail"
    echo "permissions: FAIL"
    echo '{"step":"session-start","permissions":"fail","verdict":"halt","exit_code":2}'
    exit 2
  fi
fi

# 2. Fleet sensor — monitor first; local-only if output is not valid verdict JSON
SIGNALS="$(mktemp "${TMPDIR:-/tmp}/session-start-signals.XXXXXX.json")"
trap 'rm -f "$SIGNALS"' EXIT

sensor_valid() {
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get('verdict') in ('proceed','warn','halt') else 1)" "$1" 2>/dev/null
}

run_sensor() {
  local cmd=("$@")
  SENSOR_CMD="${cmd[*]}"
  "${cmd[@]}" >"$SIGNALS" 2>/dev/null
}

echo "--- fleet sensor ---"
run_sensor python3 "$ROOT/monitor.py" --signals-only || true

if ! sensor_valid "$SIGNALS"; then
  echo "monitor unavailable — falling back to unified_sensor --local-only"
  run_sensor python3 -m unified_sensor --local-only || true
fi

if ! sensor_valid "$SIGNALS"; then
  echo "sensor collection failed"
  cat "$SIGNALS" >&2 || true
  echo '{"step":"session-start","permissions":"'"$PERMS"'","verdict":"halt","reason":"sensor collection failed","exit_code":2}'
  exit 2
fi

# Show raw sensor JSON (no interpretation)
cat "$SIGNALS"
echo

VERDICT="$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('verdict','proceed'))" "$SIGNALS" 2>/dev/null || echo proceed)"
REASON="$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('reason',''))" "$SIGNALS" 2>/dev/null || echo "")"

case "$VERDICT" in
  halt) FINAL_EXIT=2 ;;
  warn) FINAL_EXIT=1 ;;
  *)    FINAL_EXIT=0 ;;
esac

# 3. Inbox paths — print only, no interpretation
echo "--- INBOX-STATUS ---"
echo "path: $ROOT/docs/INBOX-STATUS.md"
if [[ -f "$ROOT/docs/INBOX-STATUS.md" ]]; then
  head -n 40 "$ROOT/docs/INBOX-STATUS.md"
else
  echo "(missing)"
fi

echo "--- INBOX-INDEX (latest) ---"
LATEST_INDEX="$(ls -t "$ROOT"/INBOX-INDEX__*.md 2>/dev/null | head -1 || true)"
if [[ -n "$LATEST_INDEX" ]]; then
  echo "path: $LATEST_INDEX"
  head -n 30 "$LATEST_INDEX"
else
  echo "path: (none found)"
fi

# 4. Verdict line — copy to Vellum intent post
python3 -c "
import json, sys
print('VERDICT=' + sys.argv[1] + ' reason=' + sys.argv[2] + ' exit=' + sys.argv[3])
print(json.dumps({
    'step': 'session-start',
    'permissions': sys.argv[4],
    'sensor_cmd': sys.argv[5],
    'verdict': sys.argv[1],
    'reason': sys.argv[2],
    'inbox_status': 'docs/INBOX-STATUS.md',
    'inbox_index': sys.argv[6] or None,
    'exit_code': int(sys.argv[3]),
}))
" "$VERDICT" "$REASON" "$FINAL_EXIT" "$PERMS" "$SENSOR_CMD" "${LATEST_INDEX#$ROOT/}"

exit "$FINAL_EXIT"
