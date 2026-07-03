#!/usr/bin/env python3
"""Re-bless the Cursor config integrity manifest.

Regenerates sha256 for every rule (.mdc), every hook file, and hooks.json,
then writes the manifest to BOTH the local integrity dir and the SSOT repo.
Run this after any INTENTIONAL config change so the tripwire stops firing.

Portable: uses ~ expansion + CURSOR_SSOT_REPO env (no hardcoded user path).
"""
import datetime
import hashlib
import os
import socket
import sys

HOME = os.path.expanduser("~")
CURSOR_DIR = os.path.join(HOME, ".cursor")
RULES_DIR = os.path.join(CURSOR_DIR, "rules")
HOOKS_DIR = os.path.join(CURSOR_DIR, "hooks")
HOOKS_JSON = os.path.join(CURSOR_DIR, "hooks.json")
LOCAL_INTEGRITY = os.path.join(CURSOR_DIR, "integrity")

SSOT_REPO = os.environ.get(
    "CURSOR_SSOT_REPO", os.path.join(HOME, "ingestion-to-research-pipe")
)
REPO_INTEGRITY = os.path.join(SSOT_REPO, ".cursor", "integrity")

MANIFEST_NAME = "manifest.sha256"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def covered_files():
    """Return sorted list of (key, abspath) for all config files to hash.

    key is relative to ~/.cursor. The integrity dir is never included.
    """
    entries = []
    if os.path.isfile(HOOKS_JSON):
        entries.append(("hooks.json", HOOKS_JSON))
    for base, key_prefix in ((RULES_DIR, "rules"), (HOOKS_DIR, "hooks")):
        if not os.path.isdir(base):
            continue
        for name in os.listdir(base):
            p = os.path.join(base, name)
            if not os.path.isfile(p):
                continue
            if base is RULES_DIR and not name.endswith(".mdc"):
                continue
            entries.append((f"{key_prefix}/{name}", p))
    entries.sort(key=lambda e: e[0])
    return entries


def build_manifest():
    lines = []
    ts = datetime.datetime.now().astimezone().isoformat()
    entries = covered_files()
    header = [
        "# Cursor config integrity manifest",
        f"# generated: {ts}",
        f"# host: {socket.gethostname()}",
        f"# files: {len(entries)}",
        "# format: <sha256>  <path-relative-to-~/.cursor>",
    ]
    for key, path in entries:
        lines.append(f"{sha256_file(path)}  {key}")
    return "\n".join(header + lines) + "\n", len(entries)


def write_manifest(text):
    written = []
    for d in (LOCAL_INTEGRITY, REPO_INTEGRITY):
        try:
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, MANIFEST_NAME), "w") as f:
                f.write(text)
            written.append(os.path.join(d, MANIFEST_NAME))
        except OSError as e:
            print(f"[bless] WARN: could not write {d}: {e}", file=sys.stderr)
    return written


def main():
    text, n = build_manifest()
    written = write_manifest(text)
    print(f"[bless] manifest regenerated: {n} files hashed")
    for w in written:
        print(f"[bless]   wrote {w}")
    if not written:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
