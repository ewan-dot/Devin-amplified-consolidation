#!/usr/bin/env python3
"""sessionStart — require Vellum intent post before substantive seat work.

Witnesses to ~/.amplified/logs/harness-hooks.jsonl.
Outputs additional_context for the agent (not a hard block — pre_client).
"""
from __future__ import annotations

import json
import os
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")
MARKER = os.path.expanduser("~/.amplified/logs/vellum-intent-posted.json")
SESSION_HOURS = 8

MSG = (
    "[vellum-intent] Before substantive work: post plan to Vellum (author=cursor, tier=INTUITED). "
    "Include: artefact IDs, registry rows (docs/OWNERSHIP-REGISTRY.md), 3–5 step plan, owners. "
    "Paste VERDICT= line from session-start. See vellum-witness.mdc."
)


def witness(ok: bool, note: str) -> None:
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"ts": time.time(), "hook": "session-start-vellum-intent", "ok": ok, "note": note}
                )
                + "\n"
            )
    except OSError:
        pass


def recent_intent_posted() -> bool:
    try:
        if not os.path.isfile(MARKER):
            return False
        with open(MARKER, encoding="utf-8") as f:
            data = json.load(f)
        ts = float(data.get("ts", 0))
        return (time.time() - ts) < SESSION_HOURS * 3600
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return False


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    if recent_intent_posted():
        print("{}")
        witness(True, "intent posted recently")
        return

    print(json.dumps({"additional_context": MSG}))
    witness(True, "nudge intent post")


if __name__ == "__main__":
    main()
