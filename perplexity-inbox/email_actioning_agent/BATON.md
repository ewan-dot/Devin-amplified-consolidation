# BATON — email_actioning_agent

**intent:** build the token-efficient multi-inbox email-actioning system from
`claude-gmail-brief.md`, end-to-end, deterministic-first, observable.
**seat:** cascade-mac · **branch:** feat/email-actioning-agent · **2026-06-26**

## State: WORKING (dry-run proven on real mail)
- Pipeline runs end-to-end on 19 REAL emails captured from ewan@bykerbusinesshelp.ai.
- 21 unit tests pass; doctrine pre-commit gate passes; no_send_guard passes.
- Vellum witness proven via MCP → sheet `f4168851-899b-43c6-aea5-02f4f90a7580`
  (entry `0d15da9e…`, hash `99d414c9…`). Env-driven witness path documented (RUNBOOK).

## Real measured outcomes (not the brief's numbers)
- Deterministic resolution: **17/19 (89.5%)** — zero model tokens; needs_ai = 2.
- Token saving (5 real full bodies, tiktoken cl100k_base): **52.9%/email**, breakeven 30, **45% at inbox of 200**.
- Routing: INFRA_CRITICAL 7 · FINANCIAL 2 · URGENT_HUMAN 1 · NEWSLETTER 4 · ATTRIBUTION 1 · NOISE 4.
- 3 Tier C action-requests gated (incl. a suspected Hetzner phishing email) — none auto-run.

## Open / deferred (each is a checklist line, not a blocker)
1. OAuth the other 2 inboxes (amplifiedpartners, ewanbramley@gmail) — user-only; `health=DEGRADED` until then (correct signal).
2. Wire live Gmail-MCP mutators (`servers/gmail_mcp` apply_label/archive) for Stage-1 `--apply`.
3. Set `EAA_VELLUM_*` env on the cron runner so autonomous runs witness to the ledger.
4. Install hooks: `bash email_actioning_agent/hooks/install.sh`.
5. Night Scout: confirm canonical M5 feed path with Ewan; sync `night-scout-feed/` → Beast APDS when reachable.
6. Replace frozen capture with a live in-sandbox MCP adapter when a code-exec runtime exists.

## Where to look
- Code: `email_actioning_agent/` · Tests: `tests/test_email_actioning_agent.py`
- Run: `python -m email_actioning_agent run` (dry-run) · `health` · `scout`
- Ops: `email_actioning_agent/RUNBOOK.md` · Checklists: `email_actioning_agent/checklists/`
