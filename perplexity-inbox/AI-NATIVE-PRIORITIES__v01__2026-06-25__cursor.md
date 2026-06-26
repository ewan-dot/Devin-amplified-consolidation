# AI-Native Priorities — Done vs Open

**For:** Ewan · **Seat:** cursor · **Date:** 2026-06-25 · **Tier:** INTUITED

Plain-language view of what landed in `perplexity-inbox/` on 25 Jun and what still needs a seat.

---

## Done (on disk — verified)

| Item | Evidence | Seat |
|---|---|---|
| **Track A — Mac unified sensor** | `unified_sensor/`, `monitor.py`, `tests/` (6 green), `data/sensor_snapshot.json` | cursor |
| **Track A summary doc** | `completed-by-cursor__2026-06-25/SUMMARY__unified-sensor-track-a__2026-06-25__cursor.md` | cursor |
| **Operating model** | `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md` | cursor |
| **Unified sensor plan + checklist** | `docs/UNIFIED-SENSOR-PLAN.md`, `unified-sensor__plan-and-checklist__v01__2026-06-25__cursor.md` | cursor |
| **Related work map** | `docs/RELATED-WORK-MAP.md` | cursor |
| **Master plan (Phase 0–7)** | `master-plan__v01__2026-06-25__perplexity.md` | Perplexity |
| **v03 witness doctrine** | `vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md` | Perplexity |
| **Tarball extraction** | `signal-reading-bundle/`, `prior-art-syntheses-bundle/` (8 pairs + INDEX) | Perplexity → cursor extract |
| **Worktree** | `.worktrees/feat-unified-sensor` on `feat/unified-sensor` | cursor |
| **Jun-25 plan stack** | pipe-weld brief, control-centre prior-art, beast tailscale recovery plan | Perplexity |
| **Standing grants** | `amplified_permissions.py` + `amplified_rules.json` (live, pre-dates this thread) | Perplexity |

---

## Open — seat pickup gaps

### Needs Ewan (blocks ordering)

1. **Phase 0 baton** — Mac mini hub vs peer · Cove vs CRM Infisical order · Presidio now vs Phase 5
2. **Signal-reading baton** — baseline window · drift method · false-halt budget
3. **Ops clicks** — merge agent-claude PR#1 · GitLens env · corpus reorg go/no-go

See also: `EWAN-DECISIONS-CONSOLIDATED__v01__2026-06-26.md` (deduplicated hand-back from cascade-mac).

### Cascade-Mac — Track B Phase 1

- Extend `@vellum.witness` on Beast per v03 doctrine
- Unit tests for five trial boundaries
- Hand deploy to Devin (Mac read-only for push)

### Claude Code — Phases 2 + 3

- **Phase 2:** Pipe weld (`staging_emitter.py` → perplexity-ingest → brain drainer)
- **Phase 3:** Job-start hook → `friction_monitor.sql` → proceed/warn/halt

### Perplexity — adoption

- Read `monitor.py --signals-only` or `data/sensor_snapshot.json` at every session start
- Phase 4 trial evaluation after Phases 2 + 3 live

### Devin — deploy

- Merge `feat/unified-sensor` branch
- Beast service deploy for decorator + hook when ready

### Still spec-only (no code yet)

| Phase | What |
|---|---|
| 4 | One-week witness trial + 4 acceptance criteria |
| 5 | Infisical migration (after Phase 4) |
| 6 | Scale to ~20 boundaries |
| 7 | Data lake build |

### Jun-24 backlog (unchanged)

13+ threads from `INBOX-INDEX__v01__2026-06-24__perplexity.md` remain open — JWT recovery, VSCodium lane, relay protocol, etc. Jun-25 work does not close that backlog; see v02 index for how threads relate.

---

## Priority order (recommended)

1. Ewan Phase 0 (3 lines) — unblocks security migration ordering
2. Perplexity adopts Track A snapshot at job-start (zero-code habit)
3. Cascade-Mac Phase 1 decorator (unblocks hook)
4. Claude Code Phase 2 pipe weld (closes research→brain loop)
5. Claude Code Phase 3 hook
6. Phase 4 trial → then Phases 5–7

---

## Done ladder check (Track A)

| Level | Track A status |
|---|---|
| **Minimum (shared)** | ✅ Code + docs in `perplexity-inbox/` |
| **Preferred (working)** | ✅ Tests green; `monitor.py` runs; snapshot on disk |
| **Ideal (adopted)** | ❌ Perplexity job-start habit · ❌ Vellum `witness_read` · ❌ Beast deploy |
