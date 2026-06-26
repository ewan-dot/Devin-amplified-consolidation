"""Snapshot orchestration — gather all sensors, merge, expose for Perplexity."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from unified_sensor.bridge import collect_via_control_centre
from unified_sensor.local_collectors import apply_local_rules, collect_all_local
from unified_sensor.registry import SOURCE_NAMES

DEFAULT_SNAPSHOT_PATH = Path(__file__).resolve().parent.parent / "data" / "sensor_snapshot.json"


def _merge_local(base: dict[str, Any] | None, local_events: list[dict]) -> dict[str, Any]:
    """Merge local events into a control-centre snapshot, or build standalone."""
    now = datetime.now(timezone.utc).isoformat()

    if base is None:
        findings = apply_local_rules(local_events)
        by_source: dict[str, int] = {}
        for ev in local_events:
            by_source[ev["source"]] = by_source.get(ev["source"], 0) + 1
        return {
            "generated_at": now,
            "backend": "local",
            "sensor_sources": list(SOURCE_NAMES),
            "events_total": len(local_events),
            "events_by_source": by_source,
            "events": local_events,
            "findings": findings,
            "findings_open": len(findings),
            "findings_critical": sum(
                1 for f in findings if f.get("severity") in ("RED", "BLACK")
            ),
        }

    # Augment control-centre snapshot with local-only metrics
    events = list(base.get("events") or [])
    existing_ids = {e.get("id") for e in events}
    for ev in local_events:
        if ev["id"] not in existing_ids:
            events.append(ev)

    by_source = dict(base.get("events_by_source") or {})
    for ev in local_events:
        by_source[ev["source"]] = by_source.get(ev["source"], 0) + 1

    findings = list(base.get("findings") or [])
    local_findings = apply_local_rules(local_events)
    findings.extend(local_findings)

    return {
        "generated_at": now,
        "backend": base.get("backend", "control-centre"),
        "control_centre_path": base.get("control_centre_path"),
        "sensor_sources": list(SOURCE_NAMES),
        "events_total": len(events),
        "events_by_source": by_source,
        "events": events,
        "findings": findings,
        "findings_open": len(findings),
        "findings_critical": sum(
            1 for f in findings if f.get("severity") in ("RED", "BLACK")
        ),
        "collector_errors": base.get("collector_errors", {}),
    }


def collect_snapshot(*, fast: bool = True, local_only: bool = False) -> dict[str, Any]:
    """Run all available collectors and return a unified sensor snapshot."""
    local_events = collect_all_local()
    cc = None if local_only else collect_via_control_centre(fast=fast)
    return _merge_local(cc, local_events)


def write_snapshot(path: Path | None = None, *, fast: bool = True) -> Path:
    """Collect and persist snapshot JSON for Perplexity session-start reads."""
    out = path or DEFAULT_SNAPSHOT_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    snap = collect_snapshot(fast=fast)
    out.write_text(json.dumps(snap, indent=2, default=str), encoding="utf-8")
    return out


def load_snapshot(path: Path | None = None) -> dict[str, Any]:
    """Load the last written snapshot (for offline / fast session-start)."""
    p = path or DEFAULT_SNAPSHOT_PATH
    if not p.exists():
        return collect_snapshot()
    return json.loads(p.read_text(encoding="utf-8"))
