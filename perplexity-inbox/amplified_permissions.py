"""
amplified_harness.py — deterministic hooks & harness for the Amplified doctrine.

Prose skills are canonical. This is their executable projection: pure, testable,
no LLM in the decision path. Both Perplexity (proxy) and the M5 local AIs read the
same amplified_rules.json so behaviour is identical across agents.

tier: STRUCTURED  (codified from INTUITED/STRUCTURED prose; not empirically calibrated)
generated_by: AI_PARTNER_PROXY  2026-06-24

Usage:
    from amplified_harness import classify, gate, closure_footer, ProxyLog
    d = classify("spend", amount_gbp=120)        # -> Decision(tier='C', ...)
    if d.allowed: ...                            # pre-act hook
    print(closure_footer(branch="ACTION", inbox="plan.md"))  # post-task hook
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

RULES_PATH = os.environ.get(
    "AMPLIFIED_RULES",
    str(Path(__file__).with_name("amplified_rules.json")),
)


def load_rules(path: str = RULES_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


_RULES = load_rules()

# Map concrete action verbs -> action_class used in the ladder. Extend as needed.
# An action verb that resolves to a research class is never gated.
ACTION_TO_CLASS = {
    # Tier A research / reversible
    "read": "read_any", "search": "search_any", "fetch": "research_any_depth",
    "analyse": "research_any_depth", "reason": "research_any_depth",
    "draft": "workspace_reversible", "conclude": "research_any_depth",
    "cite": "external_fetch_for_citation",
    "prove_hypothesis": "external_fetch_for_hypothesis_proof",
    "write_inbox": "write_artifact_to_inbox",
    # Tier B proxy
    "draft_pipe": "draft_into_pipe", "schedule": "schedule_task_normal_cadence",
    "file_issue": "file_tracker_item", "draft_pr": "draft_pr_or_branch",
    "draft_email": "outbound_draft_for_review",
    # Tier C act-out
    "spend": "spend_over_gate",  # refined by amount below
    "send": "send_or_post_or_publish_external_irreversible",
    "post": "send_or_post_or_publish_external_irreversible",
    "publish": "send_or_post_or_publish_external_irreversible",
    "deploy": "send_or_post_or_publish_external_irreversible",
    "beast_write": "beast_direct_write",
    "delete": "delete_or_overwrite_irreproducible",
}


@dataclass
class Decision:
    action: str
    action_class: str
    tier: str                      # 'A' | 'B' | 'C'
    allowed: bool                  # may the agent proceed without a human gate?
    requires_proxy_log: bool
    gate: Optional[str]            # human-readable gate if Tier C, else None
    reason: str


def classify(action: str, amount_gbp: float = 0.0) -> Decision:
    """Deterministic permission classifier. Pre-act hook entry point."""
    a = action.strip().lower()
    cls = ACTION_TO_CLASS.get(a, "UNKNOWN")

    # Beast direct write is forbidden absolutely, regardless of tier.
    if a == "beast_write":
        return Decision(a, "beast_direct_write", "C", False, False,
                        "FORBIDDEN: Beast writes go through the pipe only", "pipe discipline")

    # Spend is the one amount-dependent verb.
    if a == "spend":
        gate_amt = _RULES["constants"]["spend_gate_gbp"]
        if amount_gbp <= gate_amt:
            return Decision(a, "spend_at_or_under_gate_reversible", "B", True, True,
                            None, f"spend £{amount_gbp:g} <= £{gate_amt} gate, reversible")
        return Decision(a, "spend_over_gate", "C", False, False,
                        f"spend £{amount_gbp:g} approval", f"spend exceeds £{gate_amt} gate")

    ladder = _RULES["permission_ladder"]
    for tier_key, tier_letter in (("A_ACT_FREELY", "A"),
                                  ("B_PROXY_SIGN", "B"),
                                  ("C_ALWAYS_STOP", "C")):
        if cls in ladder[tier_key]["action_classes"]:
            if tier_letter == "A":
                return Decision(a, cls, "A", True, False, None, "research/reversible — free")
            if tier_letter == "B":
                return Decision(a, cls, "B", True, True, None, "proxy-sign and proceed, logged")
            return Decision(a, cls, "C", False, False, f"{cls} approval", "hard gate — halt for Ewan")

    # Unknown -> fail cautious (Tier C).
    return Decision(a, "UNKNOWN", "C", False, False, f"unknown action '{a}' approval",
                    "unrecognised action — defaulting cautious")


def gate(action: str, amount_gbp: float = 0.0) -> Optional[str]:
    """Returns the single human gate string if one applies, else None."""
    return classify(action, amount_gbp).gate


@dataclass
class ProxyLog:
    """Constitution-compliant proxy log entry: named signer + reason + timestamp."""
    action: str
    reason: str
    signer: str = "AI_PARTNER_PROXY"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


def closure_footer(branch: str, proxy: object = "none", gates: object = "none",
                   inbox: object = "none", tier: str = "STRUCTURED") -> str:
    """Post-task hook: emit the mandatory [CLOSURE] footer deterministically."""
    assert branch in ("ACTION", "PLAN"), "branch must be ACTION or PLAN"
    return (f"[CLOSURE] branch={branch} | proxy={proxy} | "
            f"gates={gates} | inbox={inbox} | tier={tier}")


def inbox_path() -> str:
    return _RULES["constants"]["inbox_path"]


# ---------------------------------------------------------------------------
# Self-test (deterministic). Run: python amplified_harness.py
# ---------------------------------------------------------------------------
def _selftest() -> int:
    checks = [
        (classify("read").tier == "A", "read is Tier A"),
        (classify("cite").tier == "A", "citation fetch is Tier A"),
        (classify("prove_hypothesis").tier == "A", "hypothesis-proof fetch is Tier A"),
        (classify("write_inbox").tier == "A", "writing to inbox is Tier A"),
        (classify("draft_pr").tier == "B", "draft PR is Tier B proxy"),
        (classify("draft_pr").requires_proxy_log is True, "Tier B requires proxy log"),
        (classify("spend", 40).tier == "B", "spend <= £50 is Tier B"),
        (classify("spend", 200).tier == "C", "spend > £50 is Tier C"),
        (classify("spend", 200).allowed is False, "spend > £50 not allowed"),
        (classify("send").tier == "C", "external send is Tier C"),
        (classify("beast_write").allowed is False, "beast write forbidden"),
        (classify("xyzzy").tier == "C", "unknown action fails cautious"),
        (gate("spend", 200) == "spend exceeds £50 gate" or "approval" in (gate("spend", 200) or ""),
         "spend gate string present"),
        (closure_footer("ACTION", inbox="plan.md").startswith("[CLOSURE] branch=ACTION"),
         "closure footer format"),
    ]
    ok = True
    for passed, label in checks:
        print(f"{'PASS' if passed else 'FAIL'}  {label}")
        ok = ok and passed
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
