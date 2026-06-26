# Token-Rule Enforcement: Mechanisms for AI Coding Estates

**Prepared for:** Ewan Bramley / Amplified Partners  
**Date:** 2026-06-24  
**Scope:** Claude Code, Cursor, LiteLLM proxy (Beast), CI/git harnesses  
**Source priority:** Official docs, dated where available. Community-only findings flagged ⚠️.

---

## Table of Contents

1. [Claude Code Hooks](#1-claude-code-hooks)
2. [Cursor Enforcement](#2-cursor-enforcement)
3. [Central Proxy Enforcement (LiteLLM)](#3-central-proxy-enforcement-litellm)
4. [Telemetry / Observability as Enforcement](#4-telemetry--observability-as-enforcement)
5. [CI / Git Hooks / Harnesses](#5-ci--git-hooks--harnesses)
6. [General Principle: Hard Block vs. Nudge](#6-general-principle-hard-block-vs-nudge)
7. [Rule → Best Enforcement Point (Master Table)](#7-rule--best-enforcement-point-master-table)

---

## 1. Claude Code Hooks

**Source:** [Anthropic Claude Code Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks), published 2026-06-16  
**Source:** [Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings), published 2026-06-22

### 1.1 Hook Event Inventory

Hooks fire at specific lifecycle points. Input is delivered as JSON on stdin (command hooks) or as HTTP POST body (HTTP hooks).

| Event | When it fires | Can BLOCK? | Blocking mechanism |
|---|---|---|---|
| `SessionStart` | Session begins or resumes | **No** | Observation only; can inject `additionalContext` |
| `Setup` | `--init-only` / CI prep | **No** | Observation only |
| `UserPromptSubmit` | After user submits prompt, before Claude processes | **Yes** | `decision: "block"` + `reason`; exit code 2 |
| `UserPromptExpansion` | When a `/command` expands to a prompt | **Yes** | `decision: "block"`; exit code 2 |
| `PreToolUse` | Before any tool call executes | **Yes** | `hookSpecificOutput.permissionDecision: "deny"` |
| `PermissionRequest` | Permission dialog appears | **Yes** | `decision.behavior: "deny"` |
| `PermissionDenied` | Tool call denied by auto-mode | No (retry only) | `{retry: true}` to allow model to try again |
| `PostToolUse` | After tool completes | **No** | Can add `additionalContext` to Claude's view |
| `PostToolBatch` | After a batch of tool calls, before next model call | **Yes (stops loop)** | `decision: "block"` stops agentic loop |
| `Stop` | When Claude is about to end its turn | **Yes** | `decision: "block"` + `reason`; Claude continues |
| `StopFailure` | API error during stop | No | Observation only |
| `SubagentStop` | Subagent about to finish | **Yes** | `decision: "block"` |
| `TaskCreated` / `TaskCompleted` | Teammate task lifecycle | **Yes** | `{continue: false, stopReason: "..."}` |
| `ConfigChange` | Any config change attempted | **Yes** | `decision: "block"` (except `policy_settings`) |
| `PreCompact` | Before context compaction | **Yes** | `decision: "block"` |

### 1.2 Exit Code Semantics

| Exit code | Meaning |
|---|---|
| `0` | Success; stdout parsed for JSON decisions/context |
| `1` | **Non-blocking** error — action proceeds (counterintuitive, but stated explicitly) |
| `2` | **Blocking** error — prevents the action for most events |

For `WorktreeCreate`, any non-zero exit blocks creation.

### 1.3 PreToolUse — Blocking MCP Calls and Injecting Decisions

`PreToolUse` is the primary enforcement point for tool-call rules. MCP tools use the naming convention `mcp__<server>__<tool>`.

**JSON decision schema:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "MCP calls blocked — use CLI equivalent",
    "updatedInput": { ... }   // optional: rewrite tool input before execution
  }
}
```

`permissionDecision` values:
- `"deny"` — hard block, message sent to Claude
- `"allow"` — skip permission prompt, execute
- `"ask"` — force user confirmation dialog
- `"defer"` — pause for later resumption

**MCP blocking pattern:**
```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "mcp__.*",
      "command": "/usr/local/bin/mcp-block-hook"
    }]
  }
}
```
The hook script exits 0 with JSON `permissionDecision: "deny"` to block all MCP tool calls at PreToolUse. The blocking message tells Claude to use the CLI equivalent.

**Input rewriting for efficiency:** Set `updatedInput` to strip verbose parameters, inject `max_tokens` caps, or normalise tool arguments before execution. Entire input object must be present; only changed fields differ.

### 1.4 UserPromptSubmit — Adding Cache-Stable Context / Blocking Verbosity

| Capability | Available |
|---|---|
| Block prompt entirely | Yes — `decision: "block"`, `reason` displayed to user |
| Inject `additionalContext` alongside prompt | Yes — string added to Claude's view |
| Replace the prompt text | **No** — cannot rewrite prompt content |

**Cache-stable prefix injection via `SessionStart`:**  
`SessionStart.additionalContext` fires once per session before the first prompt. Use it to inject a stable token-efficiency system instruction (fixed wording, no dynamic content) that benefits from prompt caching:
```bash
#!/bin/bash
# SessionStart hook
echo '{"hookSpecificOutput": {"hookEventName": "SessionStart",
  "additionalContext": "EFFICIENCY RULES: Use lean output. Prefer CLI over MCP. Keep responses under 200 words unless explicitly asked for more."}}'
```

**Stop hook — post-hoc output length check:**  
`Stop` receives `last_assistant_message` (full text of final response). A hook can measure length and — if over threshold — set `decision: "block"` with a `reason` instructing Claude to produce a shorter version. This is the closest available mechanism to enforcing output verbosity limits, but it is iterative (adds a turn), not a hard block on generation length. Claude Code will override after 8 consecutive blocks.

### 1.5 Thinking Token Caps via Settings

`MAX_THINKING_TOKENS=0` in the `env` block of managed settings disables extended thinking entirely for non-Fable 5 models. Set a non-zero integer to cap thinking token budget:
```json
// managed-settings.json
{
  "env": {
    "MAX_THINKING_TOKENS": "8000"
  }
}
```
`alwaysThinkingEnabled: false` disables thinking globally. `effortLevel: "low"` / `"medium"` reduces reasoning depth.

### 1.6 Model Allowlisting via Managed Settings

```json
// managed-settings.json (highest precedence — cannot be overridden)
{
  "availableModels": ["claude-sonnet-4-6", "claude-haiku-4-5"],
  "enforceAvailableModels": true,
  "disableAllHooks": false,
  "allowManagedHooksOnly": true
}
```

`enforceAvailableModels: true` constrains the Default model to the allowlist. `allowManagedHooksOnly: true` prevents users from adding their own hooks. Delivered via `/etc/claude-code/managed-settings.json` (Linux/WSL), macOS plist, or Windows registry — cannot be overridden by project or user settings.

### 1.7 Enforcement Table — Claude Code Hooks

| Rule | Mechanism | Block or Warn | Source |
|---|---|---|---|
| Deny MCP tool calls, force CLI | `PreToolUse` hook matching `mcp__.*`, return `permissionDecision: "deny"` | **BLOCK** | [Hooks ref, 2026-06-16](https://docs.anthropic.com/en/docs/claude-code/hooks) |
| Inject cache-stable prefix each session | `SessionStart` hook returning `additionalContext` | N/A (injection) | [Hooks ref, 2026-06-16](https://docs.anthropic.com/en/docs/claude-code/hooks) |
| Inject cache-stable prefix each prompt | `UserPromptSubmit` hook returning `additionalContext` | N/A (injection) | [Hooks ref, 2026-06-16](https://docs.anthropic.com/en/docs/claude-code/hooks) |
| Block overly verbose prompts | `UserPromptSubmit` returning `decision: "block"` after length check | **BLOCK** | [Hooks ref, 2026-06-16](https://docs.anthropic.com/en/docs/claude-code/hooks) |
| Post-hoc output verbosity check | `Stop` hook reading `last_assistant_message`, blocking if over threshold | **BLOCK (iterative)** | [Hooks ref, 2026-06-16](https://docs.anthropic.com/en/docs/claude-code/hooks) |
| Cap thinking tokens | `MAX_THINKING_TOKENS` env var in managed settings | **BLOCK (hard cap)** | [Settings ref, 2026-06-22](https://docs.anthropic.com/en/docs/claude-code/settings) |
| Model allowlist | `availableModels` + `enforceAvailableModels: true` in managed settings | **BLOCK** | [Settings ref, 2026-06-22](https://docs.anthropic.com/en/docs/claude-code/settings) |
| Prevent users adding hooks | `allowManagedHooksOnly: true` in managed settings | **BLOCK** | [Settings ref, 2026-06-22](https://docs.anthropic.com/en/docs/claude-code/settings) |
| `--max-turns` cap per session | CLI flag in launcher script: `claude -p --max-turns 40` | **BLOCK (exits on limit)** | [CLI ref, backgroundclaude.com](https://backgroundclaude.com/cli-reference) |
| `--max-budget-usd` hard cap | CLI flag in launcher script: `claude -p --max-budget-usd 5.00` | **BLOCK (aborts run)** | [CLI ref, backgroundclaude.com](https://backgroundclaude.com/cli-reference) |
| `--bare` mode (skip CLAUDE.md / MCP discovery) | CLI flag in launcher script | **BLOCK (never loads)** | [CLI ref, backgroundclaude.com](https://backgroundclaude.com/cli-reference) |
| Cache-stable prefixes via `--exclude-dynamic-system-prompt-sections` | Moves per-machine sections (cwd, env, git status) to first user message, stabilising system-prompt hash | Improves cache hit (not a block) | [CLI ref, backgroundclaude.com](https://backgroundclaude.com/cli-reference) |
| Stop agentic loop after tool batch | `PostToolBatch` hook with `decision: "block"` | **BLOCK** | [Hooks ref, 2026-06-16](https://docs.anthropic.com/en/docs/claude-code/hooks) |

---

## 2. Cursor Enforcement

**Sources:**  
- [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) — model controls, spend management, analytics  
- [awesome-cursor-rules reference](https://github.com/sanjeed5/awesome-cursor-rules-mdc/blob/main/cursor-rules-reference.md), 2025-02-17  
- [Pondero analysis of Cursor Enterprise May 2026 controls](https://pondero.ai/coding/guides/cursor-enterprise-admin-controls-may-2026/), 2026-05-05  

### 2.1 What Cursor Can Enforce vs. What Is Per-User

| Control | Admin Can ENFORCE? | Mechanism | Notes |
|---|---|---|---|
| **Model allowlist / blocklist** | **Yes (Enterprise)** | Admin dashboard → Settings → Models; block providers or specific model configurations by speed tier and context-window size | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |
| **Block Max Mode globally** | **Yes (Enterprise)** | Block "extended context" configuration in model controls dashboard | Max Mode is a context-window multiplier; blocking it prevents >200k token windows |
| **Spend hard cap (team-level)** | **Yes (Teams + Enterprise)** | Dashboard → Spend Management; hard limit stops requests; soft limit sends alerts at 50%, 80%, 100% | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |
| **Per-user spend cap** | **No (Teams); Enterprise only** | "Enforced per-member usage limits aren't available on Teams plans" per forum post | [Cursor forum, 2026-05-05](https://forum.cursor.com/t/set-each-members-usage-quota-in-the-team-version/159792/7) |
| **Team Rules (always-apply)** | **Yes (Team + Enterprise)** | Dashboard → Rules → "Enforce this rule" toggle. Enforced rules cannot be disabled in user settings | [cursor-rules reference](https://github.com/sanjeed5/awesome-cursor-rules-mdc/blob/main/cursor-rules-reference.md) |
| **Team Rules (optional)** | Non-enforced | Without "Enforce this rule", users can toggle off in `Cursor Settings → Rules` | |
| **Project rules (`alwaysApply: true`)** | Project-level only | `.cursor/rules/*.mdc` with `alwaysApply: true` frontmatter; applies to all agents in that repo | [DataCamp guide, 2026-03-11](https://www.datacamp.com/tutorial/cursor-rules) |
| **Effort level / thinking depth** | **Yes (Enterprise, new)** | Model control allows blocking specific effort-level configurations | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |
| **Block new providers by default** | **Yes (Enterprise)** | "Enterprises have the option to block new providers or model versions by default" | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |

### 2.2 Rules Enforcement Details

**`.cursor/rules/*.mdc` structure:**
```yaml
---
description: "Lean output rules"
alwaysApply: true
globs: ["**/*"]
---
# Output Discipline
- Keep responses under 200 words unless explicitly asked for more
- Never add explanatory preamble; start with the answer
- Prefer single-command CLI solutions over multi-step tool chains
```

`alwaysApply: true` prepends the rule to every agent context window in the project. Rules are **suggestions to the model**, not hard programmatic constraints — they influence generation but cannot technically block output.

**Team rules (dashboard-created):**
- Visible in `Cursor Settings → Rules → Team Rules`
- With "Enforce this rule" enabled: users cannot disable it
- Team Rules do not support `globs`, `alwaysApply` metadata (they are always applied)
- Precedence: Team Rules → Project Rules → User Rules

⚠️ **Critical limitation:** Cursor rules are prompt-level instructions. They cannot programmatically block a response. The model may ignore them. Max Mode can be administratively blocked at Enterprise tier, but not disabled per-project.

### 2.3 Central Proxy Bypass (Recommended for Hard Enforcement)

For the Beast proxy architecture, route all Cursor API calls through LiteLLM by setting Cursor's base URL override:
```json
// ~/Library/Application Support/Cursor/User/settings.json
{
  "cursor.openai.apiBaseUrl": "https://beast.amplified.internal/v1",
  "cursor.anthropic.apiBaseUrl": "https://beast.amplified.internal/anthropic"
}
```
This makes the proxy the authoritative enforcement point for all Cursor-originated calls. Deploy via MDM.

### 2.4 Enforcement Table — Cursor

| Rule | Mechanism | Block or Warn | Source |
|---|---|---|---|
| Model allowlist (deny non-approved models) | Admin dashboard → model controls blocklist | **BLOCK (Enterprise)** | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |
| Disable Max Mode (extended context) | Block extended context-window configuration | **BLOCK (Enterprise)** | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |
| Team-wide spend cap | Hard limit in spend management | **BLOCK (stops requests)** | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |
| Spend alerts | Soft limits at 50%/80%/100% | **WARN** | [Cursor changelog 2026-05-04](https://cursor.com/changelog/05-04-26) |
| Lean output rules (prompt-level) | Team Rule with "Enforce this rule", `alwaysApply: true` project rule | **WARN only** (model may deviate) | [cursor-rules ref, 2025-02-17](https://github.com/sanjeed5/awesome-cursor-rules-mdc/blob/main/cursor-rules-reference.md) |
| CLI-over-MCP preference | Team Rule injected into every context | **WARN only** | Same |
| Route all calls through Beast proxy | `cursor.openai.apiBaseUrl` / `cursor.anthropic.apiBaseUrl` override via MDM | **Enables proxy enforcement** | [Aperion docs, 2026-01-10](https://docs.aperion.ai/smartflow-ide-configuration.html) |

---

## 3. Central Proxy Enforcement (LiteLLM)

**Sources:**  
- [LiteLLM Budgets & Rate Limits](https://litellm.vercel.app/docs/proxy/users), 2023-12-22  
- [LiteLLM Guardrails Quick Start](https://docs.litellm.ai/docs/proxy/guardrails/quick_start)  
- [LiteLLM Config Settings](https://docs.litellm.ai/docs/proxy/config_settings)  
- [LiteLLM Virtual Keys](https://docs.litellm.ai/docs/proxy/virtual_keys), 2023-11-24  
- [LiteLLM Prompt Caching Tutorial](https://docs.litellm.ai/docs/tutorials/prompt_caching)  
- [LiteLLM Claude Code Prompt Cache Routing](https://docs.litellm.ai/docs/tutorials/claude_code_prompt_cache_routing)  

The proxy is the **strongest enforcement point** because every call from Claude Code and Cursor routes through it. Enforcement here cannot be bypassed by client-side settings.

### 3.1 max_tokens Cap Enforcement

**Per-model cap in `config.yaml` (hard enforcement):**
```yaml
model_list:
  - model_name: claude-sonnet-4-6
    litellm_params:
      model: anthropic/claude-sonnet-4-6
      api_key: os.environ/ANTHROPIC_API_KEY
      max_tokens: 4096          # ← caps output tokens on every request to this deployment
```
Setting `max_tokens` in `litellm_params` applies it as the ceiling for that deployment. The client-requested `max_tokens` is overridden if higher. This is a **hard cap** — the model cannot produce more output tokens than this value.

**Global default via environment variable:**
```bash
DEFAULT_MAX_TOKENS=4096   # LiteLLM config_settings default; affects all calls without explicit max_tokens
```

**Input token / context window pre-call check:**
```yaml
router_settings:
  enable_pre_call_checks: true   # rejects requests exceeding max_input_tokens before sending to provider

model_list:
  - model_name: claude-sonnet-4-6
    litellm_params:
      model: anthropic/claude-sonnet-4-6
    model_info:
      max_input_tokens: 100000   # reject prompts > 100k tokens
```
Returns an error rather than forwarding the oversized request. Requires `enable_pre_call_checks: true`.

### 3.2 Budget Enforcement — Hard Blocks

```yaml
# Global budget cap
general_settings:
  master_key: sk-beast-master
  max_budget: 500.0          # total USD cap across all keys
  budget_duration: 30d

litellm_settings:
  max_budget: 500.0
  budget_duration: 30d
  fail_closed_budget_enforcement: true  # reject with 503 when spend cannot be verified; prevents budget bypass during Redis outage
```

**Per-key budget (each developer or service gets a key):**
```bash
curl 'http://0.0.0.0:4000/key/generate' \
  -H "Authorization: Bearer sk-beast-master" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "ewan-cursor",
    "max_budget": 50.0,
    "budget_duration": "30d",
    "soft_budget": 40.0,
    "models": ["claude-sonnet-4-6", "claude-haiku-4-5"],
    "tpm_limit": 500000,
    "rpm_limit": 100
  }'
```

When `max_budget` is exceeded, the proxy returns **HTTP 402** (payment required / budget exhausted) — request is **hard-blocked**. `soft_budget` triggers an alert before the hard cap.

**Budget check frequency:** By default every 10 minutes (DB-backed). For near-real-time enforcement:
```yaml
general_settings:
  proxy_budget_rescheduler_min_time: 1
  proxy_budget_rescheduler_max_time: 1
```

### 3.3 Model Allow/Deny Routing

```bash
# Create key restricted to approved models only
curl 'http://0.0.0.0:4000/key/generate' \
  -H "Authorization: Bearer sk-beast-master" \
  -d '{
    "models": ["claude-sonnet-4-6", "claude-haiku-4-5"],
    "key_alias": "dev-team-key"
  }'
```
Requests for unlisted models fail with an auth error. An empty `models: []` means no restriction.

**Upper-bound key generation params** (prevents keys being issued with excessive budgets):
```yaml
litellm_settings:
  upperbound_key_generate_params:
    max_budget: 100
    budget_duration: "10d"
    tpm_limit: 1000000
    rpm_limit: 200
```

### 3.4 Prompt Caching Enforcement at Proxy

**Auto-inject `cache_control` checkpoints:**
```yaml
model_list:
  - model_name: claude-sonnet-4-6-cached
    litellm_params:
      model: anthropic/claude-sonnet-4-6
      api_key: os.environ/ANTHROPIC_API_KEY
      cache_control_injection_points:
        - location: message
          role: system     # injects cache_control: {type: ephemeral} on system message
```
This forces Anthropic prompt caching on every system message without requiring clients to pass `cache_control` headers. Anthropic requires minimum 2,048 tokens for Claude Sonnet 4.x to be eligible for caching.

**Cache-friendly routing (same deployment for repeated system prefixes):**
```yaml
router_settings:
  optional_pre_call_checks: ["prompt_caching"]   # routes requests with identical prefixes to the same deployment
```
This is an opt-in pre-call check that maximises cache hits by pinning cache-primed sessions to the same upstream deployment.

### 3.5 Guardrails

Guardrails run at `pre_call`, `during_call`, or `post_call` and can **hard-block** requests returning HTTP 400:

```yaml
guardrails:
  - guardrail_name: "output-length-check"
    litellm_params:
      guardrail: custom_guardrail.OutputLengthGuardrail
      mode: "post_call"
      default_on: true
```

A custom `post_call` guardrail can inspect output token count and reject the response (returning a 400 to the client). This is the proxy-side complement to the Claude Code `Stop` hook.

Disable team from circumventing guardrails:
```bash
curl -X POST 'http://0.0.0.0:4000/team/update' \
  -d '{"team_id": "...", "metadata": {"guardrails": {"modify_guardrails": false}}}'
```
Attempting to pass `{"guardrails": {"hide_secrets": false}}` then returns HTTP 403.

### 3.6 Required Parameters Enforcement (Enterprise)

```yaml
general_settings:
  master_key: sk-1234
  enforced_params:
    - user                        # every request must include user field
    - metadata.generation_name    # every request must include generation name
```
Requests missing these params get a 400 `BadRequest`. Useful for ensuring cost attribution and traceability.

### 3.7 Rate Limits

```yaml
# Per-deployment TPM/RPM (blocks at the deployment level)
model_list:
  - model_name: claude-sonnet-4-6
    litellm_params:
      model: anthropic/claude-sonnet-4-6
      rpm: 60
      tpm: 500000
```

Per-key TPM limits prevent any single key from burning context tokens at scale. TPM limits enforce token-volume caps with hard 429 responses.

### 3.8 Enforcement Table — LiteLLM Proxy

| Rule | Mechanism | Block or Warn | Source |
|---|---|---|---|
| Output token cap per model | `max_tokens` in `litellm_params` | **BLOCK (hard cap)** | [LiteLLM config overview](https://docs.litellm.ai/docs/proxy/configs) |
| Input token cap (reject oversized prompts) | `enable_pre_call_checks: true` + `model_info.max_input_tokens` | **BLOCK (pre-call rejection)** | [LiteLLM config settings](https://docs.litellm.ai/docs/proxy/config_settings) |
| Per-key budget hard cap | `max_budget` on virtual key; returns HTTP 402 | **BLOCK** | [LiteLLM budgets](https://litellm.vercel.app/docs/proxy/users) |
| Global budget cap | `general_settings.max_budget` | **BLOCK** | [LiteLLM budgets](https://litellm.vercel.app/docs/proxy/users) |
| Budget alert (soft limit) | `soft_budget` on key; sends Slack/email alert | **WARN** | [LiteLLM budgets](https://litellm.vercel.app/docs/proxy/users) |
| Fail closed during outage | `fail_closed_budget_enforcement: true` | **BLOCK (503)** | [LiteLLM config settings](https://docs.litellm.ai/docs/proxy/config_settings) |
| Model allowlist per key | `models: [...]` on virtual key | **BLOCK (auth error)** | [LiteLLM virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys) |
| TPM/RPM limits | `tpm_limit`, `rpm_limit` on key or deployment | **BLOCK (429)** | [LiteLLM budgets](https://litellm.vercel.app/docs/proxy/users) |
| Prompt caching auto-injection | `cache_control_injection_points` in `litellm_params` | Enforcement (always caches) | [LiteLLM prompt caching tutorial](https://docs.litellm.ai/docs/tutorials/prompt_caching) |
| Cache-friendly routing | `router_settings.optional_pre_call_checks: ["prompt_caching"]` | Enforcement (routing) | [LiteLLM GitHub issue #6784](https://github.com/BerriAI/litellm/issues/6784) |
| Block guardrail violation | Custom guardrail `mode: post_call` returning block | **BLOCK (400)** | [LiteLLM guardrails](https://docs.litellm.ai/docs/proxy/guardrails/quick_start) |
| Prevent teams disabling guardrails | `metadata.guardrails.modify_guardrails: false` | **BLOCK (403)** | [LiteLLM guardrails](https://docs.litellm.ai/docs/proxy/guardrails/quick_start) |
| Required params on every request | `general_settings.enforced_params` | **BLOCK (400)** | [LiteLLM enterprise](https://docs.litellm.ai/docs/proxy/enterprise) |

---

## 4. Telemetry / Observability as Enforcement

**Sources:**  
- [Claude Code Monitoring (OTel)](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage), published 2026-06-22  
- [Helicone custom rate limits](https://docs.helicone.ai/features/advanced-usage/custom-rate-limits)  
- [Langfuse token & cost tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking), 2026-05-18  
- [AIWatcher cost alerts 2026](https://www.getaiwatcher.com/blog/how-to-set-up-cost-alerts-for-ai-agents-in-2026), 2026-06-05  
- [Cycles AI cost control landscape 2026](https://runcycles.io/blog/ai-agent-cost-control-2026-litellm-helicone-openrouter-runtime-authority), 2026-04-06  

### 4.1 Claude Code OpenTelemetry

Claude Code emits OTel metrics and events natively. Enable with:
```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://beast.amplified.internal:4317
```

Administrators can push these variables via `managed-settings.json` under the `env` key — they cannot be overridden by users.

**Key token metrics emitted:**

| Metric | Description | OTel type |
|---|---|---|
| `claude_code.token.usage` | Token count per API request | Counter, per `type` (input/output/cacheRead/cacheCreation) |
| `claude_code.cost.usage` | Cost in USD per API request | Counter |
| `claude_code.session.count` | Sessions started | Counter |
| `claude_code.lines_of_code.count` | Lines added/removed | Counter |

**Key span attributes on `claude_code.llm_request`:**

| Attribute | Value |
|---|---|
| `input_tokens` | Input token count |
| `output_tokens` | Output token count |
| `cache_read_tokens` | Tokens served from prompt cache |
| `cache_creation_tokens` | Tokens written to cache |
| `effort` | `low`/`medium`/`high`/`xhigh`/`max` |
| `model` | Model identifier |
| `stop_reason` | `end_turn`, `max_tokens`, `tool_use`, etc. |
| `mcp_server.name` / `mcp_tool.name` | MCP attribution (requires `OTEL_LOG_TOOL_DETAILS=1`) |

**`stop_reason: "max_tokens"`** in OTel tells you the model was truncated — a key signal for tuning max_tokens caps.

**Distributed tracing (beta):**
```bash
export CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1
export OTEL_TRACES_EXPORTER=otlp
```
Traces link each user prompt → API calls → tool executions as a single trace, enabling end-to-end latency and cost attribution per task.

### 4.2 LiteLLM Spend Tracking and Prometheus

LiteLLM tracks spend per key, user, and team in its database. Prometheus metrics are emitted out of the box:
```yaml
general_settings:
  alerting:
    - slack
  alerting_threshold: 300    # alert when 80% of budget consumed
  alert_types:
    - budget_alerts
    - spend_reports
    - failed_tracking
```

LiteLLM publishes Prometheus metrics that can feed Grafana dashboards and PagerDuty/Slack alerts. Budget exhaustion is a **hard block** (HTTP 402), not just an alert.

### 4.3 Helicone

Helicone acts as a pass-through proxy with cost-based rate limiting. Route via Helicone by setting the base URL:
```python
client = openai.OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={"Helicone-Auth": f"Bearer {HELICONE_API_KEY}"}
)
```

**Cost-based rate limiting (hard block — returns 429):**
```
"Helicone-RateLimit-Policy": "500;w=3600;u=cents;s=user"
# Limits each user to $5.00/hour; returns 429 when exceeded
```

Helicone alerts go to Slack, email, or webhook. Token-based rate limiting is listed as "coming soon" (as of 2026-06-24). Current limits are by request count or cost-in-cents.

### 4.4 Langfuse

Langfuse records generations with full token breakdowns. It does **not** natively block requests; it is a measurement and alerting layer.

**Programmatic daily cost check (cron-based enforcement loop):**
```typescript
// Run as cron job — if over threshold, revoke key or page on-call
const metrics = await langfuse.api.traces.list({ fromTimestamp: last24h });
if (dailyCost > ALERT_THRESHOLDS.dailyCritical) {
  await revokeKey(devKey);   // hard enforcement via LiteLLM API
  await sendAlert("CRITICAL", `Daily LLM cost: $${dailyCost.toFixed(2)}`);
}
```

Langfuse → measurement → trigger → LiteLLM key revocation is the enforcement loop. Langfuse itself cannot block requests.

### 4.5 Can Telemetry Trigger Automated Cutoffs?

| Tool | Can auto-block? | Mechanism |
|---|---|---|
| **LiteLLM** | **Yes** | Budget exhaustion → HTTP 402 automatically; Prometheus alert → external webhook → key revocation via API |
| **Helicone** | **Yes** | `Helicone-RateLimit-Policy` header → HTTP 429 on cost/request threshold |
| **Claude Code OTel** | **No direct block** | Emits metrics to collector; collector (e.g. Grafana/PagerDuty) must trigger action via external webhook or LiteLLM key revocation |
| **Langfuse** | **No direct block** | Measurement only; must drive enforcement via external script/webhook |

### 4.6 Enforcement Table — Telemetry

| Rule | Mechanism | Block or Warn | Source |
|---|---|---|---|
| Token usage per session tracking | `claude_code.token.usage` OTel metric | Measure (feeds alerting) | [Claude Code monitoring, 2026-06-22](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage) |
| Cache efficiency tracking (`cacheRead` vs `input` tokens) | OTel `cache_read_tokens` / `cache_creation_tokens` attributes | Measure | [Claude Code monitoring, 2026-06-22](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage) |
| MCP vs CLI tool call ratio | OTel `mcp_tool.name` + `mcp_server.name` vs `Bash` tool | Measure | [Claude Code monitoring, 2026-06-22](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage) |
| Admin-mandated OTel endpoint | `OTEL_EXPORTER_OTLP_ENDPOINT` in managed-settings.json `env` block | **Enforce telemetry collection** | [Claude Code monitoring, 2026-06-22](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage) |
| Spend alert → key revocation | LiteLLM Prometheus alert → webhook → `/key/block` API | **BLOCK (on trigger)** | [LiteLLM virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys) |
| Cost-based rate limiting per user | Helicone `Helicone-RateLimit-Policy: "500;w=3600;u=cents;s=user"` | **BLOCK (429)** | [Helicone rate limits](https://docs.helicone.ai/features/advanced-usage/custom-rate-limits) |
| Daily cost cron + key revocation | Langfuse Metrics API → cron script → LiteLLM key block | **BLOCK (on threshold)** | [Langfuse token tracking, 2026-05-18](https://langfuse.com/docs/observability/features/token-and-cost-tracking) |

---

## 5. CI / Git Hooks / Harnesses

These are development-lifecycle enforcement points — they run before code is committed or agents are launched.

### 5.1 Pre-commit Hooks

Use [pre-commit](https://pre-commit.com/) or git's native `pre-commit` hook for static checks that fail CI before code is merged.

**CLAUDE.md / MEMORY.md size limit check:**
```bash
#!/bin/bash
# .git/hooks/pre-commit (or pre-commit config hook)
set -e

MAX_LINES=200
for f in $(find . -name "CLAUDE.md" -o -name "*.md" -path "*/.claude/*"); do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt "$MAX_LINES" ]; then
    echo "ERROR: $f has $lines lines (max $MAX_LINES). Trim before committing."
    exit 1
  fi
done
```
Anthropic's own docs recommend CLAUDE.md under 200 lines; [Claude Code memory reference](https://code.claude.com/docs/en/memory) notes that longer files consume more context and reduce adherence.

**Banned verbosity patterns:**
```bash
# Check for known verbosity anti-patterns in CLAUDE.md
if grep -qE "(always explain|provide detailed|comprehensive analysis|step-by-step breakdown)" .claude/CLAUDE.md 2>/dev/null; then
  echo "ERROR: CLAUDE.md contains verbosity-encouraging phrases. Remove them."
  exit 1
fi
```

**Ignore files / `.gitignore` presence:**
```bash
if [ ! -f .claudeignore ] || [ ! -f .gitignore ]; then
  echo "ERROR: .claudeignore and .gitignore are required"
  exit 1
fi
```

### 5.2 CI Checks (GitHub Actions / GitLab CI)

```yaml
# .github/workflows/token-hygiene.yml
name: Token Hygiene
on: [pull_request]

jobs:
  claude-md-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check CLAUDE.md size
        run: |
          MAX=200
          for f in $(find . -name "CLAUDE.md"); do
            LINES=$(wc -l < "$f")
            if [ "$LINES" -gt "$MAX" ]; then
              echo "::error file=$f::CLAUDE.md exceeds $MAX lines ($LINES found)"
              exit 1
            fi
          done

      - name: Verify .claudeignore exists
        run: test -f .claudeignore || (echo "::error::Missing .claudeignore" && exit 1)

      - name: Verify hooks config
        run: |
          jq '.hooks.PreToolUse' .claude/settings.json > /dev/null 2>&1 || \
            (echo "::error::.claude/settings.json missing PreToolUse hooks" && exit 1)
```

### 5.3 Launcher / Harness Scripts (Cannot-Launch-Without-Efficient-Config)

A wrapper script ensures developers cannot invoke Claude Code directly without efficiency flags. This is the "harness" pattern:

```bash
#!/bin/bash
# /usr/local/bin/claude-beast (replaces direct `claude` invocation)
# Enforced by: symlink, PATH override, or shell alias locked in /etc/profile.d/

set -e

# --- Mandatory efficiency config ---
EFFICIENCY_FLAGS=(
  "--bare"                                       # skip CLAUDE.md auto-discovery (CI/agentic mode)
  "--exclude-dynamic-system-prompt-sections"    # stable system-prompt for cache reuse
  "--max-budget-usd" "${CLAUDE_MAX_BUDGET:-5.00}"
  "--max-turns" "${CLAUDE_MAX_TURNS:-40}"
)

# --- Inject mandatory system prompt appendix ---
EFFICIENCY_RULES=$(cat /etc/claude-code/efficiency-rules.txt)
EFFICIENCY_FLAGS+=(
  "--append-system-prompt" "$EFFICIENCY_RULES"
)

# --- Model enforcement (block non-approved models) ---
ALLOWED_MODEL="${CLAUDE_MODEL:-claude-sonnet-4-6}"
EFFICIENCY_FLAGS+=("--model" "$ALLOWED_MODEL")

# --- Point at Beast proxy ---
export ANTHROPIC_BASE_URL="https://beast.amplified.internal"
export CLAUDE_CODE_PROPAGATE_TRACEPARENT=1

exec /usr/local/bin/claude-real "${EFFICIENCY_FLAGS[@]}" "$@"
```

**Deployment:** Install this script system-wide. Lock `~/.bashrc` / `/etc/profile.d/claude-alias.sh` to alias `claude` to `claude-beast`. Developers who bypass the wrapper bypass the proxy credential too (their API key only works via Beast).

**Thinking token cap injection:**
```bash
# In the harness or in managed-settings.json env block
export MAX_THINKING_TOKENS=8000
```

### 5.4 Enforcement Table — CI / Harness

| Rule | Mechanism | Block or Warn | Source |
|---|---|---|---|
| CLAUDE.md ≤ 200 lines | pre-commit / CI shell check, `exit 1` | **BLOCK (commit/PR fails)** | [Claude Code memory docs](https://code.claude.com/docs/en/memory) (recommendation) |
| `.claudeignore` and `.gitignore` present | CI `test -f` check | **BLOCK** | Best practice |
| Hooks config in `.claude/settings.json` | CI `jq` validation | **BLOCK** | Best practice |
| No verbosity-encouraging phrases in CLAUDE.md | CI `grep` pattern check | **BLOCK** | Best practice |
| `--bare` flag always set | Launcher harness | **BLOCK (no launch without)** | [CLI ref](https://backgroundclaude.com/cli-reference) |
| `--max-budget-usd` always set | Launcher harness | **BLOCK (abort on cap)** | [CLI ref](https://backgroundclaude.com/cli-reference) |
| `--max-turns` always set | Launcher harness | **BLOCK (exit on limit)** | [CLI ref](https://backgroundclaude.com/cli-reference) |
| `--exclude-dynamic-system-prompt-sections` | Launcher harness | Cache improvement | [CLI ref](https://backgroundclaude.com/cli-reference) |
| Efficiency rules always appended | `--append-system-prompt` in launcher | Prompt-level guidance | [CLI ref](https://backgroundclaude.com/cli-reference) |
| All traffic via Beast proxy | `ANTHROPIC_BASE_URL` in harness; API key only valid through proxy | **BLOCK (credential gates)** | Best practice |

---

## 6. General Principle: Hard Block vs. Nudge

### 6.1 What Is Technically Enforceable (Hard Block)

| Rule type | Hard block available? | Best lever |
|---|---|---|
| **Model selection** | Yes | Claude Code managed settings `availableModels`; LiteLLM key `models`; Cursor Enterprise model blocklist |
| **Max output tokens** | Yes | LiteLLM `max_tokens` in `litellm_params`; Claude Code `--max-budget-usd` (cost proxy) |
| **Max input tokens / context window** | Yes | LiteLLM `enable_pre_call_checks` + `model_info.max_input_tokens`; Cursor admin blocks Max Mode |
| **Thinking tokens** | Yes | Claude Code managed settings `MAX_THINKING_TOKENS`; `effortLevel: "low"` |
| **MCP tool calls** | Yes | Claude Code `PreToolUse` hook matching `mcp__.*` with `permissionDecision: "deny"` |
| **Budget (hard cap)** | Yes | LiteLLM `max_budget` per key → HTTP 402; Helicone cost rate limit → 429; Cursor team hard spend cap |
| **CLAUDE.md size** | Yes (at commit time) | Pre-commit / CI exit 1 |
| **Prompt caching** | Yes (injection) | LiteLLM `cache_control_injection_points`; cache-friendly routing |
| **Model routing (CLI over MCP preferred)** | Partial — can block MCP, cannot force CLI | `PreToolUse` deny MCP; system prompt rules to prefer CLI |

### 6.2 What Is Only Nudgeable (Warn / Measure)

| Rule type | Why hard block is unavailable | Best available lever |
|---|---|---|
| **Output verbosity** | LLM output is generative; no pre-call token count exists for output | (1) `max_tokens` cap at proxy (limits length but not content quality); (2) System prompt rules (`alwaysApply`); (3) `Stop` hook reading `last_assistant_message` and blocking + requesting shorter response (iterative, max 8 blocks); (4) OTel `output_tokens` measurement + trend alerting |
| **Lean code style** | Model discretion | System prompt rules + OTel output_tokens trend |
| **Explicit thinking off when not needed** | Cannot dynamically inject `MAX_THINKING_TOKENS` per-prompt without a hook | `UserPromptSubmit` hook that conditionally adds `MAX_THINKING_TOKENS=0` env hint based on prompt content; or set low globally |
| **Cache-stable prefix wording** | User can still modify CLAUDE.md locally | CI check on CLAUDE.md line count + managed claudeMd in managed settings |

### 6.3 Output Verbosity: Best Available Stack

Since model output length is generative, no single mechanism hard-blocks it. The best available stack in priority order:

1. **`max_tokens` cap at proxy** (LiteLLM `litellm_params.max_tokens`) — hard upper bound on token count, but a terse 4096-token response and a verbose 4096-token response are both allowed. This is a necessary but insufficient control.

2. **System prompt rules** (Claude Code managed `claudeMd`, Cursor enforced Team Rules, `--append-system-prompt` in launcher) — model-level guidance. Reliable for compliant models with good instruction-following; can be overridden by verbose user prompts.

3. **`Stop` hook** — reads `last_assistant_message`, measures length, blocks with "please be more concise" instruction if over threshold. Iterative (adds tokens per loop) and capped at 8 blocks. Use only for extreme violations.

4. **OTel `output_tokens` trend + alerting** — measures whether efficiency rules are working over time. Feed into weekly review. Trigger key revocation if chronic over-use.

5. **`PostToolUse` / `PostToolBatch` context injection** — after tool results, reinforce "lean output" framing before Claude generates the response. Reduces verbosity in tool-heavy sessions.

---

## 7. Rule → Best Enforcement Point (Master Table)

| Rule from Token-Efficiency Plan | Primary Enforcement Point | Mechanism | Block or Warn | Secondary / Fallback |
|---|---|---|---|---|
| **Lean output (short responses)** | LiteLLM proxy | `max_tokens` in `litellm_params` (hard cap on length) | **BLOCK** (length cap only) | Claude Code `Stop` hook (iterative block); System prompt rules (nudge) |
| **Prompt caching** | LiteLLM proxy | `cache_control_injection_points` on system message; `optional_pre_call_checks: ["prompt_caching"]` | **Enforce** (auto-inject) | Claude Code `--exclude-dynamic-system-prompt-sections` (stable prefix); Managed CLAUDE.md via `claudeMd` setting |
| **CLI over MCP** | Claude Code hooks | `PreToolUse` matching `mcp__.*` → `permissionDecision: "deny"` | **BLOCK** | System prompt rules in CLAUDE.md / Team Rules (nudge) |
| **Model allowlist / no Max Mode** | Claude Code managed settings | `availableModels` + `enforceAvailableModels: true` in managed-settings.json | **BLOCK** | LiteLLM key `models` allowlist (proxy-side); Cursor Enterprise model blocklist |
| **Thinking token cap** | Claude Code managed settings | `MAX_THINKING_TOKENS=8000` (or `0`) in managed-settings.json `env` block | **BLOCK (hard cap)** | Launcher harness `export MAX_THINKING_TOKENS=...`; `effortLevel: "low"` |
| **Cache-stable system-prompt prefix** | Claude Code launcher harness | `--exclude-dynamic-system-prompt-sections` flag + `--append-system-prompt` with fixed wording | **Enforce** (structural) | LiteLLM `cache_control_injection_points`; Managed `claudeMd` |
| **Budget hard cap per developer** | LiteLLM proxy | Virtual key `max_budget` per developer key → HTTP 402 | **BLOCK** | Cursor Enterprise per-team hard limit; `--max-budget-usd` in launcher |
| **Budget alerting (soft)** | LiteLLM proxy | `soft_budget` on key; Slack/email at 80% | **WARN** | Helicone cost rate limit; Claude Code OTel → Grafana alert |
| **Max turns per agentic run** | Launcher harness | `--max-turns 40` in launcher script | **BLOCK (exits)** | LiteLLM `tpm_limit` (velocity limit) |
| **CLAUDE.md ≤ 200 lines** | CI / pre-commit | Shell check `wc -l > 200` → `exit 1` | **BLOCK (commit)** | Managed `claudeMd` overrides local file; `--bare` flag skips CLAUDE.md |
| **Ignore files present** | CI | `test -f .claudeignore` → `exit 1` on absence | **BLOCK (PR)** | Best practice |
| **Hooks config locked (no user override)** | Claude Code managed settings | `allowManagedHooksOnly: true` in managed-settings.json | **BLOCK** | CI validation of `.claude/settings.json` |
| **Routing: cheap model for simple tasks** | LiteLLM proxy | Model-group routing by request tag; `model_group_alias` mappings | **Enforce** (routing) | System prompt rules suggesting haiku for simple tasks |
| **No spend above $X/dev/month** | LiteLLM proxy + telemetry | Per-key `max_budget` + `budget_duration: "30d"` | **BLOCK** | OTel `claude_code.cost.usage` → alert → key revocation |
| **Token-efficiency trend tracking** | OTel + LiteLLM | `claude_code.token.usage` (cacheRead vs input ratio); LiteLLM Prometheus `spend` per model | **Measure** → alert | Weekly Grafana dashboard review; Langfuse daily cost cron |

---

## Appendix: Source Registry

| Source | URL | Date |
|---|---|---|
| Claude Code Hooks Reference | https://docs.anthropic.com/en/docs/claude-code/hooks | 2026-06-16 |
| Claude Code Settings | https://docs.anthropic.com/en/docs/claude-code/settings | 2026-06-22 |
| Claude Code Monitoring (OTel) | https://docs.anthropic.com/en/docs/claude-code/monitoring-usage | 2026-06-22 |
| Claude Code Memory Reference | https://code.claude.com/docs/en/memory | 2026 |
| Claude Code CLI Reference | https://backgroundclaude.com/cli-reference | 2026 |
| Cursor Changelog — May 2026 controls | https://cursor.com/changelog/05-04-26 | 2026-05-04 |
| Cursor Rules Reference (community) | https://github.com/sanjeed5/awesome-cursor-rules-mdc/blob/main/cursor-rules-reference.md | 2025-02-17 |
| Cursor Forum — per-member limits | https://forum.cursor.com/t/set-each-members-usage-quota-in-the-team-version/159792/7 | 2026-05-05 |
| Pondero — Cursor Enterprise May 2026 | https://pondero.ai/coding/guides/cursor-enterprise-admin-controls-may-2026/ | 2026-05-05 |
| LiteLLM Budgets & Rate Limits | https://litellm.vercel.app/docs/proxy/users | 2023-12-22 |
| LiteLLM Guardrails Quick Start | https://docs.litellm.ai/docs/proxy/guardrails/quick_start | current |
| LiteLLM Config Settings | https://docs.litellm.ai/docs/proxy/config_settings | current |
| LiteLLM Virtual Keys | https://docs.litellm.ai/docs/proxy/virtual_keys | 2023-11-24 |
| LiteLLM Prompt Caching Tutorial | https://docs.litellm.ai/docs/tutorials/prompt_caching | current |
| LiteLLM Prompt Cache Routing (GitHub issue #6784) | https://github.com/BerriAI/litellm/issues/6784 | 2024-11-17 |
| LiteLLM Enterprise Features | https://docs.litellm.ai/docs/proxy/enterprise | current |
| LiteLLM Custom Auth / Model Enforcement | https://docs.litellm.ai/docs/proxy/custom_auth | current |
| Helicone Custom Rate Limits | https://docs.helicone.ai/features/advanced-usage/custom-rate-limits | current |
| Langfuse Token & Cost Tracking | https://langfuse.com/docs/observability/features/token-and-cost-tracking | 2026-05-18 |
| Cycles — AI Agent Cost Control 2026 | https://runcycles.io/blog/ai-agent-cost-control-2026-litellm-helicone-openrouter-runtime-authority | 2026-04-06 |
| AIWatcher — Cost Alerts for AI Agents 2026 | https://www.getaiwatcher.com/blog/how-to-set-up-cost-alerts-for-ai-agents-in-2026 | 2026-06-05 |
