#!/usr/bin/env python3
"""stop — nudge SSOT commit + Vellum compound delta when rules/hooks changed."""
import hashlib
import json
import os
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")
SEEN_DIR = os.path.expanduser("~/.amplified/logs/stop-compound-seen")
WATCH = (
    os.path.expanduser("~/.cursor/rules"),
    os.path.expanduser("~/.cursor/hooks"),
    os.path.expanduser("~/ingestion-to-research-pipe/.cursor/rules"),
)
SUFFIXES = (".mdc", ".py", ".sh", ".json")
SESSION_MINS = 240


def witness(ok, note):
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps({"ts": time.time(), "hook": "stop-self-compound", "ok": ok, "note": note})
                + "\n"
            )
    except Exception:
        pass


def recently_changed():
    cutoff = time.time() - SESSION_MINS * 60
    out = []
    for root_dir in WATCH:
        if not os.path.isdir(root_dir):
            continue
        for root, _, files in os.walk(root_dir):
            for name in files:
                if not name.endswith(SUFFIXES):
                    continue
                path = os.path.join(root, name)
                try:
                    if os.path.getmtime(path) >= cutoff:
                        out.append(path)
                except OSError:
                    pass
    return out


def main():
    try:
        data = json.load(sys.stdin)
        sid = data.get("session_id") or data.get("transcript_path") or "nosession"
        sentinel = os.path.join(SEEN_DIR, hashlib.sha256(str(sid).encode()).hexdigest()[:16])
        if os.path.exists(sentinel):
            print("{}")
            witness(True, "already nudged")
            return

        changed = recently_changed()
        if not changed:
            print("{}")
            witness(True, "no compound delta")
            return

        os.makedirs(SEEN_DIR, exist_ok=True)
        open(sentinel, "w", encoding="utf-8").close()
        names = sorted({os.path.basename(p) for p in changed})[:4]
        extra = len(changed) - len(names)
        tail = f" (+{extra} more)" if extra > 0 else ""
        msg = (
            f"[self-compound] Rules/hooks changed ({', '.join(names)}{tail}). "
            "Same session: (1) commit SSOT copy to repo `.cursor/` or `perplexity-inbox/.cursor/`, "
            "(2) post one-line Vellum compound delta (gap closed + where encoded)."
        )
        print(json.dumps({"followup_message": msg}))
        witness(True, f"nudge {len(changed)} files")
    except Exception as exc:
        print("{}")
        witness(False, f"error: {exc}")


if __name__ == "__main__":
    main()
