---
title: "Data lake placement — operating rule"
document_type: operating_rule
artifact_id: operating-rule__data-lake-placement__v01__2026-06-30
date_utc: "2026-06-30T23:45:00Z"
author: cursor
ratifier: pending
epistemic_tier: INTUITED
origin_type: prior_art_synthesis
contributors: [ewan, cursor]
win_win_clear: true
system_of_record: perplexity-inbox
prior_art:
  - prior-art-syntheses-bundle/data-lake-prior-art-synthesis__human__v01__2026-06-25
  - RESEARCH-CAPTURE__ai-data-lake-structure__v01__2026-06-30__cursor.md
  - PLAN__data-lake-pathway__v01__2026-06-30__cursor.md
---

# Data lake placement — operating rule

**Agreed pattern (pending architect ratification):** One canonical lake on Beast; shared working paths on Mac; lens DBs are projections, not storage.

---

## Placement tiers

| Tier | Path | May store | Must not store |
|------|------|-----------|----------------|
| **Bronze** | Beast MinIO `/opt/amplified/` raw drops | Files as-arrived; 90-day retention | Interpreted claims |
| **Silver** | Beast MinIO + Iceberg catalog | Atomized, YAMLed, deduped archive | Brain entity bodies |
| **Gold** | Pipe queue → brain write | Ephemeral extraction outputs | Long-term archive |
| **Working** | `~/amplified-pipeline/data/`, `perplexity-inbox/` | SSOT docs, research JSONL, batons | Canonical lake substitute |
| **Sandbox** | `perplexity-inbox/data/intelligence_lake.db` | Local DuckDB lens prototype | Production data |
| **Lens** | Beast `amplified_brain` (pgvector + AGE) | Assertions, embeddings, graph edges | Raw chunk body text |

---

## Pathway (mandatory direction)

```
ingest → search → Silver lake → lens projection → retrieval
```

Brain write is **Gold extraction**, not first landing. Gap events at ingest gate log to Vellum regardless of lens path.

---

## Anti-patterns (refuse)

- Dumping raw transcripts into pgvector/AGE as primary storage
- Treating Mac inbox folders as durable lake (working SSOT only)
- Cloud lake as canonical without explicit sovereignty review
- Federated gap network before single-tenant `IgnoranceGap` spec exists

---

## Sync

| Asset | SSOT |
|-------|------|
| DuckDB schemas | `.cursor/rules/intelligence-lake.mdc` |
| 19-field atom spec | `docs/ai_native_data_organization.md` |
| Full plan | `PLAN__data-lake-pathway__v01__2026-06-30__cursor.md` |

---

## GAP (v1)

- Iceberg catalog not live on Beast
- Lens projection map unwired
- Architect ratification pending

---

[CLOSURE] branch=task/sandbox-intelligence-lake | tier=INTUITED
