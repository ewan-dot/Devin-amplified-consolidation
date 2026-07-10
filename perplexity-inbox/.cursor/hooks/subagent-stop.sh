#!/usr/bin/env bash
# subagentStop — optional follow-up if subagent output looks incomplete
set -euo pipefail
INPUT=$(cat)

STATUS=""
SUMMARY=""
if command -v jq >/dev/null 2>&1; then
  STATUS=$(echo "$INPUT" | jq -r '.status // .result // empty' 2>/dev/null || true)
  SUMMARY=$(echo "$INPUT" | jq -r '.summary // .output // empty' 2>/dev/null || true)
fi

if [[ -n "${FORK_CONTRACT:-}" ]]; then
  ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
  if ! RESULT=$(python3 "$ROOT/harness/fork_flow.py" validate "$FORK_CONTRACT" --require-existing-paths 2>&1); then
    MESSAGE=$(printf '%s' "$RESULT" | tr '\n' ' ' | sed 's/"/\\"/g')
    echo "{\"followup_message\":\"Fork checkpoint missing: ${MESSAGE}\"}"
    exit 0
  fi
fi

if echo "$STATUS" | grep -qiE 'fail|error|incomplete|blocked'; then
  echo '{"followup_message":"Subagent may be incomplete — retry with narrower scope or continue in main thread with the subagent summary only."}'
  exit 0
fi

echo '{}'
exit 0
