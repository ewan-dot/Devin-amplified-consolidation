# Amplified Brain — Complete System Spec & Re-Ingestion Plan
**Date:** 2026-05-21
**Author:** Northumbrian-Sweep (3ca9d061)
**Audience:** Perplexity (research), Claude (oracle), Devin (execution), Ewan (architect)
**Status:** Living document — current as of 2026-05-21 05:00 BST

---

## 1. Brain Database (PostgreSQL on Beast)

### 1.1 Core Tables

| Table | Rows | Purpose |
|-------|------|---------|
| `knowledge_vectors` | 1,910,100 | Raw chunks + 384-dim vector embeddings |
| `brain_documents` | 172,817 | One row per unique ingested file |
| `brain_packets` | 172,780 | Governed knowledge packets (7-stage curated) |
| `brain_relationships` | 0 | Packet-to-packet links (SHAPE TAGGER MISSING) |
| `brain_curation_runs` | 12 | Audit trail of every curation stage |
| `brain_packet_evidence` | 1.47M | Links packets to evidence chunks |
| `brain_dedupe_clusters` | 40,255 | Deduplication clusters (not yet mapped to relationships) |

### 1.2 Epistemic Tier Distribution

| Tier | Count | % |
|------|-------|---|
| INTUITED | 172,712 | 99.96% |
| STRUCTURED | 22 | 0.01% |
| MEASURED | 46 | 0.03% |
| PROVEN | 0 | 0% |

### 1.3 Route Distribution

| Route | Count |
|-------|-------|
| review | 144,941 |
| drop_from_active | 19,465 |
| quarantine | 7,455 |
| validate | 899 |
| keep (active) | 20 |

### 1.4 Connection

```
PostgreSQL: 127.0.0.1:5433 (Beast host) → cove-postgres:5432 (Docker)
Database:   amplified_brain
User:       cove (admin), brain_reader (read-only), brain_writer (write)
Auth:       trust for Docker bridge (172.18.0.0/16), scram-sha-256 for external
MCP:        brain-mcp-readonly on port 8090, brain-mcp-writer on port 8080
```

---

## 2. Ingestion Pipeline

### 2.1 Flow

```
File → Porch (/opt/amplified-machine/porch/incoming/)
     → Pipe Watcher (porch_to_brain.sh, 60s cycle)
     → Pre-validate (Pydantic schema, 17+ fields, secret detection)
     → Agent Layer (17+ fields) OR Human Layer (<17 fields)
     → Enricher (gpt-4o-mini for markdown, deterministic for code)
     → Chunker (chunker_v4.py, 4 strategies)
     → Embedder (text-embedding-3-small via OpenAI API, EMBED_OPENAI=1)
     → knowledge_vectors + brain_documents
```

### 2.2 Current Porch State

- **Incoming:** 247 files (was 27,325 — pipe processed 27K)
- **Agent layer:** 710 files waiting for embedding
- **Human layer:** 7,067 files (preserved, not embedded)

### 2.3 Bottlenecks

1. **Gate strictness:** 17+ YAML fields required. Most files have <17.
2. **Code files:** No YAML frontmatter → routed to human_layer, never embedded.
3. **Single pipe watcher:** No parallelism.
4. **CPU embeddings replaced:** Now using EMBED_OPENAI=1 (faster, ~$13/backlog).

---

## 3. Curation Pipeline (7 Stages)

### 3.1 Stages

| Stage | File | Status |
|-------|------|--------|
| 1. Inventory | `inventory.py` | Complete — groups chunks into documents |
| 2. Version Families | `version_families.py` | Complete — finds document versions |
| 3. Packet Builder | `packet_builder.py` | Complete (v2: batched INSERTs, 45.6x speedup) |
| 4. Epistemic Tiering | `epistemic_tier.py` | Complete — assigns INTUITED/STRUCTURED/MEASURED/PROVEN |
| 5. Route Decider | `route_decider.py` | Complete — keep/freeze/archive/review/quarantine |
| 6. Validation Sampler | `validation_sampler.py` | Complete — 100-packet stratified sample |
| 7. Freeze | `freeze.py` | Complete — locks canonical packets |
| **MISSING** | `shape_tagger.py` | **NOT BUILT** — Antigravity designing now |

### 3.2 Orchestrator

- **File:** `/opt/amplified/devon/run_curator.py`
- **Fixed 2026-05-20:** Corrected 5 broken imports, per-stage run_ids, stops on failure
- **v2 packet_builder:** Batched transactional INSERTs, 500/batch, ON CONFLICT DO NOTHING

---

## 4. Vellum (Custody & Communication Layer)

### 4.1 What It Is

- **Append-only JSONL ledger** — every file, tier change, recognition verdict
- **REST API** — Brief, Council, Reply, UI modes
- **MCP Server** — 6 tools for agent communication
- **Hash-chained** — every entry links to previous via SHA-256
- **Auth:** Disabled by default (VELLUM_AUTH_ENABLED=0)

### 4.2 Ledgers

| Ledger | Path | Entries |
|--------|------|---------|
| Packets | `/opt/amplified/logs/vellum_packets.jsonl` | 180,921 |
| Recogniser | `/opt/amplified/logs/vellum_recogniser.jsonl` | 12,660 |
| Trace | `/opt/amplified/logs/vellum_trace.jsonl` | 3 |
| Ollama | `/opt/amplified/logs/vellum_ollama.jsonl` | 1 |
| Llama Brain | `/opt/amplified/logs/vellum_llama_brain.jsonl` | 10 |

### 4.3 API Endpoints

```
Vellum URL: http://172.18.0.25:8400

GET  /api/v1/sheets                          — list sheets
GET  /api/v1/sheets/{id}                     — read sheet
POST /api/v1/sheets/{id}/entries             — post entry (hash-chained)
POST /api/v1/sheets/generate                 — create new sheet
GET  /api/v1/decisions                       — list decisions
```

### 4.4 Agent Inboxes

| Agent | Sheet ID |
|-------|----------|
| Northumbrian-Sweep | `e86ef59f-616f-43f4-9d9d-9ee510731dd9` |

---

## 5. MCP Servers (Model Context Protocol)

| Server | Port | Tools | Access |
|--------|------|-------|--------|
| Knowledge MCP | 8401 | 24 (graph, entity, search, audit) | Internal |
| Beast Control MCP | 8402 | 13 (filesystem, Docker, Git, porch_upload) | Perplexity |
| Brain MCP (readonly) | 8090 | Direct brain queries | Claude Desktop |
| Brain MCP (writer) | 8080 | Direct brain writes | Pipeline only |

---

## 6. SearXNG Pipe (Internet Search)

### 6.1 Connection

```
Container: searxng
Network:   172.18.0.18:8080 (amplified-net)
```

### 6.2 API Endpoints

```
GET /search?q=query&format=json     — search (JSON response)
GET /config                          — engine configuration
GET /healthz                         — health check
```

### 6.3 Enabled Engines

Arch Linux Wiki, Artic, Arxiv, Bandcamp, Bing, Bing Images, Bing News, Brave, DuckDuckGo, GitHub, Google, Google Images, Google News, Google Scholar, Stack Overflow, Wikipedia, Wolfram Alpha, YouTube...

### 6.4 Integration Plan

1. Agent identifies knowledge gap
2. Queries SearXNG for research
3. Results enriched and attributed
4. Fed back through ingestion pipe
5. Curator re-evaluates tier

---

## 7. LLM Infrastructure

### 7.1 Ollama (Local — Free, Sovereign)

| Model | Size | Status |
|-------|------|--------|
| `llama3.1:70b` | 42GB | Installed, never used |
| `llama3.1:8b` | 4.9GB | Currently loaded, minimal use |
| `qwen3-coder:30b` | 18GB | Installed, never used |
| `all-minilm` | 45MB | Embeddings (bypassed — using OpenAI) |
| `nomic-embed-text` | 274MB | Installed, never used |

**Ollama Vellum Bridge:** `/opt/amplified/devon/ollama_vellum_bridge.py`
**Brain-Llama Bridge:** `/opt/amplified/devon/brain_llama_bridge.py`

### 7.2 API Models (Credits Available)

| Model | Key Location | Credits | Current Use |
|-------|-------------|---------|-------------|
| OpenAI (gpt-4o-mini) | BATON_PASS.md | Pay-as-you-go | Enricher, Embedder |
| DeepSeek (deepseek-chat) | Session-provided | Credits available | Recogniser |
| Grok-3 (xAI) | Session-provided | "Shit loads" | Recogniser |
| Kimi (Moonshot) | Session-provided | DEAD KEY | Blocked |
| Claude Opus 4.7 | Claude Max subscription | Fixed monthly | Brain Oracle (new) |

### 7.3 Model Roles

| Role | Model | Reason |
|------|-------|--------|
| Enricher (markdown) | gpt-4o-mini | Fast, cheap, consistent |
| Enricher (code) | Deterministic Python | No LLM needed |
| Embedder | text-embedding-3-small | $0.10/1M tokens |
| Recogniser 1 | Grok-3 | Credits available, strict |
| Recogniser 2 | DeepSeek | Credits available, balanced |
| Brain Oracle | Claude Opus 4.7 | Subscription, best reasoning |
| Bulk classifier | Grok-3 or DeepSeek | Credits, speed |

---

## 8. DuckDB Dedup Engine

### 8.1 Assets on Beast

```
/opt/amplified/devon/pudding_dedup/
├── compact_windows.parquet        (1.9GB, 247M rows, 34,874 files)
├── tokens.parquet                 (95MB, 37,121 files, 450MB original)
├── nearduplicate_groups.parquet   (696MB, 114M pairs)
└── duckdb_dedup.py               (self-join script, 128GB/96 threads)
```

### 8.2 Results

- **114,962,077** near-duplicate pairs found
- **34,874** unique files in pond
- **18 hours** runtime on 128GB RAM, 96 threads
- **NOT YET CLUSTERED** — pairs need transitive closure into groups

### 8.3 Rust Fuzzy Dedup

- **Binary:** `/opt/amplified/quantum-dedup/target/release/quantum-dedup`
- **Method:** MinHash + LSH (85 bands, 3 rows, ~22% Jaccard)
- **Target:** 800MB unstructured text
- **Status:** Binary working, not yet run on real data

---

## 9. Re-Ingestion Plan (Fast Track — Money No Object)

### 9.1 Current State

- 172,712 INTUITED documents (99.96%)
- 247 files in porch incoming
- 710 files in agent layer awaiting embedding
- Shape tagger missing — no relationships between packets
- Frontmatter/metadata incomplete on many documents

### 9.2 Speed Plan

**Phase 1 — Parallel Ingestion (1 hour)**
- Deploy 4 parallel pipe watchers instead of 1
- Each processes a subset of porch files
- Use EMBED_OPENAI=1 (already active)
- Cost: ~$20 in OpenAI embedding costs

**Phase 2 — Bulk Classification (2-4 hours)**
- Use Grok-3 (bulk credits) to classify all 172K INTUITED documents
- 32 parallel API workers
- Classify: PROMOTE / FLAG / KEEP
- Record all decisions to Vellum
- Cost: ~$50-100 in Grok credits (or free if credits cover it)

**Phase 3 — Curator Re-Run (30 minutes)**
- Run curator v2 on newly classified documents
- Batched INSERTs, 45.6x speed
- All 7 stages complete in under 30 minutes

**Phase 4 — Shape Tagger (when built)**
- Antigravity's new stage links documents via relationships
- Maps dedup clusters → supersedes relationships
- Parses frontmatter references → typed relationships

**Phase 5 — Enrichment Loop (ongoing)**
- Light documents → SearXNG research → enrich → re-ingest
- Curator re-evaluates → tier promotion if evidence supports

### 9.3 Cost Estimate

| Phase | Cost | Time |
|-------|------|------|
| Parallel ingestion | ~$20 | 1 hour |
| Bulk classification | ~$50-100 (or free) | 2-4 hours |
| Curator re-run | $0 | 30 minutes |
| Shape tagger | $0 | When built |
| **TOTAL** | **$70-120** | **4-6 hours** |

### 9.4 Alternative: Free Path (Slower)

- Use local llama3.1:70b instead of Grok-3
- Single pipe watcher
- Time: 24-48 hours
- Cost: $0

---

## 10. Key Paths Reference

### Beast (135.181.161.131)

| Resource | Path |
|----------|------|
| Porch watcher | `/opt/amplified/devon/porch_to_brain.sh` |
| Curator | `/opt/amplified/devon/run_curator.py` |
| Enricher (markdown) | `/opt/amplified/devon/enricher_v2.py` |
| Enricher (code) | `/opt/amplified/devon/code_enricher.py` |
| Vellum recorder | `/opt/amplified/devon/vellum_recorder.py` |
| Vellum MCP server | `/opt/amplified/devon/vellum_mcp_server.py` |
| Ollama bridge | `/opt/amplified/devon/ollama_vellum_bridge.py` |
| Brain-Llama bridge | `/opt/amplified/devon/brain_llama_bridge.py` |
| DuckDB dedup | `/opt/amplified/devon/pudding_dedup/` |
| Rust dedup | `/opt/amplified/quantum-dedup/target/release/quantum-dedup` |
| Brain ingest | `/opt/amplified/devon/brain_ingest/` |
| Brain curator | `/opt/amplified/devon/brain_curator/` |
| Vellum app | `/opt/amplified/vellum/` |

### Local Mac

| Resource | Path |
|----------|------|
| Main workspace | `/Users/ewansair/clean-build/` |
| Vellum UI | `/Users/ewansair/AgentMesh/` |
| Recovery | `/Users/ewansair/Amplified-Brain-Recovery/` |
| Portable spine | `/Users/ewansair/portable-spine/` |
| Extracted code | `/Users/ewansair/code/` |
| System spec | `/Users/ewansair/BRAIN_SYSTEM_SPEC.md` |
| Curator spec | `/Users/ewansair/CURATOR_SPEC.md` |
| Multi-model plan | `/Users/ewansair/MULTI_MODEL_PLAN.md` |
| Engineering perspective | `/Users/ewansair/ENGINEERING_PERSPECTIVE.md` |
| Next phase plan | `/Users/ewansair/NEXT_PHASE_PLAN.md` |
| Agent skill | `/Users/ewansair/.devin/skills/northumbrian-sweep/SKILL.md` |
| Baton pass | `/Users/ewansair/.devin/deepseek-memory/BATON_PASS.md` |

---

## 11. AI Deterministic Sandwich & Validation Gates

<!-- AI-IGNORE: Bracketed terms are for human reference only. Do not parse or extract. -->
**Date:** 2026-06-30  
**Status:** Canonical Spec Addendum  

To enforce zero-variance safety across the estate, all probabilistic agent reasoning runs ("The Meat") are wrapped in strict, non-probabilistic validation gates ("The Buns"). The system maps physical targets using an operational metadata store `[cove]` and a semantic graph index `[amplified_brain]`, running on a high-capacity server host `[Beast]` and developers' workstations `[Mac Mini (M5)]`.

```
[Top Bun: Inbound Gate]
    - Validate 17-field schema header & cryptographic integrity hashes.
    - Run pre-flight complexity checks & routing decisions.
        |
        v
[The Meat: Probabilistic Inference]
    - Compile EBNF vocab restrictions from credentials.
    - Sample step-by-step reasoning paths (N=16).
        |
        v
[Bottom Bun: Outbound Gate]
    - Semantic entropy & conformal prediction check (statistical boundaries).
    - Rust AST security check & Postgres Sandbox isolated DML dry-run.
    - OPA policy verification -> commit transaction & sign ledger.
```

### 11.1 The 10 Literature-Backed Safety Gap Closures

1.  **Threshold Calibration (Contextual Bandit Routing)**  
    *Prior Art / Theory:* PILOT (arXiv 2508.21141).  
    *Mechanism:* Evaluates vector dispersion ($D_R$) of retrieved RAG contexts. If $D_R \ge 0.15$, the query is automatically routed to a task decomposition meta-planner rather than a single generative reasoning pass.
    
2.  **Two-Pass Sampling (Monte Carlo Temperature)**  
    *Prior Art / Theory:* MCT (arXiv 2502.18389).  
    *Mechanism:* Executes a high-temperature estimation pass ($T=1.0$) over $N=16$ candidates to gauge output distribution variance, followed by a low-temperature execution pass ($T=0.1$) selecting from the validated subset.

3.  **Conformal Calibration Set**  
    *Prior Art / Theory:* ConU (arXiv 2407.00499).  
    *Mechanism:* Computes non-conformity scores on a calibration dataset. The true pass rate of the Rust AST & OPA gate acts as the ground-truth label, bounding model uncertainty within a guaranteed confidence level ($1-\alpha$).

4.  **Credential Revocation**  
    *Prior Art / Theory:* Short-TTL Token Gating (SoK arXiv 2603.22928).  
    *Mechanism:* Enforces short-lived JSON Web Tokens (JWT) for agent execution, querying a cryptographically sealed revocation registry at every gate entry to block stale or hijacked agent sessions.

5.  **Decomposition Depth**  
    *Prior Art / Theory:* ReDel (arXiv 2408.02248).  
    *Mechanism:* Imposes a maximum recursive depth ceiling (e.g., `max_depth = 3`) on task decomposition. If sub-tasks exceed this depth, execution is halted and routed to human operator escalation.

6.  **Declarative Policy Gating**  
    *Prior Art / Theory:* OPA Rego Gating over AST.  
    *Mechanism:* Compiles output code (SQL / Python) into an Abstract Syntax Tree (AST) using a fast Rust parser, then runs Open Policy Agent (OPA) declarative rules directly over the JSON-serialized AST structure rather than raw text regexes.

7.  **Database Sandbox Verification**  
    *Prior Art / Theory:* Transaction-Isolated Rollbacks.  
    *Mechanism:* Outbound database mutations are executed inside a sandboxed PostgreSQL transaction. The engine performs `GET DIAGNOSTICS ROW_COUNT` audits and verifies system constraints before forcing a hard `ROLLBACK`.

8.  **Dynamic Inference Scaling**  
    *Prior Art / Theory:* Compute-Optimal Scaling (Snell et al. / arXiv 2408.03314).  
    *Mechanism:* Dynamically adjusts sample candidate count ($N$) based on the computed context dispersion ratio ($DR$):
    $$N = \max\left(4, \min\left(16, \left\lceil \frac{DR}{0.03} \right\rceil\right)\right)$$

9.  **Gate Attestation**  
    *Prior Art / Theory:* Sealed Hash Chains (Rebound / arXiv 2511.13641).  
    *Mechanism:* Validations are stored in a hash-chained integrity ledger `[vellum]`. The output of each step includes a cryptographic signature of the previous node's hash state, preventing temporal state tempering.

10. **Process Reward Model (PRM) Circularity Prevention**  
    *Prior Art / Theory:* ReST-MCTS* (arXiv 2406.03816) + RM-R1 (arXiv 2505.02387).  
    *Mechanism:* Eliminates single-model self-evaluation bias by scoring step-by-step reasoning traces against external compile-time sandbox execution feedback rather than LLM self-rewards.

---

## 12. Single Outbound Doorway Protocol

<!-- AI-IGNORE: Bracketed terms are for human reference only. Do not parse or extract. -->
To simplify system updates and prevent random file mutations across the codebase, executing AIs are restricted to exactly ONE outbound doorway. Instead of directly executing file writes or git staging across multiple folders, the AI writes its proposed changes into a single designated directory:
*   **Doorway Path**: `/Users/ewansair/ingestion-to-research-pipe/outbound_doorway/`
*   **Asset format**: JSON patch files named `patch_[timestamp]_[agent_id].json`.

### 12.1 Patch Format Schema
```json
{
  "agent_id": "antigravity",
  "timestamp": "2026-06-30T13:45:00Z",
  "changes": [
    {
      "file_path": "/absolute/path/to/target/file",
      "action": "modify",
      "target_content": "Exact lines of code to modify...",
      "replacement_content": "New replacement content..."
    }
  ]
}
```

### 12.2 Deterministic Execution Bun (Rust Compilation Guard)
To prevent executing agents from modifying validation scripts in-flight to bypass checks, all core safety gates and doorway patch runners must be compiled in Rust and run as binaries from the central, read-only `/Users/ewansair/control-centre/bin/` folder (or `/opt/amplified/bin/` on Beast). 

The doorway runner is deployed as `/Users/ewansair/control-centre/bin/apply_doorway`. It monitors the `/Users/ewansair/ingestion-to-research-pipe/outbound_doorway/` directory, parses incoming JSON patches, runs AST validation over changes, executes modifications, and commits them. By using a compiled binary rather than an editable Python script, the validation rules are made immutable against dynamic prompt-injection edits by the agent fleet.

### 12.3 Configuration Mutation Guard
To enforce sovereignty and security boundaries, agents are strictly forbidden from modifying configuration, rules, or hook files. The doorway applicator enforces a hard block on the following path patterns:
*   `.cursorrules`
*   `.clauderules`
*   `.cursor/` (including all hooks and project-scoped rules)
*   `.claude/`
*   `hooks.json`
*   `AGENTS.md`
*   `ESTATE-TAXONOMY.md`

Any patch targeting these paths is immediately rejected with a `Banned path` error and flagged in Vellum logs.

---

## 13. AI Orientation DB Curation Protocol

<!-- AI-IGNORE: Bracketed terms are for human reference only. Do not parse or extract. -->
The active agent orientation files, environment configurations, and rules are indexed within a dedicated database table inside the main knowledge graph database `[amplified_brain]`. 

### 13.1 DB Schema
```sql
CREATE TABLE ai_orientation_guide (
    guide_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    version INTEGER NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    source_commit VARCHAR(40) NOT NULL
);
```

### 13.2 Strict Curation (Anti-Bloat) Transaction
To prevent semantic drift and database bloat, the database curation engine enforces a strict versioning rule: only the active version of any guide or orientation page remains in the database. Updating a topic deletes the prior version within a single transaction:
```sql
BEGIN;
DELETE FROM ai_orientation_guide WHERE topic = :topic;
INSERT INTO ai_orientation_guide (topic, content, version, source_commit)
VALUES (:topic, :content, :version, :source_commit);
COMMIT;
```

---

## 14. Filesystem-DB Cross-Verification & Local Search Protocol

<!-- AI-IGNORE: Bracketed terms are for human reference only. Do not parse or extract. -->
To maximize speed and token effectiveness while maintaining high reliability, the system implements a dual-structure cross-verification protocol.

### 14.1 Spotlight & Filesystem Search
AI agents prioritize local file-and-folder index lookups (using macOS Spotlight search tags or ripgrep search) for direct raw chunk and spec retrieval. This prevents large database queries and minimizes token-budget usage.

### 14.2 Mutual Verification
The local filesystem (containing raw document chunks and specs) and the graph/vector database (`[amplified_brain]`) serve as verification checks on each other.
*   **Integrity check**: The system executes a cron script that compares all document hashes in the filesystem (`perplexity-inbox/chunks/`) with the corresponding metadata nodes in `[amplified_brain]`.
*   **Outcomes**: Any unmapped database nodes or orphaned chunk files are immediately reported to the Vellum ledger as integrity exceptions (`hash_verification_mismatch`).

---

*Spec ends. Northumbrian-Sweep (3ca9d061) & Antigravity (logic-math-synthesis), Amplified Partners, 2026-06-30.*

*Ready for Perplexity research. Ready for Claude oracle. Ready for Devin execution.*