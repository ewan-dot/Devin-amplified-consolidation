# Vellum Senses — Implementation Brief

TIER: STRUCTURED (existence MEASURED — file located and read via Spotlight content-search)
PROVENANCE: session `7dd0ce64` (2026-06-21, 22 turns); harness dossier referenced
STATUS: code located; not yet documented as an inbox artifact
FOR: M5 watcher

## What exists

- **`/Users/ewansair/Antigravity/vellum/vellum/models/sensor_event.py`** — the Vellum senses / sensor-event model. Verified via Spotlight content-search on `context_threshold_reached`.
- The local clone in `~/Antigravity/vellum/` = the GitHub `fleet-vellum` repo. Same code; different checkout.
- From the harness dossier (2026-05-16): the `harness_event` schema includes `approval_tier` and `drift_signal` GREEN / AMBER / RED / BLACK. Senses are the signals that drive `drift_signal`.

## What was done

- File located after a failed first search (`mdfind "vellum sensors"` returned nothing; content-search on a known string found it).
- Confirmed Vellum sensor code is **on the M5**, not just on the Beast.
- Identified the Spotlight indexing reliability issue (`mdutil -s ~` returned "unknown indexing state") — sensors weren't missing, the index was stale.

## What it means

- **Vellum senses + `harness_event` + `epistemic_status*.py` are three pieces of the same gate engine.** Senses feed signals; harness events carry them; epistemic_status enforces tier-honesty on them.
- **The deterministic core (`deterministic-core` brief) is the consumer** of these senses — it reads cross-source signals and decides what's on fire.
- **`drift_signal`** = the same thing as the min-rule's auto-demotion triggers in machine-readable form. When senses fire RED/BLACK, the consuming layer demotes tier and (per min-rule) the demotion is logged, not hidden.
- **Spotlight is unreliable** until reindexed — this is the trap that made the senses look absent the first time. Real lesson for the M5 watcher: content-search beats name-search until the index is healthy.

## What to change next

1. **Read `sensor_event.py`** end-to-end and produce a one-page reference: every sense, what it watches, what `drift_signal` it raises. (Tier A.)
2. **Map senses → deterministic-core input** — which sense the core reads, which one it ignores, which it logs only.
3. **Wire RED/BLACK senses to RodGuard** (from `open-door-harness` brief). RED warns; BLACK trips.
4. **Confirm `~/Antigravity/vellum/` ↔ `fleet-vellum` main** are in sync. Risk: local edits drift from canonical.
5. **`mdutil -E /`** to make Spotlight reliable (Ewan-only — see `repo-consolidation` brief; same gate).

## Not yet verified

- Full sense list (file located, not yet read line-by-line).
- Whether the local clone has uncommitted divergence from `fleet-vellum` main.
- Whether all senses are currently emitting (some may be defined but not wired).

## Tier C gates (Ewan only)

- Spotlight reindex (same gate as `repo-consolidation` brief — collapse).

[CLOSURE] branch=PLAN | proxy=1 logged | gates=Spotlight reindex (collapsed with repo-consolidation gate) | inbox=vellum-senses__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
