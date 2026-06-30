# AI-Native Operating Model

**For:** Ewan (architect) · **Seat:** cursor · **Date:** 2026-06-25

---

## In one paragraph

Multiple AIs and IDEs work **independently** on their own projects. **Hooks and harnesses** let them do that without stepping on each other. When a seat **finishes**, the work becomes **company property** — placed in a **shared folder** or **Vellum** so everyone can use it. Sharing is the **minimum** bar for "done"; the **goal** is something that **works** end-to-end. Unified sensor adds fleet **visibility**; it does not take away who owns the fix.

---

## How work flows

1. **Pick up** — run `./scripts/session-start.sh`; post intent to Vellum (paste verdict line).
2. **Work independently** — in your IDE, worktree, or seat shell. Drafts stay local until finished.
3. **Finish** — working code, tests where they matter, smoke check ("does it run?").
4. **Share** — promote artefact to a shared path; witness on Vellum; fill seat-pass if handing off.
5. **Others adopt** — no re-doing the same work; read from shared surface.

**Not:** stop at "I'll share it later" or treat posting to Vellum as the whole job.

---

## Done ladder

| Level | What it means | Example |
|---|---|---|
| **Minimum (floor)** | Artefact in a shared path **or** Vellum entry — company can find it | Spec in `perplexity-inbox/`, witness row posted |
| **Preferred (target)** | **Working** — tested, functional, end-to-end where applicable | `python3 monitor.py` passes; 6 unit tests green |
| **Ideal** | Witnessed **and** adopted — another seat or hook actually uses it | Perplexity reads snapshot at job-start; Beast deploy live |

Shared is the **gate**, not the **finish line**.

---

## Hooks and harnesses (first-class)

These exist so seats can work alone and still stay aligned:

| Piece | Role |
|---|---|
| **`scripts/session-start.sh`** | Deterministic session opening — permissions gate + sensor + inbox paths; exit 0/1/2 |
| **`monitor.py`** | Fleet health snapshot (called by session-start) — proceed / warn / halt before work |
| **`amplified_permissions.py`** | Standing-grants classifier — what an agent may do without asking |
| **`~/control-centre/`** | Deterministic collectors + rules engine (Track A bridge) |
| **Vellum witness** | Append-only ledger — intent, completion, baton, task queue |
| **Seat-pass** | Handoff block: what was done, where it lives, what's next |
| **Relay rules** | Stop rule, PASS protocol, baton — when to hand off and how |

Hooks are not optional polish. They **are** the operating model.

---

## Done gate checklist

Before calling a job done, confirm:

- [ ] **Shared path** — code, spec, or data in `~/amplified-pipeline/`, `perplexity-inbox/`, control-centre, or Beast via PR (not only in a local worktree)
- [ ] **Vellum entry** — intent and/or completion witnessed (INTUITED tier for AI-authored rows)
- [ ] **Tests** — where applicable, unit/smoke tests pass
- [ ] **Does it run?** — one honest execution check, not "looks correct in the editor"

Mac remains read-only for git push; Beast-landing work routes through Cascade-Mac / Devin.

---

## Shared surfaces (company-owned)

| Location | What lives here |
|---|---|
| `~/amplified-pipeline/` | Multi-agent workspace — seat subfolders + shared `data/` |
| `perplexity-inbox/` | Forward specs, Track A module, snapshots, tests |
| `~/control-centre/` | Collectors + rules engine |
| Vellum ledger | Witness, baton, task queue — fleet-wide read |
| Beast `/opt/amplified/` | Decorator, friction_monitor, pipe services — deploy via PR |

Work placed here is **owned by the company, available to everybody**.

---

## How unified sensor fits

Unified sensor gives **one health snapshot** and a **proceed / warn / halt** decision across the fleet. It adds **visibility**, not collapsed ownership. Each seat still owns its boundary end-to-end; the sensor shows everyone else when something is broken. Detail: `docs/UNIFIED-SENSOR-PLAN.md`.

---

## Related docs

- `scripts/session-start.sh` + `SESSION-START__all-seats__v01__2026-06-25.md` — deterministic opening ritual
- `docs/UNIFIED-SENSOR-PLAN.md` — seat ownership, checklist, waypoints
- `docs/INBOX-STATUS.md` — current inbox snapshot
- `unified-sensor__plan-and-checklist__v01__2026-06-25__cursor.md` — entry index
