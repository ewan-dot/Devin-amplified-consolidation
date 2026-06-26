"""Bridge to control-centre — the deterministic core's collector + rule engine.

Adds ~/control-centre (or CONTROL_CENTRE_PATH) to sys.path when present.
Returns None when control-centre is unavailable; local collectors still run.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any


def control_centre_root() -> Path | None:
    env = os.environ.get("CONTROL_CENTRE_PATH")
    if env:
        p = Path(env).expanduser()
        return p if p.is_dir() else None
    default = Path.home() / "control-centre"
    return default if default.is_dir() else None


def _ensure_path(root: Path) -> None:
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def collect_via_control_centre(*, fast: bool = True) -> dict[str, Any] | None:
    """Run control-centre collectors + rules. Returns snapshot dict or None.

    fast=True (default): critical sensors only — vellum, ingestion_pipe,
    tailscale, credentials, baton. Skips full-org GitHub scan (~5 min).
    """
    root = control_centre_root()
    if root is None:
        return None

    _ensure_path(root)

    try:
        from core.engine_ext import ControlCentreEngine
        from rules.engine import run_rules
    except ImportError:
        return None

    engine = ControlCentreEngine()
    collector_errors: dict[str, str] = {}

    def _run_collector(name: str, fn) -> int:
        try:
            events = list(fn())
            n = engine.ingest_events(events)
            print(f"  [{name}]  {n} events", file=__import__("sys").stderr)
            return n
        except Exception as e:
            collector_errors[name] = str(e)
            print(f"  [{name}]  ERROR: {e}", file=__import__("sys").stderr)
            return 0

    n_events = 0
    if fast:
        from collectors.vellum import collect as vellum_collect
        from collectors.ingestion_pipe import collect as pipe_collect
        from collectors.tailscale import collect as ts_collect
        from collectors.credentials import collect as creds_collect
        from collectors.baton import collect as baton_collect
        for name, fn in (
            ("vellum", vellum_collect),
            ("ingestion_pipe", pipe_collect),
            ("tailscale", ts_collect),
            ("credentials", creds_collect),
            ("baton", baton_collect),
        ):
            n_events += _run_collector(name, fn)
    else:
        try:
            from pane import collect_all
            n_events = collect_all(engine)
        except Exception as e:
            return {
                "backend": "control-centre",
                "error": f"collect_all failed: {e}",
                "events": [],
                "findings": [],
                "collector_errors": {"collect_all": str(e)},
            }

    events: list[dict] = []
    findings: list[dict] = []

    if engine._conn:
        raw = engine._conn.execute(
            "SELECT id, source, metric, scope, value_num, value_text, tier, "
            "timestamp, collector_ver, raw_json FROM stats_events"
        ).fetchall()
        events = [
            {
                "id": r[0], "source": r[1], "metric": r[2], "scope": r[3],
                "value_num": r[4], "value_text": r[5], "tier": r[6],
                "timestamp": str(r[7]), "collector_ver": r[8], "raw_json": r[9],
            }
            for r in raw
        ]
        events_for_rules = [
            {
                "id": e["id"], "source": e["source"], "metric": e["metric"],
                "scope": e["scope"], "value_num": e["value_num"],
                "value_text": e["value_text"], "tier": e["tier"],
                "raw_json": e["raw_json"],
            }
            for e in events
        ]
        findings = run_rules(events_for_rules)
        engine.ingest_findings(findings)

        open_rows = engine.run_cc("findings_open")["rows"]
        findings_out = [
            {
                "severity": r[0], "drift_signal": r[1], "finding_type": r[2],
                "scope": r[3], "description": r[4], "timestamp": str(r[5]),
                "tier": r[6],
            }
            for r in open_rows
        ]
    else:
        findings_out = []
        n_events = 0

    engine.close()

    # Per-source event counts (proxy for collector health)
    by_source: dict[str, int] = {}
    for ev in events:
        by_source[ev["source"]] = by_source.get(ev["source"], 0) + 1

    return {
        "backend": "control-centre",
        "control_centre_path": str(root),
        "fast_mode": fast,
        "events_total": n_events,
        "events_by_source": by_source,
        "events": events,
        "findings": findings_out,
        "collector_errors": collector_errors,
    }
