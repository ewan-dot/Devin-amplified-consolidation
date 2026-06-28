#!/usr/bin/env python3
"""Database target harness connection guards (Rod 1 & No Silent Failures).

Deterministic boundary validator ensuring that AI agents and scripts connect 
to the canonical databases (e.g., amplified_brain) and preventing split-database
pollution of the orchestrator/metadata databases (e.g., cove).
"""
import sys
import urllib.parse
from typing import Any

try:
    import psycopg
except ImportError:
    print("[db_harness] WARNING: psycopg not installed in local environment.", file=sys.stderr)


def parse_db_name(connection_uri: str) -> str:
    """Safely extracts the database name from a connection URI."""
    try:
        parsed = urllib.parse.urlparse(connection_uri)
        # Path is usually /database_name, strip slash
        db_name = parsed.path.lstrip('/')
        # Strip query parameters if any
        if '?' in db_name:
            db_name = db_name.split('?')[0]
        return db_name
    except Exception as e:
        raise ValueError(f"Invalid connection URI: {connection_uri}. Error: {e}")


def assert_db_target(
    connection_uri: str, 
    expected_db: str = "amplified_brain", 
    min_graph_nodes: int = 10000
) -> None:
    """Asserts that the connection points to the correct canonical database

    and verifies that the database contains the expected production graphs
    and minimum node count. Raises AssertionError on mismatch.
    """
    db_name = parse_db_name(connection_uri)
    
    print("\n" + "="*70, file=sys.stderr)
    print(f"[DB HARNESS] PRE-FLIGHT VERIFICATION FOR DATABASE: '{db_name}'", file=sys.stderr)
    print("="*70, file=sys.stderr)
    
    # 1. Assert Database Name
    if db_name != expected_db:
        err_msg = (
            f"\n!!! [CRITICAL SENSOR BLOCK] DATABASE TARGET MISMATCH !!!\n"
            f"Expected Canonical DB : '{expected_db}'\n"
            f"Target DB Connection  : '{db_name}'\n"
            f"Reason                : Targeting '{db_name}' for Business Brain or production "
            f"operations creates split databases and pollutes orchestrator schemas.\n"
            f"ACTION                : Execution HALTED. Verify connection strings.\n"
        )
        print(err_msg, file=sys.stderr)
        raise AssertionError(err_msg)

    # 2. Check Database Node Content if targeting amplified_brain
    if expected_db == "amplified_brain":
        try:
            with psycopg.connect(connection_uri, connect_timeout=5.0) as conn:
                with conn.cursor() as cur:
                    # Verify Apache AGE extension is active
                    cur.execute("SELECT COUNT(*) FROM pg_extension WHERE extname = 'age';")
                    has_age = cur.fetchone()[0] > 0
                    if not has_age:
                        raise AssertionError(
                            "DATABASE INTEGRITY ERROR: Apache AGE extension is NOT active on target database."
                        )
                    
                    # Verify target graph exists and count vertices
                    cur.execute("SELECT COUNT(*) FROM ag_catalog.ag_graph WHERE name = 'business_brain';")
                    has_graph = cur.fetchone()[0] > 0
                    if not has_graph:
                        raise AssertionError(
                            "DATABASE INTEGRITY ERROR: 'business_brain' graph does not exist in target database."
                        )
                    
                    cur.execute("SELECT * FROM ag_catalog.cypher('business_brain', $$ MATCH (v) RETURN count(v) $$) AS (c ag_catalog.agtype);")
                    res = cur.fetchone()[0]
                    # cypher returns a string/agtype, strip quotes or cast to int
                    node_count = int(str(res).replace('"', ''))
                    
                    print(f"  ✓ Database name matches expected: '{expected_db}'", file=sys.stderr)
                    print(f"  ✓ Apache AGE extension: ACTIVE", file=sys.stderr)
                    print(f"  ✓ Active Graph: 'business_brain' contains {node_count:,} nodes", file=sys.stderr)
                    
                    # Check threshold
                    if node_count < min_graph_nodes:
                        err_msg = (
                            f"\n!!! [CRITICAL SENSOR BLOCK] SANITY CHECK FAILED !!!\n"
                            f"Target Graph  : 'business_brain'\n"
                            f"Node Count    : {node_count} nodes\n"
                            f"Threshold     : Expected >= {min_graph_nodes} nodes\n"
                            f"Reason        : Target has abnormally low node counts. This is a duplicate "
                            f"dummy sandbox or a polluted schema, not the production database.\n"
                            f"ACTION        : Execution HALTED to prevent split-database writing.\n"
                        )
                        print(err_msg, file=sys.stderr)
                        raise AssertionError(err_msg)
                    
                    print(f"  ✓ Verification PASSED. Database is safe for operations.", file=sys.stderr)
                    print("="*70 + "\n", file=sys.stderr)
                    
        except Exception as e:
            if isinstance(e, AssertionError):
                raise
            err_msg = f"DATABASE CONNECTION FAILURE: Could not connect or query target. Error: {e}"
            print(f"[DB HARNESS] ERROR: {err_msg}", file=sys.stderr)
            raise ConnectionError(err_msg) from e


if __name__ == "__main__":
    # Test script directly if connection parameters passed
    if len(sys.argv) > 1:
        uri = sys.argv[1]
        try:
            assert_db_target(uri)
            sys.exit(0)
        except Exception as err:
            print(f"Test Failed: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python3 db_harness.py <connection_uri>", file=sys.stderr)
        sys.exit(1)
