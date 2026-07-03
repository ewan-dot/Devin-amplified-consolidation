---
type: SSOT
title: Open-Door Harness — Single Source of Truth
slug: open-door-harness
version: v01
date: 2026-07-03
author: cursor
epistemic_tier: INTUITED
tier_reason: "Consolidation of four already-authored designs (A1 spec v02, A2 design, A3 draft rule, B1/B2/B3 doctrine+runtime) + live hooks.json ground truth. No new design invented; conflicts resolved and superseders named."
status: PROPOSAL — awaiting architect bless (7 decisions in §7)
revised: "2026-07-03 (Phase 1) — C-3 reclassified per RESEARCH__cursor-heavyuser-harness-guidance__v01 R1: the Mac seat DOES have a STRUCTURED wall (Cursor v2 Seatbelt sandbox + External-File/File-Deletion Protection). §3 layer table, the C-3 honest note, the §5 C-3 row, and the beforeReadFile read-wall all updated; new §3a on Cursor-native surfaces + the Mac-desktop-only / project-level-reach limitation added."
consolidates:
  - "A1 open-door-harness__architecture-spec__agent-doc__v02__2026-06-22__perplexity.md (canonical mechanism)"
  - "A2 DESIGN__open-door-harness__v01__2026-07-03__cursor.md (Cursor-seat work-class taxonomy + hook map + phasing)"
  - "A3 DRAFT-RULE__open-door-harness__v01.mdc (operator contract)"
  - "B1 research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26 (door doctrine)"
  - "B2 research-conclusion__doors-telemetry-completion__v01__2026-06-26 (F1–F8 completion)"
  - "B3 open-door-harness__implementation-brief__v01__2026-06-24 (Baton+RodGuard runtime; naming fix)"
  - "B4 CURSOR-HARNESS-MANIFEST.md (live installed stack) + live ~/.cursor/hooks.json"
supersedes: none outright — this is the ratifiable parent all others fold into
---

# Open-Door Harness — SSOT

**This file replaces "which design do we build?" with one answer.** The harness was designed four times
(2026-06-18 → 2026-07-03), has shippable hook code, a live installed stack, and a Vellum-primitive mapping.
Nothing here is new invention — it is consolidation + a wiring plan. Job = wire, not re-design.

---

## 1. The concept (Ewan's plain language)

It's an **open-door** system. You — the agent — look at the work in front of you and **choose which door
to enter**. The moment you step through, **exactly** the access that kind of work needs opens up, and
**nothing else**. Once inside you **can't wander off** — like the emergency floor lighting on a plane: one
lit, bounded path, so you go where you need to go and nowhere else. That is the **blast-radius wall**.

Your freedom is the **choice of door**. Don't like the access you've got? Step back out, pick a different
door — a different bounded path with different access. You **switch doors freely**; you never widen a door
mid-work. Escalation = exit + re-enter another door, never union.

The rule is **blinkers without ceilings**. The blinkers keep you focused and keep the blast radius small.
But there is **no ceiling on quality** — inside the door you do your brilliance without worrying about
anything else. A denial is never a curiosity gate; it only means *wrong door for that action — exit and
enter the one that opens it.*

Default is **never-stuck**: choose nothing and you are in `research_read` (read/think/search, no writes).
Thinking is never blocked; only *acting outside a chosen blast radius* is.

---

## 2. Unified door taxonomy

**Reconciliation (see §5 C-1):** the four sources describe doors on **two axes**. A1/B1 name doors by
Beast **system** (Brain, Research pipe, CRM, Cove, Vellum, Secrets…). A2/A3 name them by **work-class** at
the Cursor/Mac seat. These are not rivals: the **work-class doors are the operator front-end**; each maps
to the **system door(s)** it is allowed to touch on the backend. The canonical seat taxonomy is A2's
work-class set (below); the A1 system map is the enforcement target it wires onto.

Access dimensions per door: **FS-read / FS-write** (path globs) · **Net/Mesh** (none · web+searxng ·
tailnet · beast-ssh) · **MCP/tools** (allow-list) · **Git-write** (none · commit-local · push — *push is
universal-Red on Mac regardless*) · **Spend** (worker=haiku · mid=sonnet · plan-once=opus, a routing
*class* ceiling, not an effort ceiling).

| Door | Status | Purpose | FS-read | FS-write | Net/Mesh | MCP/tools | Git-write | Spend | Maps to A1/B1 system door |
|---|---|---|---|---|---|---|---|---|---|
| `research_read` | **SEED** (default) | Read / think / search; no mutation. | broad (repo + estate docs) | none | web+searxng | search, web, brain-read | none | mid | Brain(ro), Research pipe(ro) |
| `agentsmini_build` | **SEED** | Build/iterate agent code in one bounded project. | project subtree | same project subtree | none | fs, shell(build/test) | commit-local | mid | Agent sandbox / project repo |
| `central_handoff` | **SEED** | Write shared artefacts + baton/Vellum handoff (**absorbs `vellum_witness`**, see C-2). | shared paths | `perplexity-inbox/`, `amplified-pipeline/`, batons, Vellum forms | tailnet(vellum) | vellum, fs | commit-local | worker | Central data + Vellum(append-only) |
| `worktree_feature` | proposed | Feature work in an isolated worktree (from `worktree-door.mdc`). | worktree subtree | worktree subtree | none | fs, shell(test), git-local | commit-local | mid | Task worktree |
| `pipe_run` | proposed | Run the five-stage research pipe / capture. | repo + corpus | pipe run-dirs, jsonl logs | web+searxng+beast-read | search, brain, fs | commit-local | mid | Research pipe(run) |
| `config_harness` | proposed | Edit hooks/rules/harness — the sensitive door. Forces unlock→edit→re-bless→lock. | `~/.cursor/**`, repo `.cursor/**` | `~/.cursor/hooks/**`, repo `.cursor/**` | none | fs, shell(config-lock, manifest) | commit-local | plan-once | (Mac seat config; no Beast system) |

**Universal (not a door): Secrets / Infisical — NO DOOR, EVER.** No door opens `/opt/amplified/secrets`,
Infisical, or credential material. This is Ulysses-locked (A1). Also door-independent: **Destroy / Launder**
(yolo-ceilings Red core) and **git push on Mac** (AGENTS.md read-only-Mac; land via Beast/Devin PR).

Doors compose only by **exit + re-enter**, never by union. Two profiles in one job = two sequential doors
(usually a baton between them).

---

## 3. Doorkeeper + three enforcement layers

### The doorkeeper (A1 mechanism, expressed at two maturity levels)

A single trusted component owns the **one write-lease**. The agent never holds keys — it holds the *right
to request*. Opening door B **closes** door A (mutual exclusion is the invariant). Zero standing write; the
lease exists only while a door is open; **never the docker socket** (root-equivalent = red line). Every
open/close is logged to Vellum.

- **Mac-seat implementation (build now):** an **active-door marker** `~/.amplified/active-door.json`
  `{door, entered, task, seat}` = the local lease; Cursor hooks read `marker + doors manifest` on every
  boundary event and allow/deny. This is A2's marker realising A1's lease.
- **Estate-wide implementation (Beast/Vellum):** **Baton** mutex (`POST /acquire /release /status`) = the
  durable distributed lease; **RodGuard** = rod-violation circuit-breaker (B3). Same doctrine, durable plane.

### Three layers (honestly tiered)

| Layer | What it is | Mechanism | Tier | Where |
|---|---|---|---|---|
| **L2 — boundary wall** | The kernel/policy wall independent of agent behaviour | **Mac: Cursor v2 Seatbelt sandbox (`sandbox-exec`) — workspace-scoped FS, `networkPolicy` default-deny, `.cursorignore`, + External-File / File-Deletion Protection.** Beast: `:ro` bind mounts, SELECT-only DB role, detached network | **STRUCTURED** | **Present on the Mac seat today** (Cursor v2.0+, no setup) **and** Beast / Apple-Container (C-3 revised) |
| **L1 — in-process door check** | The inner blinker: pre-tool interception vs the active door | Cursor hooks read marker+manifest → `permission:deny` (fail-closed core) + `permissions.json` steering | **complement** (agent-cooperative + hook), layered on the L2 sandbox | Every seat; **presentation hooks Mac-desktop-only** (§3a) |
| **L0 — per-worktree/session binding** | The unit of work carries its own door grant | marker keyed to session/worktree; grant per thread | STRUCTURED (native in Claude Code; doorkeeper-supplied elsewhere) | All |

**Honest note (C-3, revised 2026-07-03):** the Mac seat **does** have a structural (L2) wall — Cursor v2.0+
ships a **macOS Seatbelt sandbox** (`sandbox-exec`) that limits filesystem writes to the workspace (+
`additionalReadwritePaths`), enforces a default-deny `networkPolicy`, and hides files via `.cursorignore`,
backed by standing **External-File Protection** (blocks auto create/modify/delete outside the workspace) and
**File-Deletion Protection** (blocks auto `rm`). So the **per-door blast radius is STRUCTURED on Mac**,
expressed as a door-scoped `sandbox.json` + `permissions.json` **preset** (see §3a, presets/). L1 hooks are
now the **complement** — door-awareness (menu/reminders) + a small **fail-closed** hard-deny core (Red
core + `git push`) — not the sole wall. What remains **INTUITED** on Mac: the hooks themselves are
fail-open unless `failClosed:true`, and `beforeReadFile` deny is unreliable (so the read wall lives in
`.cursorignore`, not the hook). Do not overclaim the *hook* as the wall; the *sandbox* is the wall.
(Source: RESEARCH__cursor-heavyuser-harness-guidance__v01 R1/R2, cursor.com/docs/agent/security/run-modes +
reference/sandbox, fetched 2026-07-03.)

### Concrete Cursor hook-point map (live `hooks.json` → door role)

| Hook point | Live script(s) | Door role |
|---|---|---|
| `sessionStart` | `session-start-preamble.sh`, `session-start-routing-hint.py` (+ new `session-start-doors.py`) | **Present the door menu**; read active-door marker; if none, state default `research_read`; surface the door's directive/reminders as `additional_context`. |
| `beforeReadFile` | `before-read-file.sh` | **Nudge/telemetry only (revised):** `beforeReadFile` deny is unreliable, so the **read boundary is `.cursorignore` + sandbox protected paths**, not this hook (research R2). The hook still *nudges* on out-of-door reads + keeps the noisy-path nudge; no `failClosed`. |
| `beforeShellExecution` | `before-shell-execution.sh` | **Fail-closed hard-deny core + nudge/telemetry (revised):** hard-deny only the door-independent lines — `git push`, secrets, Red core — with `"failClosed": true` in `hooks.json` (research §4). FS-write / network **blast radius is enforced by the door's `sandbox.json` preset (L2)**, not re-coded here; the hook *nudges* on door-scope misses. Token-bomb nudge unchanged. |
| `beforeSubmitPrompt` | `before-submit-prompt.sh`, `before-submit-constitutional.py` | **Ewan's-way + constitution reminder:** append the active door's reminders; P0/nudge gates unchanged. |
| `postToolUse` | `post-tool-use.sh` | **Telemetry:** witness each door-scoped action (which door, allow/deny) to `~/.amplified/logs/harness-hooks.jsonl`. Redaction unchanged. |
| `stop` | `stop.sh` | **Closure/exit:** finish-waypoint checklist (§4); confirm artefact in a shared path; clear the marker so next session re-chooses. |
| (config door) | `verify-config-integrity.py`, `config-lock.sh` | `config_harness` uses the existing unlock→edit→re-bless→lock cycle. **Ground truth:** `config-lock.sh` locks only `rules/*.mdc` (uchg); `hooks.json`+`hooks/*` are already editable. |

### Constitutional tiering (layered under every door, door-independent)

`constitutional-gate.mdc` staged modes apply *inside* every door: `pre_client` (default) warns + logs and
work completes; `client_live` hard-blocks until compliant. Doors bound **where** you may act; the seven
rods bound **what** you may do anywhere. The **Red core** (Destroy / Secrets / Launder) is door-independent
— no door ever opens it.

### 3a. Cursor-native enforcement surfaces — and the Mac-desktop-only limitation

**A door is realised as a preset of Cursor's own surfaces** (research R3), not walls re-coded in shell:

| Door dimension | Cursor-native surface | Tier | Staged at |
|---|---|---|---|
| FS-write blast radius | `sandbox.json` `type` + `additionalReadwritePaths` + **External-File Protection** | STRUCTURED | `presets/<door>/sandbox.json` |
| FS-read / secrets | `.cursorignore` + sandbox protected paths | STRUCTURED-ish | `presets/_base/cursorignore` |
| Net/Mesh | `sandbox.json` `networkPolicy` (default deny) | STRUCTURED | `presets/<door>/sandbox.json` |
| File deletes | **File-Deletion Protection** | STRUCTURED | native |
| Auto-run convenience | `permissions.json` `terminalAllowlist` | convenience | `presets/<door>/permissions.json` |
| Grey-zone "ask first" | `permissions.json` `autoRun.block_instructions` (no `terminalDenylist` exists) | soft steer | `presets/<door>/permissions.json` |
| `git push` / Red core | `beforeShellExecution` **fail-closed** deny | reliable hook | `hook_adapter.py` + `hooks-failclosed.snippet.json` |
| Door menu / reminders | `sessionStart.additional_context` / `beforeSubmitPrompt` | advisory | presentation hooks |

**"Door enter" = swap the door's `permissions.json` + `sandbox.json` into `~/.cursor/`** (placeholders bound
from the marker). The Seatbelt sandbox does the walling; the hook only hard-stops the dangerous few.

**Mac-desktop-only limitation (research R6, §4).** User-level `~/.cursor/hooks.json` and the events
`sessionStart` / `beforeSubmitPrompt` / `stop` / MCP hooks **do not fire in cloud agents** — Cloud Agents
also do not use Run Modes at all. So a door harness wired purely as *user* hooks is **Mac-desktop-only**.
For **estate / Beast / teammate reach**, the *enforceable* surfaces must live at **project level**: commit
`permissions.json`, `sandbox.json`, and the door hooks (`beforeShellExecution`, `beforeReadFile`) into the
repo's `<repo>/.cursor/` so cloud agents and other seats inherit them. Keep *presentation* hooks
(`sessionStart` door menu) at user level, where they actually fire. Team-dashboard config overrides both.
This is the deferred cross-seat lane; Phase 1 stages the presets so either home (user or project) can adopt
them without a redesign.

---

## 4. Vellum-primitive mapping + completion telemetry

**No new datastore.** The harness wires onto Vellum primitives that already ship (v0.2.0, live `vellum:8400`).

| Harness concern | Vellum primitive |
|---|---|
| Doorkeeper (write-lease) | **Baton** mutex + **RodGuard** circuit-breaker |
| Hooks | Witness sensors — one Sheet entry per allow/deny/open/close |
| Telemetry | Estate log / analytics / reputation / epistemic drift |
| Door-work | `/tasks/register`, ExecutionMode (YOLO vs HITL) by door risk class |

Two correlated planes: **Langfuse** traces model cost/latency; **Vellum** witnesses authority/door events.

**Completion telemetry (B2):** `completion_pct = jobs(ALL F1..F8 PASS) / jobs(F1 PASS) × 100`. Deterministic
booleans, not agent prose.

| # | Waypoint | PASS when |
|---|---|---|
| F1 | Door opened | `worktree_opened` / `door:open` row |
| F2 | Start sensor | `session-start` exit 0/1 |
| F3 | Work witnessed | ≥1 waypoint commit or hook line in window |
| F4 | End proof | pytest green OR `harness_selfcheck.py` GREEN OR smoke doc |
| F5 | Company share | shared path + `[CLOSURE]` in status file |
| F6 | Completion witness | Vellum completion + seat-pass if handoff |
| F7 | **Door closed** | `door:close` row — **known gap** until H1 (`gk-worktree-close.sh`) |
| F8 | Published | inbox artefact **and** GitHub pushed **and** Vellum telemetry row |

Report `completion_pct_f6` until F7/H1 ships. This is the same core `self-compound.mdc` §7 references.

---

## 5. Provenance — what each source gave, conflicts, resolution

| Source | Currency | Contributed | Supersession |
|---|---|---|---|
| **A1** spec v02 (06-22, perplexity) | canonical mechanism | Doorkeeper single-lease, never-socket, L0/L1/L2, system door map, Vellum-primitive mapping, honest tiering | **Parent.** Owns the *mechanism*. Its Mac-lane table is superseded by A2 for the seat. |
| **A2** DESIGN (07-03, cursor) | current seat framing | Work-class taxonomy + access dimensions, concrete hook map, 4-phase install-safe plan, rule reconciliation | Current for the Cursor seat; defers to A1 on doorkeeper mechanism. |
| **A3** DRAFT-RULE (07-03) | ready to install | One-page operator contract (enter/inside/switch/exit) | **Supersedes A2 on door count** (6, not 7 — see C-2). |
| **B1** doorways doctrine (06-26) | current | Door=bounded permission surface; three-name stack; gap list; H1/H2/H3 build jobs | Feeds enforcement + system map. |
| **B2** telemetry-completion (06-26) | current | F1–F8, completion formula, deterministic-core-not-LLM | Owns completion metrics. |
| **B3** impl brief (06-24) | runtime spine | Baton, RodGuard, keyholder, name-collision fix | Owns runtime + the rename gate. |
| **B4** manifest + live `hooks.json` | live ground truth | The 9 wired hooks, push-door philosophy, what is actually installed | The reality all plans must be install-safe against. |

**Conflicts resolved:**

- **C-1 Door axis (system vs work-class).** *Resolution:* keep both — work-class doors (A2) are the seat
  front-end, each mapping to A1/B1 system doors on the backend (mapping column in §2). Not a contradiction.
- **C-2 Door count (7 vs 6).** DESIGN lists 7 (incl. `vellum_witness`); DRAFT-RULE lists 6. *Resolution:*
  **6 canonical** — fold `vellum_witness` into `central_handoff` (ledger writes always co-occur with
  handoff). **A3 supersedes A2** here.
- **C-3 What is "the wall".** A1: L2 container boundary is the wall, hooks are bonus. A2: the hook denial
  *is* the wall. *Resolution (revised 2026-07-03, research R1):* **the Mac DOES have an L2 wall** — Cursor
  v2.0+ macOS **Seatbelt sandbox** (`sandbox-exec`) + External-File / File-Deletion Protection. So the
  per-door blast radius is **STRUCTURED on Mac**, expressed as a door-scoped `sandbox.json` + `permissions.json`
  **preset** (§3a). Hooks are the **complement**: door-awareness + a small **fail-closed** hard-deny core
  (Red core + `git push`). What stays INTUITED: hooks are fail-open unless `failClosed:true`, and
  `beforeReadFile` deny is unreliable (read wall → `.cursorignore`). Beast/Apple-Container L2 remains the
  durable estate plane. The earlier "no L2 on Mac / hook-deny is the only wall" claim is **superseded**.
- **C-4 Naming collision.** `amplified_harness.py` (permission *classifier*) ≠ open-door *runtime*
  (Baton+RodGuard). *Resolution (B3, do first):* rename classifier → `amplified_permissions.py`; runtime →
  `open_door_runtime/`. Cheapest highest-value fix; blocks a phantom layer.
- **C-5 Doorkeeper location.** A1: dumb trusted component holding the lease. A2: marker + hooks. *Resolution:*
  same mechanism, two maturity levels — marker+hooks = Mac-seat lease (Phase 1); Baton on Vellum = durable
  estate lease (B3). Marker is local, Baton is distributed.

---

## 6. Install-safe phased wiring plan

Constraint: hooks/harness are under active development; **rules are integrity-locked** (`config-lock.sh`
uchg on `rules/*.mdc` only). Every `~/.cursor/` change follows the cycle — and **rule (`.mdc`) changes need
the unlock; hook-script changes do not** (they are already editable):

```
~/.cursor/hooks/config-lock.sh unlock      # ONLY needed for rules/*.mdc edits
<edit hooks/scripts freely; edit rules only after unlock>
python3 ~/.cursor/hooks/update-config-manifest.py
~/.cursor/hooks/config-lock.sh lock
```

| Phase | Slice (smallest-safe first) | `~/.cursor/` touch | Risk |
|---|---|---|---|
| **0 — SSOT only** *(this file)* | Ship this SSOT + add doors manifest `perplexity-inbox/config/doors-v1.json` (proposed, not wired), mirroring `fleet-routing-v1.json`. Do the **C-4 rename first** in repo. | none | zero |
| **1 — Presentation only** | Add `session-start-doors.py` (reads manifest + marker, prints menu/directive as `additional_context`) + a `door` CLI (`enter/exit/status` writes the marker). **No denials.** | hooks only (no unlock) | ~zero — advisory |
| **2 — Soft wall (nudge)** | Extend `before-shell-execution.sh` + `before-read-file.sh` to compute in/out-of-scope vs active door and **nudge** (still allow). Collect `harness-hooks.jsonl` to measure false-block rate. | hooks only | low |
| **3 — Hard wall (deny), cheapest doors first** | Flip out-of-scope → `permission:deny` for `research_read` + `config_harness` first (clearest scopes, highest value). Deny message always carries the exit/re-enter remedy. | hooks only | medium — gated by Phase-2 data |
| **4 — Generalise + closure** | Roll deny to remaining doors; wire `stop.sh` to clear marker at finish-waypoint (F7); build `gk-worktree-close.sh` (H1). **Install the blessed rule** (`open-door-harness.mdc`) — requires unlock→bless→lock. | hooks + **rule (unlock)** | medium |

Each phase is independently shippable and reversible. The rule install (Phase 4) is the only step needing
the rule unlock and architect bless.

---

## 7. Decisions Ewan must make (recommended defaults)

| # | Decision | Recommended default | One-line rationale |
|---|---|---|---|
| **D1 (KEY)** | **`config_harness`: agent-enterable vs architect-only?** | **Agent-enterable for hook/script edits** via unlock→edit→re-bless→lock; **rule (`.mdc`) changes still require architect bless** (a second key). | Agents fix their own rails fast (hooks are already unlocked); the constitution stays Ulysses-locked so no agent can self-rewrite the rules that bind it. |
| D2 | Canonical door count — which proposed doors ship in v1? | **6:** 3 seed + `worktree_feature` + `config_harness`; **defer `pipe_run`**; **fold `vellum_witness` into `central_handoff`** (C-2). | Fewest doors that cover today's work; ledger writes always co-occur with handoff, so no separate door. |
| D3 | Wall hardness — hard `deny` or strong nudge? | **Nudge through Phase 2; hard-deny `research_read` + `config_harness` first (Phase 3).** | Measure the false-block rate before committing the wall; matches the push-door "nudge-before-deny" philosophy. |
| D4 | Default door | **`research_read`** | Never-stuck read-only default; thinking is never blocked, only acting outside a chosen blast radius. |
| D5 | Active-door marker location | **`~/.amplified/active-door.json`** (not `~/.cursor/ACTIVE_DOOR`) | Keeps door state out of the integrity-locked tree (no config-lock churn); mirrors the `vellum_session` marker pattern. |
| D6 | Doors manifest home | **`perplexity-inbox/config/doors-v1.json`** | Mirrors `fleet-routing-v1.json` SSOT; shared path, not worktree-only. |

**Also pending before any build (not a taxonomy choice, but a gate):** the **C-4 rename**
(`amplified_harness.py` → `amplified_permissions.py`; runtime → `open_door_runtime/`) is a prerequisite —
do it in Phase 0 to avoid a phantom layer.

---

[CLOSURE] branch=PLAN | proxy=none | mode=consolidate+wire (no new design) | conflicts-resolved=C1–C5 |
gaps=network leg (INTUITED, Devin), per-DB roles (Devin), F7 door-close (H1) | tier=INTUITED (consolidation)
