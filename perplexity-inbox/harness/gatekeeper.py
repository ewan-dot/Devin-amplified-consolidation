#!/usr/bin/env python3
"""Workspace and Database Gatekeeper.

Executes objective verification checks on git branch, PostgreSQL targets,
database extensions, and implementation plan frontmatter.
Returns exit code 0 on success, or exit code 1 if checks fail.
"""
import sys
import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple

HARNESS_DIR = Path(__file__).resolve().parent
ROOT_DIR = HARNESS_DIR.parent
COVE_CONN_URI = "postgresql://cove:lTJhzWncfPNVCAomIFtkyVoxPrIENLtE@127.0.0.1:5433/cove"

try:
    import psycopg
except ImportError:
    psycopg = None

def run_checks() -> bool:
    all_passed = True
    print("=================================================================")
    print("RUNNING WORKSPACE & DATABASE GATEKEEPER VERIFICATION")
    print("=================================================================")

    # 1. Git Status Checks
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
            cwd=str(ROOT_DIR), text=True
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], 
            cwd=str(ROOT_DIR), text=True
        ).strip()
        print(f"Git Branch: {branch} (Clean: {len(status) == 0})")
        if branch in ("main", "master"):
            print("  [FAIL] Direct work on main/master branch is prohibited.")
            all_passed = False
    except Exception as e:
        print(f"  [WARN] Could not retrieve git branch info: {e}")

    # 2. Database Capability Verification
    if psycopg is None:
        print("  [FAIL] python library 'psycopg' is missing.")
        all_passed = False
    else:
        try:
            with psycopg.connect(COVE_CONN_URI, connect_timeout=3.0) as conn:
                with conn.cursor() as cur:
                    # Query active extensions
                    cur.execute("SELECT extname FROM pg_extension WHERE extname IN ('vector', 'age');")
                    extensions = {r[0] for r in cur.fetchall()}
                    
                    print(f"Database Extensions: {list(extensions)}")
                    if "vector" not in extensions:
                        print("  [FAIL] 'vector' extension is not installed.")
                        all_passed = False
                    if "age" not in extensions:
                        print("  [FAIL] 'age' (Apache AGE) extension is not installed.")
                        all_passed = False

                    # Query active graphs
                    cur.execute("SELECT name FROM ag_catalog.ag_graph WHERE name = 'business_brain';")
                    graphs = {r[0] for r in cur.fetchall()}
                    print(f"Active Graphs: {list(graphs)}")
                    if "business_brain" not in graphs:
                        print("  [FAIL] Apache AGE graph 'business_brain' is not initialized.")
                        all_passed = False

        except Exception as e:
            print(f"  [FAIL] Connection failure to database: {e}")
            all_passed = False

    # 3. Schema File Vector Dimension Validation
    schema_path = HARNESS_DIR / "cove_trial_schema.sql"
    if schema_path.exists():
        try:
            sql_content = schema_path.read_text()
            vector_matches = re.findall(r"vector\((\d+)\)", sql_content)
            print(f"Schema Vector Dimensions: {vector_matches}")
            for dim in vector_matches:
                if dim != "384":
                    print(f"  [FAIL] Expected vector(384) for local watcher, found vector({dim}) in schema.")
                    all_passed = False
        except Exception as e:
            print(f"  [WARN] Failed to read schema file: {e}")
    else:
        print("  [FAIL] cove_trial_schema.sql is missing.")
        all_passed = False

    # 4. Implementation Plan Formatting check
    ip_path = ROOT_DIR / "implementation_plan.md"
    if not ip_path.exists():
        brain_dir = Path("/Users/ewansair/.gemini/antigravity/brain")
        if brain_dir.exists():
            candidates = []
            for folder in brain_dir.iterdir():
                if folder.is_dir() and not folder.name.startswith("."):
                    cand = folder / "implementation_plan.md"
                    if cand.exists():
                        candidates.append((cand, cand.stat().st_mtime))
            if candidates:
                candidates.sort(key=lambda x: x[1], reverse=True)
                ip_path = candidates[0][0]

    if ip_path and ip_path.exists():
        print(f"Auditing Plan: {ip_path.name}")
        try:
            content = ip_path.read_text()
            if "epistemic_tier" not in content and "epistemic_grade" not in content:
                print("  [FAIL] Plan is missing a valid epistemic_tier statement.")
                all_passed = False
            else:
                tier_match = re.search(r"epistemic_(?:tier|grade):\s*(\w+)", content)
                if tier_match:
                    print(f"  Declared Epistemic Tier: {tier_match.group(1)}")
        except Exception as e:
            print(f"  [WARN] Could not parse plan file: {e}")
    else:
        print("  [FAIL] Plan file implementation_plan.md was not found.")
        all_passed = False

    print("-----------------------------------------------------------------")
    print(f"OVERALL VERDICT: {'PASSED' if all_passed else 'FAILED'}")
    print("-----------------------------------------------------------------")
    return all_passed

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
