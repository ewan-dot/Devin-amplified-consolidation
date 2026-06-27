"""CMAN anchor generator — topic → 8 founding-discipline probe strings.

Uses DeepSeek V4 (grunt tier) with a static, byte-stable system prompt so
DeepSeek's disk-based prefix cache hits on every call after the first.

Each anchor is:
  - From a genuinely different founding discipline
  - Written in THAT discipline's own vocabulary (not crossed with the target topic)
  - Free of silo and pejorative terms
  - A raw probe string (nouns from primary sources, not AI synthesis prose)

The cross-domain connection is made at Swanson-combine time, not at search time.

Signed-by: cascade-mac | 2026-06-27 | cman-research-pipe
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from cman_pipe.silo_scrubber import scrub

# ── DeepSeek config ──────────────────────────────────────────────────────────

_DEEPSEEK_MODEL   = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
_DEEPSEEK_BASE    = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
_DEEPSEEK_KEY     = os.environ.get("DEEPSEEK_API_KEY", "")

# ── Static, byte-stable system prompt (never interpolate; cache hits depend on it) ──

_SYSTEM = """\
You are a cross-domain research anchor generator applying the CMAN methodology
(Convergent Multi-Anchor Narrowing — Amplified Partners, 2026).

Your job: given a research topic, identify EIGHT founding disciplines that each
carry the same underlying concept but use completely different vocabulary.

Rules:
1. Each anchor must be from a GENUINELY different domain (aviation, medicine,
   manufacturing, cybernetics, ecology, law, military, etc.).
2. Each anchor query must use THAT discipline's own technical vocabulary — NOT
   the target topic's terminology. The cross-domain link is made at synthesis
   time, not at search time.
3. Strip ALL silo terms (LLM, GPT, AI agent, agentic, hallucination, RLHF,
   chain-of-thought, fine-tuning, prompt injection) from every anchor query.
   Use neutral equivalents: "output error", "language model", "autonomous system",
   "structured reasoning", "model adaptation", "input manipulation".
4. Each anchor must be a compact search probe string: 6–12 words, noun-heavy,
   from primary source vocabulary, NOT a synthesis summary.
5. Anchors must be INDEPENDENT — each must reach the concept from a different
   angle, so convergence is meaningful.

Output JSON only — no prose, no markdown fences:
{
  "anchors": [
    {"domain": "<discipline name>", "query": "<probe string>", "rationale": "<one sentence why this domain carries the concept>"},
    ...
  ]
}
"""

# ── Fallback: deterministic anchors for common topics (no API call needed) ──

_DETERMINISTIC: dict[str, list[dict]] = {
    "telemetry": [
        {"domain": "Aviation / flight safety",       "query": "flight data recorder parameter capture mishap investigation feedback loop"},
        {"domain": "Industrial process control",     "query": "process control sensor historian continuous measurement kaizen improvement SCADA"},
        {"domain": "Cybernetics",                    "query": "Ashby requisite variety feedback loop measurement homeostatic control system"},
        {"domain": "Site reliability engineering",   "query": "SLO error budget measurement production feedback continuous improvement"},
        {"domain": "Medicine / critical care",       "query": "patient telemetry vital signs continuous monitoring clinical decision loop"},
        {"domain": "Statistical process control",    "query": "Shewhart control chart measurement variation reduction process improvement"},
        {"domain": "Distributed systems tracing",    "query": "distributed trace span context propagation instrumentation vendor-neutral observability"},
        {"domain": "Autonomous robotics",            "query": "sensor fusion state estimation control loop measurement autonomous system"},
    ],
}


def _keyword_match(topic: str) -> list[dict] | None:
    """Return deterministic anchors if topic matches a known key."""
    tl = topic.lower()
    for key, anchors in _DETERMINISTIC.items():
        if key in tl:
            return anchors
    return None


def generate(topic: str, *, live: bool = True) -> list[dict]:
    """Generate 8 CMAN anchors for topic.

    Returns list of dicts: [{domain, query, rationale}, ...]
    Each query is silo-scrubbed before return.

    live=False: skip API call, use deterministic fallback (dry-run / testing).
    """
    # Deterministic shortcut
    if not live:
        anchors = _keyword_match(topic) or _make_generic_fallback(topic)
        return [{**a, "query": scrub(a["query"])} for a in anchors]

    # Try DeepSeek
    key = _DEEPSEEK_KEY or _load_key_from_env_file()
    if not key:
        anchors = _keyword_match(topic) or _make_generic_fallback(topic)
        return [{**a, "query": scrub(a["query"])} for a in anchors]

    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url=_DEEPSEEK_BASE)
        resp = client.chat.completions.create(
            model=_DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user",   "content": f"Topic: {topic}"},
            ],
            temperature=0.3,
            max_tokens=1024,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        data = json.loads(raw)
        anchors = data.get("anchors", [])
        if len(anchors) >= 4:
            return [{**a, "query": scrub(a.get("query", ""))} for a in anchors[:8]]
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning("DeepSeek anchor call failed: %s", exc)

    # Fallback on any failure
    anchors = _keyword_match(topic) or _make_generic_fallback(topic)
    return [{**a, "query": scrub(a["query"])} for a in anchors]


def _load_key_from_env_file() -> str:
    """Try to load DEEPSEEK_API_KEY from the clean-build .env file."""
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


def _make_generic_fallback(topic: str) -> list[dict]:
    """Minimal deterministic anchors when topic is unrecognised."""
    return [
        {"domain": "Aviation",           "query": f"flight data recorder parameter capture feedback loop",        "rationale": "Aviation uses continuous data capture for incident investigation"},
        {"domain": "Industrial control", "query": f"process historian sensor measurement improvement loop",        "rationale": "Process control uses historians for continuous improvement"},
        {"domain": "Medicine",           "query": f"vital signs monitoring clinical decision feedback",            "rationale": "Medicine uses continuous monitoring for intervention decisions"},
        {"domain": "SRE",                "query": f"SLO error budget measurement production feedback",             "rationale": "SRE uses measurement budgets to drive improvement"},
        {"domain": "Cybernetics",        "query": f"Ashby feedback loop measurement homeostatic control",         "rationale": "Cybernetics is the founding science of measurement-driven control"},
        {"domain": "Statistics",         "query": f"Shewhart control chart variation measurement improvement",     "rationale": "Statistical process control is the root of quality measurement"},
        {"domain": "Distributed systems","query": f"trace span propagation instrumentation vendor-neutral",       "rationale": "Distributed tracing is the software engineering equivalent"},
        {"domain": "Robotics",           "query": f"sensor fusion state estimation autonomous control loop",      "rationale": "Robotics uses sensor fusion for autonomous decision loops"},
    ]
