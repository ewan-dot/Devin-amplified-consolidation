---
title: "Right model routing — right horse for right course"
document_type: operating_rule
artifact_id: operating-rule__right-model-routing__v01__2026-06-30
date_utc: "2026-06-30T18:00:00Z"
author: cursor
ratifier: Ewan
epistemic_tier: INTUITED
origin_type: architect_steer_plus_agent_encode
contributors: [ewan, cursor]
win_win_clear: true
system_of_record: perplexity-inbox
---

# Right model routing — operating rule

**Agreed:** Fleet picks the **right horse for the right course** — correct-size model + tight remit. WHO decides solo vs team is **witnessed on Vellum**, not hidden agent whim.

---

## SSOT paths

| Asset | Path |
|-------|------|
| Machine manifest | `perplexity-inbox/config/fleet-routing-v1.json` |
| Cursor rule | `ingestion-to-research-pipe/.cursor/rules/right-model-routing.mdc` |
| Runtime mirror | `~/.cursor/rules/right-model-routing.mdc` |
| Harness reader | `perplexity-inbox/harness/routing_manifest.py` |
| Session hook | `perplexity-inbox/.cursor/hooks/session-start-routing-hint.py` |

**Sync:** repo SSOT → `~/.cursor/` at seat boot; edits back to repo same session (self-compound).

---

## Routing decision (Cursor parent)

| Step | Action |
|------|--------|
| 1 | Default **solo** — parent executes in-thread |
| 2 | Delegate only when remit is **independent** and parent would load heavy context |
| 3 | Post **Vellum routing sidecar** on plan task **before** Task/subagent/API-team spawn |
| 4 | Frontier tier (plan/judgment) **≤1 per job**; workers for generation/extraction |
| 5 | Subagents: **explicit model tier** — never `inherit` |

### Vellum routing sidecar (light — not full PRM)

Attach to plan task `metadata.routing`:

```json
{
  "routing_mode": "solo",
  "parent_model_tier": "standard",
  "worker_tiers": [],
  "solo_or_delegate_reason": "Two-file fix; no parallel remit",
  "witnessed_before_spawn": true,
  "cursor_thread_owner": "cursor"
}
```

Modes: `solo` | `subagent` | `api_team` | `cross_seat`

---

## IDE sovereignty

- Config respects **Privacy, Security, Sovereignty** per IDE
- **Sub-Cursor = Cursor end-to-end** — accountable, not subcontracted
- Beast API / Vellum / other seats OK within estate — **Cursor owns Cursor-originated thread** prompt→finish
- **Cross-seat** = baton + Vellum consent — never silent offload
- Manifest holds **per-IDE slices**; each seat reads its slice only

---

## Hook chain touchpoint

`sessionStart` → `session-start-routing-hint.py` reads Cursor slice + Vellum marker routing hint → injects into session context alongside baton.

---

## GAP (v1)

- Spawn-without-sidecar: **nudge**, not hard block (`pre_client`)
- Estate token-router: separate infra; not wired here
- Claude/Antigravity slices: stub — encode when those seats adopt

---

## Related

- `token-efficiency.mdc` — context cost, subagent offload triggers
- `constitutional-gate.mdc` — rods
- `OPERATING-RULE__critical-config-and-next-steps__v01__2026-06-27__cursor.md` — protected config model
- `ui-methods-research-pipe/orchestrator-and-subagents.md` — `model: inherit` removed from orchestrator
