---
title: "SYNTHESIS-PREP — Multi-seat chunk index"
document_type: synthesis_prep
folder: research-datalake-db-30-06-2026
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
audience: [antigravity, claude, cascade-mac, scribe]
---

# SYNTHESIS-PREP — Multi-seat chunk index

**Purpose:** Index for Antigravity/Claude/other seats to mirror Cursor's DB-thread harvest. Lists discovery scope, chunk map, open gaps, and **replicable methodology**.

---

## 1. Search scope (honest audit)

| Location searched | Window | Result |
|-------------------|--------|--------|
| `~/.cursor/projects/Users-ewansair-ingestion-to-research-pipe-perplexity-inbox/agent-transcripts/` | 2026-06-27 – 2026-06-30 | **3 parent transcripts** with substantive DB work (+ 1 excluded as already A–H) |
| `~/.cursor/projects/empty-window/agent-transcripts/` | same | Duplicates of 0e0bd954, 01a2ab34 — skipped |
| `~/amplified-pipeline/` | same | **No DB artefact matches** in date window |
| `perplexity-inbox/` root + `archive/` + `chunks/` | 2026-06-27 – 30 | **AgentFS spec** (antigravity 2026-06-28) + PLAN/OPERATING-RULE (2026-06-30) |
| `.worktrees/` | same | Not exhaustively re-scanned — no new thread IDs surfaced |

**Outside window (not harvested):** `f3ce66c7` Brain Ingestion substrate brief (2026-06-26) — recommend separate harvest if still relevant.

**Excluded:** `0e0bd954` — already chunked A–H in this folder.

---

## 2. Thread registry

| Thread ID | Date | Seat | One-line topic | Chunk files |
|-----------|------|------|----------------|-------------|
| `0e0bd954-c665-4fd6-bcf5-f1ec4f0aa45a` | 2026-06-30 | cursor | Atom/lake/lens primary thesis + phoneme secondary | `chunk-A` … `chunk-H` (existing) |
| `01a2ab34-234c-46c7-ae1e-8adc60e3e9f9` | 2026-06-30 | cursor | Fleet routing config + meta-layer ignorance map + data lake pathway | `chunk-01a2ab34-1` … `-3` |
| `11410e93-33cc-4346-98fd-27a19a2214a0` | 2026-06-30 | cursor | Research pipe index + Business Brain harness + baton→datalake | `chunk-11410e93-1` … `-3` |
| `cf0da9b0-16c3-4c4a-8ce2-cd1ad5df0a91` | 2026-06-27 | cursor | Shape gate YAML/OPA + honesty tier arbiter | `chunk-cf0da9b0-1`, `-2` |
| `inbox-artefact-2026-06-28-antigravity` | 2026-06-28 | antigravity | AgentFS dual-YAML 19-field filesystem schema | `chunk-antigravity-agentfs-1` |
| *(cross-thread)* | 2026-06-30 | cursor | Prior art pass 2 synthesis | `chunk-I` |

**Counts:** 4 new threads harvested (+ 1 pre-existing A–H) · **10 new chunk files** · **10 new partner files**

---

## 3. Chunk map (full folder)

### Original session (0e0bd954) — letters A–H

See `README.md` §Chunk map A→H.

### New harvest (2026-06-30 extension)

| Chunk | Partner | Topic |
|-------|---------|-------|
| `chunk-01a2ab34-1__fleet-routing-shared-config-db.md` | `partner-01a2ab34-1__*` | Shared fleet config-as-database |
| `chunk-01a2ab34-2__meta-layer-gap-ignorance-map.md` | `partner-01a2ab34-2__*` | Gap detection = scientific instrument |
| `chunk-01a2ab34-3__data-lake-pathway-ingest-search.md` | `partner-01a2ab34-3__*` | ingest→search→Silver pathway |
| `chunk-11410e93-1__research-pipe-prior-art-index.md` | `partner-11410e93-1__*` | Research pipe prior art |
| `chunk-11410e93-2__business-brain-safety-harness.md` | `partner-11410e93-2__*` | Three-gate brain harness |
| `chunk-11410e93-3__baton-lifecycle-datalake-archive.md` | `partner-11410e93-3__*` | Baton rotation → datalake |
| `chunk-cf0da9b0-1__shape-gate-yaml-opa-boundary.md` | `partner-cf0da9b0-1__*` | YAML OPA ingestion boundary |
| `chunk-cf0da9b0-2__honesty-tier-deterministic-arbiter.md` | `partner-cf0da9b0-2__*` | Claim lifecycle / tier gate |
| `chunk-antigravity-agentfs-1__dual-yaml-19-field-schema.md` | `partner-antigravity-agentfs-1__*` | AgentFS filesystem schema |
| `chunk-I__prior-art-pass2-multi-thread.md` | `partner-I__*` | Cross-thread prior art |

---

## 4. Open gaps (cross-thread)

| Priority | Gap | Source chunk |
|----------|-----|--------------|
| P0 | Ratify atom spec v1 (label + chronology) | A, C, H |
| P0 | `IgnoranceGap` typed event at ingestion | 01a2ab34-2 |
| P0 | Architect ratification: lake placement tiers | 01a2ab34-3, I |
| P1 | Gate 1 D_R/D_G calibration | 11410e93-2 |
| P1 | Baton → Beast Bronze sync | 11410e93-3 |
| P1 | Fleet-wide shape gate install | cf0da9b0-1 |
| P1 | AgentFS v02 ↔ atom spec reconciliation | antigravity-agentfs-1 |
| P2 | Planetary Swanson node protocol | 01a2ab34-2, META-LAYER |

---

## 5. Methodology — replicate on your seat

### Step A — Discover (last N days)

```bash
# Parent transcripts only, date-filtered
find ~/.cursor/projects -path '*/agent-transcripts/*/*.jsonl' ! -path '*/subagents/*' -newermt "YYYY-MM-DD" ! -newermt "YYYY-MM-DD+1"

# Keyword filter
rg -li 'database|data lake|DuckDB|pgvector|intelligence_lake|atom|chunk|lens|YAML|medallion|Brain schema' <transcript-dir>
```

Also grep `perplexity-inbox/`, `~/amplified-pipeline/`, seat batons for DB artefacts.

### Step B — Chunk each qualifying thread

1. Read parent `.jsonl` (skip subagent duplicates unless unique content).
2. Split on logical turns (~800–1500 token sections / thematic breaks).
3. Write pair:
   - `chunk-{THREAD_ID}-N__{slug}.md` — facts, conclusions, architect intent, gaps
   - `partner-{THREAD_ID}-N__source-context.md` — quotes, cross-refs, provenance
4. Frontmatter: `author`, `epistemic_tier: INTUITED`, `source_thread`, `partner` link.

**Naming:** Thread ID = first 8 chars of UUID or full UUID prefix before slug. Inbox-only artefacts: `chunk-{seat}{topic}-1__slug.md`.

### Step C — Prior art (min 3 queries per novel thread)

Load `~/.cursor/skills/amplified-research-pipe/SKILL.md`. Per thread:

1. **Wide** SearXNG: `https://search.beast.amplifiedpartners.ai/search?q=...&format=json`
2. **Narrow** precision on survivors
3. **Wide** again for neighbourhood / pudding hop
4. OpenAlex for academic DOIs where internal inbox thin

Record queries in partner file. Demote homonyms and empty engines.

### Step D — Folder hygiene

- **Extend** README thread registry — never delete A–H.
- Append `SYNTHESIS-PREP` or seat-specific mirror doc.
- Do **not** delete root `perplexity-inbox/` files.

---

## 6. Instructions for other seats

| Seat | Suggested action |
|------|------------------|
| **antigravity** | Add chunks from your AgentFS implementation threads; verify v02 against `chunk-antigravity-agentfs-1` |
| **claude** | Add shape-gate / honesty threads from Claude Code sessions if not in Cursor transcripts |
| **cascade-mac** | `session_master.md` PUDDING storage-layer decisions → chunk as `chunk-cascade-*` if transcript available |
| **scribe** | Witness harvest on Vellum; link thread registry entry IDs |

Use **same schema** as this folder. Post compound delta: `Harvested N threads → research-datalake-db-30-06-2026/chunk-*`.

---

## 7. Cursor harvest summary

- **Threads found (new):** 4 (3 transcripts + 1 inbox artefact)
- **New chunk files:** 10
- **New partner files:** 10
- **Folder:** `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/research-datalake-db-30-06-2026/`

---
*Author: cursor · epistemic_tier: INTUITED*
