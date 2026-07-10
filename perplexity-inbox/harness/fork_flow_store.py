#!/usr/bin/env python3
"""Append-only fork/park event store and deterministic projections."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from fork_flow import load_yaml, validate_contract

STATE_TRANSITIONS = {
    "parked": {"claimed"},
    "claimed": {"running", "blocked"},
    "running": {"checked", "blocked"},
    "checked": {"used", "discarded", "blocked"},
    "blocked": {"claimed"},
    "used": set(),
    "discarded": set(),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_root() -> Path:
    return Path.home() / "amplified-pipeline" / "data" / "fork-flow"


def event_log(root: Path) -> Path:
    return root / "fork-events.jsonl"


def load_events(root: Path) -> list[dict[str, Any]]:
    path = event_log(root)
    if not path.is_file():
        return []
    events: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{number}: invalid JSON: {error}") from error
        if not isinstance(item, dict):
            raise ValueError(f"{path}:{number}: expected object")
        events.append(item)
    return events


def append_event(root: Path, event: dict[str, Any]) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    event = {
        "record_id": str(uuid.uuid4()),
        "timestamp": utc_now(),
        "schema_version": "fork-flow-event/v1",
        **event,
    }
    with event_log(root).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return event


def state_by_fork(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    states: dict[str, dict[str, Any]] = {}
    for event in events:
        fork_id = event.get("fork_id")
        if not isinstance(fork_id, str) or not fork_id:
            raise ValueError("event missing non-empty fork_id")
        if event.get("event") == "created":
            if fork_id in states:
                raise ValueError(f"duplicate create event for {fork_id}")
            states[fork_id] = dict(event)
            continue
        current = states.get(fork_id)
        if current is None:
            raise ValueError(f"event for unknown fork {fork_id}")
        current.update(event)
    return states


def require_existing_fork(root: Path, fork_id: str) -> dict[str, Any]:
    state = state_by_fork(load_events(root)).get(fork_id)
    if state is None:
        raise ValueError(f"unknown fork: {fork_id}")
    return state


def create(root: Path, contract_path: Path) -> dict[str, Any]:
    contract = load_yaml(contract_path)
    errors = validate_contract(contract, require_existing_paths=True)
    if errors:
        raise ValueError("\n".join(errors))
    fork_id = contract["fork_id"]
    if fork_id in state_by_fork(load_events(root)):
        raise ValueError(f"fork already exists: {fork_id}")
    return append_event(
        root,
        {
            "event": "created",
            "fork_id": fork_id,
            "state": "parked",
            "contract_path": str(contract_path.resolve()),
            "file_paths": contract["paths"],
            "owner": contract["ownership"],
            "review_status": "pending",
        },
    )


def transition(
    root: Path,
    fork_id: str,
    next_state: str,
    *,
    owner: str = "",
    verdict_path: str = "",
    review_receipt: str = "",
    reason: str = "",
) -> dict[str, Any]:
    current = require_existing_fork(root, fork_id)
    current_state = current.get("state")
    if next_state not in STATE_TRANSITIONS.get(current_state, set()):
        raise ValueError(f"invalid transition: {current_state} -> {next_state}")
    if next_state == "claimed" and not owner.strip():
        raise ValueError("claim requires an owner")
    if next_state in {"used", "discarded"}:
        if not verdict_path.strip() or not Path(verdict_path).is_file():
            raise ValueError("used/discarded requires an existing verdict_path")
    if review_receipt and not Path(review_receipt).is_file():
        raise ValueError("review_receipt does not resolve")
    event: dict[str, Any] = {
        "event": "transitioned",
        "fork_id": fork_id,
        "from_state": current_state,
        "state": next_state,
    }
    if owner:
        event["owner"] = owner
    if verdict_path:
        event["verdict_path"] = str(Path(verdict_path).resolve())
    if review_receipt:
        event["review_receipt"] = str(Path(review_receipt).resolve())
        event["review_status"] = "received"
    if reason:
        event["reason"] = reason
    return append_event(root, event)


def build_projection(root: Path) -> dict[str, Any]:
    states = state_by_fork(load_events(root))
    forks = []
    path_records = []
    for fork_id in sorted(states):
        state = states[fork_id]
        paths = {"contract": state.get("contract_path", ""), **state.get("file_paths", {})}
        forks.append(
            {
                "fork_id": fork_id,
                "state": state["state"],
                "owner": state.get("owner", {}),
                "contract": state.get("contract_path", ""),
                "file_paths": paths,
                "verdict_path": state.get("verdict_path", ""),
                "review_status": state.get("review_status", "pending"),
                "review_receipt": state.get("review_receipt", ""),
            }
        )
        for label, value in paths.items():
            if isinstance(value, str) and value:
                path_records.append(
                    {
                        "atom_id": hashlib.sha256(f"{fork_id}:{label}:{value}".encode()).hexdigest(),
                        "value_type": "FILE_PATH",
                        "fork_id": fork_id,
                        "label": label,
                        "content": value,
                        "epistemic_tier": "INTUITED",
                    }
                )
    return {"schema_version": "fork-park-index/v1", "forks": forks, "file_path_atoms": path_records}


def write_projection(root: Path, output: Path) -> None:
    projection = build_projection(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        yaml.safe_dump(
            {"schema_version": projection["schema_version"], "forks": projection["forks"]},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    atoms_path = output.with_suffix(".file-path-atoms.jsonl")
    atoms_path.write_text(
        "".join(json.dumps(item, sort_keys=True) + "\n" for item in projection["file_path_atoms"]),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Store and project fork-flow lifecycle events.")
    parser.add_argument("--root", type=Path, default=default_root())
    commands = parser.add_subparsers(dest="command", required=True)
    create_parser = commands.add_parser("create")
    create_parser.add_argument("contract", type=Path)
    claim_parser = commands.add_parser("claim")
    claim_parser.add_argument("fork_id")
    claim_parser.add_argument("--owner", required=True)
    transition_parser = commands.add_parser("transition")
    transition_parser.add_argument("fork_id")
    transition_parser.add_argument("state", choices=sorted(STATE_TRANSITIONS))
    transition_parser.add_argument("--verdict-path", default="")
    transition_parser.add_argument("--review-receipt", default="")
    transition_parser.add_argument("--reason", default="")
    rebuild_parser = commands.add_parser("rebuild-index")
    rebuild_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "create":
            result = create(args.root, args.contract)
        elif args.command == "claim":
            result = transition(args.root, args.fork_id, "claimed", owner=args.owner)
        elif args.command == "transition":
            result = transition(
                args.root,
                args.fork_id,
                args.state,
                verdict_path=args.verdict_path,
                review_receipt=args.review_receipt,
                reason=args.reason,
            )
        else:
            write_projection(args.root, args.output)
            print(f"PASS: wrote {args.output}")
            return 0
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
