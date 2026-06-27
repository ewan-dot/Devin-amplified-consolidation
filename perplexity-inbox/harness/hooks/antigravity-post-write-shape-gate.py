#!/usr/bin/env python3
"""Antigravity post-write adapter — shape gate (stdin or --path)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HARNESS.parent))

from harness.shape_gate import check_content, check_file, emit_verdict, witness  # noqa: E402

SEAT = "antigravity"


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--path":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        if not path:
            sys.exit(1)
        denies, fm = check_file(path, SEAT)
        sys.exit(emit_verdict(denies, path, fm, SEAT, hook_name="antigravity-shape-gate"))

    try:
        event = json.loads(sys.stdin.read() or "{}")
    except Exception:
        witness("antigravity-shape-gate", "parse-error", True, {"note": "stdin parse failed"})
        sys.exit(0)

    path = event.get("file_path") or event.get("path") or ""
    content = event.get("content") or event.get("new_content") or ""
    if not path:
        witness("antigravity-shape-gate", "no-path", True, {})
        sys.exit(0)

    if content:
        denies, fm = check_content(content, path, SEAT)
    else:
        denies, fm = check_file(path, SEAT)

    sys.exit(emit_verdict(denies, path, fm, SEAT, hook_name="antigravity-shape-gate"))


if __name__ == "__main__":
    main()
