"""
router.py — the routing surface + the safety gate.

Turns a Classification into a routed *action decision*. Every action is
decision-first: we compute what would happen and what tier it is, then only
perform it if (a) it is reversible/inbox-local (Tier A/B) AND (b) --apply is set.
Tier C actions (external send/publish/Drive/Beast-direct) are NEVER auto-run;
they are emitted as an action-request for a human.

The tier decision is delegated to the repo's existing doctrine module
amplified_permissions.classify() — one source of truth across all agents.
"""
from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .classifier import Classification
from .config import ROUTES, Route
from .servers.base import Email, InboxAdapter

# Import the repo doctrine module that the pre-commit gate also uses. It lives in
# the perplexity-inbox SSOT root (two levels up from this file's package).
_SSOT = Path(__file__).resolve().parent.parent
if str(_SSOT) not in sys.path:
    sys.path.insert(0, str(_SSOT))
amplified_permissions = importlib.import_module("amplified_permissions")

# label/archive are reversible inbox mutations the doctrine verb-map doesn't list;
# we pin them to Tier B (proxy-sign + log) explicitly, which is their honest tier.
_TIER_B_VERBS = {"label", "archive"}


@dataclass
class RoutedAction:
    msg_id: str
    inbox: str
    category: str
    route: str
    tier: str                  # 'A' | 'B' | 'C'
    allowed_without_human: bool
    mutates_inbox: bool
    performed: bool            # did we actually do it this run?
    gate: str | None           # human gate text if Tier C
    detail: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "msg_id": self.msg_id, "inbox": self.inbox, "category": self.category,
            "route": self.route, "tier": self.tier,
            "allowed_without_human": self.allowed_without_human,
            "mutates_inbox": self.mutates_inbox, "performed": self.performed,
            "gate": self.gate, "detail": self.detail,
        }


def _tier_for(route: Route) -> tuple[str, bool, str | None]:
    """(tier, allowed_without_human, gate_text) via the doctrine, with label/archive pinned to B."""
    if route.doctrine_verb in _TIER_B_VERBS:
        return "B", True, None
    d = amplified_permissions.classify(route.doctrine_verb)
    return d.tier, d.allowed, d.gate


def route_one(c: Classification, email: Email | None, adapter: InboxAdapter | None,
              apply: bool = False) -> RoutedAction:
    """Decide and (optionally) perform the action for one classification.

    apply=False  -> dry-run: nothing is mutated; performed=False everywhere.
    apply=True   -> Tier A/B actions are performed via the adapter and logged;
                    Tier C actions are STILL not performed (hard gate) — they are
                    surfaced as action-requests with their gate text.
    """
    route = ROUTES[c.category]
    tier, allowed, gate = _tier_for(route)
    detail: dict = {"description": route.description, "doctrine_verb": route.doctrine_verb}
    performed = False

    if apply and allowed and tier in ("A", "B"):
        if route.mutates_inbox and adapter is not None:
            from .servers.gmail_mcp import ROUTE_LABEL
            if route.name == "NOISE":
                detail["action"] = adapter.archive(c.msg_id)
            else:
                detail["action"] = adapter.apply_label(c.msg_id, ROUTE_LABEL.get(route.name, "EAA"))
            performed = bool(detail["action"].get("performed"))
        else:
            # Tier A inbox-local emit is handled by emit.py, not here; we just mark it routed.
            detail["action"] = {"op": "emit_jsonl", "sink": route.name, "performed": True}
            performed = True
    elif tier == "C":
        detail["action_request"] = {
            "op": route.doctrine_verb, "reason": gate,
            "note": "HARD GATE — requires explicit human authorisation; not auto-run.",
        }

    return RoutedAction(
        msg_id=c.msg_id, inbox=c.inbox, category=c.category, route=route.name,
        tier=tier, allowed_without_human=allowed, mutates_inbox=route.mutates_inbox,
        performed=performed, gate=gate, detail=detail,
    )


def route_all(classifications, emails_by_id, adapters_by_inbox, apply: bool = False) -> list[RoutedAction]:
    out: list[RoutedAction] = []
    for c in classifications:
        email = emails_by_id.get(c.msg_id)
        adapter = adapters_by_inbox.get(c.inbox)
        out.append(route_one(c, email, adapter, apply=apply))
    return out
