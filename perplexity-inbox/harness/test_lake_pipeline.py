#!/usr/bin/env python3
"""Test harness for lake_pipeline.py.

Asserts schema initialization, document ingestion, chunking,
labeling against primitives, Jaccard clustering, and version lineage.
"""
import os
import sys
import unittest
import shutil
import json
from pathlib import Path
import duckdb

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.append(str(HARNESS_DIR))

# Force database path override for testing
os.environ["AMPLIFIED_INBOX"] = str(HARNESS_DIR.parent)
import lake_pipeline


class TestLakePipeline(unittest.TestCase):

    def setUp(self):
        # Use a temporary testing DB file name
        self.original_db_path = lake_pipeline.DB_PATH
        self.test_db_dir = HARNESS_DIR / "test_data"
        self.test_db_dir.mkdir(parents=True, exist_ok=True)
        self.test_db_path = self.test_db_dir / "test_intelligence_lake.db"
        lake_pipeline.DB_PATH = self.test_db_path

        # Clear any existing test database
        if self.test_db_path.exists():
            os.remove(self.test_db_path)

        # Initialize the database schema and seeds
        lake_pipeline.init_database()

    def tearDown(self):
        # Restore original DB path
        lake_pipeline.DB_PATH = self.original_db_path
        # Clean up test directory
        if self.test_db_dir.exists():
            shutil.rmtree(self.test_db_dir)

    def test_database_initialization(self):
        conn = duckdb.connect(str(self.test_db_path))
        try:
            # Assert all tables exist
            tables = [r[0] for r in conn.execute("SHOW TABLES;").fetchall()]
            for t in ["documents", "chunks", "reasoning_primitives", "chunk_reasoning_links", "clusters", "chunk_clusters"]:
                self.assertIn(t, tables)

            # Assert reasoning primitives are seeded
            count = conn.execute("SELECT COUNT(*) FROM reasoning_primitives;").fetchone()[0]
            self.assertEqual(count, 11)

            # Check a specific seeded primitive (e.g. JACCARD)
            res = conn.execute("SELECT name, category FROM reasoning_primitives WHERE id = 'PRIM_JACCARD';").fetchone()
            self.assertEqual(res[0], "Jaccard Slot & Set Similarity")
            self.assertEqual(res[1], "mathematical")
        finally:
            conn.close()

    def test_document_ingestion_and_versioning(self):
        # Create a mock document file
        doc_path = self.test_db_dir / "mock_doc.txt"
        
        # Version 1 Content
        v1_content = """---
schema_code: PUDDING_V1
id: DOC_TEST_VERSIONING
title: "First Principles Versioning Test"
document_type: principle
expert: CLAUDE
domain: systems
semantic_dimensions:
  - trust
  - cause_effect
actionable: principle_only
status: hypothesis
created_at: "2026-06-30"
last_validated: "2026-06-30"
lbd_attribution: "Swanson (1986) ABC Model"
epistemic_tier: INTUITED
provenance_sources: []
author: ewan
bridge_candidates: []
resolved_connections: []
risk_flags: []
canonical_summary: "First version of the mock document."
---
This is the body of version 1. It contains discussion of trust and cause-effect chains.
"""
        doc_path.write_text(v1_content, encoding="utf-8")

        # Ingest Version 1
        res = lake_pipeline.ingest_document(doc_path)
        self.assertIn("v1", res)

        conn = duckdb.connect(str(self.test_db_path))
        try:
            # Query documents
            doc_rec = conn.execute("SELECT title, version, parent_hash FROM documents WHERE id = 'DOC_TEST_VERSIONING';").fetchone()
            self.assertEqual(doc_rec[0], "First Principles Versioning Test")
            self.assertEqual(doc_rec[1], 1)
            self.assertEqual(doc_rec[2], "none")

            # Query chunks
            chunk_rec = conn.execute("SELECT content, schema_code, epistemic_tier FROM chunks WHERE document_id = 'DOC_TEST_VERSIONING';").fetchall()
            self.assertEqual(len(chunk_rec), 1)
            self.assertEqual(chunk_rec[0][1], "PUDDING_V1")
            self.assertEqual(chunk_rec[0][2], "INTUITED")

            # Query reasoning primitive mapping links (should link to PRIM_TRUST and PRIM_CAUSAL)
            links = [r[0] for r in conn.execute("SELECT primitive_id FROM chunk_reasoning_links WHERE chunk_id = 'DOC_TEST_VERSIONING_chunk_01';").fetchall()]
            self.assertIn("PRIM_TRUST", links)
            self.assertIn("PRIM_CAUSAL", links)

        finally:
            conn.close()

        # Ingest Version 2 (modified text content)
        v2_content = v1_content.replace(
            "This is the body of version 1.",
            "This is the body of version 2. Modified text parameters."
        )
        doc_path.write_text(v2_content, encoding="utf-8")

        res_v2 = lake_pipeline.ingest_document(doc_path)
        self.assertIn("v2", res_v2)

        conn = duckdb.connect(str(self.test_db_path))
        try:
            # Query documents - should have two records in chronological order
            doc_recs = conn.execute("SELECT version, parent_hash FROM documents WHERE id = 'DOC_TEST_VERSIONING' ORDER BY version ASC;").fetchall()
            self.assertEqual(len(doc_recs), 2)
            self.assertEqual(doc_recs[0][0], 1) # version 1
            self.assertEqual(doc_recs[1][0], 2) # version 2
            
            # Parent hash of version 2 must match hash of version 1
            v1_hash = conn.execute("SELECT hash FROM documents WHERE id = 'DOC_TEST_VERSIONING' AND version = 1;").fetchone()[0]
            self.assertEqual(doc_recs[1][1], v1_hash)

        finally:
            conn.close()

    def test_clustering_similarity(self):
        # Ingest doc 1 (expert: DALIO, dims: trust, people)
        doc1_path = self.test_db_dir / "dalio_doc.txt"
        doc1_content = """---
schema_code: PUDDING_V1
id: DOC_DALIO
title: "Dalio Trust"
document_type: principle
expert: DALIO
domain: systems
semantic_dimensions:
  - trust
  - people
actionable: principle_only
status: hypothesis
created_at: "2026-06-30"
last_validated: "2026-06-30"
lbd_attribution: "Swanson (1986) ABC Model"
epistemic_tier: INTUITED
provenance_sources: []
author: ewan
bridge_candidates: []
resolved_connections: []
risk_flags: []
canonical_summary: "Dalio trust."
---
Body text for trust and people.
"""
        doc1_path.write_text(doc1_content, encoding="utf-8")
        lake_pipeline.ingest_document(doc1_path)

        # Ingest doc 2 (expert: KENNEDY, dims: trust, communication)
        doc2_path = self.test_db_dir / "kennedy_doc.txt"
        doc2_content = doc1_content.replace("id: DOC_DALIO", "id: DOC_KENNEDY").replace("expert: DALIO", "expert: KENNEDY").replace("people", "communication").replace("Dalio Trust", "Kennedy Trust")
        doc2_path.write_text(doc2_content, encoding="utf-8")
        lake_pipeline.ingest_document(doc2_path)

        conn = duckdb.connect(str(self.test_db_path))
        try:
            # Query clusters
            clusters = conn.execute("SELECT id, name FROM clusters;").fetchall()
            # Since they share 'trust', they should overlap and cluster together
            # Let's check how many clusters were created. Jaccard Set similarity:
            # Union of {trust, people} and {trust, communication} = {trust, people, communication} (size 3)
            # Intersection = {trust} (size 1)
            # Jaccard = 1/3 = 0.33 >= 0.25 (the threshold), so they should group in the same cluster!
            chunk1_cluster = conn.execute("SELECT cluster_id FROM chunk_clusters WHERE chunk_id = 'DOC_DALIO_chunk_01';").fetchone()[0]
            chunk2_cluster = conn.execute("SELECT cluster_id FROM chunk_clusters WHERE chunk_id = 'DOC_KENNEDY_chunk_01';").fetchone()[0]
            
            # Assert they belong to the same cluster
            self.assertEqual(chunk1_cluster, chunk2_cluster)
            print(f"[TEST] Chunks successfully grouped under shared cluster ID: {chunk1_cluster}")
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
