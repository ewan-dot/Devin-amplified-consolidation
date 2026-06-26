# Relay Protocol — Implementation Brief

TIER: STRUCTURED (Ewan-asserted; named in-thread but no canonical doc landed)
PROVENANCE: session `46e85c2e` (2026-06-19, 21 turns)
STATUS: named, not specified; "It's already done. It's called Relay. It uses Vellum." — Ewan, this session
FOR: M5 watcher

## What exists

Relay is **the Amplified implementation's substrate**, not "a transport protocol". In Ewan's own correction:

> "Vellum is closer to road + map + customs checkpoint + memory + dashboard + workbench. Transport is just the road."

Scope (Ewan, this session):

- work preformation
- immutable record
- plans
- telemetry
- hooks
- weak/strong signal capture
- agent work surface
- business substrate
- compound learning
- Python infrastructure connection

Naming discipline corrected mid-thread: **"Relay" / "Relay/Vellum" / "the Vellum-backed Relay substrate" / "Amplified's Relay"** — not "your Relay" (sloppy personalisation).

Pre-production gate (Ewan, this session) — a task enters production only when it has:

- goal link
- owner
- input refs
- acceptance test
- allowed tools/models
- data sensitivity class
- route destination
- stop condition
- baton requirement

Outcome-language convention (Ewan, this session): use behavioural descriptions instead of moralised ones — *deception-equivalent output, avoidance-equivalent behaviour, lazy-equivalent work, sycophancy, reverse sycophancy, route failure, overbuild, source failure*. No moral theatre.

## What was done

- Concept named and scoped (above list).
- Naming corrected.
- Pre-production gate enumerated.
- Outcome-language convention established.
- Question posed at end of session: *"Want me to turn this into the first actual `relay_protocol.md` artifact with YAML front matter and event schemas?"* — **not answered before session ended.** Open since 2026-06-19.

## What it means

- **None of the inbox docs mention Relay.** Token-eff describes `estate-token-router` (LiteLLM, credit-first) — Relay is the substrate beneath transport, not the router. They are different layers; the inbox docs implicitly assume Vellum-as-ledger without naming Relay-as-substrate.
- **The pre-production gate (9 items) is more restrictive than the current `[CLOSURE]` footer.** Closure asks for branch/proxy/gates/inbox/tier. Pre-production needs goal_link, owner, input_refs, acceptance_test, allowed_tools, data_sensitivity, route, stop_condition, baton_req. → Closure footer is the chat-wrapper test; this is the *task-enters-production* test.
- **Baton requirement** in the pre-production gate is the same Baton as in `open-door-harness` brief. Single write lease across the estate. Confirms that brief's design.

## What to change next

1. **Write `relay_protocol.md`** — the canonical doc Ewan asked for at the end of `46e85c2e`. YAML frontmatter + event schemas + the 10-component scope + the 9-item pre-production gate + outcome-language convention. One artifact. (Tier A — research output.)
2. **Reconcile naming** across the inbox: every reference to "the pipe" / "Vellum" / "the substrate" should resolve to *Relay/Vellum* (with Vellum as the immutable record layer of Relay). Single naming pass.
3. **Adopt the 9-item pre-production gate** as the contract for anything claiming production-ready status — token-eff §9 PROOF-OF-LIFE already aligns with this in spirit; align in name.
4. **Adopt the outcome-language convention** in Vellum events instead of moralised labels. Update existing JSONL drafts.

## Not yet verified

- Whether a Relay-named module/file already exists in the codebase (named-but-not-located).
- Whether "Vellum" in the inbox docs is in fact Relay/Vellum as Ewan defines it, or just the ledger half.

[CLOSURE] branch=PLAN | proxy=1 logged | gates=write relay_protocol.md as a Tier A research output (no Ewan input needed) — log one open item: confirm Relay codebase location | inbox=relay-protocol__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
