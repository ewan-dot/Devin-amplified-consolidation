#!/usr/bin/env python3
"""Deterministic Outbound Doorway Patch Applicator.

Monitors the outbound_doorway directory, parses structured JSON patches,
verifies target alignments, applies file modifications, and commits them.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone

HARNESS_DIR = Path(__file__).resolve().parent
ROOT_DIR = HARNESS_DIR.parent.parent
DOORWAY_DIR = ROOT_DIR / "outbound_doorway"
APPLIED_DIR = DOORWAY_DIR / "applied"


class DoorwayApplicator:
    def __init__(self, root_dir: Path = ROOT_DIR, doorway_dir: Path = DOORWAY_DIR):
        self.root_dir = root_dir
        self.doorway_dir = doorway_dir
        self.applied_dir = doorway_dir / "applied"

    def setup_directories(self):
        """Creates the doorway and applied directories if they do not exist."""
        self.doorway_dir.mkdir(parents=True, exist_ok=True)
        self.applied_dir.mkdir(parents=True, exist_ok=True)

    def scan_patches(self) -> list[Path]:
        """Scans the doorway folder for pending json patches."""
        if not self.doorway_dir.exists():
            return []
        return sorted([p for p in self.doorway_dir.glob("patch_*.json")])

    def apply_patch(self, patch_path: Path) -> tuple[bool, str]:
        """Parses and applies a single patch file."""
        try:
            with open(patch_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            return False, f"Failed to parse patch JSON: {e}"

        # Schema Validation
        agent_id = data.get("agent_id")
        timestamp = data.get("timestamp")
        changes = data.get("changes", [])

        if not agent_id or not timestamp or not isinstance(changes, list):
            return False, "Invalid patch schema: missing agent_id, timestamp, or changes list."

        applied_changes = []

        # Apply each change
        for idx, change in enumerate(changes):
            file_path_str = change.get("file_path")
            action = change.get("action")
            target = change.get("target_content")
            replacement = change.get("replacement_content")

            if not file_path_str or not action:
                return False, f"Change {idx} is missing file_path or action."

            file_path = Path(file_path_str)
            if not file_path.is_absolute():
                file_path = self.root_dir / file_path

            if not file_path.exists():
                return False, f"Target file does not exist: {file_path}"

            # Banned files for AI modifications (Security & Sovereignty Protection)
            banned_patterns = [".cursorrules", ".clauderules", ".cursor/", ".claude/", "hooks.json", "AGENTS.md", "ESTATE-TAXONOMY.md"]
            if any(pat in str(file_path) for pat in banned_patterns):
                return False, f"Banned path: Agent is forbidden from modifying configuration file: {file_path.name}"

            try:
                content = file_path.read_text()
            except Exception as e:
                return False, f"Failed to read target file {file_path.name}: {e}"

            if action == "modify":
                if target not in content:
                    return False, f"Target content not found in {file_path.name} (conflict detected)."
                
                new_content = content.replace(target, replacement, 1)
                applied_changes.append((file_path, new_content))
            else:
                return False, f"Unsupported action: '{action}'"

        # Write updates if all verified
        for file_path, new_content in applied_changes:
            try:
                file_path.write_text(new_content)
                print(f"Successfully applied modifications to {file_path.name}")
            except Exception as e:
                return False, f"Failed to write modifications to {file_path.name}: {e}"

        # Git Stage & Commit
        try:
            for file_path, _ in applied_changes:
                subprocess.check_call(["git", "add", str(file_path)], cwd=str(self.root_dir))
            
            commit_msg = f"feat(doorway): apply changes from {agent_id} at {timestamp}"
            subprocess.check_call(["git", "commit", "-m", commit_msg], cwd=str(self.root_dir))
            print(f"Git commit created: {commit_msg}")
        except Exception as e:
            print(f"Warning: Git commit failed: {e}", file=sys.stderr)

        # Move to applied folder
        try:
            dest = self.applied_dir / patch_path.name
            shutil.move(str(patch_path), str(dest))
        except Exception as e:
            return True, f"Patch applied but failed to archive patch file: {e}"

        return True, "Patch applied and committed successfully."


def main():
    applicator = DoorwayApplicator()
    applicator.setup_directories()
    patches = applicator.scan_patches()
    if not patches:
        print("No pending doorway patches found.")
        sys.exit(0)

    success = True
    for patch in patches:
        print(f"Applying patch: {patch.name}")
        ok, msg = applicator.apply_patch(patch)
        print(f"Result: {'SUCCESS' if ok else 'FAILED'} - {msg}")
        if not ok:
            success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
