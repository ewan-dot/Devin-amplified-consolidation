"""CMAN research pipe — CLI entry point.

Full pipeline:
  1. DeepSeek generates 8 CMAN anchors (cross-domain, neutral language)
  2. Silo scrubber strips any remaining silo/pejorative terms
  3. Beast M1 fan-out: 8 probes × 20 hits via M1Orchestrator + SearXNG
  4. Brutal demote: Python regex filter, drop homonyms, score survivors
  5. DeepSeek grunt pass: score + extract methodology patterns
  6. DeepSeek synthesis: Swanson combine → endpoint claim
  7. Write run doc to perplexity-inbox/

Usage:
  python3 -m cman_pipe.run "telemetry methodologies in agentic AI"
  python3 -m cman_pipe.run "email deliverability" --dry-run
  python3 -m cman_pipe.run "programmatic SEO" --no-extract --out results.json

Flags:
  --dry-run     No Beast SSH, no API calls — smoke test the pipeline structure
  --no-extract  Run Beast fan-out but skip DeepSeek extraction passes
  --live        Force live API (default: live unless --dry-run)
  --out FILE    Write full JSON to FILE instead of auto-named inbox doc

Signed-by: cascade-mac | 2026-06-27 | cman-research-pipe
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load .env from clean-build so DEEPSEEK_API_KEY is available
_env_file = Path(__file__).parents[4] / "clean-build/02_build/.env"
if _env_file.exists():
    load_dotenv(_env_file)

from cman_pipe import anchor_generator, beast_fanout, brutal_demote, methodology_extract

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("cman_pipe.run")

INBOX = Path(__file__).parent.parent  # perplexity-inbox/


def _run_id(topic: str) -> str:
    slug = "".join(c if c.isalnum() else "-" for c in topic.lower()[:40]).strip("-")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"{slug}-{date}"


def _write_run_doc(run_id: str, result: dict) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    filename = f"RESEARCH-PIPE-RUN__{run_id}__v01__{ts}__cascade-mac.md"
    path = INBOX / filename

    endpoint = result.get("synthesis", {}).get("endpoint_claim", "INTUITED — extraction not run.")
    n_methods = len(result.get("methodologies", []))
    survivors  = result.get("survivors_count", 0)
    total_hits = result.get("total_hits", 0)
    batch_id   = result.get("batch_id", "—")
    gate0      = result.get("gate0_passed", 0)
    anchors    = result.get("anchors", [])
    patterns   = result.get("synthesis", {}).get("cross_domain_patterns", [])
    combos     = result.get("synthesis", {}).get("symbiotic_combinations", [])
    gaps       = result.get("synthesis", {}).get("gaps", [])

    anchor_table = "\n".join(
        f"| {a.get('domain','?')[:30]} | {a.get('query','')[:70]} |"
        for a in anchors
    )
    patterns_md = "\n".join(f"- {p}" for p in patterns) or "— none identified"
    combos_md   = "\n".join(
        f"### {c.get('name','?')}\n"
        f"Disciplines: {', '.join(c.get('disciplines',[]))}\n"
        f"How: {c.get('how_they_combine','')}\n"
        f"Steps: {'; '.join(c.get('combined_steps',[]))}\n"
        f"Failure modes: {', '.join(c.get('failure_modes',[]))}"
        for c in combos
    ) or "— none identified"
    gaps_md = "\n".join(f"- {g}" for g in gaps) or "— none identified"

    doc = f"""\
---
title: "CMAN Research Pipe Run — {result.get('topic', run_id)}"
run_id: {run_id}
date_utc: "{datetime.now(timezone.utc).isoformat()}"
seat: cascade-mac
tier: INTUITED
batch_id: {batch_id}
total_hits: {total_hits}
survivors: {survivors}
methodologies_found: {n_methods}
gate0_passed: {gate0}
---

# CMAN Research Pipe Run

**Topic:** {result.get('topic', run_id)}
**Run ID:** `{run_id}`
**Batch:** `{batch_id}`

## Human Summary

- Beast M1 fan-out: {len(anchors)} probes → {total_hits} hits → {survivors} survivors after brutal demote
- Gate0: {gate0} packets passed
- DeepSeek grunt extracted {n_methods} methodology candidates
- Endpoint claim: _{endpoint}_

## Wide 1 — CMAN Anchors

| Domain | Probe query |
|--------|-------------|
{anchor_table}

## Brutal Demote

{survivors} docs survived. Noise dropped: dictionary pages, homonyms, unrelated commercial pages.

## Cross-Domain Patterns (Wide 2 / Narrow 2)

{patterns_md}

## Swanson Combinations

{combos_md}

## Gaps

{gaps_md}

## Beast Metrics

| Metric | Value |
|--------|-------|
| Probes | {len(anchors)} |
| Total SearXNG hits | {total_hits} |
| Gate0 passed | {gate0} |
| Batch ID | `{batch_id}` |
| Survivors after demote | {survivors} |
| Methodologies extracted | {n_methods} |

## Orchestrator Payload

```json
{json.dumps(result, indent=2, default=str)[:4000]}
```

[CLOSURE] branch=cascade/cman-research-pipe | seat=cascade-mac | tier=INTUITED | gates=M1+gate0+brutal_demote+DeepSeek_grunt+synthesis
"""
    path.write_text(doc)
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description="CMAN research pipe")
    ap.add_argument("topic", nargs="?", help="Research topic")
    ap.add_argument("--topic", dest="topic_flag")
    ap.add_argument("--dry-run",    action="store_true", help="No SSH, no API calls")
    ap.add_argument("--no-extract", action="store_true", help="Skip extraction passes")
    ap.add_argument("--out",        help="Write JSON to this file")
    args = ap.parse_args()

    topic = args.topic or args.topic_flag
    if not topic:
        ap.error("Provide a topic")

    live    = not args.dry_run
    run_id  = _run_id(topic)
    t_start = time.time()

    log.info("Topic: %r", topic)
    log.info("Run ID: %s", run_id)

    # ── Stage 1: Generate CMAN anchors ────────────────────────────────────────
    log.info("Stage 1: Generating CMAN anchors via DeepSeek...")
    anchors = anchor_generator.generate(topic, live=live)
    log.info("  %d anchors generated", len(anchors))
    for a in anchors:
        log.info("  [%s] %s", a["domain"], a["query"])

    result: dict = {
        "topic":   topic,
        "run_id":  run_id,
        "anchors": anchors,
    }

    # ── Stage 2: Beast M1 fan-out ─────────────────────────────────────────────
    if live:
        log.info("Stage 2: Beast M1 fan-out (%d probes)...", len(anchors))
        fanout = beast_fanout.run(anchors, run_id)
        if "error" in fanout and fanout["error"]:
            log.error("Beast fan-out failed: %s", fanout["error"])
            result.update(fanout)
        else:
            result.update({
                "total_hits":  fanout.get("total_hits", 0),
                "batch_id":    fanout.get("batch_id"),
                "gate0_passed":fanout.get("gate0_passed", 0),
                "gate0_failed":fanout.get("gate0_failed", 0),
                "probes":      fanout.get("probes", []),
                "raw_results": fanout.get("results", []),
            })
            log.info("  %d hits, batch=%s, gate0=%d",
                     result["total_hits"], result["batch_id"], result["gate0_passed"])
    else:
        log.info("Stage 2: DRY-RUN — skipping Beast fan-out")
        result.update({"total_hits": 0, "batch_id": "DRY-RUN",
                        "gate0_passed": 0, "raw_results": []})

    # ── Stage 3: Brutal demote ────────────────────────────────────────────────
    log.info("Stage 3: Brutal demote...")
    raw = result.get("raw_results", [])
    survivors = brutal_demote.demote(raw)
    result["survivors_count"] = len(survivors)
    result["survivors"] = [
        {"title": d.title, "url": d.url, "snippet": d.snippet,
         "score": d.score, "domain": d.domain}
        for d in survivors
    ]
    log.info("  %d / %d docs survived demote", len(survivors), len(raw))
    if survivors:
        log.info(brutal_demote.summarise(survivors))

    # ── Stage 4 + 5: Extraction (grunt + synthesis) ───────────────────────────
    if args.no_extract:
        log.info("Stage 4–5: Skipped (--no-extract)")
        result.update({"methodologies": [], "synthesis": {}})
    else:
        log.info("Stage 4: DeepSeek grunt — methodology extraction...")
        # Pass only top 15 survivors — grunt needs focused, high-score docs
        top = survivors[:15]
        extraction = methodology_extract.extract(
            [{"title": d.title, "url": d.url, "snippet": d.snippet}
             for d in top],
            topic, live=live,
        )
        result["methodologies"]  = extraction.methodologies
        result["synthesis"]      = extraction.synthesis
        if extraction.error:
            result["extraction_error"] = extraction.error
            log.error("Extraction error: %s", extraction.error)
        else:
            log.info("  %d methodologies extracted", len(extraction.methodologies))
            ep = extraction.synthesis.get("endpoint_claim", "")
            if ep:
                log.info("  Endpoint: %s", ep)

    result["elapsed_s"] = round(time.time() - t_start, 1)

    # ── Output ────────────────────────────────────────────────────────────────
    out_path = args.out
    if out_path:
        Path(out_path).write_text(json.dumps(result, indent=2, default=str))
        log.info("JSON → %s", out_path)

    doc_path = _write_run_doc(run_id, result)
    log.info("Run doc → %s", doc_path)

    # Print endpoint claim to stdout
    ep = result.get("synthesis", {}).get("endpoint_claim", "")
    print(f"\nTopic:    {topic}")
    print(f"Hits:     {result.get('total_hits', 0)}")
    print(f"Survived: {result.get('survivors_count', 0)}")
    print(f"Methods:  {len(result.get('methodologies', []))}")
    if ep:
        print(f"\nEndpoint: {ep}")
    print(f"\nRun doc → {doc_path}")


if __name__ == "__main__":
    main()
