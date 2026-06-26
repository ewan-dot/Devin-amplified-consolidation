# Perplexity Inbox — Index v02

**Date:** 2026-06-25 · **Author:** cursor · **Tier:** INTUITED  
**Supersedes:** v01 entry point for Jun-25 threads only — `INBOX-INDEX__v01__2026-06-24__perplexity.md` remains the Jun-24 audit trail.

**Read first for Jun-25 work:** this file → `docs/INBOX-STATUS.md` → `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md`

---

## What changed on 2026-06-25

Five threads completed or documented in this inbox pass. Everything below is on disk under `perplexity-inbox/`.

| # | Thread | Status | Primary artefact(s) |
|---|---|---|---|
| 1 | **Unified sensor Track A** | ✅ Working + tested | `unified_sensor/`, `monitor.py`, `tests/`, `data/sensor_snapshot.json` |
| 2 | **Tarball extraction + v03 promotion** | ✅ Extracted | `signal-reading-bundle/`, `prior-art-syntheses-bundle/`, root v03 doctrine |
| 3 | **AI-native operating model** | ✅ Documented | `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md` |
| 4 | **Plan / checklist / related-work map** | ✅ Documented | `docs/UNIFIED-SENSOR-PLAN.md`, `docs/RELATED-WORK-MAP.md`, `unified-sensor__plan-and-checklist__v01__2026-06-25__cursor.md` |
| 5 | **Worktree created** | ✅ On disk | `.worktrees/feat-unified-sensor` → branch `feat/unified-sensor` |

---

## Jun-25 thread detail

### 1. Unified sensor Track A (cursor)

**Summary:** `completed-by-cursor__2026-06-25/SUMMARY__unified-sensor-track-a__2026-06-25__cursor.md`

| Path | Purpose |
|---|---|
| `unified_sensor/` | Mac gather module (7 Python files) |
| `monitor.py` | Perplexity-facing CLI |
| `tests/test_unified_sensor.py` | 6 unit tests |
| `data/sensor_snapshot.json` | Last live snapshot |
| `docs/UNIFIED-SENSOR-PLAN.md` | Seat ownership + checklist |
| `docs/RELATED-WORK-MAP.md` | Reuse / conflict map |

**Run:** `python3 monitor.py` · `python3 monitor.py --signals-only`

**Not done:** Track B (Beast witness), job-start hook, Perplexity adoption habit.

### 2. Tarball extraction + v03 promotion

| Path | Purpose |
|---|---|
| `signal-reading-bundle/` | Extracted from `signal-reading-bundle__2026-06-25.tar.gz` |
| `prior-art-syntheses-bundle/` | Extracted from `prior-art-syntheses-bundle__2026-06-25.tar.gz` |
| `vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md` | Canonical witness spec (root) |
| `vellum-witness-doctrine-and-decorator__v01/v02__...` | Audit trail only |
| `prior-art-syntheses-bundle__INDEX__v01__2026-06-25.md` | Bundle index |

### 3. Operating model

| Path | Purpose |
|---|---|
| `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md` | Hooks, done ladder, shared surfaces |
| `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md` | Done vs open priorities |

### 4. Plan stack (Perplexity → cursor docs)

| Path | Purpose |
|---|---|
| `master-plan__v01__2026-06-25__perplexity.md` | Phase 0–7 sequence (SSOT) |
| `pipe-weld-brief__v01__2026-06-25__perplexity.md` | Phase 2 implementation brief |
| `control-centre-prior-art-synthesis-2026-06-25T0837Z-perplexity.md` | Control-centre context |
| `beast-tailscale-recovery-plan-2026-06-25T1252Z-perplexity.md` | Beast recovery notes |
| `docs/INBOX-STATUS.md` | Live status snapshot |

### 5. Worktree

| Path | Branch | Notes |
|---|---|---|
| `/Users/ewansair/ingestion-to-research-pipe/.worktrees/feat-unified-sensor` | `feat/unified-sensor` | Mac read-only — merge via Devin |

---

## Relationship to v01 index (Jun-24)

v01 covers 16 threads (token-efficiency, sovereign multi-agent, standing grants, 12 recovered briefs, Tier C gate cluster). **None of those are closed by Jun-25 work** except where Track A overlaps:

- **Deterministic core** (#9) — Antigravity done; control-centre bridge reuses it
- **Vellum senses** (folded into #9) — complements Track A; M5 write path still open
- **AI-native search methodology** (#15) — master-plan Phase 2 pipe weld is the actionable slice

For the consolidated Ewan hand-back across both eras: `EWAN-DECISIONS-CONSOLIDATED__v01__2026-06-26.md`.

---

## Quick entry points

| If you want… | Start here |
|---|---|
| Fleet health right now | `python3 monitor.py --signals-only` |
| What's done vs open | `AI-NATIVE-PRIORITIES__v01__2026-06-25__cursor.md` |
| How work should flow | `AI-NATIVE-OPERATING-MODEL__v01__2026-06-25__cursor.md` |
| Full phase sequence | `master-plan__v01__2026-06-25__perplexity.md` |
| Track A completion evidence | `completed-by-cursor__2026-06-25/SUMMARY__unified-sensor-track-a__2026-06-25__cursor.md` |
| Mac Mini Cursor pickup | `HANDOFF__mac-mini-cursor__shared-inbox-ssot__v01__2026-06-25__cursor.md` |
