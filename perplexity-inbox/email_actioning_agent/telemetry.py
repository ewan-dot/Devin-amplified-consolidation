"""
telemetry.py — observability on everything (deterministic).

Principle: if it breaks, we must know — with a fallback and a fix path.

Every run produces a RunReport with a health verdict:
  OK       — ran clean, all configured-authed inboxes captured, no errors
  DEGRADED — ran, but something is off (stale capture, unauthed inbox, Vellum
             witness unreachable, classifier errors on some rows). Still usable.
  FAILED   — could not run (no adapters, no captured mail, unhandled exception).

Witnessing is two-tier and never silent:
  1. LOCAL witness (always) — append-only JSONL at config.TELEMETRY_JSONL plus a
     latest-health snapshot at config.HEALTH_JSON. This is the fallback; it works
     with zero network and zero secrets.
  2. VELLUM witness (best-effort) — POST to an env-configured endpoint. If env is
     missing or the POST fails, that is itself recorded as a DEGRADED signal in the
     local witness; it never crashes the run and never blocks actioning.

No secrets in code: Vellum config comes from env (see RUNBOOK.md):
  EAA_VELLUM_URL    e.g. https://vellum-mcp.beast.amplifiedpartners.ai/api/v1/agents/cascade-mac/send
  EAA_VELLUM_TOKEN  bearer token
  EAA_VELLUM_AUTHOR e.g. cascade-mac
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import config


@dataclass
class RunReport:
    run_id: str
    ts: str
    n_emails: int
    inboxes_authed: int
    inboxes_configured: int
    by_category: dict
    by_tier: dict
    deterministic: int
    needs_ai: int
    deterministic_pct: float
    tier_c_pending: int          # gated action-requests awaiting a human
    tokens: dict
    subscriptions: dict = field(default_factory=dict)   # recurring-spend inventory summary
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    health: str = "OK"
    vellum_witnessed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def health_verdict(report: RunReport) -> str:
    if report.errors or report.n_emails == 0 or report.inboxes_configured == 0:
        return "FAILED" if (report.n_emails == 0 or report.errors) else "DEGRADED"
    if report.warnings:
        return "DEGRADED"
    return "OK"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _vellum_witness(report: RunReport) -> tuple[bool, str | None]:
    url = os.environ.get("EAA_VELLUM_URL")
    token = os.environ.get("EAA_VELLUM_TOKEN")
    author = os.environ.get("EAA_VELLUM_AUTHOR", "cascade-mac")
    if not url or not token:
        return False, "EAA_VELLUM_URL/TOKEN not set — local witness only"
    payload = {
        "author": author,
        "content": (f"email-actioning-agent run {report.run_id}: health={report.health} "
                    f"n={report.n_emails} deterministic={report.deterministic_pct}% "
                    f"needs_ai={report.needs_ai} tier_c_pending={report.tier_c_pending} "
                    f"saving/email={report.tokens.get('per_email_saving_pct')}%"),
        "entry_type": "agent_write", "epistemic_tier": "MEASURED",
        "message_type": "info",
        "metadata": {"surface": "email-actioning-agent", "run_id": report.run_id,
                     "health": report.health, "report": report.to_dict()},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return (200 <= resp.status < 300), f"HTTP {resp.status}"
    except (urllib.error.URLError, OSError, ValueError) as ex:
        return False, f"vellum POST failed: {ex}"


def emit(report: RunReport) -> RunReport:
    """Finalise health, write the local witness (always), best-effort Vellum."""
    report.health = health_verdict(report)

    ok, detail = _vellum_witness(report)
    report.vellum_witnessed = ok
    if not ok:
        report.warnings.append(f"vellum_witness_skipped: {detail}")
        # re-evaluate: a skipped witness degrades an otherwise-OK run
        if report.health == "OK":
            report.health = "DEGRADED"

    config.TELEMETRY_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with config.TELEMETRY_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report.to_dict(), ensure_ascii=False) + "\n")
    config.HEALTH_JSON.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return report
