---
title: "Token Reduction — What Actually Cuts Spend (human brief)"
document_type: "readable_research_conclusion"
artifact_id: "token-reduction-prior-art__human-brief__v01__2026-06-23__perplexity"
date_utc: "2026-06-23T19:35:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"
stage: "research"
audience: "Ewan"
purpose: "Plain-English read on the levers that reduce token spend across IDEs, consumer UIs, CLI-vs-MCP, and AI habits."
source_refs: ["research_cli_vs_mcp.md", "research_ide_controls.md", "research_context_habits.md", "companion agent doc same date"]
attribution: "External numbers cited in the agent doc with URLs. Synthesis by Perplexity Computer."
epistemic_tier: "STRUCTURED"
epistemic_role: "evidence_map"
tier_reason: "Cited official/benchmark numbers organised into a lever map; estate savings not yet measured."
confidence_plain_english: "Strong on the mechanism and the published magnitudes. Not yet measured on our own estate."
open_questions:
  - "Has Anthropic's Pool 1/Pool 2 split actually shipped? Research suggests it may be paused."
  - "Can we get the primary source for the 62% re-sent-context figure before citing it anywhere external?"
companion_agent_doc: "token-reduction-prior-art__research-conclusion__agent-doc__v01__2026-06-23__perplexity"
system_of_record: "Drive"
machine_action_allowed: "recommend"
next_human_decision: "Approve folding these levers + numbers into the estate spec §4 and starting the per-IDE config bake."
outcome:
  class: "methodology_candidate"
  plain_english_reason: "Gives us a reusable, cited menu of spend levers to bake into config and into the spec."
---

# Token Reduction — the short version

Your instinct is right: **CLI is a lot cheaper than MCP** for the simple read jobs — but it's one case of a single underlying rule that governs all of this:

> **Stop sending the model tokens it doesn't need this turn.**

Everything below is a way to do that.

## The four levers, ranked by payoff

1. **Caching (biggest).** Keep the prompt's top section byte-identical every time and the provider charges 90% less for it on repeat (Anthropic/Google), 50–75% (OpenAI), up to 98% (DeepSeek). Change one character at the top and you lose it. On Anthropic, batch + cache **stack** to ~95% off; on OpenAI and Google they don't.

2. **CLI-over-MCP for read-only doors.** MCP shoves every connected tool's full manual into the model on *every* turn, used or not — Anthropic measured 134,000 tokens of that in their own setup. A controlled benchmark found MCP **32× more expensive** on a simple task and **17× at scale**, and it failed 28% of the time vs CLI's 0%. The catch: on long multi-step jobs, lots of little CLI calls can cost *more* than MCP, and MCP is the right call when you're acting for *other people's* users (it has proper per-user login and audit). So: CLI for our own quick reads; code-execution pattern for big APIs; MCP only where caching + auth earn it.

3. **Cheap model for mechanical work, frontier only for judgment.** Anthropic's own setup (Opus plans, Sonnet sub-agents) beat solo-Opus by 90%. Route the boring work to Haiku or the local Mac mini ($0 tokens), keep Opus for thinking. This is the router in the estate spec.

4. **Less context in, less output out.** Compaction (~58% cut, Anthropic's own numbers), repo-maps instead of whole files (~1K tokens for the whole structure), `mdfind`/ripgrep to pre-narrow before the model sees anything, and tight output (output tokens cost ~5× input).

## Per-tool knobs worth baking in
- **Cursor:** Auto mode (not Max Mode — Max ~5×s your context), pin the model, ignore files, rules scoped by file-glob not "always on."
- **Claude Code:** capping thinking tokens is the single biggest one-knob win (−30–40%); plus `/compact` inside the 5-min cache window, `/clear` between tasks, Haiku sub-agents, CLAUDE.md under 200 lines.
- **Aider:** the repo-map and prompt caching flags do most of the work.
- **Copilot/Windsurf/Cline:** pick 0×/0-credit models where they exist; turn off the expensive defaults.

## Two honesty flags
- The **"62% of an agentic bill is re-sent context"** number is good for our own thinking but I couldn't pin the primary academic source — don't quote it to anyone external yet.
- Anthropic's **Pool 1/Pool 2 pricing split** (the thing the spec warns about) looks like it may have been **paused before shipping** — I'll confirm before we rely on that warning.

## What I'd do next
Fold these into the estate spec's lever section with the real citations, then write the actual config files per IDE. Both are ready to go on your word.
