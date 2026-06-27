#!/usr/bin/env python3
"""Cursor afterFileEdit adapter — shape gate on Write."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HARNESS.parent))

from harness.shape_gate import check_content, check_file, emit_verdict, witness  # noqa: E402

SEAT = "cursor"


def _extract(event: dict) -> tuple[str, str]:
    path = (
        event.get("file_path")
        or event.get("path")
        or (event.get("tool_input") or {}).get("file_path")
        or ""
    )
    content = (
        event.get("content")
        or event.get("new_content")
        or (event.get("tool_input") or {}).get("content")
        or ""
    )
    return str(path), str(content)


def main() -> None:
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except Exception:
        witness("cursor-shape-gate", "parse-error", True, {"note": "stdin parse failed"})
        print("{}")
        sys.exit(0)

    path, content = _extract(event)
    if not path:
        witness("cursor-shape-gate", "no-path", True, {})
        print("{}")
        sys.exit(0)

    if content:
        denies, fm = check_content(content, path, SEAT)
    else:
        denies, fm = check_file(path, SEAT)

    emit_verdict(denies, path, fm, SEAT, hook_name="cursor-shape-gate")
    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
