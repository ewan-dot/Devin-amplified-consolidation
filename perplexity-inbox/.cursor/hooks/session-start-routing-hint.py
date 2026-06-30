#!/usr/bin/env python3
"""sessionStart — inject fleet routing slice + optional Vellum routing hint."""
from __future__ import annotations

import json
import os
import sys


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    root = os.environ.get("AMPLIFIED_INBOX", os.path.expanduser("~/ingestion-to-research-pipe/perplexity-inbox"))
    sys.path.insert(0, root)
    try:
        from harness.routing_manifest import session_hint_text, vellum_routing_from_marker
    except ImportError:
        print("{}")
        return

    parts = [session_hint_text("cursor")]
    vellum_hint = vellum_routing_from_marker()
    if vellum_hint:
        parts.append(f"[vellum-routing-hint] {json.dumps(vellum_hint, separators=(',', ':'))}")

    text = "\n".join(p for p in parts if p).strip()
    if not text:
        print("{}")
        return
    print(json.dumps({"additional_context": text}))


if __name__ == "__main__":
    main()
