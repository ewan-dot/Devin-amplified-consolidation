# Expert-Partner Brief — Model-Agnostic Token Optimiser

> TIER: STRUCTURED (brief structure) · effective tier of factual claims = MIN of source tiers.
> Code claims: STRUCTURED (full read of `token_proxy.py` 991L + `context_compressor.py` 298L, verified vs GitHub `Amplified-Partners/anthropic-token-proxy` HEAD `6feef61`).
> Savings claims: INTUITED until the cost-log is measured (first job below).

---

## 1. THE SPINE (today)

- Who we are: **Amplified Partners** — AI-native business operating system. Architect: Ewan Bramley.
- Goal-lock: **get the business going. Make money so we can give it away.** Spend is ~$4–5k/month on AI; cutting it is direct fuel.
- The rods (one line): Win-win > Honesty > Transparency > Attribution > Meritocracy. On tie, goal serves over ego.
- Substrate stance: AI is substrate, not signer. AI emits congruence checks; only Ewan ratifies. Nothing enters the Beast except through the pipe (Python + Rust + Vellum + AI + Human).
- Architect's standing: Ewan can do whatever he wants provided the five rods hold. Permission-gating Ewan is out of scope. Hooks/harnesses in this brief bind **the receiving agent**, not Ewan.
- Date: 2026-06-18.

---

## 2. THE LENS (this task)

- **The situation, one sentence:** `token_proxy.py` is not a token optimiser with an Anthropic adapter — it is an Anthropic API proxy with optimisations welded to Anthropic's wire format, and there is no provider seam anywhere in it.
- **Why now:** Anthropic-only routing means the cheap-work tier (extraction, classification) pays full Claude rates and streamed calls bypass caching entirely. Both are likely the bulk of a $4–5k/month bill.
- **Strengths to lean on:** the receiving agent is strong at mechanical adapter extraction, golden-file diffing, and Python refactors with a clear contract.
- **Blind spots to watch:** drift-to-fabrication on "tests pass = correct" — the bar here is byte-identical wire output, not green tests. Also: this proxy is a single point everything routes through, with a `KeepAlive: true` launchd plist (`token_proxy.py:942`) that restarts crashes in a tight loop. A bad change fails loudly and repeatedly.
- **Unusual constraints:** all work happens in a **git worktree on a feature branch** — the live proxy's checkout (`main`) is never touched. Merge is Ewan's button. No live-service restart, no plist load, no Vellum write by the agent.

---

## 3. SPEC CHECKLIST — what counts as done

- [ ] **Cost baseline measured first.** `~/.amplified/cost-log.jsonl` parsed; spend grouped by `tool`, by `model`, by `from_cache`. Output: a table of where the money actually goes. This decides which levers pay. No refactor begins before this exists.
- [ ] A canonical internal request/response model exists, provider-neutral. No `anthropic-*` field names leak above the seam.
- [ ] An `LLMProvider` protocol exists with ≥6 methods: `base_url`, `chat_endpoint_path`, `to_provider_request`, `from_provider_response`, `inject_cache_controls`, `inject_compaction`, `parse_stream_usage`, `pricing`, `route_model`.
- [ ] `AnthropicProvider` adapter lifts current behaviour **verbatim** — passes a golden-file diff: same canonical input → byte-identical outgoing request body + headers + recorded cost vs today's `main`.
- [ ] ≥1 second provider stub (`OpenAIProvider` **or** `LocalProvider`/Ollama) implements the protocol and round-trips a canonical request without importing the Anthropic SDK.
- [ ] Provider selection works via env `LLM_PROVIDER` and/or `model:` prefix (`anthropic/…`, `openai/…`, `local/…`).
- [ ] The provider-neutral layers (semantic cache, budget control, cost log, injection scan, agent attribution) are **unchanged in behaviour** and sit above the seam.
- [ ] Edge cases handled: streaming vs non-streaming usage parsing; unknown-model pricing fallback; provider that auto-caches (cache injection is a no-op, not an error); provider with no compaction (no-op).
- [ ] Out of scope: changing the running service; loading the plist; writing to Vellum/Beast; touching `main`; rotating the leaked token (flagged separately as AMP-SEC-1).

---

## 4. RESEARCH CHECKLIST — what counts as enough

- Primary source: the two files in this repo (`token_proxy.py`, `context_compressor.py`) — already read; the 15-assumption table below is the map.
- Also read before designing: `clean-build/02_build/token_optimizer/{__init__,batch_router,context_cache_primer,max_tokens_config}.py` — **UNREAD in this analysis (local bridge timed out 3×)**. If this is the clean rewrite, the seam goes in natively and the issue list shifts left. Read it first.
- Out-of-band allowed if primary is silent: OpenAI `/v1/chat/completions` usage shape, Google `:generateContent`, Ollama API — only the request/response/usage schemas, nothing else.
- Stop conditions: once each of the 15 assumptions maps to exactly one protocol method, stop researching and build. Do not gold-plate the abstraction.
- If research contradicts the spec (e.g. a provider can't express a capability): stop, surface to Ewan, do not invent a workaround that changes Anthropic behaviour.

---

## 5. JOB CHECKLIST — what the agent must produce and verify

- [ ] **Set up the worktree before any edit:** `git worktree add ../atp-agnostic feat/provider-seam` off the canonical repo. Live proxy keeps running from `main`'s checkout. Confirm `git worktree list` shows isolation.
- [ ] Plan record committed before execution (a short `PLAN.md` in the worktree).
- [ ] Install the golden-file harness (Section: Hooks & Harnesses) as a **pre-commit hook** in the worktree. It must refuse commits where `AnthropicProvider` wire output drifts from the captured `main` baseline.
- [ ] Capture the golden baseline from `main` FIRST (record real outgoing request bodies + headers for a corpus of representative calls), then build the adapter to reproduce them.
- [ ] Two direct attempts on each blocker, one researched attempt, then wrap and surface — no thrashing.
- [ ] Durable artefacts: branch commits + a PR. Not chat output. Never a direct push to `main`.
- [ ] Self-check against every SPEC box before opening the PR.
- [ ] Session-close manifest: intent, files touched, golden-diff result, savings-estimate-now-vs-measured, open questions.
- [ ] Forbidden moves: editing `main`; starting/reloading the proxy or plist; writing to Vellum/Beast directly; declaring done on green tests without the golden diff; "improving" Anthropic behaviour while extracting it (extract first, improve in a separate commit).

---

## 6. THE PROMPT (hand-off ready)

```
You are an expert Python infrastructure agent. Today is 2026-06-18.

You are making Amplified Partners' token optimiser model-agnostic. It is currently
an Anthropic-only API proxy (`token_proxy.py`) that everything routes through. Your
job: introduce ONE provider interface so other models (local/Ollama, DeepSeek, OpenAI)
can be swapped behind it — without changing Anthropic behaviour by a single byte.

Work in a git worktree on `feat/provider-seam`. The live proxy runs from `main` —
never touch it. Merge is Ewan's. Do not start the service, load the plist, or write
to Vellum.

[paste THE SPINE]
[paste THE LENS]

The contract is the SPEC CHECKLIST. The research budget is the RESEARCH CHECKLIST.
The work discipline is the JOB CHECKLIST. The 15-assumption table and the hooks/
harness spec are below — use them.

Measure the cost log BEFORE refactoring; it tells you which levers pay.
The bar is byte-identical wire output for Anthropic, not green tests.

You are an expert partner. Use your judgement. Resilience without thrash: two direct
attempts, one researched, then wrap. Hand back with a session-close manifest.
```

---

# APPENDIX A — The 15 Anthropic assumptions (the map)

| # | Assumption | Where | Maps to protocol method |
|---|---|---|---|
| 1 | Upstream URL `https://api.anthropic.com` hardcoded | `token_proxy.py:69,586,631` | `base_url()` |
| 2 | Activation via `ANTHROPIC_BASE_URL` (Anthropic SDK reads it) | docstring `:18-22` | provider selection / env |
| 3 | Endpoint path `/v1/messages` | `:707,796,816` | `chat_endpoint_path()` |
| 4 | Request schema: `system` as str/blocks, `messages[].content` blocks | `:374-389,430-446,483-490` | `to_provider_request()` |
| 5 | Prompt caching via `cache_control: ephemeral` | `:424-446` | `inject_cache_controls()` (no-op where auto) |
| 6 | `anthropic-beta` header (`prompt-caching-2024-07-31`, `compact-2026-01-12`) | `:764-771` | `inject_cache_controls()` / `inject_compaction()` |
| 7 | Native compaction `context_management.edits[].type=compact_20260112` | `:749-755` | `inject_compaction()` (no-op elsewhere) |
| 8 | Usage keys `input_tokens`/`output_tokens`/`cache_creation_input_tokens`/`cache_read_input_tokens` | `:823-829,877-880` | `from_provider_response()` |
| 9 | SSE events `message_start`/`message_delta` carry usage | `:865-883` | `parse_stream_usage()` |
| 10 | Model IDs + pricing Claude-only; unknown→Sonnet default | `:176-186,190` | `pricing()` |
| 11 | Cache-write 1.25× / cache-read 0.10× multipliers | `:195-196` | `pricing()` |
| 12 | Router `HAIKU`/`SONNET`, Sonnet→Haiku downgrade | `:176-177,347-420` | `route_model()` |
| 13 | Injection allow-list hardcodes `api.anthropic.com` | `:114` | provider-host-aware config |
| 14 | Compressor uses `anthropic.Anthropic().messages.create`, reads `response.content[0].text` | `context_compressor.py:61,183,206-213` | summariser uses `LLMProvider` |
| 15 | Summariser model pinned `claude-haiku-4-5` | `context_compressor.py:65,208` | `route_model()` / config |

**The seam:** canonical-ise → optimise (neutral layers untouched) → `provider.to_provider_request` → forward → `provider.from_provider_response` → record. Adapters selected by env or `model:` prefix. Neutral layers (cache, budget, cost log, injection scan, attribution) stay above the seam.

---

# APPENDIX B — Hooks & Harnesses (bind the agent, not Ewan)

Six independent restraints. `rules_software_up`: bind with code, not goodwill.

1. **Worktree + branch isolation.** `git worktree add ../atp-agnostic feat/provider-seam`. The agent physically cannot edit the live `main` checkout.
2. **Golden-file pre-commit hook.** Captures a corpus of real outgoing Anthropic request bodies + headers from `main` as the baseline. On every commit, re-runs the same canonical inputs through `AnthropicProvider` and diffs. Drift → commit refused. This is the real test, not pytest green.
3. **PR-only merge.** No direct push to `main`. Ewan holds the merge button — Ulysses self-binding, operational.
4. **Shadow mode (`--dry-run`).** New provider exercised against real traffic; responses logged but NOT returned to callers. Cutover only after shadow parity. (Your `shadow_tester` primitive.)
5. **A5 confirm-gate.** Agent will not start the proxy, load the plist, or write to Vellum/Beast without explicit Ewan go.
6. **Vellum event trail.** Every fix proposed logged as a tiered event (drafted through the pipe, Ewan ratifies). Audit log as harness.

**Golden harness, minimal shape (spec, not built):**
- `baseline/` — JSON files: one per representative call, each `{canonical_input, expected_request_body, expected_headers, expected_recorded_cost}`, captured from `main`.
- `verify_parity.py` — loads each baseline, runs it through `AnthropicProvider`, asserts byte-identical body + header set + cost. Exit non-zero on any diff.
- `.git/hooks/pre-commit` (in the worktree) — runs `verify_parity.py`; blocks commit on failure.
- Corpus must cover: non-streaming, streaming, cache-injected, compaction-armed, routed (Sonnet→Haiku), and a plain Haiku call.

---

# APPENDIX C — Cost-reduction levers (beyond agnosticism)

Realistic target: **30% is conservative; more is plausible** — but INTUITED until the cost-log is measured (SPEC box 1). Code-grounded leaks:

| Lever | Source evidence | Plausible saving |
|---|---|---|
| Route extraction/classification tier to **local (Ollama)/DeepSeek** | `_HAIKU_PATTERNS` `:303-324` shows this volume exists; today it pays Claude rates | Large (toward ~$0 for that tier) |
| **Streaming semantic cache** — today caching skips ALL streamed calls | `:773-787,834` cache only on non-stream; agent/Claude-Code traffic streams | Large (dominant path) |
| Real tokenizer for compaction trigger (vs `len(str)//4`) | `:746` char-estimate arms caching/compaction late | Moderate |
| Longer TTL on stable lookups (vs flat 24h) | `:78` `CACHE_TTL_HOURS=24` | Small–moderate |
| System-prompt-hash fast path | cache key includes last-3-turns `:479-491`; identical priming still pays | Small–moderate |

**The measure-first discipline:** the proxy already exposes `GET /proxy/costs?group_by=tool`. Pull `~/.amplified/cost-log.jsonl`, group by tool and model, and the 30%-vs-more question becomes MEASURED. Spending a refactor on a 5%-of-cost tier would be the real waste.

---

# APPENDIX D — Blast radius & separate flags

- **Single point of failure:** everything sourcing `keys.env` → `localhost:8088` (`:17-22`). Proxy refactor can break all AI traffic at once. The worktree + shadow mode exist to contain this.
- **KeepAlive loop:** `:942` — a crash-on-startup restarts forever. Never deploy an unverified build to the live plist.
- **AMP-SEC-1 (separate, not the optimiser):** a live `gho_` OAuth token is embedded in the `github_porch/anthropic-token-proxy` git remote URL — plaintext credential leak. Rotate it. Not part of this brief; flagged under transparency.

---

# Footer

- **Agent surface sized for:** Devin (DeepSeek) or Claude Code — a capable Python infra agent that can run a worktree and a pre-commit harness. Generic-compatible.
- **Assumptions made:** (1) the GitHub `token_proxy.py` is the refactor target, not the unread clean-build scaffold — confirm which. (2) Cost-log lives at `~/.amplified/cost-log.jsonl` per the proxy's own config `:71`.
- **Open question that genuinely blocks build (not padding):** is the target the mature GitHub `token_proxy.py`, or the clean-build `token_optimizer/` rewrite? The seam goes in differently for each. Everything else can proceed on judgement.
