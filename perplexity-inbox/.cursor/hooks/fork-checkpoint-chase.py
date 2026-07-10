#!/usr/bin/env python3
"""Warning-level fork checkpoint chase for stop / subagentStop hooks."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
CANDIDATES = [
    HOOK_DIR.parents[1] / "harness",  # perplexity-inbox/.cursor/hooks -> perplexity-inbox/harness
    HOOK_DIR.parent / "harness",
]
for candidate in CANDIDATES:
    if (candidate / "fork_flow.py").is_file():
        sys.path.insert(0, str(candidate))
        break

from fork_flow import load_yaml, validate_contract  # noqa: E402


def missing_checkpoints(contract_path: Path) -> list[str]:
    missing: list[str] = []
    if not contract_path.is_file():
        return [f"FORK_CONTRACT does not resolve: {contract_path}"]
    try:
        contract = load_yaml(contract_path)
    except (OSError, ValueError) as error:
        return [f"contract unreadable: {error}"]
    errors = validate_contract(contract, require_existing_paths=True)
    missing.extend(errors)
    paths = contract.get("paths", {}) if isinstance(contract.get("paths"), dict) else {}
    for label in ("shared_output", "validation", "baton"):
        value = paths.get(label)
        if isinstance(value, str) and value.strip():
            path = Path(value).expanduser()
            if path.is_dir() and not any(path.iterdir()):
                missing.append(f"paths.{label}: directory is empty ({path})")
    return_data = contract.get("return", {}) if isinstance(contract.get("return"), dict) else {}
    verdict_path = return_data.get("verdict_path")
    if isinstance(verdict_path, str) and verdict_path.strip():
        if not Path(verdict_path).expanduser().is_file():
            missing.append(f"return.verdict_path missing: {verdict_path}")
    return missing


def main() -> int:
    contract = os.environ.get("FORK_CONTRACT", "").strip()
    if not contract:
        print("{}")
        return 0
    missing = missing_checkpoints(Path(contract).expanduser())
    if not missing:
        print("{}")
        return 0
    message = "Fork checkpoint chase (warning only): " + "; ".join(missing[:5])
    if len(missing) > 5:
        message += f"; +{len(missing) - 5} more"
    print(json.dumps({"followup_message": message}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
