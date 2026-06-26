# Cursor harness manifest

Lean fleet harness at `~/.cursor/`. Hooks prevent waste; rules inject policy. SSOT for Cursor seat.

## Stays

**alwaysApply rules:** lean-output, ewan-core, constitutional-gate, comms-ping, session-discipline, token-efficiency, worktree-door, finish-waypoint.

**Hooks (`hooks.json`):** sessionStart (preamble + Vellum/fleet sensor), sessionEnd, beforeSubmitPrompt (P0 secrets + constitutional P0/nudge), beforeShellExecution (token-bomb nudge), beforeReadFile (nudge), postToolUse (truncate), stop, preCompact, subagentStop.

**On demand:** vellum-witness, relay-stop, amplified-search, facilitator-interface, yolo-ceilings, etc.

## Push door

**Philosophy:** push-door permission — if the agent asks itself for permission, it gets it. Opens pathways; freedom not constraint.

- Hooks **fail-open** unless P0 (secrets/PII in prompt).
- Agent self-request through the worktree door = **granted**; ask in seat, pathway opens.
- Harness prevents **waste**, not curiosity — nudge before deny; no pre-emptive blocking.
- Hard block: obvious secret patterns (always); constitutional P0 in `client_live` via `before-submit-constitutional.py`.
- Staged constitutional mode: `CONSTITUTIONAL_HARNESS_MODE=pre_client` (default) | `client_live`.

## Removed / not here

Plugin cache, project-level duplicate rules (repo pointers only), empty unregistered hook stubs.
