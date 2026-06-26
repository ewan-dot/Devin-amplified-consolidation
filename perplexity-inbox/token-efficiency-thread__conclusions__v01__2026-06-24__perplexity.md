# Token-Efficiency Thread — Full Conclusions

TIER: STRUCTURED · vendor/benchmark numbers MEASURED at source · output-cost finding MEASURED on Ewan's threads · estate savings INTUITED until cost log runs · repo state VERIFIED (GitHub 2026-06-23)
PROVENANCE: complete Perplexity thread 2026-06-23 → 2026-06-24. Companion files in `token-efficiency-programme__2026-06-24/`.
AUTHOR: Perplexity (AI_PARTNER_PROXY, for-now). RATIFIER: Ewan (pending).
GOAL-LINK: cut recurring AI spend across the estate, prove the cut, keep Ewan's working style. Make money so we can give it away.

## What this thread was
A working session that produced a complete, proof-gated token-efficiency programme across M4/M5/Beast and every IDE/UI, plus three durable behavioural corrections to how Perplexity works with Ewan.

## Decisions made
1. **Adopt the estate token-efficiency programme.** Done = proven, not pushed (end-to-end tested; 10-point PROOF-OF-LIFE gate).
2. **Lean output is the #1 conversation lever.** Measured: AI produced ~98% of words; output costs ~5× input; ~99.5% of per-turn cost is AI output. Cut output X% → save ~X%.
3. **Created `lean-by-default` skill** (auto-loads with min-rule). Standalone, not folded into succinct-complete-output.
4. **Merged `decision-log-labeler` + `utterance-tagger` into `thread-extraction`** as Mode 7 / Mode 8 (full axis logic in references/). Kept `uix-antigravity-curator`. De-dup iso-8601 → keep user descriptive-first.
5. **Voice-first loop = divergent (cheap/local, keep the mess) split from convergent (cached/frontier-only on the sharpened query).** Maps onto the existing Epistemic Pipe.
6. **Mac mini = 24GB** → local lane default **Qwen2.5-Coder-14B 4-bit** (~9–10GB), via Ollama+LiteLLM.

## Corrections Ewan made (sharpenings — HUMAN_INTUITED)
- **Verbosity is a failure mode.** → `lean-by-default` skill + per-IDE `CONVENTIONS.md` + Claude Code block + proxy `max_tokens`.
- **Claude Code needs its own lean rule** (Computer skills don't load there) → `CLAUDE.md` block, not a Perplexity skill.
- **Standing-grants applies:** stop asking "shall I?" for Tier A/B work; the endpoint is the inbox.
- **Inbox push = Tier B, not Tier A; one attempt, no loop.** (Both originally got wrong; corrected.)

## Key findings (carry these; don't re-derive)
- **CLI vs MCP:** primaries are **32×** (Scalekit, 75-run benchmark) and **98.7%** (Anthropic, 150K→2K tokens). MCP injects all tool schemas every turn (Anthropic measured 134K tokens). Rule: CLI for read-only doors; code-execution/progressive-disclosure for big APIs; MCP only where caching+OAuth/audit earn it. CLI can cost *more* on long multi-step loops.
- **Caching is the biggest infra lever:** 90% off cached input (Anthropic/Google), 50–75% (OpenAI), ~98% (DeepSeek). Byte-identical prefix or it invalidates. **Batch×cache stacks on Anthropic (~95%), NOT on OpenAI/Google.**
- **Routing:** Opus-plans + Sonnet/Haiku-executes beat solo-Opus 90.2% (Anthropic); cheap/local for mechanical, frontier only for judgment.
- **Enforcement:** the proxy (holds the keys) is the wall — hard max_tokens, budget 402s, oversized-prompt reject, forced cache injection, model allowlist. Claude Code managed-settings+hooks for what the proxy can't see. CI/harness stops non-compliant setups existing. **Output verbosity is the only rule with no hard block** — cap + Stop-hook + OTel ratio alert.
- **Voice-first:** RAG/pipe 20–200× cheaper than dumping context; prompt distillation 2–20× fewer tokens; local STT $0.

## Verified estate state (GitHub, 2026-06-23)
- `estate-cost-tools` ~60% built (optimising proxy: caching, compaction, Haiku routing, cost log, budget cap, self-heal). Tested n=69 May only; semantic cache off; **not proven across the estate**.
- `estate-token-router` (credit-first LiteLLM router) **does not exist** — specced, unbuilt.
- `anthropic-token-proxy` archived (confirm fully superseded).

## Artifacts produced (all in the inbox subfolder)
Implementation brief (entry point) · master plan · enforcement plan · estate spec (finish-and-prove) · token-reduction research conclusion + human brief · voice-first research conclusion + human brief · lean-output estate guide · local-model-tier addendum · Vellum events JSONL (10 events, for the pipe) · 5 raw research dossiers (cli-vs-mcp, ide-controls, context-habits, voice-first, enforcement).
Also: `lean-by-default` skill (library) · updated `thread-extraction` skill · master+enforcement plans in Google Drive (Amplified Partners folder).

## Implement order (cheapest + most durable first)
1. Lean output everywhere (zero infra). 2. Bake per-IDE knobs. 3. Voice-first front end (local STT + cheap cleanup). 4. Deploy + live-prove the proxy across ALL lanes. 5. Build the credit-first router. 6. Enforcement (proxy guardrails first). 7. Telemetry → Vellum; budgets graduate to MEASURED at ≥2 weeks.

## Open items / gates
- **Tier C (Ewan only):** delete 3 merged skills in Perplexity settings (decision-log-labeler, utterance-tagger, org-scope iso-8601).
- **Verify before external use:** Anthropic Pool 1/Pool 2 status (may be unshipped); "62% re-sent context" (no primary source); confirm anthropic-token-proxy superseded.
- **Scheduled:** spend-delta check 7 July (will report "insufficient data" if proxy not live by then).
- **Pipe:** the Vellum JSONL must enter the Beast only through the pipe (Python+Rust+Vellum+AI+Human) — no side door.

[CLOSURE] branch=ACTION | proxy=1 logged (conclusions to inbox) | gates=delete 3 skills (Ewan) | tier=STRUCTURED
