# PCO Layers + Lens Selector + Production Law — Implementation Brief

TIER: STRUCTURED
PROVENANCE: session `4a26d8c1` (2026-06-16 to 22, 30 turns)
STATUS: doctrine landed in skills/memory; the PCO/Lens *primitives* not yet wired; `intent-interface` carries the intent-certainty system
FOR: M5 watcher

## What exists

Six token-efficiency practices + a **three-layer stack**:

1. **Deterministic floor** — same input → same output, no LLM in the loop. (Same layer as `deterministic-core` brief.)
2. **Context selection** — only the tokens that earn their place this turn.
3. **Routing/governor** — credit-first router with budget guard. (Same as token-eff `estate-token-router`.)

### Production Law

> No work unit ends on "built" or "pushed" without proof of life or a verified open-outcome handoff.

Two terminal states only: **landed (running)** OR **surfaced as unfinished outcome on the board**. No silent dead-ends. — This is the same gate as token-eff §C6 and §9.

### Intent-certainty system (verified live)

- Lives in TypeScript `intent-interface`.
- `markPass.ts` marks certainty **1-9** and **ambiguity/metaphor with ▲** before appending verbatim/reformatted text to Vellum.
- **The 1-9 rating and ▲ symbol are ON.** Verified by reading the code.

### Research pipe pattern

**broad → narrow → broad → narrow** until **GO** or **STOP**. **STOP is a valid negative outcome.**

### Not found (verified absent at scan time)

- The de-bias/model-agnostic normaliser was **searched for, not found**. Either not built or not in the searched surfaces.

## What was done

- Strategy consolidated.
- `intent-interface` code read; certainty system confirmed live.
- Normaliser searched; absence recorded.
- Production Law named.

## What it means

- **Token-eff's vocabulary is partially the same idea under different names:**
  - PCO three-layer stack ≈ token-eff §3 four axes (PROCEDURAL / MODEL-IDE / ROUTING / CENTRAL). PCO collapses MODEL-IDE + CENTRAL into "context selection"; both correct.
  - Production Law ≡ token-eff §C6 Production-Law gate + §9 PROOF-OF-LIFE.
  - Lens selector — not in the inbox at all. Open question whether it's a different primitive or the routing layer renamed.
- **Intent-certainty (1-9 + ▲) is upstream of every Vellum event.** The harness's `harness_event` schema should carry it as a first-class field. It is not currently in `amplified_rules.json` or `amplified_harness.py`.
- **The normaliser absence is a real gap** — model-agnostic input normalisation was promised as a step in the voice-first loop (`voice-first-token-efficiency` Step 2: cheap cleanup). The cleanup pass exists in design; the deeper *normaliser* (de-bias, model-agnostic) does not.

## What to change next

1. **Adopt the certainty-1-9 + ▲ field** in `harness_event` and Vellum events. Update `amplified_rules.json` schema and the JSONL drafts.
2. **Reconcile vocabulary** in one short addendum: PCO three-layer ↔ token-eff four-axis; Production Law ↔ §C6/§9.
3. **Decide Lens selector status** — is it the routing layer renamed, or a separate primitive between routing and the agent? (Ewan, one line.)
4. **Build the normaliser** — designed in `voice-first-token-efficiency` Step 2 + 3 (clean → idealise). The deeper de-bias / model-agnostic shape is the gap; token-eff Step 2 covers de-rambling but not de-bias.
5. **`intent-interface` is the only user door** (cross-confirmed in session `022ae58e`) — ensure the Cockpit decision (`80962bca`) lands here.

## Not yet verified

- Whether the Lens selector exists in code under a different name.
- Whether `markPass.ts` is wired live in current Cockpit / Intent Interface deployment.
- Whether the normaliser was started elsewhere.

[CLOSURE] branch=PLAN | proxy=1 logged | gates=Lens-selector status clarification (Ewan, one line) | inbox=pco-layers-lens-selector__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
