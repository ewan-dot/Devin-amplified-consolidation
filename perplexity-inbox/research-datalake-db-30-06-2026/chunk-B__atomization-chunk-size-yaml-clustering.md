---
title: "Chunk B — Atomization + Chunk Size + YAML/Clustering"
document_type: research_chunk
chunk_id: B
parent_extraction: INDEX__THREAD-EXTRACTION__atom-chunk-label-chronology__v01__2026-06-30__cursor.md
partner: partner-B__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk B — Atomization + chunk size + YAML/clustering

**Source:** Thread L1 atomization quote; architect L33 lake properties; RESEARCH-CAPTURE §C; `intelligence-lake.mdc`.

| Type | Extraction | STATUS |
|------|------------|--------|
| **Architect intent** | Atomization = each part **non-nonsense**; nonsense atoms useless | needs research (validity rubric) |
| **Architect intent** | Chunk size = atom size for lake | partially encoded (~300 lines, 250–550 words) |
| **Architect intent** | Clustered = how AI prefers grouping (not homogenized) | partially encoded (`lake_pipeline.py` Jaccard) |
| **Architect intent** | YAMLed = formatted as AI would like to read | partially encoded (19-field Tier-2) |
| **Fact** | Late chunking (arxiv 2409.04701) — embed whole doc then chunk | needs research (eval) |
| **Fact** | Parent-child retriever (Small-to-Big) — small retrieval unit + large context | GAP — not encoded |
| **Fact** | Hierarchical RAG chunking (arxiv 2507.09935) | needs research |
| **Conclusion** | Atom size correct in principle; **calibration + validity gate** missing | GAP |
| **Conclusion** | Clustering complements medallion tiers, does not replace | encoded (falsification §G) |

## Atom spec excerpt (size + clustering)

| Dimension | Spec draft |
|-----------|------------|
| **Unit** | Atom = Silver-layer chunk file (`.txt` + Tier-2 YAML header + optional `.vector` sidecar) |
| **Size heuristics** | Target **800–1500 tokens** (~250–550 words); hard cap **~300 lines**; split at paragraph/semantic boundary |
| **Non-nonsense gate** | Single coherent semantic unit; reject orphan pronouns, empty headers, pure metadata shells — **GAP: no rubric encoded** |
| **Clustering** | Semantic clusters (GraphRAG Leiden / Jaccard dimensions) sit **above** atoms; do not merge atom content |
| **YAML Tier-2** | 19-field sovereign seal + v2 extensions; field order stable for prompt caching |
