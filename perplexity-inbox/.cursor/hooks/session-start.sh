#!/usr/bin/env bash
# Cursor sessionStart hook — Vellum login + fleet sensor (perplexity-inbox)
# Reads JSON from stdin (Cursor hook protocol), returns {} on stdout.
# Side-effects go to ~/.vellum/startup.log — never pollutes the terminal.

cat > /dev/null

export CURSOR_SESSION=1
LOG="${HOME}/.vellum/startup.log"
FLEET_START="${HOME}/ingestion-to-research-pipe/perplexity-inbox/scripts/session-start.sh"

# Vellum login — non-blocking
if [ -x "${HOME}/.vellum/startup-login.sh" ]; then
  "${HOME}/.vellum/startup-login.sh" &
fi

# Fleet session-start — background, logged; hook returns immediately (10s Cursor timeout)
if [ -x "$FLEET_START" ]; then
  (
    echo "=== fleet session-start $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
    "$FLEET_START"
    echo "=== fleet session-start exit: $? ==="
  ) >>"$LOG" 2>&1 &
else
  echo "fleet session-start: missing $FLEET_START" >>"$LOG"
fi

echo '{}'
exit 0
