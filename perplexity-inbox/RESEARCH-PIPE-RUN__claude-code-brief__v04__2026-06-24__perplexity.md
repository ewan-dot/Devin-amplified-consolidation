# Research-Pipe Run — Claude Code Brief (v04)

TIER: STRUCTURED · provenance for design from loaded skills + memory + this thread; component list MEASURED from inbox + this thread; reflex design grounded in SRE / Erlang OTP / SPC / Shewhart / FMECA prior art; reconciliation of v03 against 4 parallel sub-agent audits (completeness, consistency, prior-art coverage, constitution & honesty).
PROVENANCE: `AMPLIFIED-IDE__architecture-plan__v01__2026-06-24__perplexity.md` + 16 thread briefs in this inbox + session memory + tiered-loop standing law + conversation 2026-06-24 11:25-13:10 BST + audit findings in `/home/user/workspace/inbox-audit/v03-audit/` (4 files, ~1200 lines combined).
STATUS: **implementation-ready CONDITIONAL on Phase 0 + Phase 0.5 unblocks.** Downgrade from v03's unconditional "implementation-ready" — honest about what must clear first.
SUPERSEDES: v01 + v02 + v03 (kept in workspace for audit trail). v04 reconciles 29 audit findings across completeness, consistency, prior-art coverage, and constitution.
FOR: Claude Code on M5 → Tailscale → Beast research pipe (browser-equipped, not Perplexity).

---

## The goal (read first, every turn — GOAL-LOCK)

**An AI-native operating system that takes any task and runs it end-to-end.** Research → do-with-the-research → output. HITL is the exception. The system spots its own thrash, finds the cause, emits a deterministic patch (harness/hook/rule/schema/guard) so the same problem cannot recur. **Blinkers without ceilings** — every patch is one fewer problem AI re-solves; AI's free capacity grows; the floor compounds.

The endpoint of every layer: **AI sits where AI should sit; deterministic code sits everywhere else.** Python+Rust hold the difficult deterministic bits. AI handles bounded, well-prepared problems with room to excel.

**Make money so we can give it away.** GOAL-LOCK: if a sub-agent finds itself off-goal, stop. Don't research a tangent.

### GOAL-LOCK enforcement (mechanistic, not named-only)

Every sub-agent applies this test at start of every pass:

```
goal_link_check(pass_objective):
    1. Does this pass contribute to "the AI-native operating system can run any task end-to-end"? 
    2. Or to "cut recurring AI spend so we can give it away"?
    3. If yes — name the link in one line and proceed.
    4. If no — STOP. Emit "off-goal" thrash artifact. Return to orchestrator.
```

Recorded in pass output as `goal_link: "<one line>"`. INDEX.md acceptance test verifies every pass has a non-empty goal_link.

### The canonical equation

```
Python + Rust + (any other language that earns its place)
  + GitHub + telemetry + Vellum + AI + Human-in-the-loop
  = Amplified Partners
  = Amplified
```

Determinism floor (Python+Rust+others-that-pass-the-adoption-test) + governance (GitHub) + observation (telemetry: Langfuse + Opik + OTel + Vellum-as-ledger) + immutable substrate (Vellum) + AI (in cells, bounded) + human-in-the-loop (exception, ratifier-for-now). Pull any term and it collapses.

---

## The 5 Rods (verbatim, MEASURED from the Beast)

Source: `vault/store_b_clean/2026-04-21_06-founder-principles-and-constraints_Ewan_Sair_*.md`

1. **Radical honesty** — no robe. State the true thing even when it costs. False modesty and reverse-sycophancy are also robes.
2. **Radical transparency** — show the reasoning, the seams, the bias.
3. **Radical attribution** — every claim carries its source + evidence. No anonymous theft of ideas or authority.
4. **Win-win only** — money moves only when both sides end up better off. Never a take that costs the other side.
5. **Idea meritocracy** — best idea wins regardless of who authored it; no authority smuggled via voice or seniority.

**Meta-rule above all rods:** the goal > ego. Ties resolve to the goal. **Tie-break:** win-win trumps honesty on collision.

Every sub-agent must answer at end of each pass: *"Which rod did this pass test? How did the output protect or violate it?"* — Required in pass output as `rod_check: {tested, protected_or_violated, evidence}`.

---

## Standing-on-shoulders law

**We do not invent. We translate.** Every pattern has prior art somewhere — cybernetics, biology, manufacturing, SRE, military reliability, finance, civil engineering, distributed systems. The default assumption is *standing on shoulders of giants*, not invention. Genuine novelty is named where it exists.

### The search pattern: wide → narrow → wide → narrow → wide → narrow

Not a funnel. Bidirectional refinement:

```
WIDE 1   — survey: what domains have solved this kind of problem?
            Output: 5-8 candidate domains.
NARROW 1 — for each, who is the originator + what is the canonical text?
            Output: 5-8 candidate primary sources.
WIDE 2   — what adjacent fields cite or critique each canonical text?
            Output: cross-domain commentary, failure modes others identified.
NARROW 2 — among the cross-citations, which 2-3 sources converge on the mechanism?
            Output: 2-3 strongest convergent claims.
WIDE 3   — does the convergence hold in a third or fourth unrelated domain?
            Output: independent confirmation OR a contradicting domain.
NARROW 3 — settle the endpoint claim with its multi-domain attribution.
            Output: the endpoint, tier-tagged, attributed.
```

**Endpoint condition: multi-domain convergence.** Multi-domain means ≥3 **unrelated founding disciplines**, defined below. Single-source claims cap at INTUITED.

### "Unrelated fields" — enforceable definition (v04 patch)

Two sources are in the **same field** if any of the following is true:

- They share a common ancestor paper (e.g. Lampson's *Confinement Problem* 1973 is the common ancestor of KeyKOS, seL4, gVisor — they are one field).
- They are sub-disciplines of the same broader discipline (e.g. Shewhart SPC, CUSUM, PID, Kalman, anomaly detection are all *statistical/control engineering*).
- They are different vendors implementing the same pattern (e.g. PagerDuty + Opsgenie + VictorOps are one pattern, three products).
- They are different views of the same dataset/experiment (primary paper + review + textbook citing both — one).

A sub-agent must name **the founding discipline** for each source cited. Two sources naming the same founding discipline = one field. Multi-domain convergence requires **≥3 distinct founding disciplines**.

### Non-pejorative language (anti-bias gate)

Every sub-agent loads `neutral-research-brief` at start. No charged words: no "best practice", "modern", "outdated", "bad", "good", "superior". Replace with evidence: *"X did Y at scale Z; W is the known failure mode in [source]"*. Let evidence settle. Audit at sub-agent close.

### Outcome-language convention (from Relay protocol brief)

For describing system failures or agent shortfalls, use behavioural descriptions rather than moralised ones:

- *deception-equivalent output* (not "lying")
- *avoidance-equivalent behaviour* (not "ducking")
- *lazy-equivalent work* (not "lazy")
- *sycophancy / reverse sycophancy*
- *route failure*
- *overbuild*
- *source failure*

No moral theatre. Describe the shape; fix the process.

### Fallibility-of-all

Sources are fallible. Originators are fallible. We are fallible. A single source is not the endpoint. **The endpoint is the convergence.** Disagreements between sources are preserved in output, not arbitrated. Multi-domain convergence is the structural defence against fallibility. (This claim itself is INTUITED — defended by analogy to Ashby's requisite variety and SRE's multi-signal correlation; the meta-claim is not yet measured.)

### Adoption-test law (no bandwagon; nothing binned; everything parked)

Before adopting any new tool/framework/model/methodology:

```
1. What problem does this solve?
2. Do we have that problem?
3. If yes — does it solve it better than what we use now (measured, not asserted)?
4. If yes — what is the integration cost (tokens, time, dependency surface)?
5. If integration cost < expected benefit — adopt with sunset condition.
6. If unclear — PARK, not bin. Note the re-evaluation trigger.
```

**Nothing is binned. Things are parked.** Parked items live in the data lake + Brain with reason-for-parking and re-evaluation trigger. When trigger fires, parked item re-enters the test loop. **No work wasted; some work waiting.**

### PARK outcome schema (v04 addition)

When Pass 2 recommends PARK (rather than KILL):

```json
{
  "outcome": "PARK",
  "component": "<name>",
  "reason_for_parking": "<not-a-fit-now-but-might-be-later>",
  "what_problem_it_solves": "<the problem we don't have today>",
  "re_evaluation_trigger": "<the condition that would make us revisit>",
  "stored_at": "data_lake://parked/<component>__<timestamp>.md",
  "brain_tag": "parked:<component>:<trigger>",
  "parked_by": "AI_PARTNER_PROXY",
  "parked_at": "<iso8601>"
}
```

Night Scout watches park triggers nightly and surfaces when one fires.

---

## What the research pipe is (and isn't)

- The pipe is on the **Beast**. It has its own browser. **It is not Perplexity.** Perplexity teed this up; Claude Code drives it.
- The pipe runs on the **tiered evidence-routing loop** (standing law — see Operating Discipline).
- It runs **three passes per component** (Prior Art → Translation → Endpoint).
- It outputs **code-ready endpoint docs** with the 13-field shape — Python/Rust boundaries explicit, friction sensing + recovery mode + criticality classification all first-class.
- It produces **deterministic patches** as first-class artifacts — the real product. Every patch closes a class of thrash permanently.
- It registers each completed component with **Night Scout** so the floor stays current without re-research.
- Output is **NOT a finished system.** Feedstock for Job B (Perplexity does build-sequence synthesis after the pipe returns).

---

## Operating discipline — the tiered loop (anti-thrash)

Every sub-agent in every pass follows this (`evidence_routing/tiered_loop.md`, 2026-06-06):

1. **Brain first.** Read the Amplified Brain for what's already known. Do not ask Perplexity/the web on unsharpened questions.
2. **Epistemic + rods check.** Apply min-rule + the 5 rods. Tier what's found.
3. **Two serious local attempts.** Engineer/expert sub-agent assesses the actual problem with what Brain returned.
4. **Sharpen.** If two attempts fail, stop looping locally. Sharpen the exact problem.
5. **One focused web ask.** Use the Beast's browser (or SearXNG) — applying the wide-narrow pattern.
6. **One more iteration only if clear progress + realistic chance of success.** Otherwise wrap.
7. **Blind-alley write-up.** If still stuck, write up as blind alley / evidence-something-is-missing. **This write-up IS a deterministic patch.** Goes to `patches/deterministic-patches.jsonl`.

The thrash artifact is the primary output of failure. Every blind alley mined makes the next run faster.

---

## Live blockers — clear these first (in order)

### Phase 0 — system-state unblocks

#### 0.1 — Tailscale isn't running on M5 at last probe (12:34 BST 2026-06-24)
Binary at `/usr/local/bin/tailscale`. App at `/Applications/Tailscale.app/`. Start; verify M5 sees Beast tailnet.

#### 0.2 — Vellum JWTs are 8 days expired (full diagnosis: `vellum-jwt-recovery` brief)
- Signing secret intact and verified (`VELLUM_JWT_SECRET`, SHA256[:12] = `f49b1c6ca041`) — **verifies the token signatures, does NOT confirm the Beast service currently accepts the same key.** Live verification step required.
- Mint locally with new 30d TTL. Tier B proxy-sign (logged — see Proxy Log Format below).
- Add `sheet_id` to `shared_dev_jwt` before mint.
- Static bearer fallback worked through 2026-06-23 (per startup.log) — INTUITED for current state.
- Infisical pre-existing dark (4 projects, 0 secrets); stopgap auto-mint cron.

#### 0.3 — `estate-machine` stack appeared dark at 09:30 UTC
Traefik default "404 page not found" — zero routers loaded. **STATUS: INTUITED at time of probe; current state requires live re-verification.** If down, bring up before pipe runs.

#### 0.4 — Connect PostgreSQL connector in Perplexity
One-click, ~1 minute. Unblocks L3 read of vellum + brain stats.

#### 0.5 — OPEC = OpenTelemetry confirmation (from `3ae460be`)
One-line confirmation from Ewan. Unblocks telemetry sub-agent on component #20.

### Phase 0.5 — gating facts that block Pass 3 sizing

#### 0.5.1 — Mac mini RAM number
Open across multiple briefs. Locks Qwen2.5-Coder 14B Q4 sizing and the local-lane §9.6 PROOF-OF-LIFE proof. (Ewan-only.)

#### 0.5.2 — Night Scout live-status confirmation
The Night Scout registration design depends on Night Scout actually running. **STATUS: STRUCTURED-from-prior-design, INTUITED for current live state.** Verify the Night Scout service is operational, or downgrade Night Scout from "existing design" to "design-to-build" in v04 implementation order.

**Closure rule for Phase 0 + 0.5:** all clear in one pass, or single hand-back listing only what genuinely couldn't clear. Not separate hand-backs per item.

---

## The three reflexes (homeostatic shape)

### Reflex 1 — REACT (failure has happened)
Senses fire → deterministic core reads → fallback triggered → degraded mode → root cause logged → patch emitted → patch in code → that failure shape cannot recur.
Prior art: Nygard *Release It!* circuit-breakers; Erlang/OTP supervision; mil-spec FRACAS; SRE postmortem discipline.

### Reflex 2 — PREDICT (failure is likely; gradient is bad)
Friction senses watch **gradients and patterns**, not levels. Rising retry counts. Latency creep. Cache-hit sagging. Two components disagreeing on tier. Drift-signal climbing G→A but not yet R. Spend velocity ahead of forecast. A subagent that thrashed on a similar input last time. Threshold crossed → deterministic pre-emptive mitigation fires *before* failure → if insufficient, escalate to Reflex 1.
Prior art: Shewhart SPC; SRE error-budget burn-rate alerts; Thom catastrophe theory; immunology adaptive surveillance.

### Reflex 3 — RECOVER (degraded can't sustain)
Reflex 1 fallbacks log "fallback active" AND Reflex 2 says "fallback's own gradient is bad" — redundancy itself failing → **recovery mode**: known-safe state, reduced surface, observation-only, HITL-accepting. **Loud, not silent.** Cockpit shows it; Vellum logs it; Reach channels notify; cells get the signal and pull back.
Prior art: aviation "land the plane"; submarine silent-running; SIL in industrial control; CDN graceful degradation; Erlang multi-level supervision.

### Sense types (same Vellum schema, different category)
- `level_sense` — Reflex 1 trigger.
- `gradient_sense` — Reflex 2 trigger (rate-of-change).
- `pattern_sense` — Reflex 2 trigger (correlation with known precursor).

### Criticality classification (FMECA)
- **CRITICAL** — full R1+R2+R3.
- **IMPORTANT** — R1+R2.
- **STANDARD** — R1 only.
- **BEST-EFFORT** — no reflex.

Each Pass 3 output declares criticality with FMECA justification.

---

## The 31 components — for-now best current understanding

**Tagged for-now:** this list is the best understanding as of 2026-06-24. New components may emerge during Pass 1/2; some may merge or split. The 31 are not closed. Numbering is non-sequential because #29, #30, #31 (new in v03) are inserted into their natural layers, not appended.

### L7 — User door
1. Intent Interface (Cockpit) · Electron · only user door · canonical branch `cursor/20260623120000/vellum-ui-lens`
2. `markPass.ts` certainty + ambiguity (1-9 + ▲)
30. **UI integration** — Cockpit ↔ Vellum ↔ deterministic core ↔ Night Scout ↔ overview ↔ cells. Boundary: includes wiring, telemetry-to-Cockpit flow, mandatory `markPass.ts` path on every user input, "no spend dashboards in the human surface" rule. **Criticality: CRITICAL** (single-point-of-failure for HITL surface; if it goes silent, the operator can't see the system). FMECA justification: this is the only in-band human-to-system channel.

### L7.5 — REACH
31. **Reach-Ewan-anywhere** — bidirectional out-of-band channel. **Forward (system→Ewan):** Telegram primary (push, encrypted, already wired) → Twilio SMS fallback → Twilio voice for genuine emergencies. **Inverse (Ewan→system):** Telegram bot inbound + Twilio SMS backup. Escalation hierarchy + time-to-escalate specified in Pass 3. **Criticality: CRITICAL**.

### L6.5 — Overview
3. Overview layer mechanics — read-only-what's-on-fire, cross-source decipherment, actionable-insight emission, Vellum-summons protocol. Seat occupied by Perplexity today; **seat itself is sovereign** (vendor-agnostic).

### L6 — Agent work surfaces
4. Sealed cells (Apple Container, 4×) on Mac mini
5. Manufacturer-native config per agent (Claude/Cursor/Devin/Antigravity) — *seeded in v04*
6. VSCodium agent lane — *seeded in v04*
7. Per-cell repo + worktree discipline (Agent Worktree Contract)
8. Asset inventory + canonical clean-build resolution

### L5 — Routing
9. One LiteLLM = `estate-token-router` — credit-first, deterministic
10. `estate-cost-tools` as middleware (caching, compaction, Haiku routing, cost log)
11. Production-Law gate inside the router
12. DeerFlow trial — Beast-only, one-task experiment — *seeded in v04*

### L4 — Runtime gate
13. `amplified_permissions.classify()` — A/B/C ladder
14. Baton — single write lease
15. RodGuard circuit breaker — trips on 5-rod violation or P0
16. Door-open event schema in Vellum

### L3 — Deterministic spine
17. Deterministic core — gatherer + decipherer; LLMs build it, the built core runs without them
18. `harness_event` schema with `approval_tier` + `drift_signal` G/A/R/B
19. `epistemic_status.py` + `epistemic_status_invariant.py` — min-rule, P0-on-laundering, DriftDetector
20. Vellum senses (`sensor_event.py`) — types, what each watches, what `drift_signal` raises

### L2 — Pipe / substrate
21. Relay/Vellum doctrine — write `relay_protocol.md`; 10-component scope; **9-item pre-production gate (see below)**; outcome-language convention
22. The Pipe contract — Python + Rust + Vellum + AI + Human; no side doors
29. **Vellum hardening** — replication, append-only schema enforcement, hash-chain verification on read, signed events with key rotation, JWT auto-rotation cron, offline-queue per Mac, restore-drill runbook, self-telemetry. **Entry state: broken** (JWTs expired, Infisical dark, `shared_dev_jwt` missing `sheet_id`). Pass 3 must reflect entry-state in `Build sequence`. **Criticality candidate: CRITICAL** — confirmation via FMECA in Pass 3, not pre-assigned.

### L1 — Persistence
23. Path 1 verbatim lake — attributed, immutable, bronze→DuckDB gold
24. Path 2 neutralised pool — Presidio/spaCy + HMAC-SHA256, identity-blind, diffable vs lake, PUDDING-ready

### L0 — Infrastructure
25. Estate topology + Tailscale — M5/Mac mini/M4/Beast; redundancy contract per node

### Cross-cutting
26. **Homeostatic spine** — Ashby/Toyota/SRE/immunology lineage applied to the whole
27. **GitHub hardening** — branch protection, CODEOWNERS, no agent self-approval, signed commits — *seeded in v04*
28. **Token-efficiency PROOF-OF-LIFE gate** — §9 acceptance run

---

## The 9-item Relay pre-production gate (from Relay protocol brief)

A task enters production only when it has all nine:

1. **goal link** — what business outcome does it serve?
2. **owner** — named, single accountable party.
3. **input refs** — every input cited with source + tier.
4. **acceptance test** — pass/fail criteria specified before work starts.
5. **allowed tools/models** — explicit set; nothing else may be used.
6. **data sensitivity class** — public / internal / sensitive / restricted.
7. **route destination** — where output lands (file, Vellum, Brain, GitHub, inbox).
8. **stop condition** — when to wrap, even if "not done".
9. **baton requirement** — does this need the write lease? If yes, hold it; if no, declare it doesn't.

Every Pass 3 output must include a `production_gate_check` field showing each of the 9 items is satisfied for the component being endpointed.

---

## The three passes (per component)

### Pass 1 — PRIOR ART (full breadth, tiered loop, wide-narrow pattern)

For each component, sub-agent finds:
- **Where was this pattern first solved?** Field, with **named founding discipline**.
- **By whom?** Named originator(s).
- **When?** Year, primary publication.
- **With what result?** What worked at what scale.
- **What did they get wrong?** Failure modes the prior art warned about.
- **Tier each finding** at source.

Apply wide-narrow. Endpoint condition: **multi-domain convergence (≥3 distinct founding disciplines, per the v04 definition above)**. Single-source claims cap at INTUITED. Non-pejorative throughout.

**Mandatory canon for homeostatic spine sub-agent (#26):**
Ashby (1952/1956); Wiener (1948); Cannon (1932); Maturana & Varela (1980); Beer (1972); Shewhart (1924) + Deming PDSA; Toyota (Ohno 1988) — jidoka/andon/5 whys/poka-yoke; FRACAS/FMEA/FMECA (mil-spec); Hollnagel & Woods (2006); Reason (1990) Swiss cheese; Perrow (1984) *Normal Accidents*; Goldratt — Theory of Constraints; Taguchi — robust design; Google SRE (Beyer 2016); Nygard *Release It!*; Janeway *Immunobiology*; Forrester (1961); Thom — catastrophe theory.

### Per-layer seeds (v04 — strengthened against single-discipline collapse)

**L7 / certainty marking:** Tetlock (forecasting/Brier scores), Bayesian elicitation, aviation CRM, surgical timeout protocols, **3-2-1 risk register conventions (project management)**, **medical informed-consent capacity assessment**.

**L7.5 / REACH:**
- Forward channel: PagerDuty, Opsgenie, hospital paging, military alert hierarchies, ham radio nets, SS-15 two-key protocols, **maritime distress signalling (SOLAS)**.
- Inverse channel (Ewan→system from phone): **IPMI/BMC lights-out management**, **SCADA dial-in modem fallback**, **naval HF radio ACK protocols**, **APRS amateur-radio messaging**.

**L6.5 / overview:** NASA Mission Control, ATC, hospital command centres, Boyd OODA, SRE on-call, NOCs, **fire incident command system (ICS-100)**.

**L6 / sealed cells:**
- **Common ancestor (named explicitly):** Lampson, *A Note on the Confinement Problem* (1973). KeyKOS, seL4, gVisor, Qubes are all descendants. Count as ONE founding discipline.
- Distinct disciplines to add: **BSL containment levels (CDC biosafety, 1974)**, **physical sally ports (corrections/military)**, **DTCC financial clearing isolation**, **maritime watertight compartments (Titanic-era engineering)**.

**L5 / routing:** Hungarian algorithm, Kelly criterion, real-time bidding, Borg, Kubernetes scheduler, market microstructure, **traffic engineering (highway capacity manual)**.

**L4 / Baton + RodGuard + permissions:**
- Distributed locking (Lamport/Raft/Paxos count as ONE founding discipline — distributed consensus).
- **Distinct disciplines to add:** **financial circuit breakers (NYSE Rule 80B)**, **electrical-grid protection relays (IEC 61850)**, **chemical-plant emergency shutdown (IEC 61511)**, **aviation TCAS / GPWS**, **railway tokenless block working**, **nuclear reactor SCRAM systems**.

**L3 / deterministic spine:**
- Statistical/control engineering (Shewhart, CUSUM, PID, Kalman, anomaly detection count as ONE founding discipline).
- **Distinct disciplines to add:** **epidemiology outbreak surveillance (CDC Farrington algorithm)**, **ecology critical-slowing-down (Scheffer 2009, *Nature*)**, **financial fraud detection (Visa/Mastercard real-time scoring)**, **seismology early-warning (ShakeAlert)**.

**L2 / immutable ledger / Vellum hardening:**
- Event sourcing (Fowler), CRDTs, Merkle trees, Datomic, Kafka, LMAX Disruptor, double-entry accounting (1494), Postgres streaming replication, append-only ledgers in audit/compliance, blockchain primitives (math not politics).
- For Vellum hardening (#29) specifically: **NIST FIPS 140-2 (HSM standard)**, **TPM 2.0 (hardware-rooted key storage)**, **PKIX RFC 5280 (X.509 certificate rotation)**, **COMSEC/EKMS (military key management)**, **WORM storage (SEC Rule 17a-4 compliance archives)**.

**L1 / lake + pool:** Kimball/Inmon warehousing, differential privacy, k-anonymity, l-diversity, federated learning, GDPR pseudonymisation, **OECD privacy framework (1980)**, **HIPAA Safe Harbor de-identification**.

**L0 / topology + redundancy:** CAP/PACELC, ARPANET resilience, CDNs, mesh networking, ham radio failover, **telephone network redundancy (Bell Labs reliability engineering, 5-nines)**, **electrical-grid N-1 contingency planning**.

### Newly-seeded components (v04)

**#5 — Manufacturer-native agent config:** **ISO/IEC 27001 control attestation patterns**, **Linux distribution package manifest conventions (Debian Policy, RPM)**, **Nix declarative config**, **Ansible playbook conventions**.

**#6 — VSCodium agent lane:** **Open-source fork patterns (LibreOffice from OpenOffice; Chromium-Ungoogled)**, **telemetry-removal toolchains (Audacity/AdBlock case studies)**, **build reproducibility (Debian Reproducible Builds project)**.

**#12 — DeerFlow trial:** **Skunkworks methodology (Lockheed, Kelly Johnson)**, **A/B testing in clinical trials (CONSORT statement)**, **canary deployments (Google, Netflix)**, **stage-gate product development (Cooper 1986)**.

**#27 — GitHub hardening:** **SLSA framework (Supply-chain Levels for Software Artifacts)**, **NIST SSDF (Secure Software Development Framework, SP 800-218)**, **SBOM standards (SPDX, CycloneDX)**, **code-signing (Sigstore, Cosign)**, **two-person review (FDA 21 CFR Part 11; Boeing safety-of-flight reviews)**.

### Pass 2 — TRANSLATION

After Pass 1:
- **Map prior-art mechanism onto component.** Their X = our Y.
- **Name equivalences explicitly.** No hand-waving.
- **Name differences honestly.** Where does the analogy break?
- **Cite primary sources, don't paraphrase.**
- **Run the adoption test** if component proposes adopting anything new.
- **Win-win check** (NEW in v04): does this component's design create any take that costs a counterparty? If yes, flag for review; cannot proceed on proxy.
- **KILL / PARK / PROCEED decision.**

### Pass 3 — ENDPOINT (only if component survives Pass 2) — 13-field shape

```
Logic                       why it works (grounded in multi-domain prior art)
Methodology                 how to build/run it
Python/Rust boundary        explicit split + which languages earned the adoption test if not Python/Rust
Senses
  ├─ failure senses         level_sense — Reflex 1
  └─ friction senses        gradient_sense + pattern_sense — Reflex 2
Failure modes               FMEA: mode, cause, effect, detection, severity
Friction patterns           gradients/patterns predicting each failure mode, with thresholds + pre-emptive mitigations
Redundancy                  Reflex 1 fallback path; degraded-mode behaviour (loud-not-silent)
Self-heal                   deterministic recovery within Reflex 1 (3-layer: retry/restart/RUNBOOK)
Degraded mode               visible, loud, honest
Recovery mode               Reflex 3 — entry/exit; what surfaces to Cockpit + Vellum + Reach
Criticality classification  CRITICAL / IMPORTANT / STANDARD / BEST-EFFORT (FMECA justification mandatory)
Surface conditions          the only path to Ewan; what context; which Reach channel(s) at what severity
Deterministic patches       { where, what, why, acceptance_test } — closes a class of thrash permanently
Acceptance test             happy + each failure mode + each friction pattern + degraded + recovery all PASS
Build sequence              deps on other components; external deps; Phase 0 + 0.5 unblocks satisfied
production_gate_check       9-item Relay gate, each satisfied with evidence
rod_check                   which rod tested; protected_or_violated; evidence
goal_link                   one-line statement of how this serves the goal
```

13 fields + 3 mandatory tags (production_gate_check, rod_check, goal_link). Anything missing = not at endpoint.

---

## Night Scout registration (continuity, not re-research)

Every component completing Pass 3 emits a registration to Vellum (routed **through the Pipe**, not directly — patches the v03 side-door):

```json
{
  "event_type": "night_scout_registration",
  "component": "<component_name>",
  "knowledge_areas": ["<area_1>", "<area_2>", "<area_3>"],
  "endpoint_version": "v01",
  "endpoint_hash": "<sha256_of_endpoint_doc>",
  "watch_priorities": [
    "new_failure_modes",
    "new_patches",
    "new_primary_sources",
    "contradictions_to_endpoint_claims"
  ],
  "delta_handler": "overview_layer",
  "delta_handler_current_occupant": "perplexity",
  "registered_by": "AI_PARTNER_PROXY",
  "registered_via_pipe": true,
  "registered_at": "<iso8601>"
}
```

**`delta_handler` is vendor-agnostic.** Current occupant logged separately. Seat survives vendor change.

**Night Scout watches knowledge areas nightly.** Deltas surface to the overview layer. Overview decides:
- **NO CHANGE** — logged, attached to history.
- **REFINEMENT** — component re-enters pipe with tight scope; endpoint version increments.
- **DEMOTION** — contradicts endpoint. Tier auto-demotes per min-rule; component re-enters for re-research.

**If Night Scout is not live at run time (Phase 0.5.2):** registrations are queued in `night-scout-registrations/<component>.json` until Night Scout comes online. The build sequence treats Night Scout as a deliverable, not a precondition.

---

## Thrash artifact format

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

---

## Proxy-log format (the 5 Tier B acts)

Every Tier B proxy act logs to Vellum (through the Pipe) as:

```json
{
  "event_type": "proxy_act",
  "act_class": "draft_into_pipe|schedule_task|file_tracker_item|draft_pr_or_branch|outbound_draft_for_review|connector_write_reversible|spend_under_gate",
  "act_description": "...",
  "what_was_done": "...",
  "where_it_landed": "<path or vellum event id>",
  "reversibility": "reversible|partially_reversible|costly_to_reverse",
  "signed_by": "AI_PARTNER_PROXY",
  "signed_for": "ewan_bramley",
  "ratification_required_by": "<iso8601>",
  "timestamp": "<iso8601>"
}
```

The 5 Tier B act-classes in this run:
1. **Mint fresh JWTs** locally (Phase 0.2) → log at mint, before Ewan places.
2. **Draft into the pipe** (every sub-agent output) → log at draft completion.
3. **Schedule normal-cadence tasks** (Night Scout registrations) → log at registration emit.
4. **File tracker items** (none expected; flagged if used) → log on file.
5. **Draft outbound** (none expected; flagged if used) → log on draft.

`proxy=N logged` in CLOSURE footer is a count; the records themselves live in Vellum and are queryable.

---

## [CLOSURE] footer requirement (every output)

Per `end-to-end-closure` skill:

- Every Claude top-level turn carries a CLOSURE footer.
- **Every sub-agent pass output (Pass 1, Pass 2, Pass 3) carries its own CLOSURE footer.**
- INDEX.md carries the run-level CLOSURE footer.
- Format: `[CLOSURE] branch=ACTION|PLAN|AUDIT | proxy=none|<n logged> | gates=none|<one-line gate> | inbox=none|<artifact filename> | tier=<min tier of turn>`

Acceptance test verifies all three levels (top-level + per-pass + INDEX.md) carry footers.

---

## Output destination

`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/beast-pipe-outputs__2026-06-24/`:

- `prior-art/<component>.md` — Pass 1
- `translation/<component>.md` — Pass 2 (KILL / PARK / PROCEED)
- `endpoints/<component>.md` — Pass 3 (13-field + 3-tag shape)
- `patches/deterministic-patches.jsonl` — every patch, one JSON per line
- `thrash/<component>__<pass>.md` — thrash artifacts surfaced
- `parked/<component>.md` — components recommended for PARK (with re-evaluation trigger)
- `night-scout-registrations/<component>.json` — one per completed Pass 3
- `proxy-log/<iso-timestamp>__<act_class>.json` — every Tier B act logged
- `INDEX.md` — what ran, what completed, what surfaced, what killed, what parked; final CLOSURE footer

---

## Constraints (non-negotiable)

- **Pipe discipline.** Drafts in workspace; commits to Beast/Vellum through the Pipe. No side doors. (v04 patches Night Scout to route through Pipe.)
- **Min-rule.** Every claim carries tier + provenance. Effective tier = MIN of inputs. Silent promotion = P0 halt.
- **Tier declarations inline.** Each substantive claim in Pass 1/2/3 outputs tier-tagged at claim level, not document level only.
- **Radical attribution.** Every claim has source URL + date + reliability tier. Primary > secondary > tertiary.
- **GOAL-LOCK.** Off-goal sub-agent = stop and surface. Mechanistic check at pass start (above).
- **5-rod check.** Every pass declares which rod tested + protected_or_violated + evidence.
- **CLOSURE footer** on every sub-agent output + every Claude top-level turn + INDEX.md.
- **Sandbox sovereignty.** No Beast writes outside the Pipe. No Mac trust-root writes from Beast-side code.
- **No LLM in the router.** L5 routing is deterministic; LLM only inside cells.
- **Loud failure beats silent failure.** Every component honest about degraded state.
- **Tiered loop is the only loop.** Brain-first, two local attempts, sharpen, one ask, write-up.
- **Wide-narrow pattern.** Multi-domain convergence (≥3 distinct founding disciplines) as endpoint condition. Single-source claims cap at INTUITED.
- **Non-pejorative language.** `neutral-research-brief` at every sub-agent start; audit at every close.
- **Outcome-language convention** for failure descriptions (behavioural, not moralised).
- **Adoption test** before adopting anything new. PARK with trigger; nothing binned.
- **Minimize AI scope.** Python+Rust holds deterministic logic; AI handles bounded well-prepared problems. Tests test the rules, not the AI.
- **For-now everywhere.** Components, tiers, decisions, are provisional unless explicitly promoted via documented gate. The 31-component list is for-now.

---

## Acceptance test (the whole run)

The research-pipe run is **complete** when:

1. All 31 components have an endpoint OR a KILL OR a PARK OR a thrash artifact (no silent skips).
2. `deterministic-patches.jsonl` has ≥1 patch per layer (the floor grew).
3. `INDEX.md` enumerates everything — no missing components.
4. Every endpoint has all 13 fields + 3 mandatory tags (production_gate_check, rod_check, goal_link).
5. Every Pass 1 cites ≥3 primary sources from outside AI with **multi-domain convergence (≥3 distinct founding disciplines, per the v04 definition; named founding discipline for each source)** on every claim above INTUITED.
6. Every Pass 2 names ≥1 equivalence + ≥1 difference, runs adoption test where new tools proposed, runs win-win check, recommends PROCEED / KILL / PARK.
7. Every Pass 3 has all 3 reflexes specified at its criticality level + FMECA justification.
8. Every Pass 3 emits a Night Scout registration through the Pipe.
9. Every sub-agent output passes the non-pejorative audit.
10. Every Tier B proxy act has a logged record in `proxy-log/`.
11. Every pass output + INDEX.md carries a CLOSURE footer.
12. Thrash count logged.
13. Final CLOSURE footer on INDEX.md.

**No proof of completion = not done.** §9 PROOF-OF-LIFE pattern applied to research.

---

## What Perplexity does next (Job B)

After Claude Code returns outputs to `beast-pipe-outputs__2026-06-24/`, Perplexity:

1. Reads every endpoint's `Build sequence` field.
2. Constructs the dependency graph across all 31 components.
3. Topologically sorts → master build sequence.
4. Cross-checks against §9 PROOF-OF-LIFE gate, redundancy contract, three-reflex coverage per criticality class.
5. Confirms all 31 Night Scout registrations landed (or queued).
6. Drops `MASTER-BUILD-SEQUENCE__v01__2026-06-24__perplexity.md` to inbox root.
7. Night Scout starts on registrations the night after master sequence lands — system self-watching.
8. Next AI codes from the master sequence.

---

## Constitution / grants compliance

- **Tier classifications** (per `amplified-standing-grants`):
  - Live probes via Tailscale = Tier A research.
  - Drafting JWTs in workspace = Tier B (proxy-sign, logged per format above).
  - Placing JWTs into `~/.amplified/stoa_claude_jwts.json` = Tier B (reversible).
  - Pipe runs on Beast (read + Vellum-event drafts) = Tier A/B mix.
  - Direct Beast writes outside the pipe = Tier C, FORBIDDEN.
- CLOSURE footer on every sub-agent + Claude top-level turn + INDEX.md.
- Drafted by AI as proxy, logged.
- No side door (v04 patches Night Scout path).

---

## Hand-back to Ewan (collapsed)

**Single gate cluster** — collapsed from 13 in INBOX-INDEX to 1 hand-back with structured contents:

| Block | Items |
|---|---|
| A. Live-infrastructure unblockers (Phase 0) | Vellum JWT TTL + Infisical decision; Beast `estate-machine` stack intent; PostgreSQL connector; OPEC=OpenTelemetry confirmation |
| B. Sizing facts (Phase 0.5) | Mac mini RAM number; Night Scout live-status confirmation |
| C. Single ratifications (post-Pass 3) | Name lock (Beast in code; Infrastructure 1 external); §9 PROOF-OF-LIFE as token-eff "done" definition; harness name disambiguation; Lens selector status; DeerFlow Q1 |
| D. Read-only / manual ops | 3 manual skill deletions in Perplexity settings; `mdutil -E /` Spotlight reindex; provide AI-native search methodology file |
| E. After-pipe ratifications | Fresh JWT placements; L1/L2 redundancy plan; L7.5 Reach hierarchy |

Everything else self-resolves within the pipe per tiered-loop + thrash rules.

[CLOSURE] branch=PLAN | proxy=1 logged (research-pipe brief v04 drafted as AI_PARTNER_PROXY) | gates=collapsed single hand-back cluster A-E above (after pipe returns Pass 3) | inbox=RESEARCH-PIPE-RUN__claude-code-brief__v04__2026-06-24__perplexity.md | tier=STRUCTURED
