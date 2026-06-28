#!/usr/bin/env python3
"""Perplexity Research Inbox Watcher (Continuous Background Chunker).

Scans the perplexity-inbox root directory for raw logs/markdown research inputs,
segments them into token-optimized 300-line chunk files with injected YAML metadata,
moves original files to /archive, and validates system targets.

Cleanly degrades if the remote database is unreachable.
"""
import os
import sys
import time
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Add the harness directory to python path for imports
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from harness.db_harness import assert_db_target

INBOX_DIR = ROOT_DIR
CHUNKS_DIR = ROOT_DIR / "chunks"
ARCHIVE_DIR = ROOT_DIR / "archive"
STATE_FILE = ROOT_DIR / "harness" / "watcher_state.json"
BEAST_CONN_URI = "postgresql://cove:lTJhzWncfPNVCAomIFtkyVoxPrIENLtE@127.0.0.1:5433/amplified_brain"

CHUNK_SIZE = 300
SCAN_INTERVAL_SECONDS = 15

# Directories and files that the watcher must NEVER process
IGNORE_DIRS = {
    "chunks", "archive", "harness", "scripts", "tests", "completed-by-antigravity",
    "completed-by-cascade-mac", "completed-by-cursor", "completed-by-devin",
    ".git", ".venv", "__pycache__", ".pytest_cache", ".cursor", ".claude",
    "prior-art-syntheses-bundle", "five-rods-pss-prior-art"
}
IGNORE_FILES = {
    "README.md", "brief.md", "claude-gmail-brief.md", "ESTATE-TAXONOMY.md", 
    "amplified_permissions.py", "email_to_pipe.py", "monitor.py", "research.py",
    "amplified_rules.json", "deterministic-patches.jsonl", "perplexity-inbox.code-workspace"
}


def load_state() -> dict:
    """Loads state containing processed file hashes."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WATCHER] Warning: Failed to load state: {e}", file=sys.stderr)
    return {"processed_hashes": {}}


def save_state(state: dict) -> None:
    """Saves state containing processed file hashes."""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"[WATCHER] Error saving state: {e}", file=sys.stderr)


def get_file_hash(filepath: Path) -> str:
    """Computes the SHA-256 hash of a file."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(f"[WATCHER] Error hashing file {filepath}: {e}", file=sys.stderr)
        return ""


def check_beast_database() -> bool:
    """Sanity-checks the Beast database connection. Degrades gracefully if down."""
    try:
        assert_db_target(BEAST_CONN_URI, expected_db="amplified_brain", min_graph_nodes=10000)
        print("[WATCHER] ✓ Beast DB connection guard check passed successfully.", file=sys.stderr)
        return True
    except Exception as e:
        print("\n" + "!"*70, file=sys.stderr)
        print(f"[WATCHER] WARNING: Beast database target check failed.", file=sys.stderr)
        print(f"Reason: {e}", file=sys.stderr)
        print("Degrading gracefully: Continuing local filesystem chunking operations.", file=sys.stderr)
        print("!"*70 + "\n", file=sys.stderr)
        return False


def chunk_file(filepath: Path, state: dict) -> Path | None:
    """Chunks a single file into 300-line blocks, prepending YAML headers."""
    try:
        file_hash = get_file_hash(filepath)
        if not file_hash:
            return None

        print(f"[WATCHER] Processing file: {filepath.name}...", file=sys.stderr)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        total_lines = len(lines)
        if total_lines == 0:
            print(f"[WATCHER] Warning: File {filepath.name} is empty. Skipping.", file=sys.stderr)
            return None

        total_chunks = (total_lines + CHUNK_SIZE - 1) // CHUNK_SIZE
        CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

        # Base prefix for output names (remove extension and replace spaces/dots)
        clean_prefix = filepath.stem.replace(" ", "_").replace(".", "_")
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        for i in range(total_chunks):
            start_idx = i * CHUNK_SIZE
            end_idx = min(start_idx + CHUNK_SIZE, total_lines)
            chunk_lines = lines[start_idx:end_idx]

            # Build YAML header with taxonomical clarity
            yaml_header = (
                "---\n"
                f"title: \"Chunk {i + 1} of {filepath.name}\"\n"
                f"date: \"{date_str}\"\n"
                f"document_type: \"research_chunk\"\n"
                f"epistemic_grade: \"STRUCTURED\"\n"
                f"source_file: \"{filepath.name}\"\n"
                f"chunk_index: {i + 1}\n"
                f"total_chunks: {total_chunks}\n"
                f"start_line: {start_idx + 1}\n"
                f"end_line: {end_idx}\n"
                f"parent_nodes: []\n"
                f"critical_rules: []\n"
                "---\n"
            )

            chunk_content = yaml_header + "".join(chunk_lines)
            chunk_filename = f"{clean_prefix}_chunk_{i + 1:02d}.txt"
            chunk_filepath = CHUNKS_DIR / chunk_filename

            with open(chunk_filepath, "w", encoding="utf-8") as f_out:
                f_out.write(chunk_content)

        # Archive the original file to prevent reprocessing
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        dest_path = ARCHIVE_DIR / filepath.name
        
        # If file already exists in archive, append timestamp to make it unique
        if dest_path.exists():
            ts = int(time.time())
            dest_name = f"{filepath.stem}_{ts}{filepath.suffix}"
            dest_path = ARCHIVE_DIR / dest_name

        shutil.move(str(filepath), str(dest_path))
        print(f"[WATCHER] ✓ Successfully chunked {filepath.name} into {total_chunks} pieces.", file=sys.stderr)
        print(f"[WATCHER] ✓ Original file moved to {dest_path.name}.", file=sys.stderr)

        # Record hash state
        state["processed_hashes"][filepath.name] = {
            "hash": file_hash,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "total_chunks": total_chunks,
            "lines": total_lines
        }
        return dest_path

    except Exception as e:
        print(f"[WATCHER] Error processing file {filepath.name}: {e}", file=sys.stderr)
        return None


def scan_inbox(state: dict) -> None:
    """Scans the inbox for text and markdown files and chunks them."""
    for item in INBOX_DIR.iterdir():
        # Exclude directories in ignore list or starting with dot
        if item.is_dir():
            continue
        
        # Check extensions
        if item.suffix.lower() not in (".txt", ".md"):
            continue

        # Exclude ignored filenames
        if item.name in IGNORE_FILES or item.name.startswith("INBOX-INDEX__"):
            continue

        # Exclude files that are currently being edited or locked
        if item.name.startswith(".") or item.name.endswith(".tmp"):
            continue

        # Process the file
        chunk_file(item, state)
        save_state(state)


def main():
    print("=================================================================", file=sys.stderr)
    print("STARTING PERPLEXITY INBOX WATCHER SERVICE", file=sys.stderr)
    print(f"Inbox Directory : {INBOX_DIR}", file=sys.stderr)
    print(f"Chunks Directory: {CHUNKS_DIR}", file=sys.stderr)
    print(f"Archive Directory: {ARCHIVE_DIR}", file=sys.stderr)
    print("=================================================================", file=sys.stderr)

    # Sanity-check the database status at startup
    check_beast_database()

    state = load_state()

    print(f"\n[WATCHER] Active. Monitoring every {SCAN_INTERVAL_SECONDS}s...", file=sys.stderr)
    try:
        while True:
            scan_inbox(state)
            time.sleep(SCAN_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n[WATCHER] Service stopped by user request.", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
