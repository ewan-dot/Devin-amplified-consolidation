---
title: "Master Plan — 2026-06-25"
document_type: research_conclusion
artifact_id: master-plan__v01__2026-06-25
date_utc: 2026-06-25T09:42:00Z
project: Amplified Partners
author: Perplexity Computer
stage: decision
objective: "Single ordered plan that composes every artifact produced today into one dependency-aware sequence, with owners and gates named. Read this and you can hand it to the M5 watchers as a unit."
reader: agent
source_refs:
  - pipe-weld-brief__v01__2026-06-25__perplexity.md
  - cross-ide-problem-sharing-rules (drafted; not yet pushed in this session)
  - prior-art-syntheses-bundle__INDEX__v01__2026-06-25.md
  - prior-art-syntheses-bundle__2026-06-25.tar.gz (8 paired files)
  - vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md
  - signal-reading-bundle__2026-06-25.tar.gz (doctrine v03 + signal-reading pair)
origin_type: agent_synthesis
attribution: "Composed by Perplexity Computer from the six artifacts produced 2026-06-25 07:55-10:42 BST."
epistemic_tier: STRUCTURED
tier_reason: "The components are each STRUCTURED with primary-source backing; the composition is the same."
epistemic_role: production_gate
effective_tier_rule: min-rule
preconditions:
  - All six referenced artifacts present in inbox
  - Three Tier-C baton decisions from the prior-art bundle either ratified or explicitly deferred
contradiction_status: clean
machine_action_allowed: recommend
system_of_record: local_workspace
ratifier: Ewan
next_action: "Ewan ratifies or amends the order; Phase 0 unblocks Phase 1; M5 watchers (Antigravity, Claude Code, Cascade-Mac, Devin) split the work per ownership column."
outcome_routing:
  outcome_class: production_candidate
  outcome_reason: "Every phase is implementable on the back of artifacts already in the inbox. No further research required."
  required_next_action: "Ewan signs off the three baton decisions; implementation begins."
---

# Master Plan — 2026-06-25

## Goal (the one line)

Close the loop from external information → research-pipe → brain/lake, with every boundary witnessed in Vellum and every job-start hooked to the signal-reader. First paying client becomes possible when Phase 2 completes.

## Operating model (cross-IDE)

Each seat owns one project **end-to-end** — working, tested, available in a **shared folder** unless it is genuinely IDE-local (worktree, IDE rules). Outcomes land in `~/amplified-pipeline/`, `perplexity-inbox/`, control-centre, or Beast via PR — not duplicated across seats. Unified sensor gives **visibility** (snapshot + proceed/warn/halt); it does not collapse who owns the fix. Seat table and shared-vs-local paths: `docs/UNIFIED-SENSOR-PLAN.md` §Operating model + §Seat ownership.

## The seven phases

| Phase | What | Why this order | Best owner | Tier-C gate before starting |
|---|---|---|---|---|
| **0** | **Ewan ratifies three baton decisions** from prior-art bundle §3: (a) Mac mini role (central sensor hub vs peer); (b) CRM-vs-Cove Infisical migration order; (c) Presidio scan in perplexity-ingest now vs later. | These three are the only items in the entire stack that the prior art cannot resolve without you. Everything else is unblocked. | Ewan | — |
| **1** | **Wire the Vellum @witness decorator** (extend `/opt/amplified/vellum/vellum/monitor/decorator.py`) per the v03 doctrine. Add unit tests. | The decorator is the precondition for every other phase's instrumentation. Without it, Phase 2's W2 (verifying ingest-inbox→brain drainer) cannot be witnessed and Phase 3 has nothing to read. | Cascade-Mac (worktree pattern proven) | None — Phase 0 doesn't gate this; the decorator is internal to Vellum. |
| **2** | **Pipe weld** — W1 (markdown emit + POST to perplexity-ingest from research-pipe `staging_emitter.py`), W2 (verify ingest-inbox → brain drainer), W3 (query_schema options: depth, source_mix, tier_ceiling, routing). Per pipe-weld brief. | This is the single move that closes the loop and unblocks the first-paying-client path. Half a day of work; no Tier-C blockers. | Claude Code on M5 → Tailscale → Beast | None |
| **3** | **Job-start hook** wired to the five trial boundaries (perplexity_ingest.drop, research_pipe.staging_emit, brain_mcp_writer.ingest, cove_temporal.workflow_start_end, infisical.secret_read) per v03 doctrine. The hook queries `friction_monitor.sql` (already on Beast, 58KB of detection maths) and emits the proceed/warn/halt decision per the signal-reading synthesis matrix. | Closes C1 (the reader contract — "read or graveyard"). Once Phase 2 lands, Phase 3 makes Phase 2 self-monitoring. | Claude Code | Phase 1 (decorator must exist before the hook reads its output) |
| **4** | **One-week trial** of the witness doctrine on the five boundaries. Run real traffic. At end of week, evaluate against the four acceptance criteria in v03 doctrine §"Acceptance Test": ≥95% coverage; ≤1% latency overhead; Perplexity Computer queried each boundary at job-start; ≥1 weak-signal catch. | The only honest way to prove the doctrine is empirical. If 1–3 fail, doctrine is wrong; if 4 fails, boundaries were wrong-picked but doctrine survives. | Perplexity Computer reads weekly; Cascade-Mac measures coverage/latency | Phases 2 + 3 both live |
| **5** | **Estate-security migration** per Pillar 4: move CRM, Cove/Temporal, brain-mcp-{writer,readonly}, MCP servers, LiteLLM, token-proxy, M5 + Mac mini + MacAirM4 agents onto Infisical as the single identity plane. Apply the key-rotation policy (Vellum JWT TTL = 30 days; LiteLLM keys → GitHub PATs → MCP bearers → Infisical service tokens → Vellum signing keys per Pillar 4 §"Breach response"). | Pillar 4 names this as the foundation for trustworthy expansion. Migrate AFTER Phase 4 proves the witness layer can detect drift — moving secrets without witness is flying blind. | Cascade-Mac (PR#1 hook pattern + worktree) + Antigravity (deployment) | Phase 4 acceptance |
| **6** | **Scale boundaries** to the next twenty (CRM endpoints, MCP servers, LiteLLM model calls, GitHub webhooks, M5/Mac mini sensor agents). Per v03 doctrine §"Pass all four". | Compounding floor. Each new boundary is a few lines of decorator + one signal-reader registration. | Whoever owns the surface (sweep, devin, etc.) | Phase 4 acceptance |
| **7** | **Data lake build** per Pillar 3: MinIO + Parquet + Iceberg (PyIceberg, no JVM), BLAKE3 exact dedup, MinHash/LSH near-dedup, faster-whisper for audio, GraphRAG extraction loop on ollama-2 + ollama-pudding. Bronze/Silver/Gold layers map onto existing Beast directories (raw-mac-dumps, vault, ingest_downloads, ingest_batch_*, ingest_openclaw). | The lake is the second sink; brain is the first. Builds AFTER the pipe is closed (Phase 2) and after the brain ingestion path is verified (Phase 2 W2). | Devin or a fresh subagent | Phase 2 complete |

## Critical-path summary

```
Phase 0 (Ewan, minutes)
   │
   └─▶ Phase 1 (Cascade-Mac, ~half day)
          │
          ├─▶ Phase 2 (Claude Code, ~half day) ────────┐
          │                                            │
          └─▶ Phase 3 (Claude Code, ~half day) ────┐   │
                                                   │   │
                                                   ▼   ▼
                                            Phase 4 (one week real traffic)
                                                   │
                                                   ├─▶ Phase 5 (security migration, ~1 week)
                                                   ├─▶ Phase 6 (scale boundaries, ongoing)
                                                   └─▶ Phase 7 (lake build, ~2 weeks)
```

**Time-to-first-paying-client gate**: completion of Phase 2 + Phase 4. That's roughly **one calendar week** of elapsed time, ~1.5 person-days of focused work.

## What this plan does NOT do

- Does not commit any spend over £50.
- Does not write directly to the Beast (every change goes through the pipe: Python+Rust+Vellum+AI+Human).
- Does not change the constitution, the rods, or the min-rule.
- Does not require new infrastructure — every component named exists today.
- Does not address the 12 remaining Tier-C gates from the Jun-24 INBOX-INDEX (Vellum JWT TTL is closed by Pillar 4; the other 12 remain open and are NOT on this critical path).

## How this composes with the inbox

| Inbox artifact | Used in phase |
|---|---|
| `pipe-weld-brief__v01__2026-06-25` | Phase 2 (verbatim) |
| `prior-art-syntheses-bundle__2026-06-25.tar.gz` Pillar 4 | Phase 5 (verbatim) |
| `prior-art-syntheses-bundle__2026-06-25.tar.gz` Pillar 3 | Phase 7 (verbatim) |
| `vellum-witness-doctrine-and-decorator__v03__2026-06-25` | Phases 1 + 3 + 4 + 6 |
| `signal-reading-prior-art-synthesis__agent__v01__2026-06-25` | Phase 3 (the discipline) + Phase 4 (the read protocol) |
| Cross-IDE problem-sharing rules (drafted but not yet pushed) | Cuts across all phases — the rules describe how IDEs share solutions |

## The one consolidated hand-back

You make the call on three things in Phase 0. Everything else can proceed on proxy with the artifacts already shipped:

1. Mac mini role: **central sensor hub** (aggregates M5 + MacAirM4, forwards to Vellum) or **peer** (all three Macs talk to Beast/Vellum directly)?
2. CRM Infisical migration: **CRM first** or **Cove/Temporal first** (default: Cove/Temporal first)?
3. Presidio in perplexity-ingest: **add now** (~1 hour, alongside existing secrets regex) or **batch with Phase 5**?

Three one-line answers and we run.

## Closure

[CLOSURE] branch=PLAN | proxy=1 logged (inbox push) | gates=three baton decisions in Phase 0 (consolidated) | inbox=master-plan__v01__2026-06-25__perplexity.md | tier=STRUCTURED
