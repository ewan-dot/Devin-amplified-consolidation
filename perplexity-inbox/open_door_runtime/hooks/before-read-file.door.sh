#!/usr/bin/env bash
# =============================================================================
# STAGED open-door wrapper for beforeReadFile. NOT WIRED.
# Activation = back up the live script to before-read-file.orig.sh, then copy
# this over ~/.cursor/hooks/before-read-file.sh (see ACTIVATION.md).
# Chains: door check -> original noisy-path nudge. Fail-open everywhere.
# =============================================================================
set -uo pipefail
INPUT=$(cat)
OPEN_DOOR_HOME="${OPEN_DOOR_HOME:-$HOME/ingestion-to-research-pipe/perplexity-inbox/open_door_runtime}"
ORIG="$(dirname "$0")/before-read-file.orig.sh"

DOUT=$(printf '%s' "$INPUT" | python3 "$OPEN_DOOR_HOME/hook_adapter.py" read 2>/dev/null || echo '{"permission":"allow"}')

if printf '%s' "$DOUT" | grep -q '"permission"[[:space:]]*:[[:space:]]*"deny"'; then
  printf '%s\n' "$DOUT"; exit 0
fi
if printf '%s' "$DOUT" | grep -q 'additional_context'; then
  printf '%s\n' "$DOUT"; exit 0
fi
if [[ -f "$ORIG" ]]; then
  printf '%s' "$INPUT" | bash "$ORIG"
else
  echo '{"permission":"allow"}'
fi
