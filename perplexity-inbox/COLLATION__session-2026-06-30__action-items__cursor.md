---
title: "Collation — 2026-06-30 session action items"
document_type: collation
artifact_id: COLLATION__session-2026-06-30__action-items__cursor
date_utc: "2026-06-30T23:45:00Z"
author: cursor
reader: ewan
epistemic_tier: INTUITED
system_of_record: perplexity-inbox
sources:
  - META-LAYER__gap-detection-as-scientific-instrument__v01__2026-06-30__cursor.md
  - RESEARCH-PIPE-RUN__meta-layer-prior-art__v01__2026-06-30__cursor.md
  - RESEARCH-CAPTURE__ai-data-lake-structure__v01__2026-06-30__cursor.md
  - OPERATING-RULE__right-model-routing__v01__2026-06-30__cursor.md
  - config/fleet-routing-v1.json
  - batons/active/BATON__*
  - agent transcripts 01a2ab34, 0e0bd954, f3ce66c7 (2026-06-30)
---

# Session collation — 2026-06-30

Chunked by theme. Actionable nuance only — no dumps.

---

## Theme 1 — Multi-agent routing (WHO vs WHAT)

**Decisions encoded:**
- Default **solo**; delegate only for independent remit + heavy context.
- **No `model: inherit`** on subagents — explicit tier always.
- Frontier (plan/judgment) **≤1 per job**.
- Vellum routing sidecar on plan **before** spawn (`metadata.routing`).
- Cursor owns Cursor thread end-to-end; cross-seat = baton + consent.

**Actions:**

| Action | Seat | Priority |
|--------|------|----------|
| Use routing sidecar on next multi-lane research spawn | cursor | P1 |
| Stub Claude/Antigravity slices in manifest when those seats adopt | respective seat | P2 |
| Estate token-router proxy — separate infra, not this rule | devin | P3 |

**Artefacts:** `OPERATING-RULE__right-model-routing__*`, `fleet-routing-v1.json`, `right-model-routing.mdc`, hooks installed to `~/.cursor/hooks.json`.

---

## Theme 2 — Pre-Cursor WHO / token-efficiency crossover

**Nuance:** Model choice (WHO) must not shape task content (WHAT). Opus plans once; workers execute tight remits. Token efficiency = output length + context discipline, not always cheapest model.

**Actions:**

| Action | Seat | Priority |
|--------|------|----------|
| Plan chat on frontier tier; execute in fresh worker chat when remit is mechanical | cursor | Ongoing |
| Log routing sidecar when spawning — closes "hidden whim" gap | cursor | P1 |

**Cross-ref:** `token-efficiency.mdc`, `ui-methods-research-pipe/orchestrator-and-subagents.md` (`model: inherit` removed).

---

## Theme 3 — Kaizen + PUDDING meta-layer

**Insight:** Gap detection at ingestion gate = scientific instrument. Map of ignorance > map of knowledge. Kaizen walks boundary; PUDDING holds neutral taxonomy. Together = system improves its ability to improve.

**Actions:**

| Action | Seat | Priority |
|--------|------|----------|
| Wire gap events → Vellum `metadata.gap_term` | cursor | P0 |
| Add `IgnoranceGap` graph node + temporal cluster query | devin | P1 |
| Taguchi Safe/Distress/Critical gate on gap-rate spike | cursor | P1 |
| Planetary node open-source spec (Phase 2) | antigravity | P3 |

**Artefacts:** `META-LAYER__*`, `RESEARCH-PIPE-RUN__meta-layer-prior-art__*`, baton `sovereign-ignorance-maps-planetary-swanson-nodes`.

---

## Theme 4 — Data lake structure (PRIMARY thread)

**Architect correction:** DB/lake structure **primary**; phoneme normalizer **secondary**.

**Decisions:**
- Classic Codd/FD logic **informs** atoms — not copied verbatim.
- Lake = neutral storage; lens DBs = projections.
- Three lake file properties: **atomized**, **clustered**, **YAMLed**.
- Imagineering falsification: foundations **SOLID**; YAML-as-optimal **WEAK**; lens wiring **GAP**.

**Actions:**

| Action | Seat | Priority |
|--------|------|----------|
| Codd→AI atom mapping doc (1 page) | scribe + cursor | P0 |
| Atom validity rubric | cursor | P0 |
| Lens projection map (Silver → vector/graph/relational) | cursor | P0 |
| 19-field schema v2 (`cluster_id`, `parent_atom_id`, `lens_flags`) | cursor | P1 |
| Cluster algorithm eval on inbox corpus | cursor | P1 |
| Beast MinIO Silver implementation brief | devin | P1 — after Ewan ratifies plan |
| Phoneme normalizer | cursor | P3 — secondary |

**Artefact:** `RESEARCH-CAPTURE__ai-data-lake-structure__*`, `PLAN__data-lake-pathway__*`.

---

## Theme 5 — Parallel research test (meta-layer prior art)

**Verdict:** 6 parallel WebSearch lanes viable; demote effective; needs SearXNG + JSONL witness for production GB-scale.

**Actions:**

| Action | Seat | Priority |
|--------|------|----------|
| Scaled run with SearXNG + global demote on next corpus | cursor | P2 |
| JSONL witness to `~/amplified-pipeline/data/research-pipe-docs/` | cursor | P1 — done for data-lake capture |

---

## Theme 6 — Infrastructure & pipe priority (baton)

**Ewan ratified order:**
1. Complete ingest → research → brain E2E **before** filesystem reorg.
2. Harden mesh (wanmin containers, Tailscale, one Vellum face).
3. Phone = Vellum UI only.
4. Reorg / communal AI folders **after** pipe.

**Actions:**

| Action | Seat | Priority |
|--------|------|----------|
| Beast pipe smoke: research batch → drop → drainer → brain witness | cursor / devin | **P0 blocker** |
| Merge `apply_doorway` to control-centre | cursor | P1 |
| wanmin container IDE layout | antigravity + ewan | P1 — wanmin power |
| Dependabot + Copilot e2e baton | next session | P2 |

---

## Theme 7 — Harness & environment (today's compound)

**Encoded:** `intelligence-lake.mdc`, `active-harnesses.mdc`, routing hooks, shape gates, `lake_pipeline.py` sandbox.

**Actions:**

| Action | Seat | Priority |
|--------|------|----------|
| pytest `harness/test_lake_pipeline.py` in CI scope | cursor | P1 |
| Sync repo SSOT → `~/.cursor/` after rule edits | any seat | Same session |
| Python/Rust/math formalized: spine calibration → gatekeeper hook | cursor | P2 |

---

## Theme 8 — PUDDING telemetry audit (cascade-mac)

**Signal:** `constraint` is load-bearing; R1 (M1×M3×M6) top recipe — context-identity intersection grammar.

**Action:** Feed into harness constraint gates — no separate implement this week unless pipe blocked.

---

## Top 5 actions (all seats)

1. **Beast E2E pipe smoke** — research → drop → drainer → brain (blocker for reorg).
2. **P0 lake structure** — atom mapping doc + validity rubric + lens projection map.
3. **Gap instrument** — Vellum `gap_term` hook at ingestion gate.
4. **Architect ratify** lake placement plan (`PLAN__data-lake-pathway__*`).
5. **Routing discipline** — Vellum sidecar before any subagent spawn.

---

## Decisions still with Ewan

| Decision | Options | Default if silent |
|----------|---------|-------------------|
| Canonical lake substrate | Beast MinIO + Iceberg vs DuckLake | Iceberg (2026-06-25 synthesis) |
| Federated gap nodes timing | Now vs Phase 2 | Phase 2 |
| Vault Bronze/Silver triage | One-time Beast pass | Blocks Silver promotion only |
| Medallion Gold = ephemeral brain extraction | Yes / No | Yes (prior art) |

---

[CLOSURE] branch=task/sandbox-intelligence-lake | inbox=COLLATION__session-2026-06-30__action-items__cursor.md | tier=INTUITED
