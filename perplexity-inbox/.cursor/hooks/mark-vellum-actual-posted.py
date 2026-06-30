#!/usr/bin/env python3
"""Mark Vellum ACTUAL appended. Usage: mark-vellum-actual-posted.py <entry_id>"""
from __future__ import annotations

import os
import sys

root = os.environ.get("AMPLIFIED_INBOX", os.path.expanduser("~/ingestion-to-research-pipe/perplexity-inbox"))
sys.path.insert(0, root)
from harness.vellum_session import mark_actual  # noqa: E402

if __name__ == "__main__":
    eid = sys.argv[1] if len(sys.argv) > 1 else ""
    mark_actual(eid)
    print(f"actual marked entry_id={eid}")
