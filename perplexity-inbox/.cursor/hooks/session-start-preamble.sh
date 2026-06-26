#!/usr/bin/env bash
# sessionStart — compact git/task preamble (≤800 chars)
set -euo pipefail
cat > /dev/null

PROJECT_DIR="${CURSOR_PROJECT_DIR:-${PWD}}"
PREAMBLE=""
{
  echo "branch: $(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null || echo none)"
  echo "recent:"
  git -C "$PROJECT_DIR" log --oneline -3 2>/dev/null || true
  for TASK_FILE in "$PROJECT_DIR/.cursor/CURRENT_TASK" "${HOME}/.cursor/CURRENT_TASK"; do
    if [[ -f "$TASK_FILE" ]]; then
      echo "task:"
      head -c 400 "$TASK_FILE"
      break
    fi
  done
} > /tmp/cursor-preamble.$$.txt 2>/dev/null || true

if [[ -s /tmp/cursor-preamble.$$.txt ]]; then
  PREAMBLE=$(head -c 800 /tmp/cursor-preamble.$$.txt)
fi
rm -f /tmp/cursor-preamble.$$.txt

if [[ -n "$PREAMBLE" ]] && command -v jq >/dev/null 2>&1; then
  jq -n --arg ctx "$PREAMBLE" '{additional_context: ("[session-start] " + $ctx)}'
else
  echo '{}'
fi
exit 0
