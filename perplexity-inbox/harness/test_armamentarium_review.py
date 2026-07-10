#!/usr/bin/env python3
"""Tests for the external-review receipt gate."""
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

from armamentarium_review import check_promotion, validate_receipt, write_pack


class TestArmamentariumReview(unittest.TestCase):
    def write_inputs(self, root: Path) -> tuple[Path, Path, Path]:
        for name in ("worktree", "output", "validation", "baton"):
            (root / name).mkdir()
        contract = {
            "schema_version": "fork-contract/v1",
            "fork_id": "review-test-001",
            "parent_job": "parent",
            "discovery_trigger": "test",
            "working_hypothesis": {"role": "investigating", "statement": "A receipt gates promotion."},
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
            "validation": {"commands": ["test"], "acceptance_checks": ["pass"], "independent_review": ["external review"]},
            "return": {"condition": "passes", "parent_update": "state", "verdict_path": str(root / "output/verdict.yaml"), "verdict": "used"},
            "armamentarium_selection": {"hypotheses": ["candidate-v1"], "pathways": ["validator-v1"]},
        }
        registry = {
            "schema_version": "armamentarium/v1",
            "working_hypotheses": [{
                "id": "candidate-v1", "aspect": "review", "role": "investigating", "version": "v1",
                "statement": "A receipt gates promotion.",
            }],
            "pathways": [{
                "id": "validator-v1", "kind": "harness", "trigger": "before review",
                "deterministic_check": "test", "failure_outcome": "chase", "ssot_path": "test.py",
            }],
        }
        contract_path = root / "contract.yaml"
        registry_path = root / "registry.yaml"
        pack = root / "review-pack.json"
        contract_path.write_text(yaml.safe_dump(contract), encoding="utf-8")
        registry_path.write_text(yaml.safe_dump(registry), encoding="utf-8")
        write_pack(contract_path, registry_path, pack)
        return registry_path, pack, root / "receipt.yaml"

    def test_valid_receipt_allows_candidate_promotion_check(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry_path, pack, receipt_path = self.write_inputs(root)
            receipt = {
                "schema_version": "armamentarium-review-receipt/v1",
                "reviewer": "third-party-ai",
                "pack_sha256": hashlib.sha256(pack.read_bytes()).hexdigest(),
                "verdict": "pass",
                "dissent": "",
                "evidence_pointers": ["https://example.test/review"],
            }
            receipt_path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            self.assertEqual(validate_receipt(receipt, pack), [])
            self.assertEqual(check_promotion(yaml.safe_load(registry_path.read_text()), "candidate-v1", receipt, pack), [])

    def test_missing_or_uncertain_receipt_cannot_promote(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            registry_path, pack, _ = self.write_inputs(root)
            receipt = {
                "schema_version": "armamentarium-review-receipt/v1",
                "reviewer": "third-party-ai",
                "pack_sha256": hashlib.sha256(pack.read_bytes()).hexdigest(),
                "verdict": "uncertain",
                "dissent": "Insufficient evidence.",
                "evidence_pointers": [],
            }
            errors = check_promotion(yaml.safe_load(registry_path.read_text()), "candidate-v1", receipt, pack)
            self.assertIn("receipt: promotion requires a pass verdict", errors)


if __name__ == "__main__":
    unittest.main()
