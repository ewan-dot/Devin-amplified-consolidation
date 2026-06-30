---
title: "Chunk 01a2ab34-3 — Data lake pathway ingest→search→Silver"
document_type: research_chunk
chunk_id: "01a2ab34-3"
source_thread: 01a2ab34-234c-46c7-ae1e-8adc60e3e9f9
partner: partner-01a2ab34-3__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk 01a2ab34-3 — Data lake pathway ingest→search→Silver

**Source:** Thread `01a2ab34` lines 57–59 · seat **cursor** · 2026-06-30

| Type | Extraction | STATUS |
|------|------------|--------|
| **Pathway change** | **Old:** ingest → research pipe → brain write · **New:** ingest → search → **Silver data lake** | encoded (`PLAN__data-lake-pathway__*`) |
| **Architect intuition** | Graph + vector DB = **schema building lenses** — easy if labeling done at lake ingest | partially encoded |
| **Action list** | Infra clean, shared drive, Python/Rust/math formalized, pathway redirect | `COLLATION__session-2026-06-30__action-items__*` |
| **Research ask** | Where data lakes live — prior art as whole | encoded in PLAN + OPERATING-RULE |
| **Conclusion** | Brain (pgvector+AGE) is **lens/Gold**, not first landing zone | encoded |
| **Placement tiers** | Beast MinIO+Iceberg canonical; Mac working; DuckDB sandbox; brain lens | encoded (pending ratification) |

## Recommended placement (from PLAN artefact)

| Tier | Location | Role |
|------|----------|------|
| Bronze | Beast MinIO raw | As-arrived |
| Silver | Beast MinIO + Iceberg | Atomized, YAMLed, deduped |
| Gold | Pipe queue → brain | Ephemeral extraction |
| Working | `~/amplified-pipeline/data/`, perplexity-inbox | SSOT + witness |
| Sandbox | `perplexity-inbox/data/intelligence_lake.db` | DuckDB prototype |
| Lens | Beast `amplified_brain` | Projections only |

## Anti-patterns (refuse)

- Dumping raw transcripts into pgvector/AGE as primary storage
- Mac inbox as durable canonical lake

## Open gaps

- Architect ratification of Iceberg vs DuckLake
- E2E smoke: ingest→research→brain before filesystem reorg (baton constraint)
- Label taxonomy registry v1 at Silver ingest

---
*Author: cursor · epistemic_tier: INTUITED*
