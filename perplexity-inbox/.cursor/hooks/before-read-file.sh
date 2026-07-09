#!/usr/bin/env bash
# =============================================================================
# LIVE open-door wrapper for beforeReadFile (activated 2026-07-03).
# Profile: door-scope = NUDGE only (blocks nothing); deny-core secret probe
# still applies. Chains: door check -> original noisy-path nudge
# (before-read-file.orig.sh). Fail-open everywhere. NO failClosed in hooks.json
# on purpose (read boundary is .cursorignore, not this hook).
# Backups: before-read-file.sh.pre-door.<ts>.bak ; chain: before-read-file.orig.sh
# =============================================================================
set -uo pipefail
INPUT=$(cat)
# Hardcoded because Cursor hook processes do not inherit the interactive shell env.
OPEN_DOOR_HOME="${OPEN_DOOR_HOME:-/Users/ewansair/_worktrees/open-door-phase0/perplexity-inbox/open_door_runtime}"
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
