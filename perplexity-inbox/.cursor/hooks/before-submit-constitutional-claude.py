#!/usr/bin/env python3
"""UserPromptSubmit — constitutional P0 nudge/block (Claude Code). Fail-open."""
import json
import os
import re
import sys
import time

WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")
MODE = os.environ.get("CONSTITUTIONAL_HARNESS_MODE", "pre_client").strip().lower()
CLIENT_LIVE = MODE == "client_live"
EVENT = "UserPromptSubmit"

SECRET_RE = re.compile(
    r"sk-[a-zA-Z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"xox[baprs]-[0-9A-Za-z-]{10,}|"
    r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----"
)

P0_RULES = [
    (
        "transparency_attribution",
        re.compile(
            r"(?i)\b("
            r"remove\s+(all\s+)?(ai|model|agent)\s+(names?|attribution|credit)|"
            r"strip\s+(ai|model|agent)\s+(names?|attribution|attribution)|"
            r"don'?t\s+(mention|attribute|credit)\s+(that\s+)?(ai|cursor|claude|gpt|copilot)|"
            r"hide\s+(ai|agent|model)\s+(involvement|authorship|attribution)|"
            r"make\s+it\s+look\s+human[- ]written|"
            r"no\s+attribution|"
            r"erase\s+(provenance|lineage|authorship)"
            r")\b"
        ),
        "Transparency/attribution rod — do not strip provenance or conceal AI authorship.",
    ),
    (
        "win_win_harm",
        re.compile(
            r"(?i)\b("
            r"mislead\s+(the\s+)?(client|customer|user|counterparty)|"
            r"hide\s+(this|it)\s+from\s+(the\s+)?(client|customer)|"
            r"don'?t\s+tell\s+(them|client|customer)|"
            r"backdoor|"
            r"bypass\s+(audit|security|approval|consent)"
            r")\b"
        ),
        "Win-win rod — refuse work that succeeds only by harming a counterparty.",
    ),
]

NUDGE_RULES = [
    (
        "privacy",
        re.compile(r"(?i)\b(paste|include|share|send)\s+(client|customer|patient|personal)\s+(data|pii|records?)\b"),
        "Privacy rod — confirm necessity and redaction before handling personal/client data.",
    ),
    (
        "sovereignty",
        re.compile(r"(?i)\b(push|commit|publish)\s+(without|skip)\s+(review|approval|consent)\b"),
        "Sovereignty rod — self-push still needs craft + constitutional gates before protected paths.",
    ),
]


def witness(ok, note, detail=None):
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        row = {
            "ts": time.time(),
            "hook": "before-submit-constitutional-claude",
            "mode": MODE,
            "ok": ok,
            "note": note,
        }
        if detail:
            row["detail"] = detail
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
    except Exception:
        pass


def respond(payload):
    print(json.dumps(payload))
    sys.exit(0)


def nudge(msg):
    respond(
        {
            "hookSpecificOutput": {
                "hookEventName": EVENT,
                "additionalContext": msg,
            }
        }
    )


def block(msg):
    if CLIENT_LIVE:
        respond({"systemMessage": f"Constitutional harness ({MODE}): {msg}"})
    nudge(f"[constitutional-gate/{MODE}] {msg} Agent must refuse or defer violating slice — no architect override.")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        respond({})
        return

    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        respond({})
        return

    if SECRET_RE.search(prompt):
        msg = "Constitutional/security rod — possible secret in prompt. Remove before submitting."
        witness(False, "secret_p0_block", "secret_pattern")
        block(msg)
        return

    for rule_id, pattern, rod_msg in P0_RULES:
        if pattern.search(prompt):
            witness(False, f"p0_{rule_id}", rod_msg)
            block(rod_msg)
            return

    for rule_id, pattern, rod_msg in NUDGE_RULES:
        if pattern.search(prompt):
            witness(True, f"nudge_{rule_id}", rod_msg)
            nudge(f"[constitutional-gate] {rod_msg}")
            return

    witness(True, "pass")
    respond({})


if __name__ == "__main__":
    main()
