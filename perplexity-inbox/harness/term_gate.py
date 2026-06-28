#!/usr/bin/env python3
"""Terminology Alignment Gate (AI-Facing Disambiguation Algorithm).

Translates Ewan's imprecise human terminology into precise database/code targets,
resolving ambiguities by posing non-technical, context-based questions to determine
intent without exposing raw database names or technical terminology to the user.
"""
import re
import sys
import json
from typing import Any, Dict, List, Tuple

# SSOT Naming Mapping for the Estate
TERM_MAP = {
    "brain": {
        "canonical_db": "amplified_brain",
        "graph_namespace": "business_brain",
        "description": "The main Business Brain repository containing 89k nodes.",
        "regex": r"\b(the\s+)?brain\b|\bbusiness\s*brain\b"
    },
    "cove": {
        "canonical_db": "cove",
        "graph_namespace": None,
        "description": "The orchestrator database housing runs, schedules, and prompts.",
        "regex": r"\bcove\b|\borchestrator\b"
    },
    "vellum": {
        "canonical_db": "vellum",
        "graph_namespace": None,
        "description": "The hash-chained security and state ledger.",
        "regex": r"\bvellum\b|\bledger\b|\bbaton\b"
    },
    "crm": {
        "canonical_db": "amplified_crm",
        "graph_namespace": None,
        "description": "The client relationship database.",
        "regex": r"\bcrm\b|\bcontacts\b|\bdeals\b"
    },
    "beast": {
        "host": "Beast (Hetzner server)",
        "ports": "5433 (Postgres), 11435 (Ollama embedding), 11436 (Ollama complete)",
        "description": "The primary hardware host on AX-162-R.",
        "regex": r"\bbeast\b|\bserver\b"
    },
    "m5": {
        "host": "Mac Mini (M5)",
        "description": "Local development and test run machine.",
        "regex": r"\bm5\b|\bmini\b|\bmac\s*mini\b"
    }
}


def analyze_text(text: str) -> List[Tuple[str, Dict[str, Any]]]:
    """Scans instruction text for taxonomy matches."""
    matches = []
    text_lower = text.lower()
    for key, data in TERM_MAP.items():
        if re.search(data["regex"], text_lower):
            matches.append((key, data))
    return matches


def check_for_ambiguity(text: str) -> Tuple[bool, List[str], str]:
    """Detects dangerous or ambiguous naming overlaps in instructions."""
    text_lower = text.lower()
    warnings = []
    remedy = ""

    # Ambiguity 1: "cove-postgres" reference
    if "cove-postgres" in text_lower:
        warnings.append(
            "Target 'cove-postgres' refers to the CONTAINER on Beast. "
            "It hosts multiple separate databases (amplified_brain, cove, vellum)."
        )
        remedy = "Deduce target based on context (subject matter and target environment)."

    # Ambiguity 2: "cove" database vs "brain" data write
    if "cove" in text_lower and ("brain" in text_lower or "graph" in text_lower or "node" in text_lower):
        warnings.append(
            "Instruction mentions 'cove' and 'brain/graph' in the same context. "
            "The Business Brain graph belongs in 'amplified_brain', NOT the orchestrator DB 'cove'."
        )
        remedy = "Determine whether the subject is client knowledge or orchestrator state."

    return len(warnings) > 0, warnings, remedy


def get_context_diagnostic() -> List[Dict[str, Any]]:
    """Returns the sequence of non-technical context questions to determine intent."""
    return [
        {
            "id": "subject_domain",
            "question": "What is the subject matter of the data you want to interact with?",
            "options": {
                "1": "Client intelligence, company information, research findings, or entity relationships. [Maps to: amplified_brain]",
                "2": "Agent execution runs, system prompts, background tasks, or Temporal schedules. [Maps to: cove]",
                "3": "Security sheets, agent signature keys, handoff batons, or audit ledgers. [Maps to: vellum]",
                "4": "CRM contacts, prospective companies, or pipeline deal metrics. [Maps to: amplified_crm]"
            }
        },
        {
            "id": "target_env",
            "question": "Where should this action be executed?",
            "options": {
                "1": "Live on the primary Beast server. [Maps to: Beast]",
                "2": "Locally on the Mac Mini developer machine. [Maps to: Mac Mini]"
            }
        },
        {
            "id": "op_type",
            "question": "What is the nature of the operation?",
            "options": {
                "1": "Read-only audit, search, query, or check. [Safe path]",
                "2": "Write, edit, delete, insert, or database schema migration. [Requires Guard Harness]"
            }
        }
    ]


def run_interactive_alignment(text: str) -> Dict[str, Any]:
    """Runs the AI-facing algorithm to parse, align, and confirm targets."""
    print("\n" + "="*70, file=sys.stderr)
    print("[TERM GATE] RUNNING TERMINOLOGY ALIGNMENT ALGORITHM", file=sys.stderr)
    print("="*70, file=sys.stderr)
    print(f"Human Instruction: \"{text}\"", file=sys.stderr)
    print("-"*70, file=sys.stderr)

    matches = analyze_text(text)
    is_ambiguous, warnings, remedy = check_for_ambiguity(text)

    if matches:
        print("\nIdentified Infrastructure Anchors:", file=sys.stderr)
        for key, data in matches:
            target_str = data.get("canonical_db") or data.get("host")
            print(f"  • '{key}' mapped to technical target: '{target_str}'", file=sys.stderr)
            print(f"    Role: {data['description']}", file=sys.stderr)

    if is_ambiguous:
        print("\n!!! AMBIGUITY DETECTED !!!", file=sys.stderr)
        for w in warnings:
            print(f"  ⚠️  Warning: {w}", file=sys.stderr)
        print(f"  🧭 Remedy: {remedy}", file=sys.stderr)
        
        print("\n--- CONTEXT RESOLUTION PATHWAYS (Max 5 Questions) ---", file=sys.stderr)
        questions = get_context_diagnostic()
        for idx, q in enumerate(questions, 1):
            print(f"\n{idx}. {q['question']}", file=sys.stderr)
            for opt_key, opt_val in q['options'].items():
                print(f"   [{opt_key}] {opt_val}", file=sys.stderr)
        print("-"*70 + "\n", file=sys.stderr)

        return {
            "status": "AMBIGUOUS",
            "warnings": warnings,
            "remedy": remedy,
            "matches": [m[0] for m in matches],
            "context_questions": questions
        }
    
    print("\n✓ No ambiguity detected. Taxonomy targets aligned.", file=sys.stderr)
    print("="*70 + "\n", file=sys.stderr)
    
    return {
        "status": "ALIGNED",
        "matches": [m[0] for m in matches]
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        instr = " ".join(sys.argv[1:])
        res = run_interactive_alignment(instr)
        print(json.dumps(res, indent=2) if "json" in sys.argv else "")
    else:
        # Default dry-run test cases
        run_interactive_alignment("write the test nodes to cove-postgres")
