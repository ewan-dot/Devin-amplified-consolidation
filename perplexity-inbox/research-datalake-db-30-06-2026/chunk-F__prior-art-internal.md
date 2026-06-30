---
title: "Chunk F — Prior Art Internal (Fleet Encoding)"
document_type: research_chunk
chunk_id: F
parent_extraction: INDEX__THREAD-EXTRACTION__atom-chunk-label-chronology__v01__2026-06-30__cursor.md
partner: partner-F__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Chunk F — Prior art internal (search_autocorrect, verbatim valve, 19-field)

**Source:** Subagents 1f9920af, bd35d2c9; internal grep.

| Path | Covers | Gap |
|------|--------|-----|
| `harness/search_autocorrect.py` | Levenshtein + alias map at query time | No phonetic keys |
| `docs/ai_native_data_organization.md` | 19-field atom schema; assertion-context boundary; ingestion gate | No prev/next atom; no label registry |
| `chunks/README.md` | Filesystem taxonomy; YAML headers; Spotlight tags | Category labels only; no chronology spec |
| `harness/lake_pipeline.py` | DuckDB documents/chunks/clusters/primitives | Local prototype; no Silver Parquet |
| `scripts/extract_and_chunk.py` | prev/next chunk chronology in YAML | Not wired to inbox watcher |
| `overallpicture1` chunks | Verbatim Acoustic Intake Valve doctrine | Bronze/Silver not ratified |
| `.cursor/rules/intelligence-lake.mdc` | DuckDB schema + reasoning primitives | Encoded (self-compound session) |
| `prior-art-syntheses-bundle/data-lake-*` | Medallion, BLAKE3, GraphRAG loop | Cite only |

## Internal encoding partial (from executive synthesis)

19-field YAML, chunks taxonomy, `lake_pipeline.py` DuckDB prototype, `search_autocorrect.py` (grapheme only), Vellum append-only hash chain — **no atom validity rubric, no label+chronology link spec, no lens projection map**.

## Internal prior art (label+chronology contribution)

| Asset | Contribution |
|-------|--------------|
| **Vellum ledger** | Append-only hash-chained entries; chronological witness |
| **`extract_and_chunk.py`** | `previous_chunk` / `next_chunk` in YAML — proto chronology spec |
| **`chunks/README.md`** | Category labels + `chunk_index` in YAML |
| **`lake_pipeline.py`** | `documents.version` + `parent_hash`; `chunks.chunk_index` |
| **`harness/calibrate_spine.py`** | PRIM_DECAY temporal relevance — chronology in scoring layer |
| **META-LAYER gap detection** | Temporal cluster query on IgnoranceGap nodes |
