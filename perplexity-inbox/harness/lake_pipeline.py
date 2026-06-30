#!/usr/bin/env python3
"""APQS Sandbox Intelligence Lake Pipeline.

Manages a local DuckDB-based sandbox database representing the data lake
relationship. Slices documents, tracks version lineage, maps chunks
to first-principles reasoning primitives, and groups them into clusters.
"""
import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import duckdb

HARNESS_DIR = Path(__file__).resolve().parent
ROOT_DIR = HARNESS_DIR.parent
DB_DIR = ROOT_DIR / "perplexity-inbox" / "data"
DB_PATH = DB_DIR / "intelligence_lake.db"

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def get_db_connection() -> duckdb.DuckDBPyConnection:
    """Connects to the DuckDB intelligence lake database, creating parent dirs if needed."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))


def init_database() -> None:
    """Initializes the DuckDB schemas and populates the seed reasoning primitives."""
    conn = get_db_connection()
    try:
        # 1. Create Operational Data Lake tables
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id VARCHAR,
                title VARCHAR,
                source_path VARCHAR,
                hash VARCHAR,
                version INTEGER,
                parent_hash VARCHAR,
                created_at TIMESTAMP,
                status VARCHAR,
                PRIMARY KEY (id, version)
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id VARCHAR PRIMARY KEY,
                document_id VARCHAR,
                chunk_index INTEGER,
                content TEXT,
                tokens_count INTEGER,
                schema_code VARCHAR,
                epistemic_tier VARCHAR
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunk_clusters (
                chunk_id VARCHAR,
                cluster_id INTEGER,
                similarity_score DOUBLE
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS clusters (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                representative_dimensions TEXT
            );
        """)

        # 2. Create First-Principles Reasoning Primitives tables
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reasoning_primitives (
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
                category VARCHAR,
                description TEXT,
                governing_formula TEXT,
                rubrics TEXT
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunk_reasoning_links (
                chunk_id VARCHAR,
                primitive_id VARCHAR,
                confidence_score DOUBLE,
                PRIMARY KEY(chunk_id, primitive_id)
            );
        """)

        # 3. Seed Reasoning Primitives if empty
        res = conn.execute("SELECT COUNT(*) FROM reasoning_primitives;").fetchone()
        if res and res[0] == 0:
            seed_primitives = [
                (
                    "PRIM_PMI", "Pointwise Mutual Information", "mathematical",
                    "Measures semantic correlation and word association logic.",
                    "PMI(x;y) = log2(P(x,y) / (P(x)P(y)))",
                    "Analyze co-occurrence of dimensions across corpus. PMI >= 12.85 bits defines strong matching."
                ),
                (
                    "PRIM_JACCARD", "Jaccard Slot & Set Similarity", "mathematical",
                    "Calculates structural overlap between metadata slots and document sets.",
                    "J_slot = matching_slots / 4; J_set = |A intersection B| / |A union B|",
                    "Evaluate set intersection ratios. One-differing 4-vector must yield J_set = 0.60."
                ),
                (
                    "PRIM_PUDDING", "Pudding Candidate Score", "mathematical",
                    "Calculates cross-domain A-B-C semantic linking strength.",
                    "S = (DomainDist * PatternAlign) + GapComp + TensionBonus",
                    "Score candidate recipes. Thresholds: viable >= 13, high >= 18, exceptional >= 30."
                ),
                (
                    "PRIM_TAGUCHI", "Taguchi Quality Loss Function", "mathematical",
                    "Quantifies quality loss due to operational process deviations.",
                    "L(tau) = k_d * tau^2",
                    "Compute loss cost given target deviations. Constant k_d values: AI/ML=0.50, SMB=0.10, Maths=0.001."
                ),
                (
                    "PRIM_MARKOV", "Markov State Transition", "mathematical",
                    "Models sequential transition probabilities and failure/death spiral probabilities.",
                    "P = [Q R; 0 I], N = (I - Q)^-1, B = N * R",
                    "Map processes into absorbing state spaces. Compute death spiral probabilities."
                ),
                (
                    "PRIM_ALTMAN", "Altman Z-Score Financial Distress", "mathematical",
                    "Predicts corporate financial distress and cash flow death spirals.",
                    "Z = 6.56X1 + 3.26X2 + 6.72X3 + 1.05X4",
                    "Apply financial ratio metrics. Safe zone: Z > 2.6, Distress zone: Z < 1.1."
                ),
                (
                    "PRIM_REVERSE_PUDDING", "Reverse-Pudding Risk Duality", "mathematical",
                    "Tracks superadditive risk interactions and cascading process failures.",
                    "Delta_- = -Delta_+; eta_ij = R(i,j) - R(i,0) - R(0,j) + R(0,0)",
                    "Identify compounding failures where interaction term eta_ij > 0."
                ),
                (
                    "PRIM_CAUSAL", "Causal Chaining", "logical",
                    "Resolves root cause paths and dependent system loops.",
                    "A -> B -> C (Transitive dependence)",
                    "Map transitive dependencies and process chains. Identify reinforcement loops."
                ),
                (
                    "PRIM_FRICTION", "Psychological Friction Mapping", "psychological",
                    "Measures customer resistance, operational drag, and complexity thresholds.",
                    "Friction = sum(weights * occurrences)",
                    "Scan documents for indicators of friction, delays, or process complexity."
                ),
                (
                    "PRIM_TRUST", "Trust Alignment", "psychological",
                    "Tracks credibility, benevolence, and capability markers.",
                    "Trust = Credibility + Benevolence + Capability",
                    "Extract trust indicators. Ensure marketing statements do not contain deceptive triggers."
                ),
                (
                    "PRIM_DECAY", "Temporal Relevance Decay", "mathematical",
                    "Decays the relevance score of older observation chunks over time.",
                    "R(t) = e^(-lambda * t)",
                    "Apply exponential decay. Half-life t_1/2 = 0.693 / lambda. Re-run analysis at 0.357 / lambda."
                )
            ]
            conn.executemany(
                "INSERT INTO reasoning_primitives VALUES (?, ?, ?, ?, ?, ?);",
                seed_primitives
            )
            print(f"[DATABASE] Initialized and seeded {len(seed_primitives)} reasoning primitives.")
    finally:
        conn.close()


def chunk_text(text: str, chunk_size: int = 300) -> List[str]:
    """Splits a document text into line-based segments."""
    lines = text.splitlines()
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk_content = "\n".join(lines[i:i + chunk_size])
        if chunk_content.strip():
            chunks.append(chunk_content)
    return chunks


def match_reasoning_primitives(content: str, semantic_dimensions: List[str]) -> List[Tuple[str, float]]:
    """Determines which reasoning primitives apply to a chunk based on keywords and dimensions."""
    matched = []
    content_lower = content.lower()
    dimensions_lower = [d.lower() for d in semantic_dimensions]

    # Rule-based mapping of keywords/dimensions to primitive IDs
    mappings = {
        "PRIM_PMI": ["pmi", "mutual information", "correlation"],
        "PRIM_JACCARD": ["jaccard", "similarity", "slot matching", "overlap"],
        "PRIM_PUDDING": ["pudding", "lbd", "swanson", "abc model", "recipe"],
        "PRIM_TAGUCHI": ["taguchi", "loss function", "deviation", "variance"],
        "PRIM_MARKOV": ["markov", "transition", "state chain", "absorbing"],
        "PRIM_ALTMAN": ["altman", "z-score", "bankruptcy", "distress"],
        "PRIM_REVERSE_PUDDING": ["reverse-pudding", "risk duality", "cascade", "failure interaction"],
        "PRIM_CAUSAL": ["causal", "cause-effect", "dependency", "depends_on", "root cause"],
        "PRIM_FRICTION": ["friction", "resistance", "complexity", "drag", "delay"],
        "PRIM_TRUST": ["trust", "credibility", "benevolence", "capability"],
        "PRIM_DECAY": ["decay", "relevance decay", "half-life", "lambda", "temporal decay"]
    }

    for prim_id, keywords in mappings.items():
        score = 0.0
        # Check semantic dimensions match (highest relevance)
        for dim in dimensions_lower:
            if any(k in dim for k in keywords):
                score += 0.6
        # Check text body matches
        for kw in keywords:
            if kw in content_lower:
                score += 0.3
        
        # Cap score at 1.0 and save if significant
        if score > 0.0:
            matched.append((prim_id, min(1.0, score)))

    # Fallback to Causal if no other matched
    if not matched:
        matched.append(("PRIM_CAUSAL", 0.5))

    return matched


def cluster_chunk(conn: duckdb.DuckDBPyConnection, chunk_id: str, semantic_dimensions: List[str]) -> int:
    """Clusters a chunk by looking for existing clusters sharing dimensions via Jaccard similarity."""
    if not semantic_dimensions:
        return 0  # Default unclustered group

    # Get existing clusters
    res = conn.execute("SELECT id, name, representative_dimensions FROM clusters;").fetchall()
    
    best_cluster_id = None
    best_score = 0.0

    set_a = set(semantic_dimensions)
    for c_id, name, rep_dims_str in res:
        try:
            rep_dims = set(json.loads(rep_dims_str))
        except Exception:
            continue
        
        # Calculate Jaccard Set Similarity
        union = set_a.union(rep_dims)
        j_score = len(set_a.intersection(rep_dims)) / len(union) if union else 0.0
        if j_score > best_score and j_score >= 0.25:  # threshold of 25% overlap
            best_score = j_score
            best_cluster_id = c_id

    # If matching cluster found, associate it
    if best_cluster_id is not None:
        conn.execute(
            "INSERT INTO chunk_clusters VALUES (?, ?, ?);",
            (chunk_id, best_cluster_id, best_score)
        )
        return best_cluster_id
    else:
        # Create a new cluster
        new_id = len(res) + 1
        new_name = f"Cluster_{new_id}_{list(set_a)[0] if set_a else 'unassigned'}"
        conn.execute(
            "INSERT INTO clusters VALUES (?, ?, ?);",
            (new_id, new_name, json.dumps(list(set_a)))
        )
        conn.execute(
            "INSERT INTO chunk_clusters VALUES (?, ?, ?);",
            (chunk_id, new_id, 1.0)
        )
        return new_id


def ingest_document(file_path: Path) -> str:
    """Processes a document file, chunking, labeling, clustering, and versioning it."""
    init_database()
    content = file_path.read_text(encoding="utf-8")
    
    # 1. Parse frontmatter
    from glasses_loader import extract_yaml_frontmatter
    fm, body = extract_yaml_frontmatter(content)
    if not fm:
        fm = {}
        body = content

    title = fm.get("title", file_path.stem)
    schema_code = fm.get("schema_code", "none")
    epistemic_tier = fm.get("epistemic_tier", fm.get("epistemic_grade", "INTUITED"))
    dimensions = fm.get("semantic_dimensions") or fm.get("dimensions") or []

    # Calculate body hash to verify versioning
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    doc_id = fm.get("id", f"DOC_{hashlib.sha256(str(file_path).encode('utf-8')).hexdigest()[:8]}")

    conn = get_db_connection()
    try:
        # 2. Version Lineage Check
        res = conn.execute(
            "SELECT version, hash FROM documents WHERE id = ? ORDER BY version DESC LIMIT 1;",
            (doc_id,)
        ).fetchone()

        if res:
            old_version, old_hash = res
            if old_hash == body_hash:
                return f"Document '{title}' already processed and unchanged (v{old_version})."
            
            # Hash changed, create a new version record
            new_version = old_version + 1
            parent_hash = old_hash
            print(f"[PIPELINE] Document '{title}' modified. Incrementing version to v{new_version}.")
        else:
            new_version = 1
            parent_hash = "none"
            print(f"[PIPELINE] Document '{title}' is new. Version set to v1.")

        # Insert document record
        conn.execute(
            "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            (doc_id, title, str(file_path), body_hash, new_version, parent_hash, datetime.now(), "active")
        )

        # Remove previous version's chunks and links if they exist to keep only the active version queried
        conn.execute("DELETE FROM chunk_reasoning_links WHERE chunk_id IN (SELECT id FROM chunks WHERE document_id = ?);", (doc_id,))
        conn.execute("DELETE FROM chunk_clusters WHERE chunk_id IN (SELECT id FROM chunks WHERE document_id = ?);", (doc_id,))
        conn.execute("DELETE FROM chunks WHERE document_id = ?;", (doc_id,))

        # 3. Chunking & Ingestion
        text_chunks = chunk_text(body, chunk_size=300)
        for idx, chunk_content in enumerate(text_chunks, 1):
            chunk_id = f"{doc_id}_chunk_{idx:02d}"
            tokens_est = len(chunk_content.split())  # simple word count estimate
            
            conn.execute(
                "INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?);",
                (chunk_id, doc_id, idx, chunk_content, tokens_est, schema_code, epistemic_tier)
            )

            # 4. Map Reasoning Primitives (Logic)
            prim_matches = match_reasoning_primitives(chunk_content, dimensions)
            for prim_id, confidence in prim_matches:
                conn.execute(
                    "INSERT INTO chunk_reasoning_links VALUES (?, ?, ?);",
                    (chunk_id, prim_id, confidence)
                )

            # 5. Cluster (Topology)
            cluster_chunk(conn, chunk_id, dimensions)

        return f"Successfully ingested '{title}' (v{new_version}) into Sandbox Intelligence Lake."
    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if path.exists():
            res_str = ingest_document(path)
            print(res_str)
        else:
            print(f"File not found: {path}")
            sys.exit(1)
    else:
        # Dry run db init
        init_database()
        print("Sandbox Intelligence Lake initialized.")
