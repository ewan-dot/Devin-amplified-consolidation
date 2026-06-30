---
title: "Estate Taxonomy (AI-Only Master Directory)"
document_type: "infrastructure_map"
epistemic_grade: "FACT"
author: "antigravity"
date: "2026-06-28"
valid_until: "2026-12-31"
---

# Estate Taxonomy — AI-Only Master Directory

> [!NOTE]
> This is a machine-readable directory designed purely for Sovereign AI self-orientation. It maps the host servers, databases, filesystems, and APIs of the Amplified Partners estate, detailing their purpose, contents, and connection constraints.

---

## 1. Physical & Virtual Host Layer

| Host / Node Identifier | Type | Location | Purpose / Role |
| :--- | :--- | :--- | :--- |
| `Beast` | Dedicated Server | Hetzner AX-162-R (48-core EPYC, 256GB RAM) | Core production host running the Dockerized agent runtime, Temporal worker engines, and postgres/vector/AGE datastores. |
| `Mac Mini (M5)` | Local Machine | Local Office (24GB RAM) | Clean-room build sandbox, local CLI workstation, and git-worktree checkout workspace. |

---

## 2. Beast Database Layer (Port 5433 / `cove-postgres` Container)

> [!IMPORTANT]
> The Docker container hosting all PostgreSQL databases is named `cove-postgres`. The default login user is `cove`. Connection string formatting: `postgresql://cove:<pass>@127.0.0.1:5433/<db_name>`. Do NOT default to `/cove` for business brain transactions.

| Database Name | Apache AGE Graph? | pgvector? | What It Is For (Role) | What Answers It Holds (Data & Tables) |
| :--- | :--- | :--- | :--- | :--- |
| `amplified_brain` | **ACTIVE** | **ACTIVE** | Canonical, single source of truth for the Sovereign Business Brain. | • Graph `business_brain` (89,385 nodes): Entity relations, client models, extracted rules.<br>• Graph `compound_design` (53,959 nodes): Architecture codebases, structural nodes.<br>• Tables `research_findings`, `design_patterns`, `pipeline_runs`. |
| `cove` | **INACTIVE** (Clean target) | **INACTIVE** | APDS orchestration metadata, build plans, Temporal tasks, and executor status logs. | • Tables `agent_runs`, `build_plans` (24 rows), `tasks` (218 rows).<br>• Table `system_prompts` (685 rows): Base prompts for agent fleet.<br>• Table `kaizen_applied_changes` (661 rows): Self-healing improvements. |
| `vellum` | **INACTIVE** | **INACTIVE** | Hash-chained integrity ledger for fleet operations and state persistence. | • Table `vellum_entries` (2,578 rows): Signed audit blocks.<br>• Table `vellum_batons` (13 rows): Task baton transfers.<br>• Table `vellum_sheets` (126 rows): Configuration mappings. |
| `amplified_crm` | **INACTIVE** | **INACTIVE** | Client Relationship Management metrics and contact history. | • Tables `contacts`, `companies`, `deals`, `call_transcripts` (Empty today, ready for intake). |
| `langfuse` | **INACTIVE** | **INACTIVE** | AI observability database for tracing calls, cost tracking, and prompts. | • Tables `traces`, `observations`, `scores`, `models` (135 rows). |
| `amplified_main` | **INACTIVE** | **INACTIVE** | System checkpoints database. | • Tables `checkpoint_migrations`, `checkpoint_writes`. |

---

## 3. Storage & Cache Layer (Beast Containerized)

| Resource | Type | Port | Purpose / Role | What Answers It Holds |
| :--- | :--- | :--- | :--- | :--- |
| `clickhouse` | Columnar DB | `9000` | Telemetry logs and analytics. | Structured time-series system traces and performance metrics. |
| `minio` | S3 Storage | `9000` | S3-compatible file storage. | Audio files, raw PDF/docx attachments, database backups. |
| `redis` | Key-Value Cache| `6379` | Message broker and caching. | Temporal workflow schedules, Celery task states, SearXNG search result cache. |

---

## 4. Local Filesystem & Codebase Directories

| Path | Host | Purpose / Role | Key Files & Assets |
| :--- | :--- | :--- | :--- |
| `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/` | Mac Mini | Input dropzone for Perplexity logs and research briefs. | Raw markdown exports, doc transcripts, `ESTATE-TAXONOMY.md` (this file). |
| `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/harness/` | Mac Mini | Gating and policy validation harnesses. | `shape_gate.py` (YAML tier validator), OPA policies in `/opa/amplified/`. |
| `/Users/ewansair/ingestion-to-research-pipe/clean-build/02_build/` | Mac Mini | Gated python research pipeline codebase (589 .py files). | Stage 1 validator (`intake/validator.py`), Stage 2 Search (`router.py`), Stage 5 staging emitter. |
| `/Users/ewansair/control-centre/` | Mac Mini | Deterministic core orchestration codebase. | Rule engines (`rules/engine.py`), preflight validators, metric collectors. |
| `/Users/ewansair/.gemini/config/skills/amplified-mathematical-validator/` | Mac Mini | Global Customizations | Global customization skill for Taguchi bounds, Cosine Dispersion, Semantic Entropy, and Conformal Predictions. |

---

## 5. Local AI & Search APIs

| Endpoint | Host | Service | Purpose / Role | Configuration Rules |
| :--- | :--- | :--- | :--- | :--- |
| `http://127.0.0.1:11435` | Beast | Ollama (Embeddings) | Generates dense vectors for knowledge search. | Run `all-minilm` embedding model. |
| `http://127.0.0.1:11436` | Beast | Ollama (Reasoning) | Local, cost-controlled inference execution. | Run `llama3.1:8b` completions model. |
| `http://127.0.0.1:8080` | Beast | SearXNG API | Private search aggregator for web research. | Accessible via private network alias `172.18.0.3` on Beast. |

---

## 6. Execution Guards & Safety Assertions

1.  **Split-Database Guard:** Any script targeting `business_brain` or `compound_design` MUST assert that `database_name == 'amplified_brain'` and that the node count exceeds `10000`. It must explicitly reject writes if connected to `/cove` or `/postgres`.
2.  **Secret Scrubbing Guard:** No secrets, raw passwords, or private SSH keys may cross the `pre-ingest-tier-gate` boundaries or be committed to repository logs. Verified by `/harness/shape_gate.py`.
3.  **Epistemic Floor Cap:** Any seat that invoked an LLM during text generation must cap its frontmatter output at `epistemic_tier: INTUITED`. Promotion to `STRUCTURED` or higher requires formal validation via the `promotion_record_id` gate.
4.  **Write Gate Safety Guard:** All writes to the semantic graph database via Vellum are gated. They must pass three strict bounds: `semantic_entropy < 0.4` (consensus check), `conformal_set_size <= 2` (confidence check), and `sandbox_verified == True` (isolated transactional rollback execution proof). Violating items are aborted with `HTTP 400` and emit `brain_write_blocked` warnings.
