# Repo Consolidation + Asset Inventory — Implementation Brief

TIER: STRUCTURED (worktree contract MEASURED via worktree definitions; asset inventory not yet built)
PROVENANCE: sessions `f6ae6952` (2026-06-19 to 21, 23t — Agent Worktree Contract), `7dd0ce64` (2026-06-21, 22t — repo dedup), `244626bd` (2026-06-22-24, 23t — M5 consolidation + YAML dedup)
STATUS: contract defined; inventory promised but not landed; live dedup partially run but not collapsed
FOR: M5 watcher

## What exists

### The Agent Worktree Contract (`f6ae6952`)

- **One protected local floor** with **one isolated worktree/work-desk per branch/task.**
- **Cloud agents use isolated VMs** with the same branch→PR gate.
- **Reusable shape lives in templates/recipe books**, not in worktrees. Worktrees are disposable task instances.
- **Six mandatory slots** per recipe: start / finish / waypoints / what-good-looks-like / what-bad-looks-like / hooks.
- **Fast deterministic checks block; AI reviewers are advisory** unless structured as separate non-self-approving review gates.
- **Domain/system-based repo organisation**, not department-based (rejected mid-session).

### Live M5 state (`7dd0ce64` + `244626bd`)

- Hazel moved ~29 GB / 199,418 files into `~/ingestion-to-research-pipe/`.
- Exact-dedup found 13,699 groups / 51,351 redundant files / 8.93 GB waste.
- `dedup_apply.py` exists on the M5 — keeps shortest-path exact duplicates, uses structural YAML comparison, quarantines divergent files (does not delete).
- **At least 7 copies of `clean-build`** still on the M5 across `~/Clone Github/`, `~/Projects/`, `~/Gitkrakken/`, `~/github_porch/` (+geordie-governed variant), `~/worktrees/clean-build-codex-data`, and `.worktrees/` paths. **Dedupe identified and staged; did not collapse.**
- Quarantine + move-list pattern: `~/.dedupe-quarantine/`, `~/dedupe_to_move.txt`. Safe (no delete).
- Vellum sensor code: cloned on the M5 under `~/Antigravity/vellum/` — same as GitHub `fleet-vellum`.

## What was done

- Worktree contract defined (above).
- Recipe-book/template structure defined.
- Mac dedup ran in *report-and-stage* mode; review queues + manifests produced.
- Sensor research recovered from M5 via Spotlight content-search (after Spotlight-by-name failed — index may be stale post-dedup; `mdutil -s ~` returned "unknown indexing state").

## What it means

- **The asset inventory Ewan promised is not landed.** The decision rule ("use or drop") is named; the list is not.
- **Seven `clean-build` copies** are a live source-of-truth ambiguity — the canonical one is not marked. Any agent reading "the clean-build repo" could read any of 7 different states.
- **Spotlight may be unreliable** until reindexed. mdfind "no results" should be read as "maybe not indexed", not "doesn't exist". Trap.
- **Domain/system-based organisation** is the decided convention but no current repo map enforces it.

## What to change next

1. **Read `dedupe_to_move.txt` + `.dedupe-quarantine/` + `DEDUP-STATISTICS.md`** — read-only — and produce the kill/keep list. (Tier A.)
2. **Mark the canonical `clean-build`.** One path; all others quarantined or deleted after Ewan signs off.
3. **Build the asset inventory** — one file listing every repo + worktree on M5 with: path, last-touched, branch, has-uncommitted-changes, use/drop verdict. Tier A research; no Beast writes.
4. **`mdutil -E /`** to force clean Spotlight reindex (Ewan-only — A5 in autonomy contract, spikes CPU).
5. **Codify the recipe-book template** — one file with the 6 mandatory slots, drop into each repo at init.
6. **Adopt domain/system-based repo names** — rename plan needed; not a free action.

## Not yet verified

- Contents of `dedupe_to_move.txt` and `.dedupe-quarantine/`.
- Which `clean-build` copy is canonical.
- Whether `~/Antigravity/vellum/` is up-to-date with `fleet-vellum` main.
- Spotlight index health post-dedup.

## Tier C gates (Ewan only)

- `mdutil -E /` (system-level, spikes CPU).
- Any deletion of duplicates (move-only allowed without sign-off).
- Repo renames.

[CLOSURE] branch=PLAN | proxy=1 logged | gates=reindex approval + delete vs move sign-off + canonical clean-build pick (collapse to one hand-back) | inbox=repo-consolidation-asset-inventory__implementation-brief__v01__2026-06-24__perplexity.md | tier=STRUCTURED
