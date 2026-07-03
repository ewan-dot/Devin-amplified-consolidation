#!/usr/bin/env bash
# config-lock.sh — macOS user-immutable (uchg) lock for Cursor RULE markdown ONLY.
#
# Scope (deliberate): ~/.cursor/rules/*.mdc — Ewan's constitution.
# NOT locked: hooks.json, ~/.cursor/hooks/* scripts, harness scripts, and
# ~/.cursor/integrity/* — those stay editable while the hooks/harness are
# still under development.
#
# Subcommands:
#   lock     chflags uchg   on every rules/*.mdc  (write/delete blocked)
#   unlock   chflags nouchg on every rules/*.mdc  (required before any edit/re-bless)
#   status   ls -lO of rules/*.mdc                (the flags column shows `uchg`)
#
# Correct edit cycle for a rule:
#   config-lock.sh unlock  ->  edit rule(s)  ->  update-config-manifest.py  ->  config-lock.sh lock
#
# Honest limit: this is the SAME user. `chflags nouchg` reverses it; uchg is not
# root-proof and not tamper-PROOF. It is a deliberate speed-bump against
# accidental or automated edits to the constitution — evidence + friction, not a vault.
set -euo pipefail

RULES_DIR="${CURSOR_RULES_DIR:-$HOME/.cursor/rules}"

usage() {
  echo "usage: config-lock.sh {lock|unlock|status}" >&2
  exit 2
}

[ "$#" -eq 1 ] || usage

shopt -s nullglob
mdc_files=("$RULES_DIR"/*.mdc)
shopt -u nullglob

case "$1" in
  lock)
    if [ "${#mdc_files[@]}" -eq 0 ]; then echo "[config-lock] no *.mdc in $RULES_DIR"; exit 0; fi
    for f in "${mdc_files[@]}"; do chflags uchg "$f"; done
    echo "[config-lock] LOCKED ${#mdc_files[@]} rule file(s) with uchg in $RULES_DIR"
    ;;
  unlock)
    if [ "${#mdc_files[@]}" -eq 0 ]; then echo "[config-lock] no *.mdc in $RULES_DIR"; exit 0; fi
    for f in "${mdc_files[@]}"; do chflags nouchg "$f"; done
    echo "[config-lock] UNLOCKED ${#mdc_files[@]} rule file(s) (nouchg) in $RULES_DIR"
    ;;
  status)
    ls -lO "$RULES_DIR"/*.mdc
    ;;
  *)
    usage
    ;;
esac
