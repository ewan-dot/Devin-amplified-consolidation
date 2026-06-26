"""Local deterministic collectors — run without control-centre or Beast SSH.

Always available on the Mac: inbox stats, nest log age, ingest health probe,
deterministic-patches ledger size, Vellum /health (no JWT).
"""

from __future__ import annotations

import json
import ssl
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

INBOX_PATH = Path(__file__).resolve().parent.parent
NEST_ROOT = INBOX_PATH.parent / "perplexity-nest"
PATCHES_PATH = INBOX_PATH / "deterministic-patches.jsonl"

VELLUM_HEALTH_URL = "https://vellum.beast.amplifiedpartners.ai/health"
INGEST_HEALTH_URL = "https://perplexity-ingest.beast.amplifiedpartners.ai/health"

_SSL = ssl.create_default_context()
_SSL.check_hostname = False
_SSL.verify_mode = ssl.CERT_NONE


def _event(source: str, metric: str, scope: str, value_num=None,
           value_text=None, raw_json=None) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "source": source,
        "metric": metric,
        "scope": scope,
        "value_num": value_num,
        "value_text": value_text,
        "tier": "MEASURED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "collector_ver": "unified_sensor/local v0.1.0",
        "raw_json": raw_json,
    }


def _probe_health(url: str, scope: str, source: str) -> dict:
    metric = f"{source}_endpoint_up"
    try:
        ctx = _SSL if url.startswith("https") else None
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=8, context=ctx) as resp:
            body = resp.read().decode()[:200]
            return _event(source, metric, scope, value_num=1, value_text="ok",
                          raw_json={"url": url, "response": body})
    except (HTTPError, URLError, Exception) as e:
        return _event(source, metric, scope, value_num=0, value_text=str(e),
                      raw_json={"url": url, "error": str(e)})


def collect_inbox_local() -> Iterator[dict]:
    """Perplexity-inbox file stats."""
    if not INBOX_PATH.is_dir():
        yield _event("inbox_local", "inbox_missing", "perplexity-inbox",
                     value_num=0, value_text="inbox path not found")
        return

    md_files = sorted(
        [f for f in INBOX_PATH.rglob("*.md") if f.is_file()],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    yield _event("inbox_local", "inbox_file_count", "perplexity-inbox",
                 value_num=len(md_files),
                 value_text=f"{len(md_files)} markdown artifacts")

    if md_files:
        newest = md_files[0]
        hours = round(
            (datetime.now(timezone.utc).timestamp() - newest.stat().st_mtime) / 3600, 2
        )
        yield _event("inbox_local", "inbox_newest_hours", "perplexity-inbox",
                     value_num=hours, value_text=newest.name,
                     raw_json={"file": newest.name, "hours_ago": hours})


def collect_nest_local() -> Iterator[dict]:
    """perplexity-nest log freshness."""
    log_path = NEST_ROOT / "logs" / "nest.log"
    if not log_path.exists():
        yield _event("inbox_local", "nest_log_missing", "perplexity-nest",
                     value_num=-1, value_text="nest.log not found")
        return
    hours = round(
        (datetime.now(timezone.utc).timestamp() - log_path.stat().st_mtime) / 3600, 2
    )
    yield _event("inbox_local", "nest_last_run_hours", "perplexity-nest",
                 value_num=hours, value_text=f"{hours:.1f}h since nest run")


def collect_patches_local() -> Iterator[dict]:
    """deterministic-patches.jsonl — cross-IDE problem registry size."""
    if not PATCHES_PATH.exists():
        yield _event("inbox_local", "patches_count", "deterministic-patches",
                     value_num=0, value_text="no patches file")
        return
    lines = [l for l in PATCHES_PATH.read_text(errors="replace").splitlines() if l.strip()]
    yield _event("inbox_local", "patches_count", "deterministic-patches",
                 value_num=len(lines), value_text=f"{len(lines)} patch records")


def collect_endpoint_probes() -> Iterator[dict]:
    """HTTP health probes — no auth required."""
    yield _probe_health(VELLUM_HEALTH_URL, "vellum", "vellum")
    yield _probe_health(INGEST_HEALTH_URL, "beast-ingest", "ingestion_pipe")


def collect_all_local() -> list[dict]:
    events: list[dict] = []
    for gen in (collect_inbox_local, collect_nest_local,
                collect_patches_local, collect_endpoint_probes):
        events.extend(list(gen()))
    return events


def apply_local_rules(events: list[dict]) -> list[dict]:
    """Minimal deterministic rules when control-centre is unavailable."""
    findings: list[dict] = []
    now = datetime.now(timezone.utc).isoformat()

    def _finding(sev, sig, ftype, scope, desc, metric):
        findings.append({
            "severity": sev, "drift_signal": sig, "finding_type": ftype,
            "scope": scope, "description": desc, "timestamp": now, "tier": "STRUCTURED",
            "metadata": {"metric": metric, "source": "unified_sensor/local"},
        })

    for ev in events:
        metric = ev.get("metric", "")
        val = ev.get("value_num")
        scope = ev.get("scope", "")

        if metric.endswith("_endpoint_up") and val == 0:
            _finding("RED", "RED", "automation_liveness", scope,
                     f"Endpoint down: {ev.get('value_text', '')}", metric)

        if metric == "nest_last_run_hours" and val is not None and val > 48:
            _finding("AMBER", "AMBER", "automation_liveness", scope,
                     f"perplexity-nest stale ({val:.0f}h since run)", metric)

        if metric == "nest_log_missing":
            _finding("AMBER", "AMBER", "automation_liveness", "perplexity-nest",
                     "nest.log missing — nest may never have run", metric)

    return findings
