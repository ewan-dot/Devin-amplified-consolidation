---
title: "VSCodium Build + Open-Door Harness — Thread Artifacts & Conclusions"
document_type: "agent_doc"
artifact_id: "vscodium-build-and-open-door-harness__implementation-brief__v01__2026-06-24"
date_utc: "2026-06-24T19:05:00Z"
project: "Amplified Partners"
author: "Perplexity Computer"
stage: "decision"
objective: "Hand the M5 watchers the artifacts + conclusions from the VSCodium/DeerFlow/open-door-harness thread. Artifacts and conclusions only — not a transcript."
reader: "agent"
proxy_signature:
  signer: "AI_PARTNER_PROXY"
  reason: "Tier B inbox write (standing-grants): drafting an executable artifact into the Mac handoff folder. Logged as proxy; Ewan's ratification supersedes."
  timestamp_utc: "2026-06-24T19:05:00Z"
attribution: "Genuine human+AI partnership (~70%+ AI by Ewan's measure). Direction/rods/math instinct = Ewan; majority of build = AI partners. This brief = Perplexity Computer."
epistemic_tier: "STRUCTURED"
contradiction_status: "clean"
machine_action_allowed: "recommend"
system_of_record: "Mac perplexity-inbox (handoff); never the Beast directly"
ratifier: "Ewan"
outcome_routing:
  outcome_class: "production_candidate"
  outcome_reason: "Build-now decision is ready; harness/trial are ratifiable designs. Implementation happens on M5 past the inbox."
  research_needed: false
---

# VSCodium Build + Open-Door Harness — Artifacts & Conclusions

TIER: STRUCTURED · PROVENANCE: this thread (2026-06-22 → 06-24) + live Beast/inbox reads · STATUS: ready for M5 implementation
PROXY: AI_PARTNER_PROXY — Tier B inbox write, logged per standing-grants.

## The immediate ask (this turn): build VSCodium now, GitLens-best

- **Decision: build VSCodium now.** From-source build is viable on macOS (deps: node per `.nvmrc`, jq, git, python3.11, rustup — [VSCodium howto-build](https://github.com/VSCodium/vscodium/blob/master/docs/howto-build.md)). Self-build = full sovereignty (you compile the telemetry-free binary, no trust in a prebuilt cask). `brew install --cask vscodium` remains the fast path if a built binary isn't needed.
- **GitLens:** the `.augment/skills` dir in gitkraken/vscode-gitlens is empty on GitHub — nothing to lift there. Install GitLens from Open VSX into the built VSCodium.
- **Inbox impact check (done):** the inbox thread #8 "VSCodium agent lane" and `AMPLIFIED-IDE__architecture-plan` (both 2026-06-24) are the build-relevant updates. Their open Tier C gates that touch the build: **Devin REST v3 entitlement, spillover trigger, destination repo** (agent-lane). Resolve those before wiring the agent lane; they do NOT block building the editor itself.
- **Bootstrap scripts** already produced this thread (`vscodium-bootstrap/`): `bootstrap.sh` (idempotent install + RAM/path/cloud checks), `amp-worktree.sh` (bare+worktree+baton helper). Reuse for the build host.

## Conclusions carried from this thread

1. **Open-door harness — "blinkers without ceilings."** Agent chooses freely what to work on; a doorkeeper enforces ONE writable system at a time; opening a door closes the last. No standing write access; never the docker socket. Three enforcement layers: Layer 2 = container boundary (ro mounts, SELECT-only DB role, network detached) — the universal wall; Layer 1 = in-process guardrail customized per container (DeerFlow's `GuardrailProvider` is the template); Layer 0 = per-worktree hook/door binding.
2. **Vellum IS the substrate.** The harness wires onto primitives that already ship (fleet-vellum v0.2.0, 362 tests, `vellum:8400`): the one-door lease = Vellum Baton; write-authority = RodGuard + circuit breaker; hooks = witness sheet entries; telemetry = the new sensors feeding the weak-signal engine (pairs with Langfuse: model-plane vs authority-plane). Resolves the "new infra actor" contradiction — the harness is the existing write-authority pipe applied to doors.
3. **DeerFlow = first tenant, Beast-hosted, hardened.** Driven from M5 by Claude Code over the claude-to-deerflow bridge. Wired to existing LiteLLM (never holds a real provider key) + Langfuse. Red line: never mount docker socket / never load DooD overlay; never use the AIO Beijing-registry image; IM channels + InfoQuest off. LocalSandboxProvider's bash is the soft spot — deny bash or move to K8s provisioner beyond a trial.
4. **Editor split:** Claude Code → VSCodium (both Mac mini + M5). Antigravity → VSCodium but offloaded to its Google Cloud account (RAM). Cursor + Devin keep their own UIs. Isolation via Apple Containers, single user account (no per-agent macOS users).
5. **Worktrees:** hybrid provisioning (pre-provision+lock for known tasks, native isolation for children); per-host clones synced via GitHub, never NFS; `gh --repo` explicit; the 7 standardizations.
6. **Attribution correction (important):** Amplified is ~70%+ AI partnership, not mostly Ewan's. "Long stumble," not stumbled-upon and not a pristine master-plan. Committed to memory for all future instances.

## Companion artifacts (in deerflow-trial/ on the Mac + this workspace)

- `open-door-harness__architecture-spec__agent-doc__v02` (with Vellum + 3-layer + per-worktree sections)
- `deerflow-beast-trial__deployment-brief__agent-doc__v01`
- `vscodium__setup-options__agent-doc__v01`
- `github-worktrees__setup-options__agent-doc__v01`
- `amplified-seven-month-arc__github-report__agent-doc__v02` (corrected attribution)
- `vscodium-bootstrap/` (bootstrap.sh, amp-worktree.sh, README.md)
- research/: deerflow-security, vscodium, github-worktrees full reports

## [CLOSURE]
- actioned: build-now decision made; inbox impact checked; artifacts consolidated.
- gates (Tier C, for the agent lane only — not the editor build): Devin REST v3 entitlement; spillover trigger; destination repo.
- next (M5): build VSCodium from source per howto-build; install GitLens from Open VSX; then resolve agent-lane gates before wiring the lane.
