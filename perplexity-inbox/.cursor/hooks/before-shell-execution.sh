#!/usr/bin/env bash
# =============================================================================
# LIVE open-door wrapper for beforeShellExecution (activated 2026-07-03).
# Profile: deny-core ON (fail-closed core: secrets / git push / Red-core rm-rf),
# door-scope = NUDGE only (blocks nothing). Chains: door check -> existing
# token-bomb guard (pre-bash-guard.py). Fail-open at every step for door-scope.
# Backups: before-shell-execution.sh.pre-door.<ts>.bak
# Rollback: cp before-shell-execution.sh.pre-door.<ts>.bak before-shell-execution.sh
# =============================================================================
set -uo pipefail
INPUT=$(cat)
# Hardcoded because Cursor hook processes do not inherit the interactive shell env.
# Points at the Phase-1 worktree runtime (pre-merge). Update if the runtime moves.
OPEN_DOOR_HOME="${OPEN_DOOR_HOME:-/Users/ewansair/_worktrees/open-door-phase0/perplexity-inbox/open_door_runtime}"
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
