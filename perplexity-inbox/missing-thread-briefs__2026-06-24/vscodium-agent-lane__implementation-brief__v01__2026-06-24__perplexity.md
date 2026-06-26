# VSCodium Agent Lane — Implementation Brief

TIER: STRUCTURED
PROVENANCE: sessions `41ab7b59` (Jun 17-18, 33t — VSCodium guide), `94681082` (Jun 22, 22t — VSCodium Mac bootstrap), `022ae58e` (Jun 23, 6t — VSCodium/Claude harness across M5/Beast/Vellum)
STATUS: designed across three threads, not landed as inbox artifact, not in enforcement plan
FOR: M5 watcher

## What exists

The decision and direction across three threads:

- **VSCodium, not VS Code** — explicit (`022ae58e`: "its vs codium"). De-Microsoft-telemetry build of the same editor.
- **Multi-surface harness:** Intent Interface is the only user door; Vellum is the bus; M5 polls Vellum; Beast handles heavy/local/DeerFlow seams; Claude/Cursor/Devin/Antigravity routed as peers by evidence.
- **Subscription-first**, no token harvesting/proxying from consumer plans. Beast Anthropic API key is the sanctioned metered spillover path.
- **Cursor's agent = default for settled-plan execution.**
- **Antigravity = Google's IDE** (not a wrapper — corrected in session).
- **Devin REST v3** may be Teams/Enterprise-gated; entitlement verification needed.
- **DeerFlow = ByteDance harness experiment** on Beast, not v1 foundation.
- **VSCodium + Vellum + Opik + Langfuse + GitKraken + GitLens** all named together as the lane's instrumentation.

## What was done

- Multi-surface build brief drafted; spillover paths defined; peer-routing-by-evidence rule stated.
- Mac mini RAM corrected mid-thread (2GB→24GB → confirmed elsewhere as the M5 figure, not the mini; mini still pending).
- Confirmed Beast Anthropic API key is the metered spillover lane.

## What it means

- **The enforcement plan covers Claude Code + Cursor lanes. VSCodium is a third lane it does not cover.**
- The enforcement principle (enforce close to credential → proxy) still holds: VSCodium routes through the same `estate-token-router` (the welded LiteLLM from mesh-plan S2). No new credential surface needed.
- **VSCodium-specific knobs** need their own row in the lean-output deployment table (`lean-output-deployment__estate-guide`) — currently absent.
- **Intent Interface as the only user door** is consistent with the Cockpit/Electron decision in session `80962bca`.

## What to change next

1. **Add a VSCodium row to `lean-output-deployment__estate-guide`** — `.vscode/settings.json` or equivalent slot for the lean rule.
2. **Add a VSCodium block to the enforcement plan** — Claude inside VSCodium uses the same managed-settings + hooks as the Claude Code lane; document the install path.
3. **Verify Devin REST v3 entitlement** before relying on the Devin peer-route.
4. **Wire VSCodium → estate-token-router** via `ANTHROPIC_BASE_URL` (already the rule for every IDE in the estate-spec).
5. **Decide spillover trigger** (credit exhaustion threshold) and **destination repo** for the spillover lane. (Both still open in `022ae58e`.)

## Not yet verified

- Current VSCodium release stability for headless agent use.
- Whether Cursor's agent has been measured against Claude Code on the same task class.
- Devin REST v3 plan tier requirement.

[CLOSURE] branch=PLAN | proxy=1 logged | gates=Devin REST v3 entitlement (Ewan-check) + spillover trigger threshold + spillover destination repo (3 questions, collapse to one hand-back) | inbox=vscodium-agent-lane__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
