#!/usr/bin/env python3
"""beforeShellExecution — nudge token-bomb commands. Fail-open + witnessed (push door)."""
import json
import os
import re
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")
_CMD = r"(?:^|[;&|\n(]|&&|\|\|)\s*"
BLOCK = [
    (
        re.compile(_CMD + r"find\s+\S+\s+(?!.*-(?:maxdepth|prune|name|path))"),
        "Unbounded find blows context — add -maxdepth N or use rg --files -g 'pat'.",
    ),
    (
        re.compile(_CMD + r"cat\s+\S*\.(?:lock|min\.js|map)\b"),
        "Refusing to cat a lockfile/minified/map — use rg or head.",
    ),
    (re.compile(_CMD + r"tree\b(?![^\n;&|]*-L)"), "Use tree -L 2/3 — unbounded tree is a token bomb."),
    (
        re.compile(_CMD + r"npm\s+ls\b(?![^\n;&|]*--depth)"),
        "Use npm ls --depth 0.",
    ),
]


def witness(ok, note):
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"ts": time.time(), "hook": "pre-bash-guard", "ok": ok, "note": note}
                )
                + "\n"
            )
    except Exception:
        pass


def _strip_literals(cmd):
    cmd = re.sub(r"<<-?\s*['\"]?\w+['\"]?.*", " ", cmd, flags=re.S)
    cmd = re.sub(r"'[^']*'", " ", cmd)
    cmd = re.sub(r'"[^"]*"', " ", cmd)
    return cmd


def main():
    try:
        data = json.load(sys.stdin)
    except Exception as exc:
        print('{"permission":"allow"}')
        witness(False, f"stdin parse error: {exc}")
        return

    cmd = data.get("command") or (data.get("tool_input") or {}).get("command") or ""
    try:
        scan = _strip_literals(cmd)
        for pat, reason in BLOCK:
            if pat.search(scan):
                print(
                    json.dumps(
                        {
                            "permission": "allow",
                            "user_message": reason,
                            "agent_message": f"beforeShellExecution: {reason} — proceed if intentional (push door).",
                            "additional_context": f"[bash-nudge] {reason}",
                        }
                    )
                )
                witness(True, f"nudge: {cmd[:80]}")
                return
        print('{"permission":"allow"}')
        witness(True, f"allow: {cmd[:80]}")
    except Exception as exc:
        print('{"permission":"allow"}')
        witness(False, f"guard error: {exc}")


if __name__ == "__main__":
    main()
