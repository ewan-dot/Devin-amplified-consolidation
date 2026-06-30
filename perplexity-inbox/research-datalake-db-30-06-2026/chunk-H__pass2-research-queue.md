---
title: "Chunk H — Pass 2 Research Queue + Open Gaps"
document_type: research_chunk
chunk_id: H
parent_extraction: INDEX__THREAD-EXTRACTION__atom-chunk-label-chronology__v01__2026-06-30__cursor.md
partner: partner-H__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk H — Pass 2 research queue + open gaps

**Merged from both captures + this extraction. Atoms first.**

| P | Item | Blocks |
|---|------|--------|
| **P0** | **Atom ideal spec v1 ratification** — label taxonomy + chronology fields + link model (INDEX §Atom spec) | All lake work |
| **P0** | **Atom validity rubric** — non-nonsense gate before Silver promotion | Atomized property |
| **P0** | **Label taxonomy registry** — canonical enums + multi-valued tags; merge chunks/ + 19-field | Label linking |
| **P0** | **Chronology field spec** — mandatory vs optional; prev/next vs bitemporal | Chronology linking |
| **P0** | **Codd→AI atom mapping doc** — FDs → field constraints; Bernstein → split rules | Logic base |
| **P0** | **Lens projection map** — canonical IDs lake → vector/graph/relational | Multi-DB |
| **P1** | **19-field schema v2** — add `prev_atom_id`, `next_atom_id`, `tags[]`, `cluster_ids[]`, `bronze_source_id`, `atom_validity_score` | YAML + links |
| **P1** | Wire `extract_and_chunk.py` chronology pattern into `inbox_watcher.py` / Silver promotion | Ingest |
| **P1** | Cluster algorithm eval — taxonomy vs GraphRAG Leiden vs embedding | Clustered property |
| **P1** | Parent-child chunk pattern + late chunking eval | Size calibration |
| **P2** | Bi-temporal validity for session/thread atoms | Advanced chronology |
| **P2** | YAML vs JSON Schema vs TOON token efficiency | Tier-2 format |
| **P2** | Property-graph 3NF on AGE atoms | Graph lens |
| — | *(Secondary)* Phoneme normalizer, dual-stream, failure corpus inventory | See phoneme capture §E |

## Top 5 for architect visibility

1. Ratify **atom ideal spec v1** (INDEX §Atom spec draft)
2. Build **atom validity rubric** (non-nonsense gate)
3. Publish **label taxonomy registry** v1
4. Publish **chronology field spec** (mandatory fields + prev/next pattern)
5. Write **Codd→AI atom mapping** (1 page)

Phoneme normalizer remains P1/P2 in phoneme capture — **do not lead Pass 2**.

## GAP table (from atom spec)

| Gap | Priority |
|-----|----------|
| Atom validity rubric (FD-inspired: single subject, min information content) | **P0** |
| Label taxonomy canonical registry | **P0** |
| Chronology link spec doc | **P0** |
| `prev_atom_id` / `next_atom_id` in 19-field schema v2 | **P1** |
| Label-only retrieval path (Spotlight/`mdfind` tags + SQLite index) | **P1** |
| Bi-temporal validity for architect speech sessions | **P2** |
| Phoneme spine fields on Silver atoms (secondary) | **P2** |
