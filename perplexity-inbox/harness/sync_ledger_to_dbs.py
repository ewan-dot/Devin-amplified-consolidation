#!/usr/bin/env python3
"""Deterministic Prompt and Rules Sync Pipeline.

Propagates updates from the filesystem ledger (master) to the cove and
amplified_brain databases, enforcing structural discipline and preventing drift.
"""
import os
import sys
import argparse
import hashlib
import json
import uuid
import yaml
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory of harness to python path
HARNESS_DIR = Path(__file__).resolve().parent
ROOT_DIR = HARNESS_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from harness.db_harness import assert_db_target

# Connection URIs
COVE_CONN_URI = "postgresql://cove:lTJhzWncfPNVCAomIFtkyVoxPrIENLtE@127.0.0.1:5433/cove"
BRAIN_CONN_URI = "postgresql://cove:lTJhzWncfPNVCAomIFtkyVoxPrIENLtE@127.0.0.1:5433/amplified_brain"

# 19 Required Metadata Fields (AgentFS taxonomy)
REQUIRED_19_FIELDS = [
    "title", "date", "document_type", "epistemic_tier",
    "origin_type", "author", "source_file", "chunk_index",
    "total_chunks", "start_line", "end_line", "file_hash_sha256",
    "chunk_hash_sha256", "signature", "client_scope", "project_scope",
    "domain", "pii_class", "parent_nodes"
]


def get_file_sha256(filepath: Path) -> str:
    """Computes SHA-256 hash of the entire file on disk."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def escape_sql_val(val: str) -> str:
    """Escapes single quotes for SQL/Cypher statements."""
    if val is None:
        return ""
    return str(val).replace("'", "''")


def parse_and_validate_ledger_file(filepath: Path) -> tuple[dict, str]:
    """Parses Dual-YAML frontmatter and body, asserting the 19 required fields."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        raise ValueError(f"File {filepath.name} does not start with YAML marker '---'")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"File {filepath.name} is missing closing YAML marker '---'")

    yaml_header = parts[1]
    body = parts[2].strip()

    # Load YAML metadata
    try:
        meta = yaml.safe_load(yaml_header)
    except Exception as e:
        raise ValueError(f"Failed to parse YAML header in {filepath.name}: {e}")

    if not isinstance(meta, dict):
        raise ValueError(f"YAML header in {filepath.name} is not a valid dictionary")

    # Assert 19 Required Fields
    for field in REQUIRED_19_FIELDS:
        if field not in meta:
            raise ValueError(f"Validation Error: '{filepath.name}' is missing required field '{field}'")

    # Extra validation for prompts
    if "version" not in meta:
        meta["version"] = 1
    if "uuid" not in meta and "id" not in meta:
        # Generate deterministic UUID based on file relative path to prevent orphans
        rel_path = str(filepath.relative_to(ROOT_DIR.parent))
        meta["uuid"] = str(uuid.uuid5(uuid.NAMESPACE_DNS, rel_path))

    # Verify content hash (chunk_hash_sha256)
    computed_chunk_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    expected_chunk_hash = meta["chunk_hash_sha256"]
    if computed_chunk_hash != expected_chunk_hash:
        raise ValueError(
            f"Cryptographic Hash Mismatch in {filepath.name}:\n"
            f"  Expected (chunk_hash_sha256): {expected_chunk_hash}\n"
            f"  Computed (body text hash)   : {computed_chunk_hash}"
        )

    # Automatically set actual file hash based on disk state
    meta["actual_file_hash_sha256"] = get_file_sha256(filepath)

    return meta, body


def sync_prompts(prompts_dir: Path, force: bool) -> tuple[int, list]:
    """Syncs prompt ledger files to cove.system_prompts database table."""
    import psycopg

    if not prompts_dir.exists():
        print(f"[SYNC] Prompts directory {prompts_dir} does not exist. Skipping.", file=sys.stderr)
        return 0, []

    files = [p for p in prompts_dir.glob("*.md") if p.is_file() and p.name != "README.md"]
    if not files:
        print("[SYNC] No prompts found in prompts directory.", file=sys.stderr)
        return 0, []

    print(f"[SYNC] Scanning {len(files)} prompt files from ledger...", file=sys.stderr)
    sync_count = 0
    synced_items = []

    # Pre-flight check
    assert_db_target(COVE_CONN_URI, expected_db="cove")

    with psycopg.connect(COVE_CONN_URI) as conn:
        with conn.cursor() as cur:
            for fp in files:
                try:
                    meta, body = parse_and_validate_ledger_file(fp)
                    prompt_id = meta.get("uuid") or meta.get("id")
                    agent_role = meta.get("title")
                    layer = int(meta.get("layer", 1))
                    is_active = bool(meta.get("is_active", True))
                    version = int(meta.get("version", 1))

                    # Check current DB state to see if sync is needed
                    cur.execute(
                        "SELECT prompt_text, version, is_active FROM public.system_prompts WHERE id = %s",
                        (prompt_id,)
                    )
                    row = cur.fetchone()
                    
                    needs_update = force or (row is None) or (row[0] != body) or (row[1] != version) or (row[2] != is_active)

                    if needs_update:
                        print(f"[SYNC] Upserting prompt '{agent_role}' (v{version}) into cove...", file=sys.stderr)
                        cur.execute("""
                            INSERT INTO public.system_prompts (id, agent_role, layer, prompt_text, is_active, version, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, NOW())
                            ON CONFLICT (id) DO UPDATE 
                            SET prompt_text = EXCLUDED.prompt_text, 
                                version = EXCLUDED.version, 
                                is_active = EXCLUDED.is_active, 
                                updated_at = NOW();
                        """, (prompt_id, agent_role, layer, body, is_active, version))
                        sync_count += 1
                    
                    synced_items.append({
                        "id": prompt_id,
                        "name": agent_role,
                        "file": fp.name,
                        "file_hash": meta["actual_file_hash_sha256"],
                        "type": "prompt"
                    })
                except Exception as e:
                    print(f"[SYNC] [ERROR] Failed to sync prompt file {fp.name}: {e}", file=sys.stderr)
                    raise e

            conn.commit()

    return sync_count, synced_items


def sync_logic_packets(packets_dir: Path, force: bool) -> tuple[int, list]:
    """Syncs logic packets ledger files to amplified_brain Apache AGE graph."""
    import psycopg

    if not packets_dir.exists():
        print(f"[SYNC] Logic packets directory {packets_dir} does not exist. Skipping.", file=sys.stderr)
        return 0, []

    files = [p for p in packets_dir.glob("*.md") if p.is_file() and p.name != "README.md"]
    if not files:
        print("[SYNC] No logic packets found in logic_packets directory.", file=sys.stderr)
        return 0, []

    print(f"[SYNC] Scanning {len(files)} logic packets from ledger...", file=sys.stderr)
    sync_count = 0
    synced_items = []

    # Pre-flight check
    assert_db_target(BRAIN_CONN_URI, expected_db="amplified_brain", min_graph_nodes=10000)

    with psycopg.connect(BRAIN_CONN_URI) as conn:
        with conn.cursor() as cur:
            # Initialize AGE session
            cur.execute("LOAD 'age';")
            cur.execute("SET search_path = ag_catalog, public;")

            for fp in files:
                try:
                    meta, body = parse_and_validate_ledger_file(fp)
                    uuid_val = meta.get("uuid") or meta.get("id")
                    title = escape_sql_val(meta.get("title"))
                    file_hash = escape_sql_val(meta["actual_file_hash_sha256"])
                    chunk_hash = escape_sql_val(meta["chunk_hash_sha256"])
                    canonical_path = escape_sql_val(meta.get("canonical_path", f"/brain/logic_packets/{fp.name}"))
                    epistemic_tier = escape_sql_val(meta.get("epistemic_tier", "PROVEN"))
                    document_type = escape_sql_val(meta.get("document_type", "logic_capsule"))
                    author = escape_sql_val(meta.get("author", "system"))
                    updated_at = escape_sql_val(datetime.now(timezone.utc).isoformat())

                    # Check current DB state by retrieving the node
                    query_check = f"""
                        SELECT * FROM ag_catalog.cypher('business_brain', $$
                            MATCH (d:Document {{uuid: '{uuid_val}'}})
                            RETURN d
                        $$) AS (d ag_catalog.agtype);
                    """
                    cur.execute(query_check)
                    row = cur.fetchone()
                    
                    needs_update = force or (row is None)
                    if row is not None:
                        val = str(row[0])
                        if val.endswith('::vertex'):
                            val = val[:-8]
                        node_data = json.loads(val)
                        props = node_data.get('properties', {})
                        db_hash = props.get('file_hash_sha256')
                        if db_hash != file_hash:
                            needs_update = True

                    if needs_update:
                        print(f"[SYNC] Upserting logic packet node '{title}' into amplified_brain...", file=sys.stderr)
                        # Build upsert cypher statement
                        upsert_query = f"""
                            SELECT * FROM ag_catalog.cypher('business_brain', $$
                                MERGE (d:Document {{uuid: '{uuid_val}'}})
                                SET d.name = '{title}',
                                    d.file_hash_sha256 = '{file_hash}',
                                    d.chunk_hash_sha256 = '{chunk_hash}',
                                    d.canonical_path = '{canonical_path}',
                                    d.epistemic_tier = '{epistemic_tier}',
                                    d.document_type = '{document_type}',
                                    d.author = '{author}',
                                    d.updated_at = '{updated_at}'
                                RETURN d
                            $$) AS (d ag_catalog.agtype);
                        """
                        cur.execute(upsert_query)
                        sync_count += 1
                    
                    synced_items.append({
                        "id": uuid_val,
                        "name": title,
                        "file": fp.name,
                        "file_hash": file_hash,
                        "type": "logic_packet"
                    })
                except Exception as e:
                    print(f"[SYNC] [ERROR] Failed to sync logic packet file {fp.name}: {e}", file=sys.stderr)
                    raise e

            conn.commit()

    return sync_count, synced_items


def verify_drift(prompts_dir: Path, packets_dir: Path) -> int:
    """Verifies alignment between filesystem and databases, returning non-zero on drift."""
    import psycopg

    print("[VERIFY] Starting preflight semantic drift check...", file=sys.stderr)
    drift_detected = False
    
    # 1. Verify Prompts
    if prompts_dir.exists():
        files = [p for p in prompts_dir.glob("*.md") if p.is_file() and p.name != "README.md"]
        if files:
            assert_db_target(COVE_CONN_URI, expected_db="cove")
            with psycopg.connect(COVE_CONN_URI) as conn:
                with conn.cursor() as cur:
                    for fp in files:
                        try:
                            meta, body = parse_and_validate_ledger_file(fp)
                            prompt_id = meta.get("uuid") or meta.get("id")
                            cur.execute(
                                "SELECT prompt_text, version, is_active FROM public.system_prompts WHERE id = %s",
                                (prompt_id,)
                            )
                            row = cur.fetchone()
                            if not row:
                                print(f"[DRIFT] Prompt '{meta['title']}' ({fp.name}) is MISSING from cove.", file=sys.stderr)
                                drift_detected = True
                            else:
                                if row[0] != body:
                                    print(f"[DRIFT] Prompt '{meta['title']}' ({fp.name}) text does not match cove.", file=sys.stderr)
                                    drift_detected = True
                                if row[1] != int(meta.get("version", 1)):
                                    print(f"[DRIFT] Prompt '{meta['title']}' ({fp.name}) version mismatch (disk={meta.get('version')}, DB={row[1]}).", file=sys.stderr)
                                    drift_detected = True
                                if row[2] != bool(meta.get("is_active", True)):
                                    print(f"[DRIFT] Prompt '{meta['title']}' ({fp.name}) is_active mismatch (disk={meta.get('is_active')}, DB={row[2]}).", file=sys.stderr)
                                    drift_detected = True
                        except Exception as e:
                            print(f"[VERIFY] [ERROR] Failed to check prompt {fp.name}: {e}", file=sys.stderr)
                            drift_detected = True

    # 2. Verify Logic Packets
    if packets_dir.exists():
        files = [p for p in packets_dir.glob("*.md") if p.is_file() and p.name != "README.md"]
        if files:
            assert_db_target(BRAIN_CONN_URI, expected_db="amplified_brain", min_graph_nodes=10000)
            with psycopg.connect(BRAIN_CONN_URI) as conn:
                with conn.cursor() as cur:
                    cur.execute("LOAD 'age';")
                    cur.execute("SET search_path = ag_catalog, public;")
                    for fp in files:
                        try:
                            meta, body = parse_and_validate_ledger_file(fp)
                            uuid_val = meta.get("uuid") or meta.get("id")
                            file_hash = meta["actual_file_hash_sha256"]
                            query = f"""
                                SELECT * FROM ag_catalog.cypher('business_brain', $$
                                    MATCH (d:Document {{uuid: '{uuid_val}'}})
                                    RETURN d
                                $$) AS (d ag_catalog.agtype);
                            """
                            cur.execute(query)
                            row = cur.fetchone()
                            if not row:
                                print(f"[DRIFT] Logic packet '{meta['title']}' ({fp.name}) is MISSING from AGE graph.", file=sys.stderr)
                                drift_detected = True
                            else:
                                val = str(row[0])
                                if val.endswith('::vertex'):
                                    val = val[:-8]
                                node_data = json.loads(val)
                                props = node_data.get('properties', {})
                                db_hash = props.get('file_hash_sha256')
                                if db_hash != file_hash:
                                    print(f"[DRIFT] Logic packet '{meta['title']}' ({fp.name}) hash mismatch (disk={file_hash}, DB={db_hash}).", file=sys.stderr)
                                    drift_detected = True
                        except Exception as e:
                            print(f"[VERIFY] [ERROR] Failed to check logic packet {fp.name}: {e}", file=sys.stderr)
                            drift_detected = True

    if drift_detected:
        print("\n[VERIFY] Drift check completed: DRIFT DETECTED.", file=sys.stderr)
        return 1
    
    print("\n[VERIFY] Drift check completed: ALL FILES IN COHESION.", file=sys.stderr)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Deterministic Prompt and Rules Sync Pipeline.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sync", action="store_true", help="Sync ledger changes to databases.")
    group.add_argument("--verify", action="store_true", help="Verify filesystem-database consistency and report drift.")
    parser.add_argument("--force", action="store_true", help="Force sync all files regardless of version/hash checks.")
    args = parser.parse_args()

    prompts_dir = ROOT_DIR.parent / "prompts"
    packets_dir = ROOT_DIR.parent / "brain" / "logic_packets"

    # Create directories if they do not exist
    prompts_dir.mkdir(parents=True, exist_ok=True)
    packets_dir.mkdir(parents=True, exist_ok=True)

    if args.verify:
        sys.exit(verify_drift(prompts_dir, packets_dir))

    if args.sync:
        print("[START] Beginning sync pipeline execution...", file=sys.stderr)
        prompt_syncs, prompt_items = sync_prompts(prompts_dir, args.force)
        packet_syncs, packet_items = sync_logic_packets(packets_dir, args.force)
        
        print("\n" + "="*50, file=sys.stderr)
        print(f"SYNC RUN COMPLETE", file=sys.stderr)
        print(f"  • Prompts written/updated: {prompt_syncs} of {len(prompt_items)}", file=sys.stderr)
        print(f"  • Logic packets written:   {packet_syncs} of {len(packet_items)}", file=sys.stderr)
        print("="*50 + "\n", file=sys.stderr)
        
        # After sync, run verification as an assertions check
        sys.exit(verify_drift(prompts_dir, packets_dir))


if __name__ == "__main__":
    main()
