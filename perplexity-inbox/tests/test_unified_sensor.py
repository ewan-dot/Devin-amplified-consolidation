"""Tests for unified_sensor — stdlib only, no network."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unified_sensor.signal_reader import read_signals
from unified_sensor.local_collectors import apply_local_rules


def _snap(findings=None, events=None, by_source=None, backend="local"):
    return {
        "backend": backend,
        "findings": findings or [],
        "events": events or [],
        "events_by_source": by_source or {},
    }


def test_proceed_when_clean():
    d = read_signals(_snap())
    assert d.verdict == "proceed"


def test_halt_on_black():
    d = read_signals(_snap(findings=[{
        "severity": "BLACK", "drift_signal": "BLACK",
        "description": "tier laundering", "scope": "test",
    }]))
    assert d.verdict == "halt"


def test_halt_on_red_beast():
    d = read_signals(_snap(findings=[{
        "severity": "RED", "drift_signal": "RED",
        "description": "ingest down", "scope": "beast-ingest",
    }]))
    assert d.verdict == "halt"


def test_warn_on_amber():
    d = read_signals(_snap(findings=[{
        "severity": "AMBER", "drift_signal": "AMBER",
        "description": "nest stale", "scope": "perplexity-nest",
    }]))
    assert d.verdict == "warn"


def test_local_rule_endpoint_down():
    events = [{
        "metric": "vellum_endpoint_up", "value_num": 0,
        "value_text": "connection refused", "scope": "vellum", "source": "vellum",
    }]
    findings = apply_local_rules(events)
    assert len(findings) == 1
    assert findings[0]["severity"] == "RED"


def test_local_rule_nest_stale():
    events = [{
        "metric": "nest_last_run_hours", "value_num": 72,
        "scope": "perplexity-nest", "source": "inbox_local",
    }]
    findings = apply_local_rules(events)
    assert len(findings) == 1
    assert findings[0]["severity"] == "AMBER"


if __name__ == "__main__":
    tests = [
        test_proceed_when_clean,
        test_halt_on_black,
        test_halt_on_red_beast,
        test_warn_on_amber,
        test_local_rule_endpoint_down,
        test_local_rule_nest_stale,
    ]
    ok = True
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            ok = False
    raise SystemExit(0 if ok else 1)
