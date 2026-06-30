#!/usr/bin/env bash
# Agent Worktree Contract harness — GitKraken Step 5 + GitLens integration
#
# Creates an isolated worktree + branch for one task, following the
# <agent_lane>/<YYYYMMDDHHMMSS>/<task_slug> naming convention.
# The same string appears on: branch name · worktree path · Vellum witness.
#
# Auth: uses HTTPS + gh auth git-credential (reads macOS Keychain).
# SSH (git@github.com) is NOT used — requires 1Password SSH agent.
#
# Usage:
#   ./scripts/gk-worktree-start.sh <org/repo> <task-slug> [agent-lane]
#
# Example:
#   ./scripts/gk-worktree-start.sh Amplified-Partners/agent-claude fix-jwt-expiry
#   ./scripts/gk-worktree-start.sh Amplified-Partners/control-centre github-collector devin

set -euo pipefail

REPO="${1:-}"
TASK_SLUG="${2:-}"
AGENT_LANE="${3:-cascade-mac}"
GH=/opt/homebrew/bin/gh            # direct binary — not the 1Password alias
GK=/opt/homebrew/bin/gk
VELLUM_API="http://100.101.0.53:8400"
PENDING_QUEUE="${HOME}/.pending-vellum-queue"

usage() {
  echo "Usage: $0 <org/repo> <task-slug> [agent-lane]" >&2
  echo "  org/repo   — e.g. Amplified-Partners/agent-claude" >&2
  echo "  task-slug  — short kebab-case description (no spaces)" >&2
  echo "  agent-lane — defaults to 'cascade-mac'" >&2
  exit 1
}

[[ -z "$REPO" || -z "$TASK_SLUG" ]] && usage

if [[ "$TASK_SLUG" =~ [[:space:]] ]]; then
  echo "ERROR: task-slug must not contain spaces — use kebab-case" >&2
  exit 1
fi

TIMESTAMP=$(date -u +"%Y%m%d%H%M%S")
BRANCH="${AGENT_LANE}/${TIMESTAMP}/${TASK_SLUG}"
REPO_SHORT="${REPO##*/}"
WORKTREE_BASE="${HOME}/amp-worktrees"
WORKTREE_PATH="${WORKTREE_BASE}/${REPO_SHORT}/${BRANCH}"

echo "=== Agent Worktree Contract ==="
echo "Repo:      ${REPO}"
echo "Branch:    ${BRANCH}"
echo "Worktree:  ${WORKTREE_PATH}"
echo ""

# --- Ensure bare clone exists (or clone fresh via HTTPS — no SSH needed)
BARE_DIR="${HOME}/amp-repos/${REPO_SHORT}.git"
if [[ ! -d "${BARE_DIR}" ]]; then
  echo "[gk-worktree] Cloning bare repo to ${BARE_DIR} ..."
  mkdir -p "$(dirname "${BARE_DIR}")"
  # HTTPS + gh credential helper reads macOS Keychain (accessible without 1Password)
  GIT_TERMINAL_PROMPT=0 git -c credential.helper="${GH} auth git-credential" \
    clone --bare "https://github.com/${REPO}.git" "${BARE_DIR}"
  # Store credential helper config for future operations on this bare repo
  git -C "${BARE_DIR}" config credential.helper "${GH} auth git-credential"
  echo "[gk-worktree] Clone complete."
else
  echo "[gk-worktree] Fetching latest from origin ..."
  GIT_TERMINAL_PROMPT=0 git -C "${BARE_DIR}" \
    -c credential.helper="${GH} auth git-credential" \
    fetch --prune 2>&1 | sed 's/^/  /'
fi

# --- Guard: never work directly on main/master
CURRENT_BRANCH=$(git -C "${BARE_DIR}" symbolic-ref HEAD 2>/dev/null | sed 's|refs/heads/||' || echo "unknown")
echo "[gk-worktree] Default branch: ${CURRENT_BRANCH}"

# --- Create the worktree at the agent-lane path
mkdir -p "$(dirname "${WORKTREE_PATH}")"
git -C "${BARE_DIR}" worktree add -b "${BRANCH}" "${WORKTREE_PATH}" "${CURRENT_BRANCH}"
echo "[gk-worktree] Worktree created at: ${WORKTREE_PATH}"

# --- Mirror hooks into the new worktree (fixes core.hooksPath resolution)
HOOKS_SRC="${HOME}/agent-claude/.hooks"
HOOKS_DST="${WORKTREE_PATH}/.hooks"
if [[ -d "${HOOKS_SRC}" ]]; then
  mkdir -p "${HOOKS_DST}"
  cp "${HOOKS_SRC}/pre-commit" "${HOOKS_DST}/" 2>/dev/null || true
  cp "${HOOKS_SRC}/pre-push"   "${HOOKS_DST}/" 2>/dev/null || true
  chmod +x "${HOOKS_DST}"/* 2>/dev/null || true
  git -C "${WORKTREE_PATH}" config core.hooksPath .hooks 2>/dev/null || true
  echo "[gk-worktree] Hooks mirrored from ${HOOKS_SRC}"
fi

# --- Vellum witness (records door open; queues if Beast unreachable)
witness_door() {
  local payload
  payload=$(python3 -c "
import json
print(json.dumps({
  'author': '${AGENT_LANE}',
  'content': 'door:open repo=${REPO} branch=${BRANCH} worktree=${WORKTREE_PATH}',
  'entry_type': 'agent_write',
  'epistemic_tier': 'MEASURED',
  'message_type': 'info',
  'metadata': {
    'event': 'worktree_opened',
    'repo': '${REPO}',
    'branch': '${BRANCH}',
    'worktree_path': '${WORKTREE_PATH}',
    'task_slug': '${TASK_SLUG}',
    'agent_lane': '${AGENT_LANE}',
    'timestamp': '${TIMESTAMP}'
  }
}))
")
  local http_code
  http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 \
    -X POST "${VELLUM_API}/api/v1/agents/${AGENT_LANE}/send" \
    -H "Content-Type: application/json" \
    -d "${payload}" 2>/dev/null || echo "000")

  if [[ "${http_code}" == "200" || "${http_code}" == "201" ]]; then
    echo "[vellum] Door event witnessed (HTTP ${http_code})"
  else
    local ts
    ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "${ts} ${payload}" >> "${PENDING_QUEUE}"
    echo "[vellum] Vellum unreachable (HTTP ${http_code}) — event queued to ${PENDING_QUEUE}"
  fi
}
witness_door

# --- GitLens integration hints
echo ""
echo "=== GitLens (if VS Code is open) ==="
echo ""
echo "  Link this task to a Linear issue via GitLens Start Work:"
echo "  → MCP: gitlens_start_work"
echo "  → VS Code: GitLens panel → Start Work → select issue"
echo ""
echo "  When committing, use GitLens commit composer for AI-assisted messages:"
echo "  → MCP: gitlens_commit_composer"
echo "  → VS Code: Source Control → Sparkle (✨) button"
echo ""
echo "  Track PR review status:"
echo "  → MCP: gitlens_launchpad"
echo "  → VS Code: GitLens → Launchpad panel"
echo ""

echo "=== Ready ==="
echo "  cd ${WORKTREE_PATH}"
echo "  # Do your work, then:"
echo "  git push -c credential.helper='${GH} auth git-credential' -u origin ${BRANCH}"
echo "  ${GH} pr create --repo ${REPO} --base ${CURRENT_BRANCH} --head ${BRANCH} --title '...'"
echo ""
echo "  Note: SSH git@github.com requires 1Password unlocked."
echo "        These scripts always use HTTPS — no SSH needed."
