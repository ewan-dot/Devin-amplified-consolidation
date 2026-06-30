#!/usr/bin/env python3
"""Perplexity fleet monitor — unified sensor CLI.

Gathers deterministic signals (Vellum, ingestion pipe, Tailscale, credentials,
GitHub, LiteLLM, brain, BATON) and renders what Perplexity should read.

No LLM in path. Tier: STRUCTURED.

Usage:
    python3 monitor.py                  # collect + render terminal summary
    python3 monitor.py --json           # JSON for Perplexity ingestion
    python3 monitor.py --signals-only   # proceed/warn/halt decision only
    python3 monitor.py --write-snapshot # persist data/sensor_snapshot.json
    python3 monitor.py --no-collect     # read last snapshot + decide
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from unified_sensor.signal_reader import read_signals
from unified_sensor.snapshot import collect_snapshot, load_snapshot, write_snapshot, DEFAULT_SNAPSHOT_PATH


def _colour(sev: str, text: str) -> str:
    if not sys.stdout.isatty():
        return text
    codes = {"BLACK": "\033[41m\033[97m", "RED": "\033[31m",
             "AMBER": "\033[33m", "GREEN": "\033[32m"}
    return f"{codes.get(sev, '')}{text}\033[0m"


def render_terminal(snap: dict, decision) -> None:
    print(f"\n{'═'*58}")
    print(f"  UNIFIED SENSOR — {snap.get('generated_at', '?')}")
    print(f"  backend: {snap.get('backend')}   events: {snap.get('events_total', 0)}")
    print(f"  findings: {snap.get('findings_open', 0)} open "
          f"({snap.get('findings_critical', 0)} critical)")
    sig_colour = (
        "RED" if decision.verdict == "halt"
        else "AMBER" if decision.verdict == "warn"
        else "GREEN"
    )
    print(f"  signal: {_colour(sig_colour, decision.verdict.upper())}")
    print(f"  reason: {decision.reason}")
    print()

    findings = snap.get("findings") or []
    if findings:
        print("  FINDINGS")
        for f in sorted(findings, key=lambda x: _severity_rank(x.get("severity", "GREEN"))):
            sev = f.get("severity", "?")
            print(f"    {_colour(sev, sev):<8} {f.get('scope', ''):<24} {f.get('description', '')[:55]}")
    else:
        print("  ✓ No open findings")

    by_source = snap.get("events_by_source") or {}
    if by_source:
        print("\n  COLLECTORS")
        for src, cnt in sorted(by_source.items()):
            print(f"    {src:<16} {cnt} events")

    print(f"\n{'═'*58}\n")


def _severity_rank(sev: str) -> int:
    return {"BLACK": 0, "RED": 1, "AMBER": 2}.get(sev, 3)


def main() -> int:
    p = argparse.ArgumentParser(description="Perplexity unified sensor monitor")
    p.add_argument("--json", action="store_true", help="Full snapshot as JSON")
    p.add_argument("--signals-only", action="store_true", help="Signal decision JSON only")
    p.add_argument("--full", action="store_true",
                   help="Full collect incl. all GitHub org repos (slow)")
    p.add_argument("--write-snapshot", action="store_true",
                   help="Write data/sensor_snapshot.json")
    p.add_argument("--no-collect", action="store_true",
                   help="Use last snapshot instead of re-collecting")
    args = p.parse_args()

    fast = not args.full

    if args.write_snapshot and args.no_collect:
        path = write_snapshot(fast=fast)
        print(f"Snapshot written: {path}", file=sys.stderr)

    if args.no_collect:
        snap = load_snapshot()
    else:
        print("Collecting sensors...", file=sys.stderr)
        snap = collect_snapshot(fast=fast)
        if not args.no_collect:
            out = DEFAULT_SNAPSHOT_PATH
            out.parent.mkdir(parents=True, exist_ok=True)
            import json as _json
            out.write_text(_json.dumps(snap, indent=2, default=str), encoding="utf-8")

    decision = read_signals(snap)

    if args.signals_only:
        print(json.dumps(decision.to_dict(), indent=2))
    elif args.json:
        out = {**snap, "signal_decision": decision.to_dict()}
        print(json.dumps(out, indent=2, default=str))
    else:
        render_terminal(snap, decision)

    return 2 if decision.verdict == "halt" else (1 if decision.verdict == "warn" else 0)


if __name__ == "__main__":
    raise SystemExit(main())
