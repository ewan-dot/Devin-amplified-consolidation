"""Sensor source registry — every deterministic collector Perplexity monitors.

Each entry: name, description, requires (optional deps), critical flag.
Critical sources failing → signal_reader may halt; non-critical → warn only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SensorSource:
    name: str
    description: str
    critical: bool = False
    requires_control_centre: bool = False


# Canonical sensor catalogue — matches control-centre collectors + local fallbacks.
SENSOR_SOURCES: tuple[SensorSource, ...] = (
    SensorSource("vellum", "Vellum ledger: agents, inbox volume, tier mix", critical=True),
    SensorSource("ingestion_pipe", "perplexity-nest + inbox + Beast ingest health", critical=True),
    SensorSource("tailscale", "Fleet mesh reachability (Beast, WanMini, M5)", critical=True),
    SensorSource("credentials", "JWT freshness + keys.env presence", critical=True),
    SensorSource("github", "Org repo health (branch protection, PRs, CI)", requires_control_centre=True),
    SensorSource("litellm", "LiteLLM spend + model availability", requires_control_centre=True),
    SensorSource("brain", "amplified_brain row counts + ingest lag", requires_control_centre=True),
    SensorSource("baton", "agent-claude git activity + BATON task count"),
    SensorSource("inbox_local", "Local perplexity-inbox file stats (always available)"),
)

SOURCE_NAMES = tuple(s.name for s in SENSOR_SOURCES)
CRITICAL_SOURCES = frozenset(s.name for s in SENSOR_SOURCES if s.critical)
