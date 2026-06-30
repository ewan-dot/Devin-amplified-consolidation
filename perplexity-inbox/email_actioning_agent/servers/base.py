"""
base.py — the inbox-adapter interface + the Email record.

An InboxAdapter is the code-execution-with-MCP boundary: callers ask it for
emails and (under --apply) ask it to action them. Bodies live here, in the
sandbox; only the structured result of classify/route crosses into model context.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Protocol


@dataclass
class Email:
    """A captured email. `body` is the full plaintext; it never has to enter
    model context — the classifier runs as code over it in the sandbox."""
    inbox: str                 # inbox key (config.Inbox.key)
    msg_id: str
    thread_id: str
    sender: str
    to: list[str]
    subject: str
    snippet: str
    body: str                  # full plaintext body
    label_ids: list[str] = field(default_factory=list)
    has_attachment: bool = False
    list_unsubscribe: bool = False     # List-Unsubscribe header present
    headers: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "Email":
        return cls(
            inbox=d.get("inbox", ""),
            msg_id=d["msg_id"],
            thread_id=d.get("thread_id", d["msg_id"]),
            sender=d.get("sender", ""),
            to=list(d.get("to", []) or []),
            subject=d.get("subject", ""),
            snippet=d.get("snippet", ""),
            body=d.get("body", "") or "",
            label_ids=list(d.get("label_ids", []) or []),
            has_attachment=bool(d.get("has_attachment", False)),
            list_unsubscribe=bool(d.get("list_unsubscribe", False)),
            headers=dict(d.get("headers", {}) or {}),
        )

    def to_dict(self) -> dict:
        return {
            "inbox": self.inbox, "msg_id": self.msg_id, "thread_id": self.thread_id,
            "sender": self.sender, "to": self.to, "subject": self.subject,
            "snippet": self.snippet, "body": self.body, "label_ids": self.label_ids,
            "has_attachment": self.has_attachment,
            "list_unsubscribe": self.list_unsubscribe, "headers": self.headers,
        }


class InboxAdapter(Protocol):
    """Uniform interface over an inbox. Read is always allowed; the mutating
    methods are only ever called by the router under --apply, after the doctrine
    gate (amplified_permissions) has authorised the action."""

    key: str

    def fetch(self, limit: int = 50) -> list[Email]: ...

    # Mutating actions — reversible, Tier B. Implementations should be no-ops
    # that record intent unless wired to a live MCP that can perform them.
    def apply_label(self, msg_id: str, label: str) -> dict: ...

    def archive(self, msg_id: str) -> dict: ...


class JsonlAdapter:
    """Reads captured real emails for one inbox from a JSONL file.

    This is the adapter used for the live measured demo: the model captures real
    mail into config.CAPTURE_JSONL once, and this reads it back — no mock data.
    Mutating methods are recorded-intent no-ops (the live demo defaults to
    dry-run; wiring them to the Gmail MCP is a documented go-live step)."""

    def __init__(self, key: str, jsonl_path: str | Path):
        self.key = key
        self.path = Path(jsonl_path)

    def fetch(self, limit: int = 50) -> list[Email]:
        if not self.path.exists():
            return []
        out: list[Email] = []
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                if d.get("inbox") and d["inbox"] != self.key:
                    continue
                out.append(Email.from_dict(d))
                if len(out) >= limit:
                    break
        return out

    def apply_label(self, msg_id: str, label: str) -> dict:
        return {"adapter": self.key, "op": "apply_label", "msg_id": msg_id,
                "label": label, "performed": False, "reason": "dry-run / not wired to live MCP"}

    def archive(self, msg_id: str) -> dict:
        return {"adapter": self.key, "op": "archive", "msg_id": msg_id,
                "performed": False, "reason": "dry-run / not wired to live MCP"}


def load_adapter(key: str, jsonl_path: str | Path) -> JsonlAdapter:
    """Factory. Today every inbox uses the JSONL-backed adapter over captured
    real mail. When a true in-sandbox MCP bridge exists, branch on the inbox's
    `adapter` field here and return a live adapter with the same interface."""
    return JsonlAdapter(key, jsonl_path)
