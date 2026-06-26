"""
subscriptions.py — recurring-spend inventory + unused-subscription flags (deterministic).

Financial-control goal: from email alone (no bank link), find every recurring
charge and surface the ones likely UNUSED. No LLM in the path — keyword/regex
signals only; the ambiguous residue is left for `needs_ai`.

Output is a subscription ledger (one row per detected subscription email):
vendor, amount, currency, cadence, est_annual_cost, signal_type, unused_risk,
recommended_action. Aggregated into a real recurring-spend total.

Signal set is seeded from domain knowledge and reconciled with the prior-art
research brief (see perplexity-inbox/subscription-detection-prior-art*.md).
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass

from .extract import _MONEY
from .servers.base import Email

# Prior art (perplexity research, 2026-06-26): the MOST reliable deterministic
# signal when present is schema.org Invoice/Order JSON-LD embedded by the sender
# (Gmail markup). Most senders omit it, so it augments — never replaces — the
# keyword signals below. Coverage of "unused/wasteful from email alone" is
# commercially unaddressed, so the waste heuristics here are the novel part.
# See subscription-detection-prior-art__v01__2026-06-26.md for sources.

_JSONLD = re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.S | re.I)

# Category map for duplicate/overlapping-tool detection (the documented waste
# heuristic: 2+ vendors in one category = candidate overlap). Extend freely.
_CATEGORY = {
    "ai_coding_agent": ("cognition", "devin", "kilocode", "kilo", "cursor", "copilot",
                        "codeium", "windsurf", "factory", "augment"),
    "observability": ("sentry", "datadog", "grafana", "newrelic", "honeycomb"),
    "hosting_infra": ("railway", "render", "vercel", "fly.io", "hetzner", "heroku"),
    "meeting_notes": ("circleback", "otter", "fireflies", "fathom", "granola"),
    "email_client": ("superhuman", "shortwave"),
    "llm_api": ("openai", "anthropic", "x.ai", "mistral", "groq", "cohere"),
}


def parse_invoice_jsonld(html: str) -> dict | None:
    """Extract schema.org Invoice/Order fields from email HTML if present.
    Deterministic and authoritative when the sender embeds it (Gmail markup)."""
    if not html:
        return None
    for m in _JSONLD.finditer(html):
        try:
            data = json.loads(m.group(1).strip())
        except (ValueError, TypeError):
            continue
        items = data if isinstance(data, list) else [data]
        for d in items:
            if not isinstance(d, dict):
                continue
            t = str(d.get("@type", "")).lower()
            if t in ("invoice", "order"):
                total = d.get("totalPaymentDue") or d.get("total") or {}
                price = total.get("price") if isinstance(total, dict) else total
                return {
                    "provider": (d.get("provider") or {}).get("name") if isinstance(d.get("provider"), dict) else d.get("provider"),
                    "amount": price,
                    "currency": total.get("priceCurrency") if isinstance(total, dict) else None,
                    "billing_period": d.get("billingPeriod"),     # ISO-8601 e.g. P1M / P1Y
                    "payment_due": d.get("paymentDue") or d.get("scheduledPaymentDate"),
                    "payment_status": d.get("paymentStatus"),
                }
    return None


def category_of(vendor: str) -> str | None:
    v = (vendor or "").lower()
    for cat, vendors in _CATEGORY.items():
        if any(k in v for k in vendors):
            return cat
    return None


def canonical_vendor(vendor: str) -> str:
    """Collapse name variants to one token so 'Circleback' and 'circleback.ai'
    (or 'sentry.io' and 'md.getsentry.com') count as ONE vendor, not an overlap."""
    v = (vendor or "").lower()
    for vendors in _CATEGORY.values():
        for k in vendors:
            if k in v:
                return k
    return re.split(r"[@.\s]", v)[0] if v else v

# --- recurring-billing signals (is this a subscription at all?) -------------- #
_SUB_SIGNALS = (
    "subscription", "subscribe", "renew", "renewal", "auto-renew", "auto renew",
    "billing cycle", "recurring", "membership", "your plan", "current plan",
    "next payment", "next billing", "will be charged", "we charged", "payment received",
    "receipt", "monthly", "annual", "annually", "per month", "per year", "/mo", "/year",
    "billed monthly", "billed annually", "manage subscription", "manage your subscription",
)
# --- "unused / wasteful" signals (the cancel-candidate flags) ---------------- #
_WINBACK = ("we miss you", "come back", "we noticed you haven't", "haven't seen you",
            "your account is inactive", "inactive account", "reactivate", "still there?",
            "it's been a while", "we'd love to have you back")
_TRIAL = ("free trial", "trial ends", "trial will end", "trial is ending",
          "trial will convert", "trial period", "start your free", "your trial")
_PRICE_UP = ("price increase", "new price", "updating our prices", "price change",
             "pricing update", "we're raising", "increase to your")
_CANCEL = ("cancel your subscription", "subscription cancel", "subscription has been cancel",
           "final warning", "cancellation", "will be canceled", "will be cancelled")
_OVERDUE = ("unpaid", "overdue", "past due", "non payment", "nonpayment",
            "outstanding balance", "services blocked", "payment warning", "reminder as pdf")
# Failed charges are the strongest "maybe you don't need this" signal — a forgotten
# tool quietly failing to bill is a prime cancel candidate.
_PAYMENT_FAILED = ("payment failed", "failed payment", "payment was unsuccessful",
                   "was unsuccessful", "unsuccessful", "weren't able to charge",
                   "wasn't able to charge", "couldn't charge", "could not charge",
                   "update your payment", "charge for", "most recent payment failed")

_CADENCE = [
    ("annual", ("annual", "annually", "per year", "/year", "yearly", "/yr")),
    ("monthly", ("monthly", "per month", "/mo", "/month", "a month")),
    ("weekly", ("weekly", "per week", "/week")),
]
_DATE = re.compile(
    r"\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*"
    r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}"
    r"|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b", re.I)


@dataclass
class Subscription:
    msg_id: str
    inbox: str
    vendor: str
    amount: str | None
    currency: str | None
    cadence: str | None
    est_annual: float | None
    signal_type: str            # payment_failed | overdue | winback_dormant | trial_converting | price_increase | cancellation | receipt | renewal
    unused_risk: str            # low | medium | high
    recommended_action: str     # keep | review | cancel_candidate
    signals: list
    subject: str
    category: str | None = None      # for duplicate/overlapping-tool detection

    def to_dict(self) -> dict:
        return asdict(self)


_PROCESSORS = ("stripe.com", "paddle.com", "paypal", "chargebee", "recurly", "braintree")
_VENDOR_FROM_SUBJECT = [
    re.compile(r"payment to ([A-Z][\w.&' -]+?) (?:was|is|failed)", re.I),
    re.compile(r"receipt from ([A-Z][\w.&' -]+?)(?:\s*#|\s*$)", re.I),
    re.compile(r"your ([A-Z][\w.&' -]+?) subscription", re.I),
    re.compile(r"from ([A-Z][\w.&' -]+? (?:Inc|LLC|Ltd))", re.I),
]


def _hits(text, needles):
    return [n for n in needles if n in text]


def _vendor(email: Email) -> str:
    """Real vendor name. For payment-processor senders, recover the merchant from
    the subject ('payment to Circleback', 'receipt from Cognition AI Inc.')."""
    domain = email.sender.split("@")[-1] if "@" in email.sender else email.sender
    if any(p in domain for p in _PROCESSORS):
        for pat in _VENDOR_FROM_SUBJECT:
            m = pat.search(email.subject or "")
            if m:
                return m.group(1).strip()
    return domain


def _cadence(text) -> str | None:
    for name, kws in _CADENCE:
        if any(k in text for k in kws):
            return name
    return None


def _amount_currency(text):
    m = _MONEY.search(text)
    if not m:
        return None, None
    raw = m.group(0)
    cur = "GBP" if "£" in raw else "USD" if "$" in raw else "EUR" if "€" in raw else \
          next((c for c in ("GBP", "USD", "EUR") if c in raw.upper()), None)
    num = re.sub(r"[^\d.]", "", raw)
    return raw.strip(), cur


def _est_annual(amount_raw, cadence):
    if not amount_raw:
        return None
    num = re.sub(r"[^\d.]", "", amount_raw)
    try:
        v = float(num)
    except ValueError:
        return None
    mult = {"annual": 1, "monthly": 12, "weekly": 52}.get(cadence or "", None)
    return round(v * mult, 2) if mult else None


def detect(email: Email) -> Subscription | None:
    """Return a Subscription if this email is recurring-spend related, else None."""
    text = f"{email.subject}\n{email.body}".lower()

    winback = _hits(text, _WINBACK)
    trial = _hits(text, _TRIAL)
    price_up = _hits(text, _PRICE_UP)
    cancel = _hits(text, _CANCEL)
    overdue = _hits(text, _OVERDUE)
    failed = _hits(text, _PAYMENT_FAILED)
    core = _hits(text, _SUB_SIGNALS)

    # Gate: ANY recurring-spend signal qualifies (not just the core/overdue ones —
    # trial-ending and failed-payment mail are the most important unused signals).
    if not (core or overdue or failed or winback or trial or price_up or cancel):
        return None

    # signal_type precedence: the most action-relevant (and most likely-unused) wins
    if failed:
        signal_type, risk, action = "payment_failed", "high", "cancel_candidate"
    elif winback:
        signal_type, risk, action = "winback_dormant", "high", "cancel_candidate"
    elif overdue:
        signal_type, risk, action = "overdue", "high", "review"
    elif trial:
        signal_type, risk, action = "trial_converting", "high", "review"
    elif price_up:
        signal_type, risk, action = "price_increase", "medium", "review"
    elif cancel:
        signal_type, risk, action = "cancellation", "medium", "review"
    elif "receipt" in text or "payment received" in text or "we charged" in text:
        signal_type, risk, action = "receipt", "low", "keep"
    else:
        signal_type, risk, action = "renewal", "low", "keep"

    amount_raw, currency = _amount_currency(f"{email.subject}\n{email.body}")
    cadence = _cadence(text)
    signals = ([f"failed:{f}" for f in failed] + [f"winback:{w}" for w in winback] +
               [f"trial:{t}" for t in trial] + [f"price_up:{p}" for p in price_up] +
               [f"overdue:{o}" for o in overdue])
    return Subscription(
        msg_id=email.msg_id, inbox=email.inbox,
        vendor=_vendor(email),
        amount=amount_raw, currency=currency, cadence=cadence,
        est_annual=_est_annual(amount_raw, cadence),
        signal_type=signal_type, unused_risk=risk, recommended_action=action,
        signals=signals or ["recurring_signal"], subject=email.subject,
        category=category_of(_vendor(email)),
    )


def _amount_value(raw):
    if not raw:
        return None
    try:
        return float(re.sub(r"[^\d.]", "", raw))
    except ValueError:
        return None


def overlaps(subs) -> list[dict]:
    """Duplicate/overlapping-tool detection: 2+ distinct vendors in one category
    is a documented waste signal (you may be paying for redundant tools)."""
    by_cat: dict = {}
    for s in subs:
        if s.category:
            by_cat.setdefault(s.category, {})[canonical_vendor(s.vendor)] = s.vendor
    return [{"category": c, "vendors": sorted(set(v.values())),
             "note": "multiple distinct tools in one category — candidate overlap"}
            for c, v in by_cat.items() if len(v) > 1]


def ledger(emails) -> dict:
    """Build the recurring-spend inventory from a batch of emails."""
    subs = [s for s in (detect(e) for e in emails) if s is not None]
    cancel_candidates = [s for s in subs if s.recommended_action == "cancel_candidate"]
    review = [s for s in subs if s.recommended_action == "review"]
    known_annual = round(sum(s.est_annual for s in subs if s.est_annual), 2)
    # Sum of every charge we could read, regardless of cadence — "you are being
    # charged at least this much across these emails" (failed/receipt amounts count).
    charges = round(sum(v for v in (_amount_value(s.amount) for s in subs) if v), 2)
    return {
        "subscriptions_found": len(subs),
        "cancel_candidates": len(cancel_candidates),
        "review": len(review),
        "known_est_annual_spend": known_annual,
        "known_detected_charges_sum": charges,
        "overlaps": overlaps(subs),
        "currency_note": "amounts mix currencies (mostly USD/GBP); shown unconverted",
        "rows": [s.to_dict() for s in subs],
    }
