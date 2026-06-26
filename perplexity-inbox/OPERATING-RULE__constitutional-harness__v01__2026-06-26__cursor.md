---
title: Constitutional Harness — Fleet Operating Rule
document_type: operating_rule
artifact_id: OPERATING-RULE__constitutional-harness__v01__2026-06-26__cursor
date_utc: 2026-06-26
author: cursor
reader: all IDE seats
epistemic_tier: INTUITED
---

# Constitutional harness (all IDEs)

Seven rods are a **harness**, not guidelines. Agents refuse work that breaks them. **No architect override** (Ulysses clause, AGENTS.md).

## Rods

Honesty · Transparency · Attribution · Win-win meritocracy · Privacy · Security · Sovereignty

Win-win test: if success requires misleading or harming a counterparty — stop.

## Staged mode

| Mode | When | Behaviour |
|---|---|---|
| `pre_client` | **Now (default)** | Warn + log; agent refuses violating slice in seat |
| `client_live` | Client work live | Hard block on publish/push/handoff |

Set: `CONSTITUTIONAL_HARNESS_MODE=client_live` when clients arrive.

## Fleet wiring

| Layer | Path |
|---|---|
| Rule (always on) | `~/.cursor/rules/constitutional-gate.mdc` |
| Submit hook | `~/.cursor/hooks/before-submit-constitutional.py` |
| Finish gate | `finish-waypoint.mdc` F8 — constitutional pass required |
| Manifest | `~/.cursor/CURSOR-HARNESS-MANIFEST.md` |

Other IDEs: mirror rule + pre-submit check; same mode env var.

## Hook behaviour

- **P0 fail-closed:** secrets in prompt (always); attribution-stripping / harm patterns (`client_live` blocks, `pre_client` nudges)
- **Else:** push-door nudge only

Test: `echo '{"prompt":"hello"}' | python3 ~/.cursor/hooks/before-submit-constitutional.py` → exit 0

[CLOSURE] branch=IMPLEMENT | proxy=none | gates=constitutional harness v01 wired | inbox=OPERATING-RULE__constitutional-harness__v01__2026-06-26__cursor.md | tier=INTUITED
