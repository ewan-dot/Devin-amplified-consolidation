#!/usr/bin/env python3
"""CLI — run shape gate on a file (Antigravity verification loop + manual bee)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HARNESS.parent))

from harness.shape_gate import check_file, emit_verdict  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="Shape gate — tier arithmetic at boundary")
    p.add_argument("--path", required=True, help="File path to check")
    p.add_argument("--seat", default="antigravity", help="Seat identity (cursor, claude, antigravity, …)")
    args = p.parse_args()
    denies, fm = check_file(args.path, args.seat)
    raise SystemExit(emit_verdict(denies, args.path, fm, args.seat, hook_name="shape-gate-cli"))


if __name__ == "__main__":
    main()
