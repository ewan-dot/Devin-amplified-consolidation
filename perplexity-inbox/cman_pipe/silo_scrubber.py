"""Silo and pejorative language scrubber for research queries.

Strips domain-silo and pejorative terms from queries before they go to search.
The goal: escape the vocabulary barrier so cross-domain methodology equivalents
can be found. "Hallucination reduction" only finds AI papers. "Output error
rate reduction" finds aviation, medicine, manufacturing, and AI papers — the
same underlying methodology under different vocabulary.

This is NOT the ASPS PII scrubber (that lives in research_pipe.intake.asps_scrubber).
Concern: vocabulary normalisation. ASPS concern: PII removal. They compose.

Signed-by: cascade-mac | 2026-06-27 | cman-research-pipe
"""
from __future__ import annotations

import re

# (pattern, replacement) — order matters; longer/more-specific first
_RULES: list[tuple[re.Pattern[str], str]] = [
    # Pejorative AI terms
    (re.compile(r'\bhallucination[s]?\b', re.I), 'output error'),
    (re.compile(r'\bjailbreak(?:ing|s|ed)?\b', re.I), 'policy bypass'),
    (re.compile(r'\btoxic(?:ity)?\b', re.I), 'harmful output'),
    (re.compile(r'\bprompt injection\b', re.I), 'input manipulation'),
    (re.compile(r'\bsafety alignment\b', re.I), 'output constraint'),
    (re.compile(r'\bdebiasing\b', re.I), 'systematic error reduction'),
    # Silo model-name terms
    (re.compile(r'\bGPT-?[0-9o]+\b', re.I), 'language model'),
    (re.compile(r'\bChatGPT\b', re.I), 'language model'),
    (re.compile(r'\bClaude\b(?!\s+Code)', re.I), 'language model'),
    (re.compile(r'\bGemini\b', re.I), 'language model'),
    (re.compile(r'\bLlama[-\s]?[0-9]*\b', re.I), 'language model'),
    (re.compile(r'\bDeepSeek[-\s]?\w*\b', re.I), 'language model'),
    # Silo architecture terms (only when used as AI modifiers)
    (re.compile(r'\bLLM[s]?\b'), 'language model'),
    (re.compile(r'\bSLM[s]?\b'), 'language model'),
    (re.compile(r'\bRLHF\b'), 'reinforcement learning from feedback'),
    (re.compile(r'\bchain[- ]of[- ]thought\b', re.I), 'structured reasoning'),
    (re.compile(r'\bfine[- ]tun(?:ing|ed)\b', re.I), 'model adaptation'),
    # Silo agent/autonomy terms
    (re.compile(r'\bagentic\b', re.I), 'autonomous'),
    (re.compile(r'\bAI agent[s]?\b', re.I), 'autonomous system'),
    (re.compile(r'\bAI-native\b', re.I), 'autonomous-first'),
    # Keep "agent" alone — it's neutral in many domains (agent-based models, etc.)
    # Keep "AI" alone — too broad to replace; context disambiguates
]

# Collapse multiple spaces after replacements
_SPACE_COLLAPSE = re.compile(r'  +')


def scrub(query: str) -> str:
    """Return query with silo/pejorative terms replaced by neutral equivalents."""
    result = query
    for pattern, replacement in _RULES:
        result = pattern.sub(replacement, result)
    return _SPACE_COLLAPSE.sub(' ', result).strip()


def scrub_batch(queries: list[str]) -> list[str]:
    return [scrub(q) for q in queries]
