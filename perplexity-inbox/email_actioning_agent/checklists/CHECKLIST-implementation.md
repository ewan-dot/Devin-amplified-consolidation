# CHECKLIST — implementation

Status of the build against `claude-gmail-brief.md`. `[x]` done & verified, `[~]`
done with a documented limit, `[ ]` deferred.

## Brief requirements
- [x] Multi-inbox triage that **actions** (label/file/extract/ingest), not replies
- [x] One adapter per inbox under `servers/` (code-execution-with-MCP boundary)
- [x] Classifier written **as code**, not a tool-loop (`classifier.py`, deterministic)
- [x] Tier the work, not the prompt — bulk = 1000-char truncation; high-stakes = full body
- [x] Routing surface: INFRA_CRITICAL / FINANCIAL / ATTRIBUTION / URGENT_HUMAN / NEWSLETTER / NOISE
- [x] INFRA_CRITICAL → JSONL into perplexity-inbox (`infra-critical-feed.jsonl`)
- [x] Measure tokens/email vs naive baseline on **real** mail (`tokens.py`, no mock)
- [~] Three inboxes configured; live capture only for the 1 authed account (OAuth gates the other 2)
- [x] Night Scout dual-purpose handoff (`night_scout.py`, `scout` command)

## Cross-cutting principles (Ewan, this session)
- [x] **Deterministic-first**: no LLM in classify/route/gate/extract; `needs_ai` isolates the residue (89.5% deterministic on first run)
- [x] **Observability on everything**: per-run witness (local always + Vellum best-effort) + health verdict + RUNBOOK fix paths

## Engineering
- [x] Reuses repo doctrine `amplified_permissions` for the action gate (one source of truth)
- [x] Pre-commit doctrine gate passes (`amplified_permissions.py --check-commit`)
- [x] 22 unit tests pass (synthetic fixtures); demo/measurement on real mail
- [x] Default dry-run; `--apply` performs only Tier A/B; Tier C never auto-runs
- [ ] Install agent hooks (pre-commit no-send guard, pre-push health gate) — `hooks/install.sh`
- [ ] Wire `EAA_VELLUM_*` env on the cron/launchd runner (RUNBOOK §Vellum)
- [ ] In-sandbox live MCP adapter (replaces frozen capture) when a code-exec runtime is available
