#!/usr/bin/env python3
"""Deterministic fork-contract validator and armamentarium resolver.

This is a narrow pathway: it checks contract shape and explicit selections. It
does not decide whether a working hypothesis is true or ready for promotion.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

CONTRACT_ROLES = {"investigating", "in_use"}
FORK_STATES = {"parked", "claimed", "running", "checked", "used", "discarded", "blocked"}
REQUIRED_CONTRACT_FIELDS = (
    "schema_version",
    "fork_id",
    "parent_job",
    "discovery_trigger",
    "working_hypothesis",
    "goals",
    "ownership",
    "paths",
    "file_scope",
    "checkpoints",
    "validation",
    "return",
    "armamentarium_selection",
)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def require_mapping(value: Any, field: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{field}: expected a mapping")
        return {}
    return value


def require_nonempty(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field}: required non-empty string")


def validate_paths(paths: dict[str, Any], errors: list[str], require_existing: bool) -> None:
    for field in ("worktree", "branch", "shared_output", "validation", "baton"):
        require_nonempty(paths.get(field), f"paths.{field}", errors)
    for field in ("worktree", "shared_output", "validation", "baton"):
        value = paths.get(field)
        if not isinstance(value, str) or not value.strip():
            continue
        path = Path(value).expanduser()
        if not path.is_absolute():
            errors.append(f"paths.{field}: must be absolute")
        elif require_existing and not path.exists():
            errors.append(f"paths.{field}: does not resolve: {path}")


def validate_file_scope(scope: Any, errors: list[str]) -> None:
    if not isinstance(scope, list) or not scope:
        errors.append("file_scope: required non-empty list")
        return
    for item in scope:
        if not isinstance(item, str) or not item.strip():
            errors.append("file_scope: entries must be non-empty strings")
            continue
        candidate = Path(item)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"file_scope: unsafe entry: {item}")


def validate_contract(contract: dict[str, Any], require_existing_paths: bool = False) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_CONTRACT_FIELDS:
        if field not in contract:
            errors.append(f"{field}: required")
    for field in ("schema_version", "fork_id", "parent_job", "discovery_trigger"):
        require_nonempty(contract.get(field), field, errors)
    if contract.get("schema_version") != "fork-contract/v1":
        errors.append("schema_version: expected fork-contract/v1")

    hypothesis = require_mapping(contract.get("working_hypothesis"), "working_hypothesis", errors)
    require_nonempty(hypothesis.get("statement"), "working_hypothesis.statement", errors)
    if hypothesis.get("role") not in CONTRACT_ROLES:
        errors.append("working_hypothesis.role: must be investigating or in_use")

    goals = require_mapping(contract.get("goals"), "goals", errors)
    require_nonempty(goals.get("actual"), "goals.actual", errors)
    require_nonempty(goals.get("compounding"), "goals.compounding", errors)

    ownership = require_mapping(contract.get("ownership"), "ownership", errors)
    require_nonempty(ownership.get("seat"), "ownership.seat", errors)
    require_nonempty(ownership.get("owner"), "ownership.owner", errors)
    validate_paths(require_mapping(contract.get("paths"), "paths", errors), errors, require_existing_paths)
    validate_file_scope(contract.get("file_scope"), errors)

    checkpoints = contract.get("checkpoints")
    if not isinstance(checkpoints, list) or not checkpoints:
        errors.append("checkpoints: required non-empty list")
    else:
        for position, checkpoint in enumerate(checkpoints):
            item = require_mapping(checkpoint, f"checkpoints[{position}]", errors)
            require_nonempty(item.get("id"), f"checkpoints[{position}].id", errors)
            require_nonempty(item.get("pass_condition"), f"checkpoints[{position}].pass_condition", errors)
            if not isinstance(item.get("required"), bool):
                errors.append(f"checkpoints[{position}].required: required boolean")

    validation = require_mapping(contract.get("validation"), "validation", errors)
    for field in ("commands", "acceptance_checks", "independent_review"):
        value = validation.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"validation.{field}: required non-empty list")

    return_data = require_mapping(contract.get("return"), "return", errors)
    for field in ("condition", "parent_update", "verdict_path"):
        require_nonempty(return_data.get(field), f"return.{field}", errors)
    if return_data.get("verdict") not in {"used", "discarded"}:
        errors.append("return.verdict: must be used or discarded")

    selection = require_mapping(contract.get("armamentarium_selection"), "armamentarium_selection", errors)
    for field in ("hypotheses", "pathways"):
        value = selection.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"armamentarium_selection.{field}: required non-empty list")
    return errors


def validate_index(index: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if index.get("schema_version") != "fork-park-index/v1":
        errors.append("schema_version: expected fork-park-index/v1")
    records = index.get("forks")
    if not isinstance(records, list):
        return errors + ["forks: expected a list"]
    seen: set[str] = set()
    for position, record in enumerate(records):
        item = require_mapping(record, f"forks[{position}]", errors)
        fork_id = item.get("fork_id")
        require_nonempty(fork_id, f"forks[{position}].fork_id", errors)
        if isinstance(fork_id, str) and fork_id in seen:
            errors.append(f"forks[{position}].fork_id: duplicate {fork_id}")
        seen.add(fork_id)
        if item.get("state") not in FORK_STATES:
            errors.append(f"forks[{position}].state: unsupported state")
        paths = require_mapping(item.get("file_paths"), f"forks[{position}].file_paths", errors)
        for key in ("contract", "worktree", "shared_output", "validation", "baton"):
            require_nonempty(paths.get(key), f"forks[{position}].file_paths.{key}", errors)
    return errors


def resolve(contract: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    errors = validate_contract(contract)
    if registry.get("schema_version") != "armamentarium/v1":
        errors.append("registry.schema_version: expected armamentarium/v1")
    hypotheses = {item.get("id"): item for item in registry.get("working_hypotheses", []) if isinstance(item, dict)}
    pathways = {item.get("id"): item for item in registry.get("pathways", []) if isinstance(item, dict)}
    selection = contract.get("armamentarium_selection", {})
    selected_hypotheses = []
    selected_pathways = []
    for identifier in selection.get("hypotheses", []):
        item = hypotheses.get(identifier)
        if item is None:
            errors.append(f"armamentarium_selection.hypotheses: unknown {identifier}")
        elif item.get("role") not in CONTRACT_ROLES:
            errors.append(f"registry hypothesis {identifier}: invalid role")
        else:
            for field in ("aspect", "version", "statement"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f"registry hypothesis {identifier}: missing {field}")
            selected_hypotheses.append(item)
    for identifier in selection.get("pathways", []):
        item = pathways.get(identifier)
        if item is None:
            errors.append(f"armamentarium_selection.pathways: unknown {identifier}")
        elif item.get("kind") not in {"hook", "harness"}:
            errors.append(f"registry pathway {identifier}: kind must be hook or harness")
        else:
            for field in ("trigger", "deterministic_check", "failure_outcome", "ssot_path"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f"registry pathway {identifier}: missing {field}")
            selected_pathways.append(item)
    if errors:
        raise ValueError("\n".join(errors))
    return {
        "schema_version": "fork-selection-manifest/v1",
        "fork_id": contract["fork_id"],
        "working_hypothesis_role": contract["working_hypothesis"]["role"],
        "actual_goal": contract["goals"]["actual"],
        "compounding_goal": contract["goals"]["compounding"],
        "hypotheses": selected_hypotheses,
        "pathways": selected_pathways,
        "checkpoints": contract["checkpoints"],
        "validation": contract["validation"],
        "return": contract["return"],
    }


def print_errors(errors: list[str]) -> int:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate fork contracts and resolve pathway selections.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    contract_parser = subparsers.add_parser("validate")
    contract_parser.add_argument("contract", type=Path)
    contract_parser.add_argument("--require-existing-paths", action="store_true")
    index_parser = subparsers.add_parser("validate-index")
    index_parser.add_argument("index", type=Path)
    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("contract", type=Path)
    resolve_parser.add_argument("registry", type=Path)
    resolve_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        if args.command == "validate":
            errors = validate_contract(load_yaml(args.contract), args.require_existing_paths)
            if errors:
                return print_errors(errors)
            print(f"PASS: {args.contract}")
            return 0
        if args.command == "validate-index":
            errors = validate_index(load_yaml(args.index))
            if errors:
                return print_errors(errors)
            print(f"PASS: {args.index}")
            return 0
        manifest = resolve(load_yaml(args.contract), load_yaml(args.registry))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"PASS: wrote {args.output}")
        return 0
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
