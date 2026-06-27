#!/usr/bin/env python3
"""Claude Code PostToolUse adapter — shape gate on Write|Edit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HARNESS.parent))

from harness.shape_gate import check_content, emit_verdict, witness  # noqa: E402

SEAT = "claude"


def main() -> None:
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except Exception:
        witness("pre-ingest-tier-gate", "parse-error", True, {"note": "stdin parse failed"})
        sys.exit(0)

    tool = event.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        witness("pre-ingest-tier-gate", "skip", True, {"tool": tool})
        sys.exit(0)

    tool_input = event.get("tool_input", {})
    path = tool_input.get("file_path", "") or ""
    content = tool_input.get("content", "") or ""
    if not content:
        witness("pre-ingest-tier-gate", "no-content", True, {"path": path})
        sys.exit(0)

    denies, fm = check_content(content, path, SEAT)
    sys.exit(emit_verdict(denies, path, fm, SEAT, hook_name="pre-ingest-tier-gate"))


if __name__ == "__main__":
    main()
