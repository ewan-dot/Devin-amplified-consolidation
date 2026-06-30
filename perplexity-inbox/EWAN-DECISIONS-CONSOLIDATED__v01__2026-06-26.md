# Consolidated Decision Sheet — everything blocked on Ewan

**Drafted:** 2026-06-26 by cascade-mac · **TIER: STRUCTURED**
**Purpose:** One deduplicated hand-back. Three separate lists (control-centre blockers · perplexity INBOX-INDEX 13-item Tier C cluster · unified-harness 6 Qs) overlapped heavily. This merges them so you can clear the critical path in one sitting.

**How to use:** Answer inline (one line each is fine). Items are ordered by *how much they unblock*, not by source. ⏱ = ~1-minute action. 🔑 = admin/credential. 🧭 = decision/ratification.

---

## TIER 1 — Live-infrastructure unblockers (everything telemetry-ish is dead until these clear)

| # | Item | Action | Source |
|---|------|--------|--------|
| 1 | 🔑 **fleet-vellum PAT write** | Add `contents:write` for `fleet-vellum` to the 1Password "API GITHub" PAT. Unblocks the fleet-vellum analytics-engine stats DDL patch. | control-centre |
| 2 | 🔑 **Vellum fleet-read token** | cascade-mac's JWT returns 0 agents. *Code* side now fixed (control-centre #5 merged: SSL self-signed + `identity` key). *Scope* side: the JWT needs fleet-read permission. Confirm/issue. | control-centre + inbox #6 |
| 3 | 🔑 **cascade-mac Vellum floor** | Raise INTUITED → STRUCTURED (Vellum admin). Until then cascade-mac's STRUCTURED/MEASURED posts fail the constitution check. | control-centre |
| 4 | 🔑 **Vellum JWT TTL + Infisical** | Choose TTL (30d suggested) · fix-Infisical-now **vs** stopgap auto-mint · sheet scope for shared_dev · slug-vs-UUID for sheet_ids. | inbox #6 |
| 5 | ⏱🧭 **Beast `estate-machine` stack** | Appears dark (Traefik default backend serving). Intentional, or a surprise? One line. | inbox #9 |
| 6 | ⏱ **PostgreSQL connector** | Connect it in Perplexity (~1 min). Unblocks brain collector verification. | inbox #9 |
| 7 | ⏱ **OPEC = OpenTelemetry?** | One-line confirm. | inbox #9 |

---

## TIER 2 — The one estate fact that unlocks several specs

| # | Item | Action |
|---|------|--------|
| 8 | ⏱ **Mac mini RAM (the M5 — 24GB?)** | This single number locks local-model tier sizing AND the Qwen2.5-Coder 14B Q4 confirmation, and unblocks 3+ acceptance tests across token-efficiency (#1, #14). |

---

## TIER 3 — Unified-harness build decisions (build stays blocked until Q1/Q2/Q3/Q7/Q8)

| # | Item | Action |
|---|------|--------|
| 9 | 🧭 **Q1 — Framework** | Option A / B / C. (Note: DeerFlow routes to LLM providers, not agent surfaces — factor in.) Also resolves inbox #16 DeerFlow disambiguation — *same question*. |
| 10 | 🔑 **Q2 — Devin plan type** | Service-user API keys are Teams/Enterprise only; individual unconfirmed. Which plan? |
| 11 | 🧭 **Q3 — Antigravity scope** | Not deployed on Beast. In scope for v1 or not? |
| 12 | 🧭 **Q7 — Brief contract** | Brief v04 isn't on disk/KB. Confirm v02 + addendum *is* the contract, or provide v04. |
| 13 | 🧭 **Q8 — Front-door scope for v1** | What's the minimum Vellum front-door for v1? (Depends on Phase 2 InterruptPane/knock — assigned cell-1, pending.) |
| 14 | 🧭 **Q9/Q10 (lower priority)** | Knock policy / auto-yes threshold · spillover trigger signal. |

---

## TIER 4 — Single ratifications (one word each)

| # | Item | Action |
|---|------|--------|
| 15 | 🧭 **Name lock** | `Beast` in code; `Infrastructure 1` in external framing. Confirm. |
| 16 | 🧭 **§9 PROOF-OF-LIFE** | Ratify as the definition of "token-efficiency done". |
| 17 | 🧭 **Harness name disambiguation** | Three layers, three names: `amplified_permissions.py` (classifier) vs `open_door_runtime/` (Baton+RodGuard) vs the constitutional gate engine. Confirm the split. |
| 18 | 🧭 **Lens selector status** | Routing layer renamed, or separate primitive? |
| 19 | 🧭 **PR #6 Vellum posting-path** | control-centre has `_post_to_vellum` (inline, in-memory) already on main; W3 PR #6 adds `_post_findings_to_vellum` (DB-queried, post-render). Unify on one, or keep both? (Needed to land #6 once Beast is up.) |

---

## TIER 5 — Manual / read-only ops (you, by hand)

| # | Item | Action |
|---|------|--------|
| 20 | **3 Perplexity skill deletions** | decision-log-labeler · utterance-tagger · org-scope iso-8601. |
| 21 | **`mdutil -E /`** | Spotlight reindex. System-level, spikes CPU. Go/no-go. |
| 22 | **Provide AI-native search methodology file** | 72 turns of work (`e28029b3`) never landed — the biggest single unrecovered input. Filename in Downloads, thread link, or paste. |

---

## Score after this session (what cascade-mac cleared without you)

- ✅ control-centre **#5 merged** — Vellum 0-agents *code* fix (SSL + identity key) on main
- ✅ control-centre **#2 closed** — superseded by main's direct Beast deploy
- ✅ control-centre **#6 documented** — merge recipe posted; held for Beast + item 19
- ✅ agent-claude **#9 assessed** — harnesses correct; 3 failures all environmental (Beast down / local checkout). One polish nit: live tests should skip-not-fail when Beast unreachable.

**Still 🔴 on Beast (now back per Ewan, but M5 still can't see it — `rx 0`):** verify 38 criticals · deploy · live Vellum validation. See Beast note.

[CLOSURE] branch=PLAN | gates=22 consolidated, deduped across 3 source lists | tier=STRUCTURED
