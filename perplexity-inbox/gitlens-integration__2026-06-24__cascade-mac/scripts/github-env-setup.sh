#!/usr/bin/env bash
# github-env-setup.sh — one-shot setup for GITHUB_TOKEN
#
# Fixes: GitLens (and other tools) can't authenticate to GitHub because
# 1Password SSH agent is locked and VS Code secret storage needs keychain.
#
# What this does:
#   1. Reads GITHUB_TOKEN from gh CLI (uses macOS Keychain, which IS unlocked)
#   2. Adds the export to ~/.zshrc (terminal sessions)
#   3. Installs a LaunchAgent that sets GITHUB_TOKEN at user-environment level
#      so Dock-launched VS Code also gets it
#
# Safe to re-run — all steps are idempotent.
#
# After running: restart VS Code. GitLens → Home → "GitHub is connected".

set -euo pipefail

GH=/opt/homebrew/bin/gh
ZSHRC="${HOME}/.zshrc"
TOKEN_FILE="${HOME}/.config/cascade-mac/github_token"
PLIST_SRC="$(dirname "$0")/../plists/com.cascade-mac.github-token.plist"
PLIST_DST="${HOME}/Library/LaunchAgents/com.cascade-mac.github-token.plist"

echo "=== GitHub Token Environment Setup ==="
echo ""

# --- 1. Verify gh can return a token
echo "[1/4] Getting token from gh CLI (macOS Keychain)..."
TOKEN=$("${GH}" auth token 2>/dev/null) || {
  echo "" >&2
  echo "ERROR: /opt/homebrew/bin/gh auth token failed." >&2
  echo "  Try: /opt/homebrew/bin/gh auth login --web" >&2
  exit 1
}
echo "      ✓ token obtained (${#TOKEN} chars)"

# --- 2. Cache token to file (fallback for scripts that can't run gh)
echo "[2/4] Caching token to ${TOKEN_FILE}..."
mkdir -p "$(dirname "${TOKEN_FILE}")"
printf '%s' "${TOKEN}" > "${TOKEN_FILE}"
chmod 600 "${TOKEN_FILE}"
echo "      ✓ ${TOKEN_FILE} (mode 600)"

# --- 3. Add to ~/.zshrc if not already there
echo "[3/4] Checking ~/.zshrc..."
ZSHRC_MARKER="# GITHUB_TOKEN — cascade-mac github-env-setup"
if grep -qF "${ZSHRC_MARKER}" "${ZSHRC}" 2>/dev/null; then
  echo "      skip — already present in ${ZSHRC}"
else
  cat >> "${ZSHRC}" << 'ZSHBLOCK'

# GITHUB_TOKEN — cascade-mac github-env-setup
# Reads token from macOS Keychain via gh CLI (bypasses 1Password SSH agent).
# GitLens and other GitHub API tools pick this up from the environment.
export GITHUB_TOKEN="$(/opt/homebrew/bin/gh auth token 2>/dev/null)"
ZSHBLOCK
  echo "      ✓ export added to ${ZSHRC}"
fi

# --- 4. Install LaunchAgent (sets env for all user apps including Dock-launched VS Code)
echo "[4/4] Installing LaunchAgent..."
mkdir -p "${HOME}/Library/LaunchAgents"
cp "${PLIST_SRC}" "${PLIST_DST}"
chmod 644 "${PLIST_DST}"

# Unload old version if running, then load fresh
launchctl unload "${PLIST_DST}" 2>/dev/null || true
launchctl load "${PLIST_DST}"
# Fire immediately so GITHUB_TOKEN is live now
launchctl start com.cascade-mac.github-token 2>/dev/null || true
echo "      ✓ LaunchAgent loaded — GITHUB_TOKEN set in user environment"

echo ""
echo "=== Done ==="
echo ""
echo "  GITHUB_TOKEN is now available in:"
echo "    • Terminal sessions (via ~/.zshrc)"
echo "    • VS Code / GitLens (via LaunchAgent user environment)"
echo "    • Any app launched from this session"
echo ""
echo "  Next: restart VS Code → GitLens → Home → GitHub should show as connected."
echo ""
echo "  SSH for git@github.com still requires 1Password unlocked."
echo "  All agent scripts use HTTPS (gh auth git-credential) — no SSH needed."
