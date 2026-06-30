---
title: "Chunk cf0da9b0-2 — Honesty tier deterministic claim arbiter"
document_type: research_chunk
chunk_id: "cf0da9b0-2"
source_thread: cf0da9b0-16c3-4c4a-8ce2-cd1ad5df0a91
partner: partner-cf0da9b0-2__source-context.md
date_utc: 2026-06-27
author: cursor
epistemic_tier: INTUITED
---

# Chunk cf0da9b0-2 — Honesty tier deterministic claim arbiter

**Source:** Thread `cf0da9b0` lines 30–196 · seat **cursor** · 2026-06-27

| Type | Extraction | STATUS |
|------|------------|--------|
| **Spec** | Honesty parameter YAML — Radical Honesty rods encoded as OPA-checkable fields | encoded in inbox |
| **Arbiter model** | Claim lifecycle: `open` → `claimed` (atomic) → `rejected`/`resolved` — deterministic state machine | encoded in thread |
| **DB relevance** | Epistemic tier on every artefact = **lens metadata** — prevents STRUCTURED laundering without promotion_record_id | fleet rule |
| **Question answered** | "Am I allowed to do that?" — yes if SSOT arbiter path resolves; no seat-local overrides | encoded |

## Claim state machine (thread L196)

| State | Who sets | Rule |
|-------|----------|------|
| `open` | system | spec on Vellum |
| `claimed` | first valid seat | atomic write |
| `rejected` | claiming seat | requires reason |

## Link to database layers

- Vellum = immutable ledger (hash-chained witness)
- Brain graph = assertion structure (lens)
- Honesty tier = gate between INTUITED agent output and STRUCTURED promotion

---
*Author: cursor · epistemic_tier: INTUITED*
