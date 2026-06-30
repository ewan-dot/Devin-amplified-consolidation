# Ingestion to Research Pipe — Dialogue Analysis (Part 1, Chunks 01–10)

This document provides a highly granular extraction and analysis of the raw dialogue chunks 01 to 10 from the session history folder `/Users/ewansair/ingestion-to-research-pipe/foundational_granularity_2026-06-30_18-54/raw_chunks/`.

---

## chunk_01.txt

### 1. Conclusions & Agreements
*   **Pipeline Goal:** The precise goal of the **Deterministic Prompt and Rules Sync Pipeline** is to enforce the **Assertion-Context Boundary** by synchronizing the local filesystem master ledger (stored under `/prompts/` and `/brain/logic_packets/`) to the database indexing layers (`cove` and `amplified_brain`). This prevents any semantic drift between the code/prompt states and the active database index.
*   **The File is the Node (AgentFS Core Concept):**
    *   Each individual Markdown file (`.md` or `.txt` chunk) is a self-contained, physical database node.
    *   The schema is enforced by a **19-field Dual-YAML header** (defining identity, coordinates, cryptographic witness, and scopes).
    *   The payload is the raw text content.
    *   Git acts as the database transaction log, providing rollback history, branch isolation, and diffs for free.
*   **The Database is the Map, Not the Storage:**
    *   The main database (`amplified_brain` running Postgres/Apache AGE) is **not** a data store. It is a **cognitive directory/registry**.
    *   It organizes the nodes (filesystem files) and maps the relationships (edges) between them.
    *   It holds the coordinate system (paths and hashes) to allow fast semantic and graph queries, but it does not house the actual knowledge.
*   **Constituent Chunks of the Sync Pipeline:**
    *   *Step 1: Parse and Validate (Filesystem Ledger):* Scans directories, reads the Dual-YAML headers, asserts the presence of the 19 required metadata fields, and validates the SHA-256 hash of the content against the header's `chunk_hash_sha256`. It rejects tampered, corrupt, or incomplete files at the gate.
    *   *Step 2: Sync to Orchestrator DB (`cove`):* Connects to the `cove` database (using connection guards) and upserts prompts into the `public.system_prompts` table with versioning.
    *   *Step 3: Sync to Main DB Graph (`amplified_brain`):* Connects to the AGE graph database and upserts vertices representing the rules/doctrinal files, updating their coordinate properties (file path, hash, epistemic tier, UUID) without storing raw body text.
    *   *Step 4: Verification Check (`--verify`):* Pulls current hashes from the databases and compares them against the filesystem, returning exit code `0` on match or `1` on drift.
*   **Part vs. Complete Goal:**
    *   *The Complete Goal:* A platform-agnostic, local-first data lake where AI agents can consume ingestion files, rules, and prompts with sub-millisecond retrieval.
    *   *This Part:* The sync script acts as the bridge writing the indices/relationships back to the PostgreSQL database on Beast, tying the filesystem and the graph together.

### 2. Logic & Constraints
*   **Assertion-Context Boundary:** The database remains a lightweight, sub-millisecond logical index (storing only pointers and metadata), while the filesystem remains the source of truth for raw context.
*   **Ledger File Validation Guard:** Rejects tampered, corrupt, or incomplete ledger files at the gate, ensuring only validated structural documents are written to the database.

### 3. Formulas & Operational Metrics
*   **Metadata Field Constraint:** A flat layout capped at exactly **17 to 20 fields** (standardized to 19 fields) to prevent transformer "Lost in the Middle" attention drift and minimize prompt token overhead.
*   **Hash Checking:** The SHA-256 hash of the text content must match the `chunk_hash_sha256` defined in the header.

### 4. Graph Updates & Concepts to Update
*   **Concept: AgentFS / Scale-Free Database:** The physical markdown file is the primary node; the database is a registry map.
*   **Graph Mapping `business_brain` (AGE graph inside `amplified_brain`):** Vertices represent rules/doctrinal files, storing coordinates (`file_hash_sha256`, `canonical_path`, `document_type`, `epistemic_tier`, `uuid`) and edges mapping their relationships, without storing raw text payloads.
*   **Database Tables:** `public.system_prompts` in the `cove` database.

### 5. Open Items
*   Execution of the sync script verification preflight test.

---

## chunk_02.txt

### 1. Conclusions & Agreements
*   **Superiority of AgentFS Model:**
    1.  *100% Data Sovereignty:* An SMB's database is a folder of files. They can zip their files and own their data without managing PostgreSQL, Docker, or AGE.
    2.  *Instant Rebuilds:* Running `sync_ledger_to_dbs.py` scans folders and completely reconstructs the query index in seconds if the database server is destroyed.
    3.  *Local-First AI Ergonomics:* AI agents query the index for coordinates and then read the filesystem directly, keeping database connections lightweight, fast, and secure.
*   **Division of Labor based on build characteristics:**
    1.  *AI (Probabilistic):* Good at synthesis, pattern matching, and reasoning over context. Bad at strict, zero-tolerance logic constraints.
    2.  *Python/Rust (Deterministic):* Excellent at parsing, hashing, checking bounds, and running database pre-flights. Zero pattern matching. Python/Rust is a full, critical partner in this decentralized intelligence.
*   **The Database is NOT a database:** It is a way of organizing rubrics, methodologies, algorithms, and mathematical theories in a way that allows AI to synthesize them.
    *   *The Math (The Tools):* Rubrics, methodologies, algorithms, and formulas (e.g. Altman's Z-Score, Theory of Constraints) used by the AI to compute answers.
    *   *The Logic (The Databases We Create):* The rules, constraints, and relationships that dictate how and when the AI applies those mathematical tools to a given dataset.

### 2. Logic & Constraints
*   **Fractal Schema (Scale-Free Database):** The exact same metadata fields describe the unit of data at every tier of scale:
    *   *Tier 0 (The Slice):* Granular facts (raw 300-line text file) described by local coordinates (e.g. `chunk_index`, `start_line`, `chunk_hash_sha256`).
    *   *Tier 1 (The Document):* An aggregation of Tier-0 slices (the overall file) described by coordinates encompassing the whole (e.g. `total_chunks: N`, `file_hash_sha256`). References Pillar UUID as parent.
    *   *Tier 2 (The Pillar/Corpus):* An aggregation of Tier-1 documents (e.g. "All Billing Doctrine"). Payload is a manifest of child UUIDs, and it links to the parent domain.
*   **AI Traversal Flow:** The AI reads a Tier-2 (Pillar) node to understand high-level governance/child documents, hops to a Tier-1 (Document) node to select the specific rule-set, and fetches only the Tier-0 (Slice) chunks matching the query.
*   **Taguchi Process Engineering:** Even if one piece of the base is incorrect, the pinnacle is blunted. Minor deviations at the base corrupt the outcome at the pinnacle.

### 3. Formulas & Operational Metrics
*   **Harness Script:** `harness/sync_ledger_to_dbs.py` implements parsing, verification, and upsert logic for both Postgres tables and the AGE graph.
*   **Field count:** Capped at 19 YAML frontmatter fields to describe any node at any scale.
*   **Chunk size constraint:** Tier-0 leaf slice capped at a maximum of 300 lines of text.

### 4. Graph Updates & Concepts to Update
*   **Concept: Scale-Free / Fractal Database (AgentFS).**
*   **Concept: Taguchi Process Engineering (Base-to-Pinnacle Deviation).**
*   **Concept: Math vs. Logic Separation.**
*   **AGE Graph node types:** `Document` vertices, `Mechanism` vertices in `business_brain` AGE graph.

### 5. Open Items
*   Pushed code synchronization checks and cleanup of test records.

---

## chunk_03.txt

### 1. Conclusions & Agreements
*   **Deterministic Sync Pipeline Structure & Flow:**
    *   *Filesystem Master Ledger:* `/prompts/` (e.g., `coder.md`) and `/brain/logic_packets/` (e.g., `RULE__schema.md`).
    *   *Python Sync Pipeline (`sync_ledger_to_dbs.py`):* Parses Dual-YAML frontmatter, performs cryptographic content check (SHA-256 vs `chunk_hash_sha256`), and executes pre-flight DB safety checks (`db_harness.py`).
    *   *Database Projections:* Upserts prompts to `cove.system_prompts` and executes AGE Cypher MERGE commands to write to `amplified_brain.business_brain` graph.
*   **Logic Sandwich (Retrieval Schema):**
    *   *Top Edge:* Doctrine / Rules (Constraints) — highest attention zone.
    *   *Middle Valley:* Subject Data / Chunks (Facts).
    *   *Bottom Edge:* Recipes (Formulas / Methodologies) — recency zone.
    *   The compiled Logic Sandwich forces the LLM to process constraints first, ensuring that its reasoning at the pinnacle is mathematically bounded by the rules at the base.
*   **Local Graph & Brain Metaphor:**
    *   *Cortex & Neurons:* Local filesystem folder taxonomy, chunk indices, and physical symlinks.
    *   *Short-Term Reflex (Local):* macOS Spotlight (`mdfind`) provides sub-millisecond local indexing of keywords and metadata tags without DB overhead.
    *   *Synapses:* Symlinks act as physical synapses linking files on disk. Walking folders is neural traversal.

### 2. Logic & Constraints
*   **Strict Error Isolation at the Gate:** Any deviation at the base (e.g. file content altered without updating the YAML hash, database schema target misconfigured) is blocked immediately by Python gates before it can pollute the index or feed corrupted contexts into the prompt sandwich.
*   **Lightweight Mapping:** Databases do not store fuzzy text; they store pointers and hashes, keeping ontological relationships clean, fast, and easy to audit.

### 3. Formulas & Operational Metrics
*   **Vector Cache:** `chunk_XX.vector` containing 384-dimensional float caches generated by a local MiniLM model.
*   **Chunk text scale:** Max 300 lines per text chunk slice.

### 4. Graph Updates & Concepts to Update
*   **Concept: The Logic Sandwich (Top: Doctrine/Rules, Middle: Subject Data/Chunks, Bottom: Recipes/Methodologies).**
*   **Concept: Local Graph (Cortex/Neurons: Filesystem folder structure, Spotlight, Symlinks).**
*   **Database Schema:** `cove.system_prompts` (Execution Variables).
*   **AGE Graph:** `amplified_brain.business_brain` (AGE Graph - Coordinates & Edges Only).

### 5. Open Items
*   Detailed justification of maintaining the centralized graph index alongside Spotlight.

---

## chunk_04.txt

### 1. Conclusions & Agreements
*   **Centralized Graph Index (Long-Term Memory / Hippocampus):**
    *   *Apache AGE (`amplified_brain`):* Serves as the central registry where synapses merge.
    *   *Why it is maintained:*
        1.  *Multi-Hop Reasoning:* Spotlight is great for single-step keyword filters, but it cannot traverse recursive multi-hop relationships. Apache AGE handles these complex, graph-traversal Cypher queries in milliseconds.
        2.  *Platform Cohesion:* The high-capacity server `[Beast]` runs Linux and lacks Spotlight. The AGE database on Beast replicates the exact coordinate mappings of Spotlight, allowing macOS agents and Linux servers to reason over the same index structure.
        3.  *Cross-Seat Synaptic Merging:* Different agents (Claude, Cursor, Devin) output findings at their edges, and the database acts as the central registry where their synapses merge.
*   **Three Layers of Cognitive Lighting (Observability Telemetry):**
    1.  *Terminal Pathway Light:* Prints the active traversal tree in the terminal using colored ASCII/Unicode lines (Doctrine Path -> Data Path -> Methodology Path).
    2.  *Synaptic Trail:* Signed entries in the `vellum` database (`vellum_entries` logs the sequence `Node A -> Edge -> Node B -> Read file_hash`) to create a durable, cryptographic trail of which part of the brain "fired".
    3.  *Visual Brain Hub (Next.js Dashboard):* Projects the AGE graph (`business_brain`) and Vellum synaptic log onto a force-directed network node visualizer (deemed by Ewan as "marketing theater/noise" unless it strictly shows whether the system is working or not, and if someone is dealing with it).
*   **Self-Tuning Harnesses via Thrash Reduction (How the Brain Learns):**
    *   *Learning Definition:* System learning in this architecture is not statistical backpropagation; it is structural accretion and epistemic evolution.
    *   *Epistemic Promotion (Gradient Upgrades):* All new research starts at `epistemic_tier: INTUITED` or `HYPOTHESIS` (isolated from active reasoning). When verified by tests, the validation harness promotes its file header to `STRUCTURED` or `PROVEN`, and the sync script updates the node in the AGE graph.
    *   *Synaptic Plasticity (Dynamic Traversal Mapping):* When an agent discovers a connection, it writes a filesystem symlink, which the sync script detects and maps as a `RELATES_TO` edge in Apache AGE.
    *   *Kaizen Feedback (Constraint Tuning):* When execution fails, the pipeline logs a `Friction` node. The Kaizen agent processes the friction log and refines the rule file on disk (e.g. updating `RULE__always-verify-schema.md`).

### 2. Logic & Constraints
*   **The Division of Labor Correction:** Ewan clarifies that the AI is the genius pattern matcher that handles optimization and adjustment of the harness. Ewan is the strategic architect steering the system. The Python/Rust binary validator does strictly binary, rule-based verification (checking if files exist, hashes match, and 19 fields are present).
*   **Self-Adjustment Loop:** AI analyzes telemetry, identifies bottlenecks, modifies prompts/rules in the filesystem ledger, and the Python sync pipeline acts as a firewall, validating hashes/schemas before updating databases.

### 3. Formulas & Operational Metrics
*   **Thrash telemetry variables:** Path execution cost ($1.50 vs $0.10), number of model calls (12 vs 2), and count of searched chunks (40 vs 3).

### 4. Graph Updates & Concepts to Update
*   **Concept: Centralized Graph Index (Hippocampus).**
*   **Concept: Epistemic Promotion Loop (INTUITED/HYPOTHESIS -> STRUCTURED/PROVEN).**
*   **Concept: Synaptic Plasticity.**
*   **Concept: Self-Tuning Harnesses via Thrash Reduction.**
*   **AGE Graph Edges:** `RELATES_TO` edge relationships.
*   **AGE Graph Nodes:** `Friction` nodes.

### 5. Open Items
*   Avoid proposing a heuristics engine (a "shit pattern matcher") to optimize the system. Keep the AI as the genius pattern matcher and Python as the binary validator.

---

## chunk_05.txt

### 1. Conclusions & Agreements
*   **Roles Lock-In:**
    1.  *Strategic Architect (Ewan):* Focuses on creative line dancing (strategy and outcomes) free from the laser's direct path because the base of the mountain is structurally locked in.
    2.  *Genius Pattern Matcher (AI):* Observes process thrash, reasons about looping/compute waste, and rewrites ledger rules/prompts.
    3.  *Binary Validator (Python/Rust):* Does zero pattern matching. Verifies strictly binary, rule-based conditions (existence, hashes, 19 fields).
*   **Critical Partnership:** Even though Python and Rust are deterministic, they are critical partners in this decentralized intelligence. If any single piece of the pyramid base fails to perform, the pinnacle is flattened.
*   **The Database is a Math and Logic Environment:**
    *   *The Math (The Tools):* Formulas, rubrics, algorithms, and mathematical theories (e.g. Altman's Z-Score, Theory of Constraints) compiled to compute answers.
    *   *The Logic (The Databases We Create):* Rules, constraints, and relationships dictating how and when to apply those mathematical tools to a dataset.
*   **Exploded Diagram Web App:** Initiated an interactive exploded diagram web application (running locally at `http://localhost:5173/` on the branch `task/interactive-exploded-diagram`) to display the complete Amplified Partners Process Stack (L0 through L4) on a 30-60 degree isometric layout.
    *   *30-60 Axis:* 30 degrees is the horizontal axis, and 60 degrees is the front-to-back lift.

### 2. Logic & Constraints
*   **Pyramid Integrity (Taguchi adaptation):** No piece of the base can be bypassed or disrespected; every part of the validation gate must perform strictly to keep the pinnacle sharp.

### 3. Formulas & Operational Metrics
*   **Isometric Layout angles:** 30 degrees (horizontal) and 60 degrees (front-to-back lift) for rendering the Process Stack.

### 4. Graph Updates & Concepts to Update
*   **Concept: Interactive Exploded Diagram (30-60 degree isometric layout).**
*   **Concept: Math vs. Logic (Database Environment Definition).**

### 5. Open Items
*   Transitioning to Session `3ed1b0b1-2c97-41c6-94de-b62385ec4a87` to execute deterministic checks and searches.

---

## chunk_06.txt

### 1. Conclusions & Agreements
*   **Prior Art Synthesis Milestone:** Saved raw searches and compiled a prior art synthesis document on the vision: **"Any resource that will be interpreted or used by AI is designed for AI."**
*   **Self-Policing Contradiction:** Proven mathematically that a single probabilistic LLM cannot safely audit itself because the same weights that produced an error are used to judge it. Verification requires external, deterministic inputs.
*   **Deterministic Checks Harness (`agentic_checks.py`):** Deployed a verification tool exposing discrete pathways (CLI flags) that agents can call programmatically:
    *   `--git`: Enforces branch isolation and worktree checks (No Worktree, No Work).
    *   `--db`: Verifies extensions (`age`, `vector`) and Apache AGE graph presence (`business_brain`).
    *   `--vector`: Verifies vector dimension matching (asserting 384 dimensions for the local sandbox).
    *   `--vibe`: Intercepts and fails loud on unverified subjective self-ratings (banning confidence scores based on "vibes").
*   **Enabling Constraints:** Gating boundaries (worktrees, database taxonomy targets) remove hesitation and narrow search spaces, focusing intelligence on valid pathways.
*   **Optimal Solution / Correction Burden:** Active symbolic pathways (exposing hooks as AI tools) are optimal because they prevent silent failures, but they risk an **Infinite Correction Loop**. To prevent this, we must enforce:
    1.  *AI-Native Error Diagnostics:* Harnesses must return structured JSON specifying the exact violation, coordinates, and mathematical difference (not just a binary "FAIL").
    2.  *Backoff/Decay Limits:* Pontryagin-style stop control. If a hook fails more than $N$ times (typically 3), the agent halts, archives state, and escalates to Linear. Undone is a valid state.

### 2. Logic & Constraints
*   **No Worktree, No Work:** The agent must never write code or execute mutations in an unconfigured, dirty, or untracked branch. Every task must begin by setting up a dedicated git branch or worktree.
*   **No Vibe Constraint:** Hard block on arbitrary confidence scores. Values like `1.0` or subjective self-ratings without programmatic proof fail the validation check immediately.

### 3. Formulas & Operational Metrics
*   **Vector dimension check constraint:** Exactly 384 dimensions.
*   **Backoff failure limit:** $N = 3$ fails on a single hook triggers execution halt and escalation.
*   **Local Python env path:** `/Users/ewansair/ingestion-to-research-pipe/clean-build/02_build/scripts/.venv/bin/python`.
*   **Active Git Worktree:** `task/deterministic-checks-search` under `/Users/ewansair/ingestion-to-research-pipe/.worktrees/antigravity-deterministic-checks`.

### 4. Graph Updates & Concepts to Update
*   **Concept: Self-Policing Contradiction.**
*   **Concept: Correction Burden & Infinite Correction Loop.**
*   **Concept: Enabling Constraints.**
*   **Component: agentic_checks.py Harness.**

### 5. Open Items
*   The governed worker (`temporal/workers/governed_main.py`) is defined but not active or registered in the Docker-compose worker stacks on Beast.
*   Connecting the agentic checks harness as a pre-execution hook in automated Temporal pipeline runs.

---

## chunk_07.txt

### 1. Conclusions & Agreements
*   **Python/Rust Partnership Metaphor:**
    *   *Python (The Agent):* Flexible, rapid, probabilistic, and creative. Dyn-typed, prone to runtime errors/hallucinations.
    *   *Rust (The Harness):* Strict, zero-compromise, compiler-enforced. Zero guessing; acts as borrow-checker/schema guard.
*   **Nested Gate Pipeline (Escape Room Maze):**
    *   Progress is a sequence of structured passes. Passing one gate unlocks the pathway to the next harness (e.g. term alignment -> isolated worktree -> schema validation -> ledger commitment).
    *   The deterministic harness is the **triangular hole** that the fluid intelligence of the AI must shape itself to fit before it can slip through and proceed.
    *   An error at any stage halts the pipeline immediately, preventing downstream contamination. Every final state is 100% correct, signed, and witnessed.
*   **Definition of "Job Done" vs "Merged":**
    *   "Job done" means dropping code in the repository and waiting for/answering comments.
    *   It does **not** mean merged. Merging requires a full audit before merge by a specialized agent that will fix any issues.
*   **Committed Assets:** Pushed to local branch `task/deterministic-checks-search`:
    *   Harness Tool: `perplexity-inbox/harness/agentic_checks.py`
    *   Raw Search Data: `perplexity-inbox/raw_searches/checks-and-measures-using-deterministic__2026-06-30.json`
    *   Synthesis Markdown: `perplexity-inbox/raw_searches/synthesis__deterministic_agent_validation__2026-06-30.md`

### 2. Logic & Constraints
*   **Zero Negotiation:** The AI cannot negotiate with or hack the deterministic gate. Conformance is binary.
*   **Pre-commit Gate:** Automatically executes verification layers on `git commit`, verifying if read is Tier A and citation fetch is Tier A.

### 3. Formulas & Operational Metrics
*   **Baton Epistemic Grade:** set to `PROVEN`.
*   **Database Port:** `postgresql://cove:lTJhzWncfPNVCAomIFtkyVoxPrIENLtE@127.0.0.1:5433/cove`.

### 4. Graph Updates & Concepts to Update
*   **Concept: Python/Rust Partnership.**
*   **Concept: Nested Gate Pipeline / Escape Room Maze.**
*   **Concept: Job Done vs Merged.**

### 5. Open Items
*   Execution of the background internet searches against the 6 points in the session baton.

---

## chunk_08.txt

### 1. Conclusions & Agreements
*   **SearXNG Network Port Issue:** The SearXNG container on Beast (port 8080) has no host port binding (`8080/tcp: null`), making it unreachable from the host or Tailscale. It is only reachable from inside the Docker network on Beast.
*   **Resolution:** Executed searches via an SSH tunnel / Docker network execution syntax: `ssh beast 'curl -s "http://searxng:8080/search?..."'`.
*   **Parallel Search Results (The Baton Audit):**
    *   *Point 1 — pgvector + Apache AGE coexisting in PostgreSQL:* Active and well-documented multi-model database design for hybrid GraphRAG. Microsoft published a guide on combining pgvector and Apache AGE for knowledge graphs. Benchmarks exist to avoid multi-database synchronization tax.
    *   *Point 2 — Deterministic validation checks:* Verified by the March 2026 paper "Schema-Gated Agentic AI for Reproducible Scientific Work" and n8n community practices ("Deterministic workflows break loud, agentic fail quietly"). Schema becomes a mandatory execution boundary.
    *   *Point 3 — XML prompting annotations:* Mainstream delimiter. Wrapping variables in XML tags is recommended by Anthropic, OpenAI, and Google to prevent context drift. Slicing streaming outputs favors XML under token pressure.
    *   *Point 4 — Self-policing contradiction:* Confirmed by the paper "The Self-Correction Illusion: LLM Agents Struggle to Self-Correct" (arXiv:2310.01798). Decoupling validation into external guardrail layers (e.g. Invariant Labs Guardrails) at the system/MCP level is the recommended path.
    *   *Point 5 — Temporal.io pre-flight hooks:* Temporal lacks a native "pre-flight hook" primitive. The standard pattern is using Temporal Interceptors or wrapping the check inside a first Activity as a gate.
    *   *Point 6 — Governed worker:* No native OSS concept. Registrations are done by starting the worker process and pointing it at the task queue. The compose file requires a service entry running `governed_main.py` with the correct env vars.

### 2. Logic & Constraints
*   **The Self-Correction Illusion:** LLMs cannot reliably self-correct because the same weights that produced the error are used to judge it. An external, deterministic gate is a logical necessity.

### 3. Formulas & Operational Metrics
*   **SearXNG internal URL:** `http://searxng:8080/search?`.
*   **PostgreSQL Internal Port:** 5432 / External Tunnel Port: 5433.

### 4. Graph Updates & Concepts to Update
*   **Concept: The Self-Correction Illusion.**
*   **Concept: Coexistence of Apache AGE and pgvector in PostgreSQL.**

### 5. Open Items
*   Registering the governed worker `governed_main.py` in the Docker-compose worker stacks on Beast.

---

## chunk_09.txt

### 1. Conclusions & Agreements
*   **Decoupled Metadata Taxonomy (Brackets keeping):** User approved keeping prior taxonomy names in brackets `[cove]`, `[Beast]`, `[PUDDING]` for readability, alongside an explicit HTML comment instructing parsing AIs to ignore them.
*   **Watertight Gating Pipeline:**
    ```
    [Temporal Execution Hook] 
           │
           ▼
    [Deterministic Harness (agentic_checks.py)] 
      - Runs code in sandboxed transaction rollback.
      - Computes semantic entropy and conformal set size.
           │
           ▼
    [Vellum Write Request (gate.py)]
      - Carries: semantic_entropy, conformal_set_size, sandbox_verified
      - Rejects write at the API boundary if constraints are violated.
    ```

### 2. Logic & Constraints
*   **API Boundary Constraints:** Vellum write gate (`gate.py`) rejects write requests at the API boundary if statistical constraints (semantic entropy and conformal set size) are violated or if sandboxing is not verified.

### 3. Formulas & Operational Metrics
*   **Gating parameters:** `semantic_entropy` and `conformal_set_size` computed by the harness and carried to the write request.

### 4. Graph Updates & Concepts to Update
*   **Concept: Watertight Gating Pipeline.**
*   **Component: Vellum Write Gate (`gate.py`).**
*   **Component: agentic_checks.py.**

### 5. Open Items
*   Register the governed worker (`temporal/workers/governed_main.py`) in the Docker-compose worker stacks on Beast.

---

## chunk_10.txt

### 1. Conclusions & Agreements
*   **Sandbox Transaction Hook:** The database sandbox transaction check in `agentic_checks.py` provides the exact proof (`sandbox_verified = True`) required by Vellum to authorize writing results to the semantic graph database `[amplified_brain]`.
*   **Role of `[cove]`:** strictly the **deterministic orchestrator metadata and telemetry store**. It holds task logs, run histories, schedules, base system prompts, and Kaizen patches (how the machines execute).
*   **Role of `[amplified_brain]` and filesystem:** hold the actual **semantic intelligence, graph connections, and client knowledge**.
*   **Separation of Concerns:**
    *   `[cove]` = **Deterministic Control & Execution State** (The outer sandwich buns)
    *   `[amplified_brain]` = **AI Semantic Memory & Reasoning Knowledge** (The probabilistic meat)
*   **Unified Operational Record (Write-to-Vellum & GitHub):** Every fleet agent (Claude, Cursor, Antigravity) must submit all runtime actions, file changes, and environment updates to both **GitHub** (via commits/pushes) and **Vellum** (via hash-chained entries on the correspondence ledger).
*   **Deterministic Compiler Hook ("What's What"):**
    *   The master directory map **`ESTATE-TAXONOMY.md`** is strictly **read-only** for executing agents.
    *   The deterministic Python/Rust plumbing running on the backend automatically parses incoming Vellum ledger entries, extracts structural coordinates (paths, container ports, databases, schema changes), and compiles them to overwrite `ESTATE-TAXONOMY.md`.
    *   When an agent initializes, it reads the read-only `ESTATE-TAXONOMY.md` to get an immediate, guaranteed correct map of the estate.
*   **Spine Size Law:** `AGENTS.md` must be kept at a perfect, readable size and MUST never exceed 500 lines. If it approaches 500 lines, migrate verbose details, environment context, and logs to `ESTATE-NOTES.md` (or portable spine reference directories).

### 2. Logic & Constraints
*   **Reference Synchronization Law (Session Close):** Every session MUST conclude by checking and updating the canonical estate maps. Direct editing of `ESTATE-TAXONOMY.md` is forbidden for executing agents; updates are compiled automatically by Vellum's deterministic Python/Rust plumbing.
*   **Semantic Entropy Gate:** High semantic entropy ($\ge 0.4$) during a Best-of-N reasoning loop triggers a hard block at the write gate, preventing the agent from committing contaminated knowledge.
*   **Spine size gate:** Hard ceiling of 500 lines for `AGENTS.md` (currently 82 lines).

### 3. Formulas & Operational Metrics
*   **Mathematical Gating Metrics:**
    *   *Taguchi Loss Function adaptation:* Bounding LLM response embedding deviations from target centroids ($L(y) = k(y - T)^2$).
    *   *Cosine Dispersion ($D_R$):* Bounding context similarity variance.
    *   *Semantic Entropy ($H_s$):* Measuring consensus over generation distributions (threshold: $H_s < 0.4$ required to pass write gate).
    *   *Conformal Prediction Sets:* Statistically bounding output uncertainty (threshold: set size $\le 2$ required to pass write gate).
    *   *Best-of-N reasoning loop:* $N = 16$.
    *   *Spine limit:* 500 lines.

### 4. Graph Updates & Concepts to Update
*   **Concept: Spine Size Law.**
*   **Concept: Unified Operational Record.**
*   **Concept: Separated Database roles (cove = execution control, amplified_brain = semantic memory).**
*   **Concept: Read-Only Estate Map (`ESTATE-TAXONOMY.md`).**
*   **Skill Registered:** `amplified-mathematical-validator` created and registered at `file:///Users/ewansair/.gemini/config/skills/amplified-mathematical-validator/SKILL.md`.
*   **Rules files updated:** `AGENTS.md` (lines 82) and `ESTATE-TAXONOMY.md`.

### 5. Open Items
*   The governed worker (`temporal/workers/governed_main.py`) needs to be registered in the Docker-compose worker stacks on Beast to activate the safety gate execution hooks.
