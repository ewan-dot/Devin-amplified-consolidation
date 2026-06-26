"""
emit.py — structured JSONL emitters (Tier A, inbox-local).

The brief's next executable step: "route INFRA_CRITICAL into perplexity-inbox as
JSONL". Emitting structured rows into the inbox SSOT is a Tier A action (reversible,
local) — it runs without a human gate. Beast/brain ingestion happens DOWNSTREAM by
the existing pipe reading these files; we never write to Beast directly.
"""
from __future__ import annotations

import json
from pathlib import Path


def write_jsonl(path: str | Path, rows: list[dict]) -> int:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)


def emit_infra_feed(path: str | Path, classifications, emails_by_id) -> int:
    """INFRA_CRITICAL rows -> JSONL sink the pipe ingests. Includes enough to act
    on (full body retained here in the file, not in model context)."""
    rows = []
    for c in classifications:
        if c.category != "INFRA_CRITICAL":
            continue
        e = emails_by_id.get(c.msg_id)
        rows.append({
            "msg_id": c.msg_id, "inbox": c.inbox, "category": c.category,
            "confidence": round(c.confidence, 3), "signals": c.signals,
            "subject": (e.subject if e else ""), "sender": (e.sender if e else ""),
            "body": (e.body if e else ""),
            "_tier": "INTUITED", "_sink": "beast-ingestion-pipe (via perplexity-inbox)",
        })
    return write_jsonl(path, rows)
