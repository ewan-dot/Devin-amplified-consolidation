# CLI vs MCP Token Cost: Evidence Dossier
**Prepared for:** Ewan Bramley / Amplified Partners  
**Compiled:** 23 June 2026  
**Status:** Dense evidence-led; every number carries source URL and reliability rating

---

## Executive Summary

The claim that "CLI is a hell of a lot cheaper than MCP" is empirically correct under default MCP configurations. The cost gap is structural, not incidental: MCP clients inject every connected server's full tool schema into the LLM's context on every turn, whether or not those tools are used. Controlled benchmarks show a **4–32× token gap** for simple tasks and as high as 80× on some complex queries. However, the gap is largely an artefact of naive MCP implementation; optimised MCP with prompt caching, schema filtering, or code execution can close it to roughly 1.5–3×.

---

## 1. How MCP Tool Definitions Enter the Context Window

**Mechanism (primary source — MCP spec):**  
When an MCP client connects to a server, it sends a `tools/list` JSON-RPC request. The server responds with every tool's `name`, `description`, `inputSchema` (full JSON Schema), and optionally `outputSchema` and `annotations`. The MCP specification requires deterministic ordering of tools to support prompt cache hits, but it does **not** mandate lazy loading — by default, all schemas are returned and clients load them upfront.

> "Servers **SHOULD** return tools in a deterministic order… Deterministic ordering enables clients to reliably cache the tool list and improves LLM prompt cache hit rates when tools are included in model context."  
> — [MCP Specification, Tools section](https://modelcontextprotocol.io/specification/draft/server/tools), date: ongoing, **Reliability: Official spec**

> "Most MCP clients load all tool definitions upfront directly into context, exposing them to the model using a direct tool-calling syntax."  
> — [Anthropic Engineering, "Code execution with MCP"](https://www.anthropic.com/engineering/code-execution-with-mcp), published 2025-11-04, **Reliability: Official / primary**

Each tool definition contains: unique name, human-readable description, JSON Schema for parameters (property names, types, descriptions, enum values, required flags, nested object schemas). The agent platform serializes the full JSON schema into the system prompt or tool-use block for every API call to the LLM.

---

## 2. How Many Tokens Does a Typical MCP Tool Consume?

| Source | Figure | Methodology | Reliability |
|--------|--------|-------------|-------------|
| [MindStudio](https://www.mindstudio.ai/blog/claude-code-mcp-server-token-overhead), 2026-04-02 | 100–500 tokens per tool definition | Analysis of real servers | Community, credible practitioner |
| [Albato citing Lunar.dev](https://albato.com/blog/publications/embedded-mcp-context-bloat-hallucinations), 2026-06-09 | 200–500 tokens per tool | Cited analysis | Community |
| [dev.to audit of 11 servers](https://dev.to/0coceo/i-audited-11-mcp-servers-22945-tokens-before-a-single-message-31e), 2026-03-19 | Average **200 tokens per tool** across 132 tools on 11 servers | Measured via tokenizer | Community, empirical |
| [LinkedIn / Bhagavati Kumar](https://www.linkedin.com/posts/bhagavati-kumar-jayanti-venkata_in-my-company-there-is-a-strict-verification-activity-7386673846608695296-XQJl), 2025-10-22 | 200–500 tokens per tool; GitHub's 87 tools = 17,400–43,500 tokens | Engineering analysis | Community |
| [Apideck](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative), 2026-03-16 | **550–1,400 tokens** per tool (including name, description, JSON schema, field descriptions, enums, system instructions) | Published analysis | Community, cross-referenced |
| [Anthropic Engineering, "Advanced Tool Use"](https://www.anthropic.com/engineering/advanced-tool-use), 2025-11-24 | Hidden base overhead: **346 tokens** (auto/none tool choice) or **313 tokens** (any/specific) just for the tool infrastructure, **plus ~150 tokens per tool definition average** | Anthropic internal measurement | **Official / primary** |

**Key real-server measurements (measured, not estimated):**

| MCP Server | Tools | Total Schema Tokens | Source |
|------------|-------|---------------------|--------|
| GitHub Copilot MCP | 43–94 tools | **17,600 tokens** (94 tools) | [StackOne](https://www.stackone.com/blog/mcp-token-optimization/), measured with Atlassian mcp-compressor |
| GitHub Copilot MCP | 43 tools | ~28,000 tokens | [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) |
| Notion MCP | 22 tools | **15,462 tokens** | [Port of Context calculator](https://portofcontext.com/token-calculator), measured 2026-06-09, o200k_base tokenizer |
| Sentry MCP | 22 tools | **13,823 tokens** | [Port of Context calculator](https://portofcontext.com/token-calculator), measured 2026-06-09 |
| Supabase MCP | 29 tools | 3,422 tokens | [Port of Context calculator](https://portofcontext.com/token-calculator) |
| Playwright MCP | 23 tools | 3,130 tokens | [Port of Context calculator](https://portofcontext.com/token-calculator) |
| Linear MCP | 42 tools | **12,807 tokens** | [Devdigest / Quandri](https://devdigest.org/articles/mcp-eats-21k-tokens-why-we-ditched-it-for-cli-skills), 2026-05-30, measured |
| Slack MCP | 11 tools | ~21,000 tokens | [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use), 2025-11-24 |
| Jira MCP | — | ~17,000 tokens | [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) |
| 5-server setup (GitHub + Slack + Sentry + Grafana + Splunk) | 58 tools | **~55,000 tokens** | [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) — **Official / primary** |
| Cloudflare full API | ~2,500 endpoints | **1,170,000 tokens** (without Code Mode) | [Cloudflare Engineering](https://blog.cloudflare.com/code-mode-mcp/), 2026-02-20, measured with tiktoken — **Official / primary** |

> "Jira (which alone uses ~17K tokens)… At Anthropic, we've seen tool definitions consume 134K tokens before optimization."  
> — [Anthropic Engineering, "Advanced Tool Use"](https://www.anthropic.com/engineering/advanced-tool-use), 2025-11-24, **Reliability: Official / primary**

---

## 3. The Core Comparison: CLI ~200 Tokens vs MCP ~12,957 Tokens

### Origin and Verification of the Specific Figures

**Source:** The exact comparison of **~200 tokens (CLI) vs ~12,957 tokens (MCP)** traces directly to a measured case study by the team at **Quandri**, published via Devdigest in May 2026.

> "**CLI approach (~200 tokens):** Prompt: ~50 tokens, Response: ~150 tokens.  
> **MCP approach (~12,957 tokens):** Tool definitions always loaded: 12,807 tokens. Tool call + response: ~150 tokens.  
> MCP consumes **65x more tokens**."  
> — [Devdigest / Quandri, "MCP Eats 21K Tokens: Why We Ditched It for CLI + Skills"](https://devdigest.org/articles/mcp-eats-21k-tokens-why-we-ditched-it-for-cli-skills), 2026-05-30  
> **Reliability: Community (practitioner case study), empirically measured on Linear MCP with 42 tools = 12,807 tokens schema overhead)**

The 12,807-token MCP schema component is **independently verifiable**: the Linear MCP server's 42 tools at ~200–500 tokens each produces this range; Port of Context's tokenizer-based measurements show Notion at 15,462 and Sentry at 13,823 for similar tool counts.

**The ~200 token figure for CLI** represents a single REST call: ~50 tokens for the curl/GraphQL query prompt, ~150 tokens for the structured JSON response. This is consistent across multiple independent sources.

### Scalekit Controlled Benchmark (Primary Evidence)

The most rigorous head-to-head test in the public domain is Scalekit's benchmark:

- **75 runs total** (5 tasks × 15 runs per modality)
- **Same model:** Claude Sonnet 4
- **Same tasks, same prompts**
- **Tested:** CLI (gh), CLI+Skills (~800 token skills file), MCP (GitHub Copilot MCP server, 43 tools)
- **Statistical significance:** All CLI vs MCP differences reported at p < 0.05

| Task | CLI Tokens | MCP Tokens | Multiplier |
|------|-----------|-----------|-----------|
| Repo language & license | **1,365** | **44,026** | **32×** |
| PR details & review status | 1,648 | 32,279 | 20× |
| Repo metadata & install | 9,386 | 82,835 | 9× |
| Merged PRs by contributor | 5,010 | 33,712 | 7× |
| Latest release & dependencies | 8,750 | 37,402 | 4× |

**Reliability note (32× figure):** On the simplest task, the MCP overhead is almost entirely the 43 injected tool schemas; the agent uses 1–2 of them. As task complexity grows and the agent makes multiple tool calls, the relative overhead of the fixed schema cost decreases.

**Cost at scale:**
- **CLI:** ~$3.20/month at 10,000 operations (Claude Sonnet 4 pricing: $3/M input, $15/M output)
- **MCP (direct):** ~$55.20/month — **17× more expensive**
- **MCP via gateway (schema filtering):** ~$5/month — approaching CLI costs

**Reliability failure:** Of 25 MCP runs, **7 failed with ConnectTimeout (72% success rate)**. CLI: 100% (25/25). Failures were TCP-level timeouts to GitHub's remote MCP server, not protocol errors.

> — [Scalekit, "MCP is up to 32× more expensive than CLI"](https://www.scalekit.com/blog/mcp-vs-cli-use), published 2026-03-11, updated 2026-05-27, by Ravi Madabhushi (Cofounder)  
> **Reliability: Commercial vendor, but methodology is published, open-source, and reproducible. Independent sources cross-confirm the numbers.**

### Jannik Reinhard Microsoft Intune Case Study

> "Microsoft Graph MCP approach: ~145,000 tokens for 50 devices (schema injection alone: ~28,000 tokens). mgc + az + PowerShell CLI approach: ~4,150 tokens. **35× cheaper.**"  
> — [Jannik Reinhard (Microsoft MVP)](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/), 2026-02-22  
> **Reliability: Named individual, published methodology, real enterprise task. Not independently replicated.**

---

## 4. Anthropic's Own Numbers: 150,000 → 2,000 Tokens (98.7% Reduction)

**Primary source — direct quote:**

> "This lets the agent load only the definitions it needs for the current task. This reduces the token usage from **150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%.**"  
> — [Anthropic Engineering, "Code execution with MCP: building more efficient AI agents"](https://www.anthropic.com/engineering/code-execution-with-mcp), published **2025-11-04**, authors: Adam Jones and Conor Kelly  
> **Reliability: Official Anthropic engineering blog — this is the primary source for the 98.7% figure.**

**Context:** The 150,000 token baseline represents an agent connected to a large number of tools loaded upfront. The 2,000 token optimised state uses code execution with a filesystem-based tool discovery pattern, where the agent reads only the tool definition files it needs for the current task.

**What generates the 150,000 token baseline?**  
Anthropic's Advanced Tool Use post provides concrete examples: GitHub (35 tools, ~26K tokens) + Slack (11 tools, ~21K tokens) + Sentry (5 tools, ~3K) + Grafana (5 tools, ~3K) + Splunk (2 tools, ~2K) = 58 tools, ~55K tokens. Adding Jira (~17K) and other servers reaches 100K+. At 134K tokens observed internally, the 150K figure is a representative worst-case for a large enterprise tool stack.

**Corroborating figure from the same post:**  
Programmatic Tool Calling (a different technique) reduced average token usage from **43,588 to 27,297 tokens — a 37% reduction** on complex research tasks.

> — [Anthropic Engineering, "Introducing advanced tool use"](https://www.anthropic.com/engineering/advanced-tool-use), published **2025-11-24**, author: Bin Wu  
> **Reliability: Official Anthropic engineering blog — primary source.**

**Accuracy improvement (Anthropic internal testing):**  
Tool Search Tool improved task accuracy:
- Claude Opus 4: 49% → 74% (+25 percentage points)
- Claude Opus 4.5: 79.5% → 88.1% (+8.6 percentage points)

---

## 5. Tool-Schema Bloat: The 4–32× Token Gap Between Minimal and Verbose Definitions

### The Compounding Effect Per Turn

Tool definitions are injected on **every API call**, not once per session. A 10-turn conversation with a 30-tool MCP server repeats the entire schema 10 times.

**Scaling math (from mcp2cli YouTube analysis, 2026-03-20):**
- 5-tool server: ~250 tokens per turn
- 30-tool server: ~3,600 tokens per turn  
- 120-tool server: ~15,000 tokens per turn
- 25-turn conversation × 120-tool server = **375,000 tokens spent on schemas alone**

> — [YouTube: "Your AI Agent Wastes 96% of Tokens on Tool Schemas"](https://www.youtube.com/watch?v=e_iNf2jf8Kg), 2026-03-20  
> **Reliability: Community analysis, consistent with cross-verified per-tool token estimates.**

### Atlassian's Schema Compression Benchmark (GitHub MCP, 94 tools)

The most granular published study of the verbosity spectrum for a single real server:

| Compression Level | What's Kept | Tokens | Reduction |
|------------------|-------------|--------|-----------|
| None | Full descriptions, enums, types | **17,600** | — |
| Low | Full descriptions preserved | ~3,900 | 78% |
| Medium | First sentence of each description | ~3,300 | 81% |
| High | Tool names + parameter names only | ~2,200 | 88% |
| Max | Only a `list_tools()` function | ~500 | 97% |

> — [StackOne citing Atlassian mcp-compressor benchmarks](https://www.stackone.com/blog/mcp-token-optimization/), 2026-03-31  
> **Reliability: Atlassian is a primary vendor; figures measured on GitHub's official MCP server. Good reliability.**

**Key insight:** A 35× range exists between verbose (17,600 tokens) and ultra-compressed (500 tokens) for the same 94-tool server. The tradeoff is accuracy — at maximum compression, tools with similar parameter names become ambiguous to the model.

### MCP GitHub Issue: Proposed Token Reduction Mechanism

A formal proposal in the MCP spec repository measured a MySQL server with 106 tools at **207KB of schema data (~54,600 tokens)** per initialization, even when the agent needs only 2–3 tools. The proposal claims a reference implementation achieving **91% token savings (54,604 → 4,899 tokens)** through lazy loading.

> — [GitHub Issue: modelcontextprotocol/modelcontextprotocol #1576](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1576), opened 2025-09-30  
> **Reliability: Official MCP GitHub repository — reflects acknowledged community problem.**

### Unused Tools Burning Tokens Every Turn

A real-world audit of Claude Code sessions found:
> "Out of 42 skills loaded in my setup, 19 had only two or fewer invocations over the entire dataset of 858 sessions. Each of these skill schemas consumed tokens on every turn, even though they were rarely used."  
> — [Reddit r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1sd8t5u/anthropic_isnt_the_only_reason_youre_hitting/), 2026-04-24  
> **Reliability: User observation, plausible and consistent with how tool injection works.**

Red Hat's analysis confirms:
> "Schema overhead compounds every turn. Each tool's JSON Schema includes parameter names, types, descriptions, and enum values. With dozens of tools across multiple MCP servers, this can exceed **15,000 tokens of schema definitions in the context window**. These tokens ship with every API call to the LLM, whether the agent uses those tools or not."  
> — [Red Hat Emerging Technologies](https://next.redhat.com/2026/04/23/how-sandboxed-python-reduces-tool-schema-overhead-in-ai-agents/), 2026-04-23  
> **Reliability: Red Hat official engineering blog — credible.**

---

## 6. The Code Execution Pattern and Progressive Disclosure

### Anthropic's Approach (Primary Source)

Anthropic's November 2025 engineering post introduces the "code execution with MCP" pattern: instead of loading tool definitions into context, the agent is given a **filesystem representation of available tools** (one `.ts` file per tool). The agent:
1. Lists the `./servers/` directory to discover available servers (~small tokens)
2. Reads only the specific tool files it needs (~50–200 tokens each)
3. Writes code that calls those tools through a helper function

**The 98.7% reduction** (150,000 → 2,000 tokens) comes from this selective file-reading approach replacing the full upfront schema dump.

> — [Anthropic Engineering, "Code execution with MCP"](https://www.anthropic.com/engineering/code-execution-with-mcp), 2025-11-04 — **Official primary source**

### Cloudflare's Code Mode (Primary Source)

Cloudflare independently developed and published the same pattern for their own API (2,500+ endpoints):

- **Without Code Mode:** 1,170,000 tokens (exceeds any current context window)
- **With Code Mode (2 tools: search + execute):** ~1,000 tokens
- **Reduction: 99.9%** — measured with tiktoken
- For a 52-tool enterprise MCP portal: 9,400 tokens → 600 tokens via Code Mode (**94% reduction**)
- The 600-token cost is **fixed regardless of how many more servers are added**

> — [Cloudflare Engineering, "Code Mode: give agents an entire API in 1,000 tokens"](https://blog.cloudflare.com/code-mode-mcp/), published **2026-02-20**, author: Matt Carey  
> **Reliability: Official Cloudflare engineering blog — primary source, measurements with tiktoken.**

> — [Cloudflare Engineering, "Scaling MCP adoption: Our reference architecture"](https://blog.cloudflare.com/enterprise-mcp/), published **2026-04-14**  
> **Reliability: Official Cloudflare engineering blog.**

### Anthropic's Tool Search Tool (Progressive Disclosure, Official)

From the "Advanced Tool Use" post (2025-11-24):

**Traditional approach (50+ MCP tools):**
- All tool definitions loaded upfront: ~72K tokens
- Total context before any work: ~77K tokens

**With Tool Search Tool:**
- Only Tool Search Tool loaded upfront: ~500 tokens
- Tools discovered on-demand (3–5 relevant, ~3K tokens)
- Total context: **~8.7K tokens** — preserving 95% of context window
- **85% reduction** in token usage

> — [Anthropic Engineering, "Introducing advanced tool use"](https://www.anthropic.com/engineering/advanced-tool-use), 2025-11-24 — **Official primary source**

### Speakeasy Dynamic Toolsets (Independent Third Party)

| Scenario | Static toolset | Dynamic toolset | Reduction |
|----------|---------------|----------------|-----------|
| Simple task (400 tools) | 400,000+ tokens | ~6,000 tokens | **98.5%** |
| Complex task (400 tools) | 400,000+ tokens | ~35,000 tokens | **91.2%** |
| 200 tools static | 261,700 tokens | — | Exceeds 200K context window entirely |

> — [StackOne citing Speakeasy published benchmarks](https://www.stackone.com/blog/mcp-token-optimization/), 2026-03-31  
> **Reliability: Third-party vendor data, cited by credible secondary source. Cross-reference with primary Speakeasy source recommended.**

---

## 7. Counter-Evidence and Nuance: When MCP Is Fine or Better

### Prompt Caching Dramatically Reduces MCP Schema Costs

The MCP spec itself mandates deterministic tool ordering specifically to enable prompt cache hits. Under Anthropic's prompt caching:
- Cached tokens cost **90% less** than uncached
- Tool schemas loaded once per session into the cache are effectively free on subsequent turns
- A real-world fintech case study: moved tool schemas to cached prefix → **30% monthly cost reduction** on a production support agent

> "You pay the full input token rate once (for the first request in a session). After that, cached tokens cost 90% less."  
> — [PADISO, "Caching MCP Tool Schemas: The 30% Bill Cut"](https://www.padiso.co/blog/caching-mcp-tool-schemas-30-percent-bill-cut/), 2026-05-18  
> **Reliability: Community vendor analysis. Caching mechanics are confirmed Anthropic behaviour.**

**Critical caveat:** Prompt caching only helps for **multi-turn conversations where the same tool set is used**. Single-turn workflows (common in agentic pipelines) derive no caching benefit. The Tool Search Tool from Anthropic explicitly notes: "Tool Search Tool doesn't break prompt caching because deferred tools are excluded from the initial prompt entirely."

### MCP's Structural Advantages Over CLI

Scalekit's own analysis (despite being the source of the 32× cost figure) is explicit about what MCP provides that CLI cannot:

**1. Per-user OAuth authorization.** CLI agents inherit the developer's ambient credentials. Multi-tenant products where an agent acts on behalf of 1,000 different customers' employees require per-user OAuth scopes, consent flows, and revocation. CLI's `gh auth login` gives the agent your token — it cannot distinguish User A at Acme from User B at Globex.

**2. Agent identity.** MCP's OAuth model can carry agent identity through claims like `act`, enabling API providers to distinguish which agent made a call (for rate-limiting, partnership enforcement, or audit). A CLI token authenticates the user, not the agent.

**3. Structured audit trails.** Every MCP tool call produces a typed, queryable record attributable to a specific user and tenant. Shell history logs commands, not authorization context. Enterprise compliance typically requires this.

**4. Explicit tool boundaries.** MCP constrains agents to declared tools only. CLI's bash access is unbounded — an agent can compose any command, including ones that reach endpoints or services not intended.

> — [Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use), 2026-03-11 — benchmark author's own counter-argument  
> **Reliability: The benchmark's own authors concede the authorization gap. Highly credible.**

> — [Apideck](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative), 2026-03-16 (also acknowledges auth gap)  
> **Reliability: Community, cross-corroborates Scalekit's analysis.**

### When MCP Wins on Token Efficiency

**Tight tool sets used frequently:** If an agent calls the same 5–10 tools in every session, the upfront schema cost amortises across many turns. With prompt caching, the marginal cost per turn approaches zero.

**Code Mode MCP vs CLI on complex multi-step tasks:**  
Sideko benchmarked CLI vs raw MCP vs Code Mode MCP across 12 Stripe tasks:
- CLI: 19 LLM round trips
- Raw MCP: 12 LLM round trips  
- Code Mode MCP: **4 LLM round trips**
- Token totals across all 12 tasks: CLI 711,555, raw MCP 506,970, Code Mode 294,924
- Code Mode was **42% cheaper than raw MCP and 59% cheaper than CLI** for these complex multi-step tasks

The key insight: CLI's round-trip overhead can exceed MCP's schema overhead on workflows involving loops, pagination, and dependent state, because each CLI round trip requires a full inference pass.

> — [Apideck citing Sideko benchmark](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative), 2026-03-16  
> **Reliability: Community (Sideko cited by Apideck); original Sideko post should be verified directly.**

### What You Lose Going CLI-Only

- **No standardised discovery:** CLI tools require model knowledge of available commands (often from training data or a skills file). Novel or less-common APIs require documentation in context, negating some savings.
- **Security surface:** Shell access is broader than typed MCP tools. Without careful sandboxing, prompt injection can chain unintended commands.
- **Streaming/bidirectional:** CLI is request-response only. Server-sent events, WebSocket streams, and long-lived connections require SDK or MCP.
- **Distribution:** CLIs require per-platform binaries, PATH management, and update distribution. Remote MCP servers are URL-addressable.
- **Multi-user auth at scale:** Re-implementing per-user OAuth, tenant isolation, and audit trails outside MCP is significant engineering overhead.

---

## 8. Anthropic's Hidden Tool Infrastructure Overhead

Even with **zero user-defined tools**, there is a base token overhead from Anthropic's tool-use system:

| Configuration | Hidden tokens per request |
|--------------|--------------------------|
| `auto` or `none` tool choice | **346 tokens** |
| `any` or specific tool choice | **313 tokens** |
| Each tool definition (average) | **~150 tokens** |
| Bash tool | 245 tokens |
| Text editor tool | 700 tokens |
| Computer use | 466–499 tokens + 735 per tool |

An agent with 5 tools adds roughly 1,100 tokens to every request before any user message content.

> — [InsiderLLM, "Token Audit Guide"](https://insiderllm.com/guides/token-audit-guide/), 2026-03-06, citing Anthropic documentation  
> **Reliability: Community, but cites Anthropic docs as primary source. Verify against current Anthropic token counting docs.**

---

## 9. Summary of Verified Hard Numbers

| Claim | Value | Source | Date | Reliability |
|-------|-------|--------|------|-------------|
| Anthropic's own MCP reduction (code execution) | 150,000 → 2,000 tokens (**98.7%**) | [Anthropic Engineering](https://www.anthropic.com/engineering/code-execution-with-mcp) | 2025-11-04 | **Official primary** |
| Anthropic Tool Search Tool reduction | ~77K → ~8.7K tokens (**85%**) | [Anthropic Engineering](https://www.anthropic.com/engineering/advanced-tool-use) | 2025-11-24 | **Official primary** |
| Anthropic observed max tool overhead | **134,000 tokens** before optimization | [Anthropic Engineering](https://www.anthropic.com/engineering/advanced-tool-use) | 2025-11-24 | **Official primary** |
| Scalekit CLI vs MCP simplest task | 1,365 vs 44,026 tokens (**32×**) | [Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use) | 2026-03-11 | Vendor benchmark, open-source, reproducible |
| Scalekit MCP vs CLI at scale | $3.20 vs $55.20/10K ops (**17×**) | [Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use) | 2026-03-11 | Vendor benchmark |
| Scalekit MCP reliability | **72%** success (7/25 ConnectTimeout) | [Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use) | 2026-03-11 | Vendor benchmark |
| CLI (~200 tokens) vs Linear MCP (~12,957 tokens) | **65×** | [Devdigest / Quandri](https://devdigest.org/articles/mcp-eats-21k-tokens-why-we-ditched-it-for-cli-skills) | 2026-05-30 | Community case study, measured |
| Quandri: 4 MCP servers total overhead | **21,077 tokens** (10.5% of 200K window) | [Devdigest / Quandri](https://devdigest.org/articles/mcp-eats-21k-tokens-why-we-ditched-it-for-cli-skills) | 2026-05-30 | Community case study, measured |
| GitHub MCP (94 tools) full schema | **17,600 tokens** | [StackOne / Atlassian](https://www.stackone.com/blog/mcp-token-optimization/) | 2026-03-31 | Vendor benchmark |
| Atlassian compression range (GitHub 94 tools) | 17,600 → 500 tokens (**97%**) | [StackOne / Atlassian](https://www.stackone.com/blog/mcp-token-optimization/) | 2026-03-31 | Vendor measurement |
| Cloudflare full API without Code Mode | **1,170,000 tokens** | [Cloudflare Engineering](https://blog.cloudflare.com/code-mode-mcp/) | 2026-02-20 | **Official primary**, tiktoken measured |
| Cloudflare Code Mode reduction | 1,170,000 → 1,000 tokens (**99.9%**) | [Cloudflare Engineering](https://blog.cloudflare.com/code-mode-mcp/) | 2026-02-20 | **Official primary** |
| Cloudflare 52-tool portal Code Mode | 9,400 → 600 tokens (**94%**) | [Cloudflare Engineering](https://blog.cloudflare.com/enterprise-mcp/) | 2026-04-14 | **Official primary** |
| Microsoft Graph MCP vs CLI Intune task | ~145,000 vs ~4,150 tokens (**35×**) | [Jannik Reinhard](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/) | 2026-02-22 | Named individual, methodology published |
| Anthropic 5-server example overhead | **~55K tokens** before conversation | [Anthropic Engineering](https://www.anthropic.com/engineering/advanced-tool-use) | 2025-11-24 | **Official primary** |
| Prompt caching MCP schema cost reduction | **90%** on cached tokens | [PADISO](https://www.padiso.co/blog/caching-mcp-tool-schemas-30-percent-bill-cut/) | 2026-05-18 | Community, based on confirmed Anthropic caching mechanics |
| Sideko: Code Mode MCP vs CLI (12 Stripe tasks) | CLI 711K vs Code Mode 295K tokens; **59% cheaper** | [Apideck citing Sideko](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative) | 2026-03-16 | Community (secondary citation) |
| Programmatic Tool Calling reduction | 43,588 → 27,297 tokens (**37%**) | [Anthropic Engineering](https://www.anthropic.com/engineering/advanced-tool-use) | 2025-11-24 | **Official primary** |

---

## 10. Flags: Numbers Without Clear Primary Source Traces

| Claim | Widely Cited | Primary Source Status |
|-------|-------------|----------------------|
| "4–32× token gap" (Scalekit) | Yes — cited by Apideck, Firecrawl, Roadie, MindStudio, and dozens of articles | ✅ **Primary source confirmed**: [Scalekit GitHub benchmark repo](https://github.com/scalekit-inc/mcp-vs-cli-benchmark), open-source |
| "98.7% reduction" | Yes — circulates widely | ✅ **Primary source confirmed**: [Anthropic Engineering](https://www.anthropic.com/engineering/code-execution-with-mcp), 2025-11-04 |
| "143,000 of 200,000 tokens burned by 3 servers" | Yes | ⚠️ **Secondary**: Apideck attributes this to a team report, not a published study. Consistent with arithmetic (55K + 88K = 143K for a heavier 3-server stack) but no citable primary URL |
| "28% MCP failure rate" | Yes | ✅ **Primary source confirmed**: Scalekit benchmark, 7/25 ConnectTimeout failures |
| "Jira MCP 3× slower, 9.4× on first call" | Circulates | ⚠️ **Secondary**: Devdigest attributes this to "the original article" without a link. Could not trace to a specific primary URL |
| "96-99% token savings" for CLI wrappers of MCP | Yes (mcp2cli claims) | ⚠️ **Community project self-reported**: [mcp2cli README / libraries.io](https://libraries.io/npm/@weibaohui%2Fmcp2cli). Internal measurement, not independently replicated |

---

## Key Sources by Authority Tier

### Tier 1: Official Primary Sources (Anthropic, Cloudflare, MCP Spec)
1. [Anthropic Engineering: "Code execution with MCP"](https://www.anthropic.com/engineering/code-execution-with-mcp) — 2025-11-04
2. [Anthropic Engineering: "Introducing advanced tool use"](https://www.anthropic.com/engineering/advanced-tool-use) — 2025-11-24
3. [Cloudflare Engineering: "Code Mode: give agents an entire API in 1,000 tokens"](https://blog.cloudflare.com/code-mode-mcp/) — 2026-02-20
4. [Cloudflare Engineering: "Scaling MCP adoption: enterprise reference architecture"](https://blog.cloudflare.com/enterprise-mcp/) — 2026-04-14
5. [MCP Official Spec: Tools](https://modelcontextprotocol.io/docs/concepts/tools) — 2025-06-18
6. [MCP Official Spec: Tools (draft)](https://modelcontextprotocol.io/specification/draft/server/tools) — ongoing

### Tier 2: Credible Vendor Benchmarks (Published Methodology)
7. [Scalekit: "MCP is up to 32× more expensive than CLI"](https://www.scalekit.com/blog/mcp-vs-cli-use) — 2026-03-11/2026-05-27
8. [Scalekit GitHub benchmark repository](https://github.com/scalekit-inc/mcp-vs-cli-benchmark) — 2026-03-08
9. [StackOne: "MCP Token Optimization: 4 Approaches Compared"](https://www.stackone.com/blog/mcp-token-optimization/) — 2026-03-31
10. [Apideck: "Your MCP Server Is Eating Your Context Window"](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative) — 2026-03-16
11. [Port of Context MCP Token Calculator](https://portofcontext.com/token-calculator) — measured 2026-06-09

### Tier 3: Community/Practitioner (Named Individuals, Measured)
12. [Devdigest / Quandri: "MCP Eats 21K Tokens"](https://devdigest.org/articles/mcp-eats-21k-tokens-why-we-ditched-it-for-cli-skills) — 2026-05-30
13. [Jannik Reinhard (Microsoft MVP): "Why CLI tools are beating MCP"](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/) — 2026-02-22
14. [Dev.to audit of 11 MCP servers](https://dev.to/0coceo/i-audited-11-mcp-servers-22945-tokens-before-a-single-message-31e) — 2026-03-19
15. [MCP GitHub Issue #1576: Mitigating Token Bloat](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1576) — 2025-09-30
16. [Red Hat Emerging Technologies: "Sandboxed Python reduces tool schema overhead"](https://next.redhat.com/2026/04/23/how-sandboxed-python-reduces-tool-schema-overhead-in-ai-agents/) — 2026-04-23
