---
title: "Chunk cf0da9b0-1 — Shape gate YAML OPA ingestion boundary"
document_type: research_chunk
chunk_id: "cf0da9b0-1"
source_thread: cf0da9b0-16c3-4c4a-8ce2-cd1ad5df0a91
partner: partner-cf0da9b0-1__source-context.md
date_utc: 2026-06-27
author: cursor
epistemic_tier: INTUITED
---

# Chunk cf0da9b0-1 — Shape gate YAML OPA ingestion boundary

**Source:** Thread `cf0da9b0` lines 51–110 · seat **cursor** · 2026-06-27

| Type | Extraction | STATUS |
|------|------------|--------|
| **Fix** | OPA path corrected: `harness/opa/amplified/honesty/min_rule.rego` (not dropped `opa/` level) | encoded |
| **Architecture** | **Shape gate** = bee at the door — YAML frontmatter + OPA before artefact counts as real | encoded |
| **Multi-IDE** | Shared `shape_gate.py` wired for Cursor, Claude, Antigravity post-write hooks | encoded |
| **DB relevance** | Tier-2 YAML (17–20 fields) is **pre-database contract** — same schema feeds lake atoms + lens projection | encoded |
| **Deterministic arbiter** | SSOT path resolution for OPA bundle — no seat guessing | encoded (`resolve_opa_bundle`) |

## Live touchpoints (thread)

- Claude `pre-ingest-tier-gate.py`
- Vellum `/send` tier + evidence
- Cursor `afterFileEdit` shape gate (project scope)
- `glasses_loader.py` — schema_code validation

## Relation to lake model

YAML shape gate = **Silver ingest quality gate** before atom lands in lake or projects to pgvector/AGE lens.

---
*Author: cursor · epistemic_tier: INTUITED*
