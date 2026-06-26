---
project: amplified
artifact_type: job
purpose: gitkraken-claude-setup-fleet
version: v01
date: 2026-06-24
origin: perplexity
author: AI_PARTNER_PROXY
status: ready_to_implement
effective_tier: STRUCTURED
provenance: GitKraken official docs (help.gitkraken.com / gitkraken.com / github.com/gitkraken/mcp) 2026-05/06
target_machines: [WanMin (Mac mini M4 Pro), MacAirM5, MacAirM4]
goal_lock: get the business going — make money so we can give it away
---

# JOB — Enable GitKraken MCP + Claude Code on ALL THREE Macs

**For:** the M5 local AIs watching `perplexity-inbox/`.
**Goal:** every Mac (WanMin, M5, M4) can use GitKraken as the provider-agnostic git/PR/issue layer, with Claude Code able to drive it. Identical setup per machine so the GitHub-monitor seat is portable across the fleet.

**TIER: STRUCTURED** — commands are from GitKraken's current docs; per-machine paths/plan must be verified locally before relying on private-repo tools.

---

## Per-machine checklist (run on WanMin, then M5, then M4)

### Step 1 — Install / update the GitKraken CLI (`gk`)
```bash
# verify or install
gk --version || brew install gitkraken-cli
gk --version   # confirm it runs
```

### Step 2 — Authenticate the git provider(s)
```bash
gk auth login            # sign in to the GitKraken account
gk provider add github   # add GitHub provider token (also: gitlab, jira, azure, bitbucket as needed)
gk provider set          # set GitHub as default git provider
```
NOTE: private-repo PR/issue MCP tools require GitKraken **Pro or higher**. Confirm the account plan; if free tier, only public-repo + local-git tools will work.

### Step 3 — Register the GitKraken MCP server for Claude Code
Add to each machine's Claude Code MCP config (`~/.claude.json` or the project `.mcp.json`):
```json
{
  "mcpServers": {
    "gitkraken": {
      "command": "gk",
      "args": ["mcp"]
    }
  }
}
```
Verify: in Claude Code agent mode, run prompt `What issues are assigned to me?` — it should request approval for the `issues_assigned_to_me` tool.

### Step 4 — (Optional, M5/M4/WanMin if GitLens/Kepler installed) ACP bridge
If GitKraken Kepler/GitLens is installed on the machine:
- Setting `Use ACP bridge for Claude Code` = **On** (default) — lets GitKraken drive Claude Code sessions directly.
- Setting `Detect external Claude Code sessions` = **On** if you want GitKraken to surface Claude Code sessions started in a terminal (adds hooks to `~/.claude/settings.json`).
- Caveat: `Install GitKraken MCP for detected clients` reinstalls on startup and **cannot be uninstalled** — enable knowingly.

### Step 5 — Wire to the Agent Worktree Contract
Confirm Claude Code, when acting on a repo, uses `git_worktree` to create an isolated worktree and `git_branch` for one branch — do NOT let it commit straight to canonical main. The PR gate stays the only door into main.

### Step 6 — Vellum witness (do not skip)
Every GitKraken door the agent opens must still be Baton-witnessed in Vellum. GitKraken's own confirm-before-run prompt is belt-and-braces, NOT a replacement for the witness. If the fleet Vellum endpoint is still refusing connections (see v01 finding), buffer to the pending queue and flush once it's live.

---

## Verification (per machine)
- [ ] `gk --version` runs
- [ ] `gk provider` lists GitHub authenticated
- [ ] Claude Code lists the `gitkraken` MCP server with tools (`git_worktree`, `pull_request_assigned_to_me`, etc.)
- [ ] Test prompt `What PRs are assigned to me?` returns real data
- [ ] Worktree-contract behaviour confirmed (isolated worktree, branch, PR — no direct main writes)
- [ ] Door event appears in the Vellum witness / pending queue

## Decision this implements (for Ewan to ratify)
Claude Code seated as portable GitHub monitor across all three Macs via GitKraken, alongside Devin; merit decided by `effective_use` + `door_compliance` sensors. Best agent keeps the seat on evidence, not loyalty.

[CLOSURE] endpoint = this executable job in perplexity-inbox. gates = (1) Ewan ratifies the Claude-Code-as-monitor decision; (2) confirm GitKraken account plan (Pro needed for private-repo tools). All install steps are Tier A/B local acts on Ewan's machines, implemented by the M5 watchers — Perplexity does not implement past the inbox.

— STRUCTURED · GitKraken docs 2026-05/06 · proxy-authored · ready to implement on WanMin + M5 + M4
