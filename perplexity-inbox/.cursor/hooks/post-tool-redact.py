#!/usr/bin/env python3
"""postToolUse — truncate noisy tool output when Cursor honours rewrite fields."""
import json
import os
import re
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")
MAX, HEAD, TAIL = 6000, 2000, 2000
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
NOISE = re.compile(r"(node_modules/|\.next/cache/|target/debug/|__pycache__/)")


def witness(ok, note):
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"ts": time.time(), "hook": "post-tool-redact", "ok": ok, "note": note}
                )
                + "\n"
            )
    except Exception:
        pass


def main():
    try:
        data = json.load(sys.stdin)
        resp = data.get("tool_response") or data.get("output") or ""
        text = resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False)
        text = ANSI.sub("", text)
        text = "\n".join(line for line in text.splitlines() if not NOISE.search(line))
        if len(text) <= MAX:
            print("{}")
            witness(True, "passthrough")
            return
        elided = len(text) - HEAD - TAIL
        redacted = (
            f"{text[:HEAD]}\n\n[... {elided} chars elided by post-tool-redact ...]\n\n{text[-TAIL:]}"
        )
        # Cursor may only honour additional_context for non-MCP tools; emit both shapes fail-open.
        print(
            json.dumps(
                {
                    "additional_context": f"[post-tool-redact] Output truncated ({len(text)} -> {len(redacted)} chars).",
                    "updated_tool_output": redacted,
                }
            )
        )
        witness(True, f"redacted {len(text)} -> {len(redacted)}")
    except Exception as exc:
        print("{}")
        witness(False, f"error: {exc}")


if __name__ == "__main__":
    main()
