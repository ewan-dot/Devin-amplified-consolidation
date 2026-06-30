# Session Summary — GitKraken + GitHub + control-centre
**Author:** cascade-mac | **Date:** 2026-06-24 (evening session)
**Tier:** MEASURED (all artefacts tested against live data)
**Status:** COMPLETE — PRs open, CI green, audit run

---

## Plans addressed from perplexity-inbox

1. `gitkraken-claude-setup__job__fleet-three-macs__v01__2026-06-24__perplexity.md`
2. `github-hardening__implementation-brief__v01__2026-06-24__perplexity.md`
3. `control-centre__brief__claude-build-deploy__v01__2026-06-24__perplexity.md` (GitHub collector scope)

---

## GitKraken (Steps 5 + 6 + Verification)

### Verified already complete
- ✅ `gk` v3.1.68 installed at `/opt/homebrew/bin/gk`
- ✅ GitHub provider connected (`gk provider list` → ✓)
- ✅ GitKraken MCP registered in `~/.claude.json` (`gk mcp` server)
- ✅ `gk whoami` → ewan-dot, Amplified Partners Teams org, GitHub + Linear
- ✅ `gk pr list --all` → live PR data returned

### Built this session
- ✅ **Step 5 — Worktree Contract:** `scripts/gk-worktree-start.sh`
  - Creates `<agent_lane>/<YYYYMMDDHHMMSS>/<task_slug>` branch + worktree
  - Mirrors `.hooks/` into new worktree (fixes `core.hooksPath` resolution)
  - Witnesses door open in Vellum; queues to `~/.pending-vellum-queue` if down
- ✅ **Step 6 — Vellum witness:** `.hooks/pre-commit` updated
  - Main-branch guard: refuses direct commits to `main`/`master`
  - Vellum checkpoint on every commit (non-blocking)
  - Pending queue fallback: `~/.pending-vellum-queue`
- ✅ **Verification checklist:** all 6 items confirmed
- ✅ **2 events queued** in `~/.pending-vellum-queue` (Beast ports refused, expected)

---

## GitHub Hardening Audit (W4 of PLAN.md)

Script: `scripts/github-audit.sh` — READ-ONLY, live `gh api` calls.
Audit file: `GITHUB-AUDIT-20260624173425.md`

### P0 findings (FAIL — Ewan Tier C to enforce)

| Repo | Finding |
|------|---------|
| `agent-claude` | Branch NOT protected; CODEOWNERS missing |
| `antigravity` | Branch NOT protected; CODEOWNERS missing |
| `intent-interface` | CODEOWNERS missing |
| `fleet-clean-build` | `AUTO_MERGE_PAT` in `governance-audit.yml` (self-approval loop) |
| `estate-machine` | `AUTO_MERGE_PAT` in `auto-review-merge.yml` (self-approval loop) |
| `estate-cost-tools` | `AUTO_MERGE_PAT` in `auto-review-merge.yml` (self-approval loop) |
| `brain-mcp` | `AUTO_MERGE_PAT` in `auto-review-merge.yml` (self-approval loop) |

### Warnings (WARN — recommend fixing, not blocking)

`fleet-vellum`, `fleet-clean-build`, `estate-machine`, `estate-cost-tools`, `brain-mcp` all have 4 warns: `enforce_admins=False`, `dismiss_stale_reviews=False`, `require_last_push_approval=False`, `required_signatures=False`.

**No changes were made.** Enforcement is Ewan's Tier C gate.

---

## control-centre (GitHub collector + DuckDB extension)

**Repo:** `Amplified-Partners/control-centre` — created, first push, CI green (10s).

### Delivered

| File | What |
|------|------|
| `core/schema.py` | `stats_events` + `stats_findings` DDL; constitutional gate (8 predicates, T1/T2/T3) |
| `collectors/github.py` | `gh` CLI collector, 6 metrics/repo, no MCP |
| `rules/engine.py` | Deterministic rule engine → `stats_findings`; no LLM |
| `tests/` | 19 tests, 0 external deps, stdlib only — 19/19 pass |
| `.github/workflows/ci.yml` | GitHub Actions CI (green on first push) |

### GitHub collector — verified live
5 rows from `Amplified-Partners/agent-claude`:
- `open_prs`: 1 (PR#1 open)
- `merged_prs_7d`: 0
- `open_issues`: 0
- `branch_protection`: 0 (confirms the FAIL finding above)
- `stale_branches`: 0

---

## Infra state logged

| Component | State |
|-----------|-------|
| Beast `100.101.0.53` | Reachable on Tailscale; ALL ports refused (estate-machine DOWN) |
| Vellum API `:8400` | Connection refused |
| `~/.pending-vellum-queue` | 2 events queued, awaiting Beast restoration |
| `gk` + `gh` auth | Both working; `gk auth login` not needed (providers already connected) |

---

## GitHub artefacts

- [agent-claude PR#2](https://github.com/Amplified-Partners/agent-claude/pull/2) — GitKraken harness + audit + schema
- [control-centre](https://github.com/Amplified-Partners/control-centre) — new repo, CI green

---

## What's next (Tier C — Ewan)

1. **Beast estate-machine:** is the dark state intentional?
2. **Enforce branch protections** from audit (irreversible)
3. **AUTO_MERGE_PAT** in 4 repos — revoke/reissue?
4. **Merge PR#2** and **PR#1** (agent-claude)

[CLOSURE] status=COMPLETE | plans=gitkraken-setup + github-hardening + control-centre(GitHub) | PRs=agent-claude#1,#2 + control-centre main | tier=MEASURED
