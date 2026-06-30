# Estate Token-Efficiency — Enforcement Plan

TIER: STRUCTURED · mechanisms MEASURED at source (official docs, cited) · estate effect INTUITED until live
PROVENANCE: `research_enforcement.md` (official Anthropic / Cursor / LiteLLM / OTel docs, 2026-06)
GOAL-LINK: config is suggestion; this makes the rules hold whether or not anyone cooperates. Companion to the master plan.

## The principle
**Enforce as close to the credential as possible.** A rule on the developer's good intentions is a nudge; a rule at the proxy (which holds the API key) is a wall. So: hard-block at the **proxy** wherever a rule touches the API call; use **client hooks / managed settings** for things the proxy can't see (local launch flags, MCP-vs-CLI choice); use **CI/harness** to stop non-compliant setups existing; use **telemetry** for the one rule nothing can hard-block (verbosity).

Three enforcement tiers: **HARD BLOCK** (request refused), **GATED** (can't launch/commit without it), **MEASURED** (can't hard-stop, but tracked + alerted).

## Rule → best enforcement point

| Rule | Mechanism | Tier | Where |
|---|---|---|---|
| Output max length | `max_tokens` in `litellm_params` (overrides client) | HARD BLOCK (cap) | Proxy |
| Output verbosity (style) | system prompt + `Stop` hook (iterative, ≤8) + OTel trend | MEASURED | Client + telemetry |
| Oversized prompt rejected | `enable_pre_call_checks` + `max_input_tokens` | HARD BLOCK | Proxy |
| Budget cap | per-key `max_budget` → HTTP 402; `fail_closed_budget_enforcement` | HARD BLOCK | Proxy |
| Prompt caching on | `cache_control_injection_points` (auto-inject) | HARD (enforced) | Proxy |
| Model allowlist | `availableModels` + `enforceAvailableModels:true` (managed-settings, MDM) | HARD BLOCK | Claude Code managed settings |
| Thinking-token cap | `MAX_THINKING_TOKENS` in managed settings | HARD BLOCK | Claude Code managed settings |
| Block MCP, force CLI | `PreToolUse` hook, match `mcp__.*`, `permissionDecision:"deny"` | HARD BLOCK | Claude Code hook |
| Cache-stable context | `UserPromptSubmit` hook injects `additionalContext` | GATED (inject) | Claude Code hook |
| Launch flags (`--bare`, `--exclude-dynamic-system-prompt-sections`, `--max-budget-usd`, `--max-turns`) | launcher harness script (only way to start the agent) | GATED | Harness |
| Cursor Max Mode off / model tier | Enterprise admin dashboard (hard-block by tier) | HARD BLOCK (Enterprise) | Cursor admin |
| Cursor spend cap | team hard cap blocks requests | HARD BLOCK | Cursor admin |
| Cursor `.cursor/rules` | `alwaysApply:true` | MEASURED (nudge) | Client — model can deviate |
| CLAUDE.md ≤200 lines, ignore files present, hooks config present | pre-commit + CI check, fail build | GATED | CI |

## By avenue

### 1. Proxy (LiteLLM on the Beast) — the wall
Strongest point: everything routes through it and it holds the keys. Enforce: hard `max_tokens` per model; `enable_pre_call_checks` to reject oversized prompts (402); per-key `max_budget` with `fail_closed_budget_enforcement:true` (no bypass on Redis outage); `cache_control_injection_points` to force caching without client help; post-call guardrails (`default_on:true`, `modify_guardrails:false` so teams can't disable). **Credential-gate everything through it** — if the only working API key lives in the proxy, bypass is impossible.

### 2. Claude Code — managed settings + hooks
`managed-settings.json` (highest precedence, MDM-deployable, user can't override): `enforceAvailableModels:true`, `MAX_THINKING_TOKENS`, OTel config. Hooks: `PreToolUse` deny on `mcp__.*` (force CLI); `UserPromptSubmit` inject cache-stable context; `Stop` hook to check `last_assistant_message` length (iterative, capped at 8 blocks — a nudge, not a wall).

### 3. Cursor — admin dashboard (Enterprise) + proxy
Enterprise admin hard-blocks Max Mode, model tier, context size, effort, and sets a team spend cap. `.cursor/rules` are nudges only. For hard enforcement of caching/caps, route Cursor through the proxy. Per-user caps need Enterprise (not Teams).

### 4. Telemetry — the only lever for verbosity
Claude Code OTel emits `claude_code.token.usage` split by input/output/cacheRead/cacheCreation, plus `mcp_tool.name`. Mandate OTel via managed settings. Feed to the cost log → Vellum. Verbosity can't be hard-blocked (generative), so: `max_tokens` cap as backstop + Stop-hook nudge + **OTel output-token trend with an alert when a session's output/input ratio exceeds threshold**. Helicone cost rate-limit returns 429 as a hard stop if you want a ceiling.

### 5. CI / harness — stop non-compliance existing
Pre-commit + CI: fail build if CLAUDE.md >200 lines, ignore files missing, or hooks/managed-settings absent. Launcher harness: a wrapper script is the *only* sanctioned way to start any agent — it injects the flags and points at the proxy. Developer literally cannot launch the inefficient config.

## The honest gap
**Output verbosity is the one rule with no hard block** — it's generative. The stack is: proxy `max_tokens` (backstop) → system-prompt/`CONVENTIONS.md` rule → `Stop`-hook nudge → OTel trend + alert → human review. Everything else in the plan has a real wall available, and the proxy is most of them.

## Build order (matches the master plan)
1. Stand up the proxy with hard `max_tokens`, budgets, caching injection, allowlist (covers most rules at once).
2. Credential-gate all IDEs through it.
3. Claude Code managed-settings (models, thinking tokens, OTel) + the three hooks.
4. Launcher harness + CI checks.
5. OTel → cost log → Vellum; verbosity alert on output/input ratio.

Proof: a denied MCP call forced to CLI; a 402 on over-budget; a rejected oversized prompt; cache-read >90% on repeat; OTel verbosity alert fires on a deliberately long reply. Folds into the spec §9 gate.

Sources: official docs in `research_enforcement.md` (Anthropic hooks 2026-06-16, managed settings, OTel; Cursor changelog 2026-05-04; LiteLLM budgets/guardrails/caching).
