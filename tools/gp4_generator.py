#!/usr/bin/env python3
"""Generate a PS4 patch project.gp4 from a staged directory."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

TITLE_ID_RE = re.compile(r"^[A-Z]{4}[0-9]{5}$")
PASSCODE_RE = re.compile(r"^[0-9A-Fa-f]{32}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title-id", required=True, help="PS4 title id (example: CUSA12345)")
    parser.add_argument("--content-id", required=True, help="PS4 content id for the target game")
    parser.add_argument("--passcode", required=True, help="32-character package passcode (usually 32 zeros)")
    parser.add_argument("--staged-dir", required=True, help="Directory containing staged patch files")
    parser.add_argument("--output", default="project.gp4", help="Output gp4 file path")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> Path:
    title_id = args.title_id.strip().upper()
    if not TITLE_ID_RE.fullmatch(title_id):
        raise ValueError("--title-id must match format like CUSA12345")
    args.title_id = title_id

    if not args.content_id.strip():
        raise ValueError("--content-id cannot be empty")
    if title_id not in args.content_id:
        raise ValueError("--content-id must contain the provided --title-id")

    passcode = args.passcode.strip()
    if not PASSCODE_RE.fullmatch(passcode):
        raise ValueError("--passcode must be exactly 32 hexadecimal characters")
    args.passcode = passcode.lower()

    staged_dir = Path(args.staged_dir).expanduser().resolve()
    if not staged_dir.is_dir():
        raise ValueError(f"--staged-dir is not a directory: {staged_dir}")

    param_sfo = staged_dir / "sce_sys" / "param.sfo"
    if not param_sfo.is_file():
        raise ValueError(f"required file missing: {param_sfo}")

    files = [p for p in staged_dir.rglob("*") if p.is_file()]
    if not files:
        raise ValueError("--staged-dir does not contain any files")

    return staged_dir


def file_entries(staged_dir: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for path in sorted((p for p in staged_dir.rglob("*") if p.is_file()), key=lambda p: p.as_posix()):
        rel = path.relative_to(staged_dir).as_posix()
        entries.append((rel, path.resolve().as_posix()))
    return entries


def build_gp4(title_id: str, content_id: str, passcode: str, entries: list[tuple[str, str]]) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<psproject fmt="gp4" version="1000">',
        '  <volume>',
        '    <volume_type>pkg_ps4_patch</volume_type>',
        f'    <volume_id>{escape(title_id)}</volume_id>',
        f'    <package content_id="{escape(content_id)}" passcode="{escape(passcode)}"/>',
        '  </volume>',
        '  <files img_no="0">',
    ]
    for targ_path, orig_path in entries:
        lines.append(
            f'    <file targ_path="{escape(targ_path)}" orig_path="{escape(orig_path)}"/>'
        )
    lines.extend(
        [
            '  </files>',
            '  <rootdir>',
            '    <dir targ_name=""/>',
            '  </rootdir>',
            '</psproject>',
            '',
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        staged_dir = validate_args(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    entries = file_entries(staged_dir)
    gp4 = build_gp4(args.title_id, args.content_id, args.passcode, entries)

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(gp4, encoding="utf-8")

    print(f"Wrote {output_path} with {len(entries)} file entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
