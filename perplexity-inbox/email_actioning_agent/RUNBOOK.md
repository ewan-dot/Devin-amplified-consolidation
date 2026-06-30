# RUNBOOK — email_actioning_agent

Observability contract: **if it breaks, we know — with a fallback and a fix.**
Every run writes a witness and a health verdict. Nothing fails silently.

## Where the signals live

| Signal | Location | How to read |
|--------|----------|-------------|
| Health verdict (latest) | `data/health.json` | `python -m email_actioning_agent health` (exit 0/1/2) |
| Run history (append-only) | `data/telemetry.jsonl` | one JSON RunReport per line |
| Vellum witness (fleet) | sheet `f4168851-899b-43c6-aea5-02f4f90a7580` | Vellum ledger; hash-chained |
| Token measurement | `data/token_measurement.json` | real per-email/at-scale numbers |
| Routed decisions | `data/routed_actions.jsonl` | per-email category/route/tier/extracted |

Health verdicts: **OK** = clean; **DEGRADED** = ran but something is off (still
usable); **FAILED** = could not run.

## Failure modes → signal → fallback → fix

| # | Failure | Signal | Fallback (automatic) | Fix |
|---|---------|--------|----------------------|-----|
| 1 | No captured mail | `health=FAILED`, `run` exits 2, "No captured mail" | none — run aborts safely | rebuild capture: `python email_actioning_agent/data/_build_capture.py` (or wire a live adapter) |
| 2 | An inbox unauthed | `warnings: inbox_unauthed:<key>`, `health=DEGRADED` | other authed inboxes still process | grant Gmail OAuth for that account (user-only; see CHECKLIST-multi-inbox-auth.md) then capture |
| 3 | Vellum witness unreachable | `warnings: vellum_witness_skipped`, `vellum_witnessed=false`, `health=DEGRADED` | **local witness JSONL still written** | set `EAA_VELLUM_URL/TOKEN/AUTHOR` env; check Beast/Tailscale reachability |
| 4 | Adapter fetch throws | `errors: fetch_failed:<key>`, `health=FAILED` | other adapters continue; error captured | inspect adapter/capture file; the run is witnessed even on failure |
| 5 | Classifier throws on a row | `errors: classify_failed:<msg_id>` | that row skipped, rest proceed | fix the offending input/rule; add a regression test |
| 6 | Tier C action pending | `tier_c_pending>0`, listed in `run` output | never auto-executed (safe) | human authorises the specific FINANCIAL/URGENT_HUMAN action |
| 7 | Classification looks wrong | review `routed_actions.jsonl` | safe direction: over-route to INFRA/high-stakes, not NOISE | extend keyword sets in `classifier.py` + add a regression test |
| 8 | Capture stale (old run) | compare `health.json` `ts` to now | — | re-capture; (future) add a freshness watchdog cron |

## Vellum witness wiring (production / cron)

```bash
export EAA_VELLUM_URL="https://vellum-mcp.beast.amplifiedpartners.ai/api/v1/agents/cascade-mac/send"
export EAA_VELLUM_TOKEN="<bearer>"      # never commit; pull from Infisical/codex-mcp at runtime
export EAA_VELLUM_AUTHOR="cascade-mac"
python -m email_actioning_agent run
```
If env is unset the run still completes and writes the local witness; it just
records `vellum_witness_skipped` and degrades to DEGRADED — by design.

## Heartbeat (recommended)

Cron/launchd: `python -m email_actioning_agent run` then `python -m email_actioning_agent
health`; alert if exit code != 0. The pre-push hook (CHECKLIST-implementation.md)
runs `health` so a FAILED/DEGRADED state blocks a push of broken state.
