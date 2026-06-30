#!/usr/bin/env python3
"""Utility — mark that this seat posted Vellum intent (call after successful Vellum write).

Usage: python3 mark-vellum-intent-posted.py [entry_id]
"""
from __future__ import annotations

import json
import os
import sys
import time

MARKER = os.path.expanduser("~/.amplified/logs/vellum-intent-posted.json")


def main() -> None:
    entry_id = sys.argv[1] if len(sys.argv) > 1 else ""
    os.makedirs(os.path.dirname(MARKER), exist_ok=True)
    with open(MARKER, "w", encoding="utf-8") as f:
        json.dump({"ts": time.time(), "seat": "cursor", "entry_id": entry_id}, f)
    print(f"marked: {MARKER}")


if __name__ == "__main__":
    main()
