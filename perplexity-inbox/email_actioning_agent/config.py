"""
config.py — declarative configuration for the email-actioning agent.

Single source of truth for: the inboxes we track, the routing surface, and the
paths we emit to. No behaviour here — just data the rest of the package reads.

tier: STRUCTURED
origin: perplexity-thread brief "Claude as token-efficient email-actioning system"
        (perplexity-inbox/claude-gmail-brief.md, 2026-06-26)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------- #
# Inboxes — the multi-inbox set Ewan asked us to track (2026-06-26).
# `amplifiedpartyners` in chat was read as a typo for `amplifiedpartners`.
# One adapter (servers/) is stood up per inbox. `authed` reflects whether a
# live MCP connection currently exists; unauthed inboxes are configured and
# ready (see checklists/CHECKLIST-multi-inbox-auth.md) but never faked.
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Inbox:
    key: str
    address: str
    adapter: str           # adapter module under email_actioning_agent/servers/
    authed: bool           # is there a live MCP connection right now?
    note: str = ""


INBOXES: tuple[Inbox, ...] = (
    Inbox(
        key="byker",
        address="ewan@bykerbusinesshelp.ai",
        adapter="gmail_mcp",
        authed=True,
        note="Primary inbox — connected Gmail MCP authenticates this account.",
    ),
    Inbox(
        key="amplified",
        address="ewan@amplifiedpartners.ai",
        adapter="gmail_mcp",
        authed=False,
        note="Needs Gmail OAuth (user-granted). Adapter ready; capture deferred.",
    ),
    Inbox(
        key="gmail",
        address="ewanbramley@gmail.com",
        adapter="gmail_mcp",
        authed=False,
        note="Needs Gmail OAuth (user-granted). Adapter ready; capture deferred.",
    ),
)


def inbox_by_key(key: str) -> Inbox:
    for ib in INBOXES:
        if ib.key == key:
            return ib
    raise KeyError(f"unknown inbox key: {key!r}")


def authed_inboxes() -> tuple[Inbox, ...]:
    return tuple(ib for ib in INBOXES if ib.authed)


# --------------------------------------------------------------------------- #
# Routing surface — verbatim from the brief, each mapped to:
#   - the doctrine action verb (amplified_permissions.classify) that represents
#     its most-consequential side effect, which decides the Tier/gate, and
#   - whether the route mutates the live inbox (label/archive).
# Tier A = act freely (reversible / inbox-local writes)
# Tier B = proxy-sign + log (reversible live mutation, runs only under --apply)
# Tier C = HARD GATE (external send / publish / Drive / Beast direct) — never
#          auto-executed; emitted as an action-request for a human.
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Route:
    name: str
    description: str
    doctrine_verb: str     # fed to amplified_permissions.classify()
    mutates_inbox: bool    # does fulfilling this label/archive the source msg?


ROUTES: dict[str, Route] = {
    "INFRA_CRITICAL": Route(
        "INFRA_CRITICAL",
        "extract -> JSONL -> Beast ingestion pipe (via perplexity-inbox, never direct)",
        doctrine_verb="write_inbox",       # Tier A: local JSONL emit; pipe does Beast write
        mutates_inbox=False,
    ),
    "FINANCIAL": Route(
        "FINANCIAL",
        "attachment -> Drive + row -> ledger + notify",
        doctrine_verb="send",              # Tier C: Drive write + outbound notify = gated
        mutates_inbox=False,
    ),
    "ATTRIBUTION": Route(
        "ATTRIBUTION",
        "content-harvester -> brain (via staging, never side-door)",
        doctrine_verb="write_inbox",       # Tier A: local harvest JSONL; pipe stages to brain
        mutates_inbox=False,
    ),
    "URGENT_HUMAN": Route(
        "URGENT_HUMAN",
        "Telegram/Slack push to Ewan",
        doctrine_verb="send",              # Tier C: outbound notification = gated
        mutates_inbox=False,
    ),
    "NEWSLETTER": Route(
        "NEWSLETTER",
        "digest label, no model spend after classification",
        doctrine_verb="label",             # Tier B (see router): reversible inbox mutation
        mutates_inbox=True,
    ),
    "NOISE": Route(
        "NOISE",
        "archive, no further spend",
        doctrine_verb="archive",           # Tier B (see router): reversible inbox mutation
        mutates_inbox=True,
    ),
}


# --------------------------------------------------------------------------- #
# Tiering of the *work* (not the prompt), per the brief:
#   - bulk classification -> truncate to BULK_TRUNCATE_CHARS, cheap/deterministic
#   - high-stakes -> full body, escalate to a stronger model downstream
# --------------------------------------------------------------------------- #

BULK_TRUNCATE_CHARS = 1000            # brief: "1000-char truncation"
HIGH_STAKES_ROUTES = frozenset({"INFRA_CRITICAL", "FINANCIAL", "URGENT_HUMAN"})

# --------------------------------------------------------------------------- #
# Determinism boundary — "if it can be done deterministically, it should be."
# An email consumes ZERO model tokens unless it is in the `needs_ai` residue:
#   - confidence below CONF_FLOOR (genuinely ambiguous; AI disambiguates), or
#   - its route's ACTION needs semantic judgment/drafting (AI_ACTION_ROUTES).
# Everything else (classify -> extract -> label/archive/emit) is mechanical and
# is resolved entirely by deterministic code. This is what frees AI for the work
# only AI can do.
# --------------------------------------------------------------------------- #
CONF_FLOOR = 0.35                                  # below this -> needs_ai triage
AI_ACTION_ROUTES = frozenset({"URGENT_HUMAN"})     # action = judge/draft -> needs AI


# --------------------------------------------------------------------------- #
# Paths — all relative to the perplexity-inbox SSOT this package lives in.
# --------------------------------------------------------------------------- #

PKG_DIR = Path(__file__).resolve().parent
INBOX_SSOT = PKG_DIR.parent                       # perplexity-inbox/
DATA_DIR = PKG_DIR / "data"                       # captured real mail + emitted JSONL
CAPTURE_JSONL = DATA_DIR / "captured_emails.jsonl"        # real fetched emails (gitignored)
ROUTED_JSONL = DATA_DIR / "routed_actions.jsonl"         # decisions + gated actions (gitignored)
INFRA_FEED_JSONL = INBOX_SSOT / "infra-critical-feed.jsonl"   # INFRA_CRITICAL sink into the inbox
MEASUREMENT_JSON = DATA_DIR / "token_measurement.json"   # real token numbers
TELEMETRY_JSONL = DATA_DIR / "telemetry.jsonl"           # append-only run witness (local fallback)
HEALTH_JSON = DATA_DIR / "health.json"                   # latest health snapshot (read by `health`)

# Night Scout feed — canonical sink is Beast APDS staging (not on M5); we mirror
# locally and document the deferred Beast path. See night_scout.py.
NIGHT_SCOUT_FEED_DIR = INBOX_SSOT / "night-scout-feed"
BEAST_APDS_STAGING = "/opt/amplified-machine/apds/staging/"   # canonical, Beast-only, deferred
