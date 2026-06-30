---
title: "Amplified Partners Data Lake — Prior Art Synthesis (Human)"
document_type: "human_synthesis"
artifact_id: "2026-06-25T08-57-00Z__amplified__data-lake-prior-art__human__v01"
date_utc: "2026-06-25T08:57:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"

stage: "synthesis"
audience: "Ewan"
purpose: "Answer the framing question, map what exists on Beast today, show what prior art supports, and recommend the lake's shape in plain terms."
source_refs:
  - "James Dixon, Pentaho blog, 2010-10-14"
  - "Armbrust et al., Lakehouse / Delta Lake papers, CIDR 2021 + VLDB 2020"
  - "Databricks medallion architecture docs, 2022"
  - "Edge et al., GraphRAG paper, arXiv 2404.16130, April 2024"
  - "arXiv 2606.08266, data lake / swamp research, 2026"
  - "OAIS Reference Model, ISO 14721:2012"
  - "DuckLake, MotherDuck blog, 2025-06-09"
  - "BLAKE3, Datasketch, Rensa — dedup tooling"
  - "WhisperX / pyannote — audio pipeline"
  - "Forte, Building a Second Brain, 2022"
attribution: "Research synthesis by Perplexity Computer, 2026-06-25. All claims attributed to named sources; no invention."

epistemic_tier: "STRUCTURED"
epistemic_role: "clarity"
tier_reason: "Named-source synthesis. No empirical calibration against Beast. Layer mapping and scaling conclusions are honest heuristics."
confidence_plain_english: "High confidence on the framing resolution and layer design. Medium confidence on exact Iceberg vs DuckLake choice — both are defensible; the call is low-stakes because they share Parquet data files and migration is metadata-only."
open_questions:
  - "Vault classification pass: which existing vault files are Bronze vs Silver? One-time triage needed, not blocking."

companion_agent_doc: "data-lake-prior-art-synthesis__agent__v01__2026-06-25.md"
system_of_record: "local_workspace"
machine_action_allowed: "recommend"
next_human_decision: "Ratify the Bronze/Silver/Gold layer map and the MinIO + Parquet + Iceberg substrate choice. Then commission the Beast-side implementation brief."
outcome:
  class: "no_more_research_needed"
  plain_english_reason: "All 10 domains covered. Framing resolved. No blocking open questions. Ready for your call."
---

## What the lake is for

The data lake is a durable two-tier raw reservoir sitting upstream of the brain: a hot Bronze layer that holds incoming drops transiently, and a cold Silver layer that is the permanent deduplicated archive from which local LLMs slowly extract attribution, logic, and gold nuggets back into the brain.

---

## Where the raw stuff lives today

| Location | Nature | Recommended tier |
|---|---|---|
| `/opt/amplified/raw-mac-dumps/` | Bulk Mac export dumps | Bronze |
| `/opt/amplified/ingest_downloads/` | Downloaded ingest batches | Bronze |
| `/opt/amplified/ingest_batch_283/` | Named batch drop | Bronze |
| `/opt/amplified/ingest_openclaw/` | OpenClaw output | Bronze |
| `/opt/amplified/vault/` | Partly curated; spans both | Bronze + Silver (triage needed) |
| Brain: `store_b_clean` (1.18M rows) | Store B dump — large, raw-ish | Silver candidate |
| Brain: `store_m5_drop_2026_05_11` (447K rows) | M5 drop | Silver candidate |
| Brain: `_staging` (112K rows) | Staging queue | Bronze/Silver boundary |
| Brain: `filtered_for_ingestion` (49K rows) | Pre-pipe queue | Silver → extraction |
| Brain: `_inbox` (46.9K rows) | General inbox | Bronze |
| Brain: `_inbox-voice` (30.9K rows) | Voice/audio inbox | Bronze → transcription → Silver |

---

## What prior art says

- James Dixon coined "data lake" in 2010 to mean exactly this: store raw data in natural state, decide what it means later. The lake is not the brain — it is the reservoir the brain draws from. ([Dixon, 2010](https://jamesdixon.wordpress.com/2010/10/14/pentaho-hadoop-and-data-lakes/))

- The medallion architecture (Bronze raw → Silver clean → Gold business-ready) is the canonical pattern for organising a lake into progressive quality layers. Databricks coined it; it now runs on Fabric, Snowflake, and anywhere else. ([Armbrust et al., CIDR 2021](https://people.eecs.berkeley.edu/~matei/papers/2021/cidr_lakehouse.pdf); [Databricks, 2022](https://www.databricks.com/blog/what-is-medallion-architecture))

- The "data swamp" fires when ownership is absent, metadata is thin, and nothing has been used in 90 days. All six swamp indicators are preventable by the design below. ([arXiv 2606.08266, 2026](https://arxiv.org/html/2606.08266v1))

- At under 100 GB, Iceberg's single-node metadata planning is *faster* than distributed alternatives (Delta, Hudi) because it avoids distributed scan overhead. MinIO + Parquet + Iceberg is a documented small-scale pattern. ([LHBench, Berkeley CIDR 2023](https://people.eecs.berkeley.edu/~matei/papers/2023/cidr_lhbench.pdf))

- BLAKE3 is 2–10× faster than SHA-256 for content hashing and is the right tool for exact dedup at this scale. MinHash/LSH (datasketch library) handles near-duplicates without all-pairs comparison. Both are standard practice.

- For audio, faster-whisper transcribes on CPU; WhisperX + pyannote adds speaker diarisation for multi-speaker files. The original audio lives in Bronze; the transcript lives in Silver. OAIS (ISO 14721) says: preserve the original, not only the derivative.

- Tiago Forte's "Distill" phase in Building a Second Brain (2022) is the personal-scale analogue of the extraction loop: raw captures sit in the lake until you actively distill them into the brain. The lake-to-brain extraction loop is that distillation, automated.

- The GraphRAG paper (Edge et al., arXiv 2404.16130, April 2024) gives the extraction shape: chunk corpus → LLM extracts entity/relation tuples → Leiden community detection → community summaries. This runs on Ollama locally.

---

## Recommended shape

The lake runs three layers on Beast. Bronze is append-only raw storage in MinIO, using flat Parquet or raw files. Silver is deduplicated, typed, and indexed — Parquet files in MinIO with an Iceberg catalog providing ACID and time-travel (useful for rolling back bad extraction runs). Gold is ephemeral: extraction outputs consumed by the pipe and written to the brain; nothing persists in Gold long-term.

| Layer | What goes in | Where | Retention |
|---|---|---|---|
| Bronze | Files as-arrived: code, .md, SLSO, audio, dumps | MinIO bucket, flat Parquet or raw | 90 days, then promote or purge |
| Silver | BLAKE3-deduped, MinHash near-dedup run, audio transcripts appended, metadata stamped | MinIO + Iceberg catalog tables | Indefinite — this is the durable archive |
| Gold | LLM extraction outputs (entities, relations, nuggets) | Pipe inbox | Ephemeral — consumed by brain write |

Storage substrate: MinIO (already on Beast) as object store. Parquet with ZSTD compression as file format. Iceberg via PyIceberg as catalog. No JVM required. DuckDB can query everything directly if needed for ad-hoc inspection.

Catalog: no separate catalog product needed at this scale. Iceberg handles table metadata. A lightweight SQLite file tracks every item's BLAKE3 hash, ingest timestamp, source, tier, and extraction status. An `INDEX.md` per directory covers human and agent navigation.

---

## The gold-nugget extraction loop

1. Silver layer item enters the extraction queue (manually triggered or scheduled batch).
2. Unstructured.io or LlamaIndex partitions the file into normalised JSON elements (handles PDF, .md, code, audio transcripts, SLSO).
3. ollama-2 runs GraphRAG-style extraction: chunks text, identifies entities and relations, generates descriptions.
4. ollama-pudding runs PUDDING neutralization pass on any claim carrying framing risk.
5. Vellum logs the extraction event with full attribution chain: source file → chunk → entity → claim.
6. Python + Rust pipe writes the attested claim to the brain via the approved ingestion path.
7. SQLite manifest marks the source item as `extracted`.

Nothing enters the brain except through step 6. Constitution holds.

---

## Open questions for Ewan

None that block the design. One housekeeping item: the vault (`/opt/amplified/vault/`) spans Bronze and Silver ambiguously. A one-time triage pass is needed to classify existing vault contents before the lake goes operational — but this does not block writing the implementation brief.

The Iceberg vs. DuckLake choice is low-stakes: both use Parquet data files, so migration between them is metadata-only if you change your mind later.

---

*Companion agent document: `data-lake-prior-art-synthesis__agent__v01__2026-06-25.md`*
*Sibling syntheses: `research-pipe-prior-art-synthesis__agent__v01__2026-06-25.md`, `ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25.md`, `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`*
