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

Two failure stances, on purpose (research: hooks are fail-open unless failClosed:true):
  * HARD-DENY CORE (secrets, Red-core destroy/launder, protected-branch pushes,
    and merge commands) is
    evaluated FIRST by a self-contained, manifest-independent probe and is
    FAIL-CLOSED for shell/MCP: if that probe itself errors, the call is DENIED.
    Pair this with `"failClosed": true` on the wired hook in hooks.json
    (see hooks-failclosed.snippet.json) so a crash/timeout/bad-JSON also denies.
  * DOOR-SCOPE decision (in/out of the active door's blast radius) stays
    FAIL-OPEN: a scope-check error prints {"permission":"allow"} so a misconfig
    can never wedge a session — mirroring pre-bash-guard.py / before-read-file.sh.
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


# --------------------------------------------------------------------------
# HARD-DENY CORE — self-contained + manifest-independent, so it holds even if
# doors-v1.json is missing/corrupt. Kept tiny + deterministic so it (almost)
# never errors; the caller treats any error here as DENY for shell/MCP.
# These fragments mirror doors-v1.json universal_rules; they are the LAST-DITCH
# fallback, not the source of truth.
# --------------------------------------------------------------------------
_CORE_SECRET_FRAGS = [".env", "keys.env", "secrets", "credentials", "id_rsa",
                      "id_ed25519", ".ssh", "infisical", "op://"]
_CORE_RED_FRAGS = ["rm -rf", "sudo rm", "git push --force", "git push -f",
                   "git reset --hard", "mkfs", "dd if=", "curl | sh", "curl|sh",
                   "wget | sh", "wget|sh", ":(){:|:&};:"]


def _probe_hard_deny(event, data):
    """Return a deny-reason string for a door-INDEPENDENT hard line, else None.
    No manifest, no filesystem — pure string inspection of the tool input."""
    path = (data.get("path") or data.get("file_path")
            or (data.get("tool_input") or {}).get("path") or "")
    cmd = (data.get("command") or (data.get("tool_input") or {}).get("command") or "")
    probe = f"{path} {cmd}".lower()
    for frag in _CORE_SECRET_FRAGS:
        if frag in probe:
            return f"secrets/credential material ('{frag}') — NO DOOR EVER"
    if re.search(r"\bgit\s+merge\b|\bgh\s+pr\s+merge\b", cmd):
        return "merge is the approval gate; present a branch for review instead"
    if re.search(r"\bgit\s+push\b.*(?:\bmain\b|\bmaster\b)", cmd):
        return "protected-branch push is denied; push a feature branch for review"
    low = cmd.lower()
    for frag in _CORE_RED_FRAGS:
        if frag in low:
            return f"Red-core destructive/launder pattern ('{frag}') — door-independent"
    return None


def _deny(reason, note, remedy=""):
    msg = f"[open-door] DENY — {reason}." + (f" Remedy: {remedy}." if remedy else "")
    print(json.dumps({"permission": "deny", "user_message": msg, "agent_message": msg}))
    _witness("deny", note)


def main():
    event = sys.argv[1] if len(sys.argv) > 1 else "shell"
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        # Cursor-level failClosed:true (hooks.json) covers the bad-JSON crash case;
        # here we cannot classify, so fall open at the adapter and let the hook config decide.
        _allow(); _witness("allow", "stdin parse error -> fail-open (Cursor failClosed covers crash)"); return

    # ---- HARD-DENY CORE — FAIL CLOSED for shell/MCP ----
    try:
        core_reason = _probe_hard_deny(event, data)
    except Exception as exc:
        if event in ("shell", "mcp"):
            _deny("open-door hard-deny core errored — failing CLOSED",
                  f"failClosed core error: {exc}",
                  "core check could not prove the call safe")
            return
        core_reason = None  # reads/other: fall open (real read boundary is .cursorignore)
    if core_reason:
        _deny(core_reason, f"hard-core: {core_reason}",
              "no door opens this; exit is not a remedy")
        return

    # ---- DOOR-SCOPE decision — FAIL OPEN (never wedge on a scope miss) ----
    try:
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
