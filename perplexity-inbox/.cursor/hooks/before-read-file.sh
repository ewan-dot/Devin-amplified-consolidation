#!/usr/bin/env bash
# beforeReadFile — nudge noisy paths; fail-open (push door)
set -euo pipefail
INPUT=$(cat)

PATH_VAL=""
if command -v jq >/dev/null 2>&1; then
  PATH_VAL=$(echo "$INPUT" | jq -r '.path // .file_path // .tool_input.path // empty' 2>/dev/null || true)
fi

if [[ -z "$PATH_VAL" ]]; then
  echo '{"permission":"allow"}'
  exit 0
fi

case "$PATH_VAL" in
  *.lock|*.min.js|*.map|*/node_modules/*|*/__pycache__/*|*/.pytest_cache/*)
    echo '{"permission":"allow","agent_message":"beforeReadFile: noisy path — prefer rg/head on a slice; proceed if you need the full file.","additional_context":"[read-nudge] Token-heavy path — rg/head first unless you deliberately need the whole file."}'
    exit 0
    ;;
esac

echo '{"permission":"allow"}'
exit 0
