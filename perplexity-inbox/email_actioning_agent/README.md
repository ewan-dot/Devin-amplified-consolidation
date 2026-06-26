# email_actioning_agent

Token-efficient, multi-inbox email **actioning** (not replying), built from
`perplexity-inbox/claude-gmail-brief.md` (2026-06-26).

Three principles, in order:

1. **Deterministic first.** If a step can be done by code, it is. Classification,
   routing, gating, field extraction, and token accounting are 100% deterministic
   — *no LLM in the decision path*. A model is invoked only for the `needs_ai`
   residue (ambiguous low-confidence items, or routes whose *action* needs
   judgment/drafting). On the first real run, **89.5% of emails were resolved with
   zero model tokens.**
2. **Token-efficient (code execution with MCP).** Full email bodies stay in the
   sandbox; only compact structured rows cross into model context. Measured on
   real mail: **~53% per-email token saving**, breakeven ~30 emails, ~45% at inbox
   scale (tiktoken `cl100k_base`, approximate-for-Claude; see `tokens.py`). We do
   **not** claim the brief's 98.7% — that's their worked example, this is ours.
3. **Observable, with a fallback.** Every run emits a witness — local append-only
   JSONL (always) + best-effort Vellum — and a health verdict (OK/DEGRADED/FAILED).
   If it breaks, we know. See `telemetry.py` and `RUNBOOK.md`.

## The determinism boundary

```
                 ┌──────────────────────── deterministic (code) ───────────────────────┐
 fetch (adapter) │  classify → extract fields → route → gate (amplified_permissions) →  │  emit JSONL / label / archive
                 └──────────────────────────────────────────────────────────────────────┘
                                                   │  only the residue ▼
                                          needs_ai: low-confidence triage
                                          needs_ai: URGENT_HUMAN judge/draft
```

## Routing surface (from the brief)

| Route | Action | Doctrine tier | Auto-runs? |
|-------|--------|---------------|------------|
| INFRA_CRITICAL | extract → JSONL → Beast ingestion pipe (via inbox) | A (`write_inbox`) | yes (local emit) |
| ATTRIBUTION | content-harvest → brain (via staging) | A (`write_inbox`) | yes (local emit) |
| NEWSLETTER | digest label | B (`label`) | only under `--apply`, logged |
| NOISE | archive | B (`archive`) | only under `--apply`, logged |
| FINANCIAL | Drive + ledger + notify | **C (`send`)** | **never** — gated action-request |
| URGENT_HUMAN | Telegram/Slack push | **C (`send`)** | **never** — gated action-request |

Tier C (external send/publish/Drive/Beast-direct) is never auto-executed — it is
surfaced for explicit human authorisation. Default run is **dry-run**; `--apply`
performs only Tier A/B (reversible) actions.

## Usage

```bash
python -m email_actioning_agent inboxes      # configured inboxes + auth state
python -m email_actioning_agent run          # dry-run: classify→route→emit→measure→witness
python -m email_actioning_agent run --apply  # also perform Tier A/B (label/archive/emit); Tier C still gated
python -m email_actioning_agent measure      # last real token measurement
python -m email_actioning_agent health       # exit 0=OK 1=DEGRADED 2=FAILED (for cron/hooks)
python -m email_actioning_agent scout        # route the brief into the Night Scout feed
```

## Real capture (no mock data)

This environment has no in-sandbox MCP bridge, so the capture a code-execution
runtime would do in-sandbox was performed once by the model and frozen in
`data/_build_capture.py` → `data/captured_emails.jsonl` (real mail from
`ewan@bykerbusinesshelp.ai`, 2026-06-26). The pipeline runs deterministically over
that. Wiring a live in-sandbox adapter is a drop-in change in `servers/`.

## Layout

```
email_actioning_agent/
  config.py        inboxes, routes, tiers, determinism floor, paths
  servers/         one adapter per inbox (code-execution boundary)
  classifier.py    deterministic tiered classifier (no LLM) + needs_ai boundary
  extract.py       deterministic field extraction (repo/run-id, vendor/amount)
  router.py        routing surface + doctrine gate (amplified_permissions)
  emit.py          Tier A JSONL emitters (INFRA feed + routed log)
  tokens.py        real token measurement (honest per-email + breakeven + projection)
  telemetry.py     witness (local always + best-effort Vellum) + health verdict
  night_scout.py   dual-purpose feed handoff
  pipeline.py      fetch→classify→extract→route→emit→measure→witness
checklists/        implementation / safety-gates / go-live / multi-inbox-auth
RUNBOOK.md         failure modes → signal → fallback → fix
```
