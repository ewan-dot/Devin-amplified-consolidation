# Open-Door Universal Harness — Implementation Brief

TIER: STRUCTURED
PROVENANCE: session `94681082` (2026-06-22, 22 turns); harness dossier 2026-05-16 referenced as prior art; constitutional gate engine `epistemic_status.py` + `epistemic_status_invariant.py` cited in session `3ae460be`
STATUS: designed, prior art exists, not yet wired
FOR: M5 watcher

## What exists

The "blinkers without ceilings" universal harness — distinct from the inbox's `amplified_harness.py` (which is the *permission classifier*, not this).

Components (named, prior-art-backed, not built into one runnable thing yet):

- **Baton** — single write lease across the estate. One agent holds the baton; only the baton-holder may write. Logged door-open events on hand-off.
- **RodGuard** — circuit-breaker kill switch. When any of the 5 rods is violated (or a P0 fires), RodGuard trips and refuses writes until cleared.
- **Claude Code as keyholder** — orders work, admits other agents through bounded doors. Single macOS user model; not per-agent macOS users.
- **Separate telemetry planes** — Langfuse (cost/latency/attribution) ≠ Vellum (immutable attributed ledger). Do not collapse.
- **Apple Containers** for cell isolation (matches sovereign-build).
- **Constitutional gate** (from session `3ae460be`): `harness_event` schema with `approval_tier` and `drift_signal` GREEN/AMBER/RED/BLACK; `StatusedValue` + min-rule + `P0Incident`-on-laundering; `DriftDetector`.

## What was done

- Architecture collapsed onto Vellum primitives (Baton, RodGuard, logged events).
- DeerFlow-on-Beast trial brief produced (LiteLLM + Langfuse) — explicitly NOT v1 foundation, experimental layer.
- Attribution corrected: 7-month deliberate partnership with substantial AI contribution.

## What it means

- **Name collision with the inbox.** `amplified_harness.py` in the inbox classifies actions A/B/C. The "open-door harness" here is the broader Baton+RodGuard+constitutional-gate runtime. Two different things; same word. If the M5 watcher implements one and assumes the other, you get a phantom layer.
- **The constitutional gate engine already exists** (`epistemic_status*.py`) — this is the spine. The 8 constitutional predicates extend it, not a fresh build.
- **Token-eff §C6 Production-Law gate** is one face of this same machine — every outcome lands or surfaces as unfinished. Same engine, different UI.

## What to change next

1. **Rename to disambiguate.** `amplified_harness.py` → `amplified_permissions.py` OR rename this one to `open_door_runtime/`. Either; not both with one word.
2. **Land the Baton design** as an explicit artifact — single write lease semantics, hand-off protocol, idle-timeout, contention rule.
3. **Wire RodGuard to the 5 rods + win-win gate + privacy/security/sovereignty** from `amplified-constitution`. Trip conditions deterministic.
4. **Confirm `epistemic_status.py` + `epistemic_status_invariant.py`** location in the repo so Claude Code can extend, not rebuild.
5. **Publish the door-open event schema** so Vellum can index every admission.
6. **Decide DeerFlow scope** — trial on Beast only, never on Mac trust root. Land a one-line keep/kill after the trial.

## Not yet verified

- Whether `epistemic_status*.py` is current and matches the harness dossier shape.
- Whether the inbox's harness was intended to grow into this or is a separate concern.
- Live state of any RodGuard / Baton implementation (architecture only at this point).

[CLOSURE] branch=PLAN | proxy=1 logged | gates=name-disambiguation (Ewan-ratify) + decide DeerFlow keep/kill after trial | inbox=open-door-harness__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
