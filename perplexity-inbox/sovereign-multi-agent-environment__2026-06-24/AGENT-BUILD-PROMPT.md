# Build Prompt — Sovereign Multi-Agent Mac Environment

Build this on a freshly-wiped Mac mini (macOS Tahoe 26, 24 GB RAM). The remote host is **Amplified Partners Infrastructure 1** (128 GB; runs Cove Temple, the core, inference) — referred to here as Infrastructure 1. Build exactly to this spec. Open pull requests; do not write to the main branch. Do not redesign the spec. If something here conflicts with the machine, stop and report it.

## Purpose
A secure environment where four agents work in isolation, with appropriate data access and data sharing.

## Topology
- **Mini** — four isolated agent cells (thin workers).
- **Infrastructure 1** (prior: Beast) — Cove Temple, the core (ledger/db/knowledge), shared inference, the only standing cloud.
- **M5** — command and search terminal (the human's surface).
- **Tailscale** is the front door to each machine (host-level node per machine). It is the secure network in. It is NOT run per-cell.

## Cells (the environment software)
- Use **Apple Container** (VM-per-container, real isolation). Create 4 equal cells, ~5 GB RAM each, identical spec.
- **Cells are sealed. No cell connects to another cell.** Agents share only through the pool and the lake, never by direct cell-to-cell link. There is no per-cell Tailscale.
- Schedule a nightly `container machine stop/start` recycle per cell to reclaim memory (AVF does not return freed memory to the host).
- **No GPU in cells.** Inference runs on the host (Ollama) or Infrastructure 1, reached over HTTP, shared by all cells.

## Isolation rules (do not create these holes)
- **MCP servers run as `stdio` inside each cell**, or bound to `127.0.0.1`. Never host-shared on the bridge IP — that is a cross-cell channel and is forbidden.
- No bind-mounting host paths into a cell beyond the agent's own declared workspace.
- No SSH-agent forwarding into cells.
- Tailscale ACLs scoped so one cell cannot reach what another cell can.

## Network (front door)
- Install **Tailscale as a LaunchDaemon** on the mini (and it is already on M5 and Infrastructure 1). Persistent, survives reboot. Disable key expiry on these nodes.
- `sudo pmset -a sleep 0 disablesleep 1` — the worker box must not sleep and drop the mesh.
- Test: reboot the mini, confirm automatic reconnection with no manual step.

## Deterministic foundation (the floor)
Everything in the foundation is deterministic code — same input gives same output, idempotent, no language model in the loop. Language models operate only inside cells. This is the dominant production pattern (deterministic control plane = 0% policy violations vs 26.7% for prompt-based governance, Zylos 2026).
- **Provisioning:** build the host from a file (Nix-darwin / Ansible + Brewfile + dotfiles) so wipe-and-rerun produces an identical machine.
- **Orchestration:** Temporal (already in use). Workflow code MUST be deterministic; LLM calls go only in Activities. Idempotency keys derived from (workflow_id, activity_name) by the orchestrator, never by the LLM.
- **Policy / authorization:** policy-as-code, evaluated outside the LLM. OPA for infrastructure-layer RBAC/ABAC (1-5ms); Cedar (formally verified, Rust) for tool-layer agent enforcement at the gateway boundary.
- **Access broker (door opens on job ticket):** JIT credential broker (Vault pattern). Ticket shown -> scoped token minted, short TTL -> auto-expires when the job completes. Zero standing privilege.
- **Janitor:** Hazel (see below).
- **Scheduler / watch jobs:** launchd (see below).
- **Data neutralising:** deterministic NER (Presidio/spaCy) + HMAC-SHA256 tokenisation for cross-document-consistent de-labelling; provenance via (input_hash, transform_id, output_hash) so the transform is verifiable and diffable against the lake.

## Automation layer
- **Hazel** — file hygiene/janitor (visible, licensed). Rules pass the matched file path (`$1`) to shell scripts; set `PATH` explicitly in every script (Hazel does not inherit it). Toggle rules off rather than delete to audit.
- **launchd (LaunchDaemon, dedicated no-login service user)** — all scheduled and watch-folder jobs. Headless, runs as a service account via the `UserName` key, sets PATH via `EnvironmentVariables`. This is the deterministic floor and it bypasses Tahoe TCC permission traps.
- **Shortcuts is NOT used for headless automation** — `shortcuts run` requires a logged-in GUI session and will not run from a LaunchDaemon. Use shell scripts for any headless step. Shortcuts may be used only as optional human-side glue on a logged-in machine.

## Janitor (Hazel) detail
- Watch each cell. Allowlist model: anything not on the KEEP list is swept.
- Hard-code agent-native paths as never-swept: `~/.claude/`, `~/.cursor/`, `~/.config/devin/`, `~/.gemini/` and each agent's memory/knowledge/skills dirs. Their learning persists — this enables compound engineering.
- Sweep is move-not-delete: copy → SHA-256 verify → unlink. Hazel shells out to a script that does the verify and writes a tombstone manifest (original path, lake path, hash, timestamp, agent).
- A thin LaunchDaemon handles the container recycle (Hazel cannot).

## Data paths (neutralise everything — standard practice, the PUDDING technique)
- **Path 1 — verbatim to the data lake:** exact, unaltered, attributed. Bronze layer, date-partitioned. Gold layer is a DuckDB query surface.
- **Path 2 — to the shared pool:** a deterministic Python step neutralises EVERYTHING (front matter and body). Remove all labels; keep the logic and information and all provenance facts (attribution, tier, dates, IDs). Words made neutral — non-pejorative, no softer or harder, meaning unchanged. Strip charge, never strip fact. Subtractive only — never paraphrase or alter meaning. Mark each output as cleaned and link it back to its verbatim lake source. Must be diffable against the lake copy.
- The pool is identity-blind by design (idea meritocracy). Attribution always survives in the lake.

## Compound engineering
- Preserve each agent's memory/knowledge/skills (the never-sweep list) so each agent's work makes its next task easier.
- The shared neutralised pool lets a lesson one agent learns compound for all — cross-agent compounding.
- Pre-create rule/skill dirs (`.claude/rules/`, `.cursor/rules/`, `.agents/skills/`, `.devin/`) and an `AGENTS.md` at project roots (the cross-tool fallback all four read).

## Telemetry
- **Langfuse** — observability, cost, latency, per-agent attribution. Wire LiteLLM `success_callback`/`failure_callback` to Langfuse (use the service name, not localhost, in Docker; set the three env vars). Currently not wired — fix it.
- **Opik** — LLM tracing/evaluation (output quality). Deploy/confirm the container.
- **Vellum** — the immutable attributed ledger (who did what). Underneath both.

## IDEs (install + run model)
- **Claude Code** — runs headless in-cell.
- **Antigravity (`agy`)** — runs headless in-cell.
- **Devin CLI** — runs headless in-cell.
- **Cursor** — GUI app on the Mac host → Remote-SSH into its own cell (it cannot run inside the cell).
- Each agent: own sandbox repo, read on production, write to production only via PR.
- **GitKraken** (host GUI — visual branch/PR across all four repos) and **GitLens** (in Cursor/VS Code-protocol editors).

## GitHub configuration
- No agent writes to main. PR-only. No agent approves another agent's PR.
- `/.github/workflows/` CODEOWNER → `@ewan-dot` (agents must not own their own gate).
- Neutralise auto-merge: every PR requires a human approval before merge.
- `enforce_admins: true`, `require_last_push_approval: true`, `required_signatures: true`.
- Default `* @ewan-dot` CODEOWNERS on all repos.
- **Multi-agent collision prevention:** use git worktree isolation so agents don't contend on `.git/index.lock` or overwrite each other.

## Cloud (sovereign overflow only)
- **GCP raw Compute Engine** as a burst/overflow GPU valve — only when home compute is overloaded.
- Use it as PURE rented compute: your own stack, any model (ADK is model-agnostic, sits on LiteLLM). Never use Vertex managed inference or Gemini API for sensitive work.
- **Only neutralised/anonymized data (Path 2) may go to cloud.** Verbatim, core, lake, secrets never leave home. Connect via Tailscale subnet routing; CMEK for encryption.

## Pre-install manifest (for ease — zero setup friction in-cell)
- Foundation: Homebrew, Nix-darwin/Ansible, Tailscale, Apple Container, Hazel, 1Password CLI (`op`), Infisical CLI, git, gh.
- Runtimes (host, shared): Python (uv), Node, Rust, Ollama, DuckDB, Postgres client.
- IDEs/CLIs: Claude Code, Cursor (+GitLens), Antigravity `agy`, Devin CLI, GitKraken.
- Telemetry: LiteLLM, Langfuse, Opik (wired to Vellum).
- Secrets: `.env.example` (key names only) in repos; values injected at runtime via Infisical (Infrastructure 1) + 1Password. No secret values in repos, lake, or cells.

## Deliverables (as PRs for human review)
1. Idempotent provisioning script (host built from a file).
2. Tailscale persistence config + reboot test result.
3. Four Apple Container cells, equal spec, sealed, no inter-cell links.
4. Hazel rule set + verify/tombstone script + LaunchDaemon recycle job.
5. Two-path data pipeline: verbatim-to-lake + deterministic neutralise step with cleaned stamp, diffable against lake.
6. GitHub configuration changes above + git worktree setup.
7. Host inference proxy (Ollama) for shared use.
8. Telemetry wired: LiteLLM→Langfuse, Opik deployed, Vellum ledger.
9. (Optional, when needed) GCP overflow connector via Tailscale, anonymized data only.
