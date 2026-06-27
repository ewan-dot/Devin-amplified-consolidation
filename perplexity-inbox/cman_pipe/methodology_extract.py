"""Methodology extractor — survivors → structured methodology catalogue.

Two passes, matching the clean-build model_router pattern:

  Pass 1 — DeepSeek V4 (grunt): read all survivor snippets, score each doc
  for methodology signal, extract CMO tags, brutal-demote stragglers that
  passed the regex but carry no real methodology content.

  Pass 2 — DeepSeek V4 (synthesis): write the methodology catalogue from
  survivors. Cached static system prompt so repeated calls are cheap.

Both passes use DeepSeek (openai SDK, api.deepseek.com). Claude synthesis is
available as a toggle if CLAUDE_SYNTHESIS=1 is set — but DeepSeek handles
both by default (Ewan's preference; no bias, no sabotage).

Tier: all output is INTUITED until Python promotion gates fire.

Signed-by: cascade-mac | 2026-06-27 | cman-research-pipe
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger("amplified.cman_pipe.methodology_extract")

# ── Model config ─────────────────────────────────────────────────────────────

_DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
_DEEPSEEK_BASE  = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
_DEEPSEEK_KEY   = os.environ.get("DEEPSEEK_API_KEY", "")

_CLAUDE_MODEL   = os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5-20251001")
_USE_CLAUDE_SYNTHESIS = os.environ.get("CLAUDE_SYNTHESIS", "0") == "1"

# ── Static system prompts (byte-stable — cache depends on it) ─────────────────

_GRUNT_SYSTEM = """\
You are a methodology extraction engine for the Amplified research pipe.

Given a list of research documents (title + snippet), your job is to:
1. Score each document 0–10 for methodology content (does it describe HOW
   something works, not just WHAT it is?).
2. For documents scoring ≥ 5, extract:
   - methodology_name: what the methodology is called (or coin a structural name)
   - domain: the source discipline (aviation, SRE, medicine, etc.)
   - steps: the key steps/phases as a compact list (max 5 items)
   - outcome: what the methodology produces or improves
   - source_url: the document URL
3. Drop documents scoring < 4.

Rules:
- Use the document's own vocabulary, not AI silo terms.
- Do not invent steps not evidenced in the snippet.
- Tag INTUITED where evidence is thin (single source, vague snippet).

Output JSON only:
{
  "scored": [
    {"doc_index": 0, "score": 8, "keep": true},
    ...
  ],
  "methodologies": [
    {
      "methodology_name": "...",
      "domain": "...",
      "steps": ["step 1", "step 2", ...],
      "outcome": "...",
      "source_url": "...",
      "tier": "INTUITED",
      "cmo": {"context": "...", "mechanism": "...", "outcome": "..."}
    },
    ...
  ]
}
"""

_SYNTHESIS_SYSTEM = """\
You are the methodology synthesiser for the Amplified production brain.

Given a set of extracted methodologies from multiple founding disciplines,
produce a SWANSON COMBINATION: identify which methodologies are symbiotic
(each fills a gap the other leaves) and write a combined endpoint methodology.

Rules (strict):
1. Describe HOW, not WHAT. The output must be implementable.
2. Use neutral, cross-domain vocabulary. No AI silo terms.
3. Attribute every claim to its source discipline.
4. Tag the final claim INTUITED — never promote beyond what the evidence supports.
5. If two methodologies are NOT symbiotic, say so explicitly.
6. Identify any cross-domain failure modes that appear in multiple disciplines.

Output JSON only:
{
  "endpoint_claim": "One-sentence implementable endpoint claim — INTUITED.",
  "founding_disciplines": ["domain1", "domain2", ...],
  "symbiotic_combinations": [
    {
      "name": "...",
      "disciplines": ["...", "..."],
      "how_they_combine": "...",
      "combined_steps": ["step 1", "step 2", ...],
      "failure_modes": ["..."]
    }
  ],
  "cross_domain_patterns": ["pattern that appears in ≥2 disciplines", ...],
  "gaps": ["what is NOT covered by any discipline found", ...]
}
"""


@dataclass
class ExtractionResult:
    methodologies: list[dict] = field(default_factory=list)
    synthesis:     dict       = field(default_factory=dict)
    raw_grunt:     str        = ""
    raw_synthesis: str        = ""
    error:         str        = ""


def _get_client():
    key = _DEEPSEEK_KEY or _load_key()
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY not found")
    from openai import OpenAI
    return OpenAI(api_key=key, base_url=_DEEPSEEK_BASE)


def _load_key() -> str:
    candidates = [
        Path(__file__).parents[4] / "clean-build/02_build/.env",
        Path.home() / ".env",
    ]
    for p in candidates:
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith("DEEPSEEK_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return ""


def _grunt_pass(survivors: list[dict], client) -> tuple[list[dict], str]:
    """DeepSeek grunt: score + extract methodologies from survivors."""
    docs_block = "\n".join(
        f"[{i}] TITLE: {d['title']}\n    URL: {d['url']}\n    SNIPPET: {d['snippet'][:250]}"
        for i, d in enumerate(survivors)
    )
    user_msg = f"Documents to analyse ({len(survivors)} total):\n\n{docs_block}"

    resp = client.chat.completions.create(
        model=_DEEPSEEK_MODEL,
        messages=[
            {"role": "system",  "content": _GRUNT_SYSTEM},
            {"role": "user",    "content": user_msg},
        ],
        temperature=0.1,
        max_tokens=4096,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content or "{}"
    try:
        data = json.loads(raw)
        methodologies = data.get("methodologies", [])
        return methodologies, raw
    except Exception:
        return [], raw


def _synthesis_pass(methodologies: list[dict], topic: str, client) -> tuple[dict, str]:
    """DeepSeek synthesis: Swanson combine across extracted methodologies."""
    methods_block = json.dumps(methodologies, indent=2)
    user_msg = (
        f"Topic: {topic}\n\n"
        f"Extracted methodologies from {len(methodologies)} founding disciplines:\n\n"
        f"{methods_block}"
    )
    resp = client.chat.completions.create(
        model=_DEEPSEEK_MODEL,
        messages=[
            {"role": "system",  "content": _SYNTHESIS_SYSTEM},
            {"role": "user",    "content": user_msg},
        ],
        temperature=0.2,
        max_tokens=3000,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content or "{}"
    try:
        return json.loads(raw), raw
    except Exception:
        return {}, raw


def extract(survivors: list[dict], topic: str, *, live: bool = True) -> ExtractionResult:
    """Full extraction pipeline: grunt pass → synthesis pass.

    live=False: return mock output (dry run, no API calls).
    """
    if not live:
        return ExtractionResult(
            methodologies=[{"methodology_name": "DRY-RUN", "domain": "mock", "tier": "INTUITED"}],
            synthesis={"endpoint_claim": "DRY-RUN — no live API call."},
        )

    try:
        client = _get_client()
    except RuntimeError as e:
        return ExtractionResult(error=str(e))

    result = ExtractionResult()
    try:
        result.methodologies, result.raw_grunt = _grunt_pass(survivors, client)
        log.info("Grunt pass: %d methodologies extracted", len(result.methodologies))
    except Exception as e:
        result.error = f"grunt: {e}"
        log.error("Grunt pass failed: %s", e)
        return result

    if result.methodologies:
        try:
            result.synthesis, result.raw_synthesis = _synthesis_pass(
                result.methodologies, topic, client
            )
            log.info("Synthesis pass complete")
        except Exception as e:
            log.warning("Synthesis pass failed: %s", e)
            result.synthesis = {"error": str(e)}

    return result
