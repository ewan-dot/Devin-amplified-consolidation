---
title: "Chunk 11410e93-3 — Baton lifecycle & datalake archive"
document_type: research_chunk
chunk_id: "11410e93-3"
source_thread: 11410e93-33cc-4346-98fd-27a19a2214a0
partner: partner-11410e93-3__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk 11410e93-3 — Baton lifecycle & datalake archive

**Source:** Thread `11410e93` lines 116+ · seat **cursor** · 2026-06-30

| Type | Extraction | STATUS |
|------|------------|--------|
| **Architect intent** | Baton folder: sessionStart hook reads; **max 5 active**; rest → unified archive → **datalake** | encoded (`baton_lifecycle.py`) |
| **Architect intent** | Data lake = **AI-organized file structure**, communally stored off-site, data-based | aligns Chunk A + PLAN |
| **Question** | Spotlight off-site indexing on Mac — operational, not schema | open (Mac search UX) |
| **Implementation** | `harness/baton_lifecycle.py`: active (max 5) → archive → datalake bronze | encoded |
| **Pathway link** | Baton archive rotation feeds **Bronze** tier of lake placement model | partially wired |

## Baton lifecycle (deterministic)

```
write_baton → active/ (≤5) → rotate → archive/ → datalake bronze
sessionStart hook → read_latest baton
```

## Lake model confirmation (architect L116)

> "the data lake is just going to be a file structure where the file structure is organized by AI communally stored off-site, but it's data-based"

Matches Silver atomized+YAMLed filesystem lake — not Postgres-first.

## Open gaps

- Automated baton → MinIO Bronze sync on Beast (not Mac-local only)
- Spotlight/Tailscale off-site search — needs ops pass
- Session-start baton hook fleet-wide install verify

---
*Author: cursor · epistemic_tier: INTUITED*
