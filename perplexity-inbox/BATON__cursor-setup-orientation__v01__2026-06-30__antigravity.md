---
title: "Agent Baton — Cursor — 2026-06-30 — Setup & Orientation"
document_type: baton
artifact_id: BATON__cursor-setup-orientation__v01__2026-06-30__antigravity
date_utc: 2026-06-30
from_agent: antigravity
to_agent: cursor
epistemic_tier: STRUCTURED
tier_reason: "Orientation baton from antigravity; path anchors verified against ESTATE-TAXONOMY.md and COMPLETE_SYSTEM_SPEC.md on write."
ssot_path: code/agents/cursor/BATON.md
---

# Agent Baton — Cursor — Setup & Orientation

**From:** antigravity · **To:** cursor · **Date:** 2026-06-30

SSOT: `code/agents/cursor/BATON.md`

---

## on_wake

1. Query the **AI Orientation Guide** from table `ai_orientation_guide` in database `amplified_brain` — active ports, rules, workspace mappings.
2. Verify local path anchors against master taxonomy: `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/ESTATE-TAXONOMY.md`.
3. Strictly read system specs in `/Users/ewansair/ingestion-to-research-pipe/COMPLETE_SYSTEM_SPEC.md` — safety constraints.

---

## on_stop

1. Submit session walkthrough, learned user preferences, and configuration updates to **Vellum** (`/api/v1/entries` or Vellum sheets).
2. Vellum + Python/Rust deterministic wrappers compile these updates, write to `ai_orientation_guide` (purge old versions to prevent bloat), and sync to GitHub.

---

## outbound_doorway

**Single Outbound Doorway Law** — do not mutate repository files directly.

| Rule | Detail |
|------|--------|
| Write path | `/Users/ewansair/ingestion-to-research-pipe/outbound_doorway/` |
| Patch format | Structured JSON — `patch_[timestamp]_[agent_id].json` |
| Apply | Deterministic Rust binary `/Users/ewansair/control-centre/bin/apply_doorway` parses, validates, applies, commits |

You are restricted to **exactly one** outbound doorway/hook for file changes.

---

## compiled_gates

Safety checks and doorway execution are handled by **immutable Rust binaries**:

- Mac: `/Users/ewansair/control-centre/bin/`
- Beast: `/opt/amplified/bin/`

Do not modify these scripts or binaries.

---

## warnings

- Writing direct commits or editing files outside the doorway violates the **Single Outbound Doorway Law** — rejected by pre-commit and write gates.
- **Verify before first patch:** confirm `apply_doorway` exists and is executable at `control-centre/bin/apply_doorway`.

---

[CLOSURE] branch=BATON | from=antigravity | to=cursor | inbox=BATON__cursor-setup-orientation__v01__2026-06-30__antigravity.md | tier=STRUCTURED
