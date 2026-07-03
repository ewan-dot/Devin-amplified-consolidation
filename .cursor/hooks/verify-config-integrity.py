#!/usr/bin/env python3
"""Cursor config integrity tripwire + self-heal (sessionStart hook).

Compares live config (~/.cursor/rules/*.mdc, ~/.cursor/hooks/*, hooks.json)
against the blessed manifest. On drift it prints a LOUD warning to stdout so
the drift surfaces in the agent's sessionStart context, and it SELF-HEALS any
drifted rule whose canonical copy exists in the SSOT repo.

Honest scope: single-user Mac. Any process running as the user can edit these
files (including this script and the manifest). This is TAMPER-EVIDENT +
SELF-HEALING, not tamper-PROOF. See integrity/README.md for the optional
OS-level lock (chflags), deliberately left OFF.

Fail-open: always exits 0, never blocks a session, never hangs.
"""
import datetime
import hashlib
import os
import sys

HOME = os.path.expanduser("~")
CURSOR_DIR = os.path.join(HOME, ".cursor")
RULES_DIR = os.path.join(CURSOR_DIR, "rules")
HOOKS_DIR = os.path.join(CURSOR_DIR, "hooks")
HOOKS_JSON = os.path.join(CURSOR_DIR, "hooks.json")
LOCAL_INTEGRITY = os.path.join(CURSOR_DIR, "integrity")
MANIFEST_PATH = os.path.join(LOCAL_INTEGRITY, "manifest.sha256")
DRIFT_LOG = os.path.join(LOCAL_INTEGRITY, "drift.log")

SSOT_REPO = os.environ.get(
    "CURSOR_SSOT_REPO", os.path.join(HOME, "ingestion-to-research-pipe")
)
REPO_RULES = os.path.join(SSOT_REPO, ".cursor", "rules")


def _log(events):
    if not events:
        return
    try:
        os.makedirs(LOCAL_INTEGRITY, exist_ok=True)
        ts = datetime.datetime.now().astimezone().isoformat()
        with open(DRIFT_LOG, "a") as f:
            for ev in events:
                f.write(f"{ts}\t{ev}\n")
    except OSError:
        pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def live_files():
    entries = {}
    if os.path.isfile(HOOKS_JSON):
        entries["hooks.json"] = HOOKS_JSON
    for base, prefix in ((RULES_DIR, "rules"), (HOOKS_DIR, "hooks")):
        if not os.path.isdir(base):
            continue
        for name in os.listdir(base):
            p = os.path.join(base, name)
            if not os.path.isfile(p):
                continue
            if base == RULES_DIR and not name.endswith(".mdc"):
                continue
            entries[f"{prefix}/{name}"] = p
    return entries


def load_manifest():
    manifest = {}
    with open(MANIFEST_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                continue
            manifest[parts[1].strip()] = parts[0].strip()
    return manifest


def key_to_path(key):
    return os.path.join(CURSOR_DIR, key)


def main():
    if not os.path.isfile(MANIFEST_PATH):
        print("[config-integrity] no manifest yet — run "
              "update-config-manifest.py to bless current config.")
        return 0

    try:
        manifest = load_manifest()
    except OSError:
        print("[config-integrity] WARN: could not read manifest; skipping.")
        return 0

    live = live_files()
    live_hashes = {k: sha256_file(p) for k, p in live.items()}

    changed, added, removed = [], [], []
    for key, want in manifest.items():
        if key not in live_hashes:
            removed.append(key)
        elif live_hashes[key] != want:
            changed.append(key)
    for key in live_hashes:
        if key not in manifest:
            added.append(key)

    if not (changed or added or removed):
        return 0

    log_events = []
    print("=" * 68)
    print("!! CURSOR CONFIG INTEGRITY DRIFT DETECTED !!")
    print("=" * 68)
    for key in sorted(changed):
        print(f"  CHANGED : {key}")
        log_events.append(f"CHANGED\t{key}")
    for key in sorted(removed):
        print(f"  REMOVED : {key}")
        log_events.append(f"REMOVED\t{key}")
    for key in sorted(added):
        print(f"  ADDED   : {key}")
        log_events.append(f"ADDED\t{key}")

    # Self-heal: restore drifted rules from SSOT repo canonical.
    healed, unhealed = [], []
    for key in sorted(changed + removed):
        if not key.startswith("rules/"):
            continue
        name = key[len("rules/"):]
        canonical = os.path.join(REPO_RULES, name)
        if not os.path.isfile(canonical):
            unhealed.append(key)
            continue
        try:
            with open(canonical, "rb") as src:
                data = src.read()
            dest = key_to_path(key)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as out:
                out.write(data)
            healed.append(key)
            log_events.append(f"HEALED\t{key}\tfrom {canonical}")
        except OSError as e:
            unhealed.append(key)
            log_events.append(f"HEAL_FAILED\t{key}\t{e}")

    if healed:
        print("-" * 68)
        print("  SELF-HEALED from SSOT repo (canonical content restored):")
        for key in healed:
            print(f"    RESTORED : {key}")
    if unhealed:
        print("-" * 68)
        print("  NOT auto-healed (no canonical in repo, or hooks/hooks.json):")
        for key in unhealed:
            print(f"    REVIEW   : {key}")
    print("-" * 68)
    print("  If these changes were intentional, re-bless with:")
    print("    python3 ~/.cursor/hooks/update-config-manifest.py")
    print(f"  Drift log: {DRIFT_LOG}")
    print("=" * 68)

    _log(log_events)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # never hang or crash a session
        print(f"[config-integrity] WARN: verify errored, failing open: {e}")
        sys.exit(0)
