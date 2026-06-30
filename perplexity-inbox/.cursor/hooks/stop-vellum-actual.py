#!/usr/bin/env python3
"""stop — nudge Vellum ACTUAL append when PLAN exists but ACTUAL missing."""
from __future__ import annotations

import json
import os
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")


def witness(ok: bool, note: str) -> None:
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps({"ts": time.time(), "hook": "stop-vellum-actual", "ok": ok, "note": note})
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
        from harness.vellum_session import actual_posted_for_current_plan, plan_entry_id, plan_posted_recently
    except ImportError:
        print("{}")
        return

    if not plan_posted_recently():
        print("{}")
        witness(True, "no plan this session")
        return

    if actual_posted_for_current_plan():
        print("{}")
        witness(True, "actual already posted")
        return

    pid = plan_entry_id()
    msg = (
        f"[vellum-actual] Append ACTUAL to Vellum — references plan entry_id={pid}. "
        "Include: done (verified), blocked, delta vs plan, GitHub push status. "
        "Then: python3 ~/.cursor/hooks/mark-vellum-actual-posted.py <actual_entry_id>. "
        "Push to GitHub before calling seat done."
    )
    print(json.dumps({"followup_message": msg}))
    witness(True, f"nudge actual plan={pid}")


if __name__ == "__main__":
    main()
