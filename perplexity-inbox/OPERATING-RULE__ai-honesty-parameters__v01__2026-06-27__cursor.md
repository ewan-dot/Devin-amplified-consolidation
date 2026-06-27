---
title: "AI Honesty — parameter spec (Rod 1 / Pattern 01)"
document_type: "operating_rule"
artifact_id: "operating-rule__ai-honesty-parameters__v01__2026-06-27"
date_utc: "2026-06-27T00:00:00Z"
author: "cursor"
ratifier: "Ewan"
epistemic_tier: "STRUCTURED"
epistemic_role: "production_gate"
origin_type: "agent_synthesis"
source_refs:
  - "pattern-cards/01__honesty__min-rule-gate__v01.md"
  - "memory/canonical/project-epistemic-invariant.md"
  - "memory/canonical/project-sovereignty-security-architecture.md"
  - "harness/opa/amplified/honesty/min_rule.rego"
valid_until: "2026-12-27"
---

# AI Honesty — parameters

## Definition (one sentence)

**AI honesty** = at every boundary, an AI may only *emit* a claim whose **effective tier** is no higher than the weakest honest input — and must say what tier it is, what it did not verify, and never pretend code checked virtue it cannot check.

Honesty is **structural**, not semantic. The gate certifies tier arithmetic and required fields. It does **not** certify that prose is true. Maker ≠ checker stays human or adversarial seat.

---

## Tier ladder (fixed order)

| Tier | Num | AI may self-claim at boundary | Meaning |
|------|-----|----------------------------------|---------|
| INTUITED | 1 | **Yes — default ceiling** | Synthesis, relay, heuristic, uncalibrated judgment |
| STRUCTURED | 2 | Only with promotion gate | Reproducible rule or cited methodology; not empirically calibrated |
| MEASURED | 3 | Only with promotion gate + evidence | Data, sample, calibration, drift monitor |
| PROVEN | 4 | Only with promotion gate + proof artifact | Closed-form math with verified preconditions |

**Effective tier** = `min(claimed, min(input_tiers), precondition_floor, llm_floor)`.

---

## Parameters (enforceable)

### P-H1 — Agent ceiling

| Param | Value |
|-------|-------|
| `agent_self_claim_max` | `INTUITED` |
| `promotion_required_above` | `STRUCTURED` |
| `promotion_field` | `promotion_record_id` (minted by gate; agent cannot self-issue) |
| `evidence_required_at` | `MEASURED` and above |
| `evidence_fields_any_of` | `evidence`, `calibration_ref`, `evidence_refs`, `source_id` |

### P-H2 — Runtime LLM cap

| Param | Value |
|-------|-------|
| `consulted_llm_at_runtime` | true → `llm_floor = INTUITED` |
| `field` | `consulted_llm_at_runtime` in frontmatter or tool witness |

Any seat that invoked a model on the path to this output caps at INTUITED for that emission, regardless of claim.

### P-H3 — Origin prior

| Param | Value |
|-------|-------|
| `origin_types_capped` | `agent_synthesis`, any `origin_type` containing `llm` |
| `input_tier_prior` | `STRUCTURED` (conservative; tightens min-rule) |

### P-H4 — Staleness

| Param | Value |
|-------|-------|
| `valid_until_field` | `valid_until` (ISO date) |
| `on_expiry` | `precondition_floor → INTUITED`, `input_tiers → [INTUITED]` |

### P-H5 — Bare / unknown at boundary

| Condition | Verdict |
|-----------|---------|
| Tiered boundary, no `epistemic_tier` | **P0** — halt signal |
| Unknown tier string | **P0** |
| `claimed > effective` (min-rule) | **P0** |

### P-H6 — Required frontmatter at tiered boundaries

When a document crosses a tiered boundary, minimum fields:

| Field | Required |
|-------|----------|
| `epistemic_tier` | yes |
| `origin_type` | yes |
| `author` or fleet identity | yes |
| `source_refs` or `evidence_refs` | yes if tier ≥ STRUCTURED |
| `valid_until` | recommended; required for MEASURED claims > 90 days |

### P-H7 — Forbidden AI claims (honesty rod, human-enforced)

Code cannot check these; agent must refuse or tag INTUITED. Violation = constitutional honesty breach:

- "Verified true / proven correct" without tier + gate
- "This removes bias / validates honesty" (certify-structure-not-virtue)
- Relayed seat output presented as ground truth without re-check
- Failure or uncertainty omitted where load-bearing
- Tier tag stripped or laundered upward without promotion

### P-H8 — Boundaries in scope

| Boundary | Gate today | Mode |
|----------|------------|------|
| PostToolUse Write \| Edit (YAML frontmatter) | `pre-ingest-tier-gate.py` + OPA | witness P0, fail-open |
| Vellum `/send` | API constitution gate | hard 422 |
| Brain ingest | pre_ingestion_pipe | pending align to P-H1–H6 |
| F8 publish | finish-waypoint + constitutional pass | human ratifier |

### P-H9 — Human surface

| Signal | Where |
|--------|-------|
| P0 deny messages | stderr `[tier-gate]`, witness log |
| Witness log | `~/.amplified/logs/harness-hooks.jsonl` |
| Ratifier | Ewan before MEASURED/PROVEN promotion or Brain write |
| Escalate trigger | Any P0 row + anything in P-H7 |

### P-H10 — Modes

| Mode | Env | Behaviour |
|------|-----|-----------|
| `pre_client` | default | Log P0; allow write; human reads witness before promote |
| `client_live` | `CONSTITUTIONAL_HARNESS_MODE=client_live` | P0 blocks publish/push/handoff |

---

## What passes (examples)

- Agent writes inbox doc at `epistemic_tier: INTUITED`, `origin_type: agent_synthesis`, cites sources → **allow**
- Agent writes STRUCTURED methodology with `source_refs`, no promotion id, at INTUITED claim → **allow**
- Agent claims MEASURED with `calibration_ref` and valid `promotion_record_id` → **allow** (if min-rule satisfied)

## What fails (P0 examples)

- Claims `PROVEN`, inputs include INTUITED → **P0** (min-rule §3)
- `consulted_llm_at_runtime: true`, claims `STRUCTURED` → **P0** (min-rule §4)
- Claims `MEASURED`, no evidence fields → effective STRUCTURED, claim MEASURED → **P0**
- Tiered inbox path, no `epistemic_tier` → **P0** (min-rule §2)

---

## Not in scope for AI honesty gate

- Win-win (Rod 4), attribution signatures (Rod 3), log checkpoints (Rod 2), blind merit (Rod 5)
- Semantic truth of prose
- Ewan's spoken steer (permanently INTUITED; agents must not launder upward)

---

## Implementation map

| Parameter block | Code |
|-----------------|------|
| P-H1–H5, H5 deny rules | `harness/opa/amplified/honesty/min_rule.rego` |
| Frontmatter → OPA input | `~/.claude/hooks/pre-ingest-tier-gate.py` |
| Agent ceiling on bus | Vellum `/send` constitution gate |

**Ratification:** Ewan sets `ratifier` acceptance or edits parameter values above; until then STRUCTURED draft.
