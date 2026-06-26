---
title: "Doors, Telemetry, and Completion %"
document_type: research_conclusion_addendum
artifact_id: research-conclusion__doors-telemetry-completion__v01__2026-06-26__cursor
date_utc: 2026-06-26
project: Amplified Partners
author: cursor
reader: ewan
parent: research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor
epistemic_tier: STRUCTURED
tier_reason: "Verified inbox docs + session-start + Phase 0 harness + §9. Dashboard wiring INTUITED."
ratifier: Ewan
---

# Doors, Telemetry, and Completion %

**Addendum to:** [`research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor.md`](research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor.md)

## TL;DR

**STRUCTURED:** Ewan's central deterministic core is the measurement layer behind every door. Harnesses fire when a job opens; each fire writes a Vellum event (or queues offline). The core counts booleans — not agent prose — into **completion %**: opened jobs that pass every finish waypoint. **INTUITED:** A building register — every door swipe logged; "finished completely" means every exit checkpoint is green.

---

## 1. Door open → hook → Vellum → metric

**STRUCTURED:**

```
door opens (session-start / gk-worktree-start)
  → hook fires (SessionStart, PreToolUse, @witness_stage, door:open)
  → Vellum row (worktree_opened, verdict, stage start/complete/fail)
  → metric (collector reads ledger + logs → dashboard)
```

| Stage | Fires | Records |
|---|---|---|
| Seat open | `scripts/session-start.sh` | verdict `proceed`/`warn`/`halt`; permissions pass/fail |
| Worktree | `gk-worktree-start.sh` | `door:open` — repo, branch, lane |
| Harness | 7 hooks → `harness-hooks.jsonl` | every allow/deny/error line |
| Beast pipe | `@witness_stage` (`telemetry.py`) | heartbeat 60s; boundary start/complete/fail |
| Pre-failure | `friction_monitor.sql` | sequence drift, latency, drop-rate |

Beast down → `~/.pending-vellum-queue`; events count once replayed.

---

## 2. "Job finished completely"

**STRUCTURED:** Every finish-waypoint boolean must PASS. Partial credit does not exist.

| # | Waypoint | PASS when |
|---|---|---|
| F1 | Door opened | `worktree_opened` / `door:open` row |
| F2 | Start sensor | `session-start` exit 0 or 1 |
| F3 | Work witnessed | ≥1 waypoint commit or hook line in window |
| F4 | End proof | pytest green OR `harness_selfcheck.py` GREEN OR smoke doc |
| F5 | Company share | shared path + `[CLOSURE]` in status file |
| F6 | Completion witness | Vellum completion + seat-pass if handoff |
| F7 | Door closed | `door:close` row — **gap** until H1 |
| F8 | Published | inbox artefact **and** GitHub pushed **and** Vellum telemetry row |

**INTUITED:** Missing F5/F6/F8 = unfinished — same spirit as §9 item 8 (unfinished work surfaces on the board). Recipe books use six slots (start / finish / waypoints / good / bad / hooks); each maps to booleans.

---

## 3. Deterministic core vs LLM (min-rule)

**STRUCTURED:**

| Code measures | Capped INTUITED |
|---|---|
| Exit codes, hook jsonl lines, Vellum hashes | "Looks good" in chat |
| pytest pass/fail, sensor GREEN/RED | Agent self-report MEASURED |
| `friction_monitor.sql` results | Prose quality, vibe-done |

Ambiguous deterministic cores → tier cap INTUITED (`epistemic_tier.py`). Permissions never LLM-classified.

---

## 4. Completion % formula

```
completion_pct = jobs(ALL F1..F8 PASS) / jobs(F1 PASS) × 100
```

- Denominator: open events in window (Vellum + task id).
- Numerator: F2–F6 all PASS; report `completion_pct_f6` until F7/H1 ships.
- Slice: lane, door, 7d/30d.
- **MEASURED** only after deterministic collector + independent re-verify; design today = **STRUCTURED**.

Estate token programme §9 PROOF-OF-LIFE = same philosophy fleet-wide — 10 booleans, one captured run (`token-efficiency__estate-spec__finish-and-prove__v01__2026-06-23__perplexity.md` §9; ratified EWAN-DECISIONS #16).

---

## 5. When completion % drops — tweak the failing stage

| Pattern | Fail | Fix |
|---|---|---|
| No F6 | Skip Vellum done | `inbox-finish-and-testing.mdc`; session-end witness |
| F4 red | Skip tests | `harness_selfcheck.py` must show RED |
| F2 halt | Fleet sick | `session-start.sh` / `monitor.py` inputs |
| F3 empty | No commits | `wp(<task>):` cadence (doors doc §4) |
| F5 missing | Worktree-only | Promote to inbox/pipeline |
| F7 gap | Open, no close | H1 `gk-worktree-close.sh` |
| F8 missing | Not published | inbox artefact + GitHub push + Vellum telemetry row |
| Pipe drift | Bad sequence | `friction_monitor.sql` Query 4 |

**INTUITED:** Heartbeat stops mid-job → fix Beast telemetry before re-running the LLM step.

---

## 6. Existing links

| Piece | Role |
|---|---|
| `scripts/session-start.sh` | Job-open sensor 0/1/2 |
| `monitor.py` / `unified_sensor/` | proceed/warn/halt Track A |
| `harness_selfcheck.py` | hooks GREEN or RED |
| `friction_monitor.sql` (Beast) | pre-failure maths |
| §9 PROOF-OF-LIFE | estate done = proven |
| `DOCTRINE__equal-flaws-failure-aware__2026-06-26__ewan.md` | core serves all legs |

**INTUITED next:** one collector — Vellum + jsonl + `[CLOSURE]` → weekly `completion_pct`.

---

## 7. Compound signal (self-compound harness)

**STRUCTURED:** Encoded in `self-compound.mdc` + stop hook `stop-self-compound-check.py`.

| Signal | Direction | Meaning |
|---|---|---|
| New failure patterns in research | ↓ over time | **Good** — gaps closing, fleet learning encoded |
| Same topic re-researched without implement | ↑ | **Bad** — token waste, chat-only fixes |
| Repeated hook failures on encoded gaps | ↑ | **Bad** — SSOT not deployed or not read |
| Completion % ↑ + token cost per completed job ↓ | ↑ / ↓ | **Good** — moving toward goal |

Before research: check inbox + Vellum for prior same-topic runs. After gap fix: encode in rules/hooks/repo same session; post Vellum compound delta one-liner.

---

[CLOSURE] branch=PLAN | proxy=none | gates=Ewan reads completion model | inbox=research-conclusion__doors-telemetry-completion__v01__2026-06-26__cursor.md | tier=STRUCTURED
