"""
night_scout.py — the dual-purpose Night Scout feed handoff.

The brief is BOTH an implementation order AND a Night Scout feed item. The
implementing agent must place a copy of the brief into the scout feed so overnight
scouts watch for new public prior art on the synthesis.

Resolution (recorded per the brief's "ask once / record the resolved path"):
  - Canonical sink = Beast APDS staging /opt/amplified-machine/apds/staging/ —
    NOT present on M5 (Beast-only). Deferred: needs Beast access.
  - The referenced code ~/clean-build/02_build/cove-orchestrator/nightscout/ is
    also not on M5.
  => M5-local feed mirror created at perplexity-inbox/night-scout-feed/. When the
     Beast path is reachable, sync this mirror -> APDS staging (one rsync; see
     CHECKLIST-go-live.md). Implementation and scout-routing are independent
     (brief §"Do not block implementation on the scout routing").
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from .config import BEAST_APDS_STAGING, NIGHT_SCOUT_FEED_DIR


SCOUT_TAGS = ["email-triage", "mcp-code-execution", "token-efficiency",
              "multi-inbox", "actioning-not-replying"]

WATCHLIST = [
    "new public prior art on Claude/MCP email-actioning systems",
    "new publications on token-efficient multi-inbox triage",
    "anyone publishing the (code-execution + tiered-routing + private-ingestion) synthesis",
    "re-ingest this brief as a brain artifact under scout_tags",
]


def route_brief_to_feed(brief_path: str | Path,
                        feed_dir: str | Path = NIGHT_SCOUT_FEED_DIR) -> dict:
    """Copy the brief into the M5 scout feed and write a watch manifest beside it.
    Returns a record of what was done (and what is deferred to Beast)."""
    brief_path = Path(brief_path)
    feed_dir = Path(feed_dir)
    feed_dir.mkdir(parents=True, exist_ok=True)

    copied = feed_dir / brief_path.name
    if brief_path.exists():
        shutil.copy2(brief_path, copied)

    manifest = {
        "feed_item": brief_path.name,
        "scout_tags": SCOUT_TAGS,
        "watchlist": WATCHLIST,
        "tier": "INTUITED",
        "canonical_sink": BEAST_APDS_STAGING,
        "canonical_sink_status": "deferred — Beast-only, not reachable from M5 this session",
        "m5_mirror": str(feed_dir),
    }
    (feed_dir / "WATCH-MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    manifest["copied_to"] = str(copied) if brief_path.exists() else None
    return manifest
