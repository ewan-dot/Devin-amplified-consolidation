#!/usr/bin/env python3
"""Verification Test for Cove Ingestion Pipeline.

Connects to the cove database, applies the trial schema, runs a mock
ingestion cycle (insert raw log -> generate vector -> insert node),
and asserts successful database writes.
"""
import sys
import os
import hashlib
import json
import psycopg
from pathlib import Path
from datetime import datetime, timezone

COVE_CONN_URI = "postgresql://cove:lTJhzWncfPNVCAomIFtkyVoxPrIENLtE@127.0.0.1:5433/cove"
SCHEMA_FILE = Path(__file__).resolve().parent / "cove_trial_schema.sql"

def apply_schema(conn) -> None:
    print("[TEST] Applying cove_trial_schema.sql...")
    schema_sql = SCHEMA_FILE.read_text()
    with conn.cursor() as cur:
        cur.execute(schema_sql)
    print("[TEST] Schema applied successfully.")

def run_ingestion_cycle(conn) -> bool:
    print("[TEST] Running mock ingestion cycle...")
    
    # 1. Insert Raw Ingestion Log
    raw_text = "Doctrine: Data is king. Simple is the thought. Easy is the interface. Bob drives."
    sha256 = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()
    
    with conn.cursor() as cur:
        # Check if hash already exists to prevent unique constraint violation
        cur.execute("SELECT id FROM raw_ingestion_log WHERE sha256 = %s;", (sha256,))
        existing = cur.fetchone()
        if existing:
            raw_id = existing[0]
            print(f"[TEST] Raw log already exists, ID: {raw_id}")
        else:
            cur.execute("""
                INSERT INTO raw_ingestion_log (
                    source_system, source_type, source_identifier, raw_text, sha256, status
                ) VALUES (
                    'test_harness', 'manual_note', 'test_doc_01', %s, %s, 'validated'
                ) RETURNING id;
            """, (raw_text, sha256))
            raw_id = cur.fetchone()[0]
            print(f"[TEST] Inserted raw log, ID: {raw_id}")

        # 2. Insert Knowledge Node (using mock 384-dimensional vector)
        mock_embedding = [0.1] * 384  # 384-dimensional vector of floats
        node_sha = hashlib.sha256(f"node_{raw_id}".encode('utf-8')).hexdigest()
        
        # Check if node already exists
        cur.execute("SELECT id FROM knowledge_nodes WHERE sha256 = %s;", (node_sha,))
        existing_node = cur.fetchone()
        if existing_node:
            print(f"[TEST] Knowledge node already exists, ID: {existing_node[0]}")
        else:
            cur.execute("""
                INSERT INTO knowledge_nodes (
                    raw_ingestion_id, node_type, title, body, sha256,
                    label_what, label_how, label_scale, label_time,
                    epistemic_tag, embedding
                ) VALUES (
                    %s, 'chunk', 'Test Doctrine Node', %s, %s,
                    'D', '=', '1', 'i',
                    'observed', %s
                ) RETURNING id;
            """, (raw_id, raw_text, node_sha, mock_embedding))
            node_id = cur.fetchone()[0]
            print(f"[TEST] Inserted knowledge node, ID: {node_id}")

        # 3. Verification Queries
        cur.execute("SELECT COUNT(*) FROM raw_ingestion_log;")
        raw_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM knowledge_nodes;")
        node_count = cur.fetchone()[0]
        
        print(f"[TEST] Verification: raw_ingestion_log count = {raw_count}")
        print(f"[TEST] Verification: knowledge_nodes count = {node_count}")
        
        # Fetch the inserted embedding to verify dimension size
        if not existing_node:
            cur.execute("SELECT vector_dims(embedding) FROM knowledge_nodes WHERE id = %s;", (node_id,))
            dims = cur.fetchone()[0]
            print(f"[TEST] Embedding properties: dimensions = {dims}")
            if dims != 384:
                print(f"[TEST] FAIL: Expected 384 dimensions, got {dims}")
                return False
                
    print("[TEST] Ingestion cycle completed successfully.")
    return True

def main():
    try:
        with psycopg.connect(COVE_CONN_URI) as conn:
            conn.autocommit = True
            apply_schema(conn)
            success = run_ingestion_cycle(conn)
            if success:
                print("[TEST] VERDICT: SUCCESS")
                sys.exit(0)
            else:
                print("[TEST] VERDICT: FAILED")
                sys.exit(1)
    except Exception as e:
        print(f"[TEST] Connection/Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
