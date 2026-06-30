"""Vellum session marker — plan before work, actual on close."""
from __future__ import annotations

import json
import os
import time
from typing import Any

MARKER = os.path.expanduser("~/.amplified/logs/vellum-session.json")
SESSION_HOURS = 8


def load() -> dict[str, Any]:
    try:
        if os.path.isfile(MARKER):
            with open(MARKER, encoding="utf-8") as f:
                return json.load(f)
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def save(data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(MARKER), exist_ok=True)
    with open(MARKER, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def mark_plan(entry_id: str, seat: str = "cursor") -> None:
    save(
        {
            "seat": seat,
            "plan_ts": time.time(),
            "plan_entry_id": entry_id,
            "actual_ts": None,
            "actual_entry_id": None,
        }
    )


def mark_actual(entry_id: str) -> None:
    data = load()
    data["actual_ts"] = time.time()
    data["actual_entry_id"] = entry_id
    save(data)


def plan_posted_recently() -> bool:
    data = load()
    ts = float(data.get("plan_ts") or 0)
    return bool(data.get("plan_entry_id")) and (time.time() - ts) < SESSION_HOURS * 3600


def actual_posted_for_current_plan() -> bool:
    data = load()
    if not data.get("plan_entry_id"):
        return True
    return bool(data.get("actual_entry_id")) and float(data.get("actual_ts") or 0) >= float(
        data.get("plan_ts") or 0
    )


def plan_entry_id() -> str:
    return str(load().get("plan_entry_id") or "")
