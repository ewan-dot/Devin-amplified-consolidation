# Brief: Build & deploy the Amplified control centre

Tier of this brief: STRUCTURED (verified from estate repos + live probes 2026-06-24). Effective tier of work produced = MIN of inputs.

---

## 1. THE SPINE (today)

- We are **Amplified Partners** — an AI-native business operating system.
- Goal-lock: **get the business going. Make money so we can give it away.**
- The rods: **Win-win > Honesty > Transparency > Attribution > Meritocracy.** On tie, goal serves over ego.
- Ratification stance (UPDATED 2026-06-24, supersedes the for-now human-ratifier): **an AI-native company ratifies itself through code-enforced checks, balances, and telemetry.** The AI acts autonomously when an action provably passes the **constitutional gate** (below); the human is the **rare escalation path** — summoned only when the gate cannot answer, not as the default signer. Nothing enters the Beast except through the pipe (Python + Rust + Vellum + AI), but the pipe's ratifier is now the gate, with human as exception.
- **The constitutional gate (eight predicates):** radical honesty (claim tier ≥ asserted; min-rule holds), radical transparency (reasoning + seams logged), radical attribution (every input signed_by + sourced), win-win (no take that costs the counterparty), idea meritocracy (best idea regardless of author), privacy (no unauthorised data exposure), security (no boundary/credential violation), sovereignty (no external lock-in). Pass all eight → AI ratifies and acts. Any predicate failing or unevaluable → escalate to human.
- **Where deterministic ends is governed by logic, not by hand — the Deterministic-AI Partition Test:** each predicate is classified **T1** (deterministic algorithm exists → auto-evaluate in code, no tokens), **T2** (codeable but not yet written → temporary code-gap, escalates for now, carries a trigger to graduate to T1), or **T3** (genuine semantic judgement → AI, capped INTUITED → human-escalation edge). The deterministic frontier **expands over time** as T2 graduates to T1; Rice's theorem is the only fixed ceiling. Empirical production testing (labelled steps, inter-rater agreement, mislabel-rate monitoring) decides the real classification — not assertion. The system's standing job is to push predicates T3→T2→T1, shrinking the human-exception zone deterministically.
- Date: **2026-06-24**.

## 2. THE LENS (this task)

**Prior art exists — build on it, do not reinvent.** The control centre is the concrete build of three layers already designed in `amplified-harness-control-plane-dossier.md` (2026-05-16): Trace-and-eval, Approval-and-control, Chaos-and-drift. The canonical event shape is the dossier's **`harness_event` minimal schema** (cell_id, agent_id, declared_status, effective_status, preconditions, approval_tier, drift_signal GREEN/AMBER/RED/BLACK, outcome). The gate engine already exists as `epistemic_status.py` + `epistemic_status_invariant.py` (StatusedValue, min-rule enforcement, P0Incident on laundering, append-only StatusRecord, DriftDetector). The constitutional gate's auto-vs-escalate decision is the `approval_tier` field. Reuse these; the new work is wiring real collectors into them, not designing them afresh.

Amplified has rich observability raw material (Vellum ledger, a DuckDB analytics engine, cost logs, GitHub, GitLens, optional Langfuse/Opik) but it is **scattered and partly decayed** — there is no single pane. Build the nuclear-control-room: one deterministic core that gathers every signal into one surface, deterministic rules that fire without an LLM, and a thin Perplexity-style decipherment layer on top that explains anomalies and routes fixes back through Vellum.

You run as **Claude on the M5 (MacBook Air, `MacAirM5`)**, reaching the Beast **over Tailscale** (tailnet `tail27a0cc.ts.net`). This route is what makes the job possible — a sandboxed agent has no network and cannot reach the Beast at all. **Harden the link in before building:** confirm the Beast's tailnet address resolves and the Vellum API + Postgres answer over the tailnet, and pull secrets from Infisical (not from stale local files). The link being live and durable is a precondition, not a step you discover mid-build. Watch two blind spots: (a) **do not put an LLM in the deterministic runtime path** — it caps every metric at INTUITED and the control room then lies; (b) **do not use MCP for the automated collector path** — MCP is ~30–40× CLI token cost; use `gh`, direct HTTP, direct SQL.

Unusual constraints: the live link (M5 → Tailscale → Beast) is the whole point — verify against real data, not fixtures. If the tailnet path is down, fixing/hardening it is the first deliverable, ahead of any collector code. Two things are currently **broken** and must be fixed as part of this job, not deferred: Vellum JWTs **expired 2026-06-16**, and the `estate-machine` service stack appears **down** (Traefik up, all `/api/v1/*` routers absent — `api.amplifiedpartners.ai` returns the bare Traefik 404).

## 3. SPEC CHECKLIST — what counts as done

- **Live link hardened first:** the M5 reaches the Beast over Tailscale durably (tailnet name resolves, Vellum `:8400` and Postgres answer, secrets pulled from Infisical). Captured as a repeatable check, not a one-time manual success.
- A repo `Amplified-Partners/control-centre` exists, building green in CI.
- It **extends the existing** `fleet-vellum/vellum/analytics/engine.py` DuckDB registry — adds `stats_events` + `stats_findings` tables (see the starter schema at `control-centre/core/schema.py` in the perplexity workspace handoff) — rather than building a parallel store. No second source of truth.
- Collectors exist and run deterministically, **CLI/direct, never MCP**: GitHub (`gh`), LiteLLM/cost-log, Vellum (HTTP `:8400`), brain (direct SQL). Each emits normalised `stats_events` rows carrying `source`, `metric`, `scope`, `tier`, `timestamp`.
- A deterministic rule engine fires `stats_findings` with no LLM in path: thresholds, drift, **credential_freshness**, **automation_liveness**, chain-continuity, tier-laundering. Rows stay STRUCTURED.
- A decipherment reader queries the DuckDB surface **directly** (not via MCP), explains/correlates fired findings, and emits `problem_observed`/`fix_proposed` events into Vellum. These rows are correctly capped INTUITED and never merged into core `stats_events`.
- **The constitutional gate is implemented as code, extending the existing engine** — eight predicate functions layered on `epistemic_status_invariant.py`, each tagged **T1/T2/T3** per the Deterministic-AI Partition Test, returning pass / fail / unevaluable, every evaluation an append-only StatusRecord witnessed in Vellum. T1 predicates auto-evaluate deterministically; T2 escalate but log a code-gap with a graduation trigger; T3 route to AI (capped INTUITED) and escalate. The gate's verdict sets `harness_event.approval_tier` (auto vs escalate). A fix **auto-applies only when all eight pass deterministically (all T1, all pass)**; any T2/T3/fail/unevaluable → escalate. The gate result is a `stats_findings` row carrying a `drift_signal`.
- **The T1/T2/T3 partition map of the eight predicates is itself a tracked artefact** — each predicate's current tier and its graduation trigger are recorded and monitored, so the deterministic frontier provably expands rather than stalling. A predicate stuck in T2 with a fired trigger is itself a finding.
- **Fix loop is closed and autonomous within the gate:** finding → decipher → gate evaluates → pass: apply (via pipe) + log; fail/unevaluable: escalate. No blanket human-in-the-loop on every fix.
- **Fixed as part of this job:** fresh Vellum JWT minting wired (rotation, not a one-off); and a one-line status on whether the `estate-machine` stack being down is intentional or a regression — if regression, the routers are restored or a ticket is filed with the cause.
- One pane: a single command (or the existing `generate_monitoring` job) renders the unified view from `stats_events`/`stats_findings`.
- Out of scope: GitKraken API collector (lowest value, defer); any write to the Beast that bypasses the pipe. The fixer-router and gated auto-apply ARE in scope — but auto-apply is allowed ONLY through the constitutional gate, never ungated.

## 4. RESEARCH CHECKLIST — what counts as enough

- Primary sources: the live Beast **reached over Tailscale from the M5** (Vellum API, the Postgres DBs, LiteLLM proxy, cost-log), and the repos `fleet-vellum`, `estate-cost-tools`, `estate-machine`, `brain-mcp`.
- Canonical contracts to match exactly, not reinvent: the Vellum packet schema (`fleet-vellum/rust/.../PACKET_SCHEMA.md`), the DuckDB registry (`engine.py`), the **`harness_event` schema and 17-20-field rich packet** from `amplified-harness-control-plane-dossier.md`, and the **epistemic invariant modules** (`epistemic_status.py`, `epistemic_status_invariant.py`).
- Determine the live state of `estate-machine` from evidence (running routers, logs, container state), not from this brief's snapshot — the public 404 was one probe from a sandbox; verify on the tailnet before concluding up or down.
- Stop condition: once the four collectors emit real rows and at least one deterministic rule fires on live data, stop investigating and build.
- If live data contradicts the schema in the repo, **stop and surface** — do not silently adapt the canonical contract.
- "Asking Ewan" is not research — only escalate after two direct attempts plus one researched attempt on a blocker.

## 5. JOB CHECKLIST — what you must produce and verify

- Record a short plan (intent) in Vellum before execution.
- Two direct attempts on each blocker, one researched attempt, then wrap with a clear gap note — no thrashing.
- Durable artefacts: the repo + commits + Vellum events. Not chat output.
- Verify against the SPEC CHECKLIST box-by-box; "done" means every box ticked on **live** data.
- Emit Vellum events for: problems observed (incl. the expired-JWT and stack-down findings), fixes applied, decisions, deferrals, open questions.
- Session-close manifest: intent_id, repos/files touched, what ran on live data, what is deferred, outcome.
- Forbidden moves: LLM in the deterministic runtime; MCP in the automated collector path; auto-applying fixes **without passing the constitutional gate** (gated auto-apply is correct; ungated is forbidden); writing to the Beast outside the pipe; a second analytics store parallel to the DuckDB engine; an AI ratifying its own action when a gate predicate is unevaluable (that is the human-escalation case).

## 6. THE PROMPT (hand-off ready)

```
You are Claude running on the M5 (MacBook Air, MacAirM5), reaching the Beast over Tailscale (tailnet tail27a0cc.ts.net) with Infisical secrets and live DB access. Today is 2026-06-24.

Here is the spine, the lens, and the three checklists for building the Amplified control centre — one deterministic observability pane over Vellum, cost logs, GitHub, and the brain.

[paste THE SPINE]
[paste THE LENS]

The contract is the SPEC CHECKLIST.
The research budget is the RESEARCH CHECKLIST.
The work discipline is the JOB CHECKLIST.

[paste the three checklists]

First harden the M5→Tailscale→Beast link (resolve the tailnet host, confirm Vellum :8400 + Postgres answer, secrets from Infisical) and capture it as a repeatable check — this is deliverable zero. Ratification is autonomous via a code-enforced constitutional gate (eight predicates: honesty/transparency/attribution/win-win/meritocracy/privacy/security/sovereignty); the AI applies fixes when all eight pass and escalates to the human ONLY when a predicate fails or can't be evaluated — the human is the exception, not the default signer. Key non-negotiables: no LLM in the deterministic runtime (it caps metrics at INTUITED); no MCP in the automated collector path (use gh / direct HTTP / direct SQL — MCP is ~30-40x the token cost); extend the existing DuckDB analytics engine, do not build a parallel store; never write to the Beast outside the pipe; never auto-apply ungated. Fix the expired Vellum JWTs and report on the down service stack as part of the job.

A starter schema (core/schema.py) and the as-is/to-be design are in the Perplexity workspace handoff — use them as the head start, not gospel.

You are an expert partner. Use your judgement. Resilience without thrash: two direct attempts, one researched, then wrap. Hand back with a session-close manifest.
```

---

**Sized for:** Claude on the M5, reaching the Beast over Tailscale.
**Assumed:** the DuckDB analytics engine in `fleet-vellum` is the intended deterministic core (verified present); LiteLLM proxy is the canonical token-cost source (in-path).
**Open question (only if blocking):** is the `estate-machine` stack being down intentional? If you already know, tell Claude in one line; if not, the brief already tasks Claude to determine it.
