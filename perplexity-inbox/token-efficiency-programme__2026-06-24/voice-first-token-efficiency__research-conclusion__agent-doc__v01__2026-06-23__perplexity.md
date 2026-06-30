---
title: "Voice-First, Token-Efficient Discovery Loop — keep the talking, cut the spend"
document_type: "research_conclusion"
artifact_id: "voice-first-token-efficiency__research-conclusion__agent-doc__v01__2026-06-23__perplexity"
date_utc: "2026-06-23T20:35:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"
stage: "synthesis"
objective: "Answer: how to keep Ewan's voice-first, talk-to-discover style while reducing token spend AND staying organisationally efficient. Ground the answer in Amplified's existing Epistemic Pipe doctrine; attach external prior art with numbers."
reader: "agent"
source_refs:
  - "local-mac: /Users/ewansair/ingestion-to-research-pipe/clean-build/02_build/scripts/dedup-output/METHODOLOGY-SYNTHESIS.md (Part XVI Epistemic Pipe '17-and-3'; Appendix G Transcript enrichment; XVII Portable Lens) — updated 2026-06-23"
  - "memory: notes/preferences/communication/transcription.md"
  - "memory: notes/work/Amplified/research_pipe.md (Gatekeeper + Porch Watcher + curator, PUDDING)"
  - "memory: notes/projects/voice_transcript_briefing_library.md"
  - "skills: transcription-prompt-optimiser, neutral-research-brief, content-harvester, thread-extraction, min-rule"
  - "https://arxiv.org/abs/2310.05736"  # LLMLingua
  - "https://arxiv.org/abs/2310.06839"  # LongLLMLingua
  - "https://arxiv.org/abs/2403.12968"  # LLMLingua-2
  - "https://arxiv.org/abs/2406.18665"  # RouteLLM
  - "https://arxiv.org/abs/2407.16833"  # RAG vs long-context
  - "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
  - "local: research_voice_first_efficiency.md"
origin_type: "agent_synthesis"
attribution: "External claims cited inline with URL. Internal architecture attributed to Amplified (Ewan + AI partners, Methodology Synthesis). Cost framing and loop design by Perplexity Computer."
epistemic_tier: "STRUCTURED"
tier_reason: "External pattern numbers are MEASURED at source (papers/benchmarks); the mapping onto Ewan's pipe is a STRUCTURED design; estate-specific savings INTUITED until the cost log runs."
epistemic_role: "clarity"
effective_tier_rule: "min-rule"
preconditions:
  - "Local STT available on a Mac (whisper.cpp / MacWhisper) for $0-token capture."
  - "Research pipe (Gatekeeper + Porch Watcher + curator) reachable; ResearchQuery gates enforced."
valid_until: "2026-09-23"
claim_scope: "Workflow design + published magnitudes; not estate-measured savings."
contradiction_status: "clean"
known_contradictions:
  - "Exploratory voice chat is inherently cache-hostile; caching helps the convergent phase, not the divergent one. Both true — resolved by phase-splitting."
machine_action_allowed: "recommend"
system_of_record: "Drive (human) + Beast/Brain via pipe (doctrine); this draft = local_workspace"
ratifier: "Ewan"
next_action: "Approve the 5-step loop; decide which steps to wire first (local STT capture + cheap cleanup are the fastest wins)."
companion_human_doc: "voice-first-token-efficiency__human-brief (same date)"
outcome_routing:
  outcome_class: "methodology_candidate"
  outcome_reason: "Defines a reusable divergent/convergent cost-tiered loop that fits the existing Epistemic Pipe and the estate router."
  required_next_action: "Bake Steps 1-2 (local STT + cheap cleanup) as the front of the pipe; route Step 4 through the estate credit-first router."
  research_needed: false
  tangent_refs: ["Portable Lens (Part XVII) as a parallel-agent convergent option"]
  methodology_refs: ["divergent-convergent cost tiering", "prompt distillation gate", "context offloading to pipe/Brain"]
---

# Voice-First, Token-Efficient Discovery Loop

TIER: STRUCTURED · external pattern numbers MEASURED-at-source · estate savings INTUITED until cost log runs
PROVENANCE: your own Methodology Synthesis (Part XVI Epistemic Pipe, Appendix G) + external prior art (`research_voice_first_efficiency.md`). The loop is not new — it is your Epistemic Pipe, costed.
GOAL-LINK: your talking is the discovery engine that produced the Pudding Technique (Appendix G, Transcript 1200). Protecting it while cutting spend keeps the engine running cheaper — directly serves "get the business going."

## The one idea

**Split the divergent phase from the convergent phase, and price them differently.**
- **Divergent (you talk, explore, ramble):** must stay free-form — it cannot be pre-structured without killing discovery ([Bates berrypicking, 1989](https://pages.gseis.ucla.edu/faculty/bates/berrypicking.html); CreativeDC/HAICo). Make it **$0 tokens**: capture local.
- **Convergent (idealise → route → act):** here the frontier model earns its money — so give it a **tight, cached, sharpened** payload, never the raw ramble.

Your Epistemic Pipe already encodes this: the `ResearchQuery` **requires** a `sharpened_question`, applies the Five Rods, and **gates external search behind `local_attempts_count ≥ 2`** (Methodology Synthesis, Part XVI). That gate IS the token-efficiency mechanism. We're costing what you already designed.

---

## Your three questions, answered directly

**Q1. "If we used an AI and it used my research pipe, would that reduce token spend?" — Yes, materially.**
Routing exploratory talk through the pipe (retrieval) instead of dumping everything into chat context keeps the working context small. Peer-reviewed: for ~60%+ of queries, RAG and full long-context produce **identical outputs**, and RAG runs **20–200× cheaper** ([RAG vs long-context, arXiv:2407.16833](https://arxiv.org/abs/2407.16833)). Your pipe's `local_attempts_count ≥ 2` gate is exactly the "try retrieval before burning external/frontier tokens" rule the literature endorses. Anthropic's own context-engineering post names the same three levers — compaction, external note-taking (memory), sub-agents — as the production fix ([Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025).

**Q2. "If the prompt it used was idealised, would that reduce token spend?" — Yes, on every downstream turn.**
A sharpened prompt is smaller and, crucially, stays out of the re-sent history bloat. Prompt-compression prior art quantifies it: **LLMLingua 2–20× compression** ([arXiv:2310.05736](https://arxiv.org/abs/2310.05736)); **LongLLMLingua: 4× fewer tokens with +21.4% quality, ~94% cost cut** on a long-context benchmark ([arXiv:2310.06839](https://arxiv.org/abs/2310.06839)). Your `neutral-research-brief` + `transcription-prompt-optimiser` skills ARE the idealiser — they turn the ramble into the tight brief before the paid model sees it.

**Q3. "Both together?" — That's the loop.** Idealise the prompt (Q2) AND route it through the pipe (Q1), with the frontier model invoked only on the sharpened query. Cascade routing shows the headroom: **RouteLLM hit 85% cost reduction at 95% of GPT-4 quality, sending only 14% of calls to the frontier model** ([arXiv:2406.18665](https://arxiv.org/abs/2406.18665)).

---

## The loop, step by step — and how to make each step better

### Step 1 — CAPTURE (you talk). Keep it sacred. Make it free.
- **Now:** raw speech likely hits a paid model as transcript; then sits in context for every later turn.
- **Better:** local STT (whisper.cpp / MacWhisper) = **$0 tokens/minute** (`research_voice_first_efficiency.md`). Keep raw audio + transcript as provenance — your stated rule (transcription.md: "preserve raw audio provenance… each transformation visible"). Tangents and forks are preserved, not suppressed.
- **Map:** PARA/Zettelkasten "Capture" = $0 local. Appendix G is the proof this phase is where breakthroughs are born.

### Step 2 — CLEAN (de-ramble). Cheap model, never the frontier.
- **Now:** the frontier model wades through wrong words and forks — paying premium rates to read mess.
- **Better:** a cheap/local model runs `transcription-prompt-optimiser`: fix likely-intended wording, keep forks flagged not deleted. This is the documented "cheap cleanup layer before the frontier model sees anything" (Wispr Flow / SuperWhisper / Voice-Prompt-Enhancement-Node pattern). **Frontier model never sees raw speech.**

### Step 3 — IDEALISE (sharpen into a brief/prompt). The compression payoff.
- **Now:** if a fresh ramble seeds each turn, the prefix changes every time → **caching is impossible** (any byte change invalidates the cache — Anthropic caching docs). Exploratory chat is inherently cache-hostile; this is why convergence must produce a *stable artefact*.
- **Better:** `neutral-research-brief` emits the `sharpened_question` your pipe already requires. That brief is **cache-stable** — reuse it across turns and the 90% cache discount becomes available on the convergent side. Compression numbers above (2–20×) apply here.

### Step 4 — ROUTE (pipe + right engine). Frontier only on judgment.
- **Now:** everything tends to go to one expensive model in one long thread.
- **Better:** the estate **credit-first router** sends the sharpened brief to the cheapest competent engine — pipe/RAG for discovery (20–200× cheaper), local/Haiku for mechanical, frontier **only** for genuine judgment on the narrowed query. Your `ResearchQuery` gates (`local_attempts_count ≥ 2`, `asps_scrub_applied`, LLM packets capped at INTUITED) already enforce "exhaust cheap/local before burning frontier."
- **Optional convergent upgrade:** the **Portable Lens** (Part XVII) — N parallel cheap agents, each a different question, synthesise convergence — got 2-months-stalled work done in an hour. A convergent-phase accelerator that's still cheaper than one big frontier thread.

### Step 5 — HARVEST + FILE (organisational efficiency). Zero tokens, compounding value.
- **Now:** breakthroughs risk staying trapped in a thread → rediscovered later (which costs tokens again).
- **Better:** `content-harvester` + `thread-extraction` lift the keepers (QUOTE / LEARNING / MISTAKE / ATTRIBUTION / BLOG_SEED), PUDDING-tagged via Gatekeeper + Porch Watcher + curator → Brain. The mess becomes searchable next time, so future Step 4s hit the local-attempts gate and never reach the frontier. **This is where token-efficiency and organisational-efficiency become the same thing.**

---

## Cost shape, before vs after (illustrative, INTUITED until measured)

```
NOW (one long frontier thread):
  talk(raw) → FRONTIER reads mess → grows history every turn → re-sent each turn → no cache
  cost driver: premium model × bloated, ever-changing context

AFTER (phase-split pipe):
  talk(raw) ──$0 local STT──► cheap clean ──cheap──► idealise → STABLE BRIEF
                                                          │ (cached, 90% off on reuse)
                                                          ▼
                                  pipe/RAG (20-200× cheaper) ─┐
                                  local/Haiku (mechanical) ───┼─► result
                                  FRONTIER (judgment only) ───┘
                                                          ▼
                                  harvest → Brain (───$0, prevents future spend)
```

The frontier model goes from "reads everything, every turn" to "sees a small, cached, sharpened payload, rarely." That is the whole saving.

---

## What it means
- You change **nothing** about how you talk. The saving comes from what happens to your words *after* you speak, not from disciplining your speech.
- The loop is **your existing Epistemic Pipe**, with a cost rationale and a local-STT front end. Low build risk — much of it is doctrine already.
- Token-efficient and org-efficient are the same move here: harvesting to Brain (Step 5) is what stops future rediscovery, which is itself the cheapest token saving of all.

## What to change next (fastest wins first)
1. **Steps 1–2 now:** wire local STT capture + a cheap/local cleanup pass running `transcription-prompt-optimiser`. Biggest, easiest cut; no router needed.
2. **Step 3:** make the `neutral-research-brief` output a cache-stable artefact, not a fresh ramble per turn.
3. **Step 4:** route briefs through the estate credit-first router (ties to the estate spec).
4. **Step 5:** confirm harvest → pipe → Brain runs on every breakthrough thread.

## Not yet verified
- Estate-specific savings (need the cost log — the §9 proof run in the estate spec).
- Exact local-STT setup on WanMin/M4 (whisper.cpp vs MacWhisper) — not yet checked on-device.
- Whether the pipe's curator currently auto-runs content-harvester, or it's manual.

— Pipe discipline: draft in workspace. Human brief → Drive; this doc → Brain via the pipe; Vellum event drafted separately. Nothing written direct to Beast.
