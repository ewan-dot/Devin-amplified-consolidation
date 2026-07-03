---
type: PLAN
title: Open-Door Harness — Phase 0 (scaffold-only) plan + checklist
slug: open-door-phase0
version: v01
date: 2026-07-03
author: cursor
epistemic_tier: INTUITED
tier_reason: "Execution checklist for the ratified SSOT Phase 0. On-disk plan-witness because Vellum is down; must be posted to Vellum on reconnect."
status: IN-PROGRESS
implements: perplexity-inbox/SSOT__open-door-harness__v01__2026-07-03__cursor.md (§6 Phase 0, §7 ratified defaults)
worktree: /Users/ewansair/_worktrees/open-door-phase0
branch: feat/open-door-phase0
---

# Phase 0 — SSOT scaffold only (NO live enforcement)

**Vellum is DOWN.** This file is the plan-witness. **ACTION REQUIRED on reconnect:**
post this plan + the completion to the Vellum ledger under seat `cursor`.

## Critical safety constraint (repeated so it is never lost)

Phase 0 is **SCAFFOLD-ONLY**. Do **NOT** activate live door-deny enforcement.
Specifically: **do NOT wire deny logic into the live `/Users/ewansair/.cursor/hooks.json`.**
Active `beforeShellExecution` / `beforeReadFile` deny could break running Cursor sessions.
Stage the code; activation is a single documented step left for Ewan (see `ACTIVATION.md`).

## Ratified defaults (SSOT §7)

- 6 doors: `research_read` (default), `agentsmini_build`, `central_handoff`, `worktree_feature`, `pipe_run`, `config_harness`.
- `config_harness`: agents may edit **hooks/scripts** freely; **rule `.mdc`** changes need architect bless.
- Wall hardness: **nudge → then hard-deny** (`research_read` + `config_harness` first).
- Default door: `research_read`. Marker: `~/.amplified/active-door.json`. Manifest: `perplexity-inbox/config/doors-v1.json`.
- Universal: Secrets/Infisical = NO DOOR EVER; Red destructive actions + git push on Mac = door-independent.

## Checklist

- [x] **0. Worktree** — create `feat/open-door-phase0` at `/Users/ewansair/_worktrees/open-door-phase0` (outside main checkout), work only there.
- [x] **1. Plan-witness** — write this checklist file to the worktree (this file). Tick as completed.
- [x] **2. C-4 rename** — completed `amplified_permissions.py` internal refs (`amplified_harness` → `amplified_permissions`, provenance line kept); established canonically-named runtime home `open_door_runtime/`; documented that old-named copies live only in separate nested untracked repos (out of worktree scope) and that no prior runtime dir existed to rename.
- [x] **3. Doors manifest** — `perplexity-inbox/config/doors-v1.json`: 6 doors with name, purpose, access scope (FS read/write, net/mesh, MCP/tools, git-write, spend-tier) + universal rules, mirroring `fleet-routing-v1.json` shape. JSON validated.
- [x] **4. Active-door marker** — `~/.amplified/active-door.json` created defaulting to `research_read` (state file, outside repo). Committed reproducible copy: `open_door_runtime/active-door.example.json`.
- [x] **5. Enforcement LOGIC** — `open_door_runtime/door_enforcement.py`: pure `decide(action, door, manifest) -> allow|nudge|deny` + 27 self-tests (ALL PASS). Plus staged, fail-open `hook_adapter.py` + chaining wrappers under `open_door_runtime/hooks/`. **NOT connected to live hooks.**
- [x] **6. ACTIVATION.md** — `open_door_runtime/ACTIVATION.md`: exact one activation step + nudge→deny knob (`~/.amplified/open-door-mode`), `research_read`+`config_harness` first, full rollback, honest limitations.
- [x] **7. Commit** — scoped adds on the worktree branch only. NOT pushed. NOT merged to main.

## Verification evidence

- `python3 door_enforcement.py` → ALL PASS (27/27).
- Adapter smoke: git push → deny; secret read → deny; Red-core shell → deny; out-of-scope read → nudge; repo doc read → allow; garbage stdin → fail-open allow.
- Live `~/.cursor/hooks.json` **unchanged**; no locked `rules/*.mdc` touched; no secrets read/printed/committed.
- Mode file `~/.amplified/open-door-mode` NOT present (default scaffold) — no enforcement active.

## Radical-honesty notes (reality vs brief)

1. In `ingestion-to-research-pipe` the classifier is **already** named `perplexity-inbox/amplified_permissions.py`
   (rename done on disk previously) but its docstring/import example still say `amplified_harness`. Phase 0 finishes those refs.
2. The old-named `amplified_harness.py` files exist only in **nested, untracked, independent git repos**
   (`Antigravity/`, `Projects/intent-interface/`) — NOT part of this repo and NOT in this worktree. Renaming them is
   out of scope for a worktree-only, reversible Phase 0. Flagged for Ewan as a separate cross-repo task.
3. No pre-existing `runtime` dir (Baton+RodGuard) exists in this repo to rename. Instead the new enforcement logic
   is placed in a canonically-named `open_door_runtime/` home, satisfying the intent of C-4's naming.

## Constraints honoured

worktree only · never edit live `~/.cursor/hooks.json` · no locked `rules/*.mdc` touched ·
no secrets read/printed/committed · everything reversible (worktree removable, no push, no merge).
