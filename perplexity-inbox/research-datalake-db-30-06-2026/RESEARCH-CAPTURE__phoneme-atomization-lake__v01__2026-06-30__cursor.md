---
title: "Research Capture — Phoneme Atomization & Neutral Data Lake"
document_type: research_capture
artifact_id: RESEARCH-CAPTURE__phoneme-atomization-lake__v01__2026-06-30__cursor
date_utc: 2026-06-30
corpus_item_id: phoneme-atomization-lake-2026-06-30
author: cursor
reader: ewan
epistemic_tier: INTUITED
source_threads: [0e0bd954, 1f9920af, 7a3e928f, df5da61b]
archive_engine_resolved: "xarviv → OpenAlex (L2 academic) + Common Crawl (L4 web archive); arXiv via OpenAlex"
---

# Research Capture — Phoneme Atomization & Neutral Data Lake

> **Priority correction (2026-06-30):** Architect clarified two goals were conflated. **PRIMARY research is now database/lake structure** — see `RESEARCH-CAPTURE__ai-data-lake-structure__v01__2026-06-30__cursor.md`. This document remains valid for the **SECONDARY** phoneme/accent normalization thread; do not lead with it.

**Purpose:** Capture every architect thesis point and every research finding from prior subagent runs. Each item flagged for follow-up. Companion to `RESEARCH-PIPE-RUN__phoneme-deterministic-normalizer__v01__2026-06-30__cursor.md`.

---

## Section A — Architect thesis points (thread 0e0bd954)

Plain-language restatement of verbatim intent. Status reflects inbox/Beast encoding today.

| # | Architect point | STATUS |
|---|-----------------|--------|
| 1 | **Foundational DB maths (50s–90s) before hardware caught up** — Codd normal forms, Armstrong FD axioms, relational theory; blend with AI-specific atom construction (19-field schema, graph projection). | **partially encoded** — `docs/ai_native_data_organization.md` (19-field atoms), `harness/lake_pipeline.py` (DuckDB lake); no explicit Codd→AI bridge doc |
| 2 | **Labeling, organization, data lake as neutral storage** — lake holds raw/processed without homogenizing; specialised DBs (vector, graph, ops) project from lake. | **partially encoded** — medallion in prior-art bundle; DuckDB `intelligence_lake.db`; multi-DB projection not wired |
| 3 | **Organization is organization** — neutral, multi-purpose taxonomy; no forced single schema across consumers. | **partially encoded** — `chunks/README.md` taxonomy; `ESTATE-TAXONOMY.md`; enforcement hooks incomplete |
| 4 | **Atomization of data** — each atom must be non-nonsense; nonsense atoms are useless downstream. | **needs research** — 19-field metadata exists; no nonsense-detection gate or atom validity rubric |
| 5 | **Guard against byte-for-byte dedup led astray by fat fingers / poor spelling** — BLAKE3 on raw bytes misses phonetic/spelling variants. | **partially encoded** — BLAKE3/MinHash in data-lake synthesis; `search_autocorrect.py` is grapheme Levenshtein only — **no phonetic blocking keys** |
| 6 | **Phoneme = sounds** — accents matter in transcription (architect corrected STT: "Beemones"/"phemone" → phoneme). | **needs research** — concept captured in thread; no phoneme column or accent-normalization code in inbox |
| 7 | **Deterministic phoneme process at INGEST to data lake** — cleaning, labeling, structure before Silver atoms. | **needs research** — ingest path exists (`inbox_watcher.py`, `lake_pipeline.py`); no phoneme normalizer at ingest gate |
| 8 | **Same deterministic process at SEARCH time** — query normalized so wrong spelling still finds right atoms. | **partially encoded** — `harness/search_autocorrect.py` + `scripts/search_chunks.py`; **grapheme-only**, not phoneme-aware |
| 9 | **Real-time audio→transcription feed** — reduces token spend and downstream cascade (Monologue → paste → ingest). | **needs research** — Verbatim Acoustic Intake Valve in `overallpicture1` chunks; no Monologue hook encoded in inbox harness |
| 10 | **Academic prior art exists; internal audio/failure-pattern evidence sufficient for algorithmic fix** — don't over-research what internal corpus can prove. | **needs research** — academic anchors found (SearXNG/OpenAlex); **failure-pattern corpus not inventoried** (GAP UNRESOLVED) |
| 11 | **Deterministic code pyramid below interpretation/reconstruction** — normalizer/dedup/keys sit under LLM layer for AI-readable DB format. | **partially encoded** — doctrine in thread + deterministic-first email agent precedent; phoneme pyramid not built |
| 12 | **NOT Russian maths/linguistics interpretation** — grammatical correction without corrupting natural language (no destructive normalization). | **needs research** — tension with Verbatim Acoustic Intake Valve; dual-stream Bronze/Silver proposed, not ratified |
| 13 | **Research pipe with SearXNG wide→narrow→wide** (`search.beast.amplifiedpartners.ai`). | **encoded** — 20-query pass in RESEARCH-PIPE-RUN; SearXNG HTTPS verified this session |

---

## Section B — Findings from prior runs (subagents 1f9920af, 7a3e928f, df5da61b)

Each finding: source path/URL + `NEXT:` research action.

### B.1 Internal encoded prior art

| Finding | Source | NEXT |
|---------|--------|------|
| Query autocorrect: Levenshtein + alias map on canonical vocab | `harness/search_autocorrect.py` | Add Double Metaphone / phonetic blocking alongside Levenshtein; measure on 50-utterance corpus |
| DuckDB intelligence lake: documents/chunks/clusters | `harness/lake_pipeline.py` → `data/intelligence_lake.db` | Add `phonetic_key` + `dmetaphone` columns to schema migration |
| 19-field AI-facing atom schema; `/archive/` vault; dual YAML | `docs/ai_native_data_organization.md` | Extend schema with phoneme spine fields: `{phoneme_seq, grapheme_span, morpheme_id, dmetaphone_key}` |
| Data-lake synthesis: Dixon 2010, Armbrust lakehouse, medallion, BLAKE3/MinHash, WhisperX | `prior-art-syntheses-bundle/data-lake-prior-art-synthesis__human__v01__2026-06-25.md` | Cite only — do not re-research medallion; add phoneme-aware dedup layer on top |
| Filesystem lake taxonomy (doctrine/rules/research/…) | `chunks/README.md` | Map taxonomy nodes to atom types for multi-DB projection |
| Chunks search CLI with autocorrect hook | `scripts/search_chunks.py` | Wire shared `PhonemeNormaliser v1` at query time (touchpoint 3) |
| **Verbatim Acoustic Intake Valve** — preserve false starts, certainty 1–9, ▲ metaphor tags; rejects human-centric normalization | `Amplified-Partners/Research/chunks/overallpicture1-28-06-26__chunk_22.txt` (lines 10–36); chunk_21 (lines 314–354) | Ratify dual-stream: Bronze verbatim immutable + Silver normalized keys; architect sign-off |
| Referenced script (may be aspirational): `parse_verbatim_speech_to_ai_tokens.py` | chunk_24 cites `/clean-build/02_build/scripts/parse_verbatim_speech_to_ai_tokens.py` | Verify existence on Beast; inventory vs inbox gap |
| Five research-pipe backends on Beast | `prior-art-syntheses-bundle/research-pipe-prior-art-synthesis__human__v01__2026-06-25.md` | Use OpenAlex + Common Crawl for academic/archive gaps (this capture, Section C) |

### B.2 Tension (dual-stream resolution)

| Finding | Source | NEXT |
|---------|--------|------|
| **Bronze vs Silver conflict:** Verbatim valve preserves typos/false starts; phoneme canonicalization needs normalized keys for dedup/search | RESEARCH-PIPE-RUN §Tension; overallpicture1 chunks | Implement prototype: same utterance → Bronze row (raw) + Silver row (normalized + phonetic keys) |
| Recommendation: `PhonemeNormaliser v1` same ruleset at all 3 touchpoints; LLM above normalizer | RESEARCH-PIPE-RUN architecture diagram | Spec function signature + test vectors before code |

### B.3 SearXNG survivors (pass 7a3e928f — 20 queries)

| ID | Survivor | URL | NEXT |
|----|----------|-----|------|
| S1 | WFST open-source G2P toolkit | https://aclanthology.org/W12-6208 | Code probe: fork/adapt WFST alignment tools for deterministic spine |
| S2 | Morpheme-based G2P | https://dl.acm.org/doi/10.1145/595576.595580 | Evaluate morpheme as atom unit vs whole-word phoneme keys |
| S3 | EDC: Extract, Define, Canonicalize (EMNLP 2024) | https://github.com/clear-nus/edc | Map EDC entity canonicalization to text-atom → graph projection |
| S4 | 3NF/BCNF for property graphs | https://link.springer.com/article/10.1007/s00778-025-00902-2 | Relate Codd normal forms to AGE graph atomization |
| S5 | DuckDB medallion local lakehouse | https://github.com/datatomas/duckdb-medallion | Fork pattern for Bronze/Silver Parquet in inbox lake |
| S6 | Accent-invariant ASR (saliency-driven) | https://arxiv.org/html/2510.09528v1 | Dual-POV: WFST deterministic vs neural accent handling for Monologue |

### B.4 Academic anchors (pass 1f9920af)

| Domain | Anchor | Citation | NEXT |
|--------|--------|----------|------|
| Relational NF | Codd 1971 | https://doi.org/10.1145/320557.320571 | Write 1-page Codd→19-field-atom mapping |
| FD inference | Armstrong axioms 1974 | Armstrong 1974 | Use for atom dependency validation rules |
| Phonetic keys | Double Metaphone (Philips) | Lawrence Philips 2000 | Add `dmetaphone` column; test on architect misspellings |
| ASR ITN | NeMo WFST ITN (Pynini) | https://doi.org/10.21437/interspeech.2021-1571 | Compare ITN ruleset vs phoneme normalizer scope |
| Entity resolution | Fellegi & Sunter 1969 | Record linkage theory | Phonetic blocking for entity merge without byte dedup |
| ASR error correction | FastCorrect (NeurIPS 2021) | https://arxiv.org/abs/2105.03842 | Dual-POV: deterministic vs neural spelling correction at search |

### B.5 Gaps (merged — all GAP UNRESOLVED unless noted)

| Gap | NEXT |
|-----|------|
| Failure-pattern audio/text corpus not inventoried | Inventory Brain `_inbox-voice`, vault transcripts; count accent/spelling failure modes |
| No phoneme spine in inbox code | Spec + prototype `PhonemeNormaliser v1` |
| WFST vs neural dual-POV for architect speech | Run parallel eval on 50 utterances; architect flags Δ≥3 |
| Atom schema: phoneme + entity + provenance | Draft production spec; reconcile 19-field vs APDS packet drift |
| Multi-DB projection (Brain pgvector + DuckDB + AGE) on same canonical IDs | Integration map after atom schema ratified |
| `intelligence-lake.mdc` not found | Search Beast clean-build; or encode rule in inbox |
| `process_brain/` unreachable from Mac | SSH Beast or delegate to cascade-mac seat |

---

## Section C — Archive engine results (this run)

### C.1 Name resolution: "xarviv"

| Checked | Result |
|---------|--------|
| Grep `xarviv` / `xarvix` / `archive engine` in perplexity-inbox | **Only hit:** architect STT in `overallpicture1-28-06-26 .txt` line 430: *"searXNG, xarviv and others"* |
| Grep clean-build (Mac path) | Path unreachable from Mac workspace |
| Grep `.cursor/skills` | No match |
| Fleet backend roster | **No executable named xarviv** |

**Resolved fleet names (INTUITED):**

| Architect speech | Fleet canonical name | Role | Runnable this session |
|------------------|---------------------|------|----------------------|
| **xarviv** (likely STT) | **OpenAlex** | L2 academic backend; indexes arXiv, DOI, journals | ✅ `api.openalex.org` — 6 queries run |
| (same cluster) | **arXiv** | Preprint archive (via OpenAlex + SearXNG) | ✅ survivors returned |
| "archive engine" (web) | **Common Crawl** | L4 web archive backend (`research_pipe/backends/common_crawl.py`) | ✅ CDX index API — 2 records returned |
| — | **Semantic Scholar** | L3 academic backend | Not run (OpenAlex sufficient for gaps) |

### C.2 OpenAlex queries (academic archive engine)

| Query | Top survivors |
|-------|---------------|
| `phoneme grapheme normalization speech recognition` | Connectionist Speech Recognition (W1553004968); End-to-End ASR Survey (doi:10.1109/taslp.2023.3328283) |
| `grapheme-to-phoneme WFST deterministic` | **Mlphon: Multifunctional G2P using FSTs** (doi:10.1109/access.2022.3204403); SIGMORPHON 2016 Shared Task (doi:10.18653/v1/w16-2002) |
| `Fellegi Sunter record linkage entity resolution` | Blocking and Filtering Techniques for Entity Resolution (doi:10.1145/3377455) |
| `Codd normalization relational database third normal form` | Multivalued dependencies and new NF (doi:10.1145/320557.320571); Extending relational model (doi:10.1145/320107.320109) |
| `NeMo WFST inverse text normalization speech` | NeMo ITN: Development to Production (doi:10.21437/interspeech.2021-1571; arXiv:2104.05055) |

### C.3 Common Crawl CDX probe (web archive engine)

| Query | Result |
|-------|--------|
| `*.aclanthology.org/W12-6208*` on CC-MAIN-2024-10 | 2 index records; aclanthology.org crawled 2024-02-21 and 2024-02-28; WARC paths returned |

**Note:** Beast `research_pipe` container runs Common Crawl backend internally; Mac seat used public CDX API as read-only archive probe.

### C.4 SearXNG queries (this run — 7 additional)

| Phase | Query | Key survivors |
|-------|-------|---------------|
| Wide | `phoneme grapheme normalization deterministic G2P` | Fraunhofer multitask seq2seq G2P PDF; ACL W17-5403 multilingual G2P |
| Narrow | `WFST grapheme-to-phoneme open source toolkit` | **W12-6208** (confirmed) |
| Narrow | `FastCorrect speech recognition spelling error correction` | FastCorrect NeurIPS 2021; FastCorrect 2 EMNLP Findings 2021 |
| Narrow | `Double Metaphone phonetic matching entity resolution` | Double Metaphone algorithm (ResearchGate); Splink phonetic comparisons doc |
| Wide | `medallion architecture data lake bronze silver atomization` | Databricks medallion docs; Conduktor bronze/silver/gold |
| Narrow | `accent invariant speech recognition phoneme normalization` | arXiv:2510.09528v1 (confirmed S6); IEEE unsupervised accented ASR |
| Narrow | `EDC Extract Define Canonicalize entity canonicalization EMNLP` | ACL 2024.emnlp-main.548; github.com/clear-nus/edc |
| Narrow | `property graph third normal form database normalization` | Springer VLDB J 2025 (S4 confirmed); VLDB P3031 PDF |

---

## Section D — Academic additions from this run

New survivors not fully captured in prior RESEARCH-PIPE-RUN.

| ID | Title | Source | Relevance |
|----|-------|--------|-----------|
| A1 | **Mlphon: Multifunctional G2P using Finite State Transducers** | doi:10.1109/access.2022.3204403 (OpenAlex) | Modern FST G2P toolkit — complements W12-6208 for deterministic spine |
| A2 | **Blocking and Filtering Techniques for Entity Resolution** | doi:10.1145/3377455 (OpenAlex) | Phonetic blocking without byte dedup — directly addresses architect point #5 |
| A3 | **FastCorrect / FastCorrect 2** | arXiv:2105.03842; ACL 2021.findings-emnlp.367 | Neural spelling correction — dual-POV vs deterministic normalizer |
| A4 | **Multivalued dependencies and a new normal form** (Codd 1977) | doi:10.1145/320557.320571 | Foundational NF for architect point #1 |
| A5 | **NeMo Inverse Text Normalization** | doi:10.21437/interspeech.2021-1571 | Production WFST ITN — ingest-time deterministic normalization precedent |
| A6 | **Splink phonetic algorithms guide** | moj-analytical-services.github.io/splink | Practical Double Metaphone / Soundex blocking patterns |

**Demoted this run:** YouTube medallion tutorials, generic GeeksforGeeks 3NF explainers, ResearchGate mirrors where ACL primary exists.

---

## Section E — Master research queue (prioritized)

| P | Item | Blocks | Owner hint |
|---|------|--------|------------|
| **P0** | Inventory failure-pattern corpus (Brain `_inbox-voice`, vault transcripts) | MEASURED tier; prototype tuning | cursor + Beast MCP |
| **P0** | Architect ratify dual-stream Bronze/Silver vs Verbatim Acoustic Intake Valve | Any ingest normalizer implementation | ewan |
| **P1** | Spec `PhonemeNormaliser v1`: WFST G2P (W12-6208) + Double Metaphone + alias map; same function at 3 touchpoints | Touchpoints 1–3 | cursor |
| **P1** | Atom schema v2: add phoneme spine to 19-field schema | Multi-DB projection | cursor |
| **P1** | 50-utterance prototype gate: accent/spelling join recall across search queries | Promotion past INTUITED | cursor |
| **P2** | Dual-POV eval: WFST/Mlphon vs FastCorrect vs accent-invariant ASR (S6) | Monologue touchpoint 1 | cursor |
| **P2** | EDC fork/adapt for entity canonicalization at Silver layer | Graph projection | cascade-mac |
| **P2** | DuckDB schema migration: `phonetic_key`, `dmetaphone`, Bronze/Silver tables | Lake ingest | cursor |
| **P2** | Codd→19-field-atom mapping doc (1 page) | Architect point #1 clarity | scribe |
| **P3** | Property-graph 3NF (S4) applied to AGE entity atoms | Graph normal form | devin |
| **P3** | Verify `parse_verbatim_speech_to_ai_tokens.py` on Beast | Verbatim valve encoding | cascade-mac |
| **P3** | Wire Common Crawl backend on Beast for archive-wide methodology search | Fleet archive engine | devin |

---

## Cross-reference

- **Primary run doc:** `RESEARCH-PIPE-RUN__phoneme-deterministic-normalizer__v01__2026-06-30__cursor.md` (merged pass 3 additions in this session)
- **Architect source:** thread 0e0bd954; voice corpus `overallpicture1-28-06-26 .txt`
- **Subagent passes:** 1f9920af (internal+WebSearch), 7a3e928f (SearXNG 20q), df5da61b (referenced in parent brief)

---

*Author: cursor · Epistemic tier: INTUITED · 2026-06-30*
