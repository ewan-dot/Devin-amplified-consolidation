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

find_fork_flow() {
  local dir="$1"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/perplexity-inbox/harness/fork_flow.py" ]]; then
      echo "$dir/perplexity-inbox/harness/fork_flow.py"
      return
    fi
    if [[ -f "$dir/harness/fork_flow.py" ]]; then
      echo "$dir/harness/fork_flow.py"
      return
    fi
    dir=$(dirname "$dir")
  done
}

if [[ -n "${FORK_CONTRACT:-}" ]]; then
  CONTRACT_DIR=$(cd "$(dirname "$FORK_CONTRACT")" && pwd)
  FORK_FLOW=$(find_fork_flow "$CONTRACT_DIR")
  if [[ -n "$FORK_FLOW" ]]; then
    if ! RESULT=$(python3 "$FORK_FLOW" validate "$FORK_CONTRACT" --require-existing-paths 2>&1); then
      python3 -c "import json, sys; print(json.dumps({'followup_message': 'Fork checkpoint missing: ' + sys.argv[1].strip()}))" "$RESULT"
      exit 0
    fi
  fi
fi

if echo "$STATUS" | grep -qiE 'fail|error|incomplete|blocked'; then
  echo '{"followup_message":"Subagent may be incomplete — retry with narrower scope or continue in main thread with the subagent summary only."}'
  exit 0
fi

echo '{}'
exit 0
