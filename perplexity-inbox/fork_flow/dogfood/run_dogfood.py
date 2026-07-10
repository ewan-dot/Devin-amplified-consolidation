#!/usr/bin/env python3
"""Fixture dogfood for fork-flow + armamentarium (local, deterministic)."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

HARNESS = Path(__file__).resolve().parents[2] / "harness"
INBOX = Path(__file__).resolve().parents[2]
FIXTURE_SOURCE = Path(__file__).resolve().parent / "fixtures" / "source" / "spotlight-note.txt"
REGISTRY = INBOX / "armamentarium" / "registry.yaml"

sys.path.insert(0, str(HARNESS))

from armamentarium_friction import propose_registry_delta, record_friction  # noqa: E402
from armamentarium_review import write_pack  # noqa: E402
from fork_flow import resolve  # noqa: E402
from fork_flow_store import (  # noqa: E402
    build_projection,
    create,
    resume,
    transition,
    write_projection,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_raw_envelope(source: Path, out_dir: Path) -> dict[str, Any]:
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)
    envelope = {
        "schema_version": "raw-span-envelope/v1",
        "source_path": str(source.resolve()),
        "source_sha256": sha256_bytes(raw),
        "byte_range": [0, len(raw)],
        "line_range": [1, len(lines)],
        "content": text,
        "lineage": {"fixture": "spotlight-style-dogfood", "normalizer_version": "fork-flow-dogfood/v1"},
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{envelope['source_sha256']}.json"
    path.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"envelope_path": str(path), "source_sha256": envelope["source_sha256"]}


def normalize_projection(projection: dict[str, Any]) -> dict[str, Any]:
    forks = []
    for fork in projection.get("forks", []):
        forks.append(
            {
                "fork_id": fork.get("fork_id"),
                "state": fork.get("state"),
                "review_status": fork.get("review_status"),
                "claimed_by": fork.get("claimed_by", ""),
                "path_labels": sorted((fork.get("file_paths") or {}).keys()),
            }
        )
    return {
        "schema_version": projection.get("schema_version"),
        "views": projection.get("views"),
        "forks": forks,
        "file_path_atom_count": len(projection.get("file_path_atoms", [])),
    }


def run_once(run_root: Path) -> dict[str, Any]:
    worktree = run_root / "worktree"
    shared = run_root / "shared"
    validation = run_root / "validation"
    baton_dir = run_root / "baton"
    store = run_root / "store"
    envelopes = run_root / "raw-envelopes"
    for path in (worktree, shared, validation, baton_dir):
        path.mkdir(parents=True, exist_ok=True)

    os.environ["AMPLIFIED_INBOX"] = str(run_root / "inbox")
    (run_root / "inbox" / "batons" / "active").mkdir(parents=True, exist_ok=True)

    envelope_meta = write_raw_envelope(FIXTURE_SOURCE, envelopes)
    contract = {
        "schema_version": "fork-contract/v1",
        "fork_id": "fork-dogfood-spotlight-001",
        "parent_job": "parent-continuity-job",
        "discovery_trigger": "Bounded child discovery during parent continuity.",
        "working_hypothesis": {
            "role": "investigating",
            "statement": "Fixture dogfood proves park/resume/close without promotion.",
        },
        "goals": {
            "actual": "Close the fixture with used/discarded and review pending.",
            "compounding": "Leave deterministic receipts under amplified-pipeline data.",
        },
        "ownership": {"seat": "cursor", "owner": "cursor-dogfood"},
        "paths": {
            "worktree": str(worktree),
            "branch": "cursor/fork-dogfood-spotlight",
            "shared_output": str(shared),
            "validation": str(validation),
            "baton": str(baton_dir),
        },
        "file_scope": ["perplexity-inbox/fork_flow/**", "perplexity-inbox/armamentarium/**"],
        "checkpoints": [
            {"id": "contract", "required": True, "pass_condition": "Contract validates."},
            {"id": "return", "required": True, "pass_condition": "Verdict exists."},
        ],
        "validation": {
            "commands": ["python3 -m unittest harness.test_fork_flow_store"],
            "acceptance_checks": ["projection rebuilds", "promotion denied without receipt"],
            "independent_review": ["third-party review pack pending"],
        },
        "return": {
            "condition": "Required checkpoints pass.",
            "parent_update": "Parent keeps continuity; child returns used/discarded.",
            "verdict_path": str(shared / "verdict.yaml"),
            "verdict": "used",
        },
        "armamentarium_selection": {
            "hypotheses": ["fork-flow-baseline-v1"],
            "pathways": [
                "fork-contract-validator-v1",
                "worktree-isolation-v1",
                "stop-checkpoint-nudge-v1",
            ],
        },
    }
    contract_path = run_root / "contract.yaml"
    contract_path.write_text(yaml.safe_dump(contract), encoding="utf-8")

    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    manifest = resolve(contract, registry)
    manifest_path = shared / "selection-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    create(store, contract_path)
    # park remains parked until resume
    resume(store, "fork-dogfood-spotlight-001", owner="cursor-dogfood")
    transition(store, "fork-dogfood-spotlight-001", "running")
    # deliberate park mid-run, then resume
    transition(store, "fork-dogfood-spotlight-001", "parked", reason="parent continuity checkpoint")
    resume(store, "fork-dogfood-spotlight-001", owner="cursor-dogfood")
    transition(store, "fork-dogfood-spotlight-001", "running")
    # validation failure path: block + baton, then resume
    transition(
        store,
        "fork-dogfood-spotlight-001",
        "blocked",
        reason="validation fixture failure before retry",
    )
    resume(store, "fork-dogfood-spotlight-001", owner="cursor-dogfood")
    transition(store, "fork-dogfood-spotlight-001", "running")
    transition(store, "fork-dogfood-spotlight-001", "checked")

    verdict = {
        "verdict": "used",
        "note": "Local dogfood closed; third-party review still pending.",
        "raw_envelope": envelope_meta,
        "review_status": "pending",
    }
    verdict_path = shared / "verdict.yaml"
    verdict_path.write_text(yaml.safe_dump(verdict, sort_keys=False), encoding="utf-8")
    transition(store, "fork-dogfood-spotlight-001", "used", verdict_path=str(verdict_path))

    # friction + proposed delta (no promotion)
    change = {
        "action": "update_hypothesis_evidence",
        "payload": {
            "id": "fork-flow-dogfood-candidate-v1",
            "evidence_pointers": [envelope_meta["envelope_path"]],
        },
    }
    friction = record_friction(
        selection_manifest=manifest,
        aspect="discovery-forking",
        observation="Dogfood closed used with review still pending.",
        proposed_change=change,
        output=shared / "friction-events.jsonl",
    )
    delta = propose_registry_delta(registry, friction)
    (shared / "registry-delta.yaml").write_text(yaml.safe_dump(delta, sort_keys=False), encoding="utf-8")

    pack_path = shared / "review-pack.json"
    write_pack(contract_path, REGISTRY, pack_path)

    index_path = shared / "fork-park-index.yaml"
    write_projection(store, index_path)
    projection = build_projection(store)

    local_receipt = {
        "schema_version": "fork-flow-local-receipt/v1",
        "fork_id": "fork-dogfood-spotlight-001",
        "verdict": "used",
        "review_status": "pending",
        "selection_manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
        "projection": normalize_projection(projection),
        "raw_envelope": envelope_meta,
        "commands_recorded": [
            "create",
            "resume",
            "running",
            "parked",
            "resume",
            "running",
            "blocked+baton",
            "resume",
            "running",
            "checked",
            "used",
        ],
    }
    receipt_path = shared / "local-receipt.json"
    receipt_path.write_text(json.dumps(local_receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return local_receipt


def main() -> int:
    out_root = Path(
        os.environ.get(
            "FORK_FLOW_DOGFOOD_ROOT",
            str(Path.home() / "amplified-pipeline" / "data" / "fork-flow" / "dogfood"),
        )
    )
    out_root.mkdir(parents=True, exist_ok=True)
    receipts = []
    for index in (1, 2):
        run_dir = Path(tempfile.mkdtemp(prefix=f"fork-dogfood-{index}-", dir=out_root))
        receipt = run_once(run_dir)
        receipts.append(receipt)
        (out_root / f"receipt-run-{index}.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    left = json.dumps(receipts[0]["projection"], sort_keys=True)
    right = json.dumps(receipts[1]["projection"], sort_keys=True)
    compare = {
        "schema_version": "fork-flow-dogfood-compare/v1",
        "deterministic_projections": left == right,
        "receipt_paths": [
            str(out_root / "receipt-run-1.json"),
            str(out_root / "receipt-run-2.json"),
        ],
    }
    compare_path = out_root / "compare.json"
    compare_path.write_text(json.dumps(compare, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if left != right:
        print(f"FAIL: projections diverged; see {compare_path}", file=sys.stderr)
        return 1
    # Record harness suite output into the dogfood folder.
    suite = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "test_fork_flow",
            "test_fork_flow_store",
            "test_armamentarium_review",
            "test_armamentarium_friction",
            "test_fork_flow_dogfood",
        ],
        cwd=str(HARNESS),
        capture_output=True,
        text=True,
    )
    (out_root / "unit-suite.txt").write_text(suite.stdout + "\n" + suite.stderr, encoding="utf-8")
    print(json.dumps({"PASS": True, "compare": str(compare_path), "unit_suite_ok": suite.returncode == 0}, sort_keys=True))
    return 0 if suite.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
