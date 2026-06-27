"""
classifier.py — the classifier-as-code (deterministic, no LLM in the path).

Per the brief:
  - "write the classifier as code (not as a tool-loop)"
  - "Tier the work, not the prompt": bulk/low-stakes are classified from a
    1000-char truncation by cheap deterministic signals; high-stakes are flagged
    here and marked for full-body escalation to a stronger model downstream.

This module decides a *category* (one of config.ROUTES) and a *work tier*
(bulk | high_stakes) from signals only. It does NOT mutate anything.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .config import (AI_ACTION_ROUTES, BULK_TRUNCATE_CHARS, CONF_FLOOR,
                     HIGH_STAKES_ROUTES)
from .servers.base import Email

# --------------------------------------------------------------------------- #
# Signal vocabularies. Deterministic, auditable, easy to extend. Lowercased.
# --------------------------------------------------------------------------- #

# Strong signals are decisive for their category; weak signals only win if no
# stronger competing signal is present. Split this way so an unpaid-invoice email
# that merely mentions "postgres" routes FINANCIAL, while a real CI failure that
# mentions "invoice" in a footer still routes INFRA.
_FINANCIAL_STRONG = (
    "invoice", "unpaid", "overdue", "past due", "payment due", "non payment",
    "nonpayment", "receipt", "remittance", "amount due", "balance due",
)
_FINANCIAL_WEAK = ("payment", "billing", "subscription", "payout", "vat", "tax", "refund")
_FINANCIAL_SENDERS = ("stripe.com", "paypal", "quickbooks", "intuit", "gocardless",
                      "wise.com", "xero", "square")

_INFRA_STRONG = (
    "incident", "outage", "downtime", "deploy failed", "build failed", "ci failed",
    "pipeline failed", "run failed", "jobs have failed", "all jobs have failed",
    "restart loop", "disk full", "quota exceeded", "certificate expired", "503", "401",
)
_INFRA_WEAK = ("alert", "pagerduty", "datadog", "health check", "container",
               "postgres", "kubernetes", "deployment")
_INFRA_SENDERS = ("github.com", "datadoghq", "pagerduty", "sentry", "uptimerobot",
                  "betteruptime", "grafana", "vercel", "render.com")

# Research/source value — drives ATTRIBUTION (harvest into brain) vs NEWSLETTER.
_ATTRIBUTION_KW = (
    "ai agent", "agentic", "claude", "anthropic", "mcp", "model context protocol",
    "llm", "rag", "fine-tun", "token", "context engineering", "compound engineering",
    "research", "benchmark", "eval", "prompt", "open source", "system design",
)

_URGENT_KW = ("urgent", "asap", "action required", "deadline", "today",
              "please respond", "can you", "are you available", "quick question",
              "reminder", "overdue", "final notice")

_NEWSLETTER_SENDERS = ("substack.com", "mailchimp", "beehiiv", "ghost.io",
                       "convertkit", "buttondown", "campaign-archive")
_NOISE_SENDERS = ("noreply", "no-reply", "donotreply", "notifications@",
                  "marketing@", "promo", "deals@", "offers@")


@dataclass
class Classification:
    msg_id: str
    inbox: str
    category: str               # one of config.ROUTES
    work_tier: str              # "bulk" | "high_stakes"
    confidence: float           # 0..1, deterministic score
    signals: list[str] = field(default_factory=list)
    truncated_chars: int = 0    # how much body the bulk path actually looked at

    @property
    def resolution(self) -> str:
        """'deterministic' (zero model tokens) vs 'needs_ai' (the genuine residue)."""
        if self.confidence < CONF_FLOOR:
            return "needs_ai"
        if self.category in AI_ACTION_ROUTES:
            return "needs_ai"
        return "deterministic"

    @property
    def needs_ai(self) -> bool:
        return self.resolution == "needs_ai"

    @property
    def ai_reason(self) -> str | None:
        if self.confidence < CONF_FLOOR:
            return "low_confidence_triage"
        if self.category in AI_ACTION_ROUTES:
            return "action_needs_judgment_or_draft"
        return None

    def to_dict(self) -> dict:
        return {
            "msg_id": self.msg_id, "inbox": self.inbox, "category": self.category,
            "work_tier": self.work_tier, "confidence": round(self.confidence, 3),
            "signals": self.signals, "truncated_chars": self.truncated_chars,
            "resolution": self.resolution, "ai_reason": self.ai_reason,
        }


def _hits(haystack: str, needles) -> list[str]:
    """Word-boundary match (lowercased). Prevents substring false-positives such
    as 'vat' in 'avatar', '503' in a ticket number, or 'tax' in 'syntax'."""
    out = []
    for n in needles:
        if re.search(rf"(?<![a-z0-9]){re.escape(n)}(?![a-z0-9])", haystack):
            out.append(n)
    return out


def _sender_hits(sender: str, needles) -> list[str]:
    s = sender.lower()
    return [n for n in needles if n in s]      # senders are domains — substring is correct here


def classify(email: Email, truncate: int = BULK_TRUNCATE_CHARS) -> Classification:
    """Deterministic category + work-tier for one email.

    The bulk path reads only the first `truncate` chars of the body (the brief's
    token-saving move). High-stakes signals are detected from subject + sender +
    that same truncation; when present, work_tier escalates to 'high_stakes',
    which tells the downstream router/model to pull the FULL body.
    """
    subject = (email.subject or "").lower()
    sender = (email.sender or "").lower()
    body_full = email.body or ""
    body = body_full[:truncate].lower()
    text = f"{subject}\n{body}"

    is_list = email.list_unsubscribe or bool(_sender_hits(sender, _NEWSLETTER_SENDERS))
    is_noreply = bool(_sender_hits(sender, _NOISE_SENDERS))
    urgent = _hits(text, _URGENT_KW)

    infra_strong = _hits(text, _INFRA_STRONG)
    infra_weak = _hits(text, _INFRA_WEAK)
    infra_sender = _sender_hits(sender, _INFRA_SENDERS)
    fin_strong = _hits(text, _FINANCIAL_STRONG)
    fin_weak = _hits(text, _FINANCIAL_WEAK)
    fin_sender = _sender_hits(sender, _FINANCIAL_SENDERS)

    # Precedence ladder, most-decisive first:
    # 1. A real incident (strong infra signal) beats everything — even a billing footer.
    if infra_strong:
        sig = [f"infra:{x}" for x in infra_strong + infra_weak]
        return Classification(email.msg_id, email.inbox, "INFRA_CRITICAL",
                              "high_stakes", _score(len(infra_strong), strong=True), sig, len(body))

    # 2. A real money event (strong financial signal) beats infra *nouns* and sender heuristics.
    if fin_strong or fin_sender:
        sig = [f"financial:{x}" for x in fin_strong] + [f"sender:{h}" for h in fin_sender]
        return Classification(email.msg_id, email.inbox, "FINANCIAL",
                              "high_stakes", _score(len(fin_strong) + len(fin_sender), strong=True),
                              sig or ["financial:sender"], len(body))

    # 3. Transactional infra notification: infra noun, OR an infra-vendor sender that
    #    is NOT a marketing newsletter (newsletters have List-Unsubscribe).
    if infra_weak or (infra_sender and not is_list):
        sig = [f"infra:{x}" for x in infra_weak] + [f"sender:{h}" for h in infra_sender]
        return Classification(email.msg_id, email.inbox, "INFRA_CRITICAL",
                              "high_stakes", _score(len(infra_weak) + len(infra_sender)), sig, len(body))

    # 4. Weak financial cue (e.g. "billing", "subscription") with no stronger competitor.
    if fin_weak and not is_list:
        sig = [f"financial:{x}" for x in fin_weak]
        return Classification(email.msg_id, email.inbox, "FINANCIAL",
                              "high_stakes", _score(len(fin_weak)), sig, len(body))

    # Urgent human: not a list/no-reply, addressed to the user, urgency cues OR
    # simply a personal 1:1 message (short, human sender domain).
    if not is_list and not is_noreply and (urgent or _looks_personal(email)):
        signals = [f"urgent:{x}" for x in urgent] or ["personal-1:1"]
        return Classification(email.msg_id, email.inbox, "URGENT_HUMAN",
                              "high_stakes", _score(len(urgent) + 1),
                              signals, len(body))

    # ---- bulk / low-stakes ----
    attrib = _hits(text, _ATTRIBUTION_KW)
    if is_list and attrib:
        signals = ["list"] + [f"attrib:{x}" for x in attrib]
        return Classification(email.msg_id, email.inbox, "ATTRIBUTION",
                              "bulk", _score(len(attrib)), signals, len(body))

    if is_list:
        signals = ["list"] + [f"sender:{h}" for h in _sender_hits(sender, _NEWSLETTER_SENDERS)]
        return Classification(email.msg_id, email.inbox, "NEWSLETTER",
                              "bulk", _score(1), signals or ["list-unsubscribe"], len(body))

    if is_noreply:
        signals = [f"noise-sender:{h}" for h in _sender_hits(sender, _NOISE_SENDERS)]
        return Classification(email.msg_id, email.inbox, "NOISE",
                              "bulk", _score(1), signals, len(body))

    # Unknown low-stakes -> NOISE, but low confidence (router keeps it safe).
    return Classification(email.msg_id, email.inbox, "NOISE", "bulk", 0.25,
                          ["unmatched-default"], len(body))


def _looks_personal(email: Email) -> bool:
    """Heuristic: a free-mail or business human sender (not a bulk domain) and a
    short-ish body reads as a 1:1 message worth a human's attention."""
    sender = (email.sender or "").lower()
    bulky = _NEWSLETTER_SENDERS + _NOISE_SENDERS + ("substack",)
    if any(b in sender for b in bulky):
        return False
    # Plausible personal sender with a real name in the From line.
    has_name = bool(re.match(r"^[^@<]+<", email.sender or "")) or " " in (email.sender or "").split("@")[0]
    return has_name and len(email.body or "") < 4000


def _score(n_signals: int, strong: bool = False) -> float:
    base = 0.55 if strong else 0.4
    return min(1.0, base + 0.15 * n_signals)
