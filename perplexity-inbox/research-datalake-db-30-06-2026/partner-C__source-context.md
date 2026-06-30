---
title: "Partner C — Source Context (Label + Chronology Linking)"
document_type: research_partner
chunk_id: C
paired_chunk: chunk-C__label-chronology-linking-model.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
---

# Partner C — Source context

Cross-references for Chunk C — the **core v2 link model** (label + chronology, flexible not rigid).

## Parent captures

| Document | Section | Relevance |
|----------|---------|-----------|
| `INDEX__THREAD-EXTRACTION__atom-chunk-label-chronology__v01__2026-06-30__cursor.md` | §Atom ideal spec, §Prior art label+chronology | Full link model + SearXNG survivors L1–L10 |
| `RESEARCH-CAPTURE__ai-data-lake-structure__v01__2026-06-30__cursor.md` | §A layer 4 | Lens DBs as projections |

## Architect quotes (final message L42)

- Atoms linked by **labeling + chronology** — explicitly **flexible, not rigid schema**.
- This supersedes over-normalized 19-field-as-only-link model for v2.
- Idealizing atoms = idealizing chunk size for data lake.

## Linked prior art (SearXNG survivors)

| ID | Topic | URL |
|----|-------|-----|
| L1 | Temporal KG (ATOM) | https://aclanthology.org/2026.findings-eacl.49/ |
| L2 | Bi-temporal KG | https://www.sentra.app/articles/what-is-a-bitemporal-knowledge-graph |
| L3 | Append-only ledger | https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-append-only-ledger |
| L4 | Event sourcing | https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing |
| L5 | Content-addressed (IPFS CID) | https://docs.ipfs.tech/concepts/content-addressing/ |
| L6 | RDF-star | https://www.ontotext.com/knowledgehub/fundamentals/what-is-rdf-star/ |
| L7 | RDF reification (Jeni Tennison 2008) | http://www.jenitennison.com/2008/04/11/metadata-about-rdf-triples-reification-and-linked-data.html |
| L8 | Tag-based metadata (JYU PDF) | https://users.jyu.fi/~miettine/kurssit/jatkoksem/miika11112010.pdf |
| L9 | Tag vs hierarchy (2017) | https://lobste.rs/s/hv7alh/designing_better_file_organization |
| L10 | RFC 4287 Atom syndication | https://www.ietf.org/rfc/rfc4287.txt (name collision only) |

## OpenAlex survivors

- doi:10.1109/icsc50631.2021.00049 — RDF metadata representations
- doi:10.1145/383059.383072 — Content-addressable network
- doi:10.1145/287000.287001 — Event-based data models

## Internal proto-chronology assets

| Path | Contribution |
|------|--------------|
| `scripts/extract_and_chunk.py` | `previous_chunk` / `next_chunk` in YAML — proto spec |
| `chunks/README.md` | Category labels + `chunk_index` |
| `harness/lake_pipeline.py` | `documents.version` + `parent_hash`; `chunks.chunk_index` |
| Vellum ledger | Append-only hash-chained entries; chronological witness |
| `harness/calibrate_spine.py` | PRIM_DECAY temporal relevance |
| `META-LAYER__gap-detection-as-scientific-instrument__v01__2026-06-30__cursor.md` | Temporal cluster query on IgnoranceGap nodes |

## Open gaps (Chunk C)

- Chronology field spec — mandatory vs optional; prev/next vs bitemporal (P0)
- Label taxonomy registry v1 (P0)
- `prev_atom_id` / `next_atom_id` in 19-field schema v2 (P1)
- Bi-temporal validity for session/thread atoms (P2)
