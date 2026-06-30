# GitLens Integration Checklist
**Branch:** `cascade-mac/YYYYMMDDHHMMSS/gitlens-integration`
**Tier:** STRUCTURED

## Waypoints

### W0 — Understand the auth failure
- [x] SSH fails: `Host *` → 1Password agent → locked → no identities
- [x] HTTPS works: `gh auth token` reads macOS Keychain (unlocked at login)
- [x] GitLens v18.2.0 installed at `eamodio.gitlens-18.2.0`
- [x] GitLens MCP tools already wired via `gk mcp` in `~/.claude.json`
- [x] GitLens AI model: `vscode` (copilot). GitHub integration: not yet authenticated

### W1 — GITHUB_TOKEN setup script
**Done when:** `scripts/github-env-setup.sh` exists, is executable, passes shellcheck
- [x] Script reads token via `gh auth token` (macOS Keychain, no 1Password)
- [x] Adds `GITHUB_TOKEN` export to `~/.zshrc` (terminal sessions)
- [x] Writes LaunchAgent plist to `~/Library/LaunchAgents/`
- [x] LaunchAgent sets `GITHUB_TOKEN` at user-environment level (Dock-launched VS Code)
- [x] Script is idempotent (safe to re-run)

### W2 — LaunchAgent plist
**Done when:** plist is valid XML, runs at login, sets env for all user apps
- [x] `com.cascade-mac.github-token.plist` written to plists/
- [x] `RunAtLoad: true`, reads via `gh auth token`
- [x] Logs to `/tmp/cascade-mac-github-token.log` on error

### W3 — Updated gk-worktree-start.sh (GitLens-aware)
**Done when:** script outputs GitLens tool hints, documents HTTPS-over-SSH reason
- [x] GitLens MCP tool hints in output
- [x] Comment explaining 1Password SSH bypass reason
- [x] No changes to the working HTTPS clone logic

### W4 — agent-claude PR open
**Done when:** new branch pushed, PR#3 open with all files
- [x] New worktree created via existing pattern
- [x] All files committed on new branch
- [x] PR opened against main

## Blocked (Tier C — Ewan)

- [ ] Run `github-env-setup.sh` on this Mac
- [ ] Run `github-env-setup.sh` on Beast / other Macs (adapt `AGENT_LANE`)
- [ ] Restart VS Code after setup — GitLens will pick up `GITHUB_TOKEN`
- [ ] (Optional) Disable 1Password SSH for `github.com` and use `id_ed25519_github` directly once key passphrase is stored in macOS Keychain

## What done looks like

- `GITHUB_TOKEN` in terminal: `echo $GITHUB_TOKEN | head -c 10` → prints `gho_...`
- `GITHUB_TOKEN` in VS Code: GitLens → Home → "GitHub is connected" (no auth prompt)
- `gitlens_launchpad` MCP tool returns PR list without error
- `gk-worktree-start.sh` runs end-to-end and prints GitLens hints at the end
