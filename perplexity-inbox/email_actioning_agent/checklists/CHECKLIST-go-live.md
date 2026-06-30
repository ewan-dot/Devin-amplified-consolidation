# CHECKLIST — go-live (first live actioning)

The pipeline is real and proven in dry-run on real mail. Going live = letting it
perform reversible Tier A/B actions on the inbox, then (separately, human-gated)
the Tier C ones.

## Pre-flight
- [ ] `python -m email_actioning_agent run` → `health` is OK or a known DEGRADED (unauthed inboxes only)
- [ ] Review `data/routed_actions.jsonl` — spot-check categories against intent
- [ ] Confirm Gmail labels exist or are auto-created (`servers/gmail_mcp.ROUTE_LABEL`)
- [ ] `EAA_VELLUM_*` env set so the live run is witnessed to the ledger

## Stage 1 — Tier A/B on one inbox (reversible)
- [ ] Wire the live Gmail-MCP adapter mutators (`apply_label`, `archive`) in `servers/`
- [ ] `run --apply --limit 20` on `byker` only; verify labels/archives in Gmail
- [ ] Confirm every action appears in `telemetry.jsonl` + Vellum; `health=OK`
- [ ] Rollback rehearsal: labels removable, archived mail restorable (it is — reversible)

## Stage 2 — Tier C (human-gated, one at a time)
- [ ] For each `tier_c_pending`: human reviews the action-request and authorises explicitly
- [ ] FINANCIAL Drive/ledger/notify and URGENT_HUMAN push wired only after that authorisation
- [ ] **Never** auto-pay, auto-send, or follow links from FINANCIAL mail (esp. suspected phishing)

## Stage 3 — scale-out
- [ ] Repeat Stage 1 per inbox as each is OAuth'd (CHECKLIST-multi-inbox-auth.md)
- [ ] Schedule via cron/launchd with the health heartbeat (RUNBOOK §Heartbeat)
- [ ] Night Scout: sync `night-scout-feed/` → Beast APDS staging when reachable (`night_scout.py`)
