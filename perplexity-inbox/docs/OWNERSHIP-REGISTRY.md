# Ownership Registry — who's doing what where

**Maintainer:** cursor (registry SSOT) · **Ratifier:** Ewan · **Updated:** 2026-06-30  
**Pattern:** Every boundary artefact gets one row — no spec without an owner seat.

Prior art: `docs/UNIFIED-SENSOR-PLAN.md` §Seat ownership, `archive/master-plan__v01__2026-06-25__perplexity.md` phase owners, `docs/RELATED-WORK-MAP.md`.

---

## Registry

| ID | Artefact / boundary | Build owner | Deploy owner | Merge / push | Machine | Shared path | Status |
|----|---------------------|-------------|--------------|--------------|---------|-------------|--------|
| R-001 | **Ownership registry** (this doc) | cursor | — | cursor (M5/PR) | Mac | `perplexity-inbox/docs/OWNERSHIP-REGISTRY.md` | **IN_PROGRESS** |
| R-002 | **Vellum intent hook** (post plan before work) | cursor | — | cursor | Mac | `perplexity-inbox/.cursor/hooks/session-start-vellum-intent.py` + `hooks.install.json` | **IN_PROGRESS** |
| R-003 | **`apply_doorway`** Rust binary + verify API | **cursor (e2e)** | **cursor** | **cursor** | Mac → Beast | `~/control-centre/bin/apply_doorway` | **IN_PROGRESS** |
| R-004 | **Outbound doorway** patch drop zone + schema | **cursor (e2e)** | — | **cursor** | Mac | `outbound_doorway/` | **IN_PROGRESS** |
| R-005 | **sync_ledger_to_dbs.py** | antigravity | cascade-mac | devin | Mac Mini / Beast | `perplexity-inbox/harness/sync_ledger_to_dbs.py` | **IN_PROGRESS** (branch `task/deterministic-sync-pipeline`) |
| R-006 | **OPA shape_gate** | cursor | — | cursor | Mac | `perplexity-inbox/harness/shape_gate.py` | **DONE** (pre_client) |

---

## Rules

1. **No owner → no start.** New specs/handoffs must add a registry row before implementation.
2. **Default: one seat end-to-end.** Build + deploy + merge same owner unless Ewan splits explicitly. R-003/R-004 = antigravity e2e.
3. **Validation = scoped API + harnesses** — not another IDE reviewing the diff.
4. **Status values:** `NOT_STARTED` | `IN_PROGRESS` | `PARTIAL` | `DONE` | `BLOCKED`.
5. **Handoff:** When status changes, baton + one-line Vellum compound delta; update this table same session.
6. **Sensor visibility only** — unified sensor does not collapse ownership (`AI-NATIVE-OPERATING-MODEL`).

---

## apply_doorway (R-003 + R-004)

**Owner:** cursor (e2e) · **Crate:** `~/control-centre/crates/apply_doorway/` · **Binary:** `~/control-centre/bin/apply_doorway`

---

## Adding a row (template)

```markdown
| R-0NN | [artefact] | [build seat] | [deploy seat] | [merge seat] | [machine] | [shared path] | NOT_STARTED |
```

---

[CLOSURE] registry=OWNERSHIP-REGISTRY | tier=INTUITED | ratifier=ewan
