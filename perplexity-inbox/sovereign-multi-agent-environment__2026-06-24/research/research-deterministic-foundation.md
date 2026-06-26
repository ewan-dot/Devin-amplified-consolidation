# Deterministic Foundation Research: Control Planes, Durable Execution & Agent Infrastructure
### Amplified Partners — Multi-Agent Dev Environment
*Research compiled June 2026 · Covers 2025–2026 literature, frameworks, and industry patterns*

---

## Table of Contents

1. [The Core Architectural Insight](#1-the-core-architectural-insight)
2. [Deterministic Orchestration Patterns](#2-deterministic-orchestration-patterns)
3. [Durable Execution: Temporal and the 2025–2026 Landscape](#3-durable-execution-temporal-and-the-20252026-landscape)
4. [The Broker / Capability Pattern: Zero-Standing-Privilege Access](#4-the-broker--capability-pattern-zero-standing-privilege-access)
5. [Deterministic Data Transforms and Neutralisation Pipelines](#5-deterministic-data-transforms-and-neutralisation-pipelines)
6. [What's New: 2025–2026 Frameworks, Papers, and Industry Shifts](#6-whats-new-20252026-frameworks-papers-and-industry-shifts)
7. [Recommended Deterministic Foundation Stack](#7-recommended-deterministic-foundation-stack)

---

## 1. The Core Architectural Insight

> **"The entity that governs an agent system must not itself be an LLM."**

This sentence, from a March 2026 Zylos research paper, crystallises the convergence happening independently across the industry. When an LLM orchestrates itself — deciding its own budgets, enforcing its own security policies, validating its own outputs — the "who watches the watchmen" problem collapses any safety guarantee into probabilistic hope. A red-team benchmark with 50 adversarial prompts demonstrated this starkly: standard prompt-based governance failed **26.7% of the time**, while a deterministic control plane achieved **0% violations** by making unauthorised actions architecturally impossible rather than merely discouraged. ([Zylos, March 2026](https://zylos.ai/research/2026-03-11-deterministic-governance-kernels-agent-runtimes))

The industrial production success rate for fully autonomous LLM agents sits between 5% and 11%. A study of over 1,600 production traces found failure rates ranging from 41% to 86.7%, split into system design failures (41.8%), inter-agent misalignment (37%), and task verification failures (21.3%). ([tianpan.co, April 2026](https://tianpan.co/blog/2026-04-20-workflow-engines-beat-llm-agents))

**The emerging consensus:** Treat the LLM as a nondeterministic kernel process wrapped in a deterministic runtime — the same relationship as a user-space application running inside an OS kernel. The kernel does not ask user-space processes whether they are allowed to access protected memory; it enforces that deterministically.

Google made this explicit in April 2025 when it shipped `SequentialAgent`, `ParallelAgent`, and `LoopAgent` in its Agent Development Kit (ADK), with documentation stating these classes are "not powered by an LLM, and is thus deterministic in how it executes." Four months earlier, Anthropic had drawn the same line in writing: workflows are systems where developer code controls the loop; agents are systems where the LLM does. ([YouTube analysis, April 2026](https://www.youtube.com/watch?v=QmW91KCKNj8))

The split this creates in system design:

| Layer | Characteristic | Examples |
|---|---|---|
| **Control plane** (Foundation) | Deterministic: same input → same output, replayable, auditable, no LLM | Temporal workflows, state machines, policy engines, provisioner, janitor, data normaliser, access broker |
| **Agent layer** (On top) | Probabilistic: non-deterministic reasoning, tool use, generation | LLM workers, <150-line thin agents, specialised cells |

---

## 2. Deterministic Orchestration Patterns

### 2.1 The Fundamental Decision Framework

Before choosing an orchestration approach, two questions determine whether the task belongs to deterministic code or an LLM agent: ([tianpan.co, April 2026](https://tianpan.co/blog/2026-04-20-workflow-engines-beat-llm-agents))

1. **Is the full set of execution paths enumerable at design time?** If you can draw a complete flowchart — including all exception branches — you have a workflow problem for a deterministic engine. If the execution path genuinely cannot be determined until runtime because it depends on open-ended reasoning over unstructured inputs, you have an agent problem.

2. **Does the business require reproducibility and auditability?** If a compliance officer must point to a specific execution and explain exactly what decision was made, when, and why — you need deterministic orchestration. An LLM agent running at temperature 0 does not satisfy this requirement.

The corollary: for a **surprisingly large class of structured business processes**, deterministic engines are the right tool. Temporal, AWS Step Functions, and Apache Airflow share one property that LLM agents fundamentally cannot offer — *the same input produces the same output, every time, with a full audit trail.*

### 2.2 Deterministic Workflow Engines

**Temporal** is built for durable, long-running execution where the workflow must survive process crashes, bad data, and network failures. Its event history allows replaying execution state exactly as it was — if a worker crashes mid-workflow, Temporal replays the history to reconstruct state without re-executing completed steps. Netflix runs their entire CI/CD pipeline through Temporal. Coinbase uses it for crypto transaction processing.

**AWS Step Functions** uses a visual-first state machine model, excellent for workflows with a manageable number of defined states. Native retry and error handling baked into the state definition. Tightly integrated with the AWS service ecosystem.

**Apache Airflow** dominates data engineering orchestration with a DAG-first model. Best suited for batch-oriented, sequential data pipelines. Less appropriate for event-driven or long-running agentic flows.

The Temporal approach is examined in depth in Section 3.

### 2.3 State Machines and DAGs for Agent Control

**LangGraph** (LangChain, v0.4+) models agent workflows as explicit state-machine graphs. Each node is an LLM or tool; edges define deterministic or agent-chosen transitions. The key property: *given the state at step t and an action, LangGraph deterministically produces the state at step t+1.* ([LangGraph 2025 review, Substack](https://neurlcreators.substack.com/p/langgraph-2025-review))

LangGraph's two edge types make the split explicit:
- **Definite edges** (`add_edge("A", "B")`) — always taken, deterministic
- **Conditional edges** (`add_conditional_edges(...)`) — router function inspects state and returns next node name as a string; the LLM may inform the state, but the routing function itself is a pure Python function

This architecture makes every transition auditable: inspect the state at any checkpoint and deterministically replay the decision. LangGraph Platform went GA in May 2025, adding deployment, autoscaling, and monitoring for stateful agents.

**The "planning/execution split"** is a key pattern emerging from production: a deterministic orchestrator generates a structured multi-step plan before any tool fires. The LLM proposes; deterministic routing code dispatches. On failure, a replan node generates a revised plan based on completed steps and the error — the agent routes there automatically, then re-enters execution. ([Ranjan Kumar, December 2025](https://ranjankumar.in/building-production-ready-ai-agents-with-langgraph-a-developers-guide-to-deterministic-workflows))

### 2.4 "LLM Proposes, Deterministic Code Disposes" Patterns

Four production patterns for keeping the control plane deterministic:

**Pattern A: Thin Agent / Fat Platform** (Praetorian, February 2026)
Agents are reduced to stateless, ephemeral workers of <150 lines. Skills hold knowledge, loaded strictly on-demand (Just-in-Time). Hooks provide enforcement, operating *outside* the LLM's context. An eight-layer deterministic enforcement system governs execution. The key inversion: monolithic agents had 1,200+ line bodies suffering attention dilution; the thin model moves all governance logic outside the LLM context entirely. ([Praetorian, February 2026](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/))

**Pattern B: Pre-Execution Gates + Runtime Guards**
Before any agent action runs, enforce deterministically: (1) intent validation — does the proposed action align with the user's actual goal? (2) safety checks — does this action violate any policy or constraint? (3) resource bounds — can this complete within budget/time limits? These gates run in deterministic code; their Boolean results gate execution. ([bigyan.dev](https://www.bigyan.dev/blog/deterministic-control-planes-agentic-ai/))

**Pattern C: AgentSpec DSL (ICSE 2026)**
AgentSpec is a lightweight domain-specific language for specifying and enforcing runtime constraints on LLM agents. Rules take a three-tuple form: `trigger` (event), `predicates` (Boolean conditions), `enforcement` (action). Rules are evaluated by the AgentSpec runtime — deterministic code — before any agent action executes. Enforcement overhead: **1–3ms** regardless of rule complexity. Results: 90%+ unsafe code executions blocked, 100% compliance in autonomous vehicle scenarios. ([AgentSpec, arXiv:2503.18666, ICSE 2026](https://arxiv.org/abs/2503.18666))

```
rule @prevent_credential_exfiltration
trigger
  tool_call("network_request")
check
  !is_approved_egress_domain(request.url) ||
  contains_credential_pattern(request.body)
enforce
  stop
end

rule @budget_guard
trigger
  llm_call
check
  budget.tokens_remaining < budget.min_reserve
enforce
  stop
end
```

**Pattern D: Compiled AI** (arXiv:2604.05150, April 2026)
The LLM generates executable code artifacts during a *compilation* phase, after which workflows execute deterministically **without further model invocation**. Properties: one-time LLM invocation, zero-token deterministic execution, mandatory multi-stage validation before deployment. Results: 96% task completion with zero execution tokens, 57x fewer tokens at 1,000 transactions vs direct runtime inference, 100% reproducibility. The framing: "let the probabilistic thing help you build the machine, but do not make the probabilistic thing *be* the machine." ([Compiled AI, arXiv, April 2026](https://arxiv.org/abs/2604.05150))

### 2.5 Current Best Practice Summary

The control plane/data plane analogy from network engineering is now the dominant mental model: the control plane decides where traffic goes while the data plane moves packets. In agentic systems, the control plane decides which agent executes, validates pre/postconditions, and manages state transitions — while agents handle cognitive work. ([bigyan.dev](https://www.bigyan.dev/blog/deterministic-control-planes-agentic-ai/))

The Google CTO office summarised the production imperative in December 2025: "This shifts the reliability burden from the probabilistic LLM to deterministic system design, **where it belongs**." ([Google Cloud CTO, December 2025](https://cloud.google.com/transform/ai-grew-up-and-got-a-job-lessons-from-2025-on-agents-and-trust))

---

## 3. Durable Execution: Temporal and the 2025–2026 Landscape

### 3.1 What Durable Execution Provides

Durable execution is a programming model where the *runtime*, not application code, guarantees that a function runs to completion exactly once, even across crashes, restarts, deploys, and network failures. Three guarantees that ordinary code cannot provide: ([Metacto, June 2026](https://www.metacto.com/blogs/durable-execution-ai-agents))

1. **State persistence** — workflow variables survive process death
2. **Exactly-once side effects** — external calls record their results so they are not repeated on replay
3. **Resumability** — execution continues from the failure point, not from the start

### 3.2 Temporal: Architecture and the AI Agent Fit

Temporal's model separates concerns precisely along the deterministic/non-deterministic boundary: ([Temporal blog, November 2025](https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal))

- **Workflow code** must be deterministic — same event history produces same commands. This enables replay-safe, crash-recoverable orchestration.
- **Activities** are where actual work happens: calling LLMs, invoking tools, making API requests. These can be as unpredictable and non-deterministic as needed.
- The workflow defines *what* should happen. Temporal's server handles persistence, retries, scheduling, and delivery.

**The critical implementation rule:** Never call an LLM directly inside a Temporal Workflow method. Wrap all LLM calls in Temporal Activities to keep the workflow deterministic. The Activity records its result in the event history; on replay, the cached result is returned and the LLM is never re-invoked. ([dev.to, May 2026](https://dev.to/machinecodingmaster/stop-letting-ai-agents-break-your-database-transactional-multi-agent-workflows-with-temporal-and-47dc))

**For tool calling:** Map tool calls to Activities and Workflows. Execute activities sequentially or in parallel. Push tool results into the message queue. Rely on Temporal retry policies for each tool call. ([Spiral Scout PDF, 2025](https://spiralscout.com/wp-content/uploads/2025/02/A-Practical-and-Tactical-Approach-to-AI-in-Temporal.pdf))

**Idempotency requirement:** Every tool that writes external state (creates a ticket, sends an email, charges a card) must carry an idempotency key tied to the workflow state to prevent duplicate side effects on replay. The key must be derived by the orchestrator, not the tool call — stable across LLM re-plans, across crash-recovery replays, across human-in-the-loop interruptions. ([tianpan.co, April 2026](https://tianpan.co/blog/2026-04-23-agent-idempotency-orchestration-contract))

### 3.3 2025–2026 Developments in Temporal + AI Agents

| Date | Development |
|---|---|
| September 2025 | OpenAI Agents SDK integration public preview — durable execution built directly into OpenAI-based agents |
| Late 2025 | Pydantic AI ships first-class Temporal integration |
| November 2025 | Vercel AI SDK integration: every `generateText()` call wraps in Activities automatically |
| February 2026 | Temporal raises $300M Series D at $5B valuation, led by a16z — 9.1 trillion lifetime action executions, 1.86 trillion from AI-native companies alone |
| March 2026 | OpenAI Agents SDK integration goes generally available |
| 2026 | Replay 2026 announcements: Serverless Workers, Standalone Activities, Workflow Streams, Google ADK and OpenAI SDK integrations |

Sources: ([zylos.ai, February 2026](https://zylos.ai/research/2026-02-17-durable-execution-ai-agents/)), ([agentmarketcap.ai, April 2026](https://agentmarketcap.ai/blog/2026/04/09/durable-execution-ai-agents-temporal-inngest-prefect)), ([infoq.com, September 2025](https://www.infoq.com/news/2025/09/temporal-aiagent/))

### 3.4 The Broader Durable Execution Landscape

The framework choice depends on existing infrastructure and workload shape:

| Platform | Mechanism | New Infra Required | Best For |
|---|---|---|---|
| **Temporal** | Journal/Replay | Yes (Temporal cluster) | Complex, long-running orchestrations; enterprise; Amplified's use case |
| **Restate** | Journal/Replay (lighter) | Minimal (managed server) | Serverless/edge deployments, microservice orchestration |
| **DBOS** | Transactional state in Postgres | No (uses existing DB) | Zero-infra lift; in-process durability via library |
| **LangGraph** | DB Checkpointing (Postgres/DynamoDB) | No | Graph-shaped agent workflows, natural state-machine logic |
| **Inngest** | Step-based retries | Minimal (managed service) | Serverless, event-driven, TypeScript-native |
| **Cloudflare Workflows** | Step-based (GA 2025) | None | Edge-deployed agents, runs days to weeks |
| **Azure Durable Task** | Journal/Replay | Managed (preview late 2025) | Microsoft-ecosystem agents, multi-day human-in-loop pauses |

Inngest's 2026 report noted that durable execution "crossed into the early majority in 2025 with new offerings from AWS, Cloudflare, and Vercel, driven primarily by AI Agent infrastructure needs." ([Inngest, February 2026](https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents))

### 3.5 The Saga Pattern for Agentic Workflows

When a multi-step AI workflow partially fails, previously completed steps may need to be undone. The Saga pattern adapted from distributed systems is the current best practice:

- **Orchestration saga**: Central coordinator controls step sequence and rollbacks — best for complex, predictable multi-step flows
- **Choreography saga**: Services emit events, no central coordinator — best for loosely coupled event-driven agent systems

**The AI-specific caveat:** Some agent actions are inherently irreversible (sent emails, published content). Frameworks provide compensation hooks but developers must design what compensation means for each action — and some actions require human review gates rather than automatic rollback. Register compensating actions immediately after every successful tool execution before proceeding. ([dev.to, May 2026](https://dev.to/machinecodingmaster/stop-letting-ai-agents-break-your-database-transactional-multi-agent-workflows-with-temporal-and-47dc))

---

## 4. The Broker / Capability Pattern: Zero-Standing-Privilege Access

### 4.1 The Threat Model

The core risk is not LLM capability — it is identity. AI agents are non-human identities with credentials, permissions, and execution authority. Once those identities can chain actions across code, cloud, and data systems, traditional IAM assumptions about static roles and human review no longer hold.

The numbers are stark: ([NHIMG, May 2026](https://nhimg.org/articles/ai-agent-identity-risk-is-outpacing-zero-trust-controls/))
- **80% of organisations** report their AI agents have already performed actions beyond their intended scope
- When AWS credentials are exposed publicly, attackers attempt access within an average of **17 minutes** (as fast as 9 minutes)
- Only **44% of organisations** have implemented any policies to govern AI agents, despite 92% saying governance is critical

**Zero Standing Privilege (ZSP)** is stronger than least-privilege alone: it removes persistent access altogether and grants it only when needed. Narrow permissions *plus* short access duration.

### 4.2 The Just-in-Time Credential Broker Pattern

The pattern — as implemented by Britive, Strata Maverics, HashiCorp Vault, and others — follows this flow: ([Metacto, June 2026](https://www.metacto.com/blogs/ai-agent-secrets-management-production)), ([Strata, April 2026](https://www.strata.io/blog/agentic-identity/just-in-time-provisioning-creates-artificial-agent-identities-on-demand-5b/))

1. Agent decides it needs to call Tool X
2. Credential resolver checks: is this agent identity authorised to call Tool X **right now**, given its context (tenant, user, environment, action)?
3. If yes, the resolver mints a short-lived credential (signed token, temporary API key, one-time secret) and returns it
4. Agent makes the call with the credential
5. Credential expires automatically — measured in **seconds or minutes**, not days

**HashiCorp Vault validated pattern:** ([HashiCorp developer docs, September 2025](https://developer.hashicorp.com/validated-patterns/vault/ai-agent-identity-with-hashicorp-vault))
- User authenticates → JWT with user/group claims issued
- AI agent receives JWT, validates it, exchanges it for an OBO (on-behalf-of) token
- Agent uses OBO token to authenticate with Vault
- Vault validates JWT and maps to an appropriate Vault policy based on group claims
- Vault issues a **scoped, time-limited Vault token** → agent requests dynamic just-in-time credentials
- Complete traceability and user attribution for full auditability

**Strata Maverics JIT provisioning:** An identity is provisioned when the agent is instantiated, assigned least-privilege credentials with TTL, purpose, risk, and delegation context attached. When the task is done, the identity is retired. No orphaned credentials, no permission sprawl.

**For agent-to-agent (A2A) flows:** Britive's model grants temporary permission per-agent per-task, then automatically revokes it — exactly-once, JIT, zero standing. ([Britive, July 2024](https://www.britive.com/resource/blog/agent-to-agent-access-security))

### 4.3 Policy-as-Code: OPA and Cedar for Deterministic Authorization

**The principle:** The policy engine must be deterministic, and LLM output must enter it as *data*, not as a *decision*. The final ALLOW/DENY must always come from deterministic evaluation. ([Zylos, March 2026](https://zylos.ai/research/2026-03-14-policy-engines-ai-agent-governance/))

**Open Policy Agent (OPA)**

OPA is the CNCF-graduated, general-purpose policy engine — the de facto standard for infrastructure policy. Its model: Input (JSON) + Policy (Rego) + Data (JSON) = Decision (allow/deny). For AI agents, OPA sits as a centralised policy decision point that evaluates all three authorisation layers in a single query:
- Layer 1: Tool access — can this agent invoke this MCP tool?
- Layer 2: Resource access — can this agent reach this specific resource?
- Layer 3: Command authorisation — is this specific action allowed for this role?

OPA achieves **1–5ms policy evaluation latency** for typical policies with local data. Same input always produces same output. ([codilime.com, April 2026](https://codilime.com/blog/why-use-open-policy-agent-for-your-ai-agents/))

OPA is the right choice for: structured policy against structured data, infrastructure admission control, API authorisation, rate limits, blocklist checks, trust-level minimums, capability existence checks — all "Category A: Never LLM" decisions.

**Cedar (AWS)**

Cedar is Amazon's open-source authorization policy language, used in production across AWS services including Bedrock AgentCore. Cedar's authoriser is formally **deterministic**: guaranteed to terminate and always produce the same authorisation decision for a given request, hierarchy, and set of policies. Implemented in Rust and formally verified in Lean. ([Cedar arXiv paper](https://arxiv.org/pdf/2403.04651.pdf))

AWS Bedrock AgentCore uses Cedar directly for AI agent tool governance: every agent action through the Gateway is intercepted and evaluated *at the boundary outside of agent's code* — ensuring consistent, deterministic enforcement regardless of how the agent is implemented. ([AWS Bedrock AgentCore docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.md))

Cedar for coding agent hooks ([blog.sondera.ai, March 2026](https://blog.sondera.ai/p/hooking-coding-agents-with-the-cedar)):
- A Reference Monitor using Rust hooks intercepts every tool call, satisfying three criteria: always invoked, tamper-proof, verifiable
- Cedar evaluates the event deterministically: same input, same result
- Rules can forbid dangerous commands, constrain network egress, require human approval for deletion

**Hybrid pipeline for governance:** ([Zylos, March 2026](https://zylos.ai/research/2026-03-14-policy-engines-ai-agent-governance/))

| Category | Mechanism | Examples |
|---|---|---|
| **A — Never LLM** | Pure deterministic (OPA/Cedar) | Rate limits, blocklists, trust-level checks, session isolation |
| **B — Default deterministic** | Deterministic, optional LLM assist | Routine RBAC checks with contextual enrichment |
| **C — Must LLM** | LLM produces structured output → feeds into deterministic enforcement | Semantic classification of ambiguous content |
| **D — Hybrid** | Deterministic prefilter → optional LLM → deterministic enforcement | Complex authorization with semantic understanding |

### 4.4 Zero-Trust Architecture Alignment

OWASP Agentic AI Top 10 and OWASP Non-Human Identity Top 10 now address agents explicitly. NIST Zero Trust (SP 800-207, PR.AC-4) requires continuous verification extending to non-human identities. The practical stack: ([NHIMG, May 2026](https://nhimg.org/articles/ai-agent-identity-risk-is-outpacing-zero-trust-controls/))

1. Inventory every AI agent and machine identity with named ownership, business purpose, and scope
2. Convert standing access to task-scoped access with short-lived credentials
3. Automate compromise response — pre-stage token revocation, secret rotation, agent quarantine
4. Track agent behaviour for scope drift — monitor for unexpected tool calls, access to data outside original task scope

**Identity blast radius** is the key operational metric: how far can one compromised identity move before controls intervene? This is the measure that matters more than raw access counts.

### 4.5 WASM Capability Sandboxing for Agent Cells

WebAssembly has matured into a serious server-side sandboxing primitive for agent runtime isolation. The capability model is exactly what the Amplified architecture needs for agent cells: ([Zylos, March 2026](https://zylos.ai/research/2026-03-12-wasm-sandboxing-ai-agent-runtime-isolation)), ([agentmarketcap.ai, April 2026](https://agentmarketcap.ai/blog/2026/04/07/webassembly-sandboxing-agent-tool-execution-wasm-vs-docker))

- **Deny-by-default**: A freshly instantiated WASM module can compute but cannot open files, make network connections, spawn processes, query clocks, or generate random numbers — until the host *explicitly* grants those capabilities at instantiation time
- **Hard ceiling**: Even if an agent session is compromised (e.g., prompt injection causes unexpected code execution), it cannot exfiltrate data it was never granted access to
- **Microsecond cold starts** vs 125–200ms for Firecracker microVMs
- **WASI 0.2** (stable, 2024): `wasi:http` enables HTTP client/server natively with capability-scoped access
- **Microsoft Wassette** (August 2025): security-oriented Wasmtime runtime for MCP-connected AI agents, deny-by-default fine-grained permissions

**Layered isolation strategy for production:**
- Deterministic, bounded tool calls → WASM at the edge (sub-5ms, capability-bounded)
- Arbitrary code execution by agents → Firecracker microVMs (125–200ms, kernel-isolated)
- OS-dependent trusted infrastructure → Docker (50–300ms, shared kernel with namespacing)

---

## 5. Deterministic Data Transforms and Neutralisation Pipelines

### 5.1 The Neutralisation / De-labelling Pattern

A data-neutralisation step that strips, de-identifies, or normalises content before it reaches agent cells needs to be deterministic for two reasons: reproducibility (same input → same output) and provenance (you can prove what was done to the data). The architecture pattern from production deployments:

**Deterministic token substitution** is the foundation. "Sarah Johnson" maps to `[PATIENT_A]` deterministically using: ([Towards AI, November 2025](https://pub.towardsai.net/the-builders-notes-the-de-identification-pipeline-no-one-shows-you-processing-phi-through-llms-23c803f14b08))

```python
token = hash(original_value + cryptographic_salt + identifier_type)
```

Key properties:
- Same input always generates same token (deterministic)
- One-way: difficult to reverse without salt
- Type-specific: different token formats for different identifier classes
- Cross-document consistent: the same entity gets the same token everywhere

**The full de-identification pipeline** ([Towards AI, November 2025](https://pub.towardsai.net/the-builders-notes-the-de-identification-pipeline-no-one-shows-you-processing-phi-through-llms-23c803f14b08)):
1. Validate user authorisation
2. De-identify input using deterministic tokenisation
3. Log de-identification to immutable audit trail
4. Pass de-identified content to LLM / agent cell
5. Validate LLM response for PHI/label leakage
6. Re-identify response **in secure context only** (server-side, RBAC-gated, rate-limited)
7. Log re-identification

**Deterministic NER models** outperform zero-shot LLM approaches for structured PII categories. John Snow Labs Healthcare NLP achieved 96% F1 in PHI detection vs 79% for GPT-4o, at 50–575% fewer errors, while providing deterministic behaviour, consistent obfuscation, and preserved longitudinal linkage. ([John Snow Labs, July 2025](https://www.johnsnowlabs.com/delivering-regulatory-grade-automated-multimodal-medical-data-de-identification/))

**LLM use remains appropriate for**: context-sensitive entity resolution in ambiguous text, classifying unstructured fields where rule-based patterns are insufficient, and generating synthetic replacement values — but the LLM output always feeds into a deterministic validation and substitution layer, never bypassing it.

### 5.2 Reproducible Data Transforms with Content-Addressing

Content-addressing (CAS) assigns data identifiers by hashing content, not by location or filename. The same content always produces the same hash — enabling deduplication, integrity verification, and provenance tracking. ([Abilian Innovation Lab](https://lab.abilian.com/Tech/Databases%20&%20Persistence/Content%20Addressable%20Storage%20(CAS)/))

**IETF XET protocol** (December 2025): A content-addressable storage protocol using content-defined chunking (CDC) with a rolling hash algorithm. Core requirement: "Given the same input data, any conforming implementation MUST produce identical chunks, hashes, and serialised formats." ([IETF XET draft, December 2025](https://datatracker.ietf.org/doc/html/draft-denis-xet-03))

**Cryptographically Verifiable Intent Chains** (IETF draft, March 2026): The intent chain stores what each step produced (`input_hash` + `output_hash` + `intent_sig`) creating non-repudiable evidence of what each processing step received and produced. Every transformation is labelled as deterministic (rule-based) or non-deterministic (AI-based). For deterministic transforms, the `rule_id` and `rule_hash` are recorded alongside the content hashes — enabling independent verification. ([IETF draft-mw-spice-intent-chain, March 2026](https://datatracker.ietf.org/doc/html/draft-mw-spice-intent-chain))

**Blisp.ai execution model**: Every execution produces an 8-layer hash decomposing provenance into registry, request, morphisms, plans, artifacts, score, selection, and data. Identical grounded requests against identical data produce bit-identical hashes. Sub-hash comparison localises divergence without re-execution. ([blisp.ai](https://www.blisp.ai))

**Merkle DAG for transform provenance** ([novedge.com, January 2026](https://novedge.com/blogs/design-news/tamper-evident-design-histories-cryptographic-provenance-append-only-logs-and-deterministic-rebuilds)):
- Each transform step hashes its inputs and outputs
- Parent hashes commit to child hashes — any change percolates up to a root hash
- Canonical hashing ensures identical content has identical digests regardless of storage path
- Per-step digital signatures bind the actor identity, payload digests, and metadata
- RFC 3161-compliant trusted timestamps for temporal anchoring

### 5.3 File Janitor Pattern: Content-Addressed File Movement

A janitor that moves, archives, or de-labels files can be made fully deterministic and auditable:

1. On ingestion: compute SHA-256/BLAKE3 hash of file content → use as canonical identifier
2. Apply deterministic transform pipeline (NER-based de-labelling, normalisation, date-shifting with consistent offsets)
3. Hash the output content → record `(input_hash, transform_id, output_hash)` in an append-only event log
4. Store output at content-addressed path (`/objects/{output_hash[:2]}/{output_hash}`)
5. Idempotent: running the same file through the same pipeline twice produces the same output hash

The entire transform chain is reproducible and auditable without storing the original sensitive content.

---

## 6. What's New: 2025–2026 Frameworks, Papers, and Industry Shifts

### 6.1 Formal Evidence of Industry Convergence

The industry is converging on the deterministic-foundation split from multiple independent directions:

**From academia:**
- **AgentSpec (ICSE 2026, arXiv:2503.18666)**: First framework to systematically enforce customisable safety constraints on LLM agents at runtime via a DSL evaluated externally to the LLM. The three-tuple (trigger, predicates, enforcement) is now the standard formalism for external constraint specification. ([arxiv.org](https://arxiv.org/abs/2503.18666))
- **Compiled AI (arXiv:2604.05150, April 2026)**: The "compile-once, run-deterministically-forever" paradigm — LLM used only to generate artifacts, execution is zero-token deterministic code. 96% task completion, 57x token reduction. ([arxiv.org](https://arxiv.org/abs/2604.05150))
- **PlanCompiler (arXiv:2604.13092, April 2026)**: Compilation architecture for structured LLM pipelines that separates planning from execution through a typed node registry, static graph validation, and deterministic compilation. 100% first-pass success on constrained task sets. ([arxiv.org](https://arxiv.org/abs/2604.13092))
- **Compiling Deterministic Structure into SLM Harnesses (arXiv:2604.17450, April 2026)**: Semantic Gradient Descent compiles agentic workflows into DAG topologies, system prompts, and deterministic code — 91.3% accuracy on adversarial benchmarks with compiled workflows. ([arxiv.org](https://arxiv.org/abs/2604.17450))
- **Agent Behavioral Contracts (arXiv:2602.22302, February 2026)**: Formal Design-by-Contract for agents — Preconditions, Invariants, Governance policies, Recovery mechanisms as first-class, runtime-enforceable components. ([arxiv.org](https://arxiv.org/html/2602.22302v1))
- **Zero-Trust IAM for Agentic AI (arXiv:2505.19301)**: Comprehensive framework using DIDs and Verifiable Credentials for dynamic authentication and authorisation of AI agents with Zero-Knowledge Proofs for capability-based discovery. ([emergentmind.com](https://www.emergentmind.com/papers/2505.19301))

**From major cloud vendors:**
- **Google ADK** (April 2025): Ships `SequentialAgent`, `ParallelAgent`, `LoopAgent` explicitly documented as "not powered by an LLM, and is thus deterministic in how it executes" — Google explicitly baking the deterministic/probabilistic split into its SDK at the API level. ([YouTube, April 2026](https://www.youtube.com/watch?v=QmW91KCKNj8))
- **AWS Bedrock AgentCore** (2026): Uses Cedar for all tool authorisation — deterministic enforcement at the gateway boundary outside agent code.
- **Azure Durable Task Extension** (public preview, late 2025): Durable execution for Microsoft Agent Framework, multi-day human-in-loop pauses, auto-scaling to zero.
- **Anthropic's minimal footprint principle**: Claude agents should "request only the permissions they need, prefer reversible actions over irreversible ones, and err toward doing less and confirming when uncertain." ([Anthropic, March 2026](https://www.mindstudio.ai/blog/anthropic-vs-openai-vs-google-agent-strategy))

**From the Futurum Agent Control Plane Framework (April 2026):**
A five-layer reference architecture for production AI agents, establishing as its foundational principle: "agent governability requires separation of deterministic control from probabilistic reasoning." ([Futurum, April 2026](https://futurumgroup.com/press-release/futurum-agent-control-plane-framework-a-reference-model-for-production-ai-agents/))

**From AGCP (AI Governance Control Plane):**
An emerging open specification for deterministic runtime governance architecture. The core requirement: "Determinism. Same input, same configuration, same verdict. Every time. On any hardware. No confidence scores. No probability distributions. A binary or ternary resolution that a regulator can reproduce independently." ([AGCP.ai](https://agcp.ai/framework/))

**From CASA (Constitutional AI Safety Architecture):**
A deterministic, source-agnostic, pre-execution control plane for structured execution requests. "It contains no language model, no neural network, no probabilistic element of any kind. It does not interpret content. It does not make secondary model calls." ([LinkedIn/CASA](https://media.licdn.com/dms/document/media/v2/D561FAQFZNfEvSh5A1g/feedshare-document-pdf-analyzed/B56ZyCUI5VKUAY-/0/1771712844699))

### 6.2 Who Is Advocating This Pattern

The "deterministic control plane / probabilistic agents" split now has explicit advocates across:

| Advocate | Position |
|---|---|
| **Temporal (Maxim Fateev, CEO)** | "Durable execution is an infrastructure primitive, not an application framework. It sits in the infrastructure layer and doesn't care whether you're building an AI agent or a payment pipeline." ([WorkOS interview, April 2026](https://workos.com/blog/maxim-fateev-temporal-durable-execution-ai-agents)) |
| **Google Cloud CTO office** | "This shifts the reliability burden from the probabilistic LLM to deterministic system design, where it belongs." ([Google Cloud, December 2025](https://cloud.google.com/transform/ai-grew-up-and-got-a-job-lessons-from-2025-on-agents-and-trust)) |
| **CNCF / Inngest** | Durable execution "crossed into the early majority in 2025" driven by AI agent infrastructure needs. ([Inngest, February 2026](https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents)) |
| **Praetorian** | Formal publication of the "Thin Agent / Fat Platform" architecture — LLM as nondeterministic kernel process wrapped in deterministic runtime. ([Praetorian, February 2026](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)) |
| **NHIMG (NHI Management Group)** | "Identity governance will become the control plane for agentic AI." Zero standing privilege is the minimum viable governance model. ([NHIMG, May 2026](https://nhimg.org/articles/ai-agent-identity-risk-is-outpacing-zero-trust-controls/)) |
| **Gartner** | Predicts 40%+ of agentic AI projects will be cancelled by end of 2027 primarily due to inadequate risk controls and unclear value — validating the need for deterministic governance. ([via tianpan.co, April 2026](https://tianpan.co/blog/2026-04-20-workflow-engines-beat-llm-agents)) |

---

## 7. Recommended Deterministic Foundation Stack

Based on the research, the following is the recommended stack for Amplified Partners' multi-agent dev environment. Each layer is deterministic — same inputs, same outputs, no LLM in the loop.

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT CELLS (Non-Deterministic)              │
│  Thin LLM agents (<150 lines), WASM capability-sandboxed,       │
│  stateless, no persistent credentials, scoped per job ticket     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Activities (tool calls)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              DETERMINISTIC FOUNDATION (Control Plane)           │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  TEMPORAL   │  │  ACCESS      │  │  DATA NEUTRALISER      │ │
│  │  (Workflow  │  │  BROKER      │  │                        │ │
│  │  Engine)    │  │  (JIT Creds) │  │  deterministic NER +   │ │
│  │             │  │              │  │  hash tokenisation +   │ │
│  │ Workflows:  │  │ OPA/Cedar    │  │  content-addressed     │ │
│  │ deterministic│  │ policy eval  │  │  output hashing        │ │
│  │             │  │              │  │                        │ │
│  │ Activities: │  │ Vault JIT    │  │  input_hash →          │ │
│  │ LLM calls   │  │ token minting│  │  transform → output_   │ │
│  │ (non-det)   │  │              │  │  hash in event log     │ │
│  └─────────────┘  └──────────────┘  └────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PROVISIONER / JANITOR                                   │  │
│  │  Pure deterministic code: file moves, path resolution,  │  │
│  │  workspace creation/teardown, idempotent via job-ticket  │  │
│  │  ID as idempotency key                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ROUTER                                                  │  │
│  │  Pure Python/Go conditional edges (LangGraph-style or    │  │
│  │  Temporal child workflows). Routes based on job-ticket   │  │
│  │  type, NOT LLM decision. Map of ticket_type → workflow.  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Layer-by-Layer Specifications

**1. Orchestration Engine: Temporal**
- All orchestration logic in Temporal Workflow code (must be deterministic — no LLM calls inline)
- All LLM calls, tool executions, API requests wrapped as Temporal Activities
- Idempotency keys derived from `(workflow_id, activity_name, attempt)` — stable across replays
- Saga pattern with pre-registered compensating activities for reversible actions
- Human-in-the-loop pauses via Temporal Signals (workflow suspends, waits for approval signal)
- Event history provides full audit trail by default

**2. Access Broker: JIT Credentials via Vault + OPA/Cedar**
- No agent cell ever holds a persistent credential
- Job ticket presented to broker → OPA/Cedar policy evaluated deterministically → if allowed, Vault mints short-lived scoped token (TTL: seconds to minutes)
- Token granted to Temporal Activity scope, not to the agent directly
- Token revoked / expired automatically after Activity completes
- Cedar policy rules: `principal` = job ticket identity, `action` = tool name, `resource` = scoped resource, `conditions` = job ticket constraints
- Scope drift detection: if Activity requests a resource not in the job ticket scope, Cedar returns `deny` with structured reason, Temporal Activity fails with structured error, Saga compensation triggered

**3. Data Neutraliser: Deterministic Token Pipeline**
- Input enters neutraliser before reaching any agent cell
- Deterministic NER model (locally-hosted, versioned, pinned) identifies sensitive entities
- Cryptographic tokenisation: `token = HMAC-SHA256(entity_value, classified_salt, entity_type)` — same entity always same token, cross-document consistency preserved
- Output content-hashed: `output_hash = SHA256(neutralised_content)` → stored in append-only event log as `(input_hash, pipeline_version, output_hash, timestamp)`
- Re-identification: server-side only, RBAC-gated, every operation logged
- LLM never sees original labels; works on tokenised form only

**4. Provisioner and Janitor: Pure Deterministic Code**
- Workspace provisioning: given `job_ticket_id`, compute deterministic workspace path, create directories, mount scoped filesystem namespace
- Janitor: triggered by Temporal timer activities or file-system events, applies deterministic rules (file age, content-type classification, completion status) to move/archive/delete — no LLM decision
- All operations idempotent: running the provisioner twice with the same job ticket produces the same state
- Content-addressed archival: files moved by janitor hashed and stored at content-addressed paths; event log records `(job_ticket_id, action, file_hash, destination)`

**5. Router: Deterministic Dispatch Map**
```python
ROUTING_MAP = {
    "code_review":    code_review_workflow,
    "data_pipeline":  data_pipeline_workflow,
    "security_scan":  security_scan_workflow,
    # ...
}

def route(job_ticket: JobTicket) -> Workflow:
    workflow_fn = ROUTING_MAP.get(job_ticket.type)
    if workflow_fn is None:
        raise ValueError(f"Unknown job type: {job_ticket.type}")
    return workflow_fn
```
The router is a pure function over the job ticket. No LLM decision. No probabilistic routing. If a job type is not in the map, it fails fast with a structured error.

**6. Agent Cells: WASM-Isolated, Thin**
- Each agent cell instantiated as a WASM component with capabilities granted at instantiation time only (filesystem namespace scoped to workspace, HTTP access to explicitly allowlisted hosts only, no ambient host access)
- Thin agent body <150 lines; skills/tools loaded JIT from a versioned skill registry
- Credentials injected per-Activity via the Vault JIT broker — never stored in agent state
- Cell cannot reach other cells' workspaces, cannot modify the control plane, cannot acquire credentials beyond what the current Activity scope permits

### Technology Selections

| Component | Recommended | Alternative |
|---|---|---|
| Orchestration engine | **Temporal** (already in use) | Restate (lighter infra), DBOS (Postgres-only) |
| Policy engine | **OPA** for RBAC/ABAC, **Cedar** for tool-level enforcement | OPA alone (Cedar adds formal verification) |
| JIT credential broker | **HashiCorp Vault** + JWT token exchange | AWS IAM with short-lived roles |
| Workflow definition | **Temporal Workflows** + Python/TypeScript SDK | LangGraph (for graph-shaped flows) |
| Runtime constraint enforcement | **AgentSpec DSL** or **Cedar hooks** | Custom pre-execution gate code |
| Agent cell isolation | **WASM/Wasmtime** for bounded tools | Firecracker microVM for arbitrary code |
| Data neutralisation | **spaCy/Presidio** (locally-hosted NER) | John Snow Labs Healthcare NLP (medical domain) |
| Content addressing | **SHA-256 / BLAKE3** + append-only Postgres event log | IPFS CAS for distributed provenance |
| Audit log | **Append-only Postgres table** with immutable rows | OpenTelemetry traces → Loki/S3 |

### Key Invariants to Enforce

1. **No LLM call inside a Temporal Workflow function** — only inside Activities
2. **No standing credentials in agent cells** — all credentials injected via JIT broker per-Activity
3. **All routing decisions are pure functions over job tickets** — never LLM decisions
4. **All data entering agent cells has passed through the deterministic neutraliser** — neutraliser output hash logged before handoff
5. **Idempotency keys for all side-effecting Activities derived from `(workflow_id, activity_name)`** — never random UUIDs
6. **Cedar/OPA policy evaluation happens outside agent code** — at the gateway/broker boundary, before any tool execution

---

*Research compiled from 40+ primary sources, June 2026. All URLs cited inline. Key sources:*
- *[Zylos Research — Deterministic Governance Kernels (March 2026)](https://zylos.ai/research/2026-03-11-deterministic-governance-kernels-agent-runtimes)*
- *[Zylos Research — Durable Execution Patterns (February 2026)](https://zylos.ai/research/2026-02-17-durable-execution-ai-agents/)*
- *[Praetorian — Deterministic AI Orchestration (February 2026)](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)*
- *[AgentSpec — ICSE 2026 (arXiv:2503.18666)](https://arxiv.org/abs/2503.18666)*
- *[Compiled AI — arXiv:2604.05150 (April 2026)](https://arxiv.org/abs/2604.05150)*
- *[Temporal Blog — Dynamic AI Agents (November 2025)](https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal)*
- *[NHIMG — AI Agent Identity Risk (May 2026)](https://nhimg.org/articles/ai-agent-identity-risk-is-outpacing-zero-trust-controls/)*
- *[Codilime — OPA for AI Agents (April 2026)](https://codilime.com/blog/why-use-open-policy-agent-for-your-ai-agents/)*
- *[blog.sondera.ai — Cedar Policy Language for Coding Agents (March 2026)](https://blog.sondera.ai/p/hooking-coding-agents-with-the-cedar)*
- *[Zylos Research — WASM Sandboxing (March 2026)](https://zylos.ai/research/2026-03-12-wasm-sandboxing-ai-agent-runtime-isolation)*
- *[HashiCorp Vault — AI Agent Identity Pattern (September 2025)](https://developer.hashicorp.com/validated-patterns/vault/ai-agent-identity-with-hashicorp-vault)*
- *[tianpan.co — Workflow Engines Beat LLM Agents (April 2026)](https://tianpan.co/blog/2026-04-20-workflow-engines-beat-llm-agents)*
