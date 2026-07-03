---
type: RESEARCH
title: Cursor Capabilities + Heavy-User Guidance for the Open-Door Harness
slug: cursor-heavyuser-harness-guidance
version: v01
date: 2026-07-03
author: cursor
epistemic_tier: INTUITED
tier_reason: "Synthesis of Cursor official docs (hooks, permissions.json, run-modes/sandbox, best-practices blog) + heavy-user practitioner writeups, cross-checked against SSOT__open-door-harness__v01. All external claims cited with URLs; validated against Cursor v3.6 / v2.0 docs as of 2026-07-03."
validates: SSOT__open-door-harness__v01__2026-07-03__cursor.md
sources:
  - "Cursor Hooks — https://cursor.com/docs/hooks (fetched 2026-07-03)"
  - "Cursor permissions.json — https://cursor.com/docs/reference/permissions (fetched 2026-07-03)"
  - "Cursor Run Modes + Sandbox — https://cursor.com/docs/agent/security/run-modes (fetched 2026-07-03)"
  - "Cursor Best practices for coding with agents — https://cursor.com/blog/agent-best-practices (fetched 2026-07-03)"
  - "Cursor Worktrees — https://cursor.com/docs/configuration/worktrees (fetched 2026-07-03)"
  - "InfoQ: Cursor 1.7 Adds Hooks — https://www.infoq.com/news/2025/10/cursor-hooks/ (2025-10)"
  - "GitButler: Deep Dive into new Cursor Hooks — https://blog.gitbutler.com/cursor-hooks-deep-dive"
  - "Shell command gating gist (alejo4373) — https://gist.github.com/alejo4373/ea9bc4dc47c0d13ab64a926b5e44019f"
  - "Start Debugging: Gate Cursor SDK tool calls with Auto-Review — https://startdebugging.net/2026/06/gate-cursor-sdk-tool-calls-with-auto-review-and-permissions-json/ (2026-06)"
  - "learncursor.dev: Cursor Agents (Plan/Agent/Background) — https://www.learncursor.dev/learn/cursor-agents"
  - "engincanveske: Running Parallel Agents with Git Worktree — https://engincanveske.substack.com/p/running-parallel-agents-in-cursor"
---

# Cursor Capabilities + Heavy-User Guidance for the Open-Door Harness

Purpose: bound what "the wall" can actually be on the Cursor seat, pull in what heavy users do,
and refine the SSOT so the harness stays **helpful, not restraining** — Ewan's "YOLO within hooks
and harnesses." Bottom line up front: **Cursor gives us MORE real enforcement on the Mac than the
SSOT currently claims (C-3 is outdated), and the cheapest "helpful lighting" is native Cursor
machinery (Plan Mode, native worktrees, `permissions.json`, sandbox) — not a bespoke hook wall.**

---

## 1. What Cursor hooks / permissions CAN and CAN'T do (cited)

### 1a. Hooks — the interception layer (`cursor.com/docs/hooks`)

Hooks are spawned processes, stdio JSON both ways, defined in `hooks.json` at Enterprise → Team →
Project → User priority. Two execution types: **command** and **prompt** (LLM-evaluated).

**CAN hard-block:**
| Hook | Block mechanism | Reliability |
|---|---|---|
| `beforeShellExecution` | `permission:"deny"` or **exit code 2** | Reliable — this is the workhorse gate |
| `beforeMCPExecution` | `permission:"deny"` / exit 2 (set `failClosed:true`) | Reliable |
| `preToolUse` | `permission:"deny"` (`"ask"` accepted but **NOT enforced today**) | Reliable for deny |
| `beforeReadFile` | `permission:"deny"` | **Inconsistent** — see gotcha below |
| `beforeSubmitPrompt` | `continue:false` | Reliable (desktop only) |
| `subagentStart` | `permission:"deny"` (`"ask"` treated as deny) | Reliable |

**CAN observe/modify but NOT block:** `sessionStart` (fire-and-forget — `additional_context` + `env`
injected; `continue:false` is **explicitly not enforced**, session can't be blocked), `postToolUse`
(`additional_context`, `updated_mcp_tool_output`), `afterShellExecution`/`afterFileEdit`/
`afterMCPExecution`, `stop` (can inject `followup_message` to auto-loop, cannot block), `preCompact`
/ `afterAgentResponse` / `afterAgentThought` / `sessionEnd` (pure observation).

**Hard constraints on hooks:**
- **Fail-open by default.** If a hook crashes, times out, or emits invalid JSON, *the action
  proceeds*. Security-critical hooks must set `"failClosed": true` (available on `beforeReadFile`,
  `beforeMCPExecution`, etc.). Source: `cursor.com/docs/hooks` §beforeReadFile / §Per-Script Config.
- **`beforeReadFile` deny is unreliable in practice.** Multiple practitioners report file-read denies
  triggering but being ignored by the agent in some builds; shell-exec deny is the consistent one.
  Cursor's own guidance is to treat hooks as *best-effort, not an absolute security boundary*, and
  use `.cursorignore` / rules alongside. (InfoQ 2025-10 "beta feature"; GitButler deep-dive; gist.)
- **`beforeShellExecution` matcher** matches against the full command string — good for cheap
  targeted gates (e.g. matcher `git push`, `curl|wget`). (docs §Matcher Configuration)
- **Cloud agents run PROJECT hooks only.** User-level `~/.cursor/hooks.json` is *not* loaded in cloud
  agents, and `sessionStart` / `beforeSubmitPrompt` / `stop` / MCP hooks **do not fire in cloud** at
  all. (docs §Cloud agent support)

### 1b. Permissions / auto-run / YOLO (`docs/reference/permissions`, `docs/agent/security/run-modes`)

**Run Modes** (Settings → Agents → Approvals & Execution), changelog: Auto-review shipped as default
in **v3.6, 2026-05-29**; "Ask Every Time" deprecated v3.5:
- **Auto-review** (default, = the sane "YOLO"): allowlisted calls run immediately → else sandbox
  when possible → else an LLM classifier allows/holds. **"Auto-review is not a security boundary"**
  (Cursor's own heading — the classifier can mis-allow or mis-block).
- **Allowlist**: only allowlisted actions auto-run; sandbox for the rest.
- **Run Everything**: zero prompts (true raw YOLO).

**`permissions.json`** (`~/.cursor/` machine-wide + `<project>/.cursor/`, concatenated): three
independent keys — `mcpAllowlist[]`, `terminalAllowlist[]` (command prefixes that auto-run), and
`autoRun{allow_instructions[], block_instructions[]}` (**plain-English** steering of the classifier,
Auto-review only). Defining a key **overrides** the in-app allowlist and makes the in-app editor
read-only. Only consulted when Run Mode is enabled.

**Sandbox — this is the real boundary the SSOT missed.** (`run-modes` §Sandboxing)
- **macOS: Seatbelt via `sandbox-exec`**, generated profile limits filesystem, network, process
  behaviour for the whole subprocess tree. **Cursor v2.0+, no extra setup.** Linux: Landlock+seccomp.
- Default sandbox: read/write **inside workspace only**; network **blocked by default** then opened
  by network mode + `sandbox.json` allowlist; protected paths include `.git/config`, `.git/hooks`,
  `.vscode`, `.cursorignore`, Cursor config. Commands needing full system access bypass sandbox and
  **prompt for approval**.
- `sandbox.json` controls network domains + extra readable/writable paths. **Local files cannot
  weaken team-admin or Cursor hardcoded protections** — those layer on top.
- **Standalone "other protections" that force approval even in auto modes:** Browser Protection,
  **File-Deletion Protection** (blocks auto `rm`), **External-File Protection** (blocks auto
  create/modify/delete *outside the workspace*). These are exactly the SSOT's blast-radius concerns —
  and Cursor already ships them.
- `.cursorignore` hides files from the agent entirely (the reliable read-block).

**Net capability summary for the wall:**
| SSOT wall intent | Cursor-native enforcement that actually works | Tier |
|---|---|---|
| Block writes outside blast radius | Sandbox (workspace-only FS) + External-File Protection | STRUCTURED (kernel, macOS Seatbelt) |
| Block `git push` on Mac | `beforeShellExecution` deny (matcher `git push`) | reliable hook |
| Block network beyond Net/Mesh | `sandbox.json` network allowlist (default deny) | STRUCTURED |
| Block secrets/`.git/config` reads | `.cursorignore` + sandbox protected paths | STRUCTURED-ish |
| Block file deletes | File-Deletion Protection | STRUCTURED |
| Read blast-radius wall | `beforeReadFile` deny — **unreliable**; use `.cursorignore` | INTUITED (weak) |
| Present door menu / directive | `sessionStart` `additional_context` | advisory only |
| Door reminder each turn | `beforeSubmitPrompt` append | advisory (desktop only) |

---

## 2. Heavy-user patterns to adopt (cited)

1. **Plan Mode first, save the plan** (`cursor.com/blog/agent-best-practices`, learncursor.dev).
   `Shift+Tab` → agent researches, asks clarifying Qs, produces a file+to-do plan, **waits for
   approval**, then executes. "Save to workspace" writes `.cursor/plans/*.md`. Heavy users run Plan
   on a high-reasoning model (Opus/GPT-5.x), **prune the to-dos**, then switch to a faster execution
   model. This IS Ewan's "everything with checklists" and maps cleanly onto the door's directive.
2. **Native worktrees, not bespoke plumbing** (`docs/configuration/worktrees`, best-practices blog,
   engincanveske). Cursor natively creates/manages worktrees: `/worktree`, `/apply-worktree`,
   `/delete-worktree`, `/best-of-n`, up to ~8 parallel agents, each isolated checkout+branch. This is
   Ewan's "everything on a git worktree" delivered by the product — closes the SSOT's F7/H1
   worktree-close gap for the common case.
3. **Scope narrowly with `@`-mentions + "how to verify"** (best-practices). State goal + constraint,
   point at exact files, say which tests/command prove success, start a fresh chat when context gets
   long. Enabling, not restraining — the agent farms context up front and stays on track.
4. **Nudge (probabilistic) vs gate (deterministic).** Community consensus: **rules are probabilistic
   guidance; hooks + permissions.json + sandbox are the deterministic gates.** Use rules/`sessionStart`
   context for the "lighting," reserve hard denies for the genuinely dangerous few (push, secrets,
   destroy, out-of-workspace writes). Matches Ewan's "blinkers without ceilings."
5. **`autoRun.block_instructions` for the grey zone.** Instead of hard-denying broad classes, heavy
   users write plain-English "send X through approval first" (e.g. "every command that modifies
   Kubernetes/prod resources"). Keeps YOLO fast while catching the scary calls — a softer,
   better-UX layer than a hook deny.

**Anti-patterns flagged:** two agents editing the same file → merge conflict (scope each to its own
area); trusting Auto-review/classifier as a security boundary (it isn't); relying on `beforeReadFile`
deny as a hard wall (inconsistent); building custom worktree lifecycle when native handles it.

---

## 3. Concrete refinements to the SSOT (so it stays helpful, not restrictive)

R1. **Fix C-3: the Mac DOES have a structural wall.** The SSOT (§3, lines 101–107) claims "on Mac
    there is no container boundary, so L1 hook-deny is the only wall … INTUITED." **Outdated.** Cursor
    v2.0+ ships a macOS Seatbelt sandbox (`sandbox-exec`) plus External-File / File-Deletion
    Protection. Reclassify the Mac seat: **L2 STRUCTURED wall exists today via Cursor sandbox** for
    FS-write-outside-workspace, deletes, and network. Hooks become the *complement* (door-awareness +
    the few string-matched denies), not the sole wall. This makes the harness *stronger and less
    reliant on cooperative hooks*.

R2. **Move the "read blast-radius wall" off `beforeReadFile`.** SSOT §3 assigns the read wall to
    `beforeReadFile` deny — which is unreliable. Use `.cursorignore` (+ sandbox protected paths) as
    the real read boundary; keep `beforeReadFile` as a *nudge/telemetry* only. Prevents a wall that
    silently doesn't hold.

R3. **Make doors configure `permissions.json` + `sandbox.json`, not just hook logic.** The
    highest-leverage, lowest-friction way to realise per-door blast radius is to have `door enter`
    swap in a door-scoped `permissions.json` (terminalAllowlist / autoRun) and `sandbox.json`
    (writable paths + network allowlist). This uses Cursor's own enforced surfaces instead of
    re-implementing them in `before-shell-execution.sh`. Doors become **"lighting presets," and the
    kernel does the walling.**

R4. **Adopt native worktrees for `worktree_feature`; retire bespoke close.** Let `/worktree` +
    `/apply-worktree` + `/delete-worktree` be the mechanism; the door just sets scope/reminders. The
    F7 "door closed" / H1 `gk-worktree-close.sh` gap is largely solved natively for interactive work
    — keep a custom closer only for headless/Beast runs.

R5. **Keep the wall a nudge by default; hard-deny only the Red core + push.** The phased plan (§6) is
    right. Concretely: hard-deny stays limited to git-push-on-Mac, secrets/Infisical paths, destroy
    (rm handled by File-Deletion Protection), and out-of-workspace writes (handled by sandbox).
    Everything else = `autoRun.block_instructions` (soft, plain-English) + `sessionStart` lighting.
    This is literally "YOLO within hooks and harnesses."

R6. **Split hooks project-level vs user-level for reach.** SSOT wires the harness into
    `~/.cursor/hooks.json` (user). Cloud/Beast agents won't inherit it and several events don't fire
    in cloud. Put the *enforceable* door hooks (`beforeShellExecution`, `beforeReadFile`) and
    `permissions.json`/`sandbox.json` at **project `.cursor/`** so cloud + teammates inherit them;
    keep presentation hooks (`sessionStart` menu) at user level where they actually fire.

R7. **Door menu via `sessionStart.additional_context`, reminder via `beforeSubmitPrompt`** — as SSOT
    plans. Confirmed viable and non-blocking; just don't expect `sessionStart` to *gate* anything
    (`continue:false` isn't honoured). Good: it can't accidentally lock the agent out — matches
    never-stuck default.

---

## 4. Hard Cursor constraints the Phase-0 build MUST respect

- **Hooks are fail-open unless `failClosed:true`.** Any deny that matters (push, secrets) must set
  `failClosed` or the wall evaporates on a script error.
- **`beforeReadFile` deny is not dependable.** Do not build the read wall on it; use `.cursorignore`.
- **`"ask"` is not enforced** on `preToolUse`/`subagentStart` (treated as deny or ignored). Design in
  allow/deny binary only; use `autoRun` for the "ask" grey zone.
- **User hooks don't run in cloud agents; several events (`sessionStart`, `beforeSubmitPrompt`,
  `stop`, MCP hooks) don't fire in cloud.** Door harness as user-hooks = **Mac-desktop-only**. Estate
  reach requires project-level config.
- **`permissions.json` only takes effect with a Run Mode enabled** (Auto-review / Allowlist / Run
  Everything) and, once set, makes the in-app allowlist read-only. Team-dashboard config overrides
  user+project files.
- **Auto-review classifier and permissions.json are explicitly NOT security boundaries.** The only
  real boundaries on Mac are the **sandbox (Seatbelt), `.cursorignore`, and the three Protections.**
- **Sandbox = workspace-scoped by default.** A door whose FS-write is a *subtree* of the workspace is
  free; a door needing writes to shared paths *outside* the workspace (e.g. `~/amplified-pipeline/`,
  `perplexity-inbox/`) will hit External-File Protection / sandbox and prompt — the `central_handoff`
  door must add those paths to `sandbox.json` writable list, or it will feel restrictive.
- **`git push` on Mac** already lands via Beast/Devin (AGENTS.md); the harness reinforces, doesn't
  invent, this — a `beforeShellExecution` matcher `git push` deny is cheap and correct.

---

[CLOSURE] branch=RESEARCH | proxy=none | mode=validate+refine SSOT | sources=Cursor official docs
(hooks/permissions/run-modes/worktrees/best-practices) + 4 practitioner writeups, all cited w/ URLs |
key-finding=C-3 outdated (macOS Seatbelt sandbox is a real Mac wall); read-wall must move off
beforeReadFile to .cursorignore | tier=INTUITED (synthesis)
