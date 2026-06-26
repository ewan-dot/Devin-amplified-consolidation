---
title: "Instructions — Claude Code runs wide→narrow×3 research pipe on Beast"
document_type: operating_instructions
artifact_id: INSTRUCTIONS__claude-beast-research-pipe__v01__2026-06-26__cursor
date_utc: 2026-06-26
author: cursor
reader: claude-code
epistemic_tier: INTUITED
provenance: Cursor seat Beast runs 2026-06-26 (hooks-harness-doorways, sovereign-ide-self-push); live SSH verification same day
---

# Claude Code — Beast research pipe (wide→narrow×3)

**Audience:** Claude Code on **M5/Mac**, in a **worktree** under `ingestion-to-research-pipe` (doors/harness session used `perplexity-inbox/` on that repo — prefer an isolated worktree, not the main checkout).

**Goal:** Run the five-stage **search shape** (fan-out → brutal demote → dual-POV precision → neighbourhood → Swanson combine) on **Beast**, not on Mac WebSearch alone. Beast has SearXNG + `research-pipe` container; Mac supplements gap-fill only.

**Reference runs (this session, INTUITED verified on Beast):**

- `RESEARCH-PIPE-RUN__hooks-harness-doorways__v01__2026-06-26__cursor.md`
- `RESEARCH-PIPE-RUN__sovereign-ide-self-push__v01__2026-06-26__cursor.md`
- Pattern law: `RESEARCH-PIPE-RUN__claude-code-brief__v04__2026-06-24__perplexity.md`

---

## 1. Prerequisites

| Check | Command / note |
|-------|----------------|
| **Tailscale up** | M5 must see Beast on tailnet. `tailscale status` — Beast hostname `beast` or IP `135.181.161.131`. |
| **SSH to Beast** | `ssh beast` (or `ssh root@135.181.161.131`). |
| **Worktree** | From repo root: `git worktree add .worktrees/claude-<topic> -b claude/<topic>` then `cd .worktrees/claude-<topic>/perplexity-inbox`. |
| **Containers healthy** | See §3 step 1. Expect `research-pipe` **healthy** and `searxng` **Up**. |
| **No Perplexity API key** | Fan-out uses **SearXNG inside Docker** (`SEARXNG_URL=http://searxng:8080`). No `PPLX_API_KEY` needed for this path. **INTUITED:** Max-login Perplexity browser seat is separate; this pipe is Beast SearXNG. |
| **Skills loaded** | `~/.cursor/skills/amplified-research-pipe/SKILL.md` + `source-first-retrieval/SKILL.md` |
| **Epistemic floor** | All agent-authored output stays **INTUITED** until Python promotion gates fire. |

**Mac read-only rule (Ewan architect Mac):** does not block **Claude Code sovereign self-push on M5** for F8 — see §8.

---

## 2. What Beast entrypoint IS vs IS NOT

### IS (live path — use this)

| Piece | Location on Beast |
|-------|-------------------|
| Container | `research-pipe` (healthy) |
| CLI | `python3 -m research_pipe.runner` |
| Fan-out engine | `M1Orchestrator` + `SearXNGBackend` (L1) |
| Staging | `runner process-queue` → `promotion_investigation.process_queue` |
| SearXNG | In-container `http://searxng:8080`; HTTPS fleet face `https://search.beast.amplifiedpartners.ai` |
| Wiring doc | `/app/research_pipe/docs/WIRING.md` inside container |
| Host staging | `/opt/amplified-machine/apds/staging/<batch_id>/` |
| Host queue | `/opt/amplified-machine/apds/queue/` |

**Verified 2026-06-26:** `five_stage_orchestrator.py` is **ABSENT** in the Beast container. Do not look for it on Beast.

### IS NOT (do not use on Beast)

| Wrong path | Why |
|------------|-----|
| `five_stage_orchestrator.py` | Mac/clean-build skill reference only; **not deployed** on Beast |
| Mac WebSearch as primary run | Agent-seat supplement only — label it, not the Beast run |
| Perplexity API as L1 | Empty/unwired for this job; SearXNG is L1 |
| Direct `knowledge_vectors` / Brain writes | Research is **producer → staging only** (WIRING.md constitutional boundary) |
| Auto-promote | Staging manifest `auto_promote: false` — human + gates |

---

## 3. Step-by-step — full run

### Step 0 — Craft `corpus_item_id`

Slug: `{topic-kebab}-{YYYY-MM-DD}`

Examples from this session:

- `hooks-harness-doorways-fleet-2026-06-26`
- `sovereign-ide-self-push-2026-06-26`

Use the **same string** for `RUN_ID`, `BRAIN_ID`, JSONL witness, and inbox filename stem.

### Step 1 — Preflight Beast

```bash
ssh beast "docker ps --format '{{.Names}}\t{{.Status}}' | grep -E 'research|searx'"
```

Expect:

```
searxng         Up …
research-pipe   Up … (healthy)
```

```bash
ssh beast "docker exec research-pipe python3 -m research_pipe.runner status"
```

Queue JSON shows `pending` / `processing` / `done` counts.

### Step 2 — Wide 1: raw terms only (echo chamber rule)

**Extract search terms from Ewan frame + primary source documents only.** Never paste prior synthesis headings or survivor prose back into queries.

1. List **5–8 candidate founding disciplines** (physical security, aviation CRM, OTP, event sourcing, …).
2. For each, write one **raw probe string** (nouns from primary docs, not your summary).
3. Record Wide 1 table in your run doc (discipline | raw probe terms).

Pattern (from v04 brief):

```
WIDE 1   → 5–8 domains
NARROW 1 → canonical source per domain
WIDE 2   → cross-domain failure modes
NARROW 2 → 2–3 convergent mechanisms
WIDE 3   → independent confirmation or contradicting domain
NARROW 3 → endpoint claim, tier-tagged (INTUITED unless ≥3 unrelated founding disciplines measured)
```

Agent-side stages 2–5 (brutal demote, dual-POV, neighbourhood, Swanson) happen **after** fan-out hits land — in your analysis + run doc, not in a separate Beast orchestrator.

### Step 3 — Fan-out: 8 SearXNG probes (Beast)

**Proven pattern:** one-shot Python script copied into the container. Cursor used `/tmp/beast_rerun.py` and `/tmp/beast_sovereign_ide.py`.

#### 3a — Write script locally (adapt `FANOUT_QUERIES` + `RUN_ID`)

Save as e.g. `perplexity-inbox/.tmp_beast_run.py`:

```python
"""Beast research pipe — wide1 fan-out + process-queue staging."""
import asyncio
import json
import os
from datetime import datetime, timezone

from epistemic_core.tiers import EpistemicTier
from research_pipe.backends.searxng import SearXNGBackend
from research_pipe.emitter import LogEmitter
from research_pipe.orchestrators.m1 import M1Orchestrator
from research_pipe.promotion_alert import AlertQueue, alert_from_drift
from research_pipe.promotion_investigation import process_queue
from research_pipe.query_schema import BackendLayer, ResearchQuery, SearchMode, SearchType
from research_pipe.router import BackendRouter
from research_pipe.vellum_signer import VellumSigner

RUN_ID = "YOUR-CORPUS-ITEM-ID-2026-06-26"  # ← change
BRAIN_ID = RUN_ID

FANOUT_QUERIES = [
    "probe 1 raw terms from primary docs only",
    "probe 2 …",
    # 5–8 probes total; session runs used 8
]

async def fan_out(orch):
    probes, total_hits = [], 0
    for i, q in enumerate(FANOUT_QUERIES, 1):
        query = ResearchQuery(
            mode=SearchMode.M1,
            brain_entry_id=BRAIN_ID,
            sharpened_question=q,
            query_string=q,
            search_type=SearchType.M1,
            backend_set=[BackendLayer.L1],
            local_attempts_count=2,
            five_rods_result="verify:radical_honesty:research_proposes_python_disposes",
            pudding_label=f"{RUN_ID}.wide1",
        )
        run = await orch.execute(query)
        hits = len(run.search_run.results) if run.search_run and run.search_run.results else 0
        total_hits += hits
        probes.append({"probe": i, "query": q[:60], "hits": hits, "success": run.success, "error": run.error})
    return probes, total_hits

async def main():
    ts = datetime.now(timezone.utc).isoformat()
    router = BackendRouter()
    router.register(BackendLayer.L1, SearXNGBackend())
    orch = M1Orchestrator(
        router=router,
        signer=VellumSigner(agent_id="claude-code-research-pipe"),
        emitter=LogEmitter(),
    )
    probes, total_hits = await fan_out(orch)

    claim = "One-line endpoint claim from Narrow 3 — INTUITED until measured."
    alert = alert_from_drift(
        brain_entry_id=BRAIN_ID,
        claim=claim,
        current_tier=EpistemicTier.INTUITED,
        drift_signal="green",
        reason=f"claude-code wide-narrow x3 {RUN_ID}",
        pudding_label=f"{RUN_ID}.swanson",
    )
    queue = AlertQueue()
    path = queue.enqueue(alert)
    inv_results = await process_queue(limit=1)
    inv = inv_results[0] if inv_results else None

    out = {
        "timestamp": ts,
        "run_id": RUN_ID,
        "host": "beast",
        "container": "research-pipe",
        "searxng_url": os.environ.get("SEARXNG_URL"),
        "fan_out_probes": len(probes),
        "searxng_hits_total": total_hits,
        "probes": probes,
        "alert_queued": str(path),
        "alert_id": alert.alert_id,
        "investigation": {
            "alert_id": inv.alert_id if inv else None,
            "success": inv.success if inv else False,
            "batch_id": inv.batch_id if inv else None,
            "packets_staged": inv.packets_staged if inv else 0,
            "gate0_passed": inv.gate0_passed if inv else 0,
            "gate0_failed": inv.gate0_failed if inv else 0,
            "error": inv.error if inv else "no investigation result",
        },
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

#### 3b — Copy and run on Beast

```bash
scp perplexity-inbox/.tmp_beast_run.py beast:/tmp/beast_run.py

ssh beast "docker cp /tmp/beast_run.py research-pipe:/tmp/beast_run.py && \
  docker exec research-pipe python3 /tmp/beast_run.py" \
  | tee /tmp/beast_run_out.json
```

**Session metrics (INTUITED, reproduced):** 8/8 probes success, ~160 SearXNG hits total (~20 hits/probe), `gate0_passed: 20`, `packets_staged: 20`.

#### 3c — Alternative: CLI-only queue (no fan-out script)

If fan-out was already done agent-side and you only need staging:

```bash
ssh beast "docker exec research-pipe python3 -m research_pipe.runner enqueue-alert \
  --brain-entry-id YOUR-CORPUS-ITEM-ID-2026-06-26 \
  --claim 'One-line INTUITED endpoint claim' \
  --tier INTUITED \
  --drift green \
  --reason 'claude-code promotion investigation' \
  --pudding-label YOUR-CORPUS.swanson"

ssh beast "docker exec research-pipe python3 -m research_pipe.runner process-queue --limit 1"
```

**INTUITED:** CLI-only path stages packets but **skips** the 8-probe SearXNG fan-out — use the script for a full Beast run.

### Step 4 — Agent-side stages (Wide 2 → Narrow 3)

On Mac/M5 (not Beast Python):

1. **Brutal demote** — drop homonyms (Sally Beauty, Eventbrite, unrelated Copilot products, …). Session survivors: ~5.
2. **Dual-POV precision** — methodology + completeness in parallel.
3. **Neighbourhood / Wide 3** — cross-domain check.
4. **Swanson combine** — endpoint claim with founding-discipline table.

Mac **WebSearch** allowed for Narrow 1 canonical URL gap-fill — label `mac_supplement: agent-seat, not Beast run`.

### Step 5 — Write run doc + JSONL witness

See §6.

---

## 4. Fan-out commands (quick reference)

```bash
# Health
ssh beast "docker ps --format '{{.Names}}\t{{.Status}}' | grep -E 'research|searx'"

# Runner help
ssh beast "docker exec research-pipe python3 -m research_pipe.runner --help"

# Env inside container
ssh beast "docker exec research-pipe env | grep -E 'SEARXNG|STAGING|QUEUE|RESEARCH_PIPE'"

# Expected env (verified 2026-06-26):
# RESEARCH_PIPE_QUEUE_DIR=/app/apds/queue
# RESEARCH_PIPE_STAGING_DIR=/app/apds/staging
# SEARXNG_URL=http://searxng:8080

# Queue status
ssh beast "docker exec research-pipe python3 -m research_pipe.runner status"

# Inspect staging batch on host
ssh beast "ls -la /opt/amplified-machine/apds/staging/<batch_id>/"
```

---

## 5. `runner process-queue` / staging batch

| Step | What happens |
|------|----------------|
| `enqueue` | Writes `TierPromotionAlert` to `/app/apds/queue/pending/` |
| `process-queue` | `DuckDBGate` → `M1Orchestrator` → SearXNG → `Gate0Verifier` → staging |
| Output | `/opt/amplified-machine/apds/staging/<batch_id>/manifest.json` + `packets.jsonl` |
| Gate0 | Structural verify; session runs: 20/20 pass, 0 fail |
| Promote | **No** — `auto_promote: false` |

```bash
ssh beast "docker exec research-pipe python3 -m research_pipe.runner process-queue --limit 1"
```

Optional manual porch release (ops — **INTUITED:** not required for inbox run):

```bash
ssh beast "docker exec research-pipe python3 -m research_pipe.runner release-to-porch --help"
```

---

## 6. Where output lands

| Artefact | Path |
|----------|------|
| **Run doc (primary)** | `perplexity-inbox/RESEARCH-PIPE-RUN__<topic>__v01__YYYY-MM-DD__claude.md` |
| **JSONL witness** | `~/amplified-pipeline/data/research-pipe-docs/YYYY-MM-DD_five-stage_<corpus_item_id>.jsonl` |
| **Beast staging** | `/opt/amplified-machine/apds/staging/<batch_id>/` on Beast host |
| **Script stdout** | `/tmp/beast_run_out.json` on Mac (keep for audit) |

### Run doc shape (copy session templates)

Frontmatter + sections:

- Human summary (Beast metrics: probes, hits, batch_id, survivors)
- Orchestrator payload: meta, stage_result (Wide1–3 tables), brutal demote survivors, Beast run metrics
- handoff: `do_not`, `architect_flags`, `goal_link`
- Research prompt block (raw terms only, for re-run)
- `[CLOSURE]` footer

Naming: `{topic}__{kind}__vNN__YYYY-MM-DD__{seat}.md`

### JSONL witness lines (one JSON object per line)

Emit events for: `fan_out` / `probe` / `brutal_demote` / `swanson_combine` with `corpus_item_id`, `batch_id`, `epistemic_tier: INTUITED`, `host: beast`.

---

## 7. F8 publish — commit, Vellum, self-push (sovereign IDE)

**F8 = Published** (`finish-waypoint.mdc`, `research-conclusion__doors-telemetry-completion__v01__2026-06-26__cursor.md`):

| Gate | Action |
|------|--------|
| F-RODS | Constitutional pass — no rod violations |
| Inbox artefact | Run doc in `perplexity-inbox/` with `[CLOSURE]` |
| GitHub pushed | **Claude Code self-push from M5** — sovereign IDE seat; do **not** wait for Devin |
| Vellum row | Witness on Inbox — Ewan sheet |

### Copy-paste finish sequence

```bash
cd /path/to/worktree/perplexity-inbox   # or repo root

git add RESEARCH-PIPE-RUN__* INSTRUCTIONS__* \
  ~/amplified-pipeline/data/research-pipe-docs/*_<corpus_item_id>.jsonl

git commit -m "$(cat <<'EOF'
Research pipe run: <topic> — Beast wide-narrow x3 + inbox witness.

EOF
)"

git push -u origin HEAD   # feature branch; M5 Claude Code sovereign push
```

**Vellum** (MCP `user-vellum` or API): one row — `entry_type: agent_write`, `metadata.envelope: { from: "claude", to: "ewan", type: "info", subject: "Research pipe: <topic>" }`, tier INTUITED. See `OPERATING-RULE__post-inbox-and-vellum__v01__2026-06-26__cursor.md`.

Chat to Ewan: **pointer only** (path + subject), not a duplicate essay.

---

## 8. What NOT to do

| Don't | Do instead |
|-------|------------|
| Use synthesis prose as search input | Raw terms from primary docs only (echo chamber rule) |
| Skip brutal demote | SearXNG homonym noise is high — demote before precision |
| Call `five_stage_orchestrator.py` on Beast | M1 + `runner process-queue` |
| Promote tier from agent output | Stay INTUITED; Python gates promote |
| Treat Mac WebSearch as the Beast run | Label Mac gap-fill separately |
| Use SearXNG raw IP `:8080` from Mac | HTTPS `search.beast.amplifiedpartners.ai` or in-container URL |
| Auto-promote staging packets | Staging is evidence for human review |
| Wait for Devin to push F8 | Sovereign IDE: Claude Code pushes from M5 |
| Write Brain/knowledge_vectors directly | Producer → staging → porch → APDS workflow |

---

## 9. Session evidence (INTUITED)

| Run | corpus_item_id | batch_id | probes | hits | gate0 |
|-----|----------------|----------|--------|------|-------|
| hooks-harness-doorways | hooks-harness-doorways-fleet-2026-06-26 | 1d501a25-9e71-4ee5-b238-1c1d4a6f4062 | 8/8 | 160 | 20/20 |
| sovereign-ide-self-push | sovereign-ide-self-push-2026-06-26 | 26f2dd5c-70c5-4feb-92a5-ca58d375efe5 | 8/8 | 160 | 20/20 |

Beast scripts retained in container: `/tmp/beast_rerun.py`, `/tmp/beast_sovereign_ide.py` (**INTUITED** — may be overwritten; keep copy in worktree if needed).

---

## 10. Beast path cheat sheet

| What | Path |
|------|------|
| Container app root | `/app/research_pipe/` |
| M1 orchestrator | `/app/research_pipe/orchestrators/m1.py` |
| Runner CLI | `/app/research_pipe/runner.py` |
| WIRING.md | `/app/research_pipe/docs/WIRING.md` |
| SearXNG backend | `/app/research_pipe/backends/searxng.py` |
| Host queue | `/opt/amplified-machine/apds/queue/` |
| Host staging | `/opt/amplified-machine/apds/staging/` |
| Traefik route | `research-pipe.beast.amplifiedpartners.ai` (**INTUITED:** HTTP API; CLI path above is what Cursor used) |

---

[CLOSURE] branch=PLAN | proxy=none | gates=Beast M1+runner path documented from live session | inbox=INSTRUCTIONS__claude-beast-research-pipe__v01__2026-06-26__cursor.md | tier=INTUITED
