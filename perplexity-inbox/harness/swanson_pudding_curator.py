#!/usr/bin/env python3
"""Swanson LBD / Pudding Technique Curation Engine.

Scans the chunks directory, extracts metadata matching PUDDING_V1,
performs cross-domain semantic matching on B-term dimensions,
calculates Jaccard, Simple Recipe, and Pudding Candidate Scores,
and writes out structured hypothesis recipes.
"""
import os
import re
import yaml
import json
import hashlib
from datetime import date
from pathlib import Path
from typing import Dict, Any, List, Tuple, Set

try:
    from glasses_loader import extract_yaml_frontmatter, load_lens_glasses
except ImportError:
    # Fallback to local import or inline routines
    import sys
    sys.path.append(str(Path(__file__).resolve().parent))
    from glasses_loader import extract_yaml_frontmatter, load_lens_glasses

HARNESS_DIR = Path(__file__).resolve().parent
ROOT_DIR = HARNESS_DIR.parent
CHUNKS_DIR = HARNESS_DIR.parent / "chunks"


def walk_chunks_for_pudding() -> List[Dict[str, Any]]:
    """Recursively scans CHUNKS_DIR for all markdown/text files with PUDDING_V1 metadata."""
    pudding_records = []
    if not CHUNKS_DIR.exists():
        print(f"[CURATOR] Warning: Chunks directory does not exist: {CHUNKS_DIR}")
        return pudding_records

    # We walk the directory recursively to find all text/markdown files
    for root, _, files in os.walk(CHUNKS_DIR):
        for file in files:
            if not file.endswith((".txt", ".md")):
                continue
            path = Path(root) / file
            try:
                content = path.read_text(encoding="utf-8")
                # Try to load and validate as PUDDING_V1
                res = load_lens_glasses(content)
                if res.get("status") == "VALID" and res.get("schema_code") == "PUDDING_V1":
                    record = res["metadata"]
                    record["_file_path"] = str(path)
                    record["_body"] = res.get("body", "")
                    pudding_records.append(record)
            except Exception as e:
                # Log non-fatally
                print(f"[CURATOR] Error parsing {path.name}: {e}")
                
    return pudding_records


def calculate_scores(a: Dict[str, Any], c: Dict[str, Any]) -> Dict[str, Any]:
    """Calculates all math-spine scoring formulas for the A-B-C pair."""
    # Extracted dimensions (semantic dimensions)
    dims_a = set(a.get("semantic_dimensions") or a.get("dimensions") or [])
    dims_c = set(c.get("semantic_dimensions") or c.get("dimensions") or [])

    shared = dims_a.intersection(dims_c)
    unique_a = dims_a - shared
    unique_c = dims_c - shared
    union = dims_a.union(dims_c)

    # 1. Jaccard Set (F4)
    j_set = len(shared) / len(union) if union else 0.0

    # 2. Jaccard Slot (F3) - matches slots / 4
    matching_slots = len(shared)
    j_slot = matching_slots / 4.0

    # 3. Recipe Score Simple (F5) - viable >= 5, high >= 8
    e_simple = 2 * len(shared) + len(unique_a) + len(unique_c)

    # 4. Pattern Alignment (F8) - round(J_slot * 10) half-up
    pattern_align = int(j_slot * 10 + 0.5)

    # 5. Domain Distance
    exp_a = (a.get("expert") or "none").upper()
    exp_c = (c.get("expert") or "none").upper()
    dom_a = (a.get("domain") or "none").lower()
    dom_c = (c.get("domain") or "none").lower()

    if exp_a != exp_c and dom_a != dom_c:
        domain_dist = 6
    elif dom_a != dom_c:
        domain_dist = 4
    elif exp_a != exp_c:
        domain_dist = 2
    else:
        domain_dist = 1

    # 6. Gap Complementarity (GapComp)
    gap_comp = min(5, len(unique_a) + len(unique_c))

    # 7. Tension Bonus (TensionBonus)
    # Opposing experts or different dimensions trigger the bonus
    tension_bonus = 3 if exp_a != exp_c else 0

    # 8. Pudding Candidate Score (F7)
    s_candidate = (domain_dist * pattern_align) + gap_comp + tension_bonus

    return {
        "shared": list(shared),
        "unique_a": list(unique_a),
        "unique_c": list(unique_c),
        "j_set": j_set,
        "j_slot": j_slot,
        "e_simple": e_simple,
        "pattern_align": pattern_align,
        "domain_dist": domain_dist,
        "gap_comp": gap_comp,
        "tension_bonus": tension_bonus,
        "s_candidate": s_candidate
    }


def make_pudding_recipe(a: Dict[str, Any], c: Dict[str, Any], score_res: Dict[str, Any]) -> str:
    """Drafts the generated 1+1=3 hypothesis recipe with 20 frontmatter fields."""
    recipe_hash = hashlib.sha256(
        f"{a['id']}-{c['id']}-{sorted(score_res['shared'])}".encode("utf-8")
    ).hexdigest()[:8]

    # Target fields (exactly 20 fields)
    fm = {
        "schema_code": "PUDDING_V1",
        "id": f"RECIPE_HYPOTHESIS_{recipe_hash}",
        "title": f"Swanson LBD Recipe: {a['title']} x {c['title']}",
        "document_type": "recipe",
        "expert": "CLAUDE",
        "domain": a.get("domain", "none"),
        "semantic_dimensions": score_res["shared"],
        "actionable": "needs_adaptation",
        "status": "hypothesis",
        "pudding_score": score_res["s_candidate"],
        "created_at": date.today().isoformat(),
        "last_validated": date.today().isoformat(),
        "lbd_attribution": "Swanson (1986) ABC Model",
        "epistemic_tier": "INTUITED",
        "provenance_sources": [a["id"], c["id"]],
        "author": "antigravity",
        "bridge_candidates": score_res["shared"],
        "resolved_connections": [],
        "risk_flags": [],
        "canonical_summary": f"Swanson A-B-C connection bridging {a['title']} and {c['title']} via {', '.join(score_res['shared'])}."
    }

    # Generate body of the file
    body = f"""# Swanson A-B-C Recipe: {a['title']} x {c['title']}

## 1. The Core Alignment (A-B-C Mapping)

```
[A] {a['title']} ({a.get('expert', 'UNKNOWN')} / {a.get('domain', 'UNKNOWN')})
   │
   ▼
[B] Shared Bridge Mechanisms (B-Terms):
    • {chr(10).join(f"  - {b}" for b in score_res['shared'])}
   ▲
   │
[C] {c['title']} ({c.get('expert', 'UNKNOWN')} / {c.get('domain', 'UNKNOWN')})
```

---

## 2. Mathematical Scoring & Validation Metrics

*   **Pudding Candidate Score ($S$ - F7)**: **{score_res['s_candidate']}/68**
    *   *Formula*: $(DomainDist \\times PatternAlign) + GapComp + TensionBonus$
    *   *Calculated*: $({score_res['domain_dist']} \\times {score_res['pattern_align']}) + {score_res['gap_comp']} + {score_res['tension_bonus']} = {score_res['s_candidate']}$
*   **Simple Recipe Score ($E$ - F5)**: **{score_res['e_simple']}** (viable $\\ge 5$, high $\\ge 8$)
*   **Jaccard Set Similarity ($J_{{set}}$ - F4)**: **{score_res['j_set']:.2f}**
*   **Jaccard Slot Alignment ($J_{{slot}}$ - F3)**: **{score_res['j_slot']:.2f}** (matching slots: {len(score_res['shared'])}/4)

---

## 3. The 1+1=3 Emergent Insight

By applying the underlying mechanism **{', '.join(score_res['shared'])}** (which bridges these domains), we deduce a novel business synthesis:

> [!IMPORTANT]
> **Emergent Hypothesis**: Combining {a['title']}'s approach to {a.get('domain', 'A-domain')} and {c['title']}'s approach to {c.get('domain', 'C-domain')} reveals that {score_res['shared'][0] if score_res['shared'] else 'the bridge'} operates as a fundamental scaling constraint.

### Testable Prediction
If we implement the combined technique in client pilots, decision-making latency will drop, validating the hypothesis within 90 days.

---

## 4. Provenance & Sources
*   Source A: [{a['title']}]({a.get('_file_path')})
*   Source C: [{c['title']}]({c.get('_file_path')})
"""
    # Write out YAML frontmatter format
    fm_str = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    return f"---\n{fm_str}---\n\n{body}"


def run_curator() -> List[Dict[str, Any]]:
    """Runs the Swanson LBD Curator, executing matches and generating files."""
    print("=================================================================")
    print("[CURATOR] STARTING SWANSON LITERATURE-BASED DISCOVERY PIPELINE")
    print("=================================================================")
    
    records = walk_chunks_for_pudding()
    print(f"[CURATOR] Found {len(records)} PUDDING_V1 files in chunks database.")

    recipes_generated = []
    # Avoid duplicate combinations
    seen_pairs = set()

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            a = records[i]
            c = records[j]

            # Enforce cross-domain or cross-expert rules to find non-obvious connections
            exp_a = (a.get("expert") or "").upper()
            exp_c = (c.get("expert") or "").upper()
            dom_a = (a.get("domain") or "").lower()
            dom_c = (c.get("domain") or "").lower()

            if exp_a == exp_c and dom_a == dom_c:
                # Skip within-same-domain-and-expert connections (not Swanson linking)
                continue

            pair_key = tuple(sorted([a["id"], c["id"]]))
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)

            # Score the match
            score_res = calculate_scores(a, c)
            
            # Check Viability Thresholds: simple score E >= 5 OR candidate score S >= 13
            if score_res["e_simple"] >= 5 or score_res["s_candidate"] >= 13:
                recipe_content = make_pudding_recipe(a, c, score_res)
                
                # Write to CHUNKS_DIR/research/
                out_dir = CHUNKS_DIR / "research"
                out_dir.mkdir(parents=True, exist_ok=True)
                
                recipe_hash = hashlib.sha256(
                    f"{a['id']}-{c['id']}-{sorted(score_res['shared'])}".encode("utf-8")
                ).hexdigest()[:8]
                out_path = out_dir / f"HYPOTHESIS__recipe_{recipe_hash}_chunk_01.txt"
                
                out_path.write_text(recipe_content, encoding="utf-8")
                print(f"  ✓ Generated Swanson recipe hypothesis: '{out_path.name}' (Score S={score_res['s_candidate']})")
                recipes_generated.append({
                    "path": str(out_path),
                    "score": score_res["s_candidate"],
                    "sources": [a["id"], c["id"]]
                })

    print("-----------------------------------------------------------------")
    print(f"[CURATOR] PIPELINE COMPLETE. Generated {len(recipes_generated)} recipes.")
    print("=================================================================")
    return recipes_generated


if __name__ == "__main__":
    run_curator()
