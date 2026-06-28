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
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone

# Add the harness directory to python path for imports
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from harness.db_harness import assert_db_target

# Dynamically resolve sentence_transformers if run with system python
try:
    import sentence_transformers
except ImportError:
    venv_site = "/Users/ewansair/ingestion-to-research-pipe/clean-build/02_build/scripts/.venv/lib/python3.13/site-packages"
    if os.path.exists(venv_site) and venv_site not in sys.path:
        sys.path.append(venv_site)
    try:
        import sentence_transformers
    except ImportError:
        print("[WATCHER] Warning: sentence_transformers not available. Offline vector cache generation will be skipped.", file=sys.stderr)
        sentence_transformers = None

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


def determine_document_category(filepath: Path, content: str) -> str:
    """Parses frontmatter or filename prefix to categorize the document into the taxonomy."""
    doc_type = None
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
    if fm_match:
        fm_content = fm_match.group(1)
        type_match = re.search(r'^document_type:\s*["\']?([\w\-]+)["\']?', fm_content, re.MULTILINE)
        if type_match:
            doc_type = type_match.group(1).lower()

    if doc_type:
        category_map = {
            "doctrine": "doctrine",
            "operating_rule": "rules",
            "rule": "rules",
            "rules": "rules",
            "conclusions": "briefs",
            "brief": "briefs",
            "briefs": "briefs",
            "decision": "decisions",
            "decisions": "decisions",
            "research_brief": "research",
            "research_conclusion": "research",
            "research": "research",
            "hypothesis": "research",
            "baton": "batons",
            "baton_pass": "batons",
            "batons": "batons",
            "coordination": "coordination",
            "session_start": "coordination",
            "handoff": "coordination"
        }
        if doc_type in category_map:
            return category_map[doc_type]

    # Filename prefix fallback
    filename = filepath.name.upper()
    if filename.startswith("DOCTRINE__"):
        return "doctrine"
    elif filename.startswith("DECISION__") or filename.startswith("CONCLUSIONS__"):
        return "decisions"
    elif filename.startswith("OPERATING-RULE__") or filename.startswith("RULE__"):
        return "rules"
    elif filename.startswith("RESEARCH-BRIEF__") or filename.startswith("RESEARCH-PIPE-RUN__") or filename.startswith("HYPOTHESIS__") or filename.startswith("RESEARCH__"):
        return "research"
    elif filename.startswith("BATON__") or filename.startswith("BATON-PASS__"):
        return "batons"
    elif filename.startswith("SESSION-START__") or filename.startswith("HANDOFF__"):
        return "coordination"
    elif "BRIEF" in filename:
        return "briefs"

    return "general"


def write_macos_xattr_metadata(filepath: Path, category: str, document_type: str, title: str, epistemic_grade: str) -> None:
    """Writes metadata to macOS Extended Attributes for native Spotlight indexing."""
    if sys.platform != "darwin":
        return
    
    keywords = [category, document_type, epistemic_grade]
    keywords_clean = ", ".join(sorted(list(set(k.lower() for k in keywords if k))))
    
    try:
        # 1. Write Keywords (Spotlight searchable)
        subprocess.run(
            ["xattr", "-w", "com.apple.metadata:kMDItemKeywords", keywords_clean, str(filepath)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        # 2. Write Description/Title
        if title:
            subprocess.run(
                ["xattr", "-w", "com.apple.metadata:kMDItemDescription", title, str(filepath)],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        # 3. Write Finder tag corresponding to category
        tag_name = category.capitalize()
        subprocess.run(
            ["xattr", "-w", "com.apple.metadata:kMDItemUserTags", tag_name, str(filepath)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        # Force spotlight re-import
        subprocess.run(
            ["mdimport", str(filepath)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[WATCHER] Warning: Failed to write extended attributes to {filepath.name}: {e}", file=sys.stderr)


_model_cache = None

def get_embedding_model():
    """Lazily loads the SentenceTransformer model."""
    global _model_cache
    if _model_cache is None:
        if sentence_transformers is None:
            return None
        print("[WATCHER] Loading SentenceTransformer 'all-MiniLM-L6-v2'...", file=sys.stderr)
        try:
            _model_cache = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"[WATCHER] Error loading model: {e}", file=sys.stderr)
            _model_cache = None
    return _model_cache


def generate_vector_cache(chunk_filepath: Path, text_content: str) -> None:
    """Generates embedding vector and writes it as JSON float array beside the text chunk."""
    model = get_embedding_model()
    if model is None:
        return
    try:
        # Strip frontmatter header for embedding calculation
        content_to_embed = text_content
        if text_content.startswith("---"):
            parts = text_content.split("---", 2)
            if len(parts) >= 3:
                content_to_embed = parts[2].strip()
                
        vector = model.encode(content_to_embed, normalize_embeddings=True)
        vector_filepath = chunk_filepath.with_suffix(".vector")
        with open(vector_filepath, "w", encoding="utf-8") as f:
            json.dump(vector.tolist(), f)
    except Exception as e:
        print(f"[WATCHER] Error generating vector cache for {chunk_filepath.name}: {e}", file=sys.stderr)


def chunk_file(filepath: Path, state: dict) -> Path | None:
    """Chunks a single file into 300-line blocks inside a structured folder.
    
    Generates text chunks, pre-computed vector files, and document metadata.
    """
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

        content = "".join(lines)
        category = determine_document_category(filepath, content)
        
        # Parse document metadata from frontmatter if available
        document_type = category
        title = filepath.stem
        epistemic_grade = "STRUCTURED"
        
        if category == "doctrine":
            epistemic_grade = "DOCTRINE"
        elif category == "rules":
            epistemic_grade = "RULE"

        fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
        if fm_match:
            fm_content = fm_match.group(1)
            type_match = re.search(r'^document_type:\s*["\']?([\w\-]+)["\']?', fm_content, re.MULTILINE)
            if type_match:
                document_type = type_match.group(1).lower()
            grade_match = re.search(r'^epistemic_(?:grade|tier):\s*["\']?([\w\-]+)["\']?', fm_content, re.MULTILINE)
            if grade_match:
                epistemic_grade = grade_match.group(1).upper()
            title_match = re.search(r'^title:\s*["\']?([^"\n\']+)["\']?', fm_content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)

        total_chunks = (total_lines + CHUNK_SIZE - 1) // CHUNK_SIZE
        
        # Establish structured destination directory
        clean_prefix = filepath.stem.replace(" ", "_").replace(".", "_")
        doc_dir = CHUNKS_DIR / category / clean_prefix
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        chunks_meta = []

        for i in range(total_chunks):
            start_idx = i * CHUNK_SIZE
            end_idx = min(start_idx + CHUNK_SIZE, total_lines)
            chunk_lines = lines[start_idx:end_idx]

            chunk_filename = f"chunk_{i + 1:02d}.txt"
            chunk_filepath = doc_dir / chunk_filename
            canonical_path = f"/chunks/{category}/{clean_prefix}/{chunk_filename}"

            yaml_header = (
                "---\n"
                f"title: \"Chunk {i + 1} of {title}\"\n"
                f"date: \"{date_str}\"\n"
                f"document_type: \"{document_type}\"\n"
                f"epistemic_grade: \"{epistemic_grade}\"\n"
                f"canonical_path: \"{canonical_path}\"\n"
                f"chunk_index: {i + 1}\n"
                f"total_chunks: {total_chunks}\n"
                f"start_line: {start_idx + 1}\n"
                f"end_line: {end_idx}\n"
                f"source_file: \"{filepath.name}\"\n"
                "---\n"
            )

            chunk_content = yaml_header + "".join(chunk_lines)

            with open(chunk_filepath, "w", encoding="utf-8") as f_out:
                f_out.write(chunk_content)

            # Generate offline vector embedding cache beside chunk text
            generate_vector_cache(chunk_filepath, chunk_content)
            
            # Write Spotlight extended attributes and force mdimport on macOS
            write_macos_xattr_metadata(chunk_filepath, category, document_type, f"Chunk {i + 1} of {title}", epistemic_grade)

            chunks_meta.append({
                "chunk_index": i + 1,
                "filename": chunk_filename,
                "start_line": start_idx + 1,
                "end_line": end_idx
            })

        # Write document-level metadata mapping
        doc_metadata = {
            "document_name": filepath.name,
            "document_clean_name": clean_prefix,
            "category": category,
            "document_type": document_type,
            "epistemic_grade": epistemic_grade,
            "file_hash": file_hash,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "total_chunks": total_chunks,
            "total_lines": total_lines,
            "chunks": chunks_meta
        }
        with open(doc_dir / "metadata.json", "w", encoding="utf-8") as f_meta:
            json.dump(doc_metadata, f_meta, indent=2)

        # Archive the original file to prevent reprocessing
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        dest_path = ARCHIVE_DIR / filepath.name
        
        if dest_path.exists():
            ts = int(time.time())
            dest_name = f"{filepath.stem}_{ts}{filepath.suffix}"
            dest_path = ARCHIVE_DIR / dest_name

        shutil.move(str(filepath), str(dest_path))
        print(f"[WATCHER] ✓ Successfully chunked {filepath.name} into {total_chunks} pieces inside chunks/{category}/{clean_prefix}/", file=sys.stderr)
        print(f"[WATCHER] ✓ Original file archived to {dest_path.name}.", file=sys.stderr)

        # Record hash state
        state["processed_hashes"][filepath.name] = {
            "hash": file_hash,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "total_chunks": total_chunks,
            "lines": total_lines,
            "category": category,
            "destination_dir": str(doc_dir.relative_to(ROOT_DIR))
        }
        return dest_path

    except Exception as e:
        print(f"[WATCHER] Error processing file {filepath.name}: {e}", file=sys.stderr)
        return None

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
