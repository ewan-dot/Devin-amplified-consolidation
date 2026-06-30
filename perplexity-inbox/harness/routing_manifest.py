"""Fleet routing manifest — per-IDE slices from SSOT JSON.

Read at session-start; Cursor seat loads ides.cursor only (IDE sovereignty).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def inbox_root() -> Path:
    env = os.environ.get("AMPLIFIED_INBOX", "").strip()
    if env:
        p = Path(env)
        if p.is_dir():
            return p
    for candidate in (
        Path.home() / "ingestion-to-research-pipe" / "perplexity-inbox",
        Path("/Volumes/ingestion-to-research-pipe/perplexity-inbox"),
    ):
        if candidate.is_dir():
            return candidate
    return Path(env or ".")


def manifest_path() -> Path:
    return inbox_root() / "config" / "fleet-routing-v1.json"


def load_manifest() -> dict[str, Any]:
    path = manifest_path()
    if not path.is_file():
        return {}
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def ide_slice(seat: str = "cursor") -> dict[str, Any]:
    manifest = load_manifest()
    key_map = {
        "cursor": "cursor",
        "claude": "claude_code",
        "claude_code": "claude_code",
        "antigravity": "antigravity",
    }
    ide_key = key_map.get(seat, seat)
    ides = manifest.get("ides") or {}
    return dict(ides.get(ide_key) or {})


def routing_sidecar_schema() -> dict[str, Any]:
    manifest = load_manifest()
    return dict(manifest.get("vellum_routing_sidecar") or {})


def session_hint_text(seat: str = "cursor") -> str:
    """Compact context for sessionStart injection."""
    manifest = load_manifest()
    if not manifest:
        return ""

    slice_ = ide_slice(seat)
    defaults = manifest.get("defaults") or {}
    lines = [
        "[routing-harness] Right horse for right course — SSOT:",
        str(manifest_path().relative_to(inbox_root()) if manifest_path().is_file() else "config/fleet-routing-v1.json"),
        f"default_mode={defaults.get('routing_mode', 'solo')}",
        f"forbid_subagent_inherit={defaults.get('forbid_subagent_inherit', True)}",
        f"frontier_ceiling_per_job={defaults.get('frontier_ceiling_per_job', 1)}",
    ]
    if slice_:
        lines.append(f"thread_ownership={slice_.get('thread_ownership', '')}")
        sub = slice_.get("subagent_rules") or {}
        if sub.get("delegate_when"):
            lines.append(f"delegate_when={sub['delegate_when']}")
    sidecar = routing_sidecar_schema()
    fields = (sidecar.get("fields") or {}).keys()
    if fields:
        lines.append(f"vellum_sidecar_fields={','.join(fields)}")
    lines.append("Witness routing on Vellum plan metadata.routing BEFORE spawn.")
    return "\n".join(lines)


def vellum_routing_from_marker() -> dict[str, Any] | None:
    """Optional routing hint persisted alongside vellum session marker."""
    marker = Path.home() / ".amplified" / "logs" / "vellum-session.json"
    if not marker.is_file():
        return None
    try:
        with marker.open(encoding="utf-8") as f:
            data = json.load(f)
        hint = data.get("routing_sidecar")
        return dict(hint) if isinstance(hint, dict) and hint else None
    except (OSError, json.JSONDecodeError):
        return None
