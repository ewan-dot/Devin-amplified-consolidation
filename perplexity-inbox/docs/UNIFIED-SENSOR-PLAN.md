# Unified Sensor — Plan, Checklist, Waypoints, Success

**Worktree:** `/Users/ewansair/ingestion-to-research-pipe/.worktrees/feat-unified-sensor` (`feat/unified-sensor`)  
**Canonical doctrine:** `vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md`  
**Master sequence:** `master-plan__v01__2026-06-25__perplexity.md`  
**Mac Python module (local gather):** `perplexity-inbox/unified_sensor/`

---

## Operating model

**Hooks and harnesses are the whole point** — they enable independent IDE/AI work without constant coordination. AIs work **independently**, **finish** work, **then share** it. Work produced becomes **owned by the company, available to everybody** (shared folder or Vellum).

Each seat owns a project **end-to-end**: spec → working code → tests → shared artefact. Unified sensor adds **cross-IDE visibility** (one health snapshot, proceed/warn/halt) — it does **not** replace seat ownership. If your boundary breaks, your seat fixes it; the sensor makes that visible to everyone else.

**Done ladder** (shared is the floor, not the goal):

| Level | Meaning |
|---|---|
| **Minimum** | Shared — artefact in shared path or Vellum entry; company can find it |
| **Preferred** | Working — tested, functional, end-to-end where applicable |
| **Ideal** | Witnessed + adopted — another seat or hook actually uses it |

Full plain-language version: `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`

**Shared (all seats read/write here):**

| Location | What lives here |
|---|---|
| `~/amplified-pipeline/` | Multi-agent workspace — seat subfolders (`cursor/`, `cascade-mac/`, …) plus shared `data/` |
| `perplexity-inbox/` | Forward specs, Track A module, `data/sensor_snapshot.json`, tests |
| `~/control-centre/` | Deterministic collectors + rules engine (Track A bridge) |
| Vellum ledger | Witness rows, baton, task queue — attributed writes, fleet-wide read |
| Beast `/opt/amplified/` | Decorator, friction_monitor, pipe services — deploy via Cascade-Mac/Devin, not Mac push |

**IDE-local (seat owns, not the shared contract):**

- Worktrees, branch checkout, IDE rules (`.cursor/`, Claude Code config, etc.)
- In-progress drafts until promoted to a shared path above
- Perplexity Computer workspace when running inside its own IDE shell

**How unified sensor fits:** Track A (Mac gather) and Track B (Beast witness + hook) are separate deliverables with separate owners. Perplexity **reads** the snapshot at job-start; it does not gather or witness on others' behalf. Visibility without collapsed responsibility.

---

## Seat ownership

| Seat | E2E deliverable | Shared output path | Done (preferred = working) |
|---|---|---|---|
| **Cursor** | Track A — Mac `unified_sensor/` gather + decision CLI | `perplexity-inbox/unified_sensor/`, `perplexity-inbox/monitor.py`, `perplexity-inbox/data/sensor_snapshot.json`, `perplexity-inbox/tests/` | `python3 monitor.py` smoke pass; unit tests green; Perplexity job-start doc points at snapshot path |
| **Cascade-Mac** | Track B Phase 1 — extend `@vellum.witness` on Beast | Beast `/opt/amplified/vellum/` (PR via worktree pattern); tests in fleet-vellum repo | Decorator matches v03; unit tests for five trial boundaries; hand deploy to Devin |
| **Claude Code** | Phase 2 pipe weld + Phase 3 job-start hook | research-pipe `staging_emitter.py`; Beast hook → `friction_monitor.sql` | W1–W3 live (pipe-weld brief); hook emits proceed/warn/halt at job-start on five boundaries |
| **Perplexity** | Canonical reader + Phase 4 trial evaluation | Reads `perplexity-inbox/data/sensor_snapshot.json`; SSOT plans in `perplexity-inbox/` | Session log shows snapshot read before work; weekly trial metrics (coverage, latency, weak-signal) |
| **Devin** | Beast git push + deploy | GitHub `fleet-clean-build` / fleet-vellum merges | PR merged; services live on Beast |
| **Antigravity** | Phase 5 deployment assist (with Cascade-Mac) | Infisical migration surfaces per Pillar 4 | After Phase 4 trial passes — not before |
| **Ewan** | Phase 0 baton (three one-line decisions) | `~/Code/FACILITATOR-COCKPIT.md` baton | Mini hub vs peer; Cove vs CRM Infisical order; Presidio now vs Phase 5 |

Mac remains **read-only for git push**; Beast-landing work routes through Cascade-Mac worktree → Devin.

---

## What success looks like (plain language)

Perplexity can start every job by reading **one deterministic snapshot** of fleet health — Vellum, ingest, mesh, credentials, and the rest — and get a clear **proceed / warn / halt** with no LLM in the gather path. Every important boundary writes a witness to Vellum. After one week of real traffic, we can prove ≥95% coverage, ≤1% latency overhead, and at least one weak-signal catch.

---

## Architecture

```
Deterministic write layer          Read/monitor layer (Mac + Perplexity)
─────────────────────────          ───────────────────────────────────
Falco, Tetragon, osquery, Santa  →  @vellum.witness decorator (Beast)
OTel, Langfuse, Opik             →  friction_monitor.sql (Beast)
Five trial boundaries            →  unified_sensor/ (Mac: collect + decide)
                                   →  Perplexity job-start hook (canonical reader)
```

**Two tracks — do not conflate:**

| Track | Where | Owner |
|---|---|---|
| **A — Mac gather module** | `unified_sensor/` | Cursor / Mac seats |
| **B — Beast witness + hook** | `fleet-vellum` decorator + job-start | Cascade-Mac → Beast via Devin |

Track A feeds Perplexity today; Track B is Phases 1–4 of the master plan.

---

## Waypoints (gates — do not skip)

| WP | Gate | Must be true before next |
|---|---|---|
| **WP0** | Tarballs extracted; v03 promoted | Planning / checklist usable |
| **WP1** | Ewan Phase 0 baton (3 lines) | Phase 5 security migration ordering |
| **WP2** | `unified_sensor` smoke test passes on Mac | Perplexity reads local snapshot |
| **WP3** | `@vellum.witness` extended on Beast (Phase 1) | Job-start hook (Phase 3) |
| **WP4** | Pipe weld live (Phase 2) | Trial traffic on ingest boundaries |
| **WP5** | Job-start hook wired (Phase 3) | One-week trial (Phase 4) |
| **WP6** | Trial acceptance (4 criteria in v03) | Scale to ~20 boundaries (Phase 6) |

---

## Checklist

### Extract & orient
- [x] Extract `signal-reading-bundle__2026-06-25.tar.gz`
- [x] Extract `prior-art-syntheses-bundle__2026-06-25.tar.gz`
- [x] Promote v03 doctrine to inbox root
- [x] Create worktree `feat/unified-sensor`
- [ ] Ewan Phase 0 decisions (master-plan §Phase 0)
- [ ] Signal-reading baton: baseline window, drift method, false-halt budget

### Track A — Mac `unified_sensor/` (Perplexity monitor input)
- [x] `registry.py` — sensor catalogue
- [x] `bridge.py` — control-centre integration
- [x] `local_collectors.py` — Vellum, inbox, tailscale, credentials fallbacks
- [x] `snapshot.py` — merge + JSON output
- [x] `signal_reader.py` — proceed/warn/halt matrix
- [x] CLI entrypoint (`monitor.py` + `python3 -m unified_sensor --local-only`)
- [x] Unit tests (`tests/test_unified_sensor.py` — 6 passing)
- [ ] Perplexity job-start doc: where to read `data/sensor_snapshot.json`
- [ ] Emit `witness_read` to Vellum at session start (when hook exists)

### Track B — Beast witness stack (master-plan Phases 1–4)
- [ ] Cascade-Mac worktree on `fleet-vellum` — extend `decorator.py` per v03
- [ ] Unit tests for five trial boundaries
- [ ] Wire job-start hook → `friction_monitor.sql` (not cron)
- [ ] Phase 2 pipe weld (parallel — not blocked by WP1)
- [ ] One-week trial + measure coverage/latency/readership/weak-signal

### Coordination
- [ ] Read `docs/RELATED-WORK-MAP.md` before duplicating work
- [ ] Map Jun-24 `vellum-senses` brief → `sensor_event.py` (supplement, not replace)
- [ ] Hand Beast deploy to Devin (Mac read-only for push)

---

## Success criteria (testable)

| # | Criterion | How to verify |
|---|---|---|
| 1 | Deterministic gather | `collect_snapshot()` returns JSON with no LLM call; reproducible fields |
| 2 | Decision matrix | `read_signals()` returns `proceed` \| `warn` \| `halt` with reason |
| 3 | Critical source coverage | All `CRITICAL_SOURCES` in registry present in snapshot or flagged missing |
| 4 | Perplexity reads at job-start | Session log shows snapshot read before work (Phase 3+) |
| 5 | Witness coverage ≥95% | Cascade-Mac measure during Phase 4 trial |
| 6 | Latency overhead ≤1% | Decorator benchmark during Phase 4 |
| 7 | ≥1 weak-signal catch | Trial week documents one halt/warn that prevented drift |

---

## Blockers needing Ewan

1. **Phase 0** — Mac mini hub vs peer; CRM vs Cove Infisical order; Presidio now vs Phase 5  
2. **Signal-reading** — cold-start baseline (30d vs 7d); ADWIN vs Shewhart; false-halt budget  
3. **Mac push** — decorator/hook lands via Cascade-Mac/Beast, not Mac git push  
4. **WanMin** — may be off; Pillar 4 assumes always-on edge sensor if hub model chosen
