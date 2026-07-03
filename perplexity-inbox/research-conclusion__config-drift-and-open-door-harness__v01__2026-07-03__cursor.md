---
title: "Config Drift Root-Cause + Open-Door Harness — Fix-and-Encode Index"
document_type: research_conclusion
artifact_id: research-conclusion__config-drift-and-open-door-harness__v01__2026-07-03__cursor
date_utc: 2026-07-03
project: Amplified Partners
author: cursor
reader: ewan
epistemic_tier: STRUCTURED
tier_reason: "Forensic diagnosis over git commits, rule files, and Vellum witness — verified. Prevention-effectiveness claims are INTUITED until re-drift is observed (or not) over time."
ratifier: Ewan
supersedes: none
vellum_witness: 3cf807d5
---

# Config Drift Root-Cause + Open-Door Harness — Fix-and-Encode Index

> This is an **index + lessons** doc. It points at canonical artifacts; it does not duplicate them.

## 0. Meta-principle (lead with this)

**A gap, once found, must be FIXED *and* ENCODED — durably, in BOTH config (rules/hooks) AND docs — never left to recur.**

Fixing in chat only is not a fix; it evaporates at session end. The compound loop is: *find gap → fix it → encode the fix as capital (rule/hook/doc) → witness on Vellum*. If the same ignorance can be re-discovered next session, the loop is not closed. This doc exists because this session re-discovered gaps that a prior session had "handled in chat" — the exact failure mode the principle forbids. (See `self-compound.mdc`.)

---

## 1. Findings + root causes (forensic)

| # | Symptom | Root cause | Evidence |
|---|---|---|---|
| 1 | **Rule-softening** — `ewan-core-rules.mdc` shrank to a 353B stub | Self-compound had an agent *regenerate rules from working memory* and saved the **summary as canonical**. Constitution "born thin". | commit `87182ca`, 2026-06-26 |
| 2 | **File scatter / loss** | `~/Downloads` used as a working dir; SSOT repo had **no `.gitignore`**; recovery bundles were **re-created instead of referenced**. | untracked churn; duplicate bundles |
| 3 | **Fragile + token-expensive tooling** | MCP is the brittle path — the whole Beast MCP set was **down all session** (`-32602` FastMCP arg-drop). | session logs |
| 4 | **Redundant redesign** | Open-door harness had already been designed **~4× on-Mac** and shipped code — yet was being re-researched from scratch. | prior-art scan (artifact in §4) |

---

## 2. Fixes + where encoded (so anyone can find them)

| Gap (from §1) | Fix | Encoded at |
|---|---|---|
| 1 Rule-softening | Constitution restored; **all `rules/*.mdc` uchg-locked**; **lock-aware self-heal** | commit `3bfbb29` |
| 1 (prevent recurrence) | **fullness-guard** (self-heal refuses to restore a thinned canonical) + **self-compound constitution-exclusion** (never regenerate locked rules) | commit `8bc657a`; `self-compound.mdc` |
| 2 File scatter | `.gitignore` added; **`~/Downloads` quarantined** out of the workspace | commit `8bc657a` |
| 2 (verify) | **Integrity manifest + verify** script | commit `d904cad` |
| 3 Tooling | **`vellum-access.mdc`** rewritten **tailnet-first** — prefer direct Beast HTTP (curl) over MCP; MCP as fallback | `vellum-access.mdc` |
| 4 Redesign | **Open-door SSOT consolidated** + **Phase 0 scaffold** — consolidate, do not re-research | commit `8510fd8`, worktree `feat/open-door-phase0` |
| all | Session witnessed | Vellum entry `3cf807d5` |

---

## 3. Canonical artifacts (pointers — read these, don't rebuild them)

All under `perplexity-inbox/` (dated 2026-07-03, author cursor):

- `SSOT__open-door-harness__v01__2026-07-03__cursor.md` — the single source of truth for the door harness.
- `DESIGN__open-door-harness__v01__2026-07-03__cursor.md` — design.
- `RESEARCH__open-door-harness-prior-art__v01__2026-07-03__cursor.md` — proves it was already built ~4×; **read before any redesign**.
- `RESEARCH__cursor-heavyuser-harness-guidance__v01__2026-07-03__cursor.md` — Cursor heavy-user harness guidance.
- Integrity **README + manifest/verify** — see commit `d904cad`.

Prior lineage (do not duplicate): `research-conclusion__hooks-harnesses-as-doorways__v01__2026-06-26__cursor.md`, `research-conclusion__doors-telemetry-completion__v01__2026-06-26__cursor.md`.

---

## 4. Prevention now in place

- Locked constitution + lock-aware self-heal → a rule **cannot** be silently softened.
- Fullness-guard → self-heal **refuses** to restore a thinned canonical.
- Self-compound constitution-exclusion → agents **never** regenerate locked rules from memory (additive-only, through the lock cycle).
- `.gitignore` + Downloads quarantine + integrity verify → scatter/loss caught deterministically.
- Tailnet-first Vellum access → the token-expensive/fragile MCP path is the **fallback**, not the default.

## 5. What remains

- **Phase 1**: door presets (the per-door permission surfaces on top of the Phase 0 scaffold).
- **Cross-repo `amplified_harness` rename** — propagate into `Antigravity/` and `intent-interface/`.
- Land `feat/open-door-phase0` (another worker owns git this session — do not commit from here).
