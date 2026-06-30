---
project: amplified
artifact_type: overview-addendum
purpose: gitkraken-layer-and-claude-seat
version: v02
date: 2026-06-24
origin: perplexity
author: AI_PARTNER_PROXY
status: draft_for_ratification
supersedes_section_of: amplified__overview__unified-cohesive-plan__v01__2026-06-23__perplexity.md
effective_tier: STRUCTURED
provenance: GitKraken official docs (help.gitkraken.com, gitkraken.com, github.com/gitkraken/mcp) 2026-05/06 + v01 overview + loaded doctrine
goal_lock: get the business going — make money so we can give it away
---

# v02 Addendum — GitKraken as the Agent-Git Layer

**TIER: STRUCTURED** · tool capabilities below are MEASURED from GitKraken's own current docs; the *fit* into our stack is judgment (STRUCTURED). This is an addendum to v01, not a rewrite: GitKraken changes the **occupant's tooling**, not the spine.

## 1. Where GitKraken sits in the four layers

v01 had: GitHub = ground, deterministic core = spine, Vellum = nervous system, Macs + agents = hands. The gap: the hands talked to the ground via **raw git + provider-specific APIs**. GitKraken closes that gap as a **provider-agnostic git/PR/issue layer** between agents and GitHub.

```
agents (Claude Code / Devin)
        │  via GitKraken MCP (gk mcp) or ACP bridge
        ▼
GitKraken layer  ── unified across GitHub, GitLab, Bitbucket, Azure DevOps, Jira
        │  provider API
        ▼
GitHub (ground) ── canonical code + PR gate (Agent Worktree Contract)
```

Why it serves the goal: the GitHub-monitoring **seat stays agent-agnostic** (idea-meritocracy rod). Swapping Devin → Claude Code, or running both, changes the occupant, not the wiring — because both speak the same GitKraken tool surface.

## 2. The two integration paths (both live today)

**Path 1 — GitKraken MCP server (`gk mcp`):** a local MCP server any agent can call. Verified tool surface ([Tools Reference](https://help.gitkraken.com/mcp/mcp-tools-reference/)):

| Category | Tools | Use in our plan |
|---|---|---|
| Git | `git_worktree`, `git_branch`, `git_checkout`, `git_add_or_commit`, `git_push`, `git_stash`, `git_status`, `git_log_or_diff`, `git_blame` | Enforces the worktree contract via a tool, not raw git |
| Pull Requests | `pull_request_assigned_to_me`, `pull_request_get_detail`, `pull_request_get_comments`, `pull_request_create_review` | The literal "monitor + review PRs" job |
| GitLens | `gitlens_start_work`, `gitlens_start_review`, `gitlens_commit_composer`, `gitlens_launchpad` | Issue→branch start, PR review workflow |
| Issues | `issues_assigned_to_me`, `issues_get_detail`, `issues_add_comment` | Backlog triage |
| Repo / Workspace | `repository_get_file_content`, `gitkraken_workspace_list` | Cross-repo context |

Private-remote PR/issue tools require GitKraken **Pro or higher** ([Tools Reference](https://help.gitkraken.com/mcp/mcp-tools-reference/)).

**Path 2 — ACP bridge for Claude Code:** GitKraken (Kepler/GitLens) auto-detects the Claude Code binary and can drive sessions directly through the Agent Client Protocol; "Detect external Claude Code sessions" adds hooks to `~/.claude/settings.json` so externally-started Claude Code sessions are surfaced ([Kepler settings](https://help.gitkraken.com/kepler/settings/)).

## 3. How Claude (the GitHub-monitor seat) uses it

1. **Worktree discipline via tool:** `git_worktree` + `git_branch` give the isolated-worktree → one-branch contract through a controlled surface instead of raw git.
2. **PR monitoring loop:** `pull_request_assigned_to_me` → `pull_request_get_detail` → `gitlens_start_review` / `pull_request_create_review`.
3. **Cross-repo sweeps in one prompt:** documented workflows include bumping a shared dependency across all workspace repos + opening PRs, and stale-branch cleanup ([GitKraken blog, 2025-06-10](https://www.gitkraken.com/blog/introducing-gitkraken-mcp)).
4. **MCP Apps (visual):** `git_status` and `git_graph` render interactive apps in VS Code; limited in Claude Desktop ([MCP Apps](https://help.gitkraken.com/mcp/mcp-apps/)).

## 4. Honest caveats (radical honesty)

- **Double-gate:** GitKraken MCP issues its **own** confirm-before-run prompt ([GitKraken MCP](https://www.gitkraken.com/mcp)), on top of our Vellum-witnessed one-door gate. Belt-and-braces, but decide deliberately: either accept the double-confirm, or set GitKraken toolsets to "Always Allow" for read tools and keep the human gate only on writes.
- **Witness still owns the record:** GitKraken's gate is **not** a substitute for the Vellum witness. Every door GitKraken opens must still be Baton-witnessed in Vellum — GitKraken is the tool, Vellum is the truth.
- **Pro tier likely required** for private-repo PR/issue tools — confirm the account plan before relying on them.
- **MCP install is sticky:** "Install GitKraken MCP for detected clients" reinstalls on app startup and **uninstalling is not supported** ([Kepler settings](https://help.gitkraken.com/kepler/settings/)) — know this before enabling fleet-wide.

## 5. Decision proposed (STRUCTURED — for ratification)

Seat **Claude Code as GitHub monitor on M5 via GitKraken**, alongside Devin, under the Agent Worktree Contract; let `effective_use` + `door_compliance` sensors produce the merit evidence. Companion executable handoff: `gitkraken-claude-setup__job__m5-setup__v01__2026-06-24__perplexity.md` in the perplexity-inbox.

— STRUCTURED · GitKraken docs 2026-05/06 + v01 · proxy-authored · awaiting Ewan ratification
