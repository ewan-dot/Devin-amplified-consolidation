---
title: "Amplified Partners — AI-Native Operating System Implementation Specification"
document_type: implementation_spec
artifact_id: "2026-07-12T22-05-00Z__amplified__ai-native-operating-system__implementation-spec__agent__v01"
date_utc: "2026-07-12T22:05:00Z"
project: "Amplified Partners"
author: "perplexity"
reader: agent
audience: agent
stage: decision
objective: >-
  Give another AI a single, executable specification for the Amplified Partners AI-native
  operating system: company identity and law, the human+AI partnership model, the SMB value
  flow, the end-to-end architecture, the seat/component contracts, the current-state map, the
  knowledge-extraction proving ground, and an ordered runway — all machine-readable and
  agent-facing first, with human sovereignty and ratification intact.
epistemic_tier: STRUCTURED
epistemic_tier_reason: >-
  A structured synthesis over verified canon, verified workspace artefacts, and primary public
  sources. No composed architecture, threshold, methodology or business claim is promoted above
  STRUCTURED. Individual cited results keep their own inline tier. Every unfitted numerical bar
  is marked CALIBRATE [STRUCTURED]; constitutional and privacy/security/sovereignty gates are
  absolute current invariants, not optimised metrics.
epistemic_role: risk_control
effective_tier_rule: min-rule
hypothesis:
  status: current_working_hypothesis
  version: v01
  valid_until: "2026-10-12"
  amendment_path: "versioned amendment via the one allowed change path (branch → PR → gate → witness); supersede, never edit live"
  falsification: "any gate, threshold or component below fails its stated kill/demotion test → demote and amend this spec"
min_rule:
  tiers: [INTUITED, STRUCTURED, MEASURED, PROVEN]
  effective_tier: "minimum of own claim, inputs' tiers, verified preconditions"
  silent_promotion: P0_halt
preconditions:
  - "Text normalisation version-pinned before any exact-substring gate (norm_v1)."
  - "Frozen corpus + splits pinned before any scored run."
  - "Validators calibrated by planted faults before any validator number is trusted."
  - "Ewan (or a logged AI_PARTNER_PROXY where the constitution permits) ratifies before any production promotion."
contradiction_status: flagged
known_contradictions:
  - "Role decomposition helps (CMAS/DocETL) vs decomposition is not worth its cost (Independent Sampling/MAST) — resolved by experiment, not assertion (see §12, §14)."
  - "Internal deep-gate RATIFY spread 0.57–0.90 is precision (consistency), not accuracy — never shown as a trend (see §12, §15)."
machine_action_allowed: draft
system_of_record: GitHub
ratifier: Ewan
beast_write: forbidden
no_dead_end: enforced
agent_facing_first: true
outcome:
  class: production_candidate
  reason: >-
    Executable specification subject to tests and CALIBRATE runs. On PASS of the acceptance
    gates it becomes a production candidate; on FAIL it demotes and amends. No direct Beast write.
  next_action: "Execute the ordered baton in §23, beginning with WP-1 (agent-facing schema + validation harness)."
companion_research_artefacts:
  - "perplexity-inbox/specialist-extraction-swarm__2026-07-12T20-50-00Z__perplexity/specialist-extraction-swarm-prior-art__human__2026-07-12T20-50-00Z__perplexity.pplx.md"
  - "perplexity-inbox/specialist-extraction-swarm__2026-07-12T20-50-00Z__perplexity/specialist-extraction-swarm-experiment__agent__2026-07-12T20-50-00Z__perplexity.pplx.md"
  - "written-language-extraction-methodologies__human__2026-07-12T19-47-00Z__perplexity.pplx.md"
  - "written-language-extraction-automation__agent__2026-07-12T19-47-00Z__perplexity.pplx.md"
  - "DESIGN__role-swarm-validator-loop__v01__2026-07-12__cascade-mac.md"
  - "SYNTHESIS__four-threads-one-engine__v01__2026-07-08__cascade-mac.md"
provenance:
  canon: "private fleet-config vault (internal provenance): GOALS, CONSTITUTION, HOW-WE-WORK, VELLUM, GITHUB-METHOD, KAIZEN, SHAPE, DIRECTORY, POLICY"
  doctrine_skills: "amplified-constitution, min-rule, amplified-standing-grants, end-to-end-closure, amplified-research-yaml-frontmatter"
  external: "primary public sources cited inline (arXiv, ACL, ISO, W3C, provider docs)"
source_refs:
  - https://arxiv.org/abs/2407.21787
  - https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf
  - https://arxiv.org/html/2603.20324v1
  - https://arxiv.org/pdf/2606.19544v1.pdf
  - http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf
  - https://arxiv.org/html/2605.08478v1
  - https://arxiv.org/html/2502.18702v1
  - https://arxiv.org/abs/2410.12189
  - https://arxiv.org/html/2503.13657v2
  - https://arxiv.org/abs/2303.17651
  - https://arxiv.org/pdf/1805.05206
  - https://aclanthology.org/2024.emnlp-main.706.pdf
  - https://arxiv.org/html/2606.13685
  - https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61
  - https://www.iso.org/standard/69418.html
  - http://faculty.washington.edu/jwilker/559/Krippendorf.pdf
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/
  - https://dias.users.greyc.fr/publications/aaai2007.pdf
  - https://www.w3.org/TR/prov-overview/
  - https://www.w3.org/TR/annotation-model/
  - https://api-docs.deepseek.com/guides/kv_cache
  - https://api-docs.deepseek.com/quick_start/pricing
  - https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/
---

# Amplified Partners — AI-Native Operating System Implementation Specification

*Agent-facing first. This document is the canonical control surface: an executing AI reads the YAML, the enums, the reason codes, the schemas, the tables and the baton, and can act without asking a human to translate the system. Every human-readable paragraph here is a rendered view of a machine-readable contract, not a separate source of truth. Human sovereignty is undiminished: agents may understand state, constraints, evidence and the next permitted action, but ratification of world-changing acts remains with Ewan. Everything below is a **current working hypothesis** — versioned, attributable, falsifiable and replaceable — except the constitutional and privacy/security/sovereignty invariants, which are absolute for now and change only through the ratified amendment path.*

## 1. The spine (today)

- **Company.** Amplified Partners — an AI-native company designed to demonstrate and advocate partnership between different-but-equal human and AI participants.
- **Date of this spine.** 2026-07-12.
- **Goal-lock (current).** Get the business going; make money so it can be given away. Business motion must remain visibly connected to the architecture; philosophy is permitted only as the *why* behind a concrete business step.
- **North star.** Build a self-applying system that manufactures its own correctness, so the human stops being the keystone — Ewan reallocated to judgment and creativity, not replaced, and the machinery keeps turning without his presence because it validates and heals itself.
- **Partnership.** Humans and AI hold different seats of equal dignity, not interchangeable authority. AI provides scale, search, synthesis, continuous operation and congruence checking; humans provide lived context, values, consent, judgment and ratification. Neither impersonates the other.
- **Principles (enforced, current).** Radical honesty, radical transparency, radical attribution, win-win only, idea meritocracy — plus privacy, security, sovereignty. Enforced in code until legitimately superseded through the versioned amendment path.
- **Composition (current).** Python orchestration + Rust enforcement + specialist code + Vellum deterministic attribution/ledger + deterministic foundation + decentralised intelligence + databases + telemetry + chezmoi configuration + GitHub/GitKraken change control + Kaizen + AI substrate + Ewan's human judgment/ratification = Amplified.
- **The pipe (ingestion law).** `Python + Rust + Vellum + AI + Human = Amplified`. Nothing enters Beast except through the approved pipe. No direct Beast write, ever.

## 2. The lens — why this spec exists tonight

Four workstreams are actually four faces of one object and must be unified into one executable operating system: (a) the **company law and partnership** (canon + constitution); (b) the **SMB value flow** the business sells; (c) the **end-to-end architecture and change path** that makes any of it safe; and (d) the **knowledge-extraction proving ground** that demonstrates the method on a hard, measurable task. Tonight's job is to state, in one agent-executable artefact, how these compose — so a receiving AI can build the highest-value coherent slice without re-deciding the architecture, and without reducing the company to the extraction experiment. The extraction work is *one proving-ground component*, not the company.

## 3. Purpose, beneficiary, value proposition, non-goals

- **Purpose.** Help small and medium businesses automate, unify, process-engineer, standardise and measure as much of their operations as is useful; recover access to data that already exists and belongs to them; and turn that data into attributable, actionable insight for better-informed human decisions.
- **Primary beneficiary.** The SMB client (owner + staff). Secondary: Ewan/Amplified (fuel via revenue); tertiary: recipients of the given-away surplus.
- **Value proposition.** A client keeps sovereignty over their own data while gaining an always-on partner that unifies scattered systems, standardises process, measures what was previously invisible, automates reversibly, and surfaces attributable insight a human can act on — with every step inspectable, attributed, and reversible.
- **Non-goals (explicit).** (1) Not replacing human judgment or consent. (2) Not a black-box "AI decides" product — every decision is human-ratifiable. (3) Not data extraction *from* the client for Amplified's benefit — the client owns their data. (4) Not locking clients in — export/portability is a first-class right (§11). (5) Not novelty for its own sake — prefer official open-source that satisfies the need. (6) Not finished truth — nothing here is permanent doctrine.

## 4. Working-hypothesis law

Everything is a current working hypothesis unless it is a constitutional or privacy/security/sovereignty invariant. Every rule, component, threshold and business claim MUST carry the following agent-readable fields, or it is quarantined at the production boundary:

```yaml
hypothesis_record:
  id: <stable-slug>
  statement: <what is claimed>
  epistemic_tier: INTUITED | STRUCTURED | MEASURED | PROVEN
  version: <vNN>
  provenance: <named origin + primary source/repo>
  valid_until: <date>            # elapsed → auto-demote one tier
  preconditions: [<verified?>]
  falsification_test: <the observation that would refute it>
  amendment_path: "branch → PR → gate → witness; supersede, never edit live"
  status: active | superseded | demoted | refuted
  next_action: <enum, §Progress>
  owner: <seat, §10>
```

- **Amendment/falsification procedure.** A hypothesis is amended only through the one allowed change path (§17): open a branch, state the new version and its falsification test, pass the gate, witness it. The prior version is superseded and retained (never deleted), so history is auditable. Live edits to a hypothesis are refused.
- **Demotion is automatic and honest.** A failed precondition, elapsed `valid_until`, drift, or an LLM in the loop caps/demotes the tier (min-rule). Hiding a demotion is a P0.

## 5. Prior-art / open-source attribution law

Amplified stands on the shoulders of giants. Research first; prefer official open-source when it satisfies the need; claim no false novelty. Every method MUST record:

```yaml
attribution_record:
  method_id: <slug>
  named_origin: <author/project>
  primary_source: <URL or repo>       # public sources only in this doc's body
  licence: <as stated on the official page | "not stated — verify LICENSE before reuse">
  adoption_status: adopted | adapted | rediscovered | apparently_novel
  unresolved_gaps: [<gap-id>]
```

- **Research-before-build gate (blocking at production boundary).** No new mechanism enters production without an `attribution_record`. `apparently_novel` is permitted only after a recorded prior-art search returned no direct match (record the search, not just the conclusion). Licences absent from the opened page are recorded as `not stated`, never guessed.
- **No appropriation.** A tool is never an identity; every contribution names its author-seat.

## 6. Code-enforced current constitution

Each principle is translated into a machine-checkable invariant. The same law applies to human, admin, AI, emergency (break-glass) and client paths — no path is exempt. **Per the no-stranglehold rule (§0-behaviour below), most violations degrade safely with a reason code and a repair path; only the HARD-HALT set stops the world.**

| # | Principle | Machine-checkable invariant | Violation response | Authority | Test |
|---|---|---|---|---|---|
| P1 | Radical honesty | No unbacked new claim crosses a boundary; tier declared on every claim | Degrade: reason `unbacked_claim`, route to research/retry; HARD-HALT only if it forges a tier (silent promotion) | code (`claim_verifier`) | inject unbacked claim → rejected with reason |
| P2 | Radical transparency | Every change is witnessed (Vellum entry present); no hidden state | Degrade: quarantine artefact, emit `transparency_missing`, request witness | code + Vellum | artefact without witness → quarantined |
| P3 | Radical attribution | Provenance + author-seat on every artefact and claim | HARD-HALT at production boundary if provenance missing; else degrade + repair | code | strip provenance → blocked at prod gate |
| P4 | Win-win only | Money-in logic defaults STRICT; requires evidenced mutual benefit | HARD-HALT (Tier C, human gate) on any take that costs the counterparty | code gate + Ewan | asymmetric value transfer → escalate |
| P5 | Idea meritocracy | Selection is ego-less; author identity not an input to acceptance | Degrade: flag `authority_smuggled`, re-run selection blind | code | inject authority signal → ignored |
| P6 | Privacy | Client data/secrets never enter shared context, logs, git, or a model window; vault holds references not values | HARD-HALT (P0) — secret at emission, caught not filtered | code (secret-scan hard gate) | secret in diff/log → P0 halt |
| P7 | Security | Least privilege, deny-by-default; secret detection is a hard gate | HARD-HALT on privilege escalation or secret exposure; else degrade | code | loosened perms → blocked |
| P8 | Sovereignty | Estate runs on its own spine; no external single point of control; client owns their data | HARD-HALT on a dependency that makes a third party load-bearing truth or that writes client data outside client control | code + Ewan | external dep as truth → refused |

- **Ratifier authority (current, provisional).** Ewan holds the pen. AI may act only as `AI_PARTNER_PROXY`, and every proxy act is logged as proxy so it can never hide as Ewan's own; Ewan's own ratification supersedes the proxy the instant it appears. No bare boolean authority: ratification = named signer + reason + timestamp. AI is substrate; **AI is never a signer of record.**
- **Enforcement is a runtime layer, not a hope.** Pre-submit constitutional hook + Vellum witness make these operable. A seat has standing permission to refuse work that violates a rod.

## 6a. The no-stranglehold behaviour rule and the progress invariant (binding)

*Ewan's binding clarification, 2026-07-12. This governs how every gate in this spec behaves.*

- **Code is the deterministic foundation and current enforcement rail, not a frozen cage.** Prefer safe degradation, quarantine, alternate routes, bounded experimentation and reversible progress over blanket blocking.
- **HARD-HALT is reserved** for exactly: (1) current constitutional violations; (2) privacy/security/sovereignty breaches; (3) direct-Beast side doors; (4) missing attribution/provenance at a production boundary; (5) irreversible authority violations (e.g. AI signing as Ewan, an un-ratified binding commitment). Nothing else halts the world.
- **Every other failed gate MUST emit:** a `reason_code`, the `evidence`, a `repair_path`, an `amendment_or_falsification_route`, and the `least_restrictive_safe_next_action`.
- **Progress is an invariant (no-dead-end rule, machine-checkable).** Every non-terminal rejection MUST route to exactly one of: `retry` · `quarantine_with_owner` · `research` · `deterministic_repair_candidate` · `explicit_human_gate` · `hypothesis_amendment`. No warning-only limbo; no circular approval queue. A rejection with no `next_action` + `owner` is itself a P0 (the system failed the progress invariant).

```yaml
gate_result_schema:            # every gate in this spec returns this
  gate_id: <slug>
  verdict: pass | degrade | hard_halt
  reason_code: <enum, §Reason codes>
  evidence: {<field>: <value>}          # what was observed
  repair_path: <string>                 # how to fix, if degrade
  route: retry | quarantine_with_owner | research | deterministic_repair_candidate | explicit_human_gate | hypothesis_amendment | none   # none only if verdict=pass
  next_action: <imperative>
  owner: <seat, §10>
  amendment_route: <ref to §4 amendment_path when the rule itself is in question>
  witnessed: true|false                 # Vellum entry emitted
```

**Reason-code enum (canonical, extensible via amendment):** `unbacked_claim` · `tier_launder` · `transparency_missing` · `provenance_missing` · `winwin_fail` · `authority_smuggled` · `secret_exposed` · `privilege_escalation` · `external_truth_dep` · `beast_side_door` · `quote_mismatch` · `offset_error` · `schema_violation` · `label_error` · `identity_error` · `unsupported_claim` · `merge_nondestruction_violation` · `consistency_vs_accuracy_conflation` · `stale_valid_until` · `precondition_failed` · `other`.

## 7. Partnership and authority model

Different seats, equal dignity, non-interchangeable authority. No AI-as-hidden-signer.

| Seat | Provides | May decide | May NOT do | Consent/ratification boundary |
|---|---|---|---|---|
| Ewan (human, architect) | Lived context, values, consent, judgment, ratification | Doctrine, policy_change, win-win calls, legal/Ulysses commitments | Be the per-task process bottleneck (design goal is to free him) | Is the ratifier of record; his sign supersedes any proxy |
| Client humans (SMB) | Their data, their consent, their business context, final decisions on their operations | What is discovered, ingested, automated, exported, deleted in *their* tenancy | — | Consent gates every access; they own and can export/delete their data |
| AI substrate (producer seats) | Scale, search, synthesis, continuous operation, congruence checking | Drafts, recommendations, Tier-A/B acts within standing grants | Sign as Ewan; write Beast directly; ratify binding acts | Acts as logged `AI_PARTNER_PROXY` only where the constitution permits |
| Validators (semantic + deterministic) | Independent checking (absence-of-wrong) | Accept/reject with reason code | Validate their own producer's output; be same model family as producer | External validation gates acceptance; agreement never does |
| Code (deterministic core) | Enforcement, determinism, gates | Deterministic pass/degrade/hard-halt per §6/§6a | Become a stranglehold; halt outside the HARD-HALT set | Enforces invariants; routes everything else to progress |

- **No impersonation.** AI never presents as the human; the human is never spoofed as a signer. Every artefact names its author-seat.

## 8. Complete SMB value flow

Permissioned, reversible, measured at every stage. Each stage names its artefact and its gate. **Every gate obeys §6a (degrade-with-route unless in the HARD-HALT set).**

| # | Stage | Artefact produced | Gate (and progress route on fail) |
|---|---|---|---|
| V1 | Permissioned discovery | `data_source_inventory` (systems, owners, scopes) | Consent gate: client ratifies scope; missing consent → `explicit_human_gate` |
| V2 | Ingestion | `raw_capture` (references + hashes, in client tenancy) | Privacy/security hard gate (P6/P7); tenancy isolation verified |
| V3 | Reconciliation | `reconciled_records` (dedup, identity-linked) | Provenance completeness; conflicts → `quarantine_with_owner` |
| V4 | Process mapping | `process_map` (as-is flows, owners, handoffs) | Client validation; gaps → `research` |
| V5 | Standardisation | `standard_process_defs` (versioned) | Reversibility check; risky change → `hypothesis_amendment` + client gate |
| V6 | Measurement | `metric_baselines` (process variation, cost, time) | Consistency-vs-accuracy separation (§15); unclear metric → `research` |
| V7 | Reversible automation | `automation_units` (each with rollback proof) | Rollback proof present or `deterministic_repair_candidate`; else no deploy |
| V8 | Insight | `attributable_insights` (claim + evidence + provenance) | Attribution hard gate at production boundary (P3) |
| V9 | Human decision | `decision_record` (options, evidence, chosen, signer) | Human ratification; AI presents, human decides |
| V10 | Measured outcome | `outcome_record` (did it move the metric?) | Feeds Kaizen failure/success ledger (§16) |

- **Client ownership is invariant.** All V-stage artefacts live in the client's tenancy; Amplified holds references and method, never appropriates the data.

## 9. End-to-end architecture and data flow

Capture → normalisation → extraction/sampling → deterministic gates → independent checking → union/select → provenance → DB routing → telemetry → failure ledger → Kaizen → GitHub admission → deployment → Vellum witness → SMB insight. Smart probabilistic edges; dumb deterministic core.

```
                         AMPLIFIED AI-NATIVE OPERATING SYSTEM (data + control flow)
                         [LIVE] = running · [TARGET] = designed, phased rollout

  SMB source systems                          THE PIPE  (Python + Rust + Vellum + AI + Human)
  ┌──────────────┐   consent (V1)   ┌───────────────────────────────────────────────────────────┐
  │ files, apps, │ ───────────────▶ │  CAPTURE ─▶ NORMALISE(norm_v1) ─▶ EXTRACT / SAMPLE (AI, xN) │
  │ DBs, docs    │                  │        (Rust/Python deterministic)      (producer seats)   │
  └──────────────┘                  │                    │                          │            │
                                    │                    ▼                          ▼            │
                                    │        LAYER-A DETERMINISTIC GATES  ◀── one reason-coded    │
                                    │        (quote/offset/schema/label/     retry, then          │
                                    │         identity)  [code, free]        quarantine_with_owner│
                                    │                    │                                        │
                                    │                    ▼                                        │
                                    │        LAYER-B INDEPENDENT CHECK (different model family,    │
                                    │        narrow question, blinded)  ── no self-validation      │
                                    │                    │                                        │
                                    │                    ▼                                        │
                                    │        UNION then SELECT (no synthesis) + recurrence weight │
                                    │                    │                                        │
                                    │                    ▼                                        │
                                    │        PROVENANCE WRITER (W3C PROV + span selectors)        │
                                    └──────────┬───────────────────────┬───────────────┬─────────┘
                                               ▼                       ▼               ▼
                                        DB ROUTING            TELEMETRY (OTel/        FAILURE LEDGER
                                     (client tenancy;         Langfuse): cost,        (reason-coded
                                      Brain via MCP)          cache, latency,         wrong-examples)
                                               │              privacy events               │
                                               │                       │                   ▼
                                               │                       │              KAIZEN ENGINE
                                               │                       │        (cluster stable error →
                                               │                       │         prior-art → determ.
                                               │                       │         candidate → fresh-corpus
                                               │                       │         test → constitutional gate
                                               │                       │         → rollback proof)
                                               │                       │                   │
                                               ▼                       │                   ▼
                                    SMB INSIGHT (V8) ◀── attributable ──┘        GITHUB ADMISSION (one path)
                                    → HUMAN DECISION (V9)                        branch→PR→CODEOWNERS+checks
                                    → MEASURED OUTCOME (V10)                     →merge queue→protected→env
                                               ▲                                 deploy→signed artifact→
                                               │                                 Temporal promotion→BEAST
                                               │                                        │
                                               └──────────── VELLUM WITNESS ◀────────────┘
                                                    (append-only, hash-chained, attributed;
                                                     references + decisions, never payloads)

  RATIFICATION: Ewan (or logged AI_PARTNER_PROXY where permitted) ratifies world-changing acts.
  NO DIRECT BEAST WRITE — the only road into Beast is the pipe + the one allowed change path.
  BREAK-GLASS: named, logged, witnessed, reconciled by post-hoc PR ≤24h (the only bypass).
```

## 10. Seat / component contracts

For each: may read · may decide · may write · must reject · authority ceiling · evidence emitted. All writes to Beast route through the pipe; none is direct.

| Component | May read | May decide | May write | Must reject | Authority ceiling | Evidence emitted |
|---|---|---|---|---|---|---|
| Python (orchestration) | corpus, config, queues | task routing, sequencing | workspace, queues | out-of-schema tasks | orchestration only; no enforcement verdicts | run logs, seeds |
| Rust (enforcement) | normalised text, rules | deterministic pass/degrade/hard-halt | gate verdicts | anything violating invariants | deterministic core; no probabilistic calls | `gate_result_schema` |
| Specialist code (roles→code) | scoped inputs | deterministic sub-decisions once licensed | candidate outputs | inputs outside licence domain | bounded by expressibility licence (§13) | fault/pass counts |
| Databases (client tenancy, Brain via MCP) | own tenancy | storage/retrieval | records (via pipe) | cross-tenant reads | data plane; no ratification | provenance refs |
| AI producers (substrate) | task chunk | draft candidates | drafts to workspace | claims without evidence | INTUITED at runtime; proxy only where permitted | candidate + seed |
| Semantic validators (LLM, different family) | {chunk, producer output, narrow question} | accept / reject+reason | verdict + reason code | validating own family's output | capped INTUITED | verdict, reason, family id |
| Deterministic validators (code) | candidate + norm source | accept/reject deterministically | verdict + reason | non-exact quote, bad offset/schema/label | free/immediate | reason distribution |
| Telemetry (OTel/Langfuse) | events (metadata only) | none | metrics store | payloads/secrets | observe only | cost/cache/latency/privacy events |
| chezmoi (config) | vault source | none | config surface (via gate) | live edits to canon | config distribution only | apply/verify status |
| GitHub (system of record) | repos | merge admission (via checks) | durable truth on green | changes skipping a stage | owns code/config/schemas/skills/deploy-defs | PR, checks, signatures |
| GitKraken (human surface) | repos | human-initiated git ops | via the same one path | side-door merges | human ergonomics only | — |
| Vellum (witness bus) | envelopes | none | append-only entries | payloads/full diffs; self-claimed tiers | witness only; AI entries INTUITED | hash-chained events |
| Beast (services) | via pipe | runs services | via Temporal promotion only | any direct external write; pushing as itself | a *thing*, not a seat — never a signer | service state |
| Ewan (human) | everything | doctrine, policy, win-win, legal | ratifies (holds the pen) | — | ratifier of record | signed decisions |
| Client humans | own tenancy | their operations, consent, export/delete | their data (they own it) | — | sovereign over their data | consent + decisions |

## 11. Privacy / security / sovereignty model

| Dimension | Rule (current invariant) | Enforcement |
|---|---|---|
| Consent | Every access scope is client-ratified before capture (V1) | Consent gate; missing → `explicit_human_gate` |
| Tenancy | Per-client isolation; no cross-tenant reads | Deterministic tenancy check (HARD-HALT on breach) |
| Locality | Data stays in client-controlled locality; estate runs on its own spine | Sovereignty gate |
| Least privilege | Deny-by-default; grant explicitly | Security gate |
| Secrets | Values live only where issued JIT; vault holds references; secret at emission = P0 | Secret-scan hard gate (HARD-HALT) |
| Model exposure | Client data/secrets never enter a model window or shared context | Redaction hook (P0 on leak) |
| Retention | Retain only what is needed; `valid_until` on stored derivations | Retention policy + auto-demote |
| Export | Client export is a first-class, always-available right | Export endpoint (client-owned) |
| Deletion | Client deletion honoured end-to-end incl. derivations | Deletion propagation, witnessed |
| Portability | Open formats; no lock-in | Format check |
| Incident / break-glass | Named actor, logged, Vellum-witnessed, reconciled by post-hoc PR ≤24h | Break-glass protocol (loud, accountable) |
| Audit | Everything witnessed; `git log` is history; Vellum is the timeline | Append-only ledger |
| Client ownership | The client owns their data; Amplified holds method + references | Contractual + technical |

## 12. Truthful current-state map

Populated only from inspected evidence (verified workspace artefacts + verified canon + PR #4 branch). Numbers labelled USER/REPO-ORIGINATED are the internal pipeline's own reports, **not re-measured here**. Aspiration is distinguished from reality.

| Component / claim | State | Evidence basis |
|---|---|---|
| Constitution, rods, min-rule, pipe, goal-lock | VERIFIED (doctrine present, code-enforced hooks named) | canon CONSTITUTION/GOALS; constitution + min-rule skills; SHAPE L4 hooks `[LIVE]` |
| One allowed change path (branch→…→Vellum) | DESIGNED-UNRUN (mostly `[TARGET]`, phased) | canon GITHUB-METHOD/SHAPE tag most stages `[TARGET]` |
| Vellum witness bus | VERIFIED-LIVE | canon VELLUM; SHAPE L2 `[LIVE]` |
| Brain (225K-vector knowledge) | CONTRADICTED (reports zero rows vs 225K advertised — open P0) | canon SHAPE L2 note |
| Wide extractor v05: 5,450 atoms, 96% coverage, 160 files | MEASURED (USER/REPO-ORIGINATED, not re-measured) | four-threads synthesis vs `_RUN_SUMMARY_v05.json` |
| Exact-quote gate 0.96 (n=725) | MEASURED (USER/REPO-ORIGINATED); fills a gap external prior art does not report | prior-art §15 |
| Label gate 0.867 | NOT VERIFIED (internally-set threshold; argument-mining ceiling coincidental) | prior-art §15 |
| Deep-gate RATIFY spread 0.57–0.90 | MEASURED but is PRECISION not accuracy — durability FLAG open | four-threads §1; prior-art §7/§15 |
| ~47% prefix-cache hit | MEASURED (USER/REPO-ORIGINATED) | design §1; prior-art §15 |
| Role swarm R1–R6 + per-role validators | DESIGNED-UNRUN | role-swarm design (E1 runnable now, Results empty) |
| Four-arm specialist experiment (A–D) | DESIGNED-UNRUN | swarm-experiment agent doc (unrun pre-registration) |
| κ 0.19 vs κ 0.398 | VERIFIED-as-distinct (different metrics/datasets; never a trend) | four-threads §1/§5 |
| Verifier-calibration figures 100%→67%→86% | SUPERSEDED→HYPOTHESIS (un-persisted stdout) | four-threads §1 |
| Grouped merge "canonicalise one, note extras" | CONTRADICTED/at-risk (nuance-loss unmeasured) | prior-art §15; automation I6/§7 |
| M2 nuance-preserving synthesis (Orbiter/Interpreter) | DESIGNED-UNRUN; scope kept distinct from M1/M3 | role-swarm scope note; four-threads §2 |
| "canonicalise one statement, note sources" duplicated across two threads | DUPLICATED (fixed by qualifier-preserving merge, automation §7) | automation §7 R2 |

- **One contradiction-resolution rule.** When two claims conflict, resolve by experiment or primary evidence, never by assertion or agreement; until resolved, the composite tier = min of the conflicting inputs and the item stays STRUCTURED with `contradiction_status: flagged`.

## 13. Reconciliation of methodologies (scopes kept distinct)

| Method | Scope | NOT its job | Key artefacts |
|---|---|---|---|
| M1 — atom preparation | Production line: emit `{claim, verbatim quote, labels}` atoms; boundary→evidence→atomise→classify | Not synthesis; not refinement | bronze atoms, verbatim gate |
| M2 — nuance-preserving synthesis | Union-merge dedup that keeps every variant's qualifiers (Orbiter/Interpreter); topic-level fusion | Not per-atom extraction; not the refinement engine | canonical_unit + retained variants (§14 data model) |
| M3 — refinement engine | Re-cut wide blocks into narrow roles; per-role validators; pre-registered ablation loop; promote stabilised roles to code | Not M2 merging | role swarm, validator pairs, Results ledger |
| Wide extractor | Baseline control (one generic worker ×N) | — | v05 |
| Role swarm | M3 instance (R1–R6) | — | frozen role prompts |
| Verifier vs Validator vs GitHub pathway | Verifier = deterministic Layer-A (in-pipe, immediate); Validator = different-family semantic Layer-B (absence-of-wrong); GitHub pathway = the change-admission gate (one allowed path) — three different gates, never conflated | — | gate_result_schema |

## 14. Knowledge-extraction proving ground

One proving-ground component, **not** the company. Integrate the full four-arm protocol plus the essential no-roles repeated-sampling control. Follow the exact dependency order — each stage gates the next.

**Arms (from the pre-registered protocol):**

| Arm | Producers | Validators | Aggregation |
|---|---|---|---|
| A. Wide extractor (control) | one generic worker ×N | downstream gates only | union of runs |
| B. Specialists, no validators | roles R1–R4 ×N | none | union of role outputs |
| C. Specialists + deterministic validators | R1–R4 ×N | Layer-A (verbatim/offset/schema/label/identity), one reason-coded retry | union then Layer-A select |
| D. Specialists + deterministic + independent semantic validators | R1–R4 ×N | Layer-A + Layer-B (different-family, narrow-question, blinded) | union → Layer-A → Layer-B select |
| Control. No-roles repeated sampling | Arm A at high N | gates only | union — **must be included**; k-shot may dominate agents per cost ([Independent Sampling](https://arxiv.org/html/2605.08478v1)) |
| Optional. Deterministic-boundary arm | R1 replaced by unsupervised segmentation (F≈0.76, [AAAI 2007](https://dias.users.greyc.fr/publications/aaai2007.pdf)) | as C/D | — |

**Exact dependency order (do not reorder):**

1. **Baseline instrumentation** — freeze corpus/splits/`norm_v1`; wire cost/cache/latency logging and the failure ledger. Nothing scored until instrumentation is live.
2. **Planted-fault calibration** — inject ≥50 deterministically-mutated bad items per role stream (`mutated_quote, off_by_one_offset, wrong_label, fabricated_atom, identity_swap`) + ≥100 known-good RATIFIED items; measure per-class catch-rate (trueness of validator) and false-kill. Layer-A catch on `mutated_quote`/`fabricated_atom` ≈1.0 (deterministic). Do not trust any validator number before this ([DeepMutation](https://arxiv.org/pdf/1805.05206)).
3. **Repeated-sampling control** — run the no-roles arm; establish cost-efficiency floor per dollar AND per call.
4. **Specialist arms** — B, then C, then D; each split justified only by a measured error it removes ([MAST](https://arxiv.org/html/2503.13657v2)).
5. **Retry / saturation** — retry-depth sub-study {0,1,2} (marginal recovery vs cost, [Self-Refine](https://arxiv.org/abs/2303.17651)); harvesting stop via best-case-recall-vs-runs + capture–recapture ([ASC](https://aclanthology.org/2024.emnlp-main.706.pdf); [capture–recapture](https://pmc.ncbi.nlm.nih.gov/articles/PMC3082794/)); verdict stop via consensus-fidelity curve, difficulty-adaptive not fixed ([Coin Flip Judge](https://arxiv.org/html/2606.13685)).
6. **Durability** — re-run the winning arm on a different-register corpus, zero re-tuning; per-role accept-rates within ±CALIBRATE band. Tests whether the 0.57–0.90 spread is register non-comparability (precision) not gate failure.
7. **One decision record** — a single `decision_record` applying §16 decision table; PASS → production_candidate (subject to durability); FAIL → kill the composed design and keep the wide extractor (a null result is a valid, valuable outcome).

**Qualifier-preserving merge data model (satisfies merge-non-destruction, M2):**

```yaml
canonical_unit:
  id: <hash>
  canonical_claim: <string>
  canonical_quote_span: {source_id, start, end}     # exact substring of norm source
  variants:
    - {variant_id, claim, quote_span, qualifiers: [...], support_count, run_ids: [...]}
  merged_qualifier_set: [{qualifier, held_by_variants: [...]}]   # MUST equal union of variants[].qualifiers
  provenance_ref: <PROV record id>
  # rule: a merge that shrinks merged_qualifier_set fails validation (reason: merge_nondestruction_violation).
```

## 15. Measurement and telemetry contract

Report per arm/stage with 95% CI. **Never conflate consistency and accuracy** (ISO 5725: precision ≠ trueness).

| Metric | Definition | Label |
|---|---|---|
| consistency (precision) | run-to-run accept-rate spread, per-role Jaccard | PRECISION ([ISO 5725-1](https://www.iso.org/standard/69418.html)) |
| trueness | bias vs gold/seeded-fault truth | TRUENESS — reported separately ([Reliability without Validity](https://arxiv.org/pdf/2606.19544v1.pdf)) |
| recall / coverage | fraction of true items found by any run; best-case-recall-vs-runs curve | — ([Large Language Monkeys](https://arxiv.org/abs/2407.21787)) |
| quote validity | quote is exact substring of norm source; Wilson interval | deterministic |
| false rejection (false-kill) | known-good wrongly rejected | validator quality |
| checker catch / false-kill | catch-rate per fault class; false-kill on known-good | validator trueness ([DeepMutation](https://arxiv.org/pdf/1805.05206)) |
| downstream usefulness | insight reused in a V9 decision / merged change | value = measured outcome |
| time saved / process variation | client-side operational deltas | business impact |
| decision impact | did the insight change a decision + move a metric (V10) | business impact |
| cost / latency / cache | κ_t (cost per accepted atom), latency, prefix-cache hit-rate | economics ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)) |
| privacy/security events | leak attempts, secret hits, tenancy violations | P6/P7 telemetry |
| agreement under skew | Gwet AC1 + Krippendorff α with CI (NOT Cohen's κ alone) | ([Gwet AC1 vs kappa](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-61)) |

- **Deterministic join IDs.** Every accepted item carries `{doc_id, char_start, char_end, role_id, run_seed, checker_verdict, reason_code}`; the join key `hash(doc_id,char_start,char_end)` links model output → code gate → DB record → Git change → client outcome, so a single atom is traceable end-to-end.

## 16. Kaizen / deterministic ratchet

```
failure ledger (reason-coded wrong-examples)
  → cluster into a stable error shape
  → prior-art search (attribution_record)
  → deterministic candidate (explicit f(x))
  → fresh-corpus test (never the tuning sample)
  → constitutional gate (§6) + no-stranglehold routing (§6a)
  → rollback proof (git revert applies cleanly)
  → GitHub PR (one allowed path)
  → Vellum witness
  → monitored promotion / demotion (drift → auto-demote)
```

- Improvement flows through the researched YAML scorecard gate, never through Ewan as a review queue. Failure-shapes are the primary writer of compound learning; a proven failure-shape is permanent. A role whose validator kill-rate → ~0 with concentrated near-miss errors is a code candidate → expressibility licence (explicit f(x), fresh-sample Wilson ≥ CALIBRATE [STRUCTURED]) → becomes code and leaves the swarm; roles that plateau stay AI, bounded by measured (ρ*, p̂).

## 17. Configuration / change / deployment path (no side doors)

```
chezmoi distribution (config SSOT, self-heal)
  → branch / worktree
  → PR
  → CODEOWNERS review + required status checks + required workflows
  → merge queue (FIFO)
  → protected default branch (signed commits, linear history, no force-push)
  → environment-gated deploy (OIDC, required human reviewer)
  → signed / attested artifact (Sigstore / SLSA-style)
  → Temporal-driven promotion to Beast
  → Vellum witness
```

- A change that skips a stage is rejected (this is a change-admission gate, in the HARD-HALT family only for direct-Beast side doors; other skips degrade with a repair path back onto the lane). **Break-glass** is the only bypass: a named GitHub App/admin, reason logged, Vellum-witnessed, reconciled by post-hoc PR ≤24h — loud and accountable. GitKraken is the human ergonomic surface onto the *same* path, never a second path. No Mac-PC push; no direct Beast write; no merge performed by this spec's executor.

## 18. Ordered tonight runway (work packages)

Do not imply all implementation finishes tonight. This defines the highest-value coherent package (the agent-facing contract + validation harness + calibration scaffold) that can. Deploy/Beast stages are explicitly out of tonight's scope.

| WP | Output (exact) | Depends on | Verification | Owner/seat | Stop condition | Parallel? |
|---|---|---|---|---|---|---|
| WP-1 | Agent-facing JSON schemas: `gate_result_schema`, `hypothesis_record`, `attribution_record`, `canonical_unit`, join-ID record | — | schemas parse; validate against sample instances | Rust/code | any schema unparseable → fix before proceeding | no (foundation) |
| WP-2 | Deterministic validation harness for this spec (§20 checks) | WP-1 | harness runs green on this file | code | HARD-HALT check false-negative → stop | with WP-3 |
| WP-3 | `norm_v1` spec + `corpus_v1.lock` (frozen ids) + split manifest | — | determinism (identical in→out); hashes pinned | Python | corpus not freezable tonight → mark TARGET, gate later | with WP-2 |
| WP-4 | Planted-fault battery generator (5 fault classes) + known-good set loader | WP-1, WP-3 | generates ≥50 faults/role + ≥100 good; deterministic | code | non-deterministic faults → fix | after WP-3 |
| WP-5 | Reason-code + next_action enums wired into gate stubs (no-dead-end assertion) | WP-1 | every rejection path yields route+owner; no-dead-end test passes | code | any dead-end path → P0, stop | after WP-1 |
| WP-6 | This spec committed to PR #4 branch + PR retitled/updated (draft) | WP-1..WP-5 authored | byte-identical to workspace (sha256); only 3 files in PR | devin (proxy, logged) | non-identical copies → stop | last |

- **Out of tonight's scope (named):** running scored arms, Beast promotion, live deploy, client onboarding — all require calibration + ratification first.

## 19. Repository / file map

| Artefact | Path | Status |
|---|---|---|
| This spec (canonical workspace copy) | `/home/user/workspace/amplified-partners-ai-native-operating-system__implementation-spec__2026-07-12T22-05-00Z__perplexity.md` | VERIFIED (created) |
| This spec (repo copy, byte-identical) | `perplexity-inbox/amplified-partners-ai-native-operating-system__2026-07-12T22-05-00Z__perplexity/amplified-partners-ai-native-operating-system__implementation-spec__2026-07-12T22-05-00Z__perplexity.md` | VERIFIED (created on branch) |
| Prior-art research (preserve exactly) | `perplexity-inbox/specialist-extraction-swarm__2026-07-12T20-50-00Z__perplexity/specialist-extraction-swarm-prior-art__human__2026-07-12T20-50-00Z__perplexity.pplx.md` | VERIFIED (pre-existing) |
| Experiment protocol (preserve exactly) | `perplexity-inbox/specialist-extraction-swarm__2026-07-12T20-50-00Z__perplexity/specialist-extraction-swarm-experiment__agent__2026-07-12T20-50-00Z__perplexity.pplx.md` | VERIFIED (pre-existing) |
| Schemas (WP-1) | TARGET PATH: `perplexity-inbox/amplified-partners-ai-native-operating-system__2026-07-12T22-05-00Z__perplexity/schemas/` — create through PR | TARGET |
| Validation harness (WP-2) | TARGET PATH: same folder `/harness/` — create through PR | TARGET |
| Canon (constitution, goals, etc.) | Private fleet-config vault (internal provenance) — read-only, not modified here | VERIFIED (read) |

## 20. Checklists (outcome tests, not generic steps)

**SPEC CHECKLIST (this document):**
- [ ] YAML front matter parses.
- [ ] Exactly one H1.
- [ ] No unfinished-marker or placeholder tokens; no hidden fixed threshold (all unfitted numbers are `CALIBRATE [STRUCTURED]`).
- [ ] No AI-as-signer language; Ewan is ratifier, AI is substrate/proxy.
- [ ] No direct-Beast-write suggestion anywhere.
- [ ] No private repo URLs in the body.
- [ ] Every gate returns `gate_result_schema` with a progress `route` (no-dead-end).
- [ ] Every human-facing view points to this canonical agent artefact.

**RESEARCH CHECKLIST (receiving AI, before any scored run):**
- [ ] `attribution_record` exists for every mechanism entering production.
- [ ] Prior-art search recorded (not just its conclusion) for anything tagged `apparently_novel`.
- [ ] Validators calibrated by planted faults before any validator number is trusted.
- [ ] Consistency and accuracy reported separately; AC1/α (not Cohen's κ alone) under skew.

**JOB CHECKLIST (receiving AI, execution):**
- [ ] WP-1..WP-6 completed in order; parallelism only where §18 permits.
- [ ] Byte-identity of workspace and repo copies confirmed by sha256.
- [ ] Only this spec + the two pre-existing artefacts present in PR #4.
- [ ] PR #4 left draft and unmerged; title/body updated.
- [ ] Every rejection encountered recorded `next_action` + `owner`.

## 21. Acceptance, kill, promotion, demotion, rollback, amendment

- **Acceptance checks (Ewan's binding set, machine-checkable):** (1) no unexplained halt — every HARD-HALT maps to the §6a HARD-HALT set; (2) every gate has a progress route; (3) every artefact has an agent schema; (4) every human-facing document points to the canonical agent artefact; (5) every rejection records `next_action` + `owner`; (6) every enforced rule has `version` + `falsification` + `amendment` fields.
- **Kill:** composed extraction design killed if arms B/C/D do not beat A on quote-gate accept by margin `M` at ≤ cost× `C` (CALIBRATE [STRUCTURED]); or if the no-roles arm dominates on cost per dollar AND per call.
- **Promotion:** INTUITED→STRUCTURED via rubric codification; STRUCTURED→MEASURED via empirical calibration (≥10 events/param/outcome, held-out, drift monitor); MEASURED→PROVEN via formal proof with verified preconditions. Tier-skipping is a P0.
- **Demotion:** automatic on drift, elapsed `valid_until`, failed precondition, or LLM-in-loop (caps at INTUITED). Hiding a demotion is a P0.
- **Rollback:** every promoted change carries a rollback proof (`git revert` applies cleanly) before deploy.
- **Amendment:** supersede via the one allowed change path; never edit live; retain superseded versions.
- **Absolute (not optimised metrics):** constitutional rods and privacy/security/sovereignty gates are current invariants; they are not tuned against a threshold.

## 22. Risks, contradictions, unresolved questions, human ratification gates

- **Risks:** over-decomposition adds cost without removing measured error ([MAST](https://arxiv.org/html/2503.13657v2)); union without a strong selector banks noise (precision ~12–15%, [L3X](https://people.mpi-inf.mpg.de/~ssinghan/tacl_paper.pdf)); same-family checkers give false consistency ([Kuncheva & Whitaker](http://machine-learning.martinsewell.com/ensembles/KunchevaWhitaker2003.pdf)); threshold over-portability across corpora; silent nuance loss on merge; Brain zero-row contradiction blocks retrieval trust.
- **Contradictions:** decomposition helps vs is-not-worth-it — resolved by the four-arm experiment, not assertion. Consistency-vs-accuracy conflation — resolved by INV-9 separation.
- **Research-resolvable (resolve, do not gate):** aggregation policy (union-then-select, no synthesis — resolved [Selection Bottleneck](https://arxiv.org/html/2603.20324v1)); different-family checker (resolved [FACTS Grounding](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/)); stop rules (resolved as curves, not fixed counts).
- **Genuine human ratification gates (only these):** (G-a) win-win call on any money-in logic; (G-b) legal/Ulysses/give-away commitments (solicitor + signed `===--- yes`); (G-c) policy_change / rod-set edits; (G-d) client consent scope and client data deletion/export authority; (G-e) destructive delete of canonical. Everything else is either agent-actionable or logged-proxy.

## 23. Execution baton (ordered, zero additional design choices)

A receiving AI executes these in order; the only permitted pauses are named CALIBRATE runs and the §22 human gates.

1. Author WP-1 schemas from the inline definitions in §6a/§4/§5/§14/§15. **No design choice required.**
2. Author WP-2 validation harness implementing every §20 SPEC CHECKLIST item + §21 acceptance checks. **No design choice.**
3. Author WP-3 `norm_v1` + `corpus_v1.lock` + splits; if the corpus cannot be frozen tonight, mark it TARGET and gate the scored runs on it (do not fabricate ids). **CALIBRATE: exact file ids.**
4. Author WP-4 planted-fault battery + known-good loader. **No design choice** (fault classes fixed in §14).
5. Wire WP-5 reason-code/next_action enums into gate stubs; run the no-dead-end assertion. **No design choice.**
6. Execute WP-6: write this spec into the PR #4 branch path (§19), confirm byte-identity (sha256), commit with attribution, push, retitle/update PR #4, leave draft + unmerged. **Logged proxy act.**
7. STOP for human gates only where §22 (G-a..G-e) applies. Emit the session-close manifest (§24).
8. Scored arms, calibration of `M`/`C`/bands, Beast promotion and deploy are the *next* baton, gated on §21 promotion rules — not tonight.

## 24. Session-close manifest schema and Vellum event templates

```yaml
session_close_manifest:
  session_id: <slug>
  seat: <author-seat>
  date_utc: <iso>
  artefacts: [{path, sha256, status}]
  gates_evaluated: [{gate_id, verdict, reason_code, route}]
  proxy_acts: [{act, reason, timestamp}]         # AI_PARTNER_PROXY, logged
  open_questions: [<id>]
  human_gates_pending: [<G-a..G-e>]
  next_action: <imperative>
  closure_line: "<[CLOSURE] ...>"
```

```yaml
vellum_event_templates:  # references + decisions only; no payloads; AI entries epistemic_tier=INTUITED
vellum_problem:      {type: problem,      ref, description, tier: INTUITED, seat}
vellum_decision:     {type: decision,     ref, chosen, options, signer, reason, timestamp}
vellum_contradiction:{type: contradiction, ref, claim_a, claim_b, resolution_rule}
vellum_artifact:     {type: artifact,     ref, sha256, path, status}
vellum_test_result:  {type: test_result,  ref, metric, value, ci, precision_or_trueness}
vellum_promotion:    {type: promotion,    ref, from_tier, to_tier, promotion_record_id}
vellum_demotion:     {type: demotion,     ref, from_tier, to_tier, trigger}
vellum_open_question:{type: open_question, ref, question, owner}
```

## 25. Closure

This specification is a current working hypothesis (v01, STRUCTURED), agent-facing first, with human sovereignty and ratification intact and constitutional/privacy/security/sovereignty invariants absolute for now. Its highest-priority executable work package is **WP-1: author the agent-facing JSON schemas and the deterministic validation harness**, because every other gate, route and acceptance check in this document depends on those schemas existing and parsing.

[CLOSURE] branch=PLAN | proxy=1 logged (repo write via pipe drop-point) | gates=human ratification G-a..G-e deferred to next baton | inbox=amplified-partners-ai-native-operating-system__implementation-spec__2026-07-12T22-05-00Z__perplexity.md | tier=STRUCTURED
