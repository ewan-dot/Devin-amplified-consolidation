# Estate Token-Efficiency — Master Plan

TIER: STRUCTURED · vendor numbers MEASURED at source · estate savings INTUITED until the cost log runs ≥2 weeks
PROVENANCE: synthesis of this thread's five artefacts + verified GitHub state of Amplified-Partners (2026-06-23)
GOAL-LINK: recurring AI spend is cash out. This cuts it across the whole estate and proves the cut. Make money so we can give it away.

## The one rule
**Stop sending tokens that don't earn their place this turn** — whether that's verbose output, re-sent history, raw ramble, or unused tool schemas. Every lever below is one application of it.

## The four fronts (and the artefact that owns each)

| Front | What it cuts | Owning artefact | State |
|---|---|---|---|
| 1. Output verbosity | My replies (~99.5% of conversation cost; cut X% → save ~X%) | `lean-by-default` skill (auto-loads) + `lean_output_estate_guide` (per-IDE) + Claude `CONVENTIONS.md` | Skill live; guide ready to deploy |
| 2. The estate plumbing | Caching, routing, batch, central proxy across M4/M5/Beast + every IDE | `token_efficiency_estate_spec` (finish + prove) | Proxy ~60% built (`estate-cost-tools`); router unbuilt; not proven |
| 3. The levers (evidence) | CLI-over-MCP, caching, Haiku/local routing, repo-maps, output discipline | `token_reduction_agent_doc` + 3 raw dossiers | Researched, cited |
| 4. Voice-first discovery | Frontier model paying to wade through raw speech | `voice_first_agent_doc` (5-step loop) | Designed; Steps 1–2 = fastest wins |

## How they fit
- **Front 1** is the biggest single conversation lever and the only one already live (the skill).
- **Front 4** is Front 1 applied to how you *talk*: capture local (£0), cheap clean, idealise → cache-stable brief, route, harvest to Brain.
- **Front 2** is the infrastructure that makes Fronts 1/3/4 hold automatically across machines and IDEs (the credit-first router + central proxy).
- **Front 3** is the evidence base under Front 2's §4.

## Rollout (cheapest-and-most-durable first)
1. **Now, zero infra:** deploy `CONVENTIONS.md` + lean rule into every IDE config slot (Front 1). Wire local STT + cheap cleanup for voice (Front 4, Steps 1–2).
2. **Bake per-IDE knobs:** caching, model pins, ignore files, thinking-token caps, repo-maps (Front 3 → config).
3. **Deploy + live-prove the proxy** across all lanes (`estate-cost-tools`, Front 2 §D).
4. **Build + deploy the credit-first router** (Front 2 §C).
5. **Telemetry → Vellum**; budgets graduate INTUITED→MEASURED at ≥2 weeks live (Front 2 §E).

## The exit gate (done = proven, not pushed)
The plan is complete only when the estate-wide proof run passes and lands in `PROOF-OF-LIFE.md`: proxy live + wired across **every** IDE lane; router live on the Beast, survives restart; one job routed across ≥3 executor classes with a credit-first decision logged; budget guard refuses an over-budget reserve; >90% cache-read on a repeat job; a local-lane job at $0 tokens; telemetry lands in Vellum; before/after spend delta measured. (Full 10-point gate in `token_efficiency_estate_spec` §9.)

## Open items (carried from the pieces)
1. **Mac mini RAM** — blocks the local-model tier. Need the real figure.
2. **Anthropic Pool 1/Pool 2** — may be paused/unshipped; re-verify before relying on the §6 trap.
3. **"62% re-sent context"** — not primary-sourced; internal use only until verified.
4. **CLI-vs-MCP** — cite 32× (Scalekit) / 98.7% (Anthropic) as primaries; CLI for read-only doors, code-execution for big APIs, MCP only where caching+auth earn it.
5. **Spend delta check** — scheduled 7 July; will report "insufficient data" if the proxy isn't live by then.

## Artefact index (this thread)
- `estate-token-efficiency__master-plan` (this file)
- `token_efficiency_estate_spec` — the finish-and-prove spec
- `token_reduction_agent_doc` + `_human_brief` + 3 dossiers (`research_cli_vs_mcp`, `research_ide_controls`, `research_context_habits`)
- `voice_first_agent_doc` + `_human_brief` (`research_voice_first_efficiency`)
- `lean_output_estate_guide`
- `lean-by-default` skill (library, auto-loads)

Pipe discipline: draft in workspace. Human-facing → Drive; agent docs → Brain via the pipe; Vellum events drafted, not yet written. Nothing direct to Beast.
