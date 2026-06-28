# Architectural Spec: AI-Native Data Organization (AgentFS)

This document defines the **Dual-YAML Metadata Framework** and the canonical **19-field AI-Facing Schema** designed to eliminate naming ambiguity and enable deterministic multi-agent retrieval.

---

## 1. Executive Summary: The Dual-YAML Paradigm

To allow humans and AI agents to work together without friction, metadata is divided into two distinct scopes:
1.  **Tier 1: Presentation & Display YAML (Human-Facing):** Simple, scannable fields used by UI dashboards, file managers, and exporters to represent title, category, tags, and summaries.
2.  **Tier 2: AI-Understanding & Logic YAML (AI-Facing):** Strict, high-density 19-field metadata that acts as the "Sovereign Seal". The AI uses this to calculate line-range coordinates, verify signatures, assert OPA boundaries, and link entity nodes in the database.

---

## 2. Directory Hierarchy & Folder Naming Rules

```
/inbox/                  <-- Entry point (raw drops)
/archive/                <-- Vault of processed inputs
/chunks/                 <-- Token-boundary slices (max 300 lines)
/brain/                  <-- Semantic Graph Directory
  ├── /entities/         <-- Entity definitions named by UUID5
  ├── /relationships/    <-- Ontological directories mapping graph edges
  └── /logic_packets/    <-- Markdown files containing rules and doctrines
```

---

## 3. The 19-Field AI-Facing YAML Specification

Every chunked file and logic packet must feature these 19 standardized metadata fields in its Tier 2 YAML header. The AI parses these fields programmatically to map targets and verify integrity:

```yaml
---
# Block A: Document Identity & Metadata
1. title: "[Chunk Subject]"
2. date: "YYYY-MM-DD"
3. document_type: "research_chunk | logic_capsule | ruleset"
4. epistemic_tier: "INTUITED | STRUCTURED | MEASURED | PROVEN"

# Block B: Attribution & Provenance
5. origin_type: "agent_synthesis | human_entry | prompt_run"
6. author: "[Seat ID / Actor e.g. antigravity, ewan]"
7. source_file: "[Filename of origin]"

# Block C: Structural Coordinates
8. chunk_index: N
9. total_chunks: M
10. start_line: X
11. end_line: Y

# Block D: Hashes & Cryptographic Verification
12. file_hash_sha256: "[SHA-256 hash of original file]"
13. chunk_hash_sha256: "[SHA-256 hash of this chunk's text content]"
14. signature: "[Ed25519 or SHA cryptographic witness seal]"

# Block E: Domain & Security Context
15. client_scope: "[Client identifier e.g. amplified-partners]"
16. project_scope: "[Project name or UUID]"
17. domain: "[Subject category e.g. health, machine-learning]"
18. pii_class: "none | tokenised | contains_pii"
19. parent_nodes: ["UUID-parent-1", "UUID-parent-2"]
---
```

---

## 4. Symlinked Knowledge Graphs (Logical Relationships)

Symlinks represent ontological connections (graph edges) between files without duplicating the files physically on disk. 

```
/brain/entities/company_A/
  ├── info.md                  (Physical file)
  └── related_deals/
        ├── deal_01.md -> /brain/deals/deal_01/info.md   (Symlink)
        └── deal_02.md -> /brain/deals/deal_02/info.md   (Symlink)
```

AIs walk directories using tools like `ls -l` to resolve graph relationships natively.

---

## 5. Ingestion Pipeline Recommendations

*   **Enforce Schema:** The `inbox_watcher.py` must populate all 19 fields during chunking, automatically computing line counts, hashes, and scopes.
*   **Vector Sidecars:** Embeddings should be generated and stored in a sidecar file (`.vector`) next to the text chunk to enable hybrid retrieval (Tier 1 filesystem grep + Tier 2 vector similarity).

---

## 6. The Assertion-Context Boundary (Database vs. Filesystem)

To prevent database pollution and AI retrieval confusion, a strict boundary is enforced:

1. **The AI Database (Graph/Vector):** Stores *only* atomic assertions (proven facts, active hypotheses, entities) and their logical relationships. No conversational filler, raw transcripts, or body text is stored in database records. Every node contains a pointer back to its filesystem provenance.
2. **The Local Filesystem (Ground Truth WAL):** Stores the raw, complete context (text chunks) under `/chunks/` with their 19-field headers.
3. **Execution Loop (De-referencing):**
   * The AI searches the database to find the logical connections and coordinates.
   * The AI uses those coordinates to read the raw filesystem chunks directly when it needs deep text context for synthesis or execution.


## 7. The Anonymous Database Firewall & Ingestion Validation Loop

To ensure absolute safety, database credentials and configurations are firewalled from executing AI agents:

1. **Anonymous DB Rule:** Executing AI agents have no direct access to write database endpoints or connection credentials. The database is anonymous to the agent.
2. **Single Entrance (The Ingestion Pipe):** The *only* way for any agent, script, or external system to save or update knowledge is by dropping files into `/inbox/`.
3. **The Ingestion Gate Validation Loop:** Before any file is chunked and written, the Ingestion Pipe enforces two validation checks:
   * **Domain Neutralization & Web Audit:** The pipeline translates domain-specific jargon into generalized terms (de-siloing) and queries external search engines (SearXNG/Google) to verify empirical validity and prior art. If no external basis exists, it is flagged as an unverified hypothesis.
   * **Logical Consistency Check (Contradiction Detector):** The pipeline checks the assertions against the existing corpus to detect factual, logical, temporal, or attribution contradictions.
   * **Epistemic Classification (No Destruction):** If a claim fails the web audit or consistency check, it is **never deleted or discarded** (unless it is a direct logical impossibility like 5+5=13). Instead, the raw document goes directly to the Data Lake, and its index node is saved with a lower epistemic grade (e.g. `HYPOTHESIS` or `INTUITED`), preventing it from polluting operational actions while preserving it for future pattern matching.

---

## 8. Non-Destructive Ingestion & The Data Lake

To preserve all incoming data and allow future patterns to emerge over time:

1. **The Data Lake (S3/Filesystem Archive):** All incoming research documents, raw transcript briefs, and data drops are stored immutably in the `/archive/` directory (and MinIO S3 bucket on Beast). Nothing is deleted unless it is a fatal logic error (e.g. 5+5=13).
2. **Classification over Exclusion:** The ingestion gate acts as a classifier, sorting inputs into two tiers:
   * **Active Operational Graph (PROVEN/STRUCTURED):** Clean assertions that have passed the web audit and contradiction gates. Active agents default to querying this layer for logic and execution.
   * **Hypothesis Pool (INTUITED/HYPOTHESIS):** Unverified claims, raw insights, or temporal contradictions. These are stored and indexed to allow future pattern emergence, but are isolated from the active reasoning loops of production agents.
