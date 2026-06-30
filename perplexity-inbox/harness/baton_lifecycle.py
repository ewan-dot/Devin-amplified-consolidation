#!/usr/bin/env python3
"""Baton folder lifecycle — active (max 5) → unified archive → datalake bronze.

SSOT paths under AMPLIFIED_INBOX / amplified-pipeline data/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

MAX_ACTIVE = 5
WITNESS = os.path.expanduser("~/.amplified/logs/harness-hooks.jsonl")


def inbox_root() -> Path:
    env = os.environ.get("AMPLIFIED_INBOX", "").strip()
    if env:
        return Path(env).expanduser()
    return Path(__file__).resolve().parent.parent


def pipeline_data() -> Path:
    env = os.environ.get("AMPLIFIED_PIPELINE_DATA", "").strip()
    if env:
        return Path(env).expanduser()
    home = Path.home()
    if (home / "amplified-pipeline/data").is_dir():
        return home / "amplified-pipeline/data"
    return inbox_root() / "data"


def paths() -> dict[str, Path]:
    ib = inbox_root()
    data = pipeline_data()
    return {
        "active": ib / "batons" / "active",
        "archive": data / "batons" / "archive",
        "datalake": data / "datalake" / "bronze" / "batons",
    }


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:48] or "baton"


def witness(event: str, ok: bool, note: str) -> None:
    try:
        os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
        with open(WITNESS, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"ts": time.time(), "hook": "baton_lifecycle", "event": event, "ok": ok, "note": note}
                )
                + "\n"
            )
    except OSError:
        pass


def list_active(active_dir: Path) -> list[Path]:
    if not active_dir.is_dir():
        return []
    files = [p for p in active_dir.glob("BATON__*.md") if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def archive_file(src: Path, archive_dir: Path, datalake_dir: Path) -> None:
    archive_dir.mkdir(parents=True, exist_ok=True)
    datalake_dir.mkdir(parents=True, exist_ok=True)
    day = datetime.fromtimestamp(src.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")
    arch_sub = archive_dir / day
    arch_sub.mkdir(parents=True, exist_ok=True)
    dest_arch = arch_sub / src.name
    if not dest_arch.exists():
        shutil.copy2(src, dest_arch)
    lake_sub = datalake_dir / day
    lake_sub.mkdir(parents=True, exist_ok=True)
    dest_lake = lake_sub / src.name
    if not dest_lake.exists():
        shutil.copy2(src, dest_lake)
    src.unlink(missing_ok=True)


def rotate(active_dir: Path, archive_dir: Path, datalake_dir: Path) -> list[str]:
    rotated: list[str] = []
    active = list_active(active_dir)
    while len(active) >= MAX_ACTIVE:
        oldest = active.pop()
        archive_file(oldest, archive_dir, datalake_dir)
        rotated.append(oldest.name)
    return rotated


def write_baton(
    *,
    from_agent: str,
    to_agent: str,
    title: str,
    body: str,
    seat: str | None = None,
) -> Path:
    p = paths()
    p["active"].mkdir(parents=True, exist_ok=True)
    rotated = rotate(p["active"], p["archive"], p["datalake"])
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    date = ts[:10]
    seat_slug = slugify(seat or from_agent)
    fname = f"BATON__{slugify(title)}__v01__{date}__{seat_slug}.md"
    frontmatter = f"""---
title: "{title}"
document_type: baton
date_utc: {date}
from_agent: {from_agent}
to_agent: {to_agent}
author: {from_agent}
epistemic_tier: INTUITED
baton_ts: {ts}
---

"""
    content = frontmatter + body.strip() + "\n"
    dest = p["active"] / fname
    dest.write_text(content, encoding="utf-8")
    witness("write", True, f"{fname} rotated={rotated}")
    return dest


def read_latest(max_chars: int = 3500) -> str:
    p = paths()
    active = list_active(p["active"])
    if not active:
        return ""
    latest = active[0]
    text = latest.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        text = text[:max_chars] + "\n…(truncated)"
    return f"[baton] latest={latest.name}\n{text}"


def cmd_write(args: argparse.Namespace) -> int:
    body = args.body
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    dest = write_baton(
        from_agent=args.from_agent,
        to_agent=args.to_agent,
        title=args.title,
        body=body,
        seat=args.seat,
    )
    print(dest)
    return 0


def cmd_read(_: argparse.Namespace) -> int:
    print(read_latest())
    return 0


def cmd_rotate(_: argparse.Namespace) -> int:
    p = paths()
    rotated = rotate(p["active"], p["archive"], p["datalake"])
    print(json.dumps({"rotated": rotated, "remaining": [x.name for x in list_active(p["active"])]}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Baton folder lifecycle")
    sub = parser.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("write")
    w.add_argument("--from", dest="from_agent", default="cursor")
    w.add_argument("--to", dest="to_agent", default="next-seat")
    w.add_argument("--title", required=True)
    w.add_argument("--seat", default=None)
    w.add_argument("--body", default="")
    w.add_argument("--body-file")
    w.set_defaults(func=cmd_write)

    r = sub.add_parser("read")
    r.set_defaults(func=cmd_read)

    rot = sub.add_parser("rotate")
    rot.set_defaults(func=cmd_rotate)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
