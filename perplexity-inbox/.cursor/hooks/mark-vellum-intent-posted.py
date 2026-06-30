#!/usr/bin/env python3
"""Backward compat — delegates to mark-vellum-plan-posted."""
import subprocess
import sys

subprocess.check_call([sys.executable, __file__.replace("mark-vellum-intent-posted.py", "mark-vellum-plan-posted.py"), *sys.argv[1:]])
