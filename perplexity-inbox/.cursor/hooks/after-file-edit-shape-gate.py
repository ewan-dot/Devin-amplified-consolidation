#!/usr/bin/env python3
"""Cursor afterFileEdit — delegates to SSOT harness/hooks/cursor-after-file-edit-shape-gate.py"""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parents[2] / "harness/hooks/cursor-after-file-edit-shape-gate.py"),
    run_name="__main__",
)
