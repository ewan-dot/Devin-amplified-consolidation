# DeerFlow Trial — Implementation Brief

TIER: STRUCTURED
PROVENANCE: sessions `94681082` (2026-06-22, 22t — DeerFlow-on-Beast trial brief produced), `022ae58e` (2026-06-23, 6t — DeerFlow not v1 foundation)
STATUS: designed; not yet trialled; one open Q1 unresolved
FOR: M5 watcher

## What exists

### Decisions (Ewan + session)

- **DeerFlow = ByteDance harness experiment**, trialled on the **Beast** via **LiteLLM + Langfuse**.
- **Not on the Mac trust root.** Trial only.
- **Not the v1 foundation.** A peer harness for evaluation, not a replacement for the open-door harness / Relay/Vellum spine.
- **Why Beast not Mac:** isolation; the Mac is the trust root and cannot host an experimental harness.

### Open question Q1 (`022ae58e`)

> *"What is 'DeerFlow' in this build?"* — Claude found three readings and needs the disambiguating answer. **Not resolved before session ended.**

## What was done

- Trial brief drafted (session `94681082`).
- Routing decided: Beast, via LiteLLM, telemetered through Langfuse (overlap with Opik on traces noted but kept separate).
- v1-vs-experiment boundary stated.

## What it means

- **DeerFlow is a one-trial experiment.** Either it earns its place in the routing layer, or it gets killed. The Production Law (`pco-layers-lens-selector` brief) demands a landed outcome or a surfaced unfinished one — DeerFlow has neither.
- **It uses LiteLLM**, the same router as `estate-token-router` (per mesh-plan S2). Single LiteLLM instance; DeerFlow becomes a sub-routing pattern under it, not a parallel stack.
- **Langfuse telemetry for DeerFlow** flows into the same callback path the deterministic core reads. No new pipe.

## What to change next

1. **Resolve Q1** — which of the three DeerFlow readings is in scope. (Ewan, one line.)
2. **Run the trial.** One concrete task end-to-end on the Beast, telemetered. Capture cost / latency / output quality / failure shape.
3. **Decide keep-or-kill** at trial end. Single decision; either folded into the routing layer with a documented use-case, or surfaced as unfinished-outcome with the reason.
4. **No Mac-trust-root invocation.** Enforced at the router config layer.

## Not yet verified

- Q1 disambiguation.
- Current DeerFlow release stability.
- Whether existing LiteLLM config can route to DeerFlow without modification.

## Tier C gates (Ewan only)

- Q1 disambiguation.
- Trial scope (which task class).

[CLOSURE] branch=PLAN | proxy=1 logged | gates=Q1 + trial scope (Ewan, one hand-back) | inbox=deerflow-trial__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
