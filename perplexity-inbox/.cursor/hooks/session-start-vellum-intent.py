#!/usr/bin/env python3
"""sessionStart — PLAN to Vellum before any substantive work."""
from __future__ import annotations

import json
import os
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")

MSG = (
    "[vellum-plan] STOP — post PLAN to Vellum before any work (author=cursor, INTUITED). "
    "Fields: goal, 3–5 steps, owners, VERDICT= from sensor after this message. "
    "Then: python3 ~/.cursor/hooks/mark-vellum-plan-posted.py <entry_id>. "
    "On seat close: append ACTUAL to same thread (plan entry_id + done/blocked/delta)."
)


def witness(ok: bool, note: str) -> None:
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps({"ts": time.time(), "hook": "session-start-vellum-plan", "ok": ok, "note": note})
                + "\n"
            )
    except OSError:
        pass


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    root = os.environ.get("AMPLIFIED_INBOX", os.path.expanduser("~/ingestion-to-research-pipe/perplexity-inbox"))
    sys.path.insert(0, root)
    try:
        from harness.vellum_session import plan_posted_recently  # noqa: E402
    except ImportError:
        print(json.dumps({"additional_context": MSG}))
        witness(True, "nudge (no vellum_session)")
        return

    if plan_posted_recently():
        print("{}")
        witness(True, "plan posted recently")
        return

    print(json.dumps({"additional_context": MSG}))
    witness(True, "nudge plan post")


if __name__ == "__main__":
    main()
