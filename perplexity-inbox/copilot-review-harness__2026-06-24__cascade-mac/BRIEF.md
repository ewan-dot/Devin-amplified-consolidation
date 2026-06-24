# Copilot Review Harness — 2026-06-24 (cascade-mac)

## What this is

A repeatable, token-efficient pattern for handling GitHub Copilot PR review comments
across the Amplified fleet. Built from the PR#1 (`deterministic-core`) review session.

---

## The 6 findings (PR#1 lessons) → permanent lint rules

| # | Finding | File | Fix | Lint rule in lint-core.sh |
|---|---------|------|-----|--------------------------|
| 1 | `inp.status` in `input_floor` ignores `valid_until` staleness | `epistemic_status.py:235` | Use `inp.effective_status([])` | Checks `inp.status for inp in inputs` pattern |
| 2 | `goal_link` allows bare 10+ char strings | `pre_production_gate.py:40` | Require `http://` or `https://` prefix | — |
| 3 | `compute()` returns bare `dict` | `pre_production_gate.py:122` | `dict[str, Any]` | Checks `-> dict:` on compute() |
| 4 | `assert` used for validation | `amplified_harness.py:130` | `raise ValueError` | Checks `assert ..., "..."` pattern in non-test Python |
| 5 | Hardcoded `/Users/ewansair/` in JSON | `amplified_rules.json:20` | `${AMPLIFIED_INBOX}` + env resolution | Checks `/Users/` in JSON values |
| 6 | Docstring claims no non-stdlib deps, mentions pytest | `test_deterministic_core.py:3` | "No **runtime** dependencies beyond the stdlib" | — |

---

## The harness: `scripts/lint-core.sh`

Exists in `Amplified-Partners/agent-claude`. Catches categories 1, 3, 4, 5 statically.
Run before pushing:

```bash
bash scripts/lint-core.sh      # exit 0 = clean, exit 1 = violations
```

Integrated into `.hooks/pre-push` — fires automatically on every `git push`.
No extra setup needed once hooks are installed (see `scripts/gk-worktree-start.sh`).

---

## Token-efficient flow for future Copilot rounds

When Copilot posts review comments on a PR:

1. **Don't re-read the full file** — grep for the exact line numbers Copilot cited.
2. **Check if lint-core.sh already catches the pattern** — if yes, the fix is
   already in the pre-push gate. If no, add it to lint-core.sh as a new check.
3. **Fix → test → lint in one pass**:
   ```bash
   python3 core/test_deterministic_core.py && bash scripts/lint-core.sh
   ```
4. **Write new regression tests** for each bug found — the 3 new tests in PR#6
   (`test_stale_input_propagates_through_layer`, `test_bare_string_goal_link_fails`,
   `test_closure_footer_invalid_branch_raises`) are the pattern.
5. **Single commit with all 6 fixes** — Copilot resolves all threads at once.

---

## What agents should NEVER do

- Fix one finding, push, wait for CI, fix the next — that's 6 rounds instead of 1.
- Leave a Copilot finding "acknowledged but not fixed" — it shows up in the next review.
- Use `assert` for validation anywhere in `core/` (lint-core.sh blocks this now).
- Hardcode `/Users/<username>/` paths in any tracked JSON/config file.

---

## Repo state after this session

`Amplified-Partners/agent-claude` main branch — 6 merged PRs:
- PR#1: deterministic-core (9 tests) ✅
- PR#2: gitkraken-github-control ✅
- PR#3: gitlens-integration ✅
- PR#4: tailscale-vellum-url ✅
- PR#5: vellum-tier-intuited ✅
- PR#6: copilot-pr1-fixes (12 tests, lint harness) ✅

12/12 tests passing. `scripts/lint-core.sh` runs on every push.
