# GitHub Hardening — Implementation Brief

TIER: STRUCTURED (audit findings); MEASURED at source where Devin audit ran
PROVENANCE: session `a35a5461` (2026-06-21, 12 turns); Devin audit referenced
STATUS: critique-and-handoff produced; live verification incomplete; sovereign-build GitHub config consistent with the critique
FOR: M5 watcher

## What exists

Standing laws (Ewan, this session):

- **GitHub is canonical source of truth.** Local folders are disposable worktrees/scratch.
- **Agents may author but not govern their own gates.** Verified-live finding: `devin-ai-integration[bot]` owned `/.github/workflows/` — a P0 hole. The agent owns its own CODEOWNER.
- **`AUTO_MERGE_PAT` self-approval loop** — agent approves its own PR via PAT. Verified hole.
- **Human escalation reserved for:** money / legal / credentials / security-boundary / ownership / liability / unresolved conflict. Everything else is delegated.

## What was done

- Partial Mac scan (bridge failed mid-scan — HTTP 502).
- Devin audit synthesised → conditionally safe.
- Cursor handoff produced for secure worktree + GitHub implementation.
- Two critical gaps identified and named (above).

## What it means

- **The sovereign-build's GitHub section already encodes the fixes:** `enforce_admins: true`, `require_last_push_approval: true`, `required_signatures: true`, `* @ewan-dot` CODEOWNERS, no auto-merge self-approval, git worktree isolation. → Architectural fix is in.
- **But the verified-live diff has not been logged as an artifact.** Was-broken-now-fixed proof is not in the inbox. The sovereign-build prescribes a target state; this brief records the gap-and-fix.
- **The "no human approval gate is madness" critique** (Ewan, this session) is the rod that the sovereign-build's GitHub section operationalises. Same idea, different artefact.

## What to change next

1. **Verify live GitHub state** of each Amplified repo against the sovereign-build target:
   - `enforce_admins`
   - `require_last_push_approval`
   - `required_signatures`
   - CODEOWNERS `* @ewan-dot`
   - `/.github/workflows/` CODEOWNER ≠ any agent bot
   - `AUTO_MERGE_PAT` not used for self-approval
   - Branch protection on `main`
2. **Log the diff** — was-broken / now-fixed / still-broken — per repo, in one file.
3. **`gh` CLI auth fix** — the bridge HTTP 502 + `gh` CLI auth failure both need re-running once the M5 bridge is healthy.
4. **PR-only rule** + **multi-agent collision prevention via git worktree** — both already in sovereign-build; verify implementation.
5. **`git -c core.hooksPath`** for pre-commit checks (CLAUDE.md ≤200 lines, ignore files present) — from the token-eff enforcement plan; add to provisioning script.

## Not yet verified

- Live branch protections per repo (Mac bridge was down at scan time).
- PAT scopes for each integration.
- Whether the two named holes (workflows CODEOWNER, AUTO_MERGE_PAT) have been actually closed since the critique.

## Tier C gates (Ewan only)

- Whether to run the verification against ALL Amplified repos or a named subset.
- Whether to revoke + reissue any PATs found over-scoped.

[CLOSURE] branch=PLAN | proxy=1 logged | gates=scope of verification run + PAT revocation decisions (Ewan) | inbox=github-hardening__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
