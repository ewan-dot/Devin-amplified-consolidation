---
type: PLAN
title: Open-Door Harness — Phase 1 checklist (preset-swap re-architecture)
slug: open-door-phase1
version: v01
date: 2026-07-03
author: cursor
epistemic_tier: INTUITED
tier_reason: "Executes SSOT open-door-harness v01 §6 Phase-1, re-architected per RESEARCH cursor-heavyuser-harness-guidance R1–R7. Preset contents (globs, allowlists, net policy) are first-pass INTUITED; to be calibrated from Phase-2 nudge telemetry. All Cursor schema claims cited to cursor.com/docs (fetched 2026-07-03)."
drives_from:
  - "RESEARCH__cursor-heavyuser-harness-guidance__v01__2026-07-03__cursor.md (R1–R7)"
  - "SSOT__open-door-harness__v01__2026-07-03__cursor.md (§6 Phase 1, §7 defaults)"
status: EXECUTED — STAGED ONLY. Live ~/.cursor/hooks.json UNTOUCHED. Nothing activated.
worktree: /Users/ewansair/_worktrees/open-door-phase0  (branch feat/open-door-phase0)
---

# Phase 1 — from "shell-hook walls" to "door = preset of Cursor's own enforced surfaces"

**Core re-architecture (research R3):** a door is no longer a set of walls re-coded in
`before-shell-execution.sh`. A door is a **preset** of Cursor's *own* enforced surfaces —
`permissions.json` (auto-run allowlist + Auto-review steering) and `sandbox.json` (macOS
Seatbelt writable paths + network policy). **"Door enter" = swap those two files in.** The
kernel (Seatbelt) does the walling; the shell hook shrinks to **nudge/telemetry + a
fail-closed hard-deny core** (Red core + `git push`).

All artefacts are **staged** under `open_door_runtime/presets/` and `open_door_runtime/`.
None are copied to `~/.cursor/` by this phase. Activation stays the deliberate, reversible
step in `ACTIVATION.md`.

---

## Cursor-schema ground truth used (cited)

- `permissions.json` keys: `mcpAllowlist[]`, `terminalAllowlist[]` (prefix match), `autoRun{allow_instructions[],block_instructions[]}`. **No `terminalDenylist` exists** — "deny" intent rides `autoRun.block_instructions` (soft) + the hook hard-deny. Only consulted when a Run Mode is enabled; **not a security boundary**. (cursor.com/docs/reference/permissions)
- `sandbox.json` keys: `type` (`workspace_readwrite|workspace_readonly|insecure_none`), `additionalReadwritePaths[]`, `additionalReadonlyPaths[]`, `disableTmpWrite`, `enableSharedBuildCache`, `networkPolicy{default:allow|deny, allow[], deny[]}`. macOS Seatbelt via `sandbox-exec`, Cursor v2.0+. Deny beats allow; RFC1918 + metadata blocked by default (SSRF). (cursor.com/docs/reference/sandbox)
- Always-protected (unweakenable) paths: `.cursor/*.json` (**incl. `hooks.json`**), `.git/config`, `.git/hooks/**`, `.cursorignore`, `.vscode/**`. **Writable** `.cursor` subdirs: `rules/ commands/ worktrees/ skills/ agents/`. (sandbox reference)
- Three standing Protections force approval even in auto modes: **Browser**, **File-Deletion** (blocks auto `rm`), **External-File** (blocks auto create/modify/delete *outside the workspace*). (run-modes)
- Hooks are **fail-open unless `failClosed:true`**; `beforeReadFile` deny is unreliable; user hooks + `sessionStart`/`beforeSubmitPrompt`/`stop`/MCP hooks **do not fire in cloud agents**. (cursor.com/docs/hooks + research §1,§4)

---

## Checklist

### A. Preset re-architecture (R3) — door = permissions.json + sandbox.json
- [x] A1. `presets/research_read/{permissions.json,sandbox.json}` — read-only (`workspace_readonly`), web+searxng net.
- [x] A2. `presets/agentsmini_build/{…}` — one bound project subtree writable, net none.
- [x] A3. `presets/central_handoff/{…}` — **write-boundary fix (R below): amplified-pipeline + perplexity-inbox in `additionalReadwritePaths`**, tailnet net (Vellum).
- [x] A4. `presets/worktree_feature/{…}` — bound worktree subtree writable, net none; defer to native `/worktree`.
- [x] A5. `presets/pipe_run/{…}` — pipe run-dir writable, web+searxng+beast-read net.
- [x] A6. `presets/config_harness/{…}` — `~/.cursor/hooks/` writable; note `hooks.json` (`*.json`) is sandbox-protected and prompts; rule `.mdc` needs architect bless.
- [x] A7. `presets/README.md` — the preset-swap model, net_mesh→networkPolicy map, per-door table, placeholder-binding contract.
- [x] A8. `doors-v1.json` — additive `presets` block (paths + net_mesh→sandbox mapping); no door semantics changed.

### B. Shrink the shell hook to nudge/telemetry + fail-closed deny core (R5, §4)
- [x] B1. `hook_adapter.py` — evaluate the door-independent hard lines (secrets, `git push`, Red core) in a **fail-CLOSED** path (deny on internal error for shell/git), while door-scope stays fail-open (never wedge a session on a scope miss).
- [x] B2. `hooks-failclosed.snippet.json` — exact `hooks.json` per-script config with `"failClosed": true` on `beforeShellExecution` (+ recommended `beforeMCPExecution`). Staged; not merged into live `hooks.json`.
- [x] B3. `beforeReadFile` stays **nudge-only** (unreliable as a boundary) — unchanged decide() semantics; the real read boundary moves to `.cursorignore` (C1).

### C. Add the missing read/write boundaries (R2, R3, write-gap)
- [x] C1. `presets/_base/cursorignore` — base `.cursorignore` (the reliable read boundary): universal secret/credential globs + noise. Per-door add-on notes in README. Staged (copy to workspace root activates).
- [x] C2. Write-boundary: since there is **no `beforeWriteFile` hook**, `fs_write` scoping rides the sandbox `additionalReadwritePaths`. `central_handoff` explicitly adds `~/amplified-pipeline/` + `perplexity-inbox/` so it does not trip External-File Protection.

### D. SSOT C-3 fix + cloud/project-level reach (R1, R6)
- [x] D1. Bring `SSOT__open-door-harness__v01` + `RESEARCH__cursor-heavyuser-harness-guidance__v01` into the worktree (were untracked in the main checkout).
- [x] D2. Reclassify the Mac wall in §3: **STRUCTURED** via Cursor v2 Seatbelt sandbox + External-File/File-Deletion Protection; hooks are the **complement** (door-awareness + string-matched denies), not the sole wall. Rewrite the C-3 honest note and the C-3 conflict-resolution row.
- [x] D3. Move the read-wall note off `beforeReadFile` → `.cursorignore` in the hook-point map.
- [x] D4. Add a short **§3a — Cursor-native enforcement surfaces & the Mac-desktop-only limitation** section: user hooks + `sessionStart`/`beforeSubmitPrompt`/`stop`/MCP hooks don't run in cloud agents; estate/Beast reach needs **project-level** `.cursor/` config (hooks + permissions.json + sandbox.json committed to the repo `.cursor/`).

### E. ACTIVATION.md
- [x] E1. Rewrite around the **preset-swap** model (door enter = copy the door's `permissions.json`+`sandbox.json` into `~/.cursor/`), the fail-closed deny core, and the `.cursorignore` read boundary. Keep the single reversible hook-wiring step + rollback.

### F. Verify + commit
- [x] F1. `python3 door_enforcement.py` → ALL PASS (regression guard; decide() semantics unchanged, still 27/27 + new fail-closed test).
- [x] F2. Validate every preset JSON parses; `doors-v1.json` parses.
- [x] F3. Scoped commit on `feat/open-door-phase0`. **No push, no merge.** Confirm live `~/.cursor/hooks.json` untouched (mtime unchanged).

---

## Enforcement model — after Phase 1 (summary)

| Concern | Enforcer | Tier | Where staged |
|---|---|---|---|
| Write outside blast radius | **sandbox.json** `type` + `additionalReadwritePaths` + External-File Protection | STRUCTURED (Seatbelt) | `presets/<door>/sandbox.json` |
| Network beyond Net/Mesh | **sandbox.json** `networkPolicy` (default deny) | STRUCTURED | `presets/<door>/sandbox.json` |
| Read blast radius / secrets | **`.cursorignore`** + sandbox protected paths | STRUCTURED-ish | `presets/_base/cursorignore` |
| File deletes | **File-Deletion Protection** (native) | STRUCTURED | native |
| `git push` on Mac | **hook hard-deny (failClosed)** + `autoRun.block_instructions` | reliable hook | `hook_adapter.py` + presets |
| Red core (destroy/launder) | **hook hard-deny (failClosed)** + File-Deletion Protection | reliable | `hook_adapter.py` |
| Auto-run convenience | **permissions.json** `terminalAllowlist` per door | convenience | `presets/<door>/permissions.json` |
| Grey-zone "ask first" | **permissions.json** `autoRun.block_instructions` | soft steer | `presets/<door>/permissions.json` |
| Door menu / reminders | `sessionStart` / `beforeSubmitPrompt` (Phase 1 presentation, desktop-only) | advisory | (Phase-1 presentation, unchanged from Phase-0 stage) |
| Door-scope nudge/telemetry | `beforeShellExecution` + `beforeReadFile` (nudge) | advisory | `.door.sh` + `hook_adapter.py` |

**Blinkers without ceilings, kernel-backed:** the door lights one bounded path with Seatbelt;
the hook only *hard-stops* the genuinely dangerous few, fail-closed.
