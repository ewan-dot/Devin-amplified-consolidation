# End of Session Summary — 2026-06-24

**Author:** cascade-mac (Claude Code on M5 Air)
**Tier:** MEASURED (all artefacts committed, tests verified, pushed to GitHub)
**Provenance:** Session starting from "container on m5" working directory, 2026-06-24 afternoon
**Status:** complete — all unblocked work done and pushed; blocked items documented as one Ewan hand-back

---

## 1. Orientation — What Was Read

Before writing a line of code, the session surveyed the current state:

**Antigravity (session `fef3d5bc`, 2026-06-24):** Phase 1 integration is complete. Delivered: `epistemic_status.py`, `pre_production_gate.py`, unit tests, pre-commit hooks, Vellum JWT re-minting for all M5 and Mac mini agents, Opik container restart-policy fix on Beast, clean git clones of `antigravity` and `intent-interface` on the Mac mini, and the SMB share mount script. All committed and pushed.

**Devin (report 2026-06-17, `~/.devin/capture-prep-report-2026-06-17.md`):** Repo secrets audit. Found live API keys sitting in untracked `.env` files on two repos: `clawd-autonomous-agent` (DeepSeek key) and `amplified-hermes-team` (Moonshot + Linear keys). Keys are NOT in git history — only in the working tree `.env` files. `Amplified Partners Truth` and `the-amplified-method` are clean and ready to push. These keys **still need rotating** — Devin flagged them but was blocked (Vellum unreachable at the time).

**GitHub estate:** 30 private repos in `Amplified-Partners` org. Key repos:
- `agent-claude` — my sandbox (cascade-mac cell membrane)
- `fleet-clean-build` — governance rulebook
- `intent-interface`, `antigravity` — product repos that antigravity is working in
- `Amplified-Partners/Claude` — code ingress lane (push here, not directly to production repos)

**BATON.md state on entry:** Last session (2026-06-21) left the workspace at W2 — membrane templates drafted, macOS user-account host runbook written in `runbooks/`. The next unblocked task was the deterministic core.

**Briefs read:** `deterministic-core__implementation-brief__v01__2026-06-24__perplexity.md` — confirmed the mandate: extend `epistemic_status.py`, do not rebuild it. Live wiring (Vellum + Beast) is blocked on Ewan's Tier C gates.

---

## 2. What Was Done

### 2a. Permanent `agent-claude` workspace on M5

- Cloned `Amplified-Partners/agent-claude` to `~/agent-claude` using HTTPS + `gh auth git-credential`.
- **SSH git is blocked on M5** — only HTTPS + the gh token works. The global `.gitconfig` already has `credential.helper = !/opt/homebrew/bin/gh auth git-credential` configured. The bare-token URL that appeared during cloning was immediately replaced with the clean HTTPS URL.
- Confirmed push works: `git ls-remote origin` authenticated via gh credential helper.

### 2b. Worktree — `~/agent-claude-wt/deterministic-core`

- Created via `git worktree add ~/agent-claude-wt/deterministic-core -b deterministic-core`.
- All build work for this task lives here, isolated from `main`.
- Branch pushed to `origin/deterministic-core`.

### 2c. Deterministic core files

Copied from canonical sources — **not rebuilt**, as the brief specified:

| File | Source |
|------|--------|
| `core/epistemic_status.py` | `~/ingestion-to-research-pipe/epistemic_status.py` (canonical inbox) |
| `core/pre_production_gate.py` | Antigravity session `fef3d5bc` scratch dir |
| `core/amplified_harness.py` | `~/ingestion-to-research-pipe/perplexity-inbox/amplified_permissions.py` |
| `core/amplified_rules.json` | `~/ingestion-to-research-pipe/perplexity-inbox/amplified_rules.json` |

### 2d. Tests — 9 passing (`core/test_deterministic_core.py`)

All tests are stdlib-only (no pip install required). Run with `python3 core/test_deterministic_core.py`.

**Key invariant confirmed through testing:** A failed precondition does NOT raise `P0Incident`. It *demotes* the effective status via the min-rule (e.g. STRUCTURED → INTUITED). `P0Incident` fires at the *consumer* when it tries to use a value whose tier is too low. This is the correct behaviour — test was written to document it, not fight it.

### 2e. Git hooks — `.hooks/pre-commit` and `.hooks/pre-push`

Both hooks are tracked in the repo under `.hooks/` and also mirrored in `~/agent-claude/.git/hooks/` and `~/agent-claude/.hooks/`.

**`pre-commit` does:**
- Secret scan: 13 patterns, BSD-grep-safe (macOS `grep -E`). Catches: `sk-` API keys for Anthropic/DeepSeek/Moonshot/OpenAI, GitHub tokens (`gho_`, `ghp_`), AWS keys (`AKIA`), Linear keys, PEM private keys (4 flat patterns — BSD grep can't handle the grouped variant).
- `.env` file guard: blocks staging any `.env` file.
- CLAUDE.md line-count guard: fails if a staged CLAUDE.md exceeds 200 lines.
- BATON.md warning: warns (does not block) if code files are staged without BATON.md.

**`pre-push` does:**
- Runs the full test suite (`python3 core/test_deterministic_core.py`) before any push leaves the machine. Push is blocked if tests fail.

**Bug found and fixed during this session:** `core.hooksPath=.hooks` in the main repo's `.git/config` resolves `.hooks` relative to the *main checkout* (`~/agent-claude/`), not the worktree. So a commit from the worktree was silently failing (exit 1, no output). Fixed by creating `~/agent-claude/.hooks/` as a mirror of the worktree's `.hooks/`. Once the PR merges to `main`, the `main` checkout will have `.hooks/` naturally and the mirror is self-sustaining.

### 2f. `.gitignore` updated

Added `.env`, `.env.*`, `*.env`, `secrets.*`, `*_secret.*`, `*.key`, `*.pem` — the patterns that would catch the exact secrets Devin found still sitting in local repo trees.

### 2g. `CHECKLIST.md`

Tracks task waypoints and blocked items. All 3 waypoints checked. Blocked items point to the consolidated Tier C gate hand-back (see §4).

### 2h. `BATON.md` updated

Records: this session's work, SSH-git limitation, the Tier C blockers, and the next concrete steps for the next instance.

### 2i. PR opened

[Amplified-Partners/agent-claude#1](https://github.com/Amplified-Partners/agent-claude/pull/1) — `deterministic-core` → `main`. Ewan merges; cascade-mac does not push directly to `main` in production repos.

---

## 3. What It Means

**The epistemic gate is now the floor.** Any agent that imports from `core/` gets the 4-tier invariant, the pre-production task gate, and the permission classifier. No LLM in any decision path inside these files. Tier: MEASURED (tests pass, push verified).

**Hooks prevent the exact class of incident Devin found.** The pre-commit secret scanner would have blocked the DeepSeek and Moonshot keys from ever being staged. It is live now on this repo.

**The worktree workflow is verified end-to-end.** Clone → worktree → work in waypoints → pre-push tests → PR. The `core.hooksPath` gotcha is documented and fixed. Future worktrees will inherit the corrected setup once PR#1 merges.

**Live wiring remains blocked** — and deliberately so. Nothing was invented to work around the Tier C gates. The blocked items are named, consolidated, and pointed at the correct hand-back file.

---

## 4. What Is Next

### Unblocked (next instance can start immediately)

1. **Merge PR#1** — Ewan's click. Once merged, `~/agent-claude/.hooks/` is no longer needed as a mirror (`.hooks/` will be in `main`).
2. **Continue W2** — Membrane templates for `agent-devin`, `agent-cascade`, `agent-cursor` in `runbooks/`. Draft is reversible, no Ewan sign-off needed.
3. **W3/W4** — macOS user-account host layout runbook + GitHub hardening script (per-agent fine-grained PATs replacing the current org-wide token). Runbooks are reversible; execution is Ewan's click.
4. **Rotate the Devin-flagged keys** — DeepSeek (`sk-13a9f2a2...`) and Moonshot (`sk-LQFe...`) and Linear (`lin_...`) are still live in `.env` files in local repo working trees. Delete those `.env` files (keys are NOT in git history) and rotate at the provider.

### Blocked — requires Ewan (one consolidated hand-back)

All four live blockers are in: `~/ingestion-to-research-pipe/perplexity-inbox/INBOX-INDEX__v01__2026-06-24__perplexity.md` — section **"The collapsed Tier C gate cluster"**.

Summary:
1. **Vellum JWT TTL + Infisical** — choose TTL (30d suggested), choose fix-Infisical-now vs stopgap auto-mint, set sheet scope for `shared_dev`, slug-vs-UUID for `sheet_id`.
2. **Beast estate-machine stack** — is the dark state (Traefik serving default 404) intentional or a surprise? One-line answer.
3. **PostgreSQL connector in Perplexity** — connect the Perplexity connector to the Beast database. ~1 minute action, Ewan only.
4. **OPEC = OpenTelemetry?** — one-line confirmation.

---

## 5. Files Changed / Created This Session

```
~/agent-claude/                          ← permanent clone (new this session)
~/agent-claude/.hooks/pre-commit         ← mirror of worktree hooks (new)
~/agent-claude/.hooks/pre-push           ← mirror of worktree hooks (new)
~/agent-claude-wt/deterministic-core/    ← worktree (new this session)
  .gitignore                             ← updated (added .env / secret patterns)
  .hooks/pre-commit                      ← new (secret scan + guards)
  .hooks/pre-push                        ← new (test suite gate)
  BATON.md                               ← updated to 2026-06-24
  CHECKLIST.md                           ← new (waypoints + blocked items)
  core/epistemic_status.py               ← copied from canonical source
  core/pre_production_gate.py            ← copied from antigravity session
  core/amplified_harness.py              ← copied from inbox
  core/amplified_rules.json              ← copied from inbox
  core/test_deterministic_core.py        ← new (9 tests, all pass)
```

**GitHub:** Branch `deterministic-core` pushed to `Amplified-Partners/agent-claude`. PR#1 open.

---

[CLOSURE] branch=ACTION | proxy=none | gates=4 Tier C items (Ewan hand-back consolidated in INBOX-INDEX) | inbox=completed-by-cascade-mac__2026-06-24/SUMMARY__2026-06-24__cascade-mac.md | tier=MEASURED
