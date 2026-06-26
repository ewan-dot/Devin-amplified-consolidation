# Cockpit / Intent Interface — Implementation Brief

TIER: STRUCTURED
PROVENANCE: session `80962bca` (2026-06-23, 7 turns)
STATUS: canonical branch picked; build brief drafted for Cursor; not yet implemented
FOR: M5 watcher

## What exists

- **Standardised on finishing the existing Electron `intent-interface` app** as the Cockpit surface over Vellum.
- **Canonical branch: `cursor/20260623120000/vellum-ui-lens`** (latest, working line).
- **Cursor build brief** produced — branch consolidation, PR#2 conflict resolution, preserve all modules, keep Electron packaging, token-optimisation baked in.

### Decisions

- **Electron over Tauri rebuild** — `intent-interface` already exists with live features; rebuilding loses them.
- **Mac mini RAM = 24GB** (corrected mid-session — but cross-check with `80962bca`'s 24GB claim: this was the M5 figure, not the mini. **Open: mini RAM still flagged as a Tier C gate in token-eff impl brief.**)
- **Qwen2.5-Coder 14B Q4** locked as the local free executor (assuming 24GB host, which holds for M5; mini-host re-check needed).
- **"No graphs or spend dashboards in the human surface"** — overrides earlier dashboard ideas.
- **Token optimisation is a design principle**, not a cosmetic feature.

## What was done

- Repo/spec synthesis run.
- Branches compared; canonical pick made.
- Cursor build brief drafted (for branch consolidation + PR#2 conflict resolution + module preservation).
- Earlier cost-dashboard recommendation **retracted** after reading project gates.

## What it means

- **Intent Interface = the only user door** (cross-confirmed in `022ae58e`). All other surfaces (Cursor, Claude Code, Devin, Antigravity) are agent peers behind Vellum.
- **`markPass.ts` (1-9 certainty + ▲ from PCO brief) lives in this app.** The Cockpit is the entry point for the certainty system.
- **"No spend dashboards in the human surface"** conflicts at first glance with the token-eff cost-log + Telegram digest design — *reconciliation*: the digest is for Ewan as operator (an out-of-band notification, not a UI surface). The Cockpit stays clean of spend graphs.
- **Mac mini RAM is still the binding gate** for the local-lane sizing — this session's 24GB was the M5 figure. The mini number is **still open**.

## What to change next

1. **Run the Cursor build brief** — branch consolidation + PR#2 conflict resolution. (Already drafted; needs dispatch.)
2. **Preserve `markPass.ts`** in the consolidation — it is the certainty spine.
3. **Confirm "no spend dashboards" rule** is consistent with token-eff Telegram digest (treat digest as out-of-band notification, not in-Cockpit).
4. **Reconcile Mac mini RAM** — the 24GB confirmation in this session was the M5, not the mini. Mini number still gates local-lane sizing.
5. **Lock Qwen2.5-Coder 14B Q4** as the local executor only after the mini RAM is verified.

## Not yet verified

- Whether `cursor/20260623120000/vellum-ui-lens` is still the latest line as of 2026-06-24.
- Whether PR#2 has been resolved since the session.
- Whether `markPass.ts` is wired to Vellum live or only locally.

## Tier C gates (Ewan only)

- Mac mini RAM (still open, blocks Qwen lock).
- Sign-off on branch consolidation + module preservation list.

[CLOSURE] branch=PLAN | proxy=1 logged | gates=Mac mini RAM (same gate as token-eff) + Cursor build brief dispatch sign-off | inbox=cockpit-intent-interface__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
