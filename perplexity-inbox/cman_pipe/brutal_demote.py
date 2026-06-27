"""Brutal demote — deterministic Python filter on raw search results.

Drops homonym noise (dictionary pages, unrelated uses of the same word) and
scores survivors by methodology + topic relevance. No LLM, no heuristic guessing.

Step 1: URL/title block-list for known noise patterns (regex).
Step 2: Score each doc: methodology_keywords × 2 + topic_keywords.
Step 3: Drop score ≤ 0. Sort descending. Cap at max_survivors.

Signed-by: cascade-mac | 2026-06-27 | cman-research-pipe
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

# Methodology-signal keywords — these indicate a HOW, not a WHAT
_METHOD = re.compile(
    r'\b(methodology|pattern|approach|recipe|framework|step[s]?|phase[s]?'
    r'|pipeline|procedure|technique|protocol|workflow|how[- ]to|guideline'
    r'|best[- ]practice|playbook|template|instrument[a-z]*|implementation'
    r'|loop|cycle|iteration|feedback|continuous improvement|kaizen'
    r'|measurement|monitoring|tracing|observ[a-z]+|telemetry)\b',
    re.I,
)

# Topic adjacency keywords — domain-neutral signals of relevance
_TOPIC = re.compile(
    r'\b(autonomous|sensor|control|feedback|measurement|trace|span|metric[s]?'
    r'|monitor[a-z]*|signal|data[- ]collection|instrumentation|observ[a-z]+'
    r'|parameter|state|error[- ]rate|variation|reliability|incident'
    r'|SLO|SLA|error budget|flight|process control|historian|homeosta[a-z]+'
    r'|Ashby|Shewhart|cybernetics|distributed|propagation|decision loop)\b',
    re.I,
)

# Hard noise block — guaranteed irrelevant
_NOISE = re.compile(
    r'(cambridge\.org/dictionary|reverso\.net|wooordhunt|translate\.'
    r'|definition of |meaning of |wiktionary|thesaurus'
    r'|real madrid|premier league|betting|casino|samsung\.com'
    r'|volkswagen|google play|app store|windows \d+|xbox'
    r'|roblox|porn|chicken recipe|sewing pattern|mount rainier'
    r'|law school|LL\.M|johnny (?:sins|hallyday)'
    r'|breaking news|weather forecast|stock price)',
    re.I,
)


@dataclass
class ScoredDoc:
    title:   str
    url:     str
    snippet: str
    probe:   int
    score:   int
    domain:  str = ""

    @property
    def key(self) -> str:
        return hashlib.md5(self.url.encode()).hexdigest()[:10]


def demote(results: list[dict], *, max_survivors: int = 40) -> list[ScoredDoc]:
    """Filter and score raw search results. Returns survivors sorted by score."""
    seen_keys: set[str] = set()
    scored: list[ScoredDoc] = []

    for r in results:
        url     = r.get("url", "")
        title   = r.get("title", "")
        snippet = r.get("snippet", "")
        text    = f"{title} {url} {snippet}"

        # Dedup
        key = hashlib.md5(url.encode()).hexdigest()[:10]
        if key in seen_keys:
            continue
        seen_keys.add(key)

        # Hard noise block
        if _NOISE.search(text):
            continue

        m = len(_METHOD.findall(text))
        t = len(_TOPIC.findall(text))
        score = m * 2 + t

        if score <= 0:
            continue

        scored.append(ScoredDoc(
            title=title, url=url, snippet=snippet[:300],
            probe=r.get("probe", 0), score=score,
            domain=r.get("domain", ""),
        ))

    scored.sort(key=lambda d: -d.score)
    return scored[:max_survivors]


def summarise(survivors: list[ScoredDoc]) -> str:
    lines = [f"Brutal demote survivors: {len(survivors)}"]
    for d in survivors[:20]:
        lines.append(f"  [{d.score:2d}] {d.title[:70]}")
        lines.append(f"        {d.url[:70]}")
    return "\n".join(lines)
