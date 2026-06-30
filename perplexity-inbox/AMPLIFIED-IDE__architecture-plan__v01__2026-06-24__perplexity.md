# Amplified IDE — Integrated Architecture Plan

TIER: STRUCTURED
PROVENANCE: 16 inbox threads + 5 loaded skills (`amplified-constitution`, `min-rule`, `lean-by-default`, `end-to-end-closure`, `amplified-standing-grants`) + live Beast state from `beast-state-correction`.
STATUS: synthesis pass — joins all 16 threads into one IDE picture.
FOR: Ewan + M5 watchers. Read alongside `INBOX-INDEX`.

## The one-line picture

**The Amplified IDE is a sovereign, deterministic-spined, multi-agent development environment whose only user door is the Intent Interface, whose only persistence path is the Pipe, and whose only judge is Ewan (with AI as logged proxy, for now).**

It is not a chat with extras. It is an operating environment for AI-human partnership, where the AI is substrate and the human is signer, and the rules are software-up.

## The seven layers (top = user; bottom = silicon)

```
─────────────────────────────────────────────────────────────────
L7. USER DOOR        Intent Interface (Electron) · markPass.ts certainty 1-9+▲
─────────────────────────────────────────────────────────────────
L6. AGENT WORK       Claude Code · Cursor · Devin · Antigravity · VSCodium
                     each in a sealed Apple Container cell on Mac mini
─────────────────────────────────────────────────────────────────
L5. ROUTING          ONE LiteLLM = estate-token-router (credit-first)
                     + estate-cost-tools middleware (caching/compaction/Haiku)
                     + Production-Law gate (land or surface as unfinished)
─────────────────────────────────────────────────────────────────
L4. RUNTIME GATE     Open-door harness: Baton (single write lease)
                     + RodGuard (5-rod circuit breaker)
                     + amplified_permissions.classify() (A/B/C ladder)
─────────────────────────────────────────────────────────────────
L3. DETERMINISTIC    Deterministic core: harness_event schema
    SPINE            + epistemic_status*.py (min-rule, P0, drift)
                     + Vellum senses (signals → drift_signal G/A/R/B)
                     reads Postgres, writes Vellum
─────────────────────────────────────────────────────────────────
L2. PIPE             Python + Rust + Vellum + AI + Human = Amplified
                     (Relay/Vellum substrate: transport + ledger + workbench)
─────────────────────────────────────────────────────────────────
L1. PERSISTENCE      Postgres + pgvector + Apache AGE (Beast)
                     Data Path 1: lake (verbatim, attributed)
                     Data Path 2: pool (neutralised, identity-blind, PUDDING)
─────────────────────────────────────────────────────────────────
L0. INFRASTRUCTURE   M5 (judgment) · Mac mini (local execution, 4 cells)
                     · M4 (reserve) · Beast (ledger + batch + router)
                     · Tailscale (front door)
─────────────────────────────────────────────────────────────────
```

## Each thread, mapped to its layer

| Thread (from INBOX-INDEX) | Layer | What it owns |
|---|---|---|
| Cockpit / Intent Interface (#14) | L7 | The only user door; Electron app; markPass.ts certainty |
| PCO layers + Lens selector (#13) | L7 → L5 | Certainty-1-9+▲ field; Production Law; Lens-selector status open |
| AI-native search methodology (#15) | L7 input | The methodology that should drive how Perplexity searches — once it arrives |
| Sovereign multi-agent environment (#2) | L6 | The 4-cell Apple Container build on Mac mini |
| VSCodium agent lane (#8) | L6 | A third IDE lane (besides Claude Code + Cursor) |
| Repo consolidation + asset inventory (#12) | L6 prep | Per-cell repo discipline; canonical clean-build |
| GitHub hardening (#11) | L6 governance | Branch protection, CODEOWNERS, no agent self-approval |
| Token-efficiency programme (#1) | L5 | The router, the proxy, the §9 PROOF-OF-LIFE gate |
| DeerFlow trial (#16) | L5 (experiment) | Trial harness on Beast — keep or kill |
| Open-door harness (#7) | L4 | Baton + RodGuard + keyholder model |
| Standing-grants + harness (#3) | L4 | amplified_permissions.classify() — A/B/C |
| UI-methods research pipe (#4) | L3 input | PUDDING feedstock — mechanism extraction |
| Deterministic core (#9) | L3 | The reader that turns L2 signals into decisions |
| Vellum senses (folded #9) | L3 | sensor_event.py — the signals into drift_signal |
| Beast-state correction (#5) | L1/L0 | Refresh BEAST-STATE.md to match live estate |
| Vellum JWT recovery (#6) | L2 unblock | Live blocker; without it L2 is dark |
| Relay protocol (#10) | L2 doctrine | The substrate name and shape |

**No layer is empty. No thread is loose.** Every recent thread maps to exactly one (or one→one) layer. This is the proof that they really are one IDE, not 16 projects.

## The five rods compile down through every layer

```
L7 user door        — markPass.ts records certainty + ambiguity (honesty)
L6 agents           — sealed cells (no take from another agent)
L5 router           — credit-first (idea meritocracy, not loudest model)
L4 runtime gate     — RodGuard trips on rod violation (all 5 rods, machine-enforced)
L3 deterministic    — min-rule + P0 halt on silent promotion (honesty)
L2 pipe             — Vellum attribution (radical attribution)
L1 persistence      — Path 1 verbatim (attribution) + Path 2 neutral (meritocracy)
L0 infra            — sovereignty (Mac trust root; Beast for compute only)
```

Every horizontal cross-section of the IDE has the rods compiled into it. Pull a rod and the whole column collapses. That is what "rules software-up" means in this architecture.

## The single critical path (read this if nothing else)

If you build the IDE in this order, every step unblocks the next and nothing waits on a step that hasn't run. This is THE path:

### Phase 0 — Unblock the dark (Tier C gates, Ewan-only, ~30 min total)

These four answers light the IDE:

0.1 **Mac mini RAM number.** Unlocks Qwen tier (L6) + local-lane proof (§9.6).
0.2 **Vellum JWT TTL + Infisical decision** (#6). Unlocks L2 writes; without it L3 and L5 telemetry are blind.
0.3 **Beast `estate-machine` stack** — intentional dark or surprise? (#9). Unlocks L1/L2.
0.4 **PostgreSQL connector** in Perplexity. (#9) ~1 minute click; unlocks L3 deciphering.

### Phase 1 — Weld the seams (Tier A research, 6 actions, no gates beyond Phase 0)

1.1 **Name lock** (mesh-plan S1): Beast in code; Infrastructure 1 external only. One PR through pipe via `beast-state-correction`.
1.2 **One LiteLLM, not two routers** (mesh-plan S2): `estate-token-router` IS the LiteLLM proxy; `estate-cost-tools` is middleware. One credential holder. Folds in VSCodium (#8) and DeerFlow (#16) as sub-patterns.
1.3 **Harness name disambiguation** (#7): `amplified_permissions.py` for the classifier; `open_door_runtime/` for Baton + RodGuard. Two different things, two different files.
1.4 **Adopt certainty-1-9 + ▲ field** in `harness_event` and Vellum events (#13). L7 information rides L3 spine.
1.5 **Pipe equivalence**: lake + pool + Vellum + PUDDING are three views of one pipe, not three pipes (mesh-plan S5).
1.6 **`amplified_permissions.classify()` is the only gate-classifier** across all M5 AIs (mesh-plan S4).

### Phase 2 — Land the foundation (in this order)

2.1 **GitHub hardening verification** (#11) — log the diff per repo. Required before any agent writes.
2.2 **Repo consolidation + canonical clean-build** (#12) — agents need to know which repo is the real one. `mdutil -E /` only after Ewan signs off.
2.3 **L3 deterministic core build** (#9) — Claude Code extends `epistemic_status*.py`; reads Postgres; writes Vellum drafts. Replica build is started; needs the live wiring.
2.4 **L2 Relay/Vellum doctrine** — write `relay_protocol.md` (#10). One artifact; ratifies the substrate name.
2.5 **L4 Open-door harness** wire-up (#7) — Baton lease semantics; RodGuard trip conditions; door-open event schema in Vellum.

### Phase 3 — Light the agents (4 cells, then judge)

3.1 **Sovereign cell build** (#2) — 4 sealed Apple Container cells on Mac mini. Provisioning script lands enforcement files INSIDE each cell (mesh-plan S3).
3.2 **VSCodium lane** (#8) — third IDE alongside Claude Code + Cursor, same provisioning shape.
3.3 **One real unit end-to-end** in one cell (sovereign-build's "one unit first" rule). Single agent, single task, full instrumentation. Measure delivered reliability.
3.4 **DeerFlow trial** (#16) on the Beast lane, in parallel. Single task; keep-or-kill at end.

### Phase 4 — Cockpit + prove (the IDE goes live)

4.1 **Cockpit branch consolidation** (#14) — finish `cursor/20260623120000/vellum-ui-lens`. Preserve `markPass.ts`. Resolve PR#2.
4.2 **Intent Interface as the only user door** — confirm wiring from Cockpit → L4 → L5 → agents → L2 → L7.
4.3 **Token-eff §9 PROOF-OF-LIFE** captured in `PROOF-OF-LIFE.md` — proxy live, router live, ≥3 executor classes, credit-first decision logged, budget guard, >90% cache-read, local-lane at $0 (initiated from inside a cell — mesh-plan S6), Vellum telemetry, before/after delta, self-heal.
4.4 **UI-methods pipe** (#4) — dispatched parallel; PUDDING after collection. Sealed; doesn't gate anything else.

### Phase 5 — Read the missing input (re-tier)

5.1 **AI-native search methodology** (#15) — when Ewan provides the file, read it Tier A, then re-tier the entire L7 + L5 stack against it. This is the only retro pass; everything else is forward.

## What "comprehensive IDE" means here

Most IDEs ship as one app with extensions. Amplified is the opposite: **one constitution, seven layers, many agents.** The IDE is the union of:

- the user door (L7),
- the agents you bring to it (L6),
- the rules that govern how they cooperate (L4),
- the deterministic floor that watches everything (L3),
- the substrate that records it forever (L2),
- the infrastructure that hosts it (L0/L1).

Drop any one and what's left isn't this IDE. Build them in the order above and every step earns its place.

## Honest checks

- **L5 has the heaviest external dependency burden** (Anthropic/Cursor/Devin/Antigravity pricing + Pool status). Re-verify before §9 captures any "before/after" external citation.
- **L2 is currently dark** — JWTs expired + estate-machine stack appears down. Phase 0 fixes both, but if either is structurally broken (e.g. JWT signing-secret mismatch on Beast), Phase 1+ stops.
- **L3 has a real prior-art base** (`epistemic_status*.py`, `harness_event`) — Claude Code extends, doesn't rebuild. Confirm the files are current before the Phase 2.3 build.
- **The 4th cell** on the Mac mini is the M4-equivalent reserve; the build provisions 4 equal cells, but routing today targets 3 (Claude/Cursor/Devin). Antigravity is the natural 4th.
- **One open architectural question:** is `Lens selector` the routing layer (L5) renamed, or a separate primitive between L5 and L6? — answered by Ewan in one line (#13). Until then, L5/L6 boundary is slightly fuzzy.

## The shortest definition of "done"

The Amplified IDE is **done** (v1) when:

1. Ewan opens the Intent Interface (L7).
2. He speaks. Certainty is marked. The utterance enters L2 (Vellum).
3. The deterministic core (L3) reads it, decides which agent + executor class.
4. The runtime gate (L4) opens the right door, with Baton, under RodGuard.
5. The router (L5) routes to the right cell on the right machine at credit-first cost.
6. The agent in a sealed cell (L6) does the work.
7. The result lands in Vellum (L2), attributed, hashed, ratified — or surfaces on the board as unfinished.
8. Ewan sees the result back in the Intent Interface (L7).
9. Every step is `[CLOSURE]`-footered, min-rule tiered, and proxy-logged.
10. The cost of step 1→8 is a fraction of what it was a week ago, **measured** in `PROOF-OF-LIFE.md`.

That is the IDE. That is what the 16 threads compose into. Phase 0 unblocks; Phase 1-2 welds; Phase 3-4 lights; Phase 5 retros against the missing input.

[CLOSURE] branch=PLAN | proxy=1 logged (architecture plan drafted as AI_PARTNER_PROXY) | gates=Phase 0 four-item Ewan cluster (RAM + JWT/Infisical + Beast stack + Postgres connector) | inbox=AMPLIFIED-IDE__architecture-plan__v01__2026-06-24__perplexity.md | tier=STRUCTURED
