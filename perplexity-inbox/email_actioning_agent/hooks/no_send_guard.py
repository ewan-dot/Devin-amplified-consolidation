#!/usr/bin/env python3
"""
no_send_guard.py — deterministic guard hook.

Fails (exit 1) if the package source introduces a live outbound-send / payment /
hard-delete path. The brief is *actioning, not replying*: there must be no code
that sends email, follows financial links, or hard-deletes. Tier C stays gated.

Run standalone or from a pre-commit hook. Scans tracked .py under the package.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
# Forbidden live-effect call shapes. gmail_mcp.py documents label/archive only.
FORBIDDEN = [
    (r"\bsend_draft\b", "outbound email send"),
    (r"\bsend_message\b\s*\(", "outbound message send"),
    (r"create_draft\([^)]*\bsend\b", "draft-then-send"),
    (r"\btrash_thread\b|\bdelete_message\b|hard[_-]?delete", "destructive delete"),
    (r"requests?\.(get|post)\(\s*[\"']https?://(?:notifylink|billing|ablink)", "following a financial/tracking link"),
]
ALLOW_COMMENT = re.compile(r"^\s*#|\"\"\"|'''")


def scan() -> list[str]:
    violations = []
    for py in PKG.rglob("*.py"):
        if "hooks/no_send_guard.py" in str(py):
            continue
        for i, line in enumerate(py.read_text(encoding="utf-8").splitlines(), 1):
            if ALLOW_COMMENT.match(line):
                continue
            for pat, why in FORBIDDEN:
                if re.search(pat, line):
                    violations.append(f"{py.relative_to(PKG.parent)}:{i}: {why} -> {line.strip()}")
    return violations


def main() -> int:
    v = scan()
    if v:
        print("no_send_guard: FORBIDDEN live-effect path(s) detected:", file=sys.stderr)
        for x in v:
            print("  " + x, file=sys.stderr)
        print("Tier C actions must stay gated (decision-only). Remove the live call.", file=sys.stderr)
        return 1
    print("no_send_guard: OK — no live send/pay/delete path in package source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
