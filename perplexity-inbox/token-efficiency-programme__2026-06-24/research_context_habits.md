# Context-Engineering Habits: Token-Reduction Techniques for AI Agents

**Prepared for:** Ewan Bramley / Amplified Partners  
**Date:** 23 June 2026  
**Scope:** Internal AI-agent behaviours that cut token spend — independent of IDE.

---

## Summary table

| # | Technique | Peak cost reduction | Source quality |
|---|-----------|--------------------:|----------------|
| 1 | Prompt / context caching | Up to **90% off** cached input (Anthropic/DeepSeek); 50% off (OpenAI auto) | Official pricing pages |
| 2 | Cache-stable prefix design | **90% off** the stable portion; effective ~96% with compaction stacked | Official docs + practitioner data |
| 3 | Context compaction / summarisation | **58.6%** token reduction (Anthropic cookbook); **62%** re-sent context share (Stanford DEL) | Official cookbook + academic audit |
| 4 | Sub-agent / model routing | **45–75%** cost reduction; Haiku ~⅓ price of Sonnet | Official Anthropic research + pricing |
| 5 | Repo maps (Aider / tree-sitter) | **~1 K tokens** vs entire file tree; up to **87%** less in smart-search wrappers | Official Aider docs; DEV benchmark |
| 6 | Batch APIs | **50% off** (Anthropic + OpenAI); stacks with cache → **~95–98% off** input (Anthropic); Google: **does NOT stack** | Official batch docs |
| 7 | Local model offload (Ollama / Qwen) | **$0 API tokens** for offloaded tasks; cloud API cost ≈ $2–3/M → $0 | Practitioner benchmarks |
| 8 | Retrieval / pre-filtering (ripgrep) | **87–90% fewer tokens** consumed by search steps | DEV benchmark; Medium case study |
| 9 | Output-token discipline | Output costs **4–5× input**; structured output saves 30–50% output tokens; stop sequences 20–40% | Official pricing ratios; practitioner benchmarks |

---

## 1. Prompt caching / context caching

### Mechanism
On every API call the provider checks whether the leading token prefix (system prompt + tools + earlier messages) matches a previously stored KV-cache entry. On a cache hit the tokens are served from DRAM/disk rather than recomputed through all transformer layers, enabling a dramatic pricing discount.

### Exact discounts by provider (June 2026)

| Provider | Model example | Cache-read price | vs. input price | TTL | Cache-write surcharge | Minimum cacheable |
|----------|--------------|----------------:|----------------:|-----|----------------------|-------------------|
| **Anthropic** | Claude Sonnet 4.6 ($3.00/M in) | $0.30/M | **10% of input = 90% off** | 5 min (default); 1-hour option | 1.25× input (5-min); 2× input (1-hr) | 1 024 tokens (most models); 512 (Fable 5 / Mythos 5) |
| **Anthropic** | Claude Haiku 4.5 ($1.00/M in) | $0.10/M | 10% | same | same | 4 096 tokens |
| **Anthropic** | Claude Opus 4.8 ($5.00/M in) | $0.50/M | 10% | same | same | 1 024 tokens |
| **OpenAI** | GPT-4.1 ($3.00/M in) | $0.75/M | **25% of input = 75% off** | 5–10 min inactive; up to 1 hr off-peak | None (automatic) | 1 024 tokens; cache in 128-token increments |
| **OpenAI** | GPT-4o ($3.75/M in) | $1.875/M | 50% of input = 50% off | same | None | same |
| **Google Gemini** | Gemini 2.5 Flash ($0.30/M in) | $0.03/M (standard mode) | **10% of input = 90% off** | Explicit TTL set by caller; storage billed separately at $1.00/M tokens/hr | Storage fee | 2 048 tokens |
| **Google Gemini** | Gemini 2.5 Pro ($1.25/M in ≤200 K) | $0.125/M | 10% | same | Storage $4.50/M tokens/hr | 2 048 tokens |
| **DeepSeek** | V4-Flash ($0.14/M in) | $0.0028/M | **2% of input = 98% off** | A few hours to a few days (auto-cleared when unused) | None stated; automatic | 1 024 tokens (must match byte-for-byte) |
| **DeepSeek** | V4-Pro ($0.435/M in, promo) | $0.003625/M | ~0.8% of input | same | None stated | same |

**Sources:**  
- Anthropic pricing (June 2026): https://www.anthropic.com/pricing  
- Anthropic prompt-caching docs: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching  
- OpenAI prompt-caching guide: https://platform.openai.com/docs/guides/prompt-caching  
- OpenAI pricing page: https://platform.openai.com/docs/pricing  
- Google Gemini pricing: https://ai.google.dev/gemini-api/docs/pricing  
- DeepSeek pricing: https://api-docs.deepseek.com/quick_start/pricing  
- DeepSeek cache guide: https://api-docs.deepseek.com/guides/kv_cache  

### What invalidates the cache

**Anthropic:** Cache hierarchy is `tools → system → messages`. Any change at a level invalidates that level **and all subsequent levels**. Specific invalidators: modifying tool definitions (names/descriptions/params); toggling web search, citations, or speed settings; adding/removing images anywhere; changes to extended thinking settings (enable/disable, budget). The `cache_control` marker must be in exactly the same byte position on every request — any prefix drift misses the cache entirely.  
Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

**OpenAI:** Cache cleared after ~5–10 minutes of inactivity (up to 1 hr off-peak). Any change to the prefix (even a single character) is a cache miss. High concurrency (>~15 req/min for the same prefix) can cause overflow to fresh machines.  
Source: https://platform.openai.com/docs/guides/prompt-caching

**DeepSeek:** Requires a **full, byte-identical prefix match** of a previously persisted cache-prefix unit. Even `A + C` will not hit the cache for `A + B`. Common-prefix detection can auto-persist a shared prefix after two diverging requests, but only after that divergence is observed.  
Source: https://api-docs.deepseek.com/guides/kv_cache

### Key magnitude

Anthropic's own documentation cites a **100 K-token book prompt dropping from 11.5 s to 2.4 s** with caching (85% latency reduction). At standard pricing, 90% cost reduction on the cached portion means a stable 5 K-token system prompt sent 100 times costs the equivalent of 6 500 tokens total instead of 500 000. A production coding-agent deployment (Requesty, 12-month study, April 2026) found platform-wide cache hit rates rising from 52% to 86%, with Claude Code reaching 92% cache hit rates and an effective input token rate of ~$0.30/M vs the $3.00/M list price — a **10× real-world cost compression**.  
Sources: https://www.requesty.ai/coding-agent-economy; https://www.anthropic.com/pricing

### Provider classification

| Aspect | Anthropic | OpenAI | Google Gemini | DeepSeek |
|--------|-----------|--------|---------------|----------|
| Cache discount | **90% off** | **50–75% off** | **90% off** (+ storage fee) | **98% off** |
| Explicit opt-in required? | Yes (`cache_control` breakpoints) | No (automatic for ≥1 024 tokens) | Both (explicit + implicit auto-cache on 2.5+) | No (automatic) |
| Batch stacks with cache? | **Yes** (explicitly stated) | **No** (unavailable on Batch API) | **No** ("Context Caching is not currently supported with the Batch API") | Not stated |

---

## 2. Cache-stable prefix design

### Mechanism
Because any byte-level change to the cached prefix invalidates the entry, the single most impactful structural habit is **front-loading everything static and pushing all dynamic content to the tail**:

```
[STATIC — cached]
  ├── System prompt (instructions, persona, constraints)
  ├── Tool definitions (complete JSON schemas)
  ├── Static context (repo conventions, style guide)
  └── Few-shot examples (if fixed)

[DYNAMIC — never cached]
  ├── Conversation history / tool results
  └── Current user message (including timestamps, request IDs, session tokens)
```

Dynamic values (timestamps, user IDs, session tokens) injected into the system prompt **destroy the cache on every call**. Moving them to message-level parameters costs nothing and preserves the cache hit rate.

### Quantified savings
At Anthropic's pricing, with Claude Sonnet 4.6:
- Standard input: $3.00/M  
- Cache read: $0.30/M  
- A 5 K-token system prompt sent with every one of 1 000 agent steps: **5 M tokens billed at $3.00/M = $15.00** without caching vs. **1 cache write (6 250 tokens at $3.75/M = $0.023) + 999 reads (4 995 K tokens at $0.30/M = $1.50) = ~$1.52 total** — a **90% reduction** on that prefix.

The Requesty 12-month study found Claude Code's 92% cache hit rate delivers an effective input cost of ~$0.30/M vs. $3.00/M list — a **5.4× cost advantage** over a comparable tool (Kilo Code) running at 46% cache hit rate.  
Source: https://www.requesty.ai/coding-agent-economy

A documented single-developer case went from **$720/month to $72/month (90% reduction)** solely by implementing stable system prompts with `cache_control` breakpoints.  
Source: https://zylos.ai/research/2026-05-02-ai-agent-cost-engineering-token-economics/ (Zylos, May 2026)

### Official classification: Official (Anthropic docs); corroborated by production data.

---

## 3. Context compaction / summarisation

### Mechanism
Mid-session, once the accumulated context exceeds a threshold (e.g. 80% of context window), the agent pauses, instructs the model to summarise all completed work into a compact state representation, clears the full conversation history, and resumes with only the summary. This breaks the quadratic token-accumulation pattern inherent to append-only agent loops.

Anthropic's SDK `compaction_control` parameter automates this:
1. Monitors token usage per turn  
2. At threshold: injects a summary-request user turn  
3. Model generates summary wrapped in `<summary>` tags  
4. History cleared; only summary + current task retained  
5. Execution resumes  

Source: https://platform.claude.com/cookbook/tool-use-automatic-context-compaction

### The 62% figure (verified + sourced)

Multiple independent sources attribute **62% of average agentic API bills to re-sent context** (the same system prompt, tool definitions, and conversation history re-sent on every step):

- **Stanford Digital Economy Lab**, "Agentic AI Cost Attribution" (2025): primary academic source. Cited by Cockroach Labs engineering blog (June 2026): https://www.cockroachlabs.com/blog/agentic-ai-costs-at-scale/ and Beam.ai: https://beam.ai/agentic-insights/anthropics-new-billing-split-reveals-what-ai-agents-actually-cost
- **LeanOps audit of 30 engineering teams** (March–May 2026): confirmed the same 62% figure independently. Bill breakdown: re-sent context 62%, tool definitions 14%, fresh reasoning 11%, system prompts 8%, retries 5%. Source: https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/
- **arxiv paper** (January 2026, "Quantifying Where Tokens Are Used in Agentic Software Engineering"): found input tokens constitute 53.9% of total agentic token consumption, with the Code Review loop alone consuming 59.4% of all tokens — "strong empirical evidence for the 'communication tax'." https://arxiv.org/html/2601.14470v1

**Important caveat:** The exact "62%" attribution to "Stanford Digital Economy Lab" circulates widely in practitioner sources but the original primary paper has not been verified here as directly retrievable. The LeanOps audit independently confirms it. Flag this as: *well-corroborated practitioner figure; primary academic source cited but not independently retrieved from publisher.*

### Quantified token savings

- **Anthropic cookbook example** (official, June 2025): 204 416 → 82 171 input tokens with 2 compaction events = **122 392 tokens saved, 58.6% reduction**. Source: https://platform.claude.com/cookbook/tool-use-automatic-context-compaction
- **Morph context-compaction analysis** (March 2026): a 400 K-token context compacted to 160 K (60% reduction) saves $14.40 in input costs over 20 subsequent turns on Sonnet 4.6 alone. Combined with caching on remaining tokens: effective input cost drops from $3.00/M to ~$0.12/M effective = **96% reduction**. Source: https://www.morphllm.com/context-compaction

### When compaction **hurts** cache performance

Compaction resets the conversation prefix, which can invalidate active cache entries for mid-conversation context — the stable system prompt remains cacheable, but all the accumulated conversation/tool history is replaced with a new summary text (a cache miss on that portion). Best practice: compact aggressively for long-running sessions, but keep the static system-prompt prefix byte-identical to preserve that segment's cache hits.

### Official classification: Officially documented (Anthropic SDK + cookbook); 62% figure is community-audited with academic attribution.

---

## 4. Sub-agent / model routing

### Mechanism
Not every step in an agentic pipeline requires frontier-model capability. Routing mechanical, bounded, or classification sub-tasks to a smaller/cheaper model — and reserving the frontier model only for judgment calls, planning, and synthesis — cuts per-call cost by the model price ratio without proportional quality loss.

### Anthropic's own multi-agent research findings

**Source:** "How we built our multi-agent research system", Anthropic Engineering, 13 June 2025: https://www.anthropic.com/engineering/multi-agent-research-system

Key findings:
- **Architecture used:** Claude Opus 4 as lead orchestrator + Claude Sonnet 4 subagents → **outperformed single-agent Claude Opus 4 by 90.2%** on the BrowseComp internal research eval
- **Token burn:** agents use ~**4× more tokens than chat**; multi-agent systems use ~**15× more tokens than chat**
- **Performance driver:** token usage alone explains **80% of performance variance** (of three factors explaining 95% of variance: token usage > tool calls > model choice)
- **Cost mitigation via routing:** Sonnet subagents are 60% cheaper than Opus per token yet deliver most of the performance gain; "upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget on Claude Sonnet 3.7"
- **Architecture pattern that reduces token overhead:** subagents store large outputs in external memory and pass lightweight references to the coordinator, "prevents information loss during multi-stage processing and reduces token overhead from copying large outputs through conversation history"

### Model price ratios (Anthropic, June 2026)

| Model | Input | Output | Ratio vs Haiku 4.5 |
|-------|------:|------:|------------------:|
| Claude Fable 5 | $10.00/M | $50.00/M | 10× |
| Claude Opus 4.8 | $5.00/M | $25.00/M | 5× |
| Claude Sonnet 4.6 | $3.00/M | $15.00/M | 3× |
| **Claude Haiku 4.5** | **$1.00/M** | **$5.00/M** | **1× baseline** |

Source: https://www.anthropic.com/pricing

### Routing savings in practice

- **Routing 70% of traffic to Haiku, 30% to Sonnet** vs. all-Sonnet: **47% cost reduction** (PADISO routing analysis, June 2026): https://www.padiso.co/blog/claude-model-routing-cost-lever-2026/
- **80/15/5 split (Haiku / Sonnet / Opus)** for production agents: **45–55% cost reduction** vs. routing everything to Sonnet (based on 50+ implementations): same source
- **Full delegation to Haiku subagents for bounded tasks** (file reads, data research, metric tracking): **85–92% cost reduction** vs. all-Sonnet architecture (Kaxo case study, June 2026): https://kaxo.io/insights/scaling-claude-code-sub-agent-architecture/

### Routing decision framework

Route to **Haiku / small model**: classification, extraction, file reads, format conversion, summarisation of short inputs, cron/maintenance tasks, tool-call parsing.  
Route to **Sonnet / mid-tier**: code generation, structured output, multi-step reasoning over medium contexts, most customer-facing tasks.  
Route to **Opus / frontier**: architecture decisions, complex debugging, synthesis across many sources, tasks where mistakes are expensive.

### Official classification: Official Anthropic research + official pricing.

---

## 5. Repo maps / structural context (Aider tree-sitter)

### Mechanism
Instead of reading entire files into the LLM context window, Aider builds a **1 K-token structural map** of the repository by parsing all source files with tree-sitter, extracting class/function signatures, types, and call signatures, ranking them by graph-theoretic importance (PageRank on the symbol reference graph), and including only the most relevant subset. This gives the model awareness of the full codebase structure at a fraction of the token cost of reading files.

### Quantified token numbers

| Approach | Tokens | Source |
|----------|-------:|--------|
| Aider repo map default (`--map-tokens 1024`) | **~1 000 tokens** | https://aider.chat/docs/repomap.html (Aider official docs) |
| Full repo map (all signatures, pre-ranking) | Varies; optimised to fit within `--map-tokens` budget | Same |
| Reading whole files | 10–100× more; a single 200-line file ≈ 1 000–2 000 tokens | Practitioner estimates |
| Smart ripgrep/hypergrep (L1 + budget cache) vs raw file reads for a single investigation task | **2 814 vs 20 580 tokens = 87% reduction** | https://dev.to/marjoballabani/your-ai-agent-wastes-87-of-its-tokens-just-finding-code-i-fixed-that-4d5p (DEV Community, March 2026) |
| Semble embedding-based search vs grep+read on 100 K-file codebase | **3 K vs 150 K tokens per session = 50× reduction** | https://neuralstackly.com/blog/code-search-ai-agents-token-optimization (NeuralStackly, May 2026) |

Source for Aider docs and tree-sitter architecture: https://aider.chat/2023/10/22/repomap.html (Aider blog, October 2023)

**Tool-call reduction:** Unblocked controlled test: curated context cut **token usage by 42% and tool calls by 64%** on an identical model+prompt vs. standard file-reading approach. Source: https://getunblocked.com/blog/agent-auto-loop-token-cost/

**Note on Aider's own quantification:** Aider's official documentation states the repo map defaults to 1 K tokens and is "optimised to fit within the active token budget," but does not publish an explicit comparison study of repo-map tokens vs. file-reading tokens for comparable tasks. The 87% and 50× figures are from third-party benchmarks of similar structural-map-vs-file-read approaches, not Aider's own published numbers.

### Mechanism detail: tree-sitter role
Tree-sitter parses source files into ASTs, enabling extraction of only the declarations, signatures, and reference relationships — not implementation bodies. Aider then runs PageRank on the symbol-reference graph to surface the most globally relevant identifiers within the token budget.

### Official classification: Mechanism officially documented (Aider); quantified magnitude from community benchmarks.

---

## 6. Batch APIs

### Mechanism
Instead of sending requests synchronously one-at-a-time, batch APIs collect many independent requests and process them asynchronously (typically within 24 hours). Providers discount batch usage because they can schedule jobs during off-peak GPU capacity, improving hardware utilisation.

### Discount rates

| Provider | Batch discount | Models | Deadline | Stacks with prompt caching? |
|----------|---------------:|--------|----------|----------------------------|
| **Anthropic** | **50% off** all token types | All active Claude models | 24 hrs (expire if unfinished) | **Yes — explicitly stated: "These multipliers stack with other pricing modifiers such as the Batch API discount"** |
| **OpenAI** | **50% off** | gpt-4o, gpt-4.1, o-series, most recent models | 24 hrs | **No — "Discounting for Prompt Caching is not available on the Batch API"** |
| **Google Gemini** | **~50% off** input (Batch tier vs Standard) | Gemini 2.5 Flash: $1.50 → $0.75; Gemini 2.5 Pro: $1.25 → $0.625 | Not specified | **No — "Context Caching is not currently supported with the Batch API"** (Google AI Developers Forum, September 2025) |
| **DeepSeek** | Not stated for batch | V4 series | N/A | Not stated |

Sources:  
- Anthropic batch docs (September 2024): https://docs.anthropic.com/en/docs/build-with-claude/message-batches  
- OpenAI batch guide: https://platform.openai.com/docs/guides/batch  
- Google Gemini pricing: https://ai.google.dev/gemini-api/docs/pricing  
- Google Forum (batch + caching incompatibility): https://discuss.ai.google.dev/t/context-caching-batch-api-requests/105642

### Multiplicative stacking (Anthropic only)

With Anthropic, batch discount (50%) and prompt-cache discount (90%) stack multiplicatively:

| Configuration | Effective cost per 1M input tokens (Sonnet 4.6, list $3.00) | Savings |
|---------------|-------------------------------------------------------------:|--------:|
| Standard | $3.00 | 0% |
| + Prompt cache hit | $0.30 | 90% |
| + Batch only | $1.50 | 50% |
| + Cache hit + Batch | **$0.15** | **95%** |

With context compaction also applied (reducing token count by ~60%):  
Effective cost: $0.15 × 0.4 = **$0.06 per 1M tokens = 98% off list price**  
Source: https://www.morphllm.com/anthropic-api-pricing (Morph, April 2026)

### Practical constraint: TTL clash with batch

Anthropic's batch docs note that because batch requests are processed asynchronously (up to 24 hours), 5-minute TTL cache entries will expire before the batch runs. **Recommendation: use the 1-hour cache duration** (at 2× the write cost) when combining batch + cache. Cache hit rates in batch are "best-effort" and range from **30–98% depending on traffic patterns**.  
Source: https://docs.anthropic.com/en/docs/build-with-claude/message-batches

### Official classification: Official (all provider docs).

---

## 7. Local model offload (Ollama / Qwen)

### Mechanism
Running a local open-weight model (via Ollama, vLLM, or similar) on local hardware for mechanical sub-tasks eliminates API token charges entirely for those calls. The local model serves an OpenAI-compatible REST API at `localhost:11434`, so any tool that calls the cloud API can be redirected with a single `base_url` change.

### Cost economics

| Mode | Per-token cost | Source |
|------|---------------:|--------|
| Cloud API (e.g. Sonnet 4.6) | $3.00/M input, $15.00/M output | https://www.anthropic.com/pricing |
| Cloud API (cheapest tier, e.g. Gemini 2.5 Flash-Lite) | $0.10/M input, $0.40/M output | https://ai.google.dev/gemini-api/docs/pricing |
| Ollama (local, on-hardware) | **$0.00** API cost; ~$0.0003/M tokens in electricity equivalent | https://aiordienow.com/run-local-llm/ (April 2026) |
| Local GPU inference (14B class model, full utilisation) | ~$0.004/M compute floor | https://zylos.ai/research/2026-05-02-ai-agent-cost-engineering-token-economics/ |

A typical coding session (100 K input + 20 K output) costs ~$0.80 on Sonnet vs. **$0.00** on a local Qwen2.5-Coder 32B.  
Source: https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup

### What to offload vs. keep cloud

| Task type | Local model adequate? |
|-----------|----------------------|
| Tool-call parsing, JSON extraction, format conversion | ✓ Yes |
| Routing / intent classification | ✓ Yes |
| Short summarisation (≤1 K token output) | ✓ Yes |
| Log analysis, grep-result filtering | ✓ Yes |
| Code generation in common languages (7B+ model) | ✓ Usually |
| Multi-step reasoning chains, complex debugging | ✗ No — frontier API recommended |
| Long-context reasoning (>32 K tokens) | ✗ No — local context windows are smaller |

Source: https://lumadock.com/tutorials/openclaw-ollama-local-models-setup (February 2026)

### Key models for local offload

- **Qwen2.5-Coder 32B**: strong on code tasks, 32 K context  
- **Llama 3.3 (70B)**: best general-purpose reasoning in local tier  
- **Gemma 4 (27B)**: good balance of speed and capability  

Ollama pull examples: `ollama pull qwen2.5-coder:32b` / `ollama pull llama3.3`

### Official classification: Community-sourced (practitioner benchmarks; no official provider study).

---

## 8. Retrieval / pre-filtering (ripgrep / mdfind)

### Mechanism
Instead of dumping raw files or entire repo content into the LLM context window, a fast local search tool (ripgrep, mdfind, Spotlight) first narrows the candidate set to the relevant lines/functions/snippets. Only the filtered output is passed to the model. This converts a potentially 50 K–200 K-token file-reading operation into a 2 K–5 K-token targeted snippet.

### Quantified reductions

| Approach | Tokens | Reduction | Source |
|----------|-------:|----------:|--------|
| Raw grep + file reads (single investigation task) | 20 580 tokens | — | https://dev.to/marjoballabani/your-ai-agent-wastes-87-of-its-tokens-just-finding-code-i-fixed-that-4d5p |
| Hypergrep with L1+budget cache | 2 814 tokens | **87% reduction** | Same (DEV Community, March 2026) |
| Grep pipeline (2.7M lines → 183 K via regex filter) | 183 K lines in | **15× cut before any LLM call** | https://medium.com/@jsmith0475/unlocking-unprecedented-power-why-grep-is-your-llms-secret-weapon-eb6664cd734b |
| E-commerce pilot — grep gate ahead of model | 8.2 M → 820 K billed tokens | **90% reduction; latency 5.9 s → 1.1 s** | Same (Medium, July 2025) |
| Agentic retrieval protocol (multi-agent, doc-level QA) | 60% token reduction | vs. flat RAG context sharing | https://www.reddit.com/r/AI_Agents/comments/1jugj0e/ (Reddit/r/AI_Agents, April 2025) |
| Semble embedding search vs. grep+read, 100 K-file codebase | 3 K vs 150 K tokens/session | **50× reduction** | https://neuralstackly.com/blog/code-search-ai-agents-token-optimization |

### The retrieval principle
The agent should ask: *what is the minimum token footprint that contains the decision-grade information?* A well-configured ripgrep invocation returns 20–200 lines of precise matches; a naive file-read returns the entire file. For a 500-line file, that is a 50–250× token difference for a single read; across a multi-tool-call agent loop, savings compound.

### ripgrep over grep: practical reasons
- Automatically respects `.gitignore` (skips build artifacts, node_modules, minified JS)
- Skips binary files by default — prevents accidental large binary ingest
- ~10× faster than grep on large repos (2 GB monorepo: 15 s → <2 s)

Source: https://www.learnwithparam.com/blog/ripgrep-coding-agents-fast-code-search (February 2026)

### Official classification: Community benchmarks; no official provider study. High-confidence directionally.

---

## 9. Output-token discipline

### Mechanism
Output tokens are generated sequentially (one forward pass per token) while input tokens are processed in a single parallel prefill pass. This structural asymmetry means output tokens cost more compute per token, and all major providers price them at a **4–5× premium** over input tokens.

### Output vs. input cost ratios (official pricing, June 2026)

| Model | Input ($/M) | Output ($/M) | Ratio |
|-------|------------:|-------------:|------:|
| Claude Sonnet 4.6 | $3.00 | $15.00 | **5×** |
| Claude Haiku 4.5 | $1.00 | $5.00 | **5×** |
| Claude Opus 4.8 | $5.00 | $25.00 | **5×** |
| GPT-5.4 | $2.50 | $15.00 | **6×** |
| Gemini 2.5 Flash | $0.30 | $2.50 | **8.3×** |
| Gemini 2.5 Pro | $1.25 | $10.00 | **8×** |
| DeepSeek V4-Flash | $0.14 | $0.28 | **2×** |

Source: https://www.anthropic.com/pricing; https://platform.openai.com/docs/pricing; https://ai.google.dev/gemini-api/docs/pricing; https://api-docs.deepseek.com/quick_start/pricing  
Industry summary (silicondata.com, May 2026): "The median output-to-input ratio in our dataset is approximately 4×": https://www.silicondata.com/blog/llm-cost-per-token

### High-leverage output discipline techniques

**A. Stop sequences**  
Configure `stop_sequences` to halt generation at a natural completion boundary (e.g. `"\nUser:"`, `"</answer>"`, `"[END]"`). Prevents trailing pleasantries, filler, and open-ended continuations.  
Estimated savings: **20–40% reduction in output tokens** on instruction-following tasks.  
Source: https://www.modelmath.app/guides/token-optimization

**B. Structured output / JSON schema (`response_format`)**  
Forcing structured JSON output strips prose wrappers around answers ("The email address is X…" → `{"email": "X"}`).  
- 30–50% fewer output tokens on extraction tasks vs. free-form prose  
- A workload extracting structured data from 100 K messages/day saves ~$900/month on a single feature at GPT-4o output pricing  
Source: https://dev.to/rikuq/structured-outputs-vs-json-mode-vs-function-calling-vs-raw-text-the-cost-tradeoff-explained-471g (DEV Community, June 2026)

**C. Explicit token-budget instructions in system prompt**  
Adding a "concision discipline" instruction block (anti-filler directives such as "answer in under 100 tokens", "no preambles") to a code-audit agent's system prompt:  
- **−24.7% output tokens**  
- **−20.7% cost**  
- **−27.9% wall-clock duration**  
- **+9.1 F1 points recall improvement** (sparser output was more signal-dense)  
Source: https://anatoly.cloud/research/concision-discipline-prompt-strategy

**D. `max_tokens` caps**  
Setting `max_tokens` deliberately for each call type (summary: 200, routing decision: 10, code edit: 500) prevents the model from generating beyond what the task requires. A 500-token response when 80 tokens suffice costs 6× more on output.  
Source: https://vinayakajyothi.com/blog/2026-05-11-agentic-ai-cost-optimization/

**E. Prefer input over output for known data**  
Structure tasks so the model confirms/selects from pre-enumerated options rather than generating free text. "Is this bug in category A, B, or C?" costs ~3 output tokens; "Describe this bug" costs 100–500.

### Official classification: Output pricing ratios — official; technique savings — community benchmarks with consistent cross-source agreement.

---

## Cross-cutting: combinatorial stacking potential

The nine techniques are not mutually exclusive. Their savings can compound (where compatible):

```
Base cost: $3.00/M input tokens (Sonnet 4.6)
  ├─ #1 Prompt caching (cache hit):       × 0.10  →  $0.30/M
  ├─ #3 Context compaction (60% fewer tokens):  × 0.40  →  $0.12/M effective
  ├─ #6 Batch API (50% off):             × 0.50  →  $0.06/M effective
  └─ #4 Route 80% of calls to Haiku:     × 0.33 on those calls
```

Combined effective input rate for optimised Anthropic stack: **~$0.06–0.15/M** vs. $3.00/M list = **95–98% reduction**.  
Source: https://www.morphllm.com/anthropic-api-pricing

For **output tokens** (not cacheable, not batch-discounted at same rate), output discipline (#9) is the primary lever. Claude Sonnet 4.6 at $15.00/M output: −25% from structured output → $11.25/M; −20% from concision discipline → $9.00/M effective.

---

## Source quality rating

| Source type | Techniques covered |
|-------------|-------------------|
| **Official** (provider pricing pages, official docs) | #1, #2 (partially), #6, output ratios in #9 |
| **Official primary research** (Anthropic Engineering blog) | #4 (multi-agent stats) |
| **Official cookbook / SDK docs** | #3 (58.6% compaction figure) |
| **Peer-reviewed / arXiv** | #3 (53.9% input token share in agentic coding) |
| **Audited practitioner study** (LeanOps 30-team, Requesty 12-month) | #3 (62%), #2 (cache hit rates) |
| **Community benchmarks** (reproducible, cited) | #5, #7, #8, technique savings in #9 |
| **Untraced / uncorroborated** | None — all figures above have cited sources |

**The 62% re-sent context figure:** Attributed to "Stanford Digital Economy Lab, Agentic AI Cost Attribution, 2025" in multiple independent sources (Cockroach Labs, Beam.ai, LeanOps). The LeanOps 30-team audit (March–May 2026) independently confirms the same number. *However, the original Stanford DEL paper has not been independently retrieved from a publisher URL in this research.* Treat as: well-corroborated community consensus with academic attribution; verify with primary paper URL before citing in investor materials.

---

*Research compiled 23 June 2026. All pricing correct at time of research; provider pricing pages change frequently — verify before use in financial modelling.*
