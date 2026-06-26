"""
CLI / harness for the email-actioning agent.

  python -m email_actioning_agent inboxes        # show configured inboxes + auth state
  python -m email_actioning_agent capture-stub   # print the model-side capture recipe
  python -m email_actioning_agent run [--apply]  # fetch->classify->route->emit->measure
  python -m email_actioning_agent measure        # show last token measurement
  python -m email_actioning_agent scout          # route the brief into the Night Scout feed

`run` defaults to DRY-RUN. --apply performs Tier A/B (inbox-local emit + label/
archive) and logs them; Tier C (external send/Drive) is never auto-run.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import config
from .night_scout import route_brief_to_feed
from .pipeline import run


def _cmd_inboxes(_args) -> int:
    for ib in config.INBOXES:
        state = "AUTHED" if ib.authed else "needs-oauth"
        print(f"{ib.key:10s} {ib.address:32s} [{state:11s}] adapter={ib.adapter}  {ib.note}")
    return 0


def _cmd_capture_stub(_args) -> int:
    from .servers import gmail_mcp
    print(gmail_mcp.__doc__)
    return 0


def _cmd_run(args) -> int:
    if not Path(config.CAPTURE_JSONL).exists():
        print(f"No captured mail at {config.CAPTURE_JSONL}.\n"
              f"Capture real emails first (see `capture-stub`) — we never run on mock data.",
              file=sys.stderr)
        return 2
    res = run(apply=args.apply, limit=args.limit)
    rep = res.report
    print(json.dumps(res.summary(), indent=2))
    print(f"\nHEALTH={rep.health}  deterministic={rep.deterministic}/{rep.n_emails} "
          f"({rep.deterministic_pct}%)  needs_ai={rep.needs_ai}  "
          f"vellum_witnessed={rep.vellum_witnessed}")
    print("Gated (Tier C) action-requests this run (need human authorisation):")
    for r in res.routed:
        if r.tier == "C":
            print(f"  - {r.route:14s} msg={r.msg_id}  gate={r.gate}")
    if not args.apply:
        print("\n[DRY-RUN] no inbox was mutated. Re-run with --apply to perform Tier A/B actions.")
    return 0


def _cmd_health(_args) -> int:
    """Read the latest health snapshot. Exit code: 0 OK, 1 DEGRADED, 2 FAILED/none.
    Usable by cron/launchd and the pre-push hook."""
    if not Path(config.HEALTH_JSON).exists():
        print("FAILED: no health snapshot — run `run` first", file=sys.stderr)
        return 2
    h = json.loads(Path(config.HEALTH_JSON).read_text(encoding="utf-8"))
    verdict = h.get("health", "FAILED")
    print(json.dumps({"health": verdict, "run_id": h.get("run_id"), "ts": h.get("ts"),
                      "n_emails": h.get("n_emails"), "deterministic_pct": h.get("deterministic_pct"),
                      "tier_c_pending": h.get("tier_c_pending"),
                      "vellum_witnessed": h.get("vellum_witnessed"),
                      "errors": h.get("errors"), "warnings": h.get("warnings")}, indent=2))
    return {"OK": 0, "DEGRADED": 1}.get(verdict, 2)


def _cmd_measure(_args) -> int:
    if not Path(config.MEASUREMENT_JSON).exists():
        print("No measurement yet — run `run` first.", file=sys.stderr)
        return 2
    print(Path(config.MEASUREMENT_JSON).read_text(encoding="utf-8"))
    return 0


def _cmd_scout(_args) -> int:
    brief = config.INBOX_SSOT / "claude-gmail-brief.md"
    rec = route_brief_to_feed(brief)
    print(json.dumps(rec, indent=2))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="email_actioning_agent")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inboxes").set_defaults(fn=_cmd_inboxes)
    sub.add_parser("capture-stub").set_defaults(fn=_cmd_capture_stub)
    r = sub.add_parser("run")
    r.add_argument("--apply", action="store_true", help="perform Tier A/B actions (default dry-run)")
    r.add_argument("--limit", type=int, default=100)
    r.set_defaults(fn=_cmd_run)
    sub.add_parser("measure").set_defaults(fn=_cmd_measure)
    sub.add_parser("health").set_defaults(fn=_cmd_health)
    sub.add_parser("scout").set_defaults(fn=_cmd_scout)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
