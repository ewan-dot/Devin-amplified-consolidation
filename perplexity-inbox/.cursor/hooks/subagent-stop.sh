#!/usr/bin/env bash
# subagentStop — optional follow-up if subagent output looks incomplete
set -euo pipefail
INPUT=$(cat)
DIR="$(cd "$(dirname "$0")" && pwd)"

STATUS=""
if command -v jq >/dev/null 2>&1; then
  STATUS=$(echo "$INPUT" | jq -r '.status // .result // empty' 2>/dev/null || true)
fi

CHASE=$(python3 "$DIR/fork-checkpoint-chase.py" 2>/dev/null || echo '{}')
if [[ "$CHASE" != "{}" && -n "$CHASE" ]]; then
  echo "$CHASE"
  exit 0
fi

if echo "$STATUS" | grep -qiE 'fail|error|incomplete|blocked'; then
  echo '{"followup_message":"Subagent may be incomplete — retry with narrower scope or continue in main thread with the subagent summary only."}'
  exit 0
fi

echo '{}'
exit 0
