#!/usr/bin/env python3
"""Friction events against a frozen selection; propose registry deltas without promoting."""
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

from armamentarium_review import check_promotion
from fork_flow import load_yaml


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def record_friction(
    *,
    selection_manifest: dict[str, Any],
    aspect: str,
    observation: str,
    proposed_change: dict[str, Any],
    output: Path,
) -> dict[str, Any]:
    if not aspect.strip():
        raise ValueError("aspect: required")
    if not observation.strip():
        raise ValueError("observation: required")
    if not isinstance(proposed_change, dict) or not proposed_change:
        raise ValueError("proposed_change: required mapping")
    frozen = json.dumps(selection_manifest, sort_keys=True, separators=(",", ":"))
    event = {
        "schema_version": "armamentarium-friction/v1",
        "friction_id": str(uuid.uuid4()),
        "timestamp": utc_now(),
        "fork_id": selection_manifest.get("fork_id", ""),
        "selection_manifest_sha256": sha256_text(frozen),
        "aspect": aspect,
        "observation": observation,
        "proposed_change": proposed_change,
        "status": "proposed",
        "epistemic_tier": "INTUITED",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return event


def propose_registry_delta(
    registry: dict[str, Any],
    friction: dict[str, Any],
) -> dict[str, Any]:
    change = friction.get("proposed_change", {})
    if not isinstance(change, dict):
        raise ValueError("friction.proposed_change: expected mapping")
    action = change.get("action")
    if action not in {"add_hypothesis", "update_hypothesis_evidence", "replace_hypothesis"}:
        raise ValueError("proposed_change.action: unsupported")
    return {
        "schema_version": "armamentarium-registry-delta/v1",
        "friction_id": friction.get("friction_id"),
        "selection_manifest_sha256": friction.get("selection_manifest_sha256"),
        "action": action,
        "payload": change.get("payload", {}),
        "promotion_allowed": False,
        "note": "Promotion requires a local validation receipt plus a third-party review receipt.",
        "base_registry_sha256": sha256_text(json.dumps(registry, sort_keys=True, separators=(",", ":"))),
    }


def apply_delta_if_promotable(
    registry: dict[str, Any],
    delta: dict[str, Any],
    *,
    hypothesis_id: str,
    receipt: dict[str, Any],
    pack: Path,
    local_validation_receipt: Path,
) -> dict[str, Any]:
    if not local_validation_receipt.is_file():
        raise ValueError("local validation receipt missing; cannot promote")
    errors = check_promotion(registry, hypothesis_id, receipt, pack)
    if errors:
        raise ValueError("\n".join(errors))
    updated = json.loads(json.dumps(registry))
    payload = delta.get("payload", {})
    action = delta.get("action")
    if action == "add_hypothesis":
        if not isinstance(payload, dict):
            raise ValueError("payload: expected mapping")
        updated.setdefault("working_hypotheses", []).append(payload)
    elif action == "update_hypothesis_evidence":
        target = payload.get("id")
        pointers = payload.get("evidence_pointers", [])
        found = False
        for item in updated.get("working_hypotheses", []):
            if item.get("id") == target:
                item.setdefault("evidence_pointers", []).extend(pointers)
                found = True
                break
        if not found:
            raise ValueError(f"hypothesis not found for evidence update: {target}")
    elif action == "replace_hypothesis":
        old_id = payload.get("replaces")
        new_item = payload.get("hypothesis")
        if not isinstance(new_item, dict):
            raise ValueError("replace_hypothesis requires hypothesis mapping")
        kept = []
        replaced = False
        for item in updated.get("working_hypotheses", []):
            if item.get("id") == old_id:
                history = list(item.get("replacement_history", []))
                history.append(
                    {
                        "replaced_at": utc_now(),
                        "by": new_item.get("id"),
                        "friction_id": delta.get("friction_id"),
                    }
                )
                replacement = dict(new_item)
                replacement["replacement_history"] = history
                kept.append(replacement)
                replaced = True
            else:
                kept.append(item)
        if not replaced:
            raise ValueError(f"hypothesis not found to replace: {old_id}")
        updated["working_hypotheses"] = kept
    else:
        raise ValueError(f"unsupported action: {action}")
    for item in updated.get("working_hypotheses", []):
        if item.get("id") == hypothesis_id:
            item["role"] = "in_use"
            item["validation_status"] = "third_party_pass"
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Record armamentarium friction and proposed registry deltas.")
    commands = parser.add_subparsers(dest="command", required=True)
    friction_parser = commands.add_parser("record")
    friction_parser.add_argument("selection_manifest", type=Path)
    friction_parser.add_argument("--aspect", required=True)
    friction_parser.add_argument("--observation", required=True)
    friction_parser.add_argument("--proposed-change", type=Path, required=True)
    friction_parser.add_argument("--output", type=Path, required=True)
    delta_parser = commands.add_parser("propose-delta")
    delta_parser.add_argument("registry", type=Path)
    delta_parser.add_argument("friction_event", type=Path)
    delta_parser.add_argument("--output", type=Path, required=True)
    promote_parser = commands.add_parser("apply-if-promotable")
    promote_parser.add_argument("registry", type=Path)
    promote_parser.add_argument("delta", type=Path)
    promote_parser.add_argument("hypothesis_id")
    promote_parser.add_argument("receipt", type=Path)
    promote_parser.add_argument("pack", type=Path)
    promote_parser.add_argument("local_validation_receipt", type=Path)
    promote_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "record":
            change = load_yaml(args.proposed_change)
            manifest = json.loads(args.selection_manifest.read_text(encoding="utf-8"))
            event = record_friction(
                selection_manifest=manifest,
                aspect=args.aspect,
                observation=args.observation,
                proposed_change=change,
                output=args.output,
            )
            print(json.dumps(event, sort_keys=True))
            return 0
        if args.command == "propose-delta":
            friction_line = args.friction_event.read_text(encoding="utf-8").strip().splitlines()[-1]
            friction = json.loads(friction_line)
            delta = propose_registry_delta(load_yaml(args.registry), friction)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(yaml.safe_dump(delta, sort_keys=False), encoding="utf-8")
            print(f"PASS: wrote {args.output}")
            return 0
        updated = apply_delta_if_promotable(
            load_yaml(args.registry),
            load_yaml(args.delta),
            hypothesis_id=args.hypothesis_id,
            receipt=load_yaml(args.receipt),
            pack=args.pack,
            local_validation_receipt=args.local_validation_receipt,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(yaml.safe_dump(updated, sort_keys=False), encoding="utf-8")
        print(f"PASS: wrote {args.output}")
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
