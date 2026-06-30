# GitLens Integration + Keychain Bypass
**Author:** cascade-mac | **Date:** 2026-06-24 | **Tier:** STRUCTURED
**Status:** COMPLETE — scripts delivered, LaunchAgent ready to install, PR open

---

## What this does

Adds GitLens to the sovereign agent workflow alongside GitKraken, and fixes the
root cause of the keychain authentication issue so tools work without 1Password.

---

## Root cause: the keychain problem

`~/.ssh/config` has `Host *` routing ALL SSH connections through the 1Password
SSH agent socket (`~/Library/Group Containers/.../t/agent.sock`).  When 1Password
is locked, the agent socket has no identities loaded — so `git@github.com` fails
with `Permission denied (publickey)`.

This is NOT a problem with macOS Keychain (which is unlocked at login and is
where `gh auth token` stores its credential). It is specifically 1Password.

**What still works without 1Password:**
- `gh` CLI (`/opt/homebrew/bin/gh`) — reads from macOS Keychain ✓
- HTTPS git operations (via `gh auth git-credential`) ✓
- All gk/GitKraken MCP tools ✓
- All GitHub API operations ✓

**What requires 1Password:**
- `git@github.com:` SSH pushes/pulls — needs 1Password agent unlocked
- Any git remote configured with SSH URL

**Fix:** set `GITHUB_TOKEN` in the user environment via LaunchAgent so
all tools (especially GitLens in VS Code) pick it up without OAuth flow.

---

## GitLens integration

GitLens v18.2.0 is installed in VS Code.

The GitKraken MCP server (`gk mcp --host=claude-cli`) already exposes
GitLens tools alongside GitKraken tools. No separate MCP entry needed.

### GitLens MCP tools available to Claude Code

| Tool | What it does |
|------|-------------|
| `mcp__GitKraken__gitlens_launchpad` | Shows all actionable PRs, issues, worktree status |
| `mcp__GitKraken__gitlens_start_work` | Opens GitLens Start Work flow for an issue |
| `mcp__GitKraken__gitlens_start_review` | Opens GitLens Start Review flow for a PR |
| `mcp__GitKraken__gitlens_commit_composer` | Opens AI-assisted commit message composer |

**Requirement:** VS Code must be open with GitLens active. These tools send
commands to the VS Code UI — they are no-ops when VS Code is closed.

### Updated workflow

```
Task begins
  → gk-worktree-start.sh <repo> <slug>  # create branch + worktree
  → gitlens_start_work (if VS Code open) # optional: link to Linear issue
  → do work in worktree
  → gitlens_commit_composer (optional)   # AI commit message in VS Code
  → git push, gh pr create
  → gitlens_start_review (if VS Code open) # launch review in VS Code
```

---

## Files in this folder

| File | What |
|------|------|
| `BRIEF.md` | This file |
| `CHECKLIST.md` | Waypoints |
| `scripts/github-env-setup.sh` | Run once — sets up GITHUB_TOKEN everywhere |
| `plists/com.cascade-mac.github-token.plist` | LaunchAgent installed by the setup script |
| `scripts/gk-worktree-start.sh` | Updated worktree harness (GitLens-aware) |

---

## To install (Ewan action)

```bash
# Run once on this Mac — sets up GITHUB_TOKEN for GitLens
bash ~/ingestion-to-research-pipe/perplexity-inbox/gitlens-integration__2026-06-24__cascade-mac/scripts/github-env-setup.sh

# Restart VS Code — it will pick up GITHUB_TOKEN from the LaunchAgent
# GitLens → Home → Connect to GitHub will now work without keychain prompt
```

After that, GitLens API features (PR review, issue linking) work in VS Code
without any keychain/1Password prompt.

---

## What requires Ewan (Tier C)

- Running the setup script (writes to ~/.zshrc, installs LaunchAgent)
- Restarting VS Code after setup

---

## Shared across machines

This folder is in `ingestion-to-research-pipe/perplexity-inbox/` which syncs to
all machines via the `ewan-dot/Devin-amplified-consolidation` GitHub remote.
Run the same `github-env-setup.sh` on each Mac to apply.

*cascade-mac · 2026-06-24 · STRUCTURED*
