---
title: "Handoff Prompt — Synthesize Research Folder → Parallel Implementation Plan"
document_type: handoff_prompt
artifact_id: PROMPT__synthesis-plan-handoff__2026-06-30__claude
folder: research-datalake-db-30-06-2026
date_utc: 2026-06-30
author: antigravity
epistemic_tier: INTUITED
audience: [claude, cursor, devin]
purpose: Paste-ready prompt for a fresh Claude session to synthesize all research, plan the end-to-end pipeline, and blueprint a parallel 3-lane execution map for the fleet.
---

# Handoff — Research Folder → E2E Parallel Implementation Plan

**Use this document as the operating brief for a NEW Claude instance.** Your role in this session is **planning only** — you will synthesize the research folder into a start-to-finish implementation plan with external verification at waypoints, and split the work into parallel lanes for the fleet (Claude, Cursor, Antigravity) to execute concurrently.

Do **not** edit codebase files or write operational code in the planning session. Focus on blueprinting the implementation and ratifying the plan.

---

## A. Mission Statement

Synthesize **all** material in `perplexity-inbox/research-datalake-db-30-06-2026/` into a single **verified, dependency-ordered, parallel implementation plan** for Amplified Partners' sandbox intelligence lake architecture.

The architecture flows as follows:
$$\text{Raw Ingestion (Monologue/ASR)} \xrightarrow{\text{Shape Gate}} \text{Bronze Lake (MinIO/Raw)} \xrightarrow{\text{FastCDC}} \text{Silver Lake (Atomized + Clustered + YAMLed)} \xrightarrow{\text{Lenses}} \text{Projections (DuckDB / AGE Graph / Vector)}$$

Atoms must be linked primarily by **labeling and chronology** (800–1,500 tokens, ~300 line cap) rather than rigid foreign keys. Phoneme normalization is **secondary** (P1/P2, isolated search touchpoints).

### Tonight's Urgent Priorities:
1.  **S5 Brain Ingestion Rewire**: Redirect the Brain write path to consume Silver lake atoms.
2.  **S6 Database Data Migration**: Migrate existing database records and batons into the structured lake format.

Every major architectural claim must survive an external falsification pass (using SearXNG disprove queries, academic anchors via OpenAlex, and adversarial demotes) before the plan is finalized.

---

## B. Required Reading List

Read the files in this order before constructing the plan. Each chunk has a paired `partner-*__source-context.md` — read both:

### B.1 — Folder Index & Synthesis Prep (Mandatory First)
*   [README.md](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/research-datalake-db-30-06-2026/README.md)
*   [SYNTHESIS-PREP__multi-seat-chunk-index__2026-06-30__cursor.md](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/research-datalake-db-30-06-2026/SYNTHESIS-PREP__multi-seat-chunk-index__2026-06-30__cursor.md)
*   [session_master.md](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/research-datalake-db-30-06-2026/session_master.md) (The refined high-fidelity chunk extraction of the un-chunked reference run)
*   [consolidated_15_threads.md](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/research-datalake-db-30-06-2026/consolidated_15_threads.md) (The master dialogue compilation and comparative study)

### B.2 — Multi-seat Harvest Chunks
*   `chunk-01a2ab34-1` to `-3` (Fleet routing configurations, meta-layer ignorance maps, and data lake pathways)
*   `chunk-11410e93-1` to `-3` (Research pipe indexes, Business Brain safety harnesses, and baton-to-datalake mapping)
*   `chunk-cf0da9b0-1` to `-2` (Shape gate YAML/OPA boundaries and honesty tier arbiters)
*   `chunk-antigravity-agentfs-1` (AgentFS dual-YAML 19-field filesystem schema)
*   `chunk-I` (Cross-thread prior art)

---

## C. Operating Constraints

| Constraint | Requirement |
| :--- | :--- |
| **Mac read-only push** | No direct `git push` from Mac. Land changes via Cascade-Mac / Devin PR on Beast. |
| **Worktree door** | Feature work in isolated worktree; branch `task/sandbox-intelligence-lake` under `.worktrees/`. |
| **Vellum witness** | Post PLAN intent before substantive work; ACTUAL on close. Epistemic tier: `INTUITED`, author `claude`. |
| **Constitutional gate** | Refuse rod violations (Privacy, Security, Sovereignty — no raw Brain-as-primary-dump, no client data leaks). |
| **Finish waypoint** | Plan must trace to completion ladder F1–F8 (see Section F). |
| **Self-compounding** | Any gaps resolved during planning must be encoded as a rule, hook, or harness in the repository. |
| **Token efficiency** | Scan/Glob before reading full files; use subagents for >2 unread files or >100 log lines; use CLI for read-only Brain queries. |
| **No stop sequences** | Do not specify `STOP_SEQUENCES` in LLM configs; rely on `MAX_TOKENS`. |

---

## D. Planning Methodology (Phase 0–4)

### Phase 0 — Orientation & Claim Inventory
1.  Read all materials listed in Section B.
2.  Build an internal claim inventory mapping: `Architect Intent | Conclusion | Gap | Target Code Path`.
3.  Check for newly submitted seat chunks from **antigravity**, **claude**, or **cascade-mac**. If present, resolve overlaps.

### Phase 1 — Write Staged Implementation Plan
Draft **`PLAN__sandbox-intelligence-lake__v01__2026-06-30__claude.md`** in this folder containing:
1.  **Architecture Specifications**: Merged blueprint of the logic base, neutral data lake, and lens projections.
2.  **Verdicts Carry Forward**: Confirm SOLID/WEAK/GAP status of findings from previous sessions (e.g., Codd/FD logic, 19-field schema).
3.  **Medallion Storage Flow**: Document exact directories for Bronze (raw), Silver (atoms), and Gold (lenses).
4.  **Diagrams**: Mermaid sequence of the pipeline (ingest $\rightarrow$ lake $\rightarrow$ lenses) and label/chronology node structures.

### Phase 2 — External Verification Waypoints
For **each major claim**, run a **disprove-first** query on SearXNG, then narrow to precision documents, and query OpenAlex for academic papers.
*   *Verification Table*: You must fill out the verification table documenting: `Claim | Disprove Query | Counter URL | Supporting URL | Verdict (SOLID/WEAK/GAP)`.
*   *Claims to verify*:
    1.  Codd/FD logic informs atom boundaries without enforcing warehouse 3NF on lake.
    2.  Label + chronology primary link model is superior to rigid foreign key joins.
    3.  Atomized chunks (~800-1500 tokens) yield the highest RAG recall compared to flat top-$k$.
    4.  Lake-first ingest and keeping the Brain database as a Gold lens (not primary dump).
    5.  Conformal set, semantic entropy, and OPA shape gates at the ingestion boundary.

### Phase 3 — Staged Execution Map (S0–S8)
Sequence stages S0 to S8 with dependencies, acceptance criteria, test commands, and unique IDs:
*   `S0 Worktree` $\rightarrow$ `S1 Hooks/Harnesses` $\rightarrow$ `S2 Lake Spec` $\rightarrow$ `S3 Ingest Pipeline` $\rightarrow$ `S4 Lens Projections` $\rightarrow$ `S5 Brain Ingestion Rewire` $\rightarrow$ `S6 Data Migration` $\rightarrow$ `S7 Search Layer` $\rightarrow$ `S8 Smoke Tests`.

### Phase 4 — Multi-Agent Parallelization Blueprint
Blue-print the parallel lane allocation for the three active agents (Cursor, Claude, Antigravity) to execute the plan concurrently:

```mermaid
flowchart TD
    subgraph Lane 1 [Claude: Ingestion & Safety]
        direction TB
        L1_1[Ingestion hooks / harnesses]
        L1_2[Shape gate & OPA validator]
        L1_3[IgnoranceGap events]
    end

    subgraph Lane 2 [Antigravity: Physical Lake & Schema]
        direction TB
        L2_1[Silver atom structure & dual-YAML]
        L2_2[FastCDC chunking integrations]
        L2_3[MinIO/Iceberg mapping]
    end

    subgraph Lane 3 [Cursor: Lenses & Search]
        direction TB
        L3_1[DuckDB sandbox & relational views]
        L3_2[AGE Graph & Vector sync]
        L3_3[Search layer & autocorrect]
    end

    Lane 2 --> Lane 1
    Lane 2 --> Lane 3
```

---

## E. Parallel Lane Assignments & Paths

To ensure clean-room parallel execution without file conflict, map files to lanes:

### Lane 1: Ingestion & Boundary Safety (Claude)
*   **Remit**: Ingestion hooks, shape gate validations, Whisper fine-tuning configurations, key-adjacency correction layers, and `IgnoranceGap` triggers.
*   **Target Paths**: `perplexity-inbox/harness/shape_gate.py`, `inbox_watcher.py`, `extract_and_chunk.py`, `.cursor/hooks/`.

### Lane 2: Physical Storage & Data Lake (Antigravity)
*   **Remit**: Silver lake atom file structures, 19-field YAML validation schemas, FastCDC chunking integrations, and MinIO/Iceberg coordinates mapping.
*   **Target Paths**: `perplexity-inbox/harness/glasses_loader.py`, `docs/atom-spec-v1.md`, `.worktrees/task-sandbox-intelligence-lake/`.

### Lane 3: Database Projections & Lenses (Cursor)
*   **Remit**: DuckDB sandbox creation (`intelligence_lake.db`), pgvector/AGE Brain graph rewrites, relational projections, lens weighting rotation algorithms, and search/autocorrect query layer.
*   **Target Paths**: `perplexity-inbox/harness/db_harness.py`, `perplexity-inbox/harness/search_autocorrect.py`, `search_chunks.py`.

---

## F. Completion Waypoints (F1–F8)

Your plan must map deliverables to the completion ladder:
*   **F1 Door Opened**: Worktree branch set, Vellum PLAN posted.
*   **F2 Start Sensor**: Ingestion start scripts run and logged.
*   **F3 Work Witnessed**: Mid-point commits and tests documented.
*   **F4 End Proof**: pytest checks green (`test_lake_pipeline.py`).
*   **F5 Company Share**: Consolidated results delivered to the inbox.
*   **F6 Completion Witness**: Vellum ACTUAL posted.
*   **F7 Door Closed**: Baton rotated, worktree cleared.
*   **F8 Published**: GitHub PR reviewed and merged to main.

---

## G. Starter Action
Start with Phase 0. Post your Vellum PLAN intent, read the mandatory reading list in Section B, and output the staged architecture and parallelization blueprint.
