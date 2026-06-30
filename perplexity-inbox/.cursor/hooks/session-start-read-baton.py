#!/usr/bin/env python3
"""sessionStart — inject latest baton from batons/active/ (max 5 retained)."""
from __future__ import annotations

import json
import os
import subprocess
import sys


def inbox_root() -> str:
    env = os.environ.get("AMPLIFIED_INBOX", "").strip()
    if env and os.path.isdir(env):
        return env
    for candidate in (
        os.path.expanduser("~/ingestion-to-research-pipe/perplexity-inbox"),
        os.path.expanduser("~/container on m5/perplexity-inbox"),
    ):
        if os.path.isdir(candidate):
            return candidate
    return env or ""


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    root = inbox_root()
    script = os.path.join(root, "harness", "baton_lifecycle.py")
    if not root or not os.path.isfile(script):
        print("{}")
        return

    try:
        out = subprocess.check_output(
            [sys.executable, script, "read"],
            text=True,
            timeout=5,
            env={**os.environ, "AMPLIFIED_INBOX": root},
        ).strip()
    except (subprocess.SubprocessError, OSError):
        print("{}")
        return

    if not out:
        print("{}")
        return
    print(json.dumps({"additional_context": out}))


if __name__ == "__main__":
    main()
