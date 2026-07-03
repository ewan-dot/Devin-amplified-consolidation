#!/usr/bin/env bash
# =============================================================================
# STAGED open-door wrapper for beforeShellExecution. NOT WIRED.
# Activation = copy this over ~/.cursor/hooks/before-shell-execution.sh
# (see ACTIVATION.md). Chains: door check -> existing token-bomb guard.
# Fail-open at every step; default OPEN_DOOR_MODE=scaffold = no behaviour change.
# =============================================================================
set -uo pipefail
INPUT=$(cat)
OPEN_DOOR_HOME="${OPEN_DOOR_HOME:-$HOME/ingestion-to-research-pipe/perplexity-inbox/open_door_runtime}"
GUARD="$(dirname "$0")/pre-bash-guard.py"

DOUT=$(printf '%s' "$INPUT" | python3 "$OPEN_DOOR_HOME/hook_adapter.py" shell 2>/dev/null || echo '{"permission":"allow"}')

# Door says deny -> emit and stop.
if printf '%s' "$DOUT" | grep -q '"permission"[[:space:]]*:[[:space:]]*"deny"'; then
  printf '%s\n' "$DOUT"; exit 0
fi
# Door nudge -> door message wins (avoid double-allow collision).
if printf '%s' "$DOUT" | grep -q 'additional_context'; then
  printf '%s\n' "$DOUT"; exit 0
fi
# Otherwise preserve the existing token-bomb guard.
if [[ -f "$GUARD" ]]; then
  printf '%s' "$INPUT" | python3 "$GUARD"
else
  printf '%s\n' "$DOUT"
fi
