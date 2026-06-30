# Deterministic Core — Implementation Brief

TIER: STRUCTURED
PROVENANCE: session `3ae460be` (2026-06-24, 7 turns)
STATUS: designed; replica-build started by Perplexity; Claude Code briefed; live wiring blocked on JWTs + dark estate-machine stack
FOR: M5 watcher → Claude Code

## What exists

The architecture in one line: **deterministic core gathers all signals into one Postgres/Vellum pane → Perplexity reads only what's on fire and deciphers cross-source meaning → Vellum summons the correct AI to fix, end-to-end.**

Standing laws (Ewan, this session):

- **Signals converge in a deterministic core before Perplexity reads them.** Perplexity's job is decipherment, not gathering — unless the core can't gather.
- **LLMs build the core; the built core runs without them.** Any LLM in a metric's runtime path caps that metric at INTUITED — the control room would otherwise lie.
- **Self-ratification gate = 5 rods + privacy/security/sovereignty + min-rule.** Pre-decided, deterministic, no LLM in the verdict.
- **Langfuse and Opik are complementary, not interchangeable.** Langfuse → prompt mgmt / versioning / session analytics. Opik → evaluation depth (LLM-as-judge, experiments, guardrails, online eval rules). Metric-ownership map is an OUTPUT the core produces by reading both schemas, not something a human pre-decides.

## What was done

- Spec written; Vellum event drafts produced (JSONL, awaiting pipe commit).
- `harness_event` schema named as canonical (from harness dossier 2026-05-16) — `approval_tier`, `drift_signal` GREEN/AMBER/RED/BLACK.
- Prior art identified — `epistemic_status.py` + `epistemic_status_invariant.py` (existing gate engine: `StatusedValue`, min-rule, `P0Incident`-on-laundering, append-only `StatusRecord`, `DriftDetector`). The 8 constitutional predicates extend this; they do not replace it.
- Replica build started by Perplexity against the read schemas (so the core deploys clean once wired).
- Live probe attempted: Beast public surface returns Traefik default "404 page not found" → **Traefik up, zero routers loaded** → estate-machine service stack is dark.

## What it means

- **The `amplified_rules.json` + `amplified_harness.py` in the inbox are a projection of this core's gate, not the core itself.** Same family; smaller surface.
- The 8 constitutional predicates **layer onto the existing `epistemic_status*.py`** — Claude Code extends, not starts over.
- **Two live breakages are folded into the brief, not deferred:**
  1. Vellum JWTs expired 8 days (see `vellum-jwt-recovery` brief).
  2. estate-machine service stack down (Traefik default backend serving).
- The metric-ownership map (Langfuse vs Opik) is **resolved-by-core, not Ewan-by-hand** — removed from the gate cluster.

## What to change next

1. **Connect the PostgreSQL connector** in Perplexity. Single highest-leverage move — lets the core read vellum + brain stats live. (Ewan-only, ~1 minute.)
2. **Confirm OPEC = OpenTelemetry** (one-line check — Ewan).
3. **Decide:** fold the core's run loop into the existing Daily Lens (hourly heartbeat + daily deep-read), or build a second schedule. Default: fold.
4. **Verify Beast service stack** — is the dark state intentional or a surprise? (Ewan, one line saves Claude a detour.)
5. **Wire `harness_event` schema + `epistemic_status*.py`** as the core's gate engine. Claude Code extends, not rebuilds.
6. **Live wiring deliverable zero (for Claude on M5):** resolve tailnet host → confirm Vellum :8400 + Postgres answer → confirm Infisical secrets → capture as a repeatable check.

## Not yet verified

- Live state of estate-machine stack (probed dark; intent unknown).
- Whether `epistemic_status*.py` files are current.
- Whether the Daily Lens schedule is still active.

## Tier C gates (Ewan only)

- Connect PostgreSQL connector.
- Confirm OPEC=OpenTelemetry.
- Confirm Beast stack-down is intentional or not.
- Approve fold-into-Daily-Lens vs separate schedule.

[CLOSURE] branch=PLAN | proxy=1 logged | gates=4 questions for Ewan (Postgres connector + OPEC + Beast stack + schedule fold), collapse to one hand-back | inbox=deterministic-core__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
