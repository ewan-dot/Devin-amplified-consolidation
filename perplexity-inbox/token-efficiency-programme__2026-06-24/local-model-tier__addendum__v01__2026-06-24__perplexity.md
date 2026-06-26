# Local-Model Tier — Addendum (Mac mini RAM resolved)

TIER: STRUCTURED · RAM figure MEASURED (Ewan-stated, 2026-06-24) · model sizing INTUITED (rule-of-thumb VRAM math, not benchmarked on this box)
PROVENANCE: resolves the open gate in `estate-token-efficiency-programme__implementation-brief` and `token-efficiency__estate-spec` §2.
GOAL-LINK: unblocks the free local-execution lane that absorbs 60–80% of mechanical traffic at $0 API tokens.

## Resolved
**Mac mini (M4 Pro, always-on) = 24GB unified memory.**

## Local model sizing (recommendation)
| Option | ~RAM at 4-bit | Verdict |
|---|---|---|
| **Qwen2.5-Coder-14B (4-bit)** | ~9–10GB | **Default.** Best capability/headroom balance; leaves ~12GB for OS + KV cache + context. |
| 7–8B (4-bit) | ~5–6GB | Safe floor if running other services concurrently, or for pure mechanical tasks. |
| 32B (4-bit) | ~18–20GB | Fits but starves OS/context on 24GB; only if the mini does nothing else. Not recommended as default. |

Serve via Ollama + LiteLLM (OpenAI-compatible endpoint), per the estate spec. Quant: Q4_K_M or better.

## Launch flags (unchanged, still required)
Claude-Code-to-local must use `--bare --exclude-dynamic-system-prompt-sections` and `CLAUDE_CODE_ATTRIBUTION_HEADER=0`, else KV-cache invalidation costs ~90% latency.

## Status
The §2 / implementation-brief "Mac mini RAM" hard gate is now **closed**. Remaining Tier-C gate: delete the 3 merged skills in Perplexity settings.

— still INTUITED on exact model: validate 14B vs 8B throughput on the actual box before locking; the math is rule-of-thumb, not benchmarked here.
