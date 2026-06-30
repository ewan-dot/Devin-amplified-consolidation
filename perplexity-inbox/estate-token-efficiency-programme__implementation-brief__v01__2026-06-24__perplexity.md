# Estate Token-Efficiency Programme — Implementation Brief (inbox handoff)

TIER: STRUCTURED · vendor numbers MEASURED at source · estate savings INTUITED until cost log runs
PROVENANCE: Perplexity thread 2026-06-23/24; companion files in `token-efficiency-programme__2026-06-24/`
FOR: MacAirM5 local implementer AIs. This is the entry point — read this, then the companion files.
GOAL-LINK: cut recurring AI spend across the estate and prove the cut. Make money so we can give it away.

## What this is
A complete, researched, ready-to-implement token-efficiency programme across M4/M5/Beast and every IDE/UI. Nothing here needs Ewan to think further before implementation can start; the only hard gates are listed at the bottom.

## Implement in this order (cheapest + most durable first)
1. **Lean output everywhere (zero infra).** Deploy `CONVENTIONS.md` (block in `lean-output-deployment__estate-guide`) into each IDE config slot per that guide's table. Add the Claude Code `CLAUDE.md` output-discipline block.
2. **Bake per-IDE knobs.** Caching, model pins, ignore files, thinking-token caps, repo-maps — per `token-reduction-prior-art__research-conclusion` §C and `research_ide_controls.md`.
3. **Voice-first front end.** Wire local STT ($0) + cheap cleanup pass (Steps 1–2 of `voice-first-token-efficiency__research-conclusion`). Needs: which Mac listens, whisper.cpp vs MacWhisper.
4. **Deploy + live-prove the central proxy.** `estate-cost-tools` already ~60% built (proxy, caching, compaction, Haiku routing, cost log, budget cap). Wire ALL IDE lanes via `ANTHROPIC_BASE_URL`, not just a canary. Per `token-efficiency__estate-spec` §D.
5. **Build the credit-first router** (`estate-token-router`, does not exist yet) — spec §C; LiteLLM, credit-first, budget guard, Production-Law gate.
6. **Enforcement.** Apply `estate-token-efficiency__enforcement-plan`: proxy guardrails (max_tokens, budgets, caching injection, model allowlist) first — covers most rules at once — then Claude Code managed-settings + hooks, CI/harness, OTel telemetry.
7. **Telemetry → Vellum.** Per-job tokens/cost/Effective-Tokens through the pipe; budgets graduate INTUITED→MEASURED at ≥2 weeks live.

## Done = proven, not pushed
Implement to the 10-point PROOF-OF-LIFE gate in `token-efficiency__estate-spec` §9: proxy live + wired across every lane; router live + survives restart; one job routed across ≥3 executor classes with credit-first decision logged; budget guard refuses over-budget; >90% cache-read on repeat; local-lane job at $0; telemetry in Vellum; before/after delta measured. Capture in `PROOF-OF-LIFE.md`.

## Key corrected facts (carry these, don't re-derive)
- CLI-vs-MCP primaries: 32× (Scalekit), 98.7% (Anthropic). CLI for read-only doors; code-execution for big APIs; MCP only where caching+auth earn it.
- Biggest conversation lever is OUTPUT length: ~99.5% of per-turn cost is AI output; cut X% → save ~X%. Verbosity is the only rule with no hard block — cap + Stop-hook + OTel trend.
- Batch×cache stacks on Anthropic (~95%), NOT on OpenAI/Google.

## Verify before external/production use
- Anthropic Pool 1/Pool 2 status (may be unshipped) — the spec §6 trap depends on it.
- "62% re-sent context" figure — no primary source yet; internal only.
- Confirm `anthropic-token-proxy` fully superseded by `estate-cost-tools`.

## Hard gates (Ewan only — Tier C)
- **Mac mini RAM** — blocks local-model tier sizing. Need the real figure.
- **Delete 3 merged skills** in Perplexity settings: decision-log-labeler, utterance-tagger, org-scope iso-8601 (no delete tool exposed to Perplexity).
- The Vellum events (`token-efficiency__vellum-events__pipe-draft.jsonl`) must enter the Beast **only through the pipe** (Python+Rust+Vellum+AI+Human) — do not side-door.

## Companion files
All in `token-efficiency-programme__2026-06-24/`: master plan, enforcement plan, estate spec, prior-art research (+human brief), voice-first loop (+human brief), lean-output guide, Vellum events JSONL, and 5 raw research dossiers.

[CLOSURE] branch=ACTION | proxy=1 logged (inbox handoff drop) | gates=Mac mini RAM + 3 skill deletions | tier=STRUCTURED
