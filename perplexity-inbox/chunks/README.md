# Chunks Directory - AI-Native Structured Data Lake

This directory is a structured filesystem database designed for direct, high-performance traversal and query by Sovereign AI agents and human architects. 

---

## 1. Directory Structure & Taxonomy

Instead of a flat folder, chunks are organized into subdirectories by their **epistemic category** to optimize context scoping. Each document has its own directory containing the text chunks, vector caches, and a document-level metadata map:

```
/chunks/{category}/{doc_clean_name}/
  ├── chunk_01.txt       <- Text content with YAML frontmatter header
  ├── chunk_01.vector    <- Float array vector embedding (JSON format)
  ├── chunk_02.txt
  ├── chunk_02.vector
  └── metadata.json      <- Document-level metadata map (original name, hash, timestamp)
```

### Categorization System
*   `doctrine/` - Inviolable system laws, fundamental rods, and absolute principles.
*   `rules/` - Operating rules, IDE configurations, and fleet-wide behavioral settings.
*   `decisions/` - Settled architectural decisions and thread-level conclusions.
*   `briefs/` - Daily briefs, Gmail notifications, and status summaries.
*   `research/` - Research findings, academic papers, SearXNG summaries, and proven methodologies.
*   `batons/` - Handoff batons between agent sessions.
*   `coordination/` - Shared session starts and multi-agent coordination records.
*   `general/` - Fallback for unclassified files.

---

## 2. In-File Epistemic Signals (YAML Header)

Every chunk text file (`.txt`) begins with a structured YAML frontmatter block that defines its context and authority:

```yaml
---
title: "Chunk 1 of DOCTRINE__rods.md"
date: "2026-06-28"
document_type: "doctrine"
epistemic_grade: "DOCTRINE"
canonical_path: "/chunks/doctrine/DOCTRINE__rods/chunk_01.txt"
chunk_index: 1
total_chunks: 1
---
```

---

## 3. macOS Spotlight & `mdfind` Query Patterns

On macOS, files in this directory are natively indexed by Spotlight. The watcher writes structured tags straight to the APFS filesystem Extended Attributes under the `com.apple.metadata:` namespace.

### CLI Search Examples for AI Agents
Use the `mdfind` command to locate files with sub-millisecond latency without needing a database connection:

*   **Search for all Doctrine chunks:**
    ```bash
    mdfind -onlyin ./ "kMDItemKeywords == 'doctrine'"
    ```

*   **Search for Research chunks containing the keyword "Goldratt":**
    ```bash
    mdfind -onlyin ./ "kMDItemKeywords == 'research' && kMDItemTextContent == 'Goldratt'"
    ```

*   **Query by description/title:**
    ```bash
    mdfind -onlyin ./ "kMDItemDescription == 'Uncovering the Murky Middle'"
    ```

---

## 4. Platform-Agnostic Interface

For environments running Linux (like the Beast server) where Spotlight is unavailable, use the unified `search_chunks.py` gateway script. It mimics the Spotlight interface by walking the directories, parsing `metadata.json` files, and caching them in a local SQLite index for matching performance.
