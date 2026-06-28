#!/usr/bin/env python3
"""Unified Chunks Search CLI (The Platform-Agnostic Context Compiler).

Provides identical query mechanics across macOS (wrapping Spotlight/mdfind) and 
Linux (walking folders and caching indexes in a local SQLite DB), assembling results
into a structured "Logic Sandwich" to optimize LLM positional attention.
"""
import os
import sys
import json
import sqlite3
import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
CHUNKS_DIR = ROOT_DIR / "chunks"
SQLITE_CACHE_DIR = Path.home() / ".cache"
SQLITE_CACHE_FILE = SQLITE_CACHE_DIR / "amplified_data_lake.db"

# Categorization mapping
AUTHORITY_CATEGORIES = {"doctrine", "rules"}
METHODOLOGY_CATEGORIES = {"decisions", "research"}


def parse_yaml_header(content: str) -> dict:
    """Helper to parse a chunk's YAML frontmatter."""
    meta = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_content = parts[1]
            for line in fm_content.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta


class SQLiteSearchIndex:
    """Linux fallback: SQLite database to match Spotlight speed."""
    def __init__(self):
        SQLITE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(SQLITE_CACHE_FILE)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    path TEXT PRIMARY KEY,
                    name TEXT,
                    clean_name TEXT,
                    category TEXT,
                    document_type TEXT,
                    epistemic_grade TEXT,
                    file_hash TEXT,
                    processed_at TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    path TEXT PRIMARY KEY,
                    document_path TEXT,
                    chunk_index INTEGER,
                    filename TEXT,
                    content TEXT,
                    start_line INTEGER,
                    end_line INTEGER,
                    FOREIGN KEY(document_path) REFERENCES documents(path) ON DELETE CASCADE
                )
            """)
            # Create indexes for search speed
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_chunks_content ON chunks(content)")

    def sync(self, force=False):
        """Scans the chunks/ folder and syncs SQLite database with disk files."""
        if not CHUNKS_DIR.exists():
            return

        print("[SQLITE INDEX] Syncing file cache index...", file=sys.stderr)
        
        # Get all metadata.json files
        disk_docs = {}
        for meta_path in CHUNKS_DIR.glob("**/metadata.json"):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta_data = json.load(f)
                doc_dir = meta_path.parent
                disk_docs[str(doc_dir)] = meta_data
            except Exception as e:
                print(f"[SQLITE INDEX] Warning: Failed to parse metadata {meta_path}: {e}", file=sys.stderr)

        # Get existing db documents
        db_docs = {}
        cursor = self.conn.cursor()
        cursor.execute("SELECT path, file_hash FROM documents")
        for row in cursor.fetchall():
            db_docs[row["path"]] = row["file_hash"]

        # Delete documents no longer on disk
        for db_path in list(db_docs.keys()):
            if db_path not in disk_docs:
                with self.conn:
                    self.conn.execute("DELETE FROM documents WHERE path = ?", (db_path,))
                    print(f"[SQLITE INDEX] Removed deleted doc from index: {db_path}", file=sys.stderr)

        # Insert or update documents
        for doc_path, meta in disk_docs.items():
            db_hash = db_docs.get(doc_path)
            file_hash = meta.get("file_hash")
            
            if force or db_hash != file_hash:
                print(f"[SQLITE INDEX] Indexing document: {meta['document_name']}...", file=sys.stderr)
                with self.conn:
                    # Insert document
                    self.conn.execute("""
                        INSERT OR REPLACE INTO documents 
                        (path, name, clean_name, category, document_type, epistemic_grade, file_hash, processed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        doc_path,
                        meta["document_name"],
                        meta["document_clean_name"],
                        meta["category"],
                        meta["document_type"],
                        meta["epistemic_grade"],
                        file_hash,
                        meta["processed_at"]
                    ))
                    
                    # Delete existing chunks for this doc first to prevent orphans
                    self.conn.execute("DELETE FROM chunks WHERE document_path = ?", (doc_path,))
                    
                    # Parse and insert chunks
                    doc_dir_path = Path(doc_path)
                    for chunk_meta in meta.get("chunks", []):
                        chunk_file_path = doc_dir_path / chunk_meta["filename"]
                        if chunk_file_path.exists():
                            try:
                                with open(chunk_file_path, "r", encoding="utf-8") as f_chk:
                                    chk_content = f_chk.read()
                                
                                self.conn.execute("""
                                    INSERT INTO chunks 
                                    (path, document_path, chunk_index, filename, content, start_line, end_line)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    str(chunk_file_path),
                                    doc_path,
                                    chunk_meta["chunk_index"],
                                    chunk_meta["filename"],
                                    chk_content,
                                    chunk_meta["start_line"],
                                    chunk_meta["end_line"]
                                ))
                            except Exception as e:
                                print(f"[SQLITE INDEX] Error indexing chunk {chunk_file_path.name}: {e}", file=sys.stderr)
        
        print("[SQLITE INDEX] Sync complete.", file=sys.stderr)

    def search(self, query: str = None, category: str = None) -> list:
        """Executes search against indexed SQLite database."""
        cursor = self.conn.cursor()
        
        sql = """
            SELECT c.path, c.filename, c.content, c.chunk_index,
                   d.name as doc_name, d.category, d.document_type, d.epistemic_grade
            FROM chunks c
            JOIN documents d ON c.document_path = d.path
            WHERE 1=1
        """
        params = []
        
        if category:
            sql += " AND d.category = ?"
            params.append(category.lower())
            
        if query:
            sql += " AND c.content LIKE ?"
            params.append(f"%{query}%")
            
        cursor.execute(sql, params)
        results = []
        for r in cursor.fetchall():
            results.append({
                "path": r["path"],
                "filename": r["filename"],
                "content": r["content"],
                "chunk_index": r["chunk_index"],
                "doc_name": r["doc_name"],
                "category": r["category"],
                "document_type": r["document_type"],
                "epistemic_grade": r["epistemic_grade"]
            })
        return results


def run_macos_spotlight_search(query: str = None, category: str = None) -> list:
    """Spotlight query on macOS."""
    if not CHUNKS_DIR.exists():
        return []

    # Build mdfind query string
    parts = []
    if category:
        parts.append(f"kMDItemKeywords == '{category.lower()}'")
    if query:
        parts.append(f"kMDItemTextContent == '*{query}*'")
        
    mdfind_query = " && ".join(parts) if parts else ""
    
    cmd = ["mdfind", "-onlyin", str(CHUNKS_DIR)]
    if mdfind_query:
        cmd.append(mdfind_query)
        
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        filepaths = [Path(line) for line in res.stdout.splitlines() if line.strip() and line.endswith(".txt")]
    except Exception as e:
        print(f"[SPOTLIGHT] Warning: mdfind failed: {e}. Falling back to SQLite.", file=sys.stderr)
        return None

    results = []
    for fp in filepaths:
        if fp.exists():
            try:
                # Read content and parse headers
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
                
                meta = parse_yaml_header(content)
                doc_name = meta.get("source_file", fp.parent.name)
                
                results.append({
                    "path": str(fp),
                    "filename": fp.name,
                    "content": content,
                    "chunk_index": int(meta.get("chunk_index", 1)),
                    "doc_name": doc_name,
                    "category": fp.parent.parent.name,
                    "document_type": meta.get("document_type", ""),
                    "epistemic_grade": meta.get("epistemic_grade", "")
                })
            except Exception as e:
                # Silently skip read errors
                pass
    return results


def compile_logic_sandwich(results: list, query: str = None) -> dict:
    """Sorts and packages matches into the structured U-Curve Logic Sandwich.
    
    Format:
    1. Top Edge: Constraints & Laws (Doctrine/Rules)
    2. Middle: Content (Facts/General Research/Briefs)
    3. Bottom Edge: Methodology & Rubrics (Formulas/Hypotheses/Logical templates)
    """
    top_edge = []
    middle = []
    bottom_edge = []
    
    for r in results:
        cat = r["category"]
        doc_type = r["document_type"]
        content_lower = r["content"].lower()
        
        # 1. Top Edge: Doctrine and Rules
        if cat in AUTHORITY_CATEGORIES:
            top_edge.append(r)
            
        # 3. Bottom Edge: Methodology, Formulas, Rubrics
        elif (cat == "research" and (
            doc_type in ("hypothesis", "research_conclusion") or 
            any(w in content_lower for w in ("formula", "rubric", "calculation", "methodology", "z-score", "theory of constraints"))
        )):
            bottom_edge.append(r)
            
        # 2. Middle: General raw content and briefs
        else:
            middle.append(r)

    # Sort each list by relevance or naming logic (Top first/End last)
    # Simple sort helper: prioritize match count if query exists
    def sort_by_relevance(item):
        if not query:
            return item["filename"]
        q_lower = query.lower()
        matches = item["content"].lower().count(q_lower)
        # Sort descending by match count
        return -matches

    top_edge.sort(key=sort_by_relevance)
    middle.sort(key=sort_by_relevance)
    bottom_edge.sort(key=sort_by_relevance)

    # Apply U-Curve attention distribution within the components:
    # We want top 1st and top 2nd items at the edges of their respective list
    def apply_u_curve(item_list):
        if len(item_list) <= 2:
            return item_list
        # Reorder to: [Top 1, Top 3, Top 5, ..., Top 4, Top 2]
        ordered = []
        left = True
        for item in item_list:
            if left:
                ordered.append(item)
            else:
                ordered.insert(len(ordered) - len(ordered)//2, item)
            left = not left
        return ordered

    return {
        "top_edge": apply_u_curve(top_edge),
        "middle": apply_u_curve(middle),
        "bottom_edge": apply_u_curve(bottom_edge)
    }


def format_text_output(sandwich: dict) -> str:
    """Formats the compiled Logic Sandwich into structured, AI-readable Markdown."""
    lines = []
    lines.append("# Compiled Context Ingestion — The Logic Sandwich\n")
    lines.append("> [!IMPORTANT]")
    lines.append("> This context has been deterministically structured to place governing rules and methodology templates at the edges of positional attention. Apply the methodology at the bottom to the facts in the middle, respecting the constraints at the top.\n")
    
    # 1. Top Edge
    lines.append("## === SECTION I: GOVERNING AUTHORITY & CONSTRAINTS (TOP EDGE) ===")
    if sandwich["top_edge"]:
        for item in sandwich["top_edge"]:
            lines.append(f"### [RULE] {item['doc_name']} (Chunk {item['chunk_index']} — Grade: {item['epistemic_grade']})")
            lines.append(f"**Canonical Path:** `{item['path']}`")
            lines.append("```yaml")
            lines.append(item["content"].strip())
            lines.append("```\n")
    else:
        lines.append("*No governing constraints found for this query.*\n")
        
    # 2. Middle
    lines.append("## === SECTION II: CONTEXT DATA & SUBJECT MATTER (MIDDLE VALLEY) ===")
    if sandwich["middle"]:
        for item in sandwich["middle"]:
            lines.append(f"### [DATA] {item['doc_name']} (Chunk {item['chunk_index']} — Grade: {item['epistemic_grade']})")
            lines.append(f"**Canonical Path:** `{item['path']}`")
            lines.append("```markdown")
            # Strip YAML block to save tokens if it's general data
            content_stripped = item["content"]
            if content_stripped.startswith("---"):
                parts = content_stripped.split("---", 2)
                if len(parts) >= 3:
                    content_stripped = parts[2].strip()
            lines.append(content_stripped)
            lines.append("```\n")
    else:
        lines.append("*No subject data found for this query.*\n")

    # 3. Bottom Edge
    lines.append("## === SECTION III: METHODOLOGY, FORMULAS & RUBRICS (BOTTOM EDGE) ===")
    if sandwich["bottom_edge"]:
        for item in sandwich["bottom_edge"]:
            lines.append(f"### [METHODOLOGY] {item['doc_name']} (Chunk {item['chunk_index']} — Grade: {item['epistemic_grade']})")
            lines.append(f"**Canonical Path:** `{item['path']}`")
            lines.append("```yaml")
            lines.append(item["content"].strip())
            lines.append("```\n")
    else:
        lines.append("*No execution methodologies found for this query.*\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Unified search interface for the structured data lake.")
    parser.add_argument("--query", type=str, default=None, help="The query search string.")
    parser.add_argument("--category", type=str, default=None, help="Category mapping filter.")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results.")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild SQLite cache on Linux.")
    args = parser.parse_args()

    results = None
    
    # 1. If on macOS, attempt native Spotlight search
    if sys.platform == "darwin" and not args.rebuild:
        results = run_macos_spotlight_search(args.query, args.category)

    # 2. Fallback to SQLite (or if forced on Linux)
    if results is None:
        db_index = SQLiteSearchIndex()
        # Always run sync to capture updates
        db_index.sync(force=args.rebuild)
        results = db_index.search(args.query, args.category)

    # 3. Compile the Logic Sandwich
    sandwich = compile_logic_sandwich(results, args.query)
    
    # 4. Output results
    if args.json:
        # Format JSON structure cleanly
        output = {
            "query": args.query,
            "category_filter": args.category,
            "total_matches": len(results),
            "sandwich": {
                "top_edge": [
                    {k: v for k, v in item.items() if k != "content"} for item in sandwich["top_edge"]
                ],
                "middle": [
                    {k: v for k, v in item.items() if k != "content"} for item in sandwich["middle"]
                ],
                "bottom_edge": [
                    {k: v for k, v in item.items() if k != "content"} for item in sandwich["bottom_edge"]
                ]
            }
        }
        print(json.dumps(output, indent=2))
    else:
        # Output structured Markdown logic sandwich
        print(format_text_output(sandwich))


if __name__ == "__main__":
    main()
