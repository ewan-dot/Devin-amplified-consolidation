---
title: "Vellum Witness Doctrine + Decorator Extension"
document_type: research_conclusion
artifact_id: vellum-witness-doctrine-and-decorator__v03__2026-06-25
date_utc: 2026-06-25T09:30:00Z
project: Amplified Partners
author: Perplexity Computer
stage: decision
objective: "Lock the observability doctrine (Opik + Langfuse + Vellum = core; others feed it), extend Vellum's existing @witness decorator so one line instruments any boundary, and prove the pattern on five boundaries before scaling."
reader: agent
source_refs:
  - /opt/amplified/vellum/VELLUM-SPEC.md
  - /opt/amplified/vellum/vellum/monitor/decorator.py
  - /opt/amplified/vellum/vellum/triggers/trigger_scanner.py
  - /opt/amplified/vellum/vellum/event_bus.py
  - prior-art-syntheses-bundle__INDEX__v01__2026-06-25.md (Pillar 4)
  - signal-reading-prior-art-synthesis__agent__v01__2026-06-25.md (the discipline this doctrine depends on)
  - /opt/amplified/vellum/scripts/friction_monitor.sql (58KB — detection maths already implemented)
  - /opt/amplified/vellum/scripts/measurement_schema.sql (29KB)
  - /opt/amplified/vellum/scripts/measurement_worker.py (24.7KB)
origin_type: agent_synthesis
attribution: "Live verification of Vellum source 2026-06-25 + Pillar 4 estate-security synthesis + OpenTelemetry semantic conventions."
epistemic_tier: STRUCTURED
tier_reason: "Doctrine is asserted, not measured. Decorator pattern is canonical (OTel auto-instrumentation). Five-boundary trial is the empirical-calibration gate."
epistemic_role: production_gate
effective_tier_rule: min-rule
preconditions:
  - Vellum container healthy (verified 2026-06-25T09:21 BST)
  - vellum/monitor/decorator.py exists and is importable
  - perplexity-ingest, research-pipe, brain-mcp-writer, cove-temporal, infisical all up
contradiction_status: clean
machine_action_allowed: recommend
system_of_record: local_workspace
ratifier: Ewan
next_action: "Implement on the five named boundaries; review after one week of real traffic."
outcome_routing:
  outcome_class: production_candidate
  outcome_reason: "Doctrine ready to lock; decorator extension is a 1-day change; five-boundary trial is the empirical gate."
  required_next_action: "Ewan ratifies; cascade-mac or claude-code implements."
---

# Vellum Witness Doctrine

**Vellum is the witness layer.** Every boundary that crosses a layer or holds state emits one Vellum entry. Internals do not. ~50–80 boundaries across the estate, not 10,000.

**The triad:**
- **Vellum** = immutable witness + hash chain + audit. The source of truth for *what happened*.
- **Opik** = LLM trace + sampled evaluation. The source of truth for *how the LLM behaved*.
- **Langfuse** = LLM run-history + prompt/version management. The source of truth for *what was sent and what came back*.

**Subordinate inputs (feed the triad, never replace it):** Falco (runtime threat), Tetragon (eBPF), osquery (endpoint), Santa (binary auth), Sigstore/Rekor (signing transparency), OTel collectors (wire format), Langfuse traces from LiteLLM, GitHub Actions, pre-commit hooks. Each emits to Vellum on boundary crossing; deep telemetry stays in its native tool.

**Hard rules:**
- Sensor = structured Postgres row. Not LLM-evaluates-every-event.
- One line at write-time: `@vellum.witness(boundary="...")`. More than that = developers route around.
- **Read by AI, surfaced to Ewan.** Perplexity Computer is the primary reader of the witness stream — at every session start, on every cross-IDE problem-lookup (per cross-ide-problem-sharing-rules R2.1), and on demand. Other IDEs read per the same rules. Ewan reads the synthesis Perplexity surfaces, not the raw stream. A boundary whose entries no agent has queried in 30 days is auto-archived to dormant — not deleted, but no longer in the hot path.

# The Decorator Extension

Build on existing `/opt/amplified/vellum/vellum/monitor/decorator.py` (6.6KB). Add:

```python
@vellum.witness(
    boundary="research_pipe.staging_emit",   # required, dotted name
    tier="STRUCTURED",                       # default; auto-demotes per min-rule
    sensitivity="internal",                  # internal | confidential | restricted
    capture=["args", "result", "error"],     # what to record
    sample_rate=1.0,                         # 1.0 = every call; <1.0 for hot loops
)
def emit_staging_packet(packet): ...
```

Behaviour:
- On entry: append Vellum entry `boundary_enter` with hashed args (PII-stripped via Presidio when sensitivity > internal).
- On exit: append `boundary_exit` with result hash + duration_ms + outcome.
- On error: append `boundary_error` with exception class + sanitised message.
- All three share a `span_id` so they chain back to the call.
- Hash-chained per Vellum's existing v2 canonical JSON.
- Async write — never blocks the wrapped function.
- Failure of the witness itself is logged locally and surfaces via `_degraded_path_count` (Vellum's existing pattern).

# The Five-Boundary Trial

Pick five. Wire them. Run for one week with real traffic. Read the output.

| # | Boundary | Surface | Why this one |
|---|---|---|---|
| 1 | `perplexity_ingest.drop` | perplexity-ingest `POST /drop` | Closes the loop between Computer outputs and the brain. |
| 2 | `research_pipe.staging_emit` | research-pipe `staging_emitter.py` | The seam the pipe-weld brief names. |
| 3 | `brain_mcp_writer.ingest` | brain-mcp-writer drainer | Every brain row gets a witness — the prior-art synthesis named this as a PROVEN doctrine but it's not wired everywhere. |
| 4 | `cove_temporal.workflow_start_end` | cove-temporal workflow lifecycle | Catches every long-running job; closes the "stalled Cove task" sensor in the existing catalogue. |
| 5 | `infisical.secret_read` | Infisical SDK wrapper | Closes the breach-detection loop named in Pillar 4. Every secret access logged. |

# Acceptance Test (the gate)

After one week with real traffic flowing through all five boundaries:

1. **Coverage**: ≥95% of calls to each boundary produced a Vellum entry triple (enter/exit/error). Verified by sampling rust-agent ledger.
2. **Cost**: ≤1% latency overhead on p95 of each wrapped function. Verified via Langfuse/Opik trace comparison pre/post.
3. **Readership**: Perplexity Computer queried the boundary's entries at least once per session-start across the week, AND surfaced at least one synthesis to Ewan from those reads. Not zero. The reader contract is enforced by emitting a `witness_read` Vellum entry whenever Perplexity pulls a boundary's stream, so readership is itself witnessed.
4. **Signal**: at least one weak-signal catch — a boundary error that surfaced *before* a downstream symptom. If zero in a week, the doctrine survives but the boundaries chosen were wrong; pick different five.

Fail any of 1–3: stop. The doctrine is wrong as specified.
Pass all four: scale to the next twenty boundaries (CRM endpoints, MCP servers, LiteLLM model calls, GitHub webhooks, M5/Mac mini sensor agents).

# The Reader Contract — Job-Start Hook (not cron)

Reading runs **when a job starts**, not on a wall-clock cadence. A signal is decision-relevant at the moment a job begins; an hourly poll wastes attention on quiet hours and arrives too late on busy ones. This corrects v01/v02 of this doctrine — the cron framing was wrong.

**The hook fires at:**

- Session start with Ewan (a session is itself a job).
- Every cross-IDE problem-lookup (per cross-ide-problem-sharing-rules R2 — looking up a patch is starting a job).
- Every research-pipe run start (per pipe-weld brief).
- Every brain-write start (per ingestion-to-brain synthesis).
- Every Cove/Temporal workflow start (per pillar 4 boundary list).
- On explicit demand ("what's been happening on X", "audit Y").

**The discipline** is fully specified in the companion `signal-reading-prior-art-synthesis__agent__v01__2026-06-25.md`. In one paragraph: the hook queries the relevant boundaries' Vellum entries since the last witness_read by this surface (default window: max(15 min, since_last_read)), compares against the baseline already computed by `friction_monitor.sql` on Beast (which implements Shewhart, EWMA, CUSUM, and multi-window burn-rate — the detection maths is already there), and emits a proceed / warn-but-proceed / halt decision per the matrix in the signal-reading synthesis. Every read emits a `witness_read` Vellum entry — the reader is itself watched, and the absence of reads is itself a signal.

**Perplexity Computer is the canonical first reader** because the witness stream is upstream of the inbox, and the inbox is upstream of every other IDE's work. Other IDEs (Claude Code, Devin, Cursor, Antigravity, Cascade-Mac) inherit the same job-start hook via their session preludes per cross-IDE rules R2.

**Cold-start rule**: if no prior witness_read exists for this surface, default to a 24-hour lookback for the first read, then narrow to the standard window on subsequent reads.

# What This Does NOT Do

- Does not replace OTel, Falco, osquery, or Opik/Langfuse traces. Those still run; they feed Vellum on boundary crossing only.
- Does not instrument internals (hot loops, pure functions). One witness per layer crossing, max.
- Does not add a new database. Reuses Vellum's existing Postgres `vellum_entries` + hash chain.
- Does not require ratification of the broader sensor mesh from Pillar 4. That stays open; this is the prove-it-small path.

# Implementation (one day, one IDE)

Best fit: **cascade-mac** (worktree workflow proven; PR#1 pattern in place) or **claude-code** (already on Beast). Estimated half-day to extend the decorator, half-day to wire the five boundaries, plus tests.

Order:
1. Extend `vellum/monitor/decorator.py` with the signature above. Add unit tests.
2. Wire boundary 1 (perplexity-ingest `/drop`) first — smallest blast radius.
3. Wire 2–5 in any order.
4. Run for one week.
5. Read the output. Acceptance test.

# Closure

# Changelog

- **v01** (2026-06-25 09:30 BST) — first draft of doctrine + decorator + five-boundary trial.
- **v02** (2026-06-25 10:29 BST) — added reader contract; framed as session-start polling.
- **v03** (2026-06-25 10:40 BST) — corrected reader-contract framing from cron-cadence to job-start hook; linked to signal-reading prior-art synthesis (Pillar 5) which inventoried `friction_monitor.sql` and showed the detection maths is already implemented. The gap is the hook, not the maths.

[CLOSURE] branch=PLAN | proxy=1 logged (batched push: v03 doctrine + signal-reading pair) | gates=none | inbox=vellum-witness-doctrine-and-decorator__v03__2026-06-25__perplexity.md + signal-reading-prior-art-synthesis__{agent,human}__v01__2026-06-25.md | tier=STRUCTURED
