# Perplexity-Inbox — Mesh Plan (cohesion audit + one-page wiring)

TIER: STRUCTURED · cohesion claims based on a verbatim read of every file in the inbox as of 2026-06-24T12:00; estate facts verified against `beast-state-correction-live-verified__2026-06-24T1135` (live docker_ps, 84 containers).
PROVENANCE: read of all 18 files under `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/` (README, harness, rules, 3 impl briefs, 4 threads of supporting docs, 5 research dossiers, 1 Vellum JSONL draft).
GOAL-LINK: not a plan to *get the threads done* — a plan to make sure they don't fight each other when M5 implements them. Hardening the inbox, not the world.
FOR: MacAirM5 watchers + Ewan. Read this first; it points at the others.

---

## TL;DR

The inbox is in good shape. Five independently-strong threads sit under one shared spine (pipe + min-rule + proxy log + inbox-as-endpoint + closure footer). Cohesion is high. The risks are seams, not contradictions:

1. **Naming drift** — Beast vs "Infrastructure 1" — could split references.
2. **Two routers in the same lane** — `estate-cost-tools` (Anthropic proxy) and `estate-token-router` (LiteLLM) must be **one LiteLLM instance with shared callbacks**, not parallel stacks.
3. **Enforcement files vs sealed cells** — managed-settings/hooks must live INSIDE each cell, deployed by provisioning, not pushed from the host.
4. **`amplified_rules.json` must be the single classifier** — every M5 AI reads it; no AI-private gate logic.
5. **Three "compounding" surfaces (pool, Vellum, PUDDING) are three views of one pipe**, not three pipes.

Six small fixes lock those seams. None are blockers; all are pre-implementation hygiene.

---

## What's in the inbox (the five threads)

| Thread | Owns | Files | Maturity |
|---|---|---|---|
| **A. Doctrine harness** | Machine-readable projection of the constitution + ladder + closure | `amplified_rules.json`, `amplified_harness.py`, `README.md` | Live, self-tested |
| **B. Token-efficiency programme** | Cut recurring AI spend across the estate; prove the cut | 12 docs in `token-efficiency-programme__2026-06-24/` + 1 impl brief at root + 5 raw dossiers | ~60% proxy built; router unbuilt; proof gate defined |
| **C. Sovereign multi-agent environment** | Mac-mini build for 4 sealed agent cells + deterministic foundation | `sovereign-multi-agent-environment__2026-06-24/MASTER-SYNTHESIS.md` + `AGENT-BUILD-PROMPT.md` | Architecture decided; one-unit-first rule named |
| **D. UI-methods research pipe** | Recover logic+methodology of 9 human-side UI methods → PUDDING feedstock | `ui-methods-research-pipe/orchestrator-and-subagents.md` + 1 impl brief at root | Run-ready; sealed (no token-eff coupling) |
| **E. Beast-state correction** | Refresh `/opt/amplified/BEAST-STATE.md` to match the running estate | `beast-state-correction-live-verified__2026-06-24T1135__perplexity.md` | Live-verified; pipe-routed change |

**Shared spine across all five:** pipe discipline (Python + Rust + Vellum + AI + Human), inbox as endpoint, `AI_PARTNER_PROXY` logged signer, min-rule tiering with provenance, `[CLOSURE]` footer on task-turns.

---

## Cohesion verdict

**Strong agreement on:**

- The estate model — M5 = judgment seat, Mac mini = local execution, Beast/Infra-1 = ledger+batch+router host, M4 = reserve. Asserted in token-eff master plan, sovereign-synthesis, and verified by `beast-state-correction` against live `docker_ps`.
- The "done = proven, not pushed" rule (token-eff §9 PROOF-OF-LIFE), the "one unit first, then earn the next" rule (sovereign-synthesis Part 4), and the closure footer (harness).
- The two real Tier-C gates (Mac mini RAM, manual skill deletions in Perplexity) — single-sourced consistently across master plan, impl brief, estate-spec §10, and the Vellum JSONL.
- The two open verification flags (Anthropic Pool 1/Pool 2 status; "62% re-sent context") — flagged identically in master plan, impl brief, prior-art research, and Vellum JSONL.
- Identical interpretation of the precedence order between the prose skills and `amplified_rules.json` (GOAL > WIN_WIN > MIN_RULE > PIPE > CLOSURE > LEAN).

**No contradictions to resolve.** Disagreements are absent; what follows is **seam hardening**, not arbitration.

---

## The seams (six fixes)

### S1 — Pick one name for the big machine. Stop carrying both.

- **Sovereign synthesis** renames Beast → "Amplified Partners Infrastructure 1".
- **Token-eff master plan, estate-spec, impl brief, beast-state-correction, harness rules** all still say "Beast" / `/opt/amplified/BEAST-STATE.md`.

Either is fine; both is not. Per the live system (`/opt/amplified/...`, `vellum`, `amplified-net`, `beast-control-mcp` container), **Beast remains the system-of-record name**. "Infrastructure 1" reads as a human-facing relabel for outside use.

- **Fix:** keep `Beast` in code, paths, container names, doc filenames, Vellum events. Use "Infrastructure 1" only in external/investor framing. State this once in the BEAST-STATE.md refresh so the sovereign synthesis stops drifting.

### S2 — One LiteLLM, not two routers.

The token-eff spec describes:
- `estate-cost-tools` proxy: Anthropic-specific, prompt caching + compaction + Sonnet→Haiku routing + cost log + budget cap. ~60% built.
- `estate-token-router`: LiteLLM-based, deterministic, credit-first, multi-provider. Unbuilt.

The sovereign synthesis adds: LiteLLM + Langfuse callbacks + Opik tracing + Vellum ledger.

If these become two LiteLLM-shaped things they'll fight (which one holds the API keys? which one writes to Vellum?). Per the enforcement plan's own principle — **enforce as close to the credential as possible** — there must be exactly one credential-holder.

- **Fix:** `estate-token-router` IS the LiteLLM proxy on the Beast. It holds the keys. `estate-cost-tools` provides the Anthropic-specific logic (caching/compaction/Haiku routing) as middleware modules behind the router, not as a separate process. Langfuse callbacks + Vellum cost-log writes live on the router's `success_callback`/`failure_callback`. Spec §9 proof run targets this one process.

### S3 — Enforcement files live inside cells, not on the host.

The enforcement plan installs:
- `managed-settings.json` (highest precedence; user can't override) — Claude Code.
- `PreToolUse`, `UserPromptSubmit`, `Stop` hooks — Claude Code.
- `.cursor/rules/lean-output.mdc`, `.cursorignore` — Cursor.
- Launcher harness script.

The sovereign build puts each IDE inside a sealed Apple Container cell. Pushing those files from the host into the cell would punch through the seal. Per the build prompt's own "no bind-mounting host paths beyond the agent's declared workspace" rule, this would be a hole.

- **Fix:** enforcement files ship as part of each cell's **provisioning artifact** (the idempotent build script). They land at provisioning time, are owned by the cell, and survive recycle because they live in the cell's own sandbox repo. Host pushes nothing into a running cell.

### S4 — `amplified_rules.json` is the only gate-classifier.

The harness defines `classify(action)` → A/B/C. If Perplexity uses the harness but the M5 watcher rolls its own permission logic (or vice versa), you get split decisions on identical actions.

- **Fix:** every AI on the estate that takes an action reads `amplified_rules.json` (or imports `amplified_harness.classify`). Add this as a `BEAST-STATE.md` invariant alongside "nothing enters the Beast except through the pipe". The rules JSON is doctrine projected to code — it has the same authority as the prose skills, capped at the prose skills' tier (STRUCTURED).

### S5 — Three "compounding" surfaces are one pipe with three views.

- **Sovereign synthesis** describes a "shared neutralised pool" (Path 2: Presidio/spaCy + HMAC-SHA256, identity-blind, diffable against lake).
- **Token-eff** describes Vellum cost-log events (Effective-Tokens, per-job, hash-chained).
- **UI-methods** describes PUDDING extraction onto returned mechanisms.

These look like three pipes; they are one pipe seen at three stages:

```
verbatim capture  → Path 1: lake (attributed, immutable, bronze→gold)
                  → Path 2: neutralised pool (identity-blind, idea-meritocracy)
                  → PUDDING: mechanism extraction (the structuring step)
                  → Vellum: append-only ledger of events with hash-chain attribution
```

- **Fix:** state the equivalence once in `BEAST-STATE.md` and in the sovereign-build's "Data paths" section. Pool ≠ ledger ≠ extractor — but they share neutralisation, attribution discipline, and the pipe. No second neutraliser, no second ledger, no second extractor.

### S6 — Local-lane proof must run from inside a cell, not on the mini's host.

Token-eff §9.6 says "a job runs on the Mac mini at $0 tokens with correct flags." Sovereign-build says cells are sealed, no GPU in cells, inference via host Ollama over HTTP, scoped Tailscale ACLs.

If the §9.6 proof runs from the mini's host shell, you've proven the wrong thing — that the host can hit the host. The honest proof: agent code inside a sealed cell calls host Ollama at the bridge IP and gets work done at $0 tokens.

- **Fix:** §9.6 proof line reads "a job runs on the Mac mini at $0 tokens, **initiated from inside a sealed cell**, calling host Ollama over HTTP, with `--bare --exclude-dynamic-system-prompt-sections` set." This proves both the local-lane economics AND the cell seal at once.

---

## Implementation order (the mesh)

This is the order that keeps the threads from fighting. It is NOT a re-derivation of token-eff's master plan order — it is the order in which the threads' shared seams get welded.

| # | Step | Owns the seam | Unblocks |
|---|---|---|---|
| 1 | Apply S1 + S4 + S5 inside `beast-state-correction` (one PR through the pipe) | Names, classifier, pipe-equivalence | Everything downstream reads the same names + same gate logic |
| 2 | Reconcile `estate-cost-tools` + `estate-token-router` into one LiteLLM (S2) — design note before any new code | Routing | Token-eff §9 proof run; Langfuse + Vellum callbacks have one home |
| 3 | Pin enforcement files as cell-provisioning artifacts (S3) | Isolation | Sovereign build can run cells without host bind-holes; enforcement plan is durable per cell |
| 4 | Settle the Mac mini RAM number (Tier C — Ewan-gated) | Local-lane sizing | Token-eff B3/C3/§9.6 + sovereign cell sizing |
| 5 | Run the token-eff implementation order (master plan §1–7) over the welded base | Token-eff programme | The §9 PROOF-OF-LIFE gate, captured in `PROOF-OF-LIFE.md` |
| 6 | Dispatch the UI-methods pipe (D) in parallel — it is sealed, no coupling, runs independently | UI-methods deliverable | PUDDING-onto-wireframes downstream |
| 7 | Verify the two open figures (Anthropic Pool status; 62% re-sent context) before §9 captures any "before/after" external citation | Honesty | Spec §9.9 measurement integrity |

Steps 1–4 are **pre-implementation hygiene**. Steps 5–7 are the existing plans, now safe to run in parallel because the seams are welded.

---

## Tier C gates (the hand-back, collapsed)

The whole inbox produces ONE collapsed gate cluster for Ewan, not many:

1. **Mac mini RAM figure** (one number; unblocks 3 acceptance tests + cell sizing).
2. **3 manual skill deletions** in Perplexity settings (decision-log-labeler, utterance-tagger, org-scope iso-8601). No tool to do it from the agent side.
3. **Ratify the name lock** (Beast in code; Infrastructure 1 in external framing) — single sign-off.
4. **Approve the §9 PROOF-OF-LIFE gate as the definition of "token-efficiency done"** — single sign-off.

Everything else in the inbox is research-resolved or proxy-signable.

---

## Honesty register (carried, not hidden)

- **"62% re-sent context"** — not primary-sourced. Internal use only until verified. Carried in master plan, impl brief, prior-art, Vellum events.
- **Anthropic Pool 1/Pool 2** — may be paused/unshipped. The estate-spec §6 Pool-2 trap depends on it; re-verify before relying on the guard.
- **Estate savings** — INTUITED until cost log runs ≥2 weeks. Vendor figures are MEASURED at source.
- **Unit-of-AI assumption** (tight curated domain → ~95% accuracy) — STRUCTURED per Ewan, not proven; carried in ui-methods orchestrator's preconditions.
- **Reliability gap** — Princeton 7× accuracy-vs-reliability finding; the deterministic floor exists to absorb this, not to fix it in the AI.
- **Confidently-wrong-but-in-spec residual** — the calibration floor that survives every lever. Size, monitor, do not pretend zero.

---

## What this plan is NOT

- Not a re-derivation of the token-eff master plan order (that doc already does it).
- Not a redesign of the sovereign build (architecture is decided; one unit first).
- Not a coupling of UI-methods to anything else (it's sealed; keep it sealed).
- Not a new pipe (there is exactly one pipe; this plan just makes that visible).

---

## Provenance + tiering

- All file reads verified against `stat -f %z` round-trip; no truncation.
- Live estate facts cross-checked against `beast-state-correction-live-verified__2026-06-24T1135` (`docker_ps`, `list_dir /opt/amplified`).
- Seam analysis is STRUCTURED — six rules derived by comparing the artefacts against each other and against the loaded doctrine (`amplified-constitution`, `min-rule`, `lean-by-default`, `end-to-end-closure`, `amplified-standing-grants`).
- Effective tier of this plan = MIN over inputs = STRUCTURED.

[CLOSURE] branch=PLAN | proxy=1 logged (mesh plan drafted as AI_PARTNER_PROXY) | gates=Mac mini RAM + 3 skill deletions + name-lock ratification + §9 gate ratification | inbox=perplexity-inbox__mesh-plan__v01__2026-06-24__perplexity.md | tier=STRUCTURED
