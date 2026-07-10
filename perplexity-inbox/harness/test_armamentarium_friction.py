#!/usr/bin/env python3
"""Tests for armamentarium friction and promotion-gated deltas."""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.append(str(HARNESS_DIR))

from armamentarium_friction import apply_delta_if_promotable, propose_registry_delta, record_friction
from armamentarium_review import write_pack


class TestArmamentariumFriction(unittest.TestCase):
    def test_friction_delta_and_promotion_denial(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("worktree", "output", "validation", "baton"):
                (root / name).mkdir()
            contract = {
                "schema_version": "fork-contract/v1",
                "fork_id": "friction-001",
                "parent_job": "parent",
                "discovery_trigger": "test",
                "working_hypothesis": {"role": "investigating", "statement": "Friction proposes, receipt promotes."},
                "goals": {"actual": "test", "compounding": "test"},
                "ownership": {"seat": "cursor", "owner": "cursor-child"},
                "paths": {
                    "worktree": str(root / "worktree"),
                    "branch": "cursor/test",
                    "shared_output": str(root / "output"),
                    "validation": str(root / "validation"),
                    "baton": str(root / "baton"),
                },
                "file_scope": ["perplexity-inbox/armamentarium/**"],
                "checkpoints": [{"id": "check", "required": True, "pass_condition": "passes"}],
                "validation": {
                    "commands": ["test"],
                    "acceptance_checks": ["pass"],
                    "independent_review": ["external review"],
                },
                "return": {
                    "condition": "passes",
                    "parent_update": "state",
                    "verdict_path": str(root / "output/verdict.yaml"),
                    "verdict": "used",
                },
                "armamentarium_selection": {
                    "hypotheses": ["candidate-v1"],
                    "pathways": ["validator-v1"],
                },
            }
            registry = {
                "schema_version": "armamentarium/v1",
                "required_aspects": [],
                "working_hypotheses": [
                    {
                        "id": "candidate-v1",
                        "aspect": "review",
                        "role": "investigating",
                        "version": "v1",
                        "statement": "Friction proposes, receipt promotes.",
                        "evidence_pointers": [],
                        "replacement_history": [],
                    }
                ],
                "pathways": [
                    {
                        "id": "validator-v1",
                        "kind": "harness",
                        "trigger": "before review",
                        "deterministic_check": "test",
                        "failure_outcome": "chase",
                        "ssot_path": "test.py",
                    }
                ],
            }
            contract_path = root / "contract.yaml"
            registry_path = root / "registry.yaml"
            contract_path.write_text(yaml.safe_dump(contract), encoding="utf-8")
            registry_path.write_text(yaml.safe_dump(registry), encoding="utf-8")
            pack = root / "pack.json"
            write_pack(contract_path, registry_path, pack)
            manifest = json.loads(pack.read_text(encoding="utf-8"))["selection_manifest"]
            friction = record_friction(
                selection_manifest=manifest,
                aspect="review",
                observation="Local dogfood suggests evidence update.",
                proposed_change={
                    "action": "update_hypothesis_evidence",
                    "payload": {"id": "candidate-v1", "evidence_pointers": ["envelope://x"]},
                },
                output=root / "friction.jsonl",
            )
            delta = propose_registry_delta(registry, friction)
            self.assertFalse(delta["promotion_allowed"])
            with self.assertRaisesRegex(ValueError, "local validation receipt missing"):
                apply_delta_if_promotable(
                    registry,
                    delta,
                    hypothesis_id="candidate-v1",
                    receipt={
                        "schema_version": "armamentarium-review-receipt/v1",
                        "reviewer": "third-party",
                        "pack_sha256": hashlib.sha256(pack.read_bytes()).hexdigest(),
                        "verdict": "pass",
                        "dissent": "",
                        "evidence_pointers": [],
                    },
                    pack=pack,
                    local_validation_receipt=root / "missing-local.json",
                )


if __name__ == "__main__":
    unittest.main()
