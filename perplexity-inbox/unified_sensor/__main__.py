"""CLI: deterministic snapshot + proceed/warn/halt for Perplexity job-start."""

from __future__ import annotations

import argparse
import json
import sys

from unified_sensor import collect_snapshot, read_signals, write_snapshot


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Unified sensor — fleet snapshot for Perplexity")
    p.add_argument("--local-only", action="store_true", help="Skip control-centre (fast; no GitHub sweep)")
    p.add_argument("--write", action="store_true", help="Write snapshot JSON to data/sensor_snapshot.json")
    p.add_argument("--json", action="store_true", help="Print full snapshot JSON")
    args = p.parse_args(argv)

    snap = collect_snapshot(local_only=args.local_only)
    decision = read_signals(snap)

    if args.write:
        path = write_snapshot(snap)
        print(f"snapshot: {path}", file=sys.stderr)

    out = {
        "verdict": decision.verdict,
        "reason": decision.reason,
        "missing_critical": decision.missing_critical,
        "critical_findings": len(decision.critical_findings),
        "warnings": len(decision.warnings),
        "generated_at": snap.get("generated_at"),
        "backend": snap.get("backend"),
    }

    if args.json:
        out["snapshot"] = snap
        out["decision"] = decision.to_dict()

    print(json.dumps(out, indent=2))
    return 0 if decision.verdict == "proceed" else (1 if decision.verdict == "warn" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
