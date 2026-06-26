---
title: Token-Efficiency Estate Spec — Finish and Prove (end-to-end, tested, working)
date: 2026-06-23
timezone: Europe/London
author: Perplexity (AI_PARTNER_PROXY, for-now)
ratifier: Ewan Bramley (pending)
effective_tier: STRUCTURED
provenance: 7 prior token/spend docs (this thread, 2026-06-16 → 2026-06-22) + live GitHub state of Amplified-Partners org (read 2026-06-23) + estate topology from memory notes
goal_link: stop the token bleed across the whole estate; run on what is already paid for; nothing slips through unmeasured
status: draft_for_ratification
---

# Token-Efficiency Estate Spec — Finish and Prove

TIER: STRUCTURED · external billing/benchmark facts MEASURED (cited in source docs) · current spend INTUITED until the cost log runs live ≥2 weeks · repo state VERIFIED (read on GitHub 2026-06-23)
PROVENANCE: synthesis of the 7 prior docs + verified GitHub org state. No web re-search this pass; the underlying figures were cited at source and are referenced, not re-fetched.
GOAL-LINK: recurring AI spend is direct cash out. This closes it across M4, M5, and the Beast, on every IDE and UI, and proves the cut with telemetry — not a green build.

VELLUM: target db=vellum @172.18.0.45:5432 (Beast) · NOT amplified_brain · AI drafts JSONL in sandbox → pipe writes. See VELLUM-PATH-CANONICAL.md

---

## 0. The one rule that governs this whole spec

**Done means proven, not pushed.** A green build, a merged PR, or a running container is NOT done. Every requirement below has an explicit acceptance test, and the spec is only complete when the **estate-wide proof run** in §9 passes and is captured in `PROOF-OF-LIFE.md`. This is the failure mode every prior doc warned about (code lands in GitHub and then sits there doing nothing) — it is now the spine, per your instruction.

Core thesis (unchanged, MEASURED at source): **frontier tokens are for judgment only.** Everything mechanical runs free — locally or off the Spotlight index — and the expensive model only ever sees a small, cached, pre-narrowed payload. The 20× cuts in the wild come from eliminating re-sent context (measured ~62% of the average agentic bill).

---

## 1. What already exists (VERIFIED on GitHub, 2026-06-23) — so we finish, not rebuild

Honest baseline. The central + procedural primitives are already coded. The router and the proof are the gaps.

| Component | Repo | State (verified) | Gap |
|---|---|---|---|
| Optimising Anthropic proxy: prompt caching, native compaction beta, semantic cache (Qdrant→pgvector per ADR-001), Sonnet→Haiku routing, cost log, daily budget cap, injection alert | `estate-cost-tools` (`token_proxy.py`, `context_compressor.py`, `daily_cost_report.py`, compose, RUNBOOK) | Built; tested **n=69 on 2026-05-03** (100% routing, 30.7% saving on sample); compose + 3-layer self-heal documented | **No live-traffic proof; semantic cache OFF; only a "canary agent" wiring step — NOT proven across the estate** |
| Earlier proxy (superseded) | `anthropic-token-proxy` | **archived** | Confirm fully superseded by `estate-cost-tools`; do not wire |
| Beast service stack / compose / fleet configs | `estate-machine` | Live (core graphs, db clients, dashboard API) | Token-proxy + router must be added to the canonical Beast stack and survive restart |
| Vellum ledger (append-only, hash-chained event bus) | `fleet-vellum` (`VELLUM-SPEC.md`, `VELLUM-CONNECT.md`) | Live; JSONL-draft → pipe write path | Cost/Effective-Tokens events must land here as first-class entries |
| Per-IDE agent ingress lanes | `Cursor`, `Claude`, `Devin`, `antigravity`, `grok-build`, `agent-cascade` (Windsurf) | Live; pushed within last 24h | Each lane needs its token policy baked in (config-as-code), not chosen at runtime |
| Deterministic LiteLLM credit-first router (job-class → executor, credit-first, budget guard) | **`estate-token-router` — DOES NOT EXIST** | Specced in the M5 builder-brief (2026-06-22); **never built** | **Build it, deploy it, prove it** |

**Implication for the spec:** ~60% of the mechanism is already in `estate-cost-tools`. The work is (a) deploy + live-prove the proxy across the estate, (b) build + deploy + prove the router, (c) bake per-IDE/per-UI config, (d) wire telemetry to Vellum, (e) one estate-wide proof run.

---

## 2. The estate (what "across the estate, nothing slips through" means)

Three machines + every agent surface. Each has a defined role and a token policy that is enforced in code, not by habit.

| Node | Role | Token posture |
|---|---|---|
| **M5 MacBook Air (24GB, daily seat)** | Judgment + orchestration. Claude Code on the **Max seat (Pool 1, auto-cached, 1-hr TTL, free at margin)**. Opus plans once; execution is mechanical. | Caching + `/compact` at ~60% + Haiku sub-agents + repo-map + `mdfind`-first. No mid-session model switch. |
| **Mac mini M4 (always-on, active cooling)** | Free local-execution node. Ollama + LiteLLM, OpenAI-compatible endpoint. Absorbs the 60–80% mechanical traffic. | Local model = $0 tokens. Claude-Code-to-local needs `--bare --exclude-dynamic-system-prompt-sections` (else KV-cache invalidation = ~90% slower). |
| **MacBook Air M4 (reserve, currently disconnected)** | Second agent host / overflow executor. Inherits the same baked config. | Same policy as the mini; brought online inherits, never re-specced. |
| **Beast (Hetzner AX162-R, CPU server)** | Ledger + batch + telemetry + router host. NOT a fast-LLM box. | Runs `estate-cost-tools` proxy + `estate-token-router` + Vellum + overnight Batch (batch 50% × cache 90% ≈ up to 95% off; stacks multiplicatively on Anthropic/OpenAI/xAI, NOT Google). |
| **Every IDE/UI** (Cursor, Claude Code, Devin, Antigravity, Windsurf/Cascade, Grok, the Vellum-substrate UI) | Work surfaces. | Each routes through the proxy/router and carries a baked token policy (§4). None bypasses telemetry. |

**RAM blocker (min-rule halt, still open):** the Mac mini RAM was written once as "2GB" (impossible) and once as "≥24GB assumed". The local model tier (7–8B vs 14B vs 32B) cannot be locked until you confirm the real figure. Flagged, not guessed.

---

## 3. The four axes mapped to enforcement surfaces (so optimisation is mechanical, not negotiated)

| Axis | Controls | Enforced where | Owner layer |
|---|---|---|---|
| **PROCEDURAL** | prompt prefix + context shape | session bootstrap (stable cache head + variable tail), ignore files, CLAUDE.md trim, `mdfind`-first, hooks-not-model | Python/Rust |
| **MODEL/IDE** | per-tool token settings | per-IDE config baked in, not chosen at runtime | Python + hooks |
| **ROUTING** | which job → which model/lane | `estate-token-router` (LiteLLM, credit-first, budget guard) | Rust governance + Python |
| **CENTRAL** | provider-side caching/batch/discount | `estate-cost-tools` proxy at the API boundary + telemetry | proxy + Vellum |

Each axis lands on a surface that already exists or is named. No bolt-on system.

---

## 4. Requirements — each with an acceptance test (this is the contract)

### A. PROCEDURAL floor (free, compounding, do first)
- **A1. Cache-stable prefix.** Stable head = operating bundle + tool/door schema + CLAUDE.md, byte-identical every job. Nothing dynamic at the top (no timestamps/IDs/per-machine paths → move to the tail). Apply `--exclude-dynamic-system-prompt-sections`.
  - *Test:* on two consecutive jobs from different machines, cache-read tokens > 0 on the second; prefix hash identical across both.
- **A2. CLAUDE.md ≤ 200 lines**, domain rules in `.claude/rules/` with `paths:` frontmatter (load only on matching file).
  - *Test:* `wc -l CLAUDE.md` ≤ 200; a rule file loads only when a matching path is touched (observed in a turn log).
- **A3. `.claudeignore` / `.cursorignore` per IDE lane** (node_modules, dist, build, locks).
  - *Test:* ignore file present in each lane repo; an indexed-file count drop is logged before/after.
- **A4. `mdfind`-first file location** is a mandatory pre-flight before any agentic search.
  - *Test:* router/bootstrap refuses (or logs a warning event) if an agent issues a directory-browse to locate a file instead of `mdfind`.
- **A5. Hooks do mechanical work** (lint/format/log/checkpoint) deterministically — zero model tokens.
  - *Test:* a commit runs lint+format via hook with zero LLM calls in the cost log for those steps.

### B. MODEL/IDE config, baked per lane (config-as-code, no runtime choice)
- **B1. Cursor lane:** Auto mode default (does not draw the credit pool); Max Mode OFF globally; model fixed at job start; `@`-references + `.cursorignore` over broad index.
  - *Test:* Cursor settings export shows Auto default + Max Mode off; a sample task shows no API-pool draw.
- **B2. Claude Code lane (M5):** Max-seat login only (decline API-credit prompts); automatic caching; `/compact` at ~60%, `/clear` between tasks; sub-agent model pinned to Haiku; `MAX_THINKING_TOKENS` capped; **no naive `/opusplan` toggling** (each plan↔execute switch invalidates cache — pin per session unless planning genuinely needs Opus).
  - *Test:* `/status` shows Pool 1 only; a heavy session shows >90% cache-read; sub-agent calls log as Haiku.
- **B3. Local lane (mini/M4):** Claude-Code-to-local launched with `--bare --exclude-dynamic-system-prompt-sections`; `CLAUDE_CODE_ATTRIBUTION_HEADER=0`.
  - *Test:* local inference latency is in the expected band (no ~90% KV-cache penalty); attribution header absent.
- **B4. Repo-map offload (any coding lane):** tree-sitter repo map (Aider-style) as a standing bootstrap artefact (~1K tokens structural understanding vs whole-file reads; ~10× reduction, 2.1× fewer tool calls at source).
  - *Test:* repo-map artefact present; a task completes without reading whole files to understand structure.
- **B5. MCP discipline:** CLI-over-MCP for read-only doors (Brain/Research/CRM reads); one tool-set per door (4–32× token gap at source; CLI lookup ~200 tok vs MCP ~12,957 tok).
  - *Test:* read-only doors use `gh`/CLI, not MCP; per-turn schema bytes drop measurably.

### C. ROUTING — build `estate-token-router` (the structural bleed-stopper)
- **C1. Deterministic plan distributor** (Python): job-spec → routing decision, **no model call in the routing logic itself**.
- **C2. Credit-first watcher:** reads remaining Claude Max credit/quota; routes eligible jobs to the Max seat FIRST until exhausted, then cheapest-competent fallback.
- **C3. LiteLLM router config:** mechanical→local Mac-mini, cleanup→Haiku, implementation→best-fit (Sonnet), overnight→Batch+cache, hard 20%→Opus (rare, flagged); cost logged per call.
- **C4. Affine budget guard:** integrate the `token-budgets` Rust crate (arXiv 2606.04056) — reserve/commit/release per job; double-spend across parent→subagent is a **compile error**. Optional fleet pool via `token-budget-pool`.
- **C5. Edge cap:** LiteLLM proxy budgets enforce 402 / silent `max_tokens` cap before the provider call.
- **C6. Production-Law gate (build into the router):** the central deterministic watcher forces every piece of work to terminate as a **landed (running) outcome** OR be surfaced as an **unfinished outcome** onto the board of jobs (Linear or a Vellum-backed `open_outcomes`). No silent dead-ends; it forces THAT there is an outcome, never WHICH.
  - *Test (C1–C6):* one real job-spec routed across ≥3 executor classes with a credit-first decision logged; an over-budget reserve is refused; an unfinished outcome appears on the board.

### D. CENTRAL — deploy + live-prove `estate-cost-tools`
- **D1. Proxy live on the Beast** (`token-proxy:8088` on `amplified-net`), `restart: always` + healthcheck + Temporal `token_proxy_health` watchman.
- **D2. Every IDE/agent wired** via `ANTHROPIC_BASE_URL: http://token-proxy:8088` — not just the canary. "Across the estate" = all lanes in §2.
- **D3. Daily budget cap + Telegram digest** active; semantic cache turned ON after one week stable.
  - *Test (D1–D3):* `/proxy/stats` 200 from inside `amplified-net`; cost-log grows for every wired agent; a forced-Haiku-on-budget event fires in a controlled test; 08:00 digest delivered.

### E. CENTRAL measurement — telemetry to Vellum (makes spend MEASURED)
- **E1. Per-job log:** tokens-in/out, cache-read, model, node, IDE, cost → cost-log + Vellum draft JSONL → pipe → `vellum` db.
- **E2. Effective-Tokens metric** (output ×4, cache-read ×0.1, model multiplier) normalises across models so a 10% ET drop = 10% cost drop regardless of lane.
- **E3. Budgets graduate INTUITED→MEASURED** only after ≥10 events/parameter (~2 weeks live), per min-rule.
  - *Test:* a daily auditor surfaces the most expensive jobs; ET trend visible; no budget claimed MEASURED before the threshold.

---

## 5. The locked token-flow (start to finish)

```
YOU (chaotic speech, M5 CLI)
  │ UI filter (Python): transcription-optimiser + neutral-research-brief → clean, CACHE-STABLE prompt
  ▼
OPUS 4.8 — Claude Code, Max seat (M5)            [JUDGMENT — auto-cached, 1-hr TTL, free at margin]
  │ mdfind narrows local files (FREE) · research → research pipe → back
  │ writes the detailed plan + prompt (nothing downstream is tricky)
  ▼
estate-token-router (Beast) — credit-first, deterministic, budget-guarded
  ├─ mechanical / 60–80% ─► Mac mini local (Qwen-Coder)     [FREE tokens]
  ├─ cleanup / classify ──► Haiku 4.5                        [cheap]
  ├─ implementation ──────► Sonnet 4.6                       [mid]
  ├─ overnight / batch ───► Batch API + cache (Beast)        [up to 95% off]
  └─ hard 20% ────────────► Opus (rare, flagged)             [premium]
  ▼
estate-cost-tools proxy ── caching · compaction · semantic cache · cost log · budget cap
  ▼
RESULT ─► Vellum (ledger + cost/Effective-Tokens telemetry) ─► Production-Law gate (landed or on the board)
```

**Design law:** Opus thinks ONCE; execution is mechanical. If a downstream step is "tricky," fix the plan — do not escalate the executor.

---

## 6. Conflicts to encode as guards (not honoured by discipline — enforced in code)
- Compression/compaction touches the **tail only**, never the cached head (else cache → 0%).
- **No mid-session model switch** (incl. naive `/opusplan`) — pin per lane.
- **No dynamic data in the prefix** (timestamps/IDs/per-machine paths → tail).
- **Local lanes:** attribution header off; `--bare`.
- **Google batch×cache does NOT stack** — pick provider per lane.
- **Pool-2 trap:** never wire Claude Code as an unattended GitHub Action on the Max seat (one loop can clear a Max credit in an afternoon, then bills ~10× marginal). Automated/CI → dedicated capped API key only.

---

## 7. Build/deploy order (cheapest-and-most-durable first)
1. **PROCEDURAL floor** (A1–A5) — free, no provider dependency, compounds everywhere.
2. **MODEL/IDE config per lane** (B1–B5) — quick wins baked into each agent repo.
3. **Deploy + live-prove the proxy** (D1–D3) across all lanes (estate-cost-tools already built).
4. **Build + deploy `estate-token-router`** (C1–C6) — the structural bleed-stopper.
5. **Telemetry to Vellum** (E1–E3) — proves it and calibrates budgets.
6. **Estate-wide proof run** (§9).

---

## 8. Pipe + min-rule discipline (non-negotiable)
- Mechanism + mapping: STRUCTURED. External %/billing: MEASURED at source. Current spend + savings: INTUITED until the cost log runs ≥2 weeks.
- **Nothing writes to the `vellum` db or the Beast directly.** Code → GitHub; this doc → Drive; events → Vellum JSONL draft → pipe; tasks → Linear. Ewan (or logged proxy) ratifies.
- Vendor-neutral by rule: the router decides per task; no provider is baked as default. Claude Max spend prioritised first because it is already paid for.

---

## 9. THE EXIT GATE — estate-wide, end-to-end, tested, proven (this is what "done" means)

The spec is complete only when ALL of the following are demonstrated in one captured run and written to `PROOF-OF-LIFE.md` in `estate-token-router` (and referenced from `estate-cost-tools`):

1. **Proxy live + wired estate-wide.** `/proxy/stats` returns 200 from inside `amplified-net`; cost-log shows entries from **every** IDE/agent lane in §2 (M5 Claude Code, Cursor, Devin, Antigravity, Windsurf, local mini), not just a canary.
2. **Router live on the Beast**, started by a documented compose/`start` command, survives a restart (restart policy verified by `docker restart` + re-`/health`).
3. **One real job routed across ≥3 executor classes** (e.g. mechanical→local mini, cleanup→Haiku, implementation→Sonnet) with the **credit-first decision logged** (Max seat chosen first while credit remains).
4. **Budget guard proven:** an over-budget reserve is **refused** (and, if using `token-budgets`, a double-spend attempt fails to compile — capture the compiler error).
5. **Caching proven:** a repeated job shows >90% cache-read on the second run (cost-log line).
6. **Local lane proven:** a job runs on the Mac mini at $0 tokens with correct flags (no KV-cache penalty).
7. **Telemetry proven:** the run's tokens/cost/Effective-Tokens land as a **Vellum draft JSONL** handed to the pipe; ET line present.
8. **Production-Law gate proven:** a deliberately-unfinished piece of work is **surfaced onto the board of jobs**, not silently dead-ended.
9. **Before/after spend delta:** the daily cost report shows a measured drop vs the pre-deployment baseline (or, if <2 weeks of data, the baseline is captured and the measurement window is scheduled).
10. **Self-heal proven:** kill the proxy container; the 3-layer self-heal (Docker restart → Temporal watchman → RUNBOOK) brings it back within the documented window.

**No proof-of-life = not done.** A green build sitting in any repo is a failure regardless of code quality.

---

## 10. Open questions for Ewan (block where flagged)
1. **Mac mini RAM** — the one number that locks the local model tier. (Blocks B3/C3 local sizing.)
2. **Confirm `anthropic-token-proxy` is fully superseded by `estate-cost-tools`** — archive-only, do not wire?
3. **Adopt `token-budgets` (arXiv 2606.04056) as the router budget core**, or evaluate `runcycles`/`iron_cost` first?
4. **Who builds what:** the M5 builder-brief already exists for `estate-token-router`. Re-issue it as-is, or fold these acceptance tests into it first?
5. **Usage exports** (Cursor, Devin, Anthropic Console, Perplexity, last 30 days) — needed to turn the §9.9 before/after from INTUITED to MEASURED and to settle the Cursor/Devin/Perplexity downgrade calls on evidence.
6. **Semantic cache:** keep OFF until one week stable (current default), or enable in the proof window with a guard?

---

VELLUM: target db=vellum @172.18.0.45:5432 (Beast) · NOT amplified_brain · AI drafts JSONL in sandbox → pipe writes. See VELLUM-PATH-CANONICAL.md
