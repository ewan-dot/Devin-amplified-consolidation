# Vellum JWT Recovery — Implementation Brief

TIER: MEASURED (token expiry decoded from payloads + system clock; signing-secret verified cryptographically)
PROVENANCE: session `01587f48` (2026-06-24 09:20-09:32 UTC); `~/.amplified/stoa_claude_jwts.json`; `~/.vellum/intent-interface.env`; Infisical methodology doc
STATUS: implementation-ready (plan in Ewan's hands for Claude Code)
FOR: M5 watcher → Claude Code

## What exists

- 3 HS256 JWTs in `~/.amplified/stoa_claude_jwts.json` (stoa, claude, shared_dev). All issued 2026-06-09, 7-day TTL, **expired 2026-06-16 14:33 UTC — dead 8 days as of 2026-06-24**.
- `VELLUM_JWT_SECRET` in `~/.vellum/intent-interface.env` — 28 chars, SHA256[:12] = `f49b1c6ca041`. **Cryptographically verifies all three old tokens** → it is the genuine signing key the Beast used.
- Static Vellum bearer token: still working (startup.log shows HTTP 200 through 2026-06-23).
- Infisical state: **4 projects, 0 secrets populated**; documented admin-token-lacks-org-scope 401 bug. Never served the signing secret. Pre-existing, not caused by the recent tidy-up.
- `shared_dev_jwt` has **no `sheet_id`** — broken even before expiry (verifier requires it).

## What was done

- Decoded all three JWTs; verified expiry timestamps and signature against the env secret.
- Confirmed the tidy-up did not break the key.
- Drafted the Claude Code handover plan: canonical verifier source (`vellum/auth/tokens.py`), exact claim shape, real Beast endpoint, known sheet IDs, the three distinct auth surfaces (so they don't get conflated), and the non-secret fingerprint to compare Mac↔Beast secrets without printing either.

## What it means

- **The inbox depends on this.** Token-eff §E1 (Vellum telemetry), the harness's Vellum write events, and any `[CLOSURE]` footer claiming `system_of_record: Vellum` all silently fail until JWTs are live again.
- This is the *first* Tier C gate. Mac mini RAM is the second. Without fresh JWTs, the §9 PROOF-OF-LIFE telemetry line in the token-eff spec cannot pass.

## What to change next

1. **Re-mint 3 JWTs** with the verified secret, new exp. Claude Code runs the mint script; Perplexity drafts the values; Ewan places them.
2. **Decide TTL** — recommend 30d given rotation path is broken. (Ewan-only.)
3. **Add `sheet_id` to shared_dev**. Slug-vs-UUID decision (Ewan-only).
4. **Populate VELLUM_JWT_SECRET into Infisical** `beast-infrastructure` project; fix org-scope/service-token issue. This is the structural fix that stops recurrence.
5. **Decide:** fix Infisical now, or run a stopgap auto-mint cron until the proper rotation is in. (Ewan-only.)

## Not yet verified

- Beast verifies with the same secret (strongly implied by cryptographic match on the Mac side; not live-confirmed — Perplexity sandbox has no Beast network).
- Whether the dark `estate-machine` service stack (separate finding, session `3ae460be`) affects JWT acceptance once minted.

## Tier C gates (Ewan only)

- TTL choice (30d suggested).
- Infisical-now vs stopgap.
- Which sheet `shared_dev` scopes to.
- Slug-vs-UUID for sheet_ids.

[CLOSURE] branch=PLAN | proxy=1 logged (recovery brief drafted as AI_PARTNER_PROXY) | gates=TTL + Infisical-vs-stopgap + sheet scope + slug/UUID (4 questions, single hand-back) | inbox=vellum-jwt-recovery__implementation-brief__v01__2026-06-24__perplexity.md | tier=MEASURED
