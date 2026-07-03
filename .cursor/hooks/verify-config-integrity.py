#!/usr/bin/env python3
"""Cursor config integrity tripwire + self-heal + lock-guard (sessionStart hook).

Compares live config (~/.cursor/rules/*.mdc, ~/.cursor/hooks/*, hooks.json)
against the blessed manifest. On drift it prints a LOUD warning to stdout so
the drift surfaces in the agent's sessionStart context, and it SELF-HEALS any
drifted rule whose canonical copy exists in the SSOT repo.

LOCK-AWARE (rules only):
  ~/.cursor/rules/*.mdc are EXPECTED to be macOS user-immutable (uchg) locked —
  they are Ewan's constitution. On session start, a rule that is found NOT locked
  (nouchg) OR whose hash drifted is treated as a tamper signal: the rule is
  unlocked, restored from SSOT canonical if its content drifted, then RE-LOCKED
  (uchg re-applied). All events go to drift.log.

  hooks.json, ~/.cursor/hooks/*, and ~/.cursor/integrity/* are NOT locked and NOT
  healed — they stay editable while the hooks/harness are under development. Drift
  there is report-only.

FULLNESS-GUARD (anti stale-over-fresh restore):
  Self-heal restores a drifted rule FROM the SSOT repo canonical (repo -> home).
  That direction is a trap if the repo ever holds a THIN / softened / gutted copy:
  it would silently overwrite a good locked home rule. So BEFORE restoring, the
  repo canonical must pass a fullness/anchor check (see FULLNESS_* config block
  below): a minimum byte floor for every rule, plus required anchor substrings for
  named constitutional rules (e.g. ewan-core-rules.mdc). If the canonical FAILS,
  we DO NOT restore — it is treated as a tamper/corruption signal: LOUD warning to
  stdout, logged to drift.log, and the existing (locked) home file is left intact.

Honest scope: single-user Mac. Any process running as the user can edit these
files (including this script and the manifest) and can `chflags nouchg` any lock.
This is TAMPER-EVIDENT + SELF-HEALING + a lock speed-bump, not tamper-PROOF.
See integrity/README.md.

Fail-open: always exits 0, never blocks a session, never hangs. No network.
"""
import datetime
import hashlib
import os
import stat
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

# ── FULLNESS-GUARD CONFIG (extend me) ─────────────────────────────────────────
# Gate applied to a repo canonical BEFORE it is allowed to overwrite a home rule
# during self-heal. Purpose: never let a thin/softened/stale/tampered canonical
# clobber a good locked home file (the repo->home restore is a stale-over-fresh
# trap). Fail-SAFE: if the canonical does not pass, keep the home file as-is.
#
# To extend: bump the byte floor, or add "<rule-filename>": [<anchor>, ...] to
# require that named rules contain ALL listed anchor substrings (case-insensitive).
FULLNESS_MIN_BYTES = 400  # global floor. Smallest real rule is ~650B, so 400B
                          # passes every legitimate rule while rejecting gutted
                          # copies. Raise if you want a stricter floor.
FULLNESS_ANCHORS = {
    # ewan-core-rules.mdc is the constitution — a valid canonical MUST name the
    # architect/expert-partner relationship and the sovereignty principle.
    "ewan-core-rules.mdc": ["architect", "expert partner", "sovereignty"],
}


def canonical_passes_fullness(name, data):
    """Return (ok, reason). Decide whether a repo canonical is 'full' enough to
    be trusted as a restore source. A False result means: refuse to restore,
    treat as tamper/corruption, keep the existing home file. Cheap + offline."""
    if len(data) < FULLNESS_MIN_BYTES:
        return False, f"too small: {len(data)}B < floor {FULLNESS_MIN_BYTES}B"
    anchors = FULLNESS_ANCHORS.get(name)
    if anchors:
        text = data.decode("utf-8", errors="replace").lower()
        missing = [a for a in anchors if a.lower() not in text]
        if missing:
            return False, f"missing anchors: {', '.join(missing)}"
    return True, "ok"


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


def is_uchg(path):
    """True if the user-immutable (uchg) flag is set."""
    try:
        return bool(os.stat(path).st_flags & stat.UF_IMMUTABLE)
    except (OSError, AttributeError):
        return False


def set_uchg(path, on):
    """Set/clear ONLY the uchg bit, preserving other flags. Returns True on success."""
    try:
        cur = os.stat(path).st_flags
        new = (cur | stat.UF_IMMUTABLE) if on else (cur & ~stat.UF_IMMUTABLE)
        if new != cur:
            os.chflags(path, new)
        return True
    except (OSError, AttributeError):
        return False


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


def heal_rule(key, want_restore, log_events):
    """(validate canonical) -> unlock -> restore -> re-lock a rules/ file.

    want_restore: True if content drifted/removed and should be restored from
    SSOT canonical. If False, we only re-apply the uchg lock.
    Returns one of: "healed", "relocked", "rejected", "unhealed".

    FULLNESS-GUARD: for a restore, the canonical is validated FIRST — before the
    home file is unlocked or touched. If it fails the fullness/anchor check it is
    a tamper/corruption signal: we do NOT restore, we leave the (locked) home
    file intact, and return "rejected".
    """
    name = key[len("rules/"):]
    dest = key_to_path(key)
    canonical = os.path.join(REPO_RULES, name)

    if want_restore:
        # Validate the canonical BEFORE touching the home file so a thin/stale
        # canonical can never overwrite a good locked home rule.
        if not os.path.isfile(canonical):
            log_events.append(f"HEAL_FAILED\t{key}\tno canonical in repo")
            if os.path.exists(dest):
                set_uchg(dest, True)  # keep home locked; do not rewrite
            return "unhealed"
        try:
            with open(canonical, "rb") as src:
                data = src.read()
        except OSError as e:
            log_events.append(f"HEAL_FAILED\t{key}\t{e}")
            if os.path.exists(dest):
                set_uchg(dest, True)
            return "unhealed"

        ok, reason = canonical_passes_fullness(name, data)
        if not ok:
            log_events.append(
                f"HEAL_REJECTED\t{key}\tcanonical failed fullness ({reason})"
                f"\thome left intact + locked"
            )
            # Leave the home file untouched; make sure it stays locked.
            if os.path.exists(dest):
                set_uchg(dest, True)
            return "rejected"

        # Canonical passed the fullness guard — safe to restore.
        if os.path.exists(dest):
            set_uchg(dest, False)
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as out:
                out.write(data)
            set_uchg(dest, True)
            log_events.append(f"HEALED\t{key}\tfrom {canonical}\tre-locked uchg")
            return "healed"
        except OSError as e:
            log_events.append(f"HEAL_FAILED\t{key}\t{e}")
            if os.path.exists(dest):
                set_uchg(dest, True)
            return "unhealed"

    # content OK, just re-apply the lock
    if set_uchg(dest, True):
        log_events.append(f"RELOCKED\t{key}\tuchg re-applied")
        return "relocked"
    log_events.append(f"RELOCK_FAILED\t{key}")
    return "unhealed"


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

    # Lock drift: any live rules/*.mdc that is NOT uchg-locked.
    unlocked_rules = [
        k for k, p in live.items()
        if k.startswith("rules/") and not is_uchg(p)
    ]

    if not (changed or added or removed or unlocked_rules):
        return 0

    log_events = []
    print("=" * 68)
    print("!! CURSOR CONFIG INTEGRITY DRIFT DETECTED !!")
    print("=" * 68)
    for key in sorted(changed):
        print(f"  CHANGED  : {key}")
        log_events.append(f"CHANGED\t{key}")
    for key in sorted(removed):
        print(f"  REMOVED  : {key}")
        log_events.append(f"REMOVED\t{key}")
    for key in sorted(added):
        print(f"  ADDED    : {key}")
        log_events.append(f"ADDED\t{key}")
    for key in sorted(unlocked_rules):
        print(f"  UNLOCKED : {key}  (rule not uchg-locked — tamper signal)")
        log_events.append(f"UNLOCKED\t{key}")

    # Self-heal + lock-guard for rules/ only.
    healed, relocked, rejected, unhealed = [], [], [], []
    rules_to_restore = {k for k in (changed + removed) if k.startswith("rules/")}
    rules_to_touch = sorted(rules_to_restore | set(unlocked_rules))
    for key in rules_to_touch:
        result = heal_rule(key, want_restore=(key in rules_to_restore), log_events=log_events)
        if result == "healed":
            healed.append(key)
        elif result == "relocked":
            relocked.append(key)
        elif result == "rejected":
            rejected.append(key)
        else:
            unhealed.append(key)

    if healed:
        print("-" * 68)
        print("  SELF-HEALED from SSOT repo + RE-LOCKED (uchg):")
        for key in healed:
            print(f"    RESTORED : {key}")
    if relocked:
        print("-" * 68)
        print("  RE-LOCKED (content OK, uchg re-applied):")
        for key in relocked:
            print(f"    LOCKED   : {key}")
    if rejected:
        print("!" * 68)
        print("  FULLNESS-GUARD: repo canonical REJECTED — RESTORE REFUSED.")
        print("  A thin/softened/stale canonical did NOT overwrite your rule.")
        print("  The locked home file was LEFT INTACT. Investigate the repo copy")
        print("  (possible tamper/corruption/softening) before re-blessing.")
        for key in rejected:
            print(f"    REFUSED  : {key}  (home kept; canonical failed fullness)")
        print("!" * 68)
    if unhealed:
        print("-" * 68)
        print("  NOT auto-healed (no canonical, or lock op failed):")
        for key in unhealed:
            print(f"    REVIEW   : {key}")

    # hooks.json / hooks/* / integrity are report-only (never healed or locked).
    report_only = [k for k in (changed + added + removed) if not k.startswith("rules/")]
    if report_only:
        print("-" * 68)
        print("  REPORT-ONLY (hooks/hooks.json — editable by design, not healed):")
        for key in sorted(report_only):
            print(f"    NOTE     : {key}")

    print("-" * 68)
    print("  Legit rule edit cycle:")
    print("    ~/.cursor/hooks/config-lock.sh unlock")
    print("    <edit rule(s)>")
    print("    python3 ~/.cursor/hooks/update-config-manifest.py")
    print("    ~/.cursor/hooks/config-lock.sh lock")
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
