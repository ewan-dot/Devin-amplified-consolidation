---
name: baton-pass
description: >-
  Operationalises the seat-to-seat BATON PASS (agent/seat handoff) per relay-stop,
  finish-waypoint, and vellum-witness rules. Use when any seat says "hand off",
  "seat close", "pass the baton", "relay stop", "wrap up for the next agent",
  or whenever ~65–70% context capacity is reached on non-trivial work.
  Covers full PASS protocol: seat-pass doc → Vellum witness → baton write → shared path.
---

# Baton Pass

## CHANGELOG

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-07-03 | Initial skill — consolidates relay-stop.mdc, finish-waypoint.mdc, vellum-witness.mdc, baton_lifecycle.py, AGENTS.md seat-pass, and sovereignty-with-mutuality model. First CHANGELOG entry; no defects found (nothing to retroactively fix yet). |
| 0.1.1 | 2026-07-08 | cursor evening-seat handoff: clean pass (baton via harness to batons/active; 05-pass.md at `code/agents/cursor/05-pass.md` updated with prior PASS retained as history; Vellum preform 9bfcc0e0). Lessons: (1) baton harness truncates long titles (~50 chars) in the filename — keep `--title` short; (2) `05-pass.md` lives per-seat at `ingestion-to-research-pipe/code/agents/<seat>/05-pass.md`, not repo root; (3) Vellum estate/log requires `metadata:{repo,action,pr}` or 422 — payload shape documented in the baton body. |

---

## When to invoke

- **~65–70% context capacity** on any non-trivial seat (relay-stop.mdc: "stop at 65–70%").
- Any of the explicit stop triggers applies (see relay-stop.mdc): next step needs external verification, you would have to guess repo/API shape, one PR-slice is done and fresh eyes add more value, attention is fuzzy on preconditions.
- **Cross-IDE handoff** (Cursor → Antigravity, Cursor → Devin, etc.) — companion to finish-waypoint.mdc.
- **Session wrap** — always before closing a seat that did non-trivial work.

Invoke even when the work is partial or blocked. "Undone is a valid baton state" (relay-stop.mdc).

---

## Full PASS protocol (in order)

Do all three. No session ends without all three (relay-stop.mdc).

### Step 1 — Update seat-pass doc (`05-pass.md`)

Fill only the `[ENGINEER-WRITE]` fields (vellum-witness.mdc):

| Field | What to write |
|-------|---------------|
| `done_this_seat` | Verified delta — what was completed, not intentions |
| `next_seat_should` | 3–5 concrete, actionable bullets for the next seat |
| `blockers` | Anything that stopped progress, with enough detail to unblock without re-investigation |
| `feedback` | Quality signal on the pack/preparation: `good` / `weak` / `missing` |
| `delta_reason` | Why the outcome differed from the prediction (if it did); omit if on-track |

Do **not** write `[AUTO]` fields — git SHA, timestamps, experiment IDs, seat duration. The system fills these.

### Step 2 — Fill Vellum `preform-seat-pass`

Authority: vellum-witness.mdc.

- Post using the correct seat slug: `cursor`, `antigravity`, `devin`, `cascade`, `scribe`. Never a tool-name prefix (`codex-mcp/cursor` is WRONG — the identity is `cursor`).
- Epistemic tier: `INTUITED` for all AI-authored Vellum entries.
- Verify topology before writing: Beast `:8400` is the fleet ledger; `127.0.0.1:8400` is the dev sandbox — writes there do NOT reach the fleet. Check `~/Code/VELLUM-TOPOLOGY.md` if unsure.
- If Beast Vellum is unreachable, hold the write and flag it. Do not silently drop it.

### Step 3 — Write the baton file

Authority: baton_lifecycle.py (`perplexity-inbox/harness/baton_lifecycle.py`).

```bash
python3 /Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/harness/baton_lifecycle.py write \
  --from cursor \
  --to next-seat \
  --title "<slug-title>" \
  --seat cursor \
  --body-file /path/to/baton-body.md
```

Or inline body:

```bash
python3 …/baton_lifecycle.py write \
  --from cursor --to next-seat \
  --title "seat-slug-here" \
  --body "## Done this seat\n…\n\n## Next seat should\n1. …"
```

The harness auto-rotates: active max 5 → unified archive → datalake bronze. Never manage that rotation manually.

**Landing paths (active batons):**
- `perplexity-inbox/batons/active/BATON__<slug>__v01__<date>__<seat>.md`

**Shared company path requirement** (finish-waypoint.mdc): the baton must land in a shared path (`~/amplified-pipeline/`, `perplexity-inbox/`, control-centre, or Beast via PR), not worktree-only.

---

## Baton body — what to write

Write thinking about what you would want to read if you were starting cold (relay-stop.mdc).

```markdown
# Baton pass — <seat> — <date>

## Done this seat (verified)
- <bullet per completed item, verified delta only>

## Open
| Item | Owner | Blocker |
|------|-------|---------|
| <item> | <seat> | <reason or "—"> |

## Next seat should
1. <concrete action 1>
2. <concrete action 2>
3. <concrete action 3>

## Read first
- <path or doc the next seat needs to orient>

## Blockers
<detail sufficient to unblock without re-investigation, or "none">

[CLOSURE] tier=INTUITED | branch=<current-branch>
```

---

## Sovereignty-with-mutuality framing

Authority: `COLLABORATION-MODEL__sovereignty-with-mutuality__2026-07-03.md`.

The baton is the sequencing mechanism between sovereign seats. Each seat:
- Works in its own worktree (bounded blast radius — no shared mutable state).
- **Reads** the previous baton; does not co-edit the same file.
- Drops its outputs to the **shared surface** (Vellum + shared path) before closing.
- Does not assume the next seat shares its context — write the baton for a cold start.

This is not joint work. It is sovereign agents contributing to a shared pool with the whole goal in mind.

---

## Identity / attribution

- Post under the correct seat slug: `cursor` / `antigravity` / `devin` / `cascade` / `scribe`.
- All AI-authored Vellum entries: `epistemic_tier: INTUITED`.
- A tool or relay name (e.g. `codex-mcp`) is NOT an identity. Never prefix it onto your slug.
- Full roster: `~/Code/FLEET-ROSTER.md`.

---

## Finish-waypoint alignment

Before calling any seat done, cross-check finish-waypoint.mdc:

- [ ] Baton in shared path (not worktree-only)
- [ ] Vellum `preform-seat-pass` filled and posted
- [ ] `05-pass.md` updated
- [ ] If F8 publish: constitutional pass + GitHub pushed + Vellum telemetry row

---

## Self-rewrite after every use

After each handoff:

1. **Run the rubric** — was `next_seat_should` concrete and actionable (3–5 bullets)? Were blockers actionable? Did the baton land on a shared path? Was Vellum witnessed? All four = clean pass; note any failures.
2. **Log in CHANGELOG** — one row per handoff, even if clean ("no defects found"). Date + seat + one-line note.
3. **Rewrite ADDITIVELY** — append lessons as new sections or append to existing. Never remove or paraphrase existing guidance. Version-bump the metadata.
4. **Mirror to repo SSOT** — `perplexity-inbox/.cursor/skills/baton-pass/SKILL.md`. If that path does not exist, create it.
5. **Constitutional rule** — self-rewrite is additive only. Do not regenerate this skill from memory, do not summarize existing guidance into shorter form, do not drop sections. Adding is always safe; removing is never safe.

---

## Authorities consolidated (references, not forks)

| Source | What this skill draws from it |
|--------|-------------------------------|
| `~/.cursor/rules/relay-stop.mdc` | Stop triggers, PASS protocol order, baton content requirements |
| `~/.cursor/rules/finish-waypoint.mdc` | Done ladder, shared-path gate, F8 checklist |
| `~/.cursor/rules/vellum-witness.mdc` | When/what to fill in preform-seat-pass; [ENGINEER-WRITE] vs [AUTO] fields; identity; topology guard |
| `perplexity-inbox/harness/baton_lifecycle.py` | write/read/rotate commands; active→archive→datalake bronze lifecycle; frontmatter schema |
| `AGENTS.md` seat-pass section | Seat slug list, INTUITED tier for AI rows |
| `COLLABORATION-MODEL__sovereignty-with-mutuality__2026-07-03.md` | Baton = sequencing between sovereign seats via shared surface, not co-editing |
