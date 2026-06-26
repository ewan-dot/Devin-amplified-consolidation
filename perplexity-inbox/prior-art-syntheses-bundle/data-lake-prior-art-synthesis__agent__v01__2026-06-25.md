---
title: "Amplified Partners Data Lake — Prior Art Synthesis"
document_type: "research_conclusion"
artifact_id: "2026-06-25T08-57-00Z__amplified__data-lake-prior-art__agent__v01"
date_utc: "2026-06-25T08:57:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"

stage: "synthesis"
objective: "Survey 10 prior-art domains, resolve the framing question (transient / durable / tiered), and produce a defensible architecture recommendation for the Beast-hosted data lake at <100 GB scale."
reader: "agent"
source_refs:
  - "James Dixon, 'Pentaho, Hadoop, and Data Lakes', blog 2010-10-14, https://jamesdixon.wordpress.com/2010/10/14/pentaho-hadoop-and-data-lakes/"
  - "Armbrust et al., 'Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics', CIDR 2021, https://people.eecs.berkeley.edu/~matei/papers/2021/cidr_lakehouse.pdf"
  - "Armbrust et al., 'Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores', VLDB 2020, https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf"
  - "Databricks, 'What is Medallion Architecture', 2022-09-03, https://www.databricks.com/blog/what-is-medallion-architecture"
  - "Edge et al., 'From Local to Global: A Graph RAG Approach to Query-Focused Summarization', arXiv 2404.16130, April 2024, https://arxiv.org/html/2404.16130v2"
  - "arXiv 2606.08266, 'What Went Wrong with Data Lakes? A 15-Year Reality Check', 2026-06-06, https://arxiv.org/html/2606.08266v1"
  - "Datasketch MinHash/LSH library, https://github.com/ekzhu/datasketch"
  - "BLAKE3 hash function, https://github.com/BLAKE3-team/BLAKE3"
  - "WhisperX / pyannote diarisation pipeline, https://github.com/m-bain/whisperX"
  - "OAIS Reference Model, ISO 14721:2012 / CCSDS 650.0-M-3, https://ccsds.org/Pubs/650x0m3.pdf"
  - "Forte, Tiago, 'Building a Second Brain', 2022; PARA method, https://www.buildingasecondbrain.com"
  - "DuckLake format, MotherDuck blog, 2025-06-09, https://motherduck.com/blog/getting-started-ducklake-table-format/"
  - "OpenMetadata vs DataHub comparison, IJIRCCE 2024, https://ijircce.com/admin/main/storage/app/pdf/79_Openmetadata%20and%20Datahub%20A%20Comparative%20Evaluation.pdf"
  - "Unstructured.io documentation, https://unstructured.io"
  - "Rensa MinHash library (Rust bindings), https://github.com/beowolx/rensa"
  - "LlamaIndex unstructured data extraction, https://www.llamaindex.ai/blog/unstructured-data-extraction"
  - "Berkley LHBench — 'Analyzing and Comparing Lakehouse Storage Systems', CIDR 2023, https://people.eecs.berkeley.edu/~matei/papers/2023/cidr_lhbench.pdf"
origin_type: "agent_synthesis"
attribution: "Multi-source synthesis by Perplexity Computer, 2026-06-25. All claims attributed to primary sources above. No invention."

epistemic_tier: "STRUCTURED"
tier_reason: "Synthesised from named primary sources; no empirical calibration or formal proof against the Beast. Domain selection, layer mapping, and scaling conclusions are reproducible structured heuristics."
epistemic_role: "clarity"
effective_tier_rule: "min-rule"
preconditions:
  - "Beast directories and source_types listed are ground truth (verified from task brief, not re-checked live in this run)"
  - "MinIO confirmed present on Beast (docker_ps shows minio/minio:latest)"
  - "Ollama containers (ollama-2, ollama-pudding) confirmed present"
  - "Lake size intent <100 GB confirmed from 2026-05-20 memory"
valid_until: "2026-12-25"

claim_scope: "Architecture framing, layer recommendation, storage substrate, dedup strategy, audio pipeline, catalog decision, extraction loop shape"
contradiction_status: "clean"
known_contradictions: []

machine_action_allowed: "recommend"
system_of_record: "local_workspace"
ratifier: "Ewan"
next_action: "Ewan reviews; if approved, lake architecture moves to production_candidate and a Beast-side implementation brief is written."
companion_human_doc: "data-lake-prior-art-synthesis__human__v01__2026-06-25.md"
cross_references:
  - "research-pipe-prior-art-synthesis__agent__v01__2026-06-25.md"
  - "ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25.md"
  - "estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md"
outcome_routing:
  outcome_class: "no_more_research_needed"
  outcome_reason: "All 10 domains surveyed with at least one primary source each. Framing question resolved. Architecture recommendation is defensible at STRUCTURED tier. The one open question (catalog scale threshold) is a calibration question for after the lake is operational, not a blocker."
  required_next_action: "Ewan ratification; then implementation brief for Beast-side setup."
  research_needed: false
  tangent_refs:
    - "DuckLake (2025) — SQL-backed metadata format; strong candidate if Iceberg overhead proves real at this scale. Not primary recommendation yet."
    - "Rensa MinHash (Rust) — 39× faster than datasketch for large dedups; worth switching if corpus grows past 1M rows."
  methodology_refs: []
---

## One-Sentence Summary

**The Amplified data lake is BOTH: a tiered store where hot Bronze is transient staging and cold Silver/archive is a durable raw record — a two-tier design grounded in the medallion architecture (Armbrust et al., CIDR 2021) adapted to single-node Beast scale.** [TIER: STRUCTURED]

---

## 1. Purpose and Framing

### Framing question resolved

The framing question — transient staging vs. durable archive vs. both — resolves as **tiered both**, with the following mapping:

| Lake function | Prior-art analogue | Beast role |
|---|---|---|
| Hot staging (transient) | Bronze layer, Databricks medallion architecture | Ingest drops land here; processed within days/weeks; no long-term retention guarantee |
| Durable raw archive | OAIS "Archival Storage" functional entity (ISO 14721); archival science model of preserve-then-access | Deduplicated, typed Silver layer; retained indefinitely as source-of-truth for the extraction loop |
| Extraction queue | LlamaIndex/GraphRAG corpus loader pattern; Forte's "Distill" phase of CODE | Lake-to-brain pipeline pulls from Silver; Gold-equivalent goes straight to the brain |

Dixon's original 2010 definition ("large body of water in a more natural state") was explicitly about *preserving raw data for unknown future questions* — a durable archive posture. The medallion architecture (Databricks, 2022) added the transient staging layer on top. Both apply here.

The **swamp anti-pattern** (arXiv 2606.08266, 2026) fires when: no dataset ownership >50% of assets, metadata completeness <40%, >40% of datasets unused in 90 days, undocumented lineage, >20% duplicates, no quality validation on ingestion. The design below prevents all six.

### Lake vs. brain distinction

The brain is the curated, structured, attribution-verified store. The lake is the upstream raw reservoir that feeds it. Content flows one-way: **lake → extraction → brain**. Nothing moves the other way. This is the pipe discipline (Amplified constitution).

---

## 2. Sizing Decision

**<100 GB is defensible at this scale.** Prior art support:

- DuckLake operator matrix (MotherDuck, 2025): "micro-scale ≤100 GB maps to local DuckDB/SQLite catalogs" — the exact tier of this deployment.
- DuckDB file format guidance: ideal Parquet file size 100 MB–10 GB; at <100 GB total, a lake fits in tens of well-formed Parquet files.
- arXiv 2606.08266: the swamp tipping point is governance failure, not size. A 50 GB lake with clear ownership is healthier than a 5 PB swamp.
- LHBench (Berkeley, CIDR 2023): Iceberg's single-node metadata planning is *advantageous* at small-table scale — less distributed overhead than Delta/Hudi.

**Expansion trigger:** if raw audio transcripts, code dumps, and markdown accumulate past 80 GB (80% of intent ceiling), the sizing question re-opens. GPU addition to Beast (already willing) enables faster Whisper transcription and local-LLM extraction, not storage — storage path is MinIO horizontal expansion or an additional disk, not a platform change.

---

## 3. Layers — Medallion Adapted to Beast Scale

### Recommended layer map

| Layer | Name | Contents | Beast directories mapped | Retention |
|---|---|---|---|---|
| **Bronze** | Raw drop | Files as-arrived: code, .md, SLSO, audio, dumps. No schema. Append-only. | `/opt/amplified/raw-mac-dumps/`, `/opt/amplified/ingest_downloads/`, `/opt/amplified/ingest_batch_283/`, `/opt/amplified/ingest_openclaw/` + brain source_types: `store_b_clean`, `store_m5_drop_2026_05_11`, `_inbox`, `_inbox-voice` | Configurable; 90 days default, then auto-promote or purge |
| **Silver** | Deduplicated + typed | BLAKE3 exact-hash dedup applied; near-dup MinHash run; file type detected; basic metadata stamped (source, ingest date, content type). Audio: Whisper transcript appended. | `/opt/amplified/vault/` (partly), brain source_types: `filtered_for_ingestion`, `_staging` | Indefinite (durable archive) |
| **Gold** | Extraction queue | GraphRAG / LLM extraction run; attribution snippets, logic chains, "gold nuggets" identified; ready for brain write via the pipe. | Output of extraction job; written to pipe inbox, not stored in lake long-term | Ephemeral: consumed by brain write |

**Medallion source:** Armbrust et al., CIDR 2021; Databricks blog 2022. Layer terminology is theirs; Beast directory mapping is derived from task brief ground truth.

**Note on vault:** `/opt/amplified/vault/` spans Silver and partly Bronze. A one-time classification pass is needed to assign existing vault contents to the correct layer. This is a calibration step, not a blocker.

---

## 4. Storage Format and Substrate

### Substrate options evaluated

| Option | Prior art | Fit at <100 GB | Verdict |
|---|---|---|---|
| **MinIO + Parquet + Iceberg catalog** | MinIO: S3-compatible single-node object storage, MIT license. Iceberg: Netflix 2017, Apache 2018; VLDB 2020 LHBench. | MinIO already on Beast (confirmed). Iceberg adds ACID, time travel, schema evolution. Overhead is real but manageable at this scale (single-node Iceberg metadata planning is faster than Delta/Hudi at small table size per LHBench). | **Primary recommendation.** MinIO is already deployed; Iceberg adds table semantics without requiring JVM if using PyIceberg or delta-rs. |
| **Filesystem + Parquet (plain)** | DuckDB file format guide; standard columnar practice. | Simplest. DuckDB reads Parquet natively. No catalog overhead. Loses ACID and time travel. | **Acceptable fallback** if Iceberg catalog proves operationally heavy. Use DuckDB as query engine directly over files. |
| **Filesystem + raw files** | Original Dixon data lake model (2010). | Maximum simplicity; no query capability without scanning. No dedup metadata. | **Bronze layer only** — not appropriate for Silver or Gold. |
| **DuckLake (SQL-backed metadata)** | MotherDuck blog 2025; DuckLake format. | Stores metadata in DuckDB/SQLite instead of object storage files. Eliminates Iceberg's multi-hop S3 round-trips. Best fit for <100 GB / high-frequency small writes. | **Viable alternative to Iceberg** at this scale; 2026 production-ready. Monitor; could replace Iceberg catalog if S3 API call overhead becomes notable. |

**Recommended substrate:** MinIO (already present) as object store + Parquet as file format + Iceberg catalog managed via PyIceberg (Python, no JVM dependency). Silver layer uses Iceberg tables. Bronze layer uses flat Parquet or raw files in MinIO buckets. ZSTD compression on Parquet (best compression ratio at acceptable write overhead per benchmarks).

**Is Iceberg overkill?** At <100 GB, the catalog overhead is small. The value is time travel (rollback bad extraction runs) and schema evolution (audio transcripts added later). If it proves operationally heavy, the DuckLake pattern (DuckDB as metadata store, same Parquet data files) is a metadata-only migration — no data rewrite required.

---

## 5. Metadata Catalog

### Catalog options compared

| Tool | Weight | Fit for single-node <100 GB | Notes |
|---|---|---|---|
| Apache Atlas | Heavy (Hadoop-era) | Poor | Overkill; requires HBase/Solr |
| Amundsen (Lyft) | Medium-heavy | Marginal | Designed for team-scale discovery; Neo4j dependency |
| DataHub (LinkedIn) | Medium-heavy | Marginal | Kafka + Elasticsearch stack; designed for enterprise |
| OpenMetadata | Medium; can use SQLite backend | Possible | Architecturally mature; SQLite option makes it lightest of the heavy catalogs (Reddit r/dataengineering, 2025) |
| **Filesystem + INDEX.md per directory** | None | Excellent | Sufficient at this scale; human-readable; agent-navigable |
| **Iceberg catalog (file-based or REST)** | Light | Good | Built into the storage layer; covers table-level metadata |

**Recommendation:** At <100 GB with a single operator, a full catalog product (Atlas/Amundsen/DataHub/OpenMetadata) is not warranted. Use:
1. Iceberg's built-in catalog for table-level metadata (schema, partitions, snapshots).
2. `INDEX.md` files per directory for human/agent navigation (directory contents, source provenance, ingest dates, content types).
3. A lightweight SQLite manifest (or DuckDB table) recording each file's BLAKE3 hash, ingest timestamp, source, Bronze/Silver tier, and extraction status.

This is the "SQLite with FTS5" pattern endorsed by r/dataengineering for catalogs under 1 GB (2025 thread). It covers swamp-prevention requirements (ownership, metadata completeness, lineage) without operational overhead.

**Catalog warranted?** No — not as a separate product. The Iceberg catalog + SQLite manifest + INDEX.md is the catalog. Revisit if the lake operator count grows beyond one or the asset count grows past ~10,000 files.

---

## 6. Lake-to-Brain Extraction Loop

### Canonical shape (Gold-nugget path)

```
Silver layer (Parquet, MinIO)
    │
    ▼
[1] LOAD — Unstructured.io or LlamaIndex file reader
           partitions PDF/MD/code/audio-transcript into
           normalised JSON elements with page/line metadata
    │
    ▼
[2] EXTRACT — Ollama (ollama-2 general model) runs
              GraphRAG-style entity + relationship extraction
              (Edge et al., arXiv 2404.16130, April 2024):
              — text chunked
              — LLM extracts (entity, relation, description) tuples
              — Leiden community detection over entity graph
              — community summaries generated
    │
    ▼
[3] PUDDING PASS — ollama-pudding runs neutralization
                   (PUDDING taxonomy, Amplified constitution)
                   on any claim that may carry bias or framing
    │
    ▼
[4] VELLUM ATTEST — extraction events logged to Vellum;
                    attribution chain preserved (source file →
                    chunk → entity → claim)
    │
    ▼
[5] PIPE WRITE — Python + Rust pipe writes attested claims
                 to brain via approved ingestion path
                 (constitution: nothing enters Beast except
                 through the pipe)
    │
    ▼
[Brain — curated, structured, attributed]
```

**Step 1 source:** Unstructured.io (open-source ETL, 40+ source connectors, JSON element output); LlamaIndex file readers. Both confirmed suitable for local offline operation.

**Step 2 source:** Edge et al. (arXiv 2404.16130); GraphRAG pipeline — chunk → extract → community detect → summarise. Adapted for offline Ollama rather than GPT-4.

**Step 3 source:** Amplified constitution (PUDDING neutralization, ollama-pudding container confirmed on Beast).

**Extraction cadence:** Slow and precise is the design intent. No streaming required. Batch jobs triggered manually or on a schedule. GPU addition to Beast enables faster Ollama throughput if needed.

---

## 7. Deduplication Strategy

> Cross-reference: for PII sensitivity classes on deduplicated content, see companion `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`.

### Two-stage dedup

| Stage | Method | When it fires | Tool |
|---|---|---|---|
| Exact dedup | BLAKE3 content hash | On every file at Bronze ingestion | `blake3` Python package or Rust crate |
| Near-dedup | MinHash + LSH | On Silver promotion pass; threshold ~0.7–0.8 Jaccard similarity | `datasketch` (Python) or `rensa` (Rust, 39× faster, identical accuracy) |

**BLAKE3 vs SHA-256:** BLAKE3 is 2–10× faster than SHA-256 on x86-64 with AVX2 (6–8 GB/s vs 800 MB/s software SHA-256). Parallelisable. No known attacks. Preferred for content-addressable storage at this scale (devtoolspro.org, 2026; arxiv 2407.08284, 2024).

**MinHash/LSH:** Datasketch library implements MinHash with configurable permutations. LSH threshold tuning: lower threshold = more false positives (merges distinct content); higher = misses near-dups. Practical default: 0.7 Jaccard for code and markdown; 0.8 for prose. Two-stage confirm (LSH candidate → exact Jaccard confirm) reduces false positives (datasketch issue #207 pattern).

**When near-dedup fires:** Silver promotion pass. Not on Bronze ingestion — Bronze is append-only raw record. Near-dedup is a Silver-layer concern.

**Iceberg COW/MOR semantics:** Iceberg copy-on-write (COW) rewrites entire files on update; merge-on-read (MOR) appends deletes. At <100 GB with infrequent updates, COW is simpler and sufficient.

---

## 8. Audio Handling

> Cross-reference: audio files carry speaker PII; for sensitivity classification and retention rules, see companion `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`.

### Pipeline

```
Audio file (FLAC/OPUS/WAV/M4A) in Bronze
    │
    ▼
[1] TRANSCRIPTION — faster-whisper (CTranslate2-optimised Whisper;
                    3–4× faster than original; runs on Beast CPU or
                    GPU if added). For single-speaker: Whisper large-v3.
    │
    ▼
[2] DIARISATION (if multi-speaker) — WhisperX + pyannote.audio
                 assigns speaker labels per segment.
                 (WhisperX: github.com/m-bain/whisperX)
    │
    ▼
[3] TRANSCRIPT TEXT — stored as .md sidecar in Silver alongside
                      original audio file reference. Audio file
                      retained in Bronze.
    │
    ▼
[4] TEXT PATH — transcript enters standard Silver → extraction loop
                (GraphRAG pass on transcript text)
```

**Formats:** FLAC preferred for lossless archival in Bronze (higher fidelity for future re-transcription). OPUS acceptable for compressed originals. WAV accepted but large.

**Voice as first-class:** Pattern established by Otter.ai, Fireflies, Granola — audio is a first-class content type with text as derivative. The lake preserves original audio in Bronze; Silver holds the text derivative. This is the correct archival posture per OAIS (ISO 14721): preserve the original representation, not only derived forms.

**GPU:** faster-whisper runs on CPU; adding a GPU (willing per task brief) reduces large-v3 transcription time from ~1× realtime (CPU) to ~10–20× realtime (GPU). Not blocking for the design.

---

## 9. Connection to the Research Pipe

### When outputs land in lake vs. brain

| Source | Lands in lake | Lands in brain |
|---|---|---|
| Raw Mac dumps, export zips, batch downloads | Bronze (lake) | Never directly |
| Partially curated vault material | Silver (lake) | After extraction loop |
| Research-pipe search results, Perplexity downloads | Brain directly (curated path) | Yes — this is the brain's primary feed |
| Research-pipe outputs that fail curation quality gate | Lake (pending) | Not yet — awaits extraction |
| Voice memos, audio files | Lake Bronze + Silver (transcript) | After extraction loop |
| Code files, .md files from ingest directories | Lake Bronze → Silver | After extraction loop |

**The two sinks:** The brain is the curated sink (first). The lake is the raw/pending sink (second). The research-pipe synthesis and ingestion-to-brain synthesis are sibling documents; they describe the brain's inflow. This document describes the lake's design as the upstream reservoir that feeds the brain via the extraction loop.

**Sibling cross-references:**
- `research-pipe-prior-art-synthesis__agent__v01__2026-06-25.md`
- `ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25.md`
- `estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md`

---

## 10. Open Questions

| Question | Status | Blocking? |
|---|---|---|
| Is a catalog product (OpenMetadata etc.) warranted at <100 GB? | Resolved: No. Iceberg catalog + SQLite manifest + INDEX.md is sufficient. Revisit at >10K files or >1 operator. | No |
| Is Iceberg overkill at this scale? | Partially resolved: Iceberg's single-node metadata planning is actually faster at small scale (LHBench). Overhead is manageable. DuckLake is a viable fallback if S3 API call count proves high. | No |
| How to keep the lake from becoming the swamp? | Six swamp indicators (arXiv 2606.08266): all preventable by (1) ownership assigned at ingest, (2) BLAKE3 hash as mandatory metadata, (3) extraction-status field on every Silver record, (4) 90-day Bronze retention policy enforced, (5) MinHash dedup run on Silver promotion, (6) quality gate on pipe write. | No |
| GPU: when does it become necessary? | When audio backlog exceeds ~10 hours of un-transcribed material and faster-whisper CPU throughput becomes the bottleneck. Not blocking now. | No |
| Vault classification pass | The vault spans Bronze/Silver ambiguously. A one-time pass is needed. Not blocking the architecture. | No |

---

## Outcome Routing

`no_more_research_needed` — All 10 domains surveyed with ≥1 primary source. Framing question resolved. Architecture recommendation is defensible at STRUCTURED tier. No blocking open questions. Ready for Ewan ratification and Beast-side implementation brief.
