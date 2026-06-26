#!/usr/bin/env python3
"""stop — one compact nudge per session at ~60% transcript size."""
import hashlib
import json
import os
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")
SEEN_DIR = os.path.expanduser("~/.amplified/logs/stop-nudge-seen")


def witness(ok, note):
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps({"ts": time.time(), "hook": "stop-nudge", "ok": ok, "note": note})
                + "\n"
            )
    except Exception:
        pass


def main():
    try:
        data = json.load(sys.stdin)
        tp = data.get("transcript_path")
        sid = data.get("session_id") or (os.path.basename(tp) if tp else "nosession")
        sentinel = os.path.join(SEEN_DIR, hashlib.sha256(str(sid).encode()).hexdigest()[:16])
        if os.path.exists(sentinel):
            print("{}")
            witness(True, "already nudged")
            return
        if tp and os.path.exists(tp):
            util = os.path.getsize(tp) / 800_000
            if util > 0.60:
                os.makedirs(SEEN_DIR, exist_ok=True)
                open(sentinel, "w", encoding="utf-8").close()
                print(
                    json.dumps(
                        {
                            "followup_message": (
                                f"[ctx ~{int(util * 100)}%] Consider summarising open task + file list "
                                "before the next long turn. Finish-waypoint + relay-stop still apply on handoff."
                            )
                        }
                    )
                )
                witness(True, f"nudge {int(util * 100)}%")
                return
        print("{}")
        witness(True, "no nudge")
    except Exception as exc:
        print("{}")
        witness(False, f"error: {exc}")


if __name__ == "__main__":
    main()
