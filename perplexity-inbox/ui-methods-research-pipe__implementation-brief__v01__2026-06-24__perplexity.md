---
title: "UI-Methods Research Pipe — Implementation Brief"
document_type: "implementation_brief"
artifact_id: "2026-06-24T10-30-00Z__amplified__ui-methods-research-pipe__brief__v01"
date_utc: "2026-06-24T10:30:00Z"
project: "Amplified Partners"
author: "Perplexity Computer (AI_PARTNER_PROXY)"
stage: "decision"
audience: "M5 local AIs + Ewan"
epistemic_tier: "STRUCTURED"
tier_reason: "Prompt design from a verbatim read of Every's agent files + house skills; reproducible structure, not fitted from data. Unit-of-AI assumption is STRUCTURED per Ewan, not proven."
attribution: "Prompt shape mirrors EveryInc/compound-engineering-plugin. Method targets from the UI-human-side baton (this thread). Discipline from expert-partner-brief + min-rule + amplified-research-yaml-frontmatter."
system_of_record: "local_workspace -> M5 implementation"
machine_action_allowed: "execute_with_gate"
ratifier: "Ewan"
---

# UI-Methods Research Pipe — what to run

## Goal
Recover the **logic** (why it works on humans) and **methodology** (how to run it) for nine human-side-UI methods, so the mechanisms can later feed PUDDING onto wireframes. Each method = one bounded domain = one unit of AI.

## What's in this bundle
`ui-methods-research-pipe/` contains the run-ready prompts:
- `orchestrator-and-subagents.md` — the orchestrator prompt + nine sub-agent prompts (shared skeleton + per-method cards), in Every's agent format.
- `human-doc.md` — the readable rationale and the design reconciliation (personas: expert-role IN, backstory OUT).

## How to implement (M5)
1. Instantiate the orchestrator (`ui-methods-orchestrator`).
2. Assemble each sub-agent = shared skeleton + its method card. Nine agents.
3. **Dispatch all nine in parallel.** No cross-dependency; concurrency is strictly faster. If concurrency is capped, order: calm-technology → cognitive-load-theory → distributed-cognition → the rest → heuristic-evaluation (capped) last.
4. Each sub-agent reads PRIMARY sources, returns a YAML-frontmatter doc with the mandatory `Logic` + `Methodology` sections, tiered per min-rule (STRUCTURED on primary read, INTUITED on secondary-only).
5. Orchestrator reconciles into one index; tier = MIN across contributors. Do NOT homogenise bodies.
6. **THEN PUDDING** on the returned mechanisms — not before; PUDDING on summaries is weak feedstock.

## Decisions already resolved (no input needed)
- All nine in parallel — resolved.
- PUDDING after collection — resolved (sequenced in the orchestrator).
- Heuristic Evaluation capped, must return its own critique — resolved.

## Gate
None binding. This is a research run (Tier A research → Tier A inbox drop). The only act-out is the local implementation under your watchers; the PUDDING-onto-wireframes step and any Beast ingestion remain on the Mac, through the pipe.

[CLOSURE] branch=ACTION | proxy=1 logged (inbox drop as AI_PARTNER_PROXY) | gates=none | inbox=ui-methods-research-pipe__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
