# Track A Complete — Unified Sensor (Mac Gather)

**Author:** cursor · **Date:** 2026-06-25 · **Tier:** INTUITED (AI-authored summary; collector output is MEASURED/STRUCTURED)

---

## For Ewan (plain language)

Cursor built the **Mac-side health checker** for the fleet. One command gathers signals from Vellum, the ingest pipe, Tailscale, credentials, and the inbox — then says **proceed**, **warn**, or **halt**. No AI in the gather path. Six unit tests pass. A live snapshot from 25 Jun is on disk.

**What this is not:** Beast witness wiring, the job-start hook, or Perplexity actually reading the snapshot at session start — those are still open (Track B + adoption).

---

## What was built

### Python module — `unified_sensor/`

| File | Role |
|---|---|
| `registry.py` | Sensor catalogue (9 sources); marks critical vs optional |
| `bridge.py` | Bridges to `~/control-centre/` collectors + rules engine when present |
| `local_collectors.py` | Always-on Mac probes: Vellum /health, ingest /health, inbox stats, nest log age |
| `snapshot.py` | Merges control-centre + local events → unified JSON snapshot |
| `signal_reader.py` | Deterministic proceed / warn / halt decision matrix |
| `__init__.py` | Public API: `collect_snapshot`, `write_snapshot`, `read_signals` |
| `__main__.py` | Module CLI (`python3 -m unified_sensor`) |

### CLI entrypoints

| File | Role |
|---|---|
| `monitor.py` | Primary Perplexity-facing CLI — terminal render, JSON, signals-only |
| `tests/test_unified_sensor.py` | 6 stdlib-only unit tests (no network) |

### Data

| Path | Role |
|---|---|
| `data/sensor_snapshot.json` | Last collected snapshot (2026-06-25T10:17Z; backend: control-centre) |

### Docs (same session)

| Path | Role |
|---|---|
| `docs/UNIFIED-SENSOR-PLAN.md` | Seat ownership, checklist, waypoints, success criteria |
| `docs/RELATED-WORK-MAP.md` | Reuse map — what exists elsewhere, conflict risks |
| `docs/INBOX-STATUS.md` | Finished / in progress / blocked snapshot |
| `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md` | How fleet work runs — hooks, done ladder |
| `unified-sensor__plan-and-checklist__v01__2026-06-25__cursor.md` | Entry index for unified sensor thread |
| `master-plan__v01__2026-06-25__perplexity.md` | Phase 0–7 sequence (Perplexity SSOT) |
| `vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md` | Canonical witness spec (v01/v02 = audit trail) |

### Extracted bundles (tarballs removed after extract)

| Path | Contents |
|---|---|
| `signal-reading-bundle/` | v03 doctrine copy + signal-reading prior-art pair |
| `prior-art-syntheses-bundle/` | 8 paired synthesis files + INDEX |

### Worktree

| Path | Branch |
|---|---|
| `/Users/ewansair/ingestion-to-research-pipe/.worktrees/feat-unified-sensor` | `feat/unified-sensor` |

Mac is read-only for git push — worktree holds Track A code until Devin/Cascade-Mac merge.

---

## How to run

From `perplexity-inbox/`:

```bash
# Full collect + terminal summary (fast mode — critical collectors only)
python3 monitor.py

# Perplexity job-start shape — decision JSON only
python3 monitor.py --signals-only

# Full snapshot as JSON
python3 monitor.py --json

# Re-collect and persist snapshot file
python3 monitor.py --write-snapshot

# Read last snapshot without re-collecting (uses data/sensor_snapshot.json)
python3 monitor.py --no-collect --signals-only

# Slow mode — all GitHub org repos (~5 min)
python3 monitor.py --full

# Local collectors only — skip control-centre (works without ~/control-centre/)
python3 -m unified_sensor --local-only --json

# Run unit tests
python3 -m pytest tests/test_unified_sensor.py -q
```

Exit codes: `0` = proceed · `1` = warn · `2` = halt.

---

## What works vs spec-only

### Works (verified on disk)

- [x] `unified_sensor/` module — all 7 Python files present
- [x] `monitor.py` CLI — collect, render, JSON, signals-only, no-collect, write-snapshot
- [x] `python3 -m unified_sensor --local-only` — module CLI
- [x] Bridge to `~/control-centre/` when directory exists (fast + full modes)
- [x] Local fallbacks when control-centre absent
- [x] `read_signals()` → proceed / warn / halt with reason
- [x] 6 unit tests green (`pytest tests/test_unified_sensor.py`)
- [x] Live snapshot in `data/sensor_snapshot.json` (22 events, 6 sources at last run)
- [x] Planning stack: master-plan, v03 doctrine, bundles extracted, worktree created

### Spec-only (not implemented in this track)

- [ ] `@vellum.witness` decorator extension on Beast (Track B — Cascade-Mac)
- [ ] Job-start hook → `friction_monitor.sql` (Phase 3 — Claude Code)
- [ ] Pipe weld in `staging_emitter.py` (Phase 2 — Claude Code)
- [ ] Perplexity reads snapshot at every session start (adoption habit)
- [ ] `witness_read` Vellum row at session start
- [ ] One-week trial + acceptance metrics (Phase 4)
- [ ] Phases 5–7 (Infisical migration, scale boundaries, data lake)

---

## Last snapshot state (2026-06-25)

At collection time the sensor correctly reported **halt** — Beast ingest unreachable, Beast offline in Tailscale mesh. This is expected behaviour when Beast was down; the sensor is working as designed.

---

## Seat ownership handoff

| Seat | Next deliverable | Where |
|---|---|---|
| **Perplexity** | Read `data/sensor_snapshot.json` or `monitor.py --signals-only` at job-start | This inbox |
| **Cascade-Mac** | Track B Phase 1 — extend `@vellum.witness` per v03 | Beast `/opt/amplified/vellum/` via worktree → Devin |
| **Claude Code** | Phase 2 pipe weld + Phase 3 job-start hook | research-pipe + Beast hook |
| **Devin** | Merge `feat/unified-sensor` + deploy Beast services | GitHub PR |
| **Ewan** | Phase 0 baton (3 one-line decisions) | See `master-plan__v01__2026-06-25__perplexity.md` §Phase 0 |

**Cursor Track A status:** shared + working + tested. Adoption (Perplexity habit + Vellum witness) is the remaining gap before "ideal" on the done ladder.

---

## Related

- Operating model: `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`
- Priorities (done vs open): `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md`
- Inbox index: `INBOX-INDEX__v02__2026-06-25__cursor.md`

**GitHub:** [PR #1](https://github.com/ewan-dot/Devin-amplified-consolidation/pull/1) · branch `feat/unified-sensor-inbox` · commit `341c296`
