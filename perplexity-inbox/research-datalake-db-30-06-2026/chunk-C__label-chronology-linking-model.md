---
title: "Chunk C — Label + Chronology Linking Model"
document_type: research_chunk
chunk_id: C
parent_extraction: INDEX__THREAD-EXTRACTION__atom-chunk-label-chronology__v01__2026-06-30__cursor.md
partner: partner-C__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk C — Label + chronology linking model (NEW emphasis)

**Source:** Architect final message L42; `extract_and_chunk.py`; `chunks/README.md`; this session SearXNG prior art.

| Type | Extraction | STATUS |
|------|------------|--------|
| **Architect intent** | Atoms linked by **labeling + chronology** — **flexible, not rigid schema** | **needs research** (spec doc) |
| **Architect intent** | Idealizing atoms = idealizing chunk size for data lake | INTUITED (this extraction) |
| **Internal** | `extract_and_chunk.py` writes `previous_chunk` / `next_chunk` in YAML header | partially encoded (script exists, not in 19-field SSOT) |
| **Internal** | `chunks/` category folders = label dimension | encoded |
| **Internal** | 19-field: `date`, `chunk_index`, `total_chunks`, `parent_nodes` — chronology + graph labels | partially encoded (missing prev/next atom IDs) |
| **Internal** | Vellum = append-only hash-chained ledger; chronology via entry ordering | encoded (fleet) |
| **Internal** | `documents.parent_hash` + `version` = document-level chronology | encoded (`lake_pipeline.py`) |
| **Prior art** | Event sourcing — immutable event log, reconstruct state from chronology | cited (Azure pattern) |
| **Prior art** | Bi-temporal KG / valid-time + transaction-time (MDPI 2025; Sentra bitemporal article) | needs research |
| **Prior art** | Tag-based metadata > rigid hierarchy for flexible org (PKMS literature) | cited |
| **Prior art** | RDF-star / reification — metadata about statements without collapsing atoms | cited (Ontotext, W3C) |
| **Prior art** | Content-addressed IDs (IPFS CID ≈ BLAKE3/SHA-256 identity) | partially encoded |
| **Conclusion** | **Primary link model for v2:** multi-valued labels + chronology chain; 19-field is coordinates, not sole join key | INTUITED — architect-aligned |

## Link model (from atom spec)

**Primary links:** label overlap (shared tags/category/domain) + chronology adjacency (prev/next, same document, same session timeline).

**Secondary links:** cluster similarity, graph `parent_nodes`, content hash dedup.

**Not required:** rigid FK schema across all atoms.

### Label taxonomy (v1 + v2)

- **v1:** `category`, `document_type`, `epistemic_tier`, `domain`, `author`/`seat`, `client_scope`, `project_scope`
- **v2 (flexible):** multi-valued `tags[]`, `cluster_ids[]`, `reasoning_primitive_ids[]`, `parent_nodes[]` — no single mandatory join table

### Chronology fields

`date`, `created_at`, `chunk_index` + `total_chunks`, `prev_atom_id` + `next_atom_id`, `document_version` + `parent_hash`, optional `session_id` + `thread_seq`
