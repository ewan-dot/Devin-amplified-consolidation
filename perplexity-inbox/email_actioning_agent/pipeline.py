"""
pipeline.py — fetch -> classify -> extract -> route -> emit -> measure -> witness.

Runs entirely as deterministic code over captured real mail. Only the compact
routed rows are the thing that would cross into model context under a code-
execution runtime, and a model is invoked only for the `needs_ai` residue.

Every run is wrapped so a failure in one step is captured as an error/warning and
witnessed (telemetry.emit) rather than crashing silently.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

from . import config
from .classifier import classify
from .emit import emit_infra_feed, write_jsonl
from .extract import extract_financial, extract_infra
from .router import route_all
from .servers.base import Email, load_adapter
from .telemetry import RunReport, _now, emit as emit_telemetry
from .tokens import measure


@dataclass
class RunResult:
    report: RunReport
    routed: list
    measurement: object
    applied: bool

    def summary(self) -> dict:
        return self.report.to_dict()


def _classifier_source() -> str:
    # The deterministic decision surface loaded once in a code-exec model.
    return (Path(__file__).with_name("classifier.py")).read_text(encoding="utf-8")


def _run_id() -> str:
    return "eaa-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())


def run(capture_jsonl: str | Path = config.CAPTURE_JSONL,
        limit: int = 100, apply: bool = False) -> RunResult:
    capture_jsonl = Path(capture_jsonl)
    errors: list = []
    warnings: list = []

    # 1) fetch — one adapter per inbox; only authed inboxes have captured mail.
    adapters_by_inbox = {ib.key: load_adapter(ib.key, capture_jsonl) for ib in config.INBOXES}
    for ib in config.INBOXES:
        if not ib.authed:
            warnings.append(f"inbox_unauthed: {ib.key} ({ib.address}) — capture deferred")
    emails: list[Email] = []
    for key, ad in adapters_by_inbox.items():
        try:
            emails.extend(ad.fetch(limit=limit))
        except Exception as ex:                       # never let one adapter sink the run
            errors.append(f"fetch_failed:{key}:{ex}")
    emails_by_id = {e.msg_id: e for e in emails}

    # 2) classify — deterministic.
    classifications = []
    for e in emails:
        try:
            classifications.append(classify(e))
        except Exception as ex:
            errors.append(f"classify_failed:{e.msg_id}:{ex}")

    # 3) route — decision-first; mutations only under apply, Tier C always gated.
    routed = route_all(classifications, emails_by_id, adapters_by_inbox, apply=apply)

    # 4) extract (deterministic) + emit — Tier A inbox-local JSONL.
    infra_rows = emit_infra_feed(config.INFRA_FEED_JSONL, classifications, emails_by_id)
    enriched = []
    for c, r in zip(classifications, routed):
        e = emails_by_id.get(c.msg_id)
        row = {**c.to_dict(), "route": r.route, "tier": r.tier, "performed": r.performed}
        if e is not None and c.category == "INFRA_CRITICAL":
            row["extracted"] = extract_infra(e)
        elif e is not None and c.category == "FINANCIAL":
            row["extracted"] = extract_financial(e)
        enriched.append(row)
    write_jsonl(config.ROUTED_JSONL, enriched)

    # 5) measure — real tokens on the REAL FULL-body subset (honest baseline).
    by_id_class = {c.msg_id: c for c in classifications}
    by_id_routed = {r.msg_id: r for r in routed}

    def compact(e):
        c = by_id_class[e.msg_id]; r = by_id_routed[e.msg_id]
        return {**c.to_dict(), "route": r.route, "tier": r.tier}

    full_emails = [e for e in emails if e.headers.get("body_source") == "full"]
    measure_set = full_emails or emails
    m = (measure(measure_set, [compact(e) for e in measure_set], classifier_source=_classifier_source())
         if measure_set else None)
    if m is not None:
        config.MEASUREMENT_JSON.parent.mkdir(parents=True, exist_ok=True)
        config.MEASUREMENT_JSON.write_text(m.to_json(), encoding="utf-8")

    # ---- aggregate + determinism stats ----
    by_category: dict = {}
    by_tier: dict = {}
    det = ai = 0
    for c in classifications:
        by_category[c.category] = by_category.get(c.category, 0) + 1
        by_tier[c.work_tier] = by_tier.get(c.work_tier, 0) + 1
        if c.needs_ai:
            ai += 1
        else:
            det += 1
    n = len(classifications)
    det_pct = round(det / n * 100.0, 2) if n else 0.0
    tier_c_pending = sum(1 for r in routed if r.tier == "C")

    authed = sum(1 for ib in config.INBOXES if ib.authed)

    report = RunReport(
        run_id=_run_id(), ts=_now(), n_emails=len(emails),
        inboxes_authed=authed, inboxes_configured=len(config.INBOXES),
        by_category=by_category, by_tier=by_tier,
        deterministic=det, needs_ai=ai, deterministic_pct=det_pct,
        tier_c_pending=tier_c_pending,
        tokens=(json.loads(m.to_json()) if m is not None else {}),
        errors=errors, warnings=warnings,
    )
    report = emit_telemetry(report)          # local witness always + best-effort Vellum
    return RunResult(report=report, routed=routed, measurement=m, applied=apply)
