---
title: "Partner B — Source Context (Atomization & Clustering)"
document_type: research_partner
chunk_id: B
paired_chunk: chunk-B__atomization-chunk-size-yaml-clustering.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Partner B — Source context

Cross-references for Chunk B (atomization, chunk size, YAML, clustering).

## Parent captures

| Document | Section | Relevance |
|----------|---------|-----------|
| `RESEARCH-CAPTURE__ai-data-lake-structure__v01__2026-06-30__cursor.md` | §C (atomized/clustered/YAMLed) | Lake file shape properties |
| `INDEX__THREAD-EXTRACTION__atom-chunk-label-chronology__v01__2026-06-30__cursor.md` | §Atom ideal spec draft | Size heuristics, non-nonsense gate, clustering |
| `RESEARCH-CAPTURE__phoneme-atomization-lake__v01__2026-06-30__cursor.md` | §A point 4 | Atomization = non-nonsense |

## Architect quotes

- **Atomization:** Each part must be **non-nonsense** — nonsense atoms are useless downstream.
- **Lake properties (L33):** Lake files **atomized + clustered + YAMLed**.
- **Clustering:** Grouped how AI prefers — **not homogenized**.
- **YAMLed:** Formatted as AI would like to read (Tier-2 scannable headers).

## Linked prior art & internal paths

| Path / citation | Role |
|-----------------|------|
| `.cursor/rules/intelligence-lake.mdc` | DuckDB schema; 300 lines / 250–550 words constraint |
| `harness/lake_pipeline.py` | Jaccard clustering prototype; documents/chunks/clusters |
| `docs/ai_native_data_organization.md` | 19-field Tier-2 YAML atom schema |
| arxiv 2409.04701 | Late chunking — embed whole doc then chunk |
| arxiv 2507.09935 | Hierarchical RAG chunking |
| arxiv 2407.21059 | Modular RAG |
| arxiv 2501.00309 | GraphRAG — cluster layer over atoms |
| `harness/swanson_pudding_curator.py` | Cross-domain cluster scoring |
| `prior-art-syntheses-bundle/data-lake-prior-art-synthesis__human__v01__2026-06-25.md` | Medallion tiers — complementary to clustering |

## Open gaps (Chunk B)

- Atom validity rubric (P0)
- Parent-child chunk pattern + late chunking eval (P1)
- Cluster algorithm eval — taxonomy vs GraphRAG Leiden vs embedding (P1)
