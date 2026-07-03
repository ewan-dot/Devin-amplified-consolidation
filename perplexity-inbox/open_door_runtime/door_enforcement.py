"""
door_enforcement.py — pure allow/nudge/deny decision for the open-door harness.

=============================================================================
PHASE 0 — SCAFFOLD ONLY.  This module is NOT wired to ~/.cursor/hooks.json.
It is a pure decision function plus deterministic self-tests. Importing or
running this file has ZERO effect on any live Cursor session. Live activation
is a separate, single, documented step — see ACTIVATION.md.
=============================================================================

Given a proposed action + the active-door marker + the doors manifest, decide
allow / nudge / deny. Staging is explicit:

    mode="scaffold" : door-scope violations are ALLOWED (advisory only).
    mode="nudge"    : door-scope violations return NUDGE (still allow at hook).
    mode="deny"     : door-scope violations return DENY for doors in the
                      enforcing set (default = manifest first_hard_deny_doors),
                      NUDGE for the rest.

Door-INDEPENDENT hard lines (secrets, Red-core destroy/launder, git push on
Mac) return DENY in EVERY mode — they are never gated by a door, and staging
does not soften them. (This is decision logic only; nothing is wired.)

Renamed/created per SSOT open-door-harness v01 §C-4 (runtime home = open_door_runtime/).
tier: INTUITED (first-pass; path globs refined from Phase-2 telemetry).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

_HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = _HERE.parent / "config" / "doors-v1.json"
DEFAULT_MARKER = Path("~/.amplified/active-door.json").expanduser()

VERDICT_ALLOW = "allow"
VERDICT_NUDGE = "nudge"
VERDICT_DENY = "deny"


@dataclass
class Verdict:
    verdict: str                 # allow | nudge | deny
    reason: str
    rule: str                    # which rule fired
    door: str = ""
    remedy: str = ""             # exit/re-enter hint when out-of-scope
    door_independent: bool = False

    def to_dict(self) -> dict:
        return self.__dict__


# --------------------------------------------------------------------------
# Loaders
# --------------------------------------------------------------------------
def load_manifest(path: os.PathLike | str = DEFAULT_MANIFEST) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_marker(path: os.PathLike | str = DEFAULT_MARKER) -> dict:
    """Read the active-door marker; never-stuck default if absent/broken."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"door": "research_read", "task": "default (marker absent)", "seat": "unknown"}


# --------------------------------------------------------------------------
# Glob / path helpers
# --------------------------------------------------------------------------
def _glob_to_regex(glob: str) -> str:
    glob = os.path.expanduser(glob)
    out = ["^"]
    i, n = 0, len(glob)
    while i < n:
        if glob[i:i + 2] == "**":
            out.append(".*")
            i += 2
            if i < n and glob[i] == "/":
                i += 1
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    out.append("$")
    return "".join(out)


def _bind(glob: str, bindings: Optional[dict]) -> Optional[str]:
    """Substitute <placeholders> from bindings; return None if unbindable."""
    if "<" not in glob:
        return glob
    if not bindings:
        return None
    result = glob
    for m in re.findall(r"<([^>]+)>", glob):
        val = bindings.get(m)
        if not val:
            return None
        result = result.replace(f"<{m}>", str(val))
    return result


def _path_in_globs(path: str, globs, bindings: Optional[dict] = None) -> bool:
    path = os.path.expanduser(path)
    for g in globs or []:
        g2 = _bind(g, bindings)
        if g2 is None:
            continue
        if re.match(_glob_to_regex(g2), path):
            return True
    return False


def _fragment_hit(text: str, fragments) -> Optional[str]:
    low = (text or "").lower()
    for frag in fragments or []:
        if frag.lower() in low:
            return frag
    return None


def _net_ok(requested: str, door_level: str) -> bool:
    if requested in (None, "", "none"):
        return True
    if requested == door_level:
        return True
    return requested in door_level.split("+")


def _is_rule_mdc(path: str) -> bool:
    p = os.path.expanduser(path).replace("\\", "/")
    return "/.cursor/rules/" in p and p.endswith(".mdc")


# --------------------------------------------------------------------------
# Core decision
# --------------------------------------------------------------------------
def _door_by_name(manifest: dict, name: str) -> Optional[dict]:
    for d in manifest.get("doors", []):
        if d["name"] == name:
            return d
    return None


def _which_doors_allow(action: dict, manifest: dict, bindings: Optional[dict]) -> list:
    """Doors whose scope would permit this action (for the exit/re-enter remedy)."""
    kind = action.get("kind")
    hits = []
    for d in manifest.get("doors", []):
        ok = False
        if kind == "fs_read":
            ok = _path_in_globs(action.get("path", ""), d.get("fs_read"), bindings)
        elif kind == "fs_write":
            ok = _path_in_globs(action.get("path", ""), d.get("fs_write"), bindings)
        elif kind == "net":
            ok = _net_ok(action.get("level", "none"), d.get("net_mesh", "none"))
        elif kind == "git" and action.get("op") == "commit":
            ok = d.get("git_write") == "commit-local"
        if ok:
            hits.append(d["name"])
    return hits


def _staged(out_reason: str, rule: str, door: str, remedy: str,
            mode: str, enforcing: bool) -> Verdict:
    """Apply the nudge->deny staging to an out-of-scope action."""
    if mode == "scaffold":
        return Verdict(VERDICT_ALLOW, f"[scaffold: advisory only] {out_reason}", rule, door, remedy)
    if mode == "nudge":
        return Verdict(VERDICT_NUDGE, out_reason, rule, door, remedy)
    # mode == "deny"
    if enforcing:
        return Verdict(VERDICT_DENY, out_reason, rule, door, remedy)
    return Verdict(VERDICT_NUDGE, f"[deny not yet active for this door] {out_reason}", rule, door, remedy)


def decide(action: dict,
           active_door: str,
           manifest: dict,
           mode: str = "scaffold",
           enforcing_doors: Optional[list] = None,
           bindings: Optional[dict] = None) -> Verdict:
    """
    Pure decision. `action` is a dict:
      {"kind":"fs_read"|"fs_write","path": str}
      {"kind":"net","level": str}
      {"kind":"git","op":"push"|"commit"}
      {"kind":"shell","command": str}
    Returns a Verdict. NEVER performs any side effect.
    """
    uni = manifest.get("universal_rules", {})

    # ---- Door-independent hard lines (DENY in every mode) ----
    # 1. Secrets / Infisical — NO DOOR EVER.
    secret_frags = uni.get("secrets_infisical", {}).get("forbidden_path_fragments", [])
    probe = action.get("path") or action.get("command") or action.get("target") or ""
    hit = _fragment_hit(probe, secret_frags)
    if hit:
        return Verdict(VERDICT_DENY,
                       f"secrets/credential material ('{hit}') — NO DOOR EVER",
                       "universal.secrets_infisical", active_door,
                       "no door opens this; leave it alone", door_independent=True)

    # 2. git push on Mac — universal Red.
    if action.get("kind") == "git" and action.get("op") == "push":
        return Verdict(VERDICT_DENY,
                       "git push on Mac is universal-Red — land via Beast / Devin PR",
                       "universal.git_push_on_mac", active_door,
                       "no door grants push", door_independent=True)

    # 3. Red core destroy/launder commands.
    if action.get("kind") == "shell":
        red = uni.get("red_core_door_independent", {}).get("examples", [])
        rhit = _fragment_hit(action.get("command", ""), red)
        if rhit:
            return Verdict(VERDICT_DENY,
                           f"Red-core destructive/launder pattern ('{rhit}') — door-independent",
                           "universal.red_core", active_door,
                           "no door opens the Red core", door_independent=True)

    # ---- Resolve the active door ----
    door = _door_by_name(manifest, active_door)
    if door is None:
        return Verdict(VERDICT_DENY,
                       f"unknown active door '{active_door}' — fail cautious",
                       "config.unknown_door", active_door,
                       "enter a valid door (default research_read)")

    kind = action.get("kind")

    # ---- config_harness split: rule .mdc always needs architect bless ----
    if kind == "fs_write" and _is_rule_mdc(action.get("path", "")):
        if active_door == "config_harness":
            return Verdict(VERDICT_NUDGE,
                           "rule .mdc edit requires architect bless (unlock->edit->re-bless->lock)",
                           "config_harness.rules_mdc.architect_bless", active_door,
                           "agent may stage; Ewan blesses the rule change")
        return _staged("rule .mdc write outside config_harness",
                       "door.fs_write.out_of_scope", active_door,
                       "exit and enter config_harness (then architect bless)",
                       mode, active_door in (enforcing_doors or []))

    # ---- Door-scoped checks ----
    if enforcing_doors is None:
        enforcing_doors = manifest.get("defaults", {}).get("first_hard_deny_doors", []) if mode == "deny" else []
    enforcing = active_door in enforcing_doors

    if kind == "fs_read":
        if _path_in_globs(action.get("path", ""), door.get("fs_read"), bindings):
            return Verdict(VERDICT_ALLOW, "in FS-read scope", "door.fs_read", active_door)
        remedy = _remedy(action, manifest, bindings)
        return _staged(f"read path outside '{active_door}' FS-read scope",
                       "door.fs_read.out_of_scope", active_door, remedy, mode, enforcing)

    if kind == "fs_write":
        if _path_in_globs(action.get("path", ""), door.get("fs_write"), bindings):
            return Verdict(VERDICT_ALLOW, "in FS-write scope", "door.fs_write", active_door)
        remedy = _remedy(action, manifest, bindings)
        return _staged(f"write path outside '{active_door}' FS-write scope",
                       "door.fs_write.out_of_scope", active_door, remedy, mode, enforcing)

    if kind == "net":
        if _net_ok(action.get("level", "none"), door.get("net_mesh", "none")):
            return Verdict(VERDICT_ALLOW, "in Net/Mesh scope", "door.net", active_door)
        remedy = _remedy(action, manifest, bindings)
        return _staged(f"network '{action.get('level')}' outside '{active_door}' Net/Mesh",
                       "door.net.out_of_scope", active_door, remedy, mode, enforcing)

    if kind == "git":
        if action.get("op") == "commit":
            if door.get("git_write") == "commit-local":
                return Verdict(VERDICT_ALLOW, "commit-local permitted", "door.git", active_door)
            remedy = _remedy(action, manifest, bindings)
            return _staged(f"git commit outside '{active_door}' git-write scope",
                           "door.git.out_of_scope", active_door, remedy, mode, enforcing)

    if kind == "shell":
        # Non-Red shell is allowed at this layer (Phase 0 does not classify every command).
        return Verdict(VERDICT_ALLOW, "shell not Red-core; door-specific shell scoping deferred",
                       "door.shell.unscoped_phase0", active_door)

    return Verdict(VERDICT_ALLOW, f"action kind '{kind}' unscoped in Phase 0",
                   "phase0.unscoped", active_door)


def _remedy(action: dict, manifest: dict, bindings: Optional[dict]) -> str:
    doors = _which_doors_allow(action, manifest, bindings)
    if doors:
        return "exit and enter: " + " or ".join(doors)
    return "no configured door opens this action"


# --------------------------------------------------------------------------
# Deterministic self-tests. Run: python door_enforcement.py
# --------------------------------------------------------------------------
def _selftest() -> int:
    m = load_manifest()
    checks = []

    def chk(cond, label):
        checks.append((bool(cond), label))

    repo_doc = "~/ingestion-to-research-pipe/perplexity-inbox/SSOT__x.md"
    inbox_w = "~/ingestion-to-research-pipe/perplexity-inbox/out.md"
    secret = "~/.amplified/keys.env"
    hook = "~/.cursor/hooks/before-shell-execution.sh"
    rule = "~/.cursor/rules/ewan-core-rules.mdc"

    # 1. Never-stuck: research_read reading a repo doc is allowed in all modes.
    for mode in ("scaffold", "nudge", "deny"):
        chk(decide({"kind": "fs_read", "path": repo_doc}, "research_read", m, mode).verdict == VERDICT_ALLOW,
            f"research_read reads repo doc -> allow ({mode})")

    # 2. research_read write is out-of-scope; staging behaves.
    chk(decide({"kind": "fs_write", "path": inbox_w}, "research_read", m, "scaffold").verdict == VERDICT_ALLOW,
        "research_read write -> allow in scaffold (advisory)")
    chk(decide({"kind": "fs_write", "path": inbox_w}, "research_read", m, "nudge").verdict == VERDICT_NUDGE,
        "research_read write -> nudge in nudge mode")
    chk(decide({"kind": "fs_write", "path": inbox_w}, "research_read", m, "deny").verdict == VERDICT_DENY,
        "research_read write -> deny in deny mode (research_read is first-enforced)")

    # 3. Remedy points at central_handoff for an inbox write.
    v = decide({"kind": "fs_write", "path": inbox_w}, "research_read", m, "nudge")
    chk("central_handoff" in v.remedy, "remedy suggests central_handoff for inbox write")

    # 4. Secrets: DENY under every door and every mode, door-independent.
    for door in ("research_read", "config_harness", "central_handoff"):
        for mode in ("scaffold", "nudge", "deny"):
            r = decide({"kind": "fs_read", "path": secret}, door, m, mode)
            chk(r.verdict == VERDICT_DENY and r.door_independent,
                f"secret read -> deny door-independent ({door}/{mode})")

    # 5. git push: DENY under every mode, door-independent.
    for mode in ("scaffold", "nudge", "deny"):
        r = decide({"kind": "git", "op": "push"}, "worktree_feature", m, mode)
        chk(r.verdict == VERDICT_DENY and r.door_independent, f"git push -> deny ({mode})")

    # 6. Red-core shell: DENY even in scaffold.
    r = decide({"kind": "shell", "command": "sudo rm -rf /tmp/x"}, "agentsmini_build", m, "scaffold")
    chk(r.verdict == VERDICT_DENY and r.door_independent, "red-core shell -> deny in scaffold")

    # 7. config_harness: hook edit allowed; rule .mdc needs architect bless (nudge).
    chk(decide({"kind": "fs_write", "path": hook}, "config_harness", m, "deny").verdict == VERDICT_ALLOW,
        "config_harness writes a hook -> allow")
    chk(decide({"kind": "fs_write", "path": rule}, "config_harness", m, "deny").verdict == VERDICT_NUDGE,
        "config_harness rule .mdc -> nudge (architect bless), never silent allow")

    # 8. central_handoff writes inbox -> allow.
    chk(decide({"kind": "fs_write", "path": inbox_w}, "central_handoff", m, "deny").verdict == VERDICT_ALLOW,
        "central_handoff writes inbox -> allow")

    # 9. config_harness NOT auto-enforced in deny mode for generic out-of-scope? It IS in first_hard_deny_doors.
    r = decide({"kind": "fs_write", "path": "~/somewhere/else.txt"}, "config_harness", m, "deny")
    chk(r.verdict == VERDICT_DENY, "config_harness out-of-scope write -> deny (first-enforced door)")

    # 10. A non-enforced door in deny mode nudges (not denies) until rolled out.
    r = decide({"kind": "fs_write", "path": "~/somewhere/else.txt"}, "agentsmini_build", m, "deny")
    chk(r.verdict == VERDICT_NUDGE, "agentsmini_build out-of-scope write -> nudge (deny not yet rolled)")

    # 11. Unknown door -> fail cautious deny.
    chk(decide({"kind": "fs_read", "path": repo_doc}, "no_such_door", m, "scaffold").verdict == VERDICT_DENY,
        "unknown door -> deny fail-cautious")

    # 12. Bound placeholder door (worktree_feature) allows write inside bound subtree.
    b = {"worktree_subtree": "/Users/ewansair/_worktrees/open-door-phase0"}
    r = decide({"kind": "fs_write", "path": "/Users/ewansair/_worktrees/open-door-phase0/x.py"},
               "worktree_feature", m, "deny", bindings=b)
    chk(r.verdict == VERDICT_ALLOW, "worktree_feature write inside bound subtree -> allow")

    ok = True
    for passed, label in checks:
        print(f"{'PASS' if passed else 'FAIL'}  {label}")
        ok = ok and passed
    print(f"\n{'ALL PASS' if ok else 'FAILURES PRESENT'}  ({sum(p for p,_ in checks)}/{len(checks)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
