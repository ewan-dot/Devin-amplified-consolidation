#!/usr/bin/env python3
"""
hook_adapter.py — STAGED Cursor-hook adapter for the open-door harness.

=============================================================================
NOT WIRED. This file is referenced by NOTHING in the live ~/.cursor/hooks.json.
It exists so that activation is a single, reversible copy step (see ACTIVATION.md).
Behaviour is controlled by env OPEN_DOOR_MODE (default "scaffold" = pass-through):

    scaffold : always "allow" (advisory) — wiring this changes NO behaviour.
    nudge    : out-of-scope -> allow + nudge message (never blocks).
    deny     : out-of-scope -> "deny" for enforcing doors only; else nudge.

Door-independent hard lines (secrets, Red-core, git push) deny in every mode.
FAIL-OPEN: any error prints {"permission":"allow"} so a misconfig can never
wedge a Cursor session — mirroring the existing pre-bash-guard.py / before-read-file.sh.
=============================================================================

Usage (from a hook dispatcher):  echo "$INPUT" | python3 hook_adapter.py shell
                                 echo "$INPUT" | python3 hook_adapter.py read
"""
import importlib.util
import json
import os
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")


def _allow():
    print('{"permission":"allow"}')


def _witness(verdict, note):
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.time(), "hook": "open-door-adapter",
                                "verdict": verdict, "note": note}) + "\n")
    except Exception:
        pass


def _load_enforcement():
    spec = importlib.util.spec_from_file_location(
        "door_enforcement", os.path.join(_HERE, "door_enforcement.py"))
    mod = importlib.util.module_from_spec(spec)
    # Register before exec so @dataclass can resolve cls.__module__ (importlib gotcha).
    sys.modules["door_enforcement"] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    # Fail-open around EVERYTHING.
    try:
        event = sys.argv[1] if len(sys.argv) > 1 else "shell"
        raw = sys.stdin.read()
        try:
            data = json.loads(raw) if raw.strip() else {}
        except Exception:
            _allow(); _witness("allow", "stdin parse error -> fail-open"); return

        # Mode resolution order: env OPEN_DOOR_MODE -> ~/.amplified/open-door-mode -> "scaffold".
        # The file fallback lets Ewan flip staged->nudge->deny by editing one tiny file
        # (no env plumbing into Cursor, no restart). See ACTIVATION.md.
        mode = os.environ.get("OPEN_DOOR_MODE")
        if not mode:
            try:
                with open(os.path.expanduser("~/.amplified/open-door-mode"), "r", encoding="utf-8") as f:
                    mode = f.read().strip() or "scaffold"
            except FileNotFoundError:
                mode = "scaffold"
        enforcing_env = os.environ.get("OPEN_DOOR_ENFORCING", "")
        enforcing = [d.strip() for d in enforcing_env.split(",") if d.strip()] or None

        de = _load_enforcement()
        manifest = de.load_manifest()
        marker = de.load_marker()
        door = marker.get("door", "research_read")
        bindings = {
            "worktree_subtree": marker.get("worktree_subtree") or marker.get("subtree"),
            "project_subtree": marker.get("project_subtree") or marker.get("subtree"),
            "corpus_dir": marker.get("corpus_dir"),
            "pipe_run_dir": marker.get("pipe_run_dir"),
            "repo": marker.get("repo"),
        }

        if event == "read":
            path = data.get("path") or data.get("file_path") \
                or (data.get("tool_input") or {}).get("path") or ""
            if not path:
                _allow(); _witness("allow", "no path -> allow"); return
            action = {"kind": "fs_read", "path": path}
        else:  # shell
            cmd = data.get("command") or (data.get("tool_input") or {}).get("command") or ""
            if re.search(r"\bgit\s+push\b", cmd):
                action = {"kind": "git", "op": "push", "command": cmd}
            else:
                action = {"kind": "shell", "command": cmd}

        v = de.decide(action, door, manifest, mode=mode,
                      enforcing_doors=enforcing, bindings=bindings)

        if v.verdict == de.VERDICT_DENY:
            msg = f"[open-door:{door}] DENY — {v.reason}."
            if v.remedy:
                msg += f" Remedy: {v.remedy}."
            print(json.dumps({"permission": "deny", "user_message": msg,
                              "agent_message": msg}))
            _witness("deny", f"{door}: {v.rule}")
            return
        if v.verdict == de.VERDICT_NUDGE:
            msg = f"[open-door:{door}] {v.reason}." + (f" {v.remedy}." if v.remedy else "")
            print(json.dumps({"permission": "allow", "user_message": msg,
                              "additional_context": msg}))
            _witness("nudge", f"{door}: {v.rule}")
            return
        _allow(); _witness("allow", f"{door}: {v.rule}")
    except Exception as exc:
        _allow()
        _witness("allow", f"adapter error -> fail-open: {exc}")


if __name__ == "__main__":
    main()
