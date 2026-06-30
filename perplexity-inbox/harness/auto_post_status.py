#!/usr/bin/env python3
import os
import sys
import json
import glob
import ssl
import jwt
import uuid
import hashlib
import subprocess
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Paths
BRAIN_DIR = Path("/Users/ewansair/.gemini/antigravity/brain")
BATON_FILE = Path("/Users/ewansair/portable-spine/agents/antigravity/BATON.md")
VELLUM_URL = "https://vellum.beast.amplifiedpartners.ai"
VELLUM_JWT_SECRET = "vellum-dogfood-2026-scaffold"

def get_active_conv_id():
    meta = os.environ.get("ANTIGRAVITY_SOURCE_METADATA")
    if meta:
        try:
            data = json.loads(meta)
            conv_id = data.get("tool", {}).get("conversationId")
            if conv_id:
                return conv_id
        except Exception:
            pass
    # Fallback to latest modified folder
    folders = glob.glob(str(BRAIN_DIR / "*"))
    folder_mtimes = []
    for f in folders:
        if os.path.basename(f) == "tempmediaStorage":
            continue
        tp = Path(f) / ".system_generated" / "logs" / "transcript.jsonl"
        if tp.exists():
            folder_mtimes.append((tp.stat().st_mtime, os.path.basename(f)))
    if folder_mtimes:
        folder_mtimes.sort(reverse=True)
        return folder_mtimes[0][1]
    return None

def make_token(sheet_id: str, role: str = "write") -> str:
    return jwt.encode(
        {
            "jti": str(uuid.uuid4()),
            "sub": "mcp-agent",
            "sheet_id": sheet_id,
            "role": role,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        },
        VELLUM_JWT_SECRET,
        algorithm="HS256",
    )

def api_post(path: str, body: dict, token: str = None) -> dict:
    data = json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"{VELLUM_URL}{path}",
        data=data,
        headers=headers,
        method="POST"
    )
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=10, context=context) as resp:
        return json.loads(resp.read().decode())

def run_cmd(cmd: list, cwd: str) -> str:
    try:
        res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    conv_id = get_active_conv_id()
    if not conv_id:
        print("No active conversation found.", file=sys.stderr)
        sys.exit(1)

    print(f"Active Conversation ID: {conv_id}")
    conv_folder = BRAIN_DIR / conv_id
    transcript_path = conv_folder / ".system_generated" / "logs" / "transcript.jsonl"
    walkthrough_path = conv_folder / "walkthrough.md"

    first_prompt = "Unknown prompt"
    walkthrough_lines = []

    # 1. Parse transcript for first prompt
    if transcript_path.exists():
        with open(transcript_path, "r", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if data.get("type") == "USER_INPUT":
                        content = data.get("content", "")
                        if content:
                            first_prompt = content.strip().replace("\n", " ")[:150]
                            break
                except Exception:
                    pass

    # 2. Parse walkthrough
    if walkthrough_path.exists():
        with open(walkthrough_path, "r", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                if stripped and (stripped.startswith("#") or stripped.startswith("-") or stripped.startswith("*")):
                    walkthrough_lines.append(f"  - \"{stripped}\"")
                if len(walkthrough_lines) >= 8:
                    break

    # 3. Get Git repository details
    repo_path = "/Users/ewansair/ingestion-to-research-pipe"
    branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_path)
    status = run_cmd(["git", "status", "--porcelain"], repo_path)
    last_commit = run_cmd(["git", "log", "-n", "1", "--oneline"], repo_path)

    git_summary = f"Branch: {branch}\nLast Commit: {last_commit}"
    if status:
        git_summary += f"\nModified Files:\n{status}"
    else:
        git_summary += "\nWorking directory clean."

    # 4. Format Baton Output
    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    baton_content = f"""---
title: "Session Baton — {date_str} — {conv_id[:8]}"
document_type: "baton"
date: "{date_str}"
from_agent: "antigravity"
to_agent: "next instance"
epistemic_grade: "STRUCTURED"

load_bearing:
  - "Thread initial prompt: {first_prompt}"
"""
    if walkthrough_lines:
        baton_content += "  - \"Thread Walkthrough/Actions:\"\n" + "\n".join(walkthrough_lines) + "\n"
    
    baton_content += f"""
open_items:
  - item: "Git Workspace Sync"
    priority: "medium"
    context: "{git_summary.replace(chr(10), ' | ')}"

read_first:
  - "/Users/ewansair/ingestion-to-research-pipe/COMPLETE_SYSTEM_SPEC.md"
  - "/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/ESTATE-TAXONOMY.md"
  - "/Users/ewansair/ingestion-to-research-pipe/AGENTS.md"

next_action:
  immediate: "Check active branches and proceed with governed worker registration"
  rationale: "Align with Ewan's roadmap for compile-time gates"

session_summary: "Automated status sync run for thread {conv_id}."
warnings: []
---
"""

    # 5. Write to local BATON.md
    try:
        BATON_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(BATON_FILE, "w") as f:
            f.write(baton_content)
        print(f"Successfully updated local baton at {BATON_FILE}")
    except Exception as e:
        print(f"Failed to write local baton: {e}", file=sys.stderr)

    # 6. Post to Vellum
    print("Posting update to Vellum estate log...")
    token = make_token("estate-status", "write")
    payload = {
        "author": "antigravity",
        "content": baton_content,
        "metadata": {
            "repo": "ingestion-to-research-pipe",
            "action": "auto-sync-status",
            "pr": "none"
        }
    }
    try:
        res = api_post("/api/v1/estate/log", payload, token)
        print("Vellum sync logged successfully:", res)
    except Exception as e:
        print(f"Failed to post to Vellum: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
