#!/usr/bin/env python3
"""sessionStart — inject latest Antigravity baton from portable-spine agents/antigravity/."""
from __future__ import annotations

import json
import os
import sys

def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    baton_path = os.path.expanduser("~/portable-spine/agents/antigravity/BATON.md")
    if not os.path.isfile(baton_path):
        print("{}")
        return

    try:
        with open(baton_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except OSError:
        print("{}")
        return

    if not content:
        print("{}")
        return

    # Truncate content to keep within safety bounds for additional_context
    max_chars = 8000
    if len(content) > max_chars:
        content = content[:max_chars] + "\n...(truncated)"

    output = f"[antigravity-baton] latest={baton_path}\n{content}"
    print(json.dumps({"additional_context": output}))

if __name__ == "__main__":
    main()
