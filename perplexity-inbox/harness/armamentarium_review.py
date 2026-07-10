#!/usr/bin/env python3
"""Create attributable third-party review packs and validate promotion evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from fork_flow import load_yaml, resolve

REQUIRED_RECEIPT_FIELDS = (
    "schema_version",
    "reviewer",
    "pack_sha256",
    "verdict",
    "dissent",
    "evidence_pointers",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_receipt(receipt: dict[str, Any], pack: Path) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_RECEIPT_FIELDS:
        if field not in receipt:
            errors.append(f"{field}: required")
    if receipt.get("schema_version") != "armamentarium-review-receipt/v1":
        errors.append("schema_version: expected armamentarium-review-receipt/v1")
    if not isinstance(receipt.get("reviewer"), str) or not receipt["reviewer"].strip():
        errors.append("reviewer: required non-empty string")
    if receipt.get("pack_sha256") != sha256_file(pack):
        errors.append("pack_sha256: does not match review pack")
    if receipt.get("verdict") not in {"pass", "fail", "uncertain"}:
        errors.append("verdict: expected pass, fail, or uncertain")
    if not isinstance(receipt.get("dissent"), str):
        errors.append("dissent: required string; use empty string when none")
    if not isinstance(receipt.get("evidence_pointers"), list):
        errors.append("evidence_pointers: expected list")
    return errors


def write_pack(contract_path: Path, registry_path: Path, output: Path) -> None:
    contract = load_yaml(contract_path)
    registry = load_yaml(registry_path)
    manifest = resolve(contract, registry)
    pack = {
        "schema_version": "armamentarium-review-pack/v1",
        "purpose": "Independent structural review before any hypothesis promotion.",
        "contract_path": str(contract_path.resolve()),
        "registry_path": str(registry_path.resolve()),
        "contract_sha256": sha256_file(contract_path),
        "registry_sha256": sha256_file(registry_path),
        "selection_manifest": manifest,
        "acceptance_checks": contract["validation"]["acceptance_checks"],
        "independent_review_request": contract["validation"]["independent_review"],
        "required_receipt_schema": "armamentarium-review-receipt/v1",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(pack, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def check_promotion(registry: dict[str, Any], hypothesis_id: str, receipt: dict[str, Any], pack: Path) -> list[str]:
    errors = validate_receipt(receipt, pack)
    hypotheses = registry.get("working_hypotheses", [])
    candidate = next((item for item in hypotheses if item.get("id") == hypothesis_id), None)
    if candidate is None:
        errors.append(f"hypothesis: unknown {hypothesis_id}")
    elif candidate.get("role") != "investigating":
        errors.append("hypothesis: only investigating candidates are eligible for promotion")
    if receipt.get("verdict") != "pass":
        errors.append("receipt: promotion requires a pass verdict")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Build third-party review packs and check promotion receipts.")
    commands = parser.add_subparsers(dest="command", required=True)
    pack_parser = commands.add_parser("write-pack")
    pack_parser.add_argument("contract", type=Path)
    pack_parser.add_argument("registry", type=Path)
    pack_parser.add_argument("--output", type=Path, required=True)
    receipt_parser = commands.add_parser("validate-receipt")
    receipt_parser.add_argument("receipt", type=Path)
    receipt_parser.add_argument("pack", type=Path)
    promotion_parser = commands.add_parser("check-promotion")
    promotion_parser.add_argument("hypothesis_id")
    promotion_parser.add_argument("registry", type=Path)
    promotion_parser.add_argument("receipt", type=Path)
    promotion_parser.add_argument("pack", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "write-pack":
            write_pack(args.contract, args.registry, args.output)
            print(f"PASS: wrote {args.output}")
            return 0
        receipt = load_yaml(args.receipt)
        if args.command == "validate-receipt":
            errors = validate_receipt(receipt, args.pack)
        else:
            errors = check_promotion(load_yaml(args.registry), args.hypothesis_id, receipt, args.pack)
        if errors:
            for error in errors:
                print(f"FAIL: {error}", file=sys.stderr)
            return 1
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
