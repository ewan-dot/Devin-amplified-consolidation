---
title: "Chunk 11410e93-2 — Business Brain safety harness"
document_type: research_chunk
chunk_id: "11410e93-2"
source_thread: 11410e93-33cc-4346-98fd-27a19a2214a0
partner: partner-11410e93-2__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk 11410e93-2 — Business Brain safety harness

**Source:** Thread `11410e93` lines 41–55 · architect paste formalized · seat **cursor** · 2026-06-30

| Type | Extraction | STATUS |
|------|------------|--------|
| **Architecture** | Hybrid pipeline: deterministic Python/Rust gates around probabilistic LLM core | spec written |
| **Gate 1** | Pre-flight complexity: cosine dispersion D_R, graph density D_G — block high-entropy RAG | design spec |
| **Gate 2** | ACAP JWT → EBNF → constrained decode (vLLM/llama.cpp) | design spec |
| **Gate 3** | Post-inference: semantic entropy, conformal sets, Rust AST, Postgres sandbox, OPA shape_gate | partial (OPA wired) |
| **Storage touchpoints** | Vector (`knowledge_vectors`), AGE graph, staging/APDS queue | lens path — aligns with lake-first redirect |
| **Built vs spec** | Shape gate partial; Gates 1–2, entropy/CP stack pending verify | honest map in artefact |

## Data flow (summary)

```
Ingest (parse·hash·move) → RAG (vector + graph) → Gate1 (D_R/D_G) → Gate2 (grammar) → LLM → Gate3 (entropy·CP·AST·sandbox·OPA) → outbound
```

## SearXNG prior art (narrow)

- Conformal prediction + RAG gating literature (emerging 2024–2025)
- Semantic entropy for LLM uncertainty (Farquhar et al. line)

## Open gaps

- Gate 1 D_R/D_G thresholds need calibration on `amplified_brain` corpus
- Postgres sandbox ROLLBACK gate — verify Beast deployment
- Fleet-wide shape gate install (workspace-only today)

---
*Author: cursor · epistemic_tier: INTUITED*
