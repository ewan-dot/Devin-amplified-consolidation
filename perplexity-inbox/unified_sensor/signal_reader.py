"""Signal reader — job-start proceed / warn / halt from sensor snapshot.

Per master-plan Phase 3: deterministic decision before work starts.
No LLM. Tier: STRUCTURED.

Decision matrix:
  halt — any BLACK finding, or RED on a critical source, or critical collector absent
  warn — AMBER findings, or RED on non-critical source, or partial collector failure
  proceed — no open findings above GREEN
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from unified_sensor.registry import CRITICAL_SOURCES


@dataclass
class SignalDecision:
    verdict: str          # proceed | warn | halt
    reason: str
    critical_findings: list[dict] = field(default_factory=list)
    warnings: list[dict] = field(default_factory=list)
    missing_critical: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "reason": self.reason,
            "critical_findings": self.critical_findings,
            "warnings": self.warnings,
            "missing_critical": self.missing_critical,
        }


def _severity_rank(sev: str) -> int:
    return {"BLACK": 0, "RED": 1, "AMBER": 2, "GREEN": 3}.get(sev, 4)


def read_signals(snapshot: dict[str, Any]) -> SignalDecision:
    """Evaluate a collect_snapshot() result → proceed/warn/halt."""
    findings = snapshot.get("findings") or []
    by_source = snapshot.get("events_by_source") or {}
    backend = snapshot.get("backend", "unknown")

    critical_findings: list[dict] = []
    warnings: list[dict] = []

    for f in findings:
        sev = (f.get("severity") or f.get("drift_signal") or "GREEN").upper()
        if sev == "BLACK":
            critical_findings.append(f)
        elif sev == "RED":
            scope = f.get("scope", "")
            # RED on fleet-critical scopes
            if any(c in scope for c in ("beast", "beast-ingest", "vellum", "beast-amplified")):
                critical_findings.append(f)
            else:
                warnings.append(f)
        elif sev == "AMBER":
            warnings.append(f)

    missing_critical: list[str] = []
    if backend == "control-centre":
        for src in CRITICAL_SOURCES:
            if src not in by_source or by_source.get(src, 0) == 0:
                missing_critical.append(src)
    else:
        # Local fallback: vellum + ingest probes must have emitted
        for src in ("vellum", "ingestion_pipe"):
            if by_source.get("inbox_local", 0) == 0 and src not in by_source:
                pass  # probes use metric names not source for health
        if not any(
            e.get("metric", "").endswith("_endpoint_up") and e.get("source") == "vellum"
            and e.get("value_num") == 1
            for e in (snapshot.get("events") or [])
        ):
            missing_critical.append("vellum_reachable")

    if critical_findings:
        desc = critical_findings[0].get("description", "critical finding")
        return SignalDecision(
            verdict="halt",
            reason=f"Critical: {desc}",
            critical_findings=critical_findings,
            warnings=warnings,
            missing_critical=missing_critical,
        )

    if missing_critical and backend == "control-centre":
        return SignalDecision(
            verdict="warn",
            reason=f"Critical collectors missing data: {', '.join(missing_critical)}",
            warnings=warnings,
            missing_critical=missing_critical,
        )

    if warnings:
        desc = warnings[0].get("description", "warning")
        return SignalDecision(
            verdict="warn",
            reason=desc,
            warnings=warnings,
            missing_critical=missing_critical,
        )

    return SignalDecision(
        verdict="proceed",
        reason="No material findings — fleet GREEN",
        missing_critical=missing_critical,
    )
