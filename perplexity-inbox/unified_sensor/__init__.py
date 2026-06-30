"""Unified sensor — deterministic fleet signals for Perplexity monitoring.

Signals converge here before Perplexity reads them. No LLM in the gather path.
Tier: STRUCTURED (collector output MEASURED; findings STRUCTURED).

Usage:
    from unified_sensor import collect_snapshot, read_signals

    snap = collect_snapshot()
    decision = read_signals(snap)  # proceed | warn | halt
"""

from unified_sensor.snapshot import collect_snapshot, write_snapshot
from unified_sensor.signal_reader import read_signals, SignalDecision

__all__ = ["collect_snapshot", "write_snapshot", "read_signals", "SignalDecision"]
