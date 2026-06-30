#!/bin/bash
# install.sh — wire the email-actioning-agent guards into git WITHOUT clobbering
# the repo's existing shared pre-commit (amplified_permissions). We append to the
# common hooks dir's pre-commit and add a pre-push health+test gate.
set -euo pipefail

PKG_DIR="$(cd "$(dirname "$0")/.." && pwd)"          # .../perplexity-inbox/email_actioning_agent
INBOX_DIR="$(cd "$PKG_DIR/.." && pwd)"               # .../perplexity-inbox
HOOKS_DIR="$(git -C "$INBOX_DIR" rev-parse --git-path hooks)"

echo "hooks dir: $HOOKS_DIR"

# --- pre-commit: run no_send_guard (append-safe) ---
PRECOMMIT="$HOOKS_DIR/pre-commit"
GUARD_LINE="python3 \"$PKG_DIR/hooks/no_send_guard.py\" || exit 1"
if [ -f "$PRECOMMIT" ] && grep -q "no_send_guard.py" "$PRECOMMIT"; then
  echo "pre-commit already has no_send_guard"
else
  { [ -f "$PRECOMMIT" ] || printf '#!/bin/bash\nset -e\n'; echo "# email_actioning_agent guard"; echo "$GUARD_LINE"; } >> "$PRECOMMIT"
  chmod +x "$PRECOMMIT"
  echo "appended no_send_guard to pre-commit"
fi

# --- pre-push: tests + health gate ---
PREPUSH="$HOOKS_DIR/pre-push"
cat > "$PREPUSH" <<EOF
#!/bin/bash
set -e
echo "[pre-push] email_actioning_agent tests + health gate"
( cd "$INBOX_DIR" && python3 -m pytest tests/test_email_actioning_agent.py -q )
( cd "$INBOX_DIR" && python3 -m email_actioning_agent health ) || {
  code=\$?; if [ "\$code" = "2" ]; then echo "[pre-push] health FAILED — blocking push"; exit 1; fi
  echo "[pre-push] health DEGRADED (\$code) — allowed, but check RUNBOOK"; }
EOF
chmod +x "$PREPUSH"
echo "wrote pre-push health+test gate"
echo "done."
