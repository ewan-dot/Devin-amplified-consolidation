---
title: "Token-Reduction Prior Art — IDEs, Consumer UIs, CLI-vs-MCP, and AI-Internal Habits"
document_type: "research_conclusion"
artifact_id: "token-reduction-prior-art__research-conclusion__agent-doc__v01__2026-06-23__perplexity"
date_utc: "2026-06-23T19:30:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"
stage: "research"
objective: "Catalogue, with citable numbers, every lever that reduces token/credit spend across IDEs, consumer AI UIs, the CLI-vs-MCP boundary, and AI-internal habits — as the evidence base for §4 of the estate token-efficiency spec."
reader: "agent"
source_refs:
  - "https://www.anthropic.com/engineering/code-execution-with-mcp"
  - "https://www.anthropic.com/engineering/advanced-tool-use"
  - "https://blog.cloudflare.com/code-mode-mcp/"
  - "https://www.scalekit.com/blog/mcp-vs-cli-use"
  - "https://github.com/scalekit-inc/mcp-vs-cli-benchmark"
  - "https://devdigest.org/articles/mcp-eats-21k-tokens-why-we-ditched-it-for-cli-skills"
  - "https://www.stackone.com/blog/mcp-token-optimization/"
  - "https://docs.cursor.com/en/context/rules"
  - "https://docs.anthropic.com/en/docs/claude-code/monitoring-usage"
  - "https://aider.chat/docs/usage/caching.html"
  - "https://www.anthropic.com/engineering/multi-agent-research-system"
  - "local: research_cli_vs_mcp.md"
  - "local: research_ide_controls.md"
  - "local: research_context_habits.md"
  - "local: memory/sessions/.../agent_control_surfaces.md (2026-06-21)"
  - "local: memory/sessions/.../token-budget-prior-art-integration (2026-06-22)"
origin_type: "agent_synthesis"
attribution: "External claims cited inline with URL + date. Synthesis and tiering by Perplexity Computer. Internal prior art attributed to prior Amplified sessions."
epistemic_tier: "STRUCTURED"
tier_reason: "Official-doc and reproducible-benchmark numbers organised into a reusable lever catalogue. Vendor figures are MEASURED at source but not re-run by us; estate-specific savings remain INTUITED until our own cost log runs."
epistemic_role: "evidence_map"
effective_tier_rule: "min-rule"
preconditions:
  - "Vendor pricing/behaviour current as of fetch date (fast-moving; see valid_until)."
  - "Provider terms permit the routing/caching pattern used."
valid_until: "2026-09-23"
claim_scope: "Token/credit reduction levers and their published magnitudes; not estate-measured savings."
contradiction_status: "clean"
known_contradictions:
  - "CLI is cheaper than MCP on simple/single tool calls, but CLI round-trip overhead can EXCEED MCP on complex multi-step workflows (Sideko, 12 Stripe tasks). Both true; scope-dependent."
machine_action_allowed: "recommend"
system_of_record: "Drive (human-facing) + GitHub (estate-cost-tools docs); this draft = local_workspace"
ratifier: "Ewan"
next_action: "Fold the verified levers + corrected numbers into §4 of the estate spec; mark which are config-bakeable now vs need the router."
companion_human_doc: "token-reduction-prior-art__human-brief (same date)"
outcome_routing:
  outcome_class: "methodology_candidate"
  outcome_reason: "Produces a reusable, tiered lever catalogue that feeds the estate spec and a future per-IDE config bake; not itself a production gate."
  required_next_action: "Bake config levers per IDE lane; verify the two flagged figures (62% re-sent context; Pool 1/Pool 2 status) before any external/investor citation."
  research_needed: false
  tangent_refs: []
  methodology_refs: ["context-engineering lever catalogue", "credit-first routing", "CLI-over-MCP for read-only doors"]
---

# Token-Reduction Prior Art

TIER: STRUCTURED · vendor numbers MEASURED-at-source (cited) · estate savings INTUITED until our cost log runs
PROVENANCE: 3 external research passes (CLI-vs-MCP, IDE controls, context habits) + 2 internal Amplified prior-art docs. Full dossiers in workspace: `research_cli_vs_mcp.md`, `research_ide_controls.md`, `research_context_habits.md`.
GOAL-LINK: this is the evidence under §4 of the estate spec. It converts "we should use caching/CLI/Haiku" from assertion (STRUCTURED-by-vibe) to cited magnitudes, so the config bake is defensible.

## What exists — the answer to your question, in one line each

Your instinct holds: **CLI is materially cheaper than MCP for the read-only doors** — but the win comes from the same root cause as every other lever here: **stop sending tokens the model doesn't need this turn.** Four families of lever do that.

---

## A. CLI vs MCP — your instinct, verified (and the one caveat)

**Verified, primary sources:**
- MCP clients inject **every connected server's full tool schema into context on every turn**, used or not ([Anthropic, "Code execution with MCP"](https://www.anthropic.com/engineering/code-execution-with-mcp), 2025-11-04). This is the structural cost.
- Anthropic measured **tool definitions consuming 134,000 tokens** in their own systems before optimisation; their code-execution pattern cut a representative stack **150,000 → 2,000 tokens (98.7%)** ([Anthropic, "Code execution with MCP"](https://www.anthropic.com/engineering/code-execution-with-mcp), 2025-11-04).
- Controlled benchmark, Claude Sonnet 4, 75 runs, open-source: simplest task **1,365 (CLI) vs 44,026 (MCP) tokens = 32×**; at scale **$3.20 vs $55.20 per 10K ops = 17×**; MCP reliability **72%** (7/25 ConnectTimeout) vs CLI 100% ([Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use), 2026-03-11; [benchmark repo](https://github.com/scalekit-inc/mcp-vs-cli-benchmark)).
- The specific "~200 vs ~12,957" figure you carry: traced to a measured Linear-MCP case — 42 tools = **12,807 tokens** of permanent schema vs a single CLI/GraphQL call ~200 tokens = **65×** ([Devdigest/Quandri](https://devdigest.org/articles/mcp-eats-21k-tokens-why-we-ditched-it-for-cli-skills), 2026-05-30). Real but a *community* case study, not a primary benchmark — the **32× and 98.7% are the citable primaries**.
- Per-tool cost: **~150 tokens/tool** average + 313–346 token base infra overhead ([Anthropic, "Advanced Tool Use"](https://www.anthropic.com/engineering/advanced-tool-use), 2025-11-24). Real servers: GitHub 94 tools ≈ 17,600 tok; Slack 11 ≈ 21,000 tok; a 5-server stack ≈ 55,000 tok (same source).

**The caveat (contradiction, both true, scope-dependent):**
- On **complex multi-step** workflows, CLI's per-call round-trip can cost *more* than MCP: 12 Stripe tasks — CLI 711K tok / raw MCP 507K / Code-Mode MCP 295K; **Code Mode 59% cheaper than CLI** ([Apideck citing Sideko](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative), 2026-03-16, secondary). Each CLI round trip is a full inference pass.
- MCP also buys things CLI can't at protocol level: **per-user OAuth, tenant isolation, structured audit trails, bounded tool surface** ([Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use), the benchmark author's own concession). Matters when acting on behalf of *other people's* users — not your own workflow.
- **Caching closes most of the MCP gap:** schema in a cached prefix → 90% off on repeat turns ([Anthropic caching mechanics]; community case 30% bill cut, [PADISO](https://www.padiso.co/blog/caching-mcp-tool-schemas-30-percent-bill-cut/), 2026-05-18). Only helps multi-turn with a stable tool set.

**Estate rule (STRUCTURED):** CLI-over-MCP for **read-only, single-shot doors** (Brain/Research/CRM reads, `gh`) — that's where the 17–65× lives and where you have no multi-tenant need. Keep MCP only where you need a stable, heavily-cached tool set or genuine OAuth/audit. For big APIs, the **code-execution / progressive-disclosure pattern** (Anthropic Tool Search 85% off; Cloudflare Code Mode 99.9%) beats both.

---

## B. AI-internal habits — the biggest single lever is caching

**Prompt/context caching (the top lever, MEASURED at source):**
- Anthropic & Google: **90% off** cached input ($0.30 vs $3.00/M, Sonnet). OpenAI: **50–75% off**, automatic. DeepSeek: up to **98% off**. (`research_context_habits.md`, provider pricing pages.)
- **Cache-stable prefix discipline:** keep system prompt + tool defs + instructions byte-identical; push every variable (timestamps, IDs, per-machine paths) to the tail. A single byte change in the prefix invalidates the cache. Worked example: $720→$72/mo (90%) from stable prefix alone.
- **Batch × cache stacks multiplicatively on Anthropic** (batch 50% × cache) ≈ **95–98% off input**; **OpenAI and Google batch do NOT stack with cache** (confirmed). Provider choice per lane matters.

**Context compaction / re-sent context:**
- Anthropic cookbook: compaction cut **204K → 82K tokens (58.6%)** over 2 events (official).
- The "**~62% of an average agentic bill is re-sent context**" figure: attributed to *Stanford Digital Economy Lab, "Agentic AI Cost Attribution," 2025*, corroborated by a LeanOps production audit — but the **primary academic URL was not independently retrieved**. ⚠️ FLAG: do not use in any external/investor citation until the primary is verified.

**Sub-agent / model routing (MEASURED at source):**
- Opus orchestrator + Sonnet sub-agents beat single-agent Opus by **90.2%** on Anthropic's research eval; token usage explains **80% of performance variance**; multi-agent uses ~15× the tokens of chat ([Anthropic, "multi-agent research system"](https://www.anthropic.com/engineering/multi-agent-research-system), 2025). Implication: route mechanical work to cheap models, reserve frontier for judgment. Community 80/15/5 splits report 45–55% cost cuts.

**Repo maps / structural context:** Aider tree-sitter map default **~1K tokens** for whole-repo structure vs reading files (official). The "87% reduction" vs whole-file is a *community* benchmark (hypergrep), flagged community.

**Retrieval / pre-filtering:** ripgrep/`mdfind` to narrow before feeding the model — community benchmarks 87–90% fewer tokens; embedding search ~50× vs grep+read on big repos. (Community-tier; mechanism sound.)

**Local-model offload:** mechanical tasks on Ollama/Qwen = **$0 API tokens** (electricity ≈ $0.0003/M). The estate's M4 mini lane.

**Output discipline:** output tokens cost **5× input** (Claude), 6–8× (GPT-5.4/Gemini). Stop sequences −20–40% output; structured output −30–50%; a concision instruction measured −24.7% output / −20.7% cost with +9.1 F1 (community). Output is the expensive side — keep it tight.

---

## C. IDE / consumer-UI knobs (config-bakeable now)

Per-tool, the levers that actually move spend (full tables in `research_ide_controls.md`):

| Tool | Highest-value knobs | Note |
|---|---|---|
| **Cursor** | Auto mode (not Max Mode — Max = ~5× context expansion); pin model at job start; `.cursorignore`/`.cursorindexingignore`; `.cursor/rules/*.mdc` with **glob frontmatter** (not `alwaysApply: true`); `@`-references over broad index; spend cap | Pricing moved to pool-charged; verify current Auto behaviour |
| **Claude Code** | Automatic caching (95%+ hit in active sessions); `/compact` **within the 5-min cache window**; `/clear` between tasks; Haiku-pinned sub-agents; **`MAX_THINKING_TOKENS` cap = single biggest single lever, −30–40%**; `/effort low`; CLAUDE.md <200 lines, no mid-session edits; `--bare`, `--exclude-dynamic-system-prompt-sections` | ⚠️ FLAG: the **Pool 1 / Pool 2 split** (announced ~May 2026 for 15 Jun) appears **paused/not shipped** per the IDE research — the spec's Pool-2 warning must be re-checked against current Anthropic terms before relying on it |
| **GitHub Copilot** | Premium-request multipliers (0×–30×); included models (GPT-4.1/4o/5-mini = 0×); Auto selection −10%; `#file` over `@workspace`; "Enhance non-chat requests" off; admin budget/block | Multiplier table is the spend map |
| **Windsurf/Cascade** | SWE-1.5 = 0 credits; BYOK; third-party model multipliers; Flow-Action credits removed Apr 2025 | |
| **Cline / Roo** | Automatic 3-point caching; Auto Compact; `/smol`, `/newtask`; deduped file reads; lazy MCP docs; watch the 1M-context price cliff | |
| **Aider** | `--map-tokens` (map is 50–60% of session tokens); `--cache-prompts` + keepalive (−70% input); `--architect`/`--editor-model` split (−30–50%); `--weak-model`; `--max-chat-history-tokens` | Strong, scriptable per-task routing via `.aider.conf.yml` |
| **Gemini CLI / Codex CLI / Zed** | Free tier (Gemini 1,000 req/day $0); `/model` (8× spread); cached input (Codex 90%); watch >200K/272K long-context surcharges; Zed local Ollama $0 | |
| **Consumer UIs** | Model selection; Projects/Gems/Custom Instructions to avoid re-pasting context; memory; mind context bloat | Perplexity's search architecture = lower bloat risk |

---

## What it means (for the estate spec)

1. **The four §4 axes are now evidence-backed**, not asserted. Caching is the top lever; CLI-over-MCP is verified for read-only doors; Haiku-routing and local-offload have hard magnitudes.
2. **Three corrections to carry into the spec:**
   - The flagship CLI-vs-MCP primaries are **32× (Scalekit)** and **98.7% (Anthropic)** — cite those, treat the 65×/200-vs-12,957 as a supporting community case.
   - **Re-check the Pool 1/Pool 2 status** — it may not have shipped; the spec's §6 Pool-2 trap depends on it.
   - The **62% re-sent-context** figure is not yet primary-sourced — keep it internal until verified.
3. **CLI is not universally cheaper** — on complex multi-step loops, prefer code-execution/progressive-disclosure (Anthropic Tool Search / Cloudflare Code Mode), not raw CLI round-trips.

## What to change next
- Fold A–C into estate spec §4 with these citations; tag each lever **config-bakeable-now** vs **needs-router**.
- Verify the two flagged figures before any external use.
- Per IDE lane, write the actual config file (ignore files, rules globs, thinking-token caps, model pins) — that's the bake.

## Not yet verified
- Estate-specific savings (need our own cost log — the §9 proof run in the spec).
- Sideko original post (only seen via Apideck secondary).
- Speakeasy dynamic-toolset numbers (via StackOne secondary).
- Current Cursor Auto pricing and Anthropic Pool status (fast-moving; verify at bake time).

— Pipe discipline: this is a draft in the workspace. Route human brief → Drive, agent doc → estate-cost-tools/docs via the pipe; Vellum event drafted separately. Nothing written direct to Beast.
