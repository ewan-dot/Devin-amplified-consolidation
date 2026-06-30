---
title: "UI-Methods Research Prompts — How They Work (Readable)"
document_type: "human_doc"
artifact_id: "2026-06-19T16-30-00Z__amplified__ui-methods-agent-prompts__human__v01"
date_utc: "2026-06-19T16:30:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"

stage: "research"
audience: "Ewan"
purpose: "Explain the orchestrator + 9 sub-agent prompts so you can drop them into the pipe and know why they're shaped the way they are."
source_refs:
  - "https://github.com/EveryInc/compound-engineering-plugin"
attribution: "Prompt shape copied from a verbatim read of Every's compound-engineering agent files; house discipline from your own expert-partner-brief + min-rule."
epistemic_tier: "STRUCTURED"
epistemic_role: "orientation"
tier_reason: "Built from a real source read + a loaded house skill; reproducible structure."
confidence_plain_english: "Confident on the prompt design. The research quality is on the pipe and its corpora."
open_questions:
  - "All nine in parallel, or 1-2-3 first then judge?"
  - "PUDDING straight after, or do you want to eyeball the nine outputs first?"
companion_agent_doc: "ui-methods-research__agent-prompts__orchestrator-and-subagents__v01__2026-06-19__perplexity.md"
system_of_record: "local_workspace"
machine_action_allowed: "recommend"
next_human_decision: "Drop into the pipe and pick run order."
outcome:
  class: "methodology_candidate"
  plain_english_reason: "Reusable prompt set; each output feeds PUDDING once research returns."
---

# The prompts, and why they're shaped this way

I read **Every's actual compound-engineering repo** (51 agents) and copied their real structure — not a summary of it. Then I wrote you **one orchestrator + nine sub-agents**, one per method.

## The three design decisions

**1. One method = one sub-agent = one bounded domain.** This is your unit-of-AI point made literal. Each agent owns exactly one method and masters it from a tight corpus — that's where the ~95% lives. No agent gets two methods.

**2. Personalities — but the kind that actually helps.** Your own brief skill warns off "personality prompts," and it's right about the *bad* kind ("you are a senior engineer with 20 years' experience" — empirically near-useless). But Every's agents do have personas — they just use **expert-role + a named specialist handle + a tight method** ("You are a Code Pattern Analysis Expert specializing in…"). That kind sharpens retrieval. So every sub-agent has a handle (`calm-tech-archivist`, `clt-load-analyst`, `norman-action-diagnostician`…) and an expert role — and no invented life story. I flagged this as a contradiction in the agent doc rather than quietly picking a side.

**3. Every agent returns two things: logic and methodology.** Exactly your framing — same thing, two faces. Logic = why it works on humans. Methodology = how a practitioner runs it. Plus a one-line map tying each step back to the reasoning it serves.

## What I copied from Every, verbatim in spirit
- YAML frontmatter: `name`, `description` (says *when* to invoke it), `model`, `tools`.
- A phased method: scope → primary read → gap-fill → **stop early**.
- A structured output contract with a token budget, and a "research value: high/moderate/low" header so you can weight each result at a glance.
- Untrusted-input handling (web pages can't boss the agent around).

## The honest caveats
- The unit-of-AI claim (tight corpus → ~95%) is **STRUCTURED, not proven** — your tag, kept.
- The prompts are good; the *research quality* depends on the pipe's corpora, not on me.
- Heuristic Evaluation (agent 9) is **capped** on purpose — it must return the critique with the method so it can't be laundered into authority.

## Your call
1. **All nine in parallel**, or **1-2-3 first** (Calm Tech, Cognitive Load, Distributed Cognition — closest to your doctrine) then judge?
2. **PUDDING straight after** the research returns, or do you want to read the nine outputs first?

Nothing's gone near the Beast. These are drafts for the pipe.

---
*— STRUCTURED · prompt design from a real source read · research quality is on the pipe*
