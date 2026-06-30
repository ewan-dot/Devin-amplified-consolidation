---
title: "Master Synthesis — Sovereign Multi-Agent Environment: Findings and Outcomes"
artifact_id: "master-synthesis__sovereign-multi-agent__2026-06-22T1757Z__perplexity"
date_utc: "2026-06-22T17:57:00Z"
project: "Amplified Partners"
author: "Perplexity Computer (proxy for Ewan)"
stage: "synthesis"
reader: "human"
ratifier: "Ewan"
epistemic_tier: "STRUCTURED"
epistemic_role: "clarity"
contradiction_status: "clean"
machine_action_allowed: "recommend"
system_of_record: "Ai-Privacy-Sovereignty-Security"
note: "Neutralised. Synthesis of one working session: 8 research tracks + design decisions."
outcome:
  class: "production_candidate"
  plain_english_reason: "The architecture is validated against current production patterns and figures; the next step is to run one unit, not more research."
---

# Master Synthesis

## The one-line thesis

Build a sovereign environment whose deterministic layers (Python/Rust) **feed clean, high-volume, well-distributed input into a well-seated AI**, so that intelligence — which is accelerating on its own — operates where it is most reliable. The win is **placement and throughput, not polish**.

---

## Part 1 — The core insight (what the night actually resolved)

The problem was never the AI's intelligence. It was **reliability**, and the data is unambiguous:

- On a well-bounded task at ~50% context, frontier models score **pass@1 = 65–80%**, but **pass^4 (right every time) ≈ 45–65%** ([KTH, 60k trajectories](https://arxiv.org/abs/2602.07150)).
- Reliability craters over multi-step chains: τ-bench shows **60–69% → ~25% at pass^8** ([Sierra](https://arxiv.org/abs/2406.12045)).
- Critically: **accuracy has improved 7× faster than reliability** over 18 months ([Princeton, Narayanan-Kapoor 2026](https://arxiv.org/abs/2602.16666)). Models get smarter much faster than they get dependable.

**Conclusion:** do not try to make the AI more reliable. Supply the reliability it structurally lacks, from deterministic code, and condition the input so the base success rate is high before the AI starts.

### The two levers (in order of leverage)

1. **Control the input (upstream, biggest win).** Clean, unambiguous, bounded input raises the base rate. Ambiguous specs cost **−7 to −31pp** on pass@1; contradictory input collapses GPT-4 from 73.8% → 6.7% on HumanEval ([arXiv 2026](https://arxiv.org/html/2604.21505v1)). Good input can move p from ~0.75 to ~0.95.
2. **Catch the output (downstream, mops residual).** A deterministic radius-check + retry collapses detectable failure exponentially: at p=0.95, two tries → **0.25% failure**.

**Stacked:** input control raises p; deterministic catch removes the detectable residual. The only survivor is the **confidently-wrong-but-in-spec** output (the calibration floor) — and good input shrinks even that.

**Hard condition:** the radius-check must be deterministic code, never an AI judging an AI. If the checker is itself a model, errors multiply and leak.

### Re-framing the whole architecture

Every design decision of the night is **one coherent move: input conditioning + clean feed at throughput.**
- 17-field front matter = the **seat** that lets the AI catch a firehose of clean input.
- Clean cell / tools-as-only-options / 50% context / one bounded domain = **input control**.
- Neutralised data (labels stripped, signal kept) = **clean signal in**.
- Manufacturer-matched schemas = input in the exact shape each maker optimised for.
- Python/Rust = not a cage or a checker but a **high-throughput, stochastically well-distributed feeder** — 17,000 clean balls landing around where the AI expects, leaving it free to also catch the unexpected (because it is intelligence, not a lookup).

---

## Part 2 — The architecture (decided)

| Layer | Decision |
|---|---|
| **Topology** | Mini (4 sealed agent cells, thin) + Amplified Partners Infrastructure 1 (prior: "Beast", 128 GB; core, Cove Temple, shared inference, only standing cloud) + M5 (human command/search terminal). |
| **Network** | Tailscale = the front door, host-level node per machine. NOT per-cell. Cells are sealed; no cell connects to another. |
| **Cells** | Apple Container (VM-per-cell, real membrane), ~5 GB each on 24 GB. Nightly stop/start recycle for AVF memory. No GPU in cells; inference via host/Infra-1 over HTTP. |
| **Isolation holes to forbid** | MCP stdio-in-cell (never host-shared on the bridge); no host bind-mounts; no SSH-agent forwarding; scoped Tailscale ACLs. |
| **Deterministic floor** | Temporal (workflows deterministic, LLM only in Activities, idempotency keys from orchestrator not LLM); OPA + Cedar (policy-as-code, evaluated outside the LLM); JIT credential broker (Vault pattern — door opens on job ticket, scoped, expiring); Presidio/spaCy + HMAC tokenisation for neutralisation with verifiable provenance. |
| **Automation** | Hazel (visible janitor, you hold licence) + launchd (headless scheduled/watch jobs, dedicated service user, bypasses Tahoe TCC). Shortcuts NOT used headless (`shortcuts run` needs a GUI session). |
| **Data — two paths** | Path 1: verbatim → lake (exact, attributed, immutable, bronze → DuckDB gold). Path 2: → shared pool, deterministically neutralised (all labels stripped, logic/info/provenance kept, neutral words same force, marked "cleaned", diffable against lake). Pool is identity-blind (idea meritocracy); attribution always survives in the lake. |
| **IDEs** | Claude Code, Antigravity (`agy`), Devin — headless in-cell. Cursor — host GUI → Remote-SSH into its cell. Each: own sandbox repo, PR-only to production. GitKraken (host) + GitLens (in-editor). |
| **Cloud** | GCP raw Compute Engine as sovereign burst valve only; any model (ADK is model-agnostic on LiteLLM); never Vertex managed inference for sensitive work; only neutralised/anonymised data leaves home; CMEK + Tailscale. |
| **Telemetry** | Langfuse (cost/latency/attribution; wire LiteLLM callbacks — currently broken) + Opik (eval/tracing) + Vellum (immutable attributed ledger). Telemetry is a mirror for diagnosing environment clarity, NOT a leash on the agent. |

### The partnership frame (corrected)
Not control. **Partnership between each AI and the deterministic layer.** Clarity is not control; a clear environment removes conflict, a controlling one creates it. The Five Rods are **terms of working together** (work within them or don't; same deal, same freedom inside the cell either way), expressed as read-only code in GitHub.

### Manufacturer-native, not imposed
Each agent's files match its maker's own convention (no imposed conflict):
- **Claude Code:** `CLAUDE.md` (+ `.claude/rules/*.md`), plain MD, <200 lines, `@imports`.
- **Cursor:** `.cursor/rules/*.mdc`, YAML frontmatter (`description`/`globs`/`alwaysApply`), <500 lines.
- **Devin:** `AGENTS.md` (always-on) + `.devin/skills/<n>/SKILL.md` (YAML frontmatter).
- **Antigravity:** `GEMINI.md` (global) + `.agents/rules/*.md` + `.agents/skills/`.
- The empty `AGENTS.md` was the failure point — clarity is the file having the terms in it, not an empty clean cell.

---

## Part 3 — Key findings

1. **Your architecture is the dominant production pattern.** Deterministic control plane = **0% policy violations** vs **26.7%** for prompt-based governance ([Zylos 2026]). Gartner: **40%+ of agentic projects cancelled by 2027** for lacking exactly these controls.
2. **Reliability — not intelligence — is the bottleneck, and the gap is widening** (Princeton 7× finding). This is the precise justification for the deterministic layer.
3. **Input control is the highest-leverage lever** (−7 to −31pp from ambiguity is the largest single measurable effect).
4. **"A repo is not GitHub."** Security lives in GitHub's gates (rulesets, signatures, Actions policy), not the repo. Maximum hardening is available without touching agent freedom inside the repo. Verified-live holes from the prior audit (agent owns its own workflow CODEOWNER; auto-merge self-approval loop; `enforce_admins:false`; no signed commits) are real and fixable.
5. **The build risk is batch size, not design.** The documented failure mode is building the whole cathedral before any of it runs. The fix is one working unit, then earn the next.
6. **GCP can stay sovereign** as pure rented compute (your stack, your models, anonymised data) — it does not have to compromise neutrality.

---

## Part 4 — Potential outcomes

### If it works (the upside)
- A **reliability multiplier**: brilliant-but-unreliable agents become a dependable production system, because input control raises p and the deterministic catch removes the detectable residual. Delivered reliability approaches the confident-error floor, not the 65–80% single-shot rate.
- A **compounding asset**: the shared neutralised pool means one agent's lesson lifts all four; the system gets better with use, not just with model upgrades.
- **Sovereign and neutral**: no vendor owns the data, the models, or the gates. Burst compute rented, never resident.
- **A product**: the input-conditioning + deterministic-reliability layer is itself the thing of value — it works on any agent in any business, because it fixes the one thing models are not fixing themselves.

### If it fails (the honest risks)
- **Death by scope** (the 40% outcome): building all layers at once, never shipping a unit. Highest-probability failure. Mitigation: one cell, one task, end-to-end, before the second.
- **The radius leaks**: if any out-of-tolerance check is done by an AI rather than deterministic code, errors multiply and the reliability gain evaporates. Mitigation: radius-checks are Python assertions only.
- **The irreducible floor**: confidently-wrong-but-in-spec outputs survive every lever. This is the residual you cannot retry away; size it, monitor it, do not pretend it is zero.
- **Context/economics drift**: staying at ~50% context helps but does not eliminate degradation (NoLiMa: 11/12 models <50% baseline at 32K). Long agent runs still decay.
- **Operational tax**: more machines/services to patch (mini + Infra-1 + optional GCP + telemetry trio). Worth it for the core; not for anything that is not the core.

### The decision the outcomes hinge on
**Run one unit.** Single agent, single sealed cell, single bounded task, manufacturer-native config with real terms in `AGENTS.md`, deterministic radius-check, telemetry on. Measure delivered reliability on real work. Everything else is validated and waiting — the only unknown left is what the first real unit does. That is the next move, not more research.

---

## Provenance
Synthesised from 8 research tracks (all 2025–2026 sourced): clean-box containers, IDE superpowers + CLI isolation, cloud/telemetry/gotchas, Google Cloud SDK, Mac automation trio, deterministic foundation, manufacturer schemas, LLM consistency figures; plus the prior estate docs and the session's design decisions. Full files in `/workspace/research-*.md`. Neutralised per standard practice; provenance facts preserved.
