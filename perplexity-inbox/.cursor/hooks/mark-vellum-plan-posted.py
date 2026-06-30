#!/usr/bin/env python3
"""Mark Vellum PLAN posted. Usage: mark-vellum-plan-posted.py <entry_id> [seat]"""
from __future__ import annotations

import os
import sys

root = os.environ.get("AMPLIFIED_INBOX", os.path.expanduser("~/ingestion-to-research-pipe/perplexity-inbox"))
sys.path.insert(0, root)
from harness.vellum_session import mark_plan  # noqa: E402

if __name__ == "__main__":
    eid = sys.argv[1] if len(sys.argv) > 1 else ""
    seat = sys.argv[2] if len(sys.argv) > 2 else "cursor"
    mark_plan(eid, seat)
    print(f"plan marked entry_id={eid}")
