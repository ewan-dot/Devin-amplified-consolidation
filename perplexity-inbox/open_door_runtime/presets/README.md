# Door presets — Cursor-native enforcement surfaces (STAGED)

**A door is a preset of Cursor's own enforced surfaces, not a wall re-coded in shell.**
(Research `RESEARCH__cursor-heavyuser-harness-guidance__v01` R3.) Each door directory holds a
pair:

- `permissions.json` — `terminalAllowlist` (prefixes that auto-run) + `autoRun` steering.
  **There is no `terminalDenylist`** in Cursor's schema; "deny" intent is expressed as
  `autoRun.block_instructions` (soft steer) **plus** the fail-closed hook hard-deny. Only active
  when a Run Mode is enabled; **not a security boundary**. (cursor.com/docs/reference/permissions)
- `sandbox.json` — macOS Seatbelt: `type`, `additionalReadwritePaths`, `additionalReadonlyPaths`,
  `networkPolicy`. **This is the STRUCTURED wall** (write scope + network). (cursor.com/docs/reference/sandbox)

## "Door enter" = swap these two files in

The door-enter step (a `door` CLI / marker write, Phase-1 presentation layer) copies the active
door's pair into the live config, after substituting placeholders:

```
cp presets/<door>/permissions.json  ~/.cursor/permissions.json
cp presets/<door>/sandbox.json      ~/.cursor/sandbox.json     # placeholders substituted first
# writes ~/.amplified/active-door.json {door, entered, task, seat, <bindings>}
```

Exit + re-enter another door = swap a different pair in. Doors never union (SSOT §2).
**Nothing in this directory is copied by Phase 1** — see `../ACTIVATION.md`.

## Placeholder binding contract

Placeholder tokens in `additionalReadwrite/ReadonlyPaths` are bound at enter-time from the
active-door marker; **unbound placeholders MUST be dropped** (never left literal — an invalid path):

| Token | Marker key | Door(s) |
|---|---|---|
| `__PROJECT_SUBTREE__` | `project_subtree` | agentsmini_build |
| `__WORKTREE_SUBTREE__` | `worktree_subtree` | worktree_feature |
| `__PIPE_RUN_DIR__` | `pipe_run_dir` | pipe_run |
| `__CORPUS_DIR__` | `corpus_dir` | pipe_run |

If the workspace root already *is* the project/worktree, no extra path is needed (the sandbox is
workspace-scoped by default) and the placeholder is simply dropped.

## net_mesh → `networkPolicy` mapping (SSOT §2 Net/Mesh)

Sandbox `networkPolicy` governs **sandboxed shell egress**. Broad web *search/fetch* is a Cursor
tool governed by Run Mode, not `sandbox.json`. `default:deny` + explicit allow is used everywhere
except where open web egress is the door's job.

| net_mesh | networkPolicy | Rationale |
|---|---|---|
| `none` | `{default:deny, allow:[]}` | build/config/worktree doors need no egress |
| `web+searxng` | `{default:deny, allow:["search.beast.amplifiedpartners.ai"]}` | SearXNG host for shell; open-web reading rides the WebSearch/Fetch tool |
| `tailnet` | `{default:deny, allow:["vellum.beast.amplifiedpartners.ai","beast-amplified.tail27a0cc.ts.net","100.64.0.0/10"]}` | Vellum public DNS + tailnet (see SSRF note) |
| `beast-read` | `{default:deny, allow:["*.beast.amplifiedpartners.ai","beast-amplified.tail27a0cc.ts.net","100.64.0.0/10"]}` | Beast read APIs |
| `web+searxng+beast-read` (pipe_run) | union of the above (searxng + beast + tailnet) | pipe fan-out + Brain reads |

**Honest SSRF caveat:** Cursor blocks RFC1918 + cloud-metadata by default to prevent SSRF; the
Tailscale range is CGNAT `100.64.0.0/10`. If Cursor's hardcoded SSRF guard refuses the tailnet
CIDR, estate reach falls back to the **public** Vellum/Beast DNS (`*.beast.amplifiedpartners.ai`),
which is reachable — so `tailnet`/`beast-read` degrade gracefully, not to a hard stop.

## Per-door summary

| Door | `type` | net_mesh | git-write | Notable |
|---|---|---|---|---|
| research_read | `workspace_readonly` | web+searxng | none | broad readonly estate paths; no write scope at all |
| agentsmini_build | `workspace_readwrite` | none | commit-local | one bound project subtree writable |
| central_handoff | `workspace_readwrite` | tailnet | commit-local | **write-boundary: `~/amplified-pipeline` + `perplexity-inbox` in `additionalReadwritePaths`** (else External-File Protection blocks) |
| worktree_feature | `workspace_readwrite` | none | commit-local | one bound worktree subtree; prefer native `/worktree` (R4) |
| pipe_run | `workspace_readwrite` | web+searxng+beast-read | commit-local | pipe run-dir + amplified-pipeline writable |
| config_harness | `workspace_readwrite` | none | commit-local | `~/.cursor/hooks/` writable; `hooks.json`/`*.json` sandbox-protected (prompts); rule `.mdc` needs architect bless |

## What the sandbox always protects (unweakenable, every door)

`~/.cursor/*.json` (incl. `hooks.json`), `.git/config`, `.git/hooks/**`, `.cursorignore`,
`.vscode/**`. Writable `.cursor` subdirs: `rules/ commands/ worktrees/ skills/ agents/`. Secrets are
additionally hidden by `_base/cursorignore`. File deletes and out-of-workspace writes are gated by
the native File-Deletion / External-File Protections.

Contents (globs, allowlists) are **first-pass INTUITED**, to be calibrated from Phase-2 nudge
telemetry before any flip to hard behaviour.
