# Research-Pipe Run — Claude Code Brief (v02)

TIER: STRUCTURED · brief design from `expert-partner-brief` + `succinct-complete-output` + `amplified-standing-grants` + tiered-evidence-routing loop (memory/notes/work/Amplified/evidence_routing/tiered_loop.md) + minimize-AI-scope doctrine (memory/notes/work/philosophy/ai_system_design/minimize_ai_scope.md); component list MEASURED from inbox; reflex design grounded in SRE / Erlang OTP / SPC / Shewhart / FMECA prior art.
PROVENANCE: `AMPLIFIED-IDE__architecture-plan__v01__2026-06-24__perplexity.md` + 16 thread briefs in this inbox + session memory + tiered-loop standing law.
STATUS: implementation-ready · run on Beast via Tailscale · Perplexity standing-grants Tier A throughout.
SUPERSEDES: v01 (kept in workspace for audit trail). Changes: three-reflex shape + friction sensing + criticality classification + tiered-loop discipline + endpoint frame upgraded to 13 fields.
FOR: Claude Code on M5 → Tailscale → Beast research pipe (browser-equipped, not Perplexity).

---

## The goal (read first, every turn — GOAL-LOCK)

**An AI-native operating system that takes any task and runs it end-to-end.** Research → do-with-the-research → output. HITL is the exception, not the rule. The system spots its own thrash, finds the cause, and emits a deterministic patch (harness/hook/rule/schema/guard) so the same problem can never recur. **Blinkers without ceilings** — every patch is one fewer problem AI re-solves; AI's free capacity grows; the floor compounds.

The endpoint of every layer is **AI sits where AI should sit, deterministic code sits everywhere else.** Python+Rust hold the difficult deterministic bits so AI isn't asked to be a unicycling genius (Ewan's own framing). AI handles bounded, well-prepared problems where doing a reasonable job is enough and there's still room to excel.

**Make money so we can give it away.** GOAL-LOCK: if a sub-agent finds itself off-goal, stop. Don't research a tangent.

---

## What the research pipe is (and isn't)

- **The pipe** is on the Beast. It has its own browser. It is **not Perplexity**. Perplexity teed this up; Claude Code drives it.
- The pipe runs on the **tiered evidence-routing loop** (your existing standing law — see Operating Discipline below).
- It runs **three passes per component** (Prior Art → Translation → Endpoint).
- It outputs **code-ready endpoint docs** with the **13-field shape** below — Python/Rust boundaries explicit, friction sensing + recovery mode + criticality classification all first-class.
- It produces **deterministic patches** as first-class artifacts — the real product. Every patch closes a class of thrash permanently.
- Output is **NOT a finished system.** It is the feedstock for the next job (Perplexity does build-sequence synthesis after the pipe returns).

---

## Operating discipline — the tiered loop (anti-thrash by design)

Every sub-agent in every pass follows this discipline. It is the existing Amplified standing law (`evidence_routing/tiered_loop.md`, 2026-06-06):

1. **Brain first.** Read the Amplified Brain for what's already known about this component. Do not ask Perplexity/the web on unsharpened questions.
2. **Epistemic + rods check.** Apply min-rule + the 5 rods. Tier what's found.
3. **Two serious local attempts.** Engineer/expert sub-agent assesses the actual problem with what the Brain returned.
4. **Sharpen.** If two attempts fail, **stop looping locally. Sharpen the exact problem.** This is the anti-thrash move — the failure to sharpen is what generates infinite agent thrash.
5. **One focused web ask.** With the sharpened problem, use the Beast's browser (or SearXNG) for one focused research pass.
6. **One more iteration only if clear progress + realistic chance of success.** Otherwise wrap.
7. **Blind-alley write-up.** If still stuck after the focused ask, write it up as a blind alley or evidence-something-is-missing. **This write-up IS a deterministic patch** — it teaches the floor "don't loop on this shape again without doing X first." Patch goes to `patches/deterministic-patches.jsonl`.

**The thrash artifact is the primary output of failure, not the failure itself.** Every blind alley mined makes the next run faster. This is the homeostatic loop in its actual form.

---

## Live blockers — clear these first (in order)

### 0.1 — Tailscale isn't running on M5 at last probe (12:34 BST 2026-06-24)

`tailscale status` returned *"failed to connect to local Tailscale service; is Tailscale running?"* Binary at `/usr/local/bin/tailscale`. App at `/Applications/Tailscale.app/`.
**Action:** start Tailscale; verify M5 sees the Beast tailnet.

### 0.2 — Vellum JWTs are 8 days expired (full diagnosis: `vellum-jwt-recovery` brief in this inbox)

- Signing secret intact and verified. `VELLUM_JWT_SECRET` in `~/.vellum/intent-interface.env`, 28 chars, SHA256[:12] = `f49b1c6ca041`. Cryptographically verifies all three expired tokens.
- **Mint locally** with new 30d TTL. Tier B proxy-sign (logged), Ewan ratifies on placement.
- Add `sheet_id` to `shared_dev_jwt` before mint.
- Static Vellum bearer token still works as fallback (startup.log HTTP 200 through 2026-06-23).
- Infisical is pre-existing dark (4 projects, 0 secrets). Stopgap auto-mint cron; populate Infisical in L2 work later.

### 0.3 — `estate-machine` stack appeared dark at 09:30 UTC

Traefik default backend "404 page not found" — Traefik up, zero routers loaded. Probe live before assuming. If down, bring up before the pipe can run.

### 0.4 — Connect PostgreSQL connector in Perplexity

One-click action from Perplexity settings. ~1 minute. Unblocks L3 read of vellum + brain stats. Tier A for Claude (Ewan's connector but Claude can prompt single-ask in-line).

**Closure rule for Phase 0:** all four clear in one pass, or stop with a single hand-back listing only those that genuinely couldn't be cleared. Not four hand-backs.

---

## The three reflexes (the homeostatic shape of every component)

This is the design backbone. Every component the pipe processes must spec all three:

### Reflex 1 — REACT (failure has happened)

- Failure senses fire → deterministic core reads → fallback triggered → system keeps going in degraded mode → root cause logged → deterministic patch emitted → patch lands in code → that failure shape cannot recur.
- Prior art: Nygard *Release It!* circuit-breakers; Erlang/OTP supervision trees; mil-spec FRACAS (Failure Reporting Analysis & Corrective Action System); SRE postmortem action-item discipline.

### Reflex 2 — PREDICT (failure is likely to happen, gradient is bad)

- Friction senses watch **gradients and patterns**, not levels. Rising retry counts. Latency creep. Cache-hit sagging. Two components disagreeing on tier. Drift-signal climbing G→A but not yet R. Spend velocity ahead of forecast. A subagent that thrashed on a similar input last time.
- When friction crosses threshold → deterministic **pre-emptive mitigation** fires *before* the failure → if mitigation insufficient, escalate to Reflex 1.
- Prior art: Shewhart SPC (1924) — leading indicators, control limits; Google SRE error-budget burn-rate alerts; Thom catastrophe theory (when gradients tip into state changes); immunology adaptive surveillance (T-cell patrol without symptoms).

### Reflex 3 — RECOVER (degraded mode can't sustain)

- When Reflex 1's fallbacks log "fallback active" + Reflex 2 says "fallback's own gradient is bad" — meaning the redundancy itself is failing — the component enters **recovery mode**: a known-safe state with reduced surface. It still observes, logs, and accepts HITL input. It does NOT pretend to be operational. **Loud, not silent.**
- The Intent Interface shows recovery state; Vellum logs it; agents in cells get the signal and pull back to non-critical work.
- Prior art: aviation "land the plane" mode; submarine silent-running; SIL (safety integrity levels) in industrial control; CDN graceful degradation; Erlang "let it crash" with multi-level supervisor recovery.

### The three sense types

Same Vellum schema, different sense category:

- `level_sense` — fired by Reflex 1 (failure crossed threshold).
- `gradient_sense` — fired by Reflex 2 (rate-of-change predicts threshold-crossing within N units).
- `pattern_sense` — fired by Reflex 2 (correlation with a known failure-precursor pattern).

The deterministic core consumes all three.

### Criticality classification (FMECA)

Not everywhere gets the full triple-reflex treatment — that would be unbuildable. Each component, in Pass 3, identifies its own **critical points** and triages:

- **CRITICAL** — full triple-reflex (R1+R2+R3). Examples: L2 Pipe writes, L4 RodGuard, L3 deterministic core gate.
- **IMPORTANT** — Reflex 1 + Reflex 2, no formal Recovery (graceful degradation handles it). Examples: L5 routing, L1 lake/pool writes.
- **STANDARD** — Reflex 1 only. Examples: agent inside a cell on a non-money-affecting task.
- **BEST-EFFORT** — no reflex (failure has no compounding cost). Examples: a single Perplexity decipher pass; can just retry on the next overview tick.

Prior art: mil-spec FMECA — failure modes, effects, **criticality** analysis. Triage is part of the endpoint, not an afterthought.

---

## What goes through the pipe (the input set)

**28 named components** — 25 layer-anchored + 3 cross-cutting. (Same as v01.)

### L7 — User door
1. Intent Interface (Cockpit) · Electron · only user door · canonical branch `cursor/20260623120000/vellum-ui-lens`
2. `markPass.ts` certainty + ambiguity (1-9 + ▲) — input-side honesty

### L6.5 — Overview (Perplexity's role today; the seat, not the vendor)
3. Overview layer mechanics — read-only-what's-on-fire, cross-source decipherment, actionable-insight emission, Vellum-summons protocol

### L6 — Agent work surfaces
4. Sealed cells (Apple Container, 4×) on Mac mini
5. Manufacturer-native config per agent (Claude/Cursor/Devin/Antigravity)
6. VSCodium agent lane
7. Per-cell repo + worktree discipline (Agent Worktree Contract)
8. Asset inventory + canonical clean-build resolution

### L5 — Routing
9. One LiteLLM = `estate-token-router` — credit-first, multi-provider, deterministic
10. `estate-cost-tools` as middleware (caching, compaction, Haiku routing, cost log)
11. Production-Law gate inside the router — every job lands or surfaces
12. DeerFlow trial — Beast-only, one-task experiment

### L4 — Runtime gate
13. `amplified_permissions.classify()` — A/B/C ladder
14. Baton — single write lease across the estate
15. RodGuard circuit breaker — trips on 5-rod violation or P0
16. Door-open event schema in Vellum

### L3 — Deterministic spine
17. Deterministic core — gatherer + decipherer; LLMs build it, the built core runs without them
18. `harness_event` schema with `approval_tier` + `drift_signal` G/A/R/B
19. `epistemic_status.py` + `epistemic_status_invariant.py` — min-rule, P0-on-laundering, DriftDetector
20. Vellum senses (`sensor_event.py`) — types, what each watches, what `drift_signal` raises

### L2 — Pipe / substrate
21. Relay/Vellum doctrine — write `relay_protocol.md`; 10-component scope; 9-item pre-production gate; outcome-language convention
22. The Pipe contract — Python + Rust + Vellum + AI + Human; no side doors

### L1 — Persistence
23. Path 1 verbatim lake — attributed, immutable, bronze→DuckDB gold
24. Path 2 neutralised pool — Presidio/spaCy + HMAC-SHA256, identity-blind, diffable vs lake, PUDDING-ready

### L0 — Infrastructure
25. Estate topology + Tailscale — M5/Mac mini/M4/Beast; redundancy contract per node

### Cross-cutting
26. **Homeostatic spine** — Ashby/Toyota/SRE/immunology lineage applied to the whole
27. **GitHub hardening** — branch protection, CODEOWNERS, no agent self-approval, signed commits
28. **Token-efficiency PROOF-OF-LIFE gate** — §9 acceptance run; how we know the system actually works under load

---

## The three passes (per component)

### Pass 1 — PRIOR ART (full breadth, runs first, via the tiered loop)

For each component, a sub-agent finds:
- **Where was this pattern first solved?** Field (any: cybernetics, control theory, biology, manufacturing, SRE, distributed systems, economics, military, civil engineering, finance, anything).
- **By whom?** Named originator(s).
- **When?** Year, primary publication.
- **With what result?** What worked at what scale.
- **What did they get wrong?** Failure modes the prior art warned about.
- **Tier each finding** at source. MEASURED if benchmarked at source; STRUCTURED if synthesised; INTUITED if claim only.

Apply the tiered loop: Brain first; sharpen if local-only insufficient; ONE focused web ask; blind-alley write-up if stuck.

**Mandatory canon for the homeostatic spine sub-agent (#26):**
- Ashby — *Design for a Brain* (1952), *Introduction to Cybernetics* (1956), Law of Requisite Variety, ultrastable system
- Wiener — *Cybernetics* (1948)
- Cannon — *The Wisdom of the Body* (1932), homeostasis
- Maturana & Varela — *Autopoiesis and Cognition* (1980)
- Beer — Viable System Model (1972)
- Shewhart — Statistical Process Control (1924); Deming PDSA loop
- Toyota Production System (Ohno, 1988) — jidoka, andon, 5 whys, poka-yoke
- FRACAS / FMEA / FMECA (mil-spec, 1960s onward)
- Hollnagel & Woods — *Resilience Engineering* (2006), Safety-II
- Reason — *Human Error* (1990), Swiss cheese model
- Perrow — *Normal Accidents* (1984)
- Goldratt — Theory of Constraints
- Taguchi — quality engineering, robust design
- Google SRE — Beyer et al. (2016), error budgets, burn-rate alerts
- Nygard — *Release It!* (circuit breakers, bulkheads)
- Janeway — *Immunobiology* (innate vs adaptive immunity, immune memory)
- Forrester — system dynamics (1961)
- Thom — catastrophe theory

**Per-layer seeds** (sub-agents extend, don't limit):
- L7 / certainty marking — Tetlock (forecasting), Brier scores, Bayesian elicitation, aviation CRM, surgical timeout protocols
- L6.5 / overview — NASA mission control, ATC, hospital command centres, Boyd OODA, SRE on-call, NOCs
- L6 / sealed cells — KeyKOS, seL4, Qubes OS, gVisor, unikernels, Erlang/OTP, microkernels
- L5 / routing — Hungarian algorithm, Kelly criterion, real-time bidding, Borg, Kubernetes, market microstructure
- L4 / Baton + circuit breaker — Lamport distributed locking, Raft/Paxos, capability tickets, deadman switches
- L3 / drift detection + deterministic gate — Shewhart SPC, CUSUM, PID controllers, Kalman filters, anomaly detection
- L2 / immutable ledger — event sourcing (Fowler), CRDTs, Merkle trees, Datomic, Kafka, LMAX Disruptor, double-entry accounting (1494)
- L1 / lake + pool / neutralisation — Kimball/Inmon, differential privacy, k-anonymity, federated learning, GDPR pseudonymisation
- L0 / topology + redundancy — CAP/PACELC, ARPANET resilience, CDNs, mesh networking, ham radio failover

Sub-agent uses the **browser** (real web, primary sources). LLM memory is not a source.

### Pass 2 — TRANSLATION

For each component, after Pass 1 returns:
- **Map the prior-art mechanism onto our component.** Their X = our Y.
- **Name the equivalences explicitly.** No hand-waving.
- **Name the differences honestly.** Where does the analogy break?
- **Cite primary sources, don't paraphrase.** Radical attribution.
- **KILL decision gate:** if Pass 1+2 reveal the mechanism is known not to work (or only under conditions we don't have), **emit a KILL recommendation.** Re-scoping or killing is a win at this stage.

### Pass 3 — ENDPOINT (only if component survives Pass 2) — the 13-field shape

```
Logic                       why it works on the system it regulates (grounded in prior art)
Methodology                 how to build/run it (informed by prior art)
Python/Rust boundary        explicit split:
                            - what is deterministic Python (orchestration)
                            - what is deterministic Rust (spine, perf-critical, safety-critical)
                            - what genuinely requires LLM judgment
                            - exact boundary line and why (minimize_ai_scope doctrine)
Senses
  ├─ failure senses         (level_sense — Reflex 1 triggers)
  └─ friction senses        (gradient_sense + pattern_sense — Reflex 2 triggers)
Failure modes               FMEA-style: mode, cause, effect, detection, severity
Friction patterns           the gradients/patterns that predict each failure mode
                            with thresholds and pre-emptive mitigations
Redundancy                  Reflex 1 fallback path
                            - which other component absorbs the work
                            - degraded-mode behaviour (loud-not-silent)
Self-heal                   deterministic recovery within Reflex 1
                            - 3-layer pattern: in-process retry / supervisor restart / RUNBOOK
                            - bounded retry counts; no infinite loops
Degraded mode               what the component does when its primary path fails
                            but it must keep contributing — visible, loud, honest
Recovery mode               Reflex 3 — known-safe state when degraded can't hold
                            - reduced surface, observation-only, HITL-accepting
                            - what triggers entry / exit
                            - how Intent Interface + Vellum see it
Criticality classification  CRITICAL / IMPORTANT / STANDARD / BEST-EFFORT (FMECA)
                            - which reflexes apply at this component
                            - justification
Surface conditions          when ALL reflexes exhaust and HITL is the only option
                            - the only path to Ewan
                            - what context surfaces with it (failed attempts shown)
Deterministic patches       the rules/hooks/schemas this component adds to the floor
                            patch format: { where, what, why, acceptance_test }
                            each patch closes a class of thrash permanently
Acceptance test             proof component works AND fails safely:
                            - happy path passes
                            - each failure mode triggers correct redundancy + self-heal
                            - each friction pattern triggers pre-emptive mitigation
                            - degraded mode is loud, not silent
                            - recovery mode entry/exit is loud and bounded
Build sequence              what must exist before this can be built
                            - dependencies on other components (by name)
                            - external deps (libraries, services, hardware)
                            - prerequisite Phase 0 unblocks satisfied
```

13 fields (senses are one field with two parts). Anything missing = not at endpoint.

---

## Thrash-mining (the recursion rule, via the tiered loop)

Per `evidence_routing/tiered_loop.md`, each sub-agent attempts a pass via:
1. **Brain-first read** (most authoritative for our own prior work).
2. **Two serious local attempts** with what Brain returned.
3. **Sharpen + one focused web ask** through the Beast pipe's browser.
4. **One more iteration only if clear progress + realistic chance.**
5. **Blind-alley write-up** if still stuck — this IS the patch.

When stuck, the sub-agent emits a **thrash artifact**:

```json
{
  "component": "<name>",
  "pass": "1|2|3",
  "loop_stages_run": ["brain", "local_attempt_1", "local_attempt_2", "sharpen", "focused_ask"],
  "what_was_tried": "...",
  "what_failed_and_why": "...",
  "what_a_human_would_need_to_unstick_this": "...",
  "proposed_deterministic_patch": {
    "where": "...",
    "what": "...",
    "why": "...",
    "acceptance_test": "..."
  },
  "criticality_if_unfixed": "CRITICAL|IMPORTANT|STANDARD|BEST_EFFORT"
}
```

**The patch is the primary output. The thrash is just where the patch came from.**

---

## Output destination

`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/beast-pipe-outputs__2026-06-24/`:

- `prior-art/<component>.md` — Pass 1 outputs
- `translation/<component>.md` — Pass 2 outputs (including KILL recommendations)
- `endpoints/<component>.md` — Pass 3 outputs (13-field shape)
- `patches/deterministic-patches.jsonl` — every patch emitted across all passes, one JSON per line
- `thrash/<component>__<pass>.md` — thrash artifacts that surfaced
- `INDEX.md` — what ran, what completed, what surfaced, what killed; final `[CLOSURE]` footer

Perplexity reads this folder when the pipe returns and does **Job B (build-sequence synthesis)** — dependency graph across all 28 components → master build sequence → `MASTER-BUILD-SEQUENCE__v01__2026-06-24__perplexity.md` to inbox root. From there the next AI codes.

---

## Constraints (non-negotiable)

- **Pipe discipline.** Drafts in workspace; commits to Beast/Vellum through the Pipe. No side doors.
- **Min-rule.** Every output carries tier and provenance. Effective tier = MIN of inputs. Silent promotion = P0 halt.
- **Radical attribution.** Every claim has source URL + date + reliability tier. Primary > secondary > tertiary.
- **GOAL-LOCK.** Off-goal sub-agent = stop and surface. Don't research tangents.
- **`[CLOSURE]` footer** on every sub-agent output + every Claude top-level turn.
- **Sandbox sovereignty.** No Beast writes outside the Pipe. No Mac trust-root writes from Beast-side code.
- **No LLM in the router.** L5 routing is deterministic; LLM only inside cells.
- **Loud failure beats silent failure.** Every component honest about degraded state.
- **Tiered loop is the only loop.** Brain-first, two local attempts, sharpen, one ask, write-up. No agents on Perplexity-equivalents for unsharpened questions.
- **Minimize AI scope.** Python+Rust holds deterministic logic; AI handles bounded well-prepared problems. Tests test the rules, not the AI.

---

## Acceptance test (the whole run)

The research-pipe run is **complete** when:

1. All 28 components have an endpoint doc OR a KILL OR a thrash artifact (no silent skips).
2. `deterministic-patches.jsonl` has ≥1 patch per layer (the floor grew).
3. `INDEX.md` enumerates everything — no missing components.
4. Every endpoint doc has all 13 fields populated (or missing fields explicitly "not yet verified" with why).
5. Every Pass 1 output cites ≥3 primary sources from outside AI.
6. Every Pass 2 output names ≥1 equivalence + ≥1 difference, or recommends KILL.
7. Every Pass 3 output has all 3 reflexes specified at its criticality level.
8. Thrash count logged (`N components hit thrash, M produced patches`) — even if zero.
9. Final `[CLOSURE]` footer on `INDEX.md`.

**No proof of completion = not done.** §9 PROOF-OF-LIFE pattern applied to research.

---

## What Perplexity does next (Job B, not part of this brief)

After Claude Code returns outputs to `beast-pipe-outputs__2026-06-24/`, Perplexity:

1. Reads every endpoint's `Build sequence` field.
2. Constructs the dependency graph across all 28 components.
3. Topologically sorts → emits master build sequence.
4. Cross-checks against the §9 PROOF-OF-LIFE gate, the redundancy contract, and the three-reflex coverage per criticality class.
5. Drops `MASTER-BUILD-SEQUENCE__v01__2026-06-24__perplexity.md` to the inbox root.
6. From there, the next AI codes from it.

---

## Constitution / grants compliance

- **Tier classifications** (per `amplified-standing-grants`):
  - Live probes via Tailscale = Tier A research.
  - Drafting fresh JWTs in workspace = Tier B (proxy-sign, logged).
  - Placing JWTs into `~/.amplified/stoa_claude_jwts.json` = Tier B (reversible, no external irreversible effect).
  - Pipe runs on Beast (read + Vellum-event drafts) = Tier A/B mix.
  - Direct Beast writes outside the pipe = Tier C, FORBIDDEN.
- **`[CLOSURE]` footer** required on every sub-agent + Claude top-level turn.
- **Drafted by AI as proxy, logged.** Routed to inbox.
- **No side door.** Beast writes only through the pipe.

---

## Hand-back to Ewan (collapsed)

**One gate:** ratify fresh JWT placements + confirm L1/L2 redundancy plan when it surfaces (likely Postgres replication + Vellum hot-standby + local-JSONL queue per Mac — per Pass 3 outputs).

Everything else self-resolves within the pipe per the tiered-loop + thrash rules.

[CLOSURE] branch=PLAN | proxy=1 logged (research-pipe brief v02 drafted as AI_PARTNER_PROXY) | gates=JWT placement ratification + L1/L2 redundancy plan ratification (one hand-back, after pipe returns Pass 3) | inbox=RESEARCH-PIPE-RUN__claude-code-brief__v02__2026-06-24__perplexity.md | tier=STRUCTURED
