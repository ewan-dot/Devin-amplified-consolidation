# Perplexity-Inbox — Coverage Audit (recent threads vs landed artifacts)

TIER: STRUCTURED · thread list MEASURED from session memory index; mapping to inbox artifacts STRUCTURED by content match.
PROVENANCE: `memory/sessions/sessions_index.md` + summary.md for each session + verbatim read of every inbox file (2026-06-24T12:15).
CORRECTION: my first pass (`perplexity-inbox__mesh-plan__v01`) audited the inbox in isolation. You asked the right question: does the inbox reflect the **last several Computer threads**? The answer is partial — it covers ~4 threads cleanly. Nine threads of substantive work have **no artifact** in the inbox.
FOR: Ewan + the M5 watchers, so the gap is visible.

---

## What "last several threads" actually contains

Filtering session memory to substantive Computer threads from 2026-06-16 onward (excluding 1-turn pokes, dedup/Hazel ops, casual asides):

| Thread | Topic | Inbox artifact | Status |
|---|---|---|---|
| `fe675ab4` (Jun 23-24, 19t) | Token-efficiency programme — full | `token-efficiency-programme__2026-06-24/` + impl brief | ✅ landed |
| `e1e80901` (Jun 24, 10t) | Standing-grants skill refinement (HITL, research-as-endpoint) | `amplified-standing-grants` skill v1.2 + `amplified_rules.json` + `amplified_harness.py` + README | ✅ landed |
| `363c44fd` (Jun 21-22, 41t) | Sovereign multi-agent env / 17-field front matter / deterministic floor / master synthesis | `sovereign-multi-agent-environment__2026-06-24/` | ✅ landed |
| `a4942258` (Jun 22-24, 42t) | Boundary/seam research, pipe prompt, lens through standing-grants | folded into standing-grants + closure | ✅ landed (as skills) |
| `4a26d8c1` (Jun 16-22, 30t) | Token optimisation, PCO layers, Lens selector, Claude CLI topology | partially folded into token-eff bundle | ⚠️ partial — PCO layers + Lens selector NOT carried |
| `e28029b3` (Jun 17-18, 72t) | AI-native compatibility search methodology, Hansard/ONS/Companies House, CAMS intuitee | none | ❌ missing |
| `41ab7b59` (Jun 17-18, 33t) | VSCodium agent guide + Vellum/Opik/Langfuse/GitKraken/GitLens | none | ❌ missing |
| `46e85c2e` (Jun 19, 21t) | **Relay protocol** (uses Vellum), UI integration, transport | none | ❌ missing |
| `f6ae6952` (Jun 19-24, 23t) | Agent workspaces, manufacturer-recommended layouts, Claude Code in-cell, **repo consolidation + asset inventory** | partially folded into sovereign synthesis Part 2 | ⚠️ partial — repo consolidation list NOT carried |
| `7dd0ce64` (Jun 21, 22t) | Canonical routing spec + token-balancing, antigravity scans, Vellum senses | partially folded into estate-spec | ⚠️ partial — Vellum senses research NOT carried |
| `a35a5461` (Jun 21, 12t) | GitHub security hardening, "no human approval gate is madness" | sovereign-build's GitHub section is consistent | ⚠️ partial — no standalone artifact, no critique log |
| `94681082` (Jun 22, 22t) | **Open-door universal harness ("blinkers without ceilings")**, DeerFlow-on-Beast trial, VSCodium Mac bootstrap, single-user + Apple Containers, **Baton write lease + RodGuard circuit breaker**, **Claude Code as keyholder** | none | ❌ missing — and these are foundation pieces the harness in the inbox assumes |
| `244626bd` (Jun 22-24, 23t) | M5 consolidation, YAML-aware `dedup_apply.py`, Antigravity workspaces audit | none | ❌ missing (the dedup script is on the Mac, not in inbox) |
| `022ae58e` (Jun 23, 6t) | VSCodium IDE + Anthropic API + local model + Vellum integration + DeerFlow Q1 | none | ❌ missing |
| `80962bca` (Jun 23, 7t) | Robust UI spec, canonical (single source) decision, 24GB M5 figure, token-optimised UI design | none | ❌ missing |
| `3ae460be` (Jun 24, 7t) | **Deterministic core schemas**, Opik wiring, **Perplexity ON the Beast live**, AI self-ratification | none | ❌ missing |
| `01587f48` (Jun 24, 2t) | **JWT tokens in Vellum** — nobody can get access | none | ❌ missing — and this is a live blocker on Vellum writes |
| `561d20e5` (Jun 24, 1t) | "Primary unit of synthesis — what should each filled blank connect to" | possibly UI-methods orchestrator | ⚠️ unclear |

**Score:** 4 threads fully landed, 4 partially landed, 9 not in the inbox.

---

## What this means for "does it all link together"

The inbox is cohesive **within its own four-thread subset** — the mesh-plan analysis stands. But three of the missing threads are **upstream** of what's in the inbox, and one is **a live blocker**. The inbox is not fighting with itself, but it is missing pieces it depends on.

### Critical gaps (the inbox depends on these and they're not landed)

1. **Open-door universal harness + Baton + RodGuard (`94681082`).** The `amplified_harness.py` in the inbox is a permission classifier — it is NOT the universal open-door harness from this thread (which has Baton write lease, RodGuard circuit breaker, logged door-open events, Claude Code as keyholder). Two different "harnesses" with the same word. **Risk:** M5 watcher implements one and assumes the other exists.

2. **Vellum JWT access (`01587f48`).** "Nobody can get access to the JWT." Token-eff §E1 and the Vellum events JSONL both assume Vellum writes work. If JWT access is unresolved, the §9.7 telemetry proof gate is dead on arrival. **This belongs in the inbox as a Tier C gate, not just a thread aside.**

3. **VSCodium agent guide (`41ab7b59`, `022ae58e`, `94681082`).** The enforcement plan bakes `managed-settings.json` and hooks into "Claude Code lane" and "Cursor lane" — but a VSCodium lane was the explicit target across three threads (Claude inside VSCodium, with Vellum/Opik/Langfuse wired). The inbox plans Claude Code + Cursor; **VSCodium is a third lane that the enforcement plan doesn't cover.**

4. **Deterministic core schemas + Perplexity-on-Beast-live (`3ae460be`).** The `amplified_rules.json` is a deterministic projection — but the broader deterministic-core schemas from this thread (which feed metric ownership, AI self-ratification logic) are not in the inbox. The harness in the inbox is the simpler classifier, not the full deterministic core.

5. **Relay protocol (`46e85c2e`).** Relay-uses-Vellum was named as the existing transport. None of the inbox docs mention Relay. The estate-spec talks about a credit-first router; Relay would be the transport beneath it. **If Relay is the canonical transport, the inbox doesn't say so.**

### Partial carries (something landed, but not the whole)

6. **PCO layers + Lens selector (`4a26d8c1`).** Token-eff bundle carries the routing/caching/CLI-vs-MCP evidence but does not mention PCO layers or the Lens selector. If those are the routing primitives, the spec is using different vocabulary.

7. **Repo consolidation + asset inventory (`f6ae6952`).** Sovereign synthesis describes the per-cell repo model but not the **inventory of existing assets** Ewan said to either use or drop. That inventory was promised; it is not in the inbox.

8. **Vellum senses research (`7dd0ce64`).** Named explicitly; not carried.

9. **GitHub hardening critique (`a35a5461`).** The "no human approval gate is madness" critique drove the sovereign-build's GitHub config. The critique itself — what was verified-live broken vs what's now fixed — is not logged as an inbox artifact. If you can't see the diff, you can't prove the fix.

### Honest gaps with no obvious owner

10. **AI-native compatibility search / Hansard/ONS/Companies House / CAMS (`e28029b3`).** 72 turns of methodology work with no landed artifact. This is the largest unaccounted-for thread.

11. **DeerFlow trial brief (`94681082`, `022ae58e`).** Designed; not landed.

12. **Robust UI spec, single-source canonical decision (`80962bca`).** Discussed; not landed.

---

## The honest cohesion verdict, restated

- **Inbox internally:** strong cohesion, six small seams (per `perplexity-inbox__mesh-plan__v01`). Stands.
- **Inbox vs recent threads:** ~40% coverage. Nine threads of work either fully missing or partially carried.
- **Risk:** the inbox can be implemented to its own internal proof gate while the threads it depends on (open-door harness, Vellum JWT, VSCodium lane, Relay, deterministic-core schemas) sit unbuilt. Token-eff §9 PROOF-OF-LIFE could pass on a foundation that doesn't include half the recent decisions.

This is the answer to your question. The work that's been done is **not all in the inbox**, and some of what's not in the inbox is structurally upstream of what is.

---

## What to do about it (the recovery path, not a re-derivation)

You asked for a plan that ties threads together. Two ways to do that:

### Path A — Land the missing threads as inbox briefs (recommended)

For each of the 9 ❌/⚠️ rows above, produce one short implementation brief in the inbox, even if it just says "designed, not built — next action is X". The brief format already exists (`*__implementation-brief__v01__2026-06-24__perplexity.md`). Once landed, the M5 watcher sees the whole estate, not just a slice. The mesh-plan's six seams then apply across the full surface.

Order (cheapest, highest-unblock-first):

1. **Vellum JWT brief** — escalate as Tier C; nothing telemetry-ish works without it.
2. **Open-door harness brief** — rename to disambiguate from `amplified_harness.py`; state Baton + RodGuard + Claude-Code-as-keyholder design.
3. **VSCodium lane brief** — add as a third lane in the enforcement plan with its own `managed-settings.json` equivalent.
4. **Deterministic-core schemas brief** — what the rules JSON projects from, including metric ownership and self-ratification.
5. **Relay protocol brief** — state whether Relay is the transport beneath the credit-first router, or whether they're alternatives.
6. **GitHub hardening verification brief** — the diff between "was broken" and "now fixed" + the live verification.
7. **Repo consolidation + asset inventory brief** — list assets, mark use/drop.
8. **PCO layers + Lens selector brief** — reconcile vocabulary with token-eff.
9. **AI-native compatibility search methodology brief** — what came out of the 72 turns.
10. **DeerFlow trial brief** — designed; either land or kill.
11. **Robust UI spec brief** — single-source canonical decision logged.
12. **Vellum senses research brief** — capture what was found.

This is ~12 briefs of 1-3 pages each. They are research outputs from work already done — Tier A, no gates beyond the existing ones (Mac mini RAM, skill deletions, JWT access, name lock, §9 gate).

### Path B — Decide the missing threads are deferred (alternative)

If the goal is just to ship the token-efficiency programme and the sovereign cell build, then explicitly **park** the other 9 threads with a one-line "deferred, will be re-opened after PROOF-OF-LIFE" note in the inbox. Same effect — visibility — without writing all the briefs.

Either is honest. Both are better than the current state, where the inbox looks complete but isn't.

---

## What stays true

- The six seams in `perplexity-inbox__mesh-plan__v01` are real and should still be welded before implementation.
- The four landed threads are cohesive with each other.
- The pipe + min-rule + ladder + closure spine holds across everything I read.
- The Tier C gate cluster (Mac mini RAM, skill deletions, name lock, §9 ratification) is still the correct hand-back — now **+ Vellum JWT access**, which I missed in the first pass.

---

## Provenance + tiering

- Thread list from `memory/sessions/sessions_index.md` (preloaded session memory, 2026-06-15 → 2026-06-24).
- Per-thread topic extracted from session `summary.md` where present, query previews otherwise.
- Mapping inbox-artifact ↔ thread by content match (filename + body content vs thread queries). STRUCTURED, not fitted.
- One ambiguity: `561d20e5` ("primary unit of synthesis") may be the UI-methods thread or something else; flagged.
- Effective tier = STRUCTURED. Coverage percentage (~40%) is an STRUCTURED estimate over a 13-thread denominator; the missing-thread list is the load-bearing claim, not the number.

[CLOSURE] branch=PLAN | proxy=1 logged (coverage audit drafted as AI_PARTNER_PROXY) | gates=Vellum JWT access + Mac mini RAM + 3 skill deletions + name-lock ratification + §9 gate ratification + decide Path A or Path B | inbox=perplexity-inbox__coverage-audit__v01__2026-06-24__perplexity.md | tier=STRUCTURED
