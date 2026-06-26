"""
extract.py — deterministic field extraction (no LLM).

Pushing determinism as far as it goes: for the structured routes we can pull the
fields a downstream system needs with regex, so the routed JSONL carries real data
and NO email body has to reach a model. Whatever regex cannot resolve is left for
the `needs_ai` residue — that, and only that, is where a model earns its tokens.
"""
from __future__ import annotations

import re

from .servers.base import Email

_RUN_URL = re.compile(r"actions/runs/(\d+)")
_REPO = re.compile(r"\b([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)\b")
_MONEY = re.compile(r"(?<![\w])(?:£|\$|€|USD|GBP|EUR)\s?\d[\d,]*(?:\.\d{2})?", re.I)
_INVOICE_NO = re.compile(r"\b(?:invoice|inv|ticket)[#\s:]*([A-Z0-9][A-Z0-9-]{3,})\b", re.I)


def extract_infra(e: Email) -> dict:
    """Repo / run-id / status from a CI or infra notification — deterministic."""
    text = f"{e.subject}\n{e.body}"
    run = _RUN_URL.search(text)
    repos = [m for m in _REPO.findall(e.subject) if "/" in m]
    failed = bool(re.search(r"\b(failed|failure|all jobs have failed)\b", text, re.I))
    return {
        "repo": repos[0] if repos else None,
        "run_id": run.group(1) if run else None,
        "status": "failed" if failed else "unknown",
        "vendor_sender": e.sender,
    }


def extract_financial(e: Email) -> dict:
    """Vendor / amounts / invoice ref — deterministic. Amounts left to AI only if none found."""
    text = f"{e.subject}\n{e.body}"
    amounts = _MONEY.findall(text)
    inv = _INVOICE_NO.search(text)
    return {
        "vendor": e.sender.split("@")[-1] if "@" in e.sender else e.sender,
        "amounts": amounts,
        "invoice_ref": inv.group(1) if inv else None,
        "amounts_found": bool(amounts),
    }
