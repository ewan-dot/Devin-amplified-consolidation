#!/usr/bin/env python3
"""Deterministic Validation Harness for Agentic Workflows.

Implements objective, rule-based verification checks as actionable pathways
(tools) that agents can call programmatically to verify system state.
"""

import os
import sys
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


class DeterministicHarness:
    def __init__(self, workspace_root: Path = ROOT_DIR):
        self.workspace_root = workspace_root

    def check_git_isolation(self) -> Tuple[bool, str]:
        """Pathway 1: Verify that the agent is running in a configured git worktree or isolated branch."""
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=str(self.workspace_root), text=True
            ).strip()
            
            worktrees_output = subprocess.check_output(
                ["git", "worktree", "list"],
                cwd=str(self.workspace_root), text=True
            ).strip()
            
            is_worktree = ".worktrees" in worktrees_output or "worktrees" in worktrees_output
            
            if branch in ("main", "master"):
                return False, f"Banned branch checkout: currently on direct branch '{branch}'."
            
            status_desc = f"Git isolation verified: active branch is '{branch}' (Worktree: {is_worktree})."
            return True, status_desc
        except Exception as e:
            return False, f"Failed git isolation check: {e}"

    def check_database_capabilities(self, uri: str = COVE_CONN_URI) -> Tuple[bool, List[str]]:
        """Pathway 2: Verify PostgreSQL capabilities, active extensions, and graph namespaces."""
        if psycopg is None:
            return False, ["Missing required 'psycopg' library."]

        issues = []
        try:
            with psycopg.connect(uri, connect_timeout=3.0) as conn:
                with conn.cursor() as cur:
                    # Check AGE and Vector extensions
                    cur.execute("SELECT extname FROM pg_extension WHERE extname IN ('vector', 'age');")
                    exts = {r[0] for r in cur.fetchall()}
                    if "vector" not in exts:
                        issues.append("PostgreSQL 'vector' extension is missing.")
                    if "age" not in exts:
                        issues.append("PostgreSQL 'age' extension is missing.")
                    
                    # Check AGE Graph
                    cur.execute("SELECT name FROM ag_catalog.ag_graph WHERE name = 'business_brain';")
                    graphs = {r[0] for r in cur.fetchall()}
                    if "business_brain" not in graphs:
                        issues.append("AGE Graph 'business_brain' is not initialized.")
                        
        except Exception as e:
            return False, [f"Database connection failure: {e}"]

        return len(issues) == 0, issues if issues else ["Database capabilities and AGE graph verified successfully."]

    def check_vector_dimension_match(self, schema_file: Path, expected_dim: int = 384) -> Tuple[bool, str]:
        """Pathway 3: Verify that SQL schema vector columns match the expected embeddings dimension size."""
        if not schema_file.exists():
            return False, f"Schema file not found: {schema_file}"
        try:
            sql_content = schema_file.read_text()
            dimensions = [int(d) for d in re.findall(r"vector\((\d+)\)", sql_content)]
            if not dimensions:
                return False, "No vector columns found in the schema file."
            for dim in dimensions:
                if dim != expected_dim:
                    return False, f"Dimension mismatch: expected vector({expected_dim}), found vector({dim}) in schema."
            return True, f"Vector dimensions successfully verified (dimension={expected_dim})."
        except Exception as e:
            return False, f"Failed dimension verification: {e}"

    def verify_no_vibe_self_ratings(self, file_path: Path) -> Tuple[bool, str]:
        """Pathway 4: Ensures that validation files do not rely on subjective, unverified self-ratings."""
        if not file_path.exists():
            return True, f"File {file_path.name} does not exist (skip vibe check)."
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            # If it's JSON, parse and check
            if file_path.suffix == '.json':
                data = json.loads(content)
                rating = data.get("confidence_rating", {})
                if rating:
                    score = rating.get("score")
                    if score == 1.0 and "verified" not in rating.get("rationale", "").lower():
                        return False, "Banned 'vibe' rating: score is set to 1.0 without programmatic verification."
            return True, "No subjective vibe self-ratings detected."
        except Exception as e:
            return False, f"Failed vibe self-rating check: {e}"


def print_help():
    print("""Deterministic Validation Harness (AI Pathway Tool)

Available pathways:
  --git      Verify git branch isolation and worktree status.
  --db       Verify database extensions (vector, age) and AGE graph.
  --vector   Verify schema vector dimensions against embedding settings.
  --vibe     Check target JSON files for subjective confidence vibe-ratings.
  --test     Run all validation pathways with test suites.
  --all      Run all validation pathways (default).
""")


def main():
    harness = DeterministicHarness()
    args = sys.argv[1:]
    
    if not args or "--all" in args:
        args = ["--git", "--db", "--vector"]

    if "--help" in args or "-h" in args:
        print_help()
        sys.exit(0)

    if "--test" in args:
        # Run test suites
        git_ok, git_msg = harness.check_git_isolation()
        print(f"[-] Git Isolation Check: {'PASSED' if git_ok else 'FAILED'}\n    {git_msg}")
        
        db_ok, db_msg = harness.check_database_capabilities()
        print(f"[-] DB Capabilities Check: {'PASSED' if db_ok else 'FAILED'}")
        for msg in db_msg:
            print(f"    {msg}")
            
        schema_path = HARNESS_DIR / "cove_trial_schema.sql"
        dim_ok, dim_msg = harness.check_vector_dimension_match(schema_path, expected_dim=384)
        print(f"[-] Vector Dimensions Check: {'PASSED' if dim_ok else 'FAILED'}\n    {dim_msg}")
        
        # Test vibe check on dummy
        dummy_path = HARNESS_DIR / "dummy_vibe.json"
        with open(dummy_path, "w") as f:
            json.dump({"confidence_rating": {"score": 1.0, "rationale": "It feels right"}}, f)
        vibe_ok, vibe_msg = harness.verify_no_vibe_self_ratings(dummy_path)
        if dummy_path.exists():
            os.remove(dummy_path)
        print(f"[-] No Vibe Check (Fail Test): {'PASSED' if not vibe_ok else 'FAILED'}\n    {vibe_msg}")
        
        all_passed = git_ok and db_ok and dim_ok and not vibe_ok
        print("----------------------------------------------------------------")
        print(f"OVERALL VERDICT: {'PASSED' if all_passed else 'FAILED'}")
        sys.exit(0 if all_passed else 1)

    # Individual pathway runs
    success = True
    if "--git" in args:
        ok, msg = harness.check_git_isolation()
        print(f"[PATHWAY: git] {'PASS' if ok else 'FAIL'} - {msg}")
        if not ok: success = False
        
    if "--db" in args:
        ok, msgs = harness.check_database_capabilities()
        print(f"[PATHWAY: db] {'PASS' if ok else 'FAIL'}")
        for msg in msgs:
            print(f"  • {msg}")
        if not ok: success = False
        
    if "--vector" in args:
        schema_path = HARNESS_DIR / "cove_trial_schema.sql"
        ok, msg = harness.check_vector_dimension_match(schema_path, expected_dim=384)
        print(f"[PATHWAY: vector] {'PASS' if ok else 'FAIL'} - {msg}")
        if not ok: success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
