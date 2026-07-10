#!/usr/bin/env python3
"""Lightweight Python syntax check for the shape gate.

Returns (ok, message) so the shape gate can block on syntax errors and log
any autocorrect events. Ruff auto-fix is used only when available.
"""
from __future__ import annotations

import hashlib
import py_compile
import shutil
import subprocess
from pathlib import Path


def check_and_repair_file(path: Path) -> tuple[bool, str]:
    """Compile the file and, if ruff is installed, apply safe fixes.

    Returns (True, "ok") when the file passes, (True, "[AUTOCORRECT] ...")
    when ruff changed the file, or (False, "Syntax error: ...") when the
    file cannot compile.
    """
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, f"Syntax error in {path}: {exc}"

    if shutil.which("ruff"):
        before = _sha256(path)
        try:
            result = subprocess.run(
                ["ruff", "check", "--fix", str(path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and _sha256(path) != before:
                return True, "[AUTOCORRECT] ruff applied safe fixes"
        except (OSError, subprocess.TimeoutExpired):
            pass

    return True, "ok"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
