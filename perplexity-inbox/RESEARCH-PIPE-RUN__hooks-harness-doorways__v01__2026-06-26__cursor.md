---
title: "Research Pipe Run — Hooks & Harnesses as Doorways"
document_type: research_pipe_run
artifact_id: RESEARCH-PIPE-RUN__hooks-harness-doorways__v01__2026-06-26__cursor
date_utc: 2026-06-26
corpus_item_id: hooks-harness-doorways-fleet-2026-06-26
author: cursor
reader: ewan
epistemic_tier: INTUITED
run_host: Beast (research-pipe container + SearXNG L1)
note: five_stage_orchestrator.py not deployed on Beast; run used M1Orchestrator + runner process-queue (canonical Beast entrypoint per WIRING.md)
---

## Human summary

Ran on **Beast** (not Mac fallback): `research-pipe` container healthy; 8 SearXNG fan-out probes + one `runner process-queue` cycle for corpus `hooks-harness-doorways-fleet-2026-06-26`. Wide→narrow×3 across seven candidate domains (physical interlock/mantrap, git worktree agent isolation, aviation CRM challenge-response, Erlang OTP supervision, event-sourcing witness log, MCP-vs-CLI agent tooling, Ashby requisite variety). Brutal demote stripped homonym junk (Sally Beauty, Eventbrite, etc.). **Five survivors** converge on one mechanism: *sequential doorway* — only one permission transition live at a time, deterministic interlock between stages, append-only witness on pass. Beast staged **20 INTUITED packets** (batch `1fe59119-947e-486b-a6ca-f2d228533483`, Gate0 20/20). Cross-domain endpoint claim caps at INTUITED until ≥3 founding disciplines measured on fleet implementation, not search alone.

## Orchestrator payload

### meta

```yaml
run_id: hooks-harness-doorways-fleet-2026-06-26
stage: swanson_combine
corpus_item_id: hooks-harness-doorways-fleet-2026-06-26
epistemic_tier: INTUITED
chunk_id: single-item
survivor_count: 5
run_host: beast
beast_entrypoint: research_pipe.runner process-queue + M1Orchestrator
beast_batch_id: 1fe59119-947e-486b-a6ca-f2d228533483
beast_staging_path: /opt/amplified-machine/apds/staging/1fe59119-947e-486b-a6ca-f2d228533483/
jsonl_witness: ~/amplified-pipeline/data/research-pipe-docs/2026-06-26_five-stage_hooks-harness-doorways-fleet-2026-06-26.jsonl
searxng: search.beast.amplifiedpartners.ai (container http://searxng:8080)
mac_supplement: WebSearch gap-fill only (labeled agent-seat, not Beast run)
```

### stage_result

#### Wide 1 — candidate domains (raw terms from v04 brief + Ewan frame)

| # | Founding discipline | Raw probe terms |
|---|---------------------|-----------------|
| 1 | Physical security / civil | sally port, airlock, mantrap, sequential interlock |
| 2 | Software engineering | git worktree, isolated branch, agent orchestration |
| 3 | Human factors / aviation | CRM, challenge-response, checklist gate |
| 4 | Telecom / distributed systems | Erlang OTP, supervision tree, let it crash |
| 5 | Software architecture | event sourcing, append-only ledger, witness audit |
| 6 | AI tooling | Model Context Protocol, CLI, agent tool cost |
| 7 | Cybernetics / control | Ashby requisite variety, homeostatic control |

#### Narrow 1 — canonical sources per domain

| Domain | Canonical source | URL |
|--------|------------------|-----|
| Capability confinement | Lampson, *A Note on the Confinement Problem* (1973) | https://www.cs.cornell.edu/andru/cs711/2003fa/reading/lampson73note.pdf |
| Physical interlock | US3602536A sequential airlock closure | https://patents.google.com/patent/US3602536A |
| Supervision tree | Erlang OTP supervisor behaviour (official docs) | https://www.erlang.org/doc/apps/stdlib/supervisor.html |
| Event witness log | Fowler, Event Sourcing (2005) | https://martinfowler.com/eaaDev/EventSourcing.html |
| Requisite variety | Ashby, *Introduction to Cybernetics* (1956) ch.11 | https://link.springer.com/chapter/10.1007/978-1-4899-0718-9_28 |
| Worktree isolation | git-scm worktree documentation | https://git-scm.com/docs/git-worktree |
| Aviation gate | FAA CRM / challenge-response briefing materials | https://www.cfidarren.com/crmchecklist.htm |

#### Wide 2 — cross-domain failure modes (others identified)

- Mantrap: simultaneous door open if switches too slow; fail-secure vs life-safety tension (Security Info Watch; Nexlar install guide).
- Worktree: shared `.git/config` and hooks — isolation is filesystem not credential (DEV Community, Augment Code).
- OTP: supervisor escalation when restart intensity exceeded — redundancy itself can fail (OTP docs).
- MCP: schema bloat 4–32× token vs CLI for identical ops (Tyk, Mechanical Advantage benchmarks 2025–2026).

#### Narrow 2 — convergent mechanisms (2–3 strongest)

1. **Sequential interlock** — never two live transitions (mantrap doors; worktree working dirs; OTP rest_for_one; hook before next tool).
2. **Append-only witness** — event log as audit trail (Fowler event sourcing; Vellum hash-chain design intent in fleet briefs).
3. **Harness split** — deterministic CLI/hooks for open-once rituals; MCP for structured read-witness when schema cost earns its keep (Tyk MCP-vs-CLI guide; Addy Osmani MCP deep dive).

#### Wide 3 / Narrow 3 — multi-domain endpoint claim (INTUITED)

**Endpoint claim:** Fleet hooks/harnesses implement *sequential doorways* — bounded permission surfaces opened one at a time (push-door self-request), isolated worktree per stage, Vellum telemetry on open/close, completion % tracked per door cycle. Prior art spans physical interlock (≥1 discipline), process supervision (≥1), append-only witness (≥1). **Not promoted to STRUCTURED** — fleet open-door runtime (Baton/RodGuard) still unwired per inbox corpus.

#### Brutal demote — survivors (5)

| id | vector | founding discipline |
|----|--------|---------------------|
| S1 | Sequential interlock (one live transition) | Physical security + distributed systems |
| S2 | Git worktree as agent filesystem doorway | Software engineering |
| S3 | OTP supervision tree / let-it-crash containment | Telecom |
| S4 | Append-only event witness (Fowler event sourcing) | Software architecture / audit |
| S5 | CLI harness vs MCP read-witness cost split | AI tooling / governance |

#### Beast run metrics

```yaml
m1_fan_out_queries: 8
searxng_hits_total: 159
runner_alert_id: 944d68ca-2559-4b9c-9d80-4d949aed04be
packets_staged: 20
gate0_passed: 20
gate0_failed: 0
auto_promote: false
```

### handoff

```yaml
next_stage: done
architect_flags:
  - "five_stage_orchestrator.py absent on Beast clean-build-latest; M1+runner is live path"
  - "Endpoint claim INTUITED — fleet door-close witness + Baton runtime still gaps"
  - "Beast SearXNG homonym noise high; demote mandatory before precision"
do_not:
  - promote epistemic tier from agent output
  - synthesise final truth without promotion gates
  - use prior synthesis prose as search input
goal_link: "Sequential doorways reduce recurring agent thrash — deterministic patches close permission-shape failures"
```

### Research prompt (raw terms only — for re-run)

```
Corpus: hooks-harness-doorways-fleet-2026-06-26
Pattern: wide→narrow×3
Terms: push-door permission, sequential doorway, git worktree, Agent Worktree Contract,
  Vellum telemetry, door-open event schema, harness_event approval_tier drift_signal,
  amplified_permissions classify, Baton RodGuard, hooks beforeShellExecution,
  session-start witness, completion percentage, CLI vs MCP sovereign AI seats,
  sally port mantrap interlock, aviation CRM challenge-response, Erlang OTP supervision,
  event sourcing append-only, Ashby requisite variety, FRACAS FMECA, circuit breaker
Exclude: prior synthesis headings (door map, H1 H2 H3)
```

[CLOSURE] branch=AUDIT | proxy=none | gates=Beast run complete; STRUCTURED promotion blocked on fleet wiring | inbox=RESEARCH-PIPE-RUN__hooks-harness-doorways__v01__2026-06-26__cursor.md | tier=INTUITED
