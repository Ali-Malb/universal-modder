#!/usr/bin/env python3
"""Generate a PS4 .gp4 project file from staged app0/patch0 content."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

DEFAULT_PASSCODE = "00000000000000000000000000000000"
PASSCODE_RE = re.compile(r"^[0-9A-Fa-f]{32}$")
TITLE_ID_RE = re.compile(r"[A-Z]{4}[0-9]{5}")
EXCLUDED_DIRS = {"changeinfo"}
EXCLUDED_SUFFIXES = {".pkg"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged-dir", required=True, help="Path to staged app0/patch0 files")
    parser.add_argument("--output-gp4", required=True, help="Output .gp4 file path")
    parser.add_argument("--content-id", required=True, help="PS4 content id")
    parser.add_argument(
        "--passcode",
        default=DEFAULT_PASSCODE,
        help=f"Package passcode (default: {DEFAULT_PASSCODE})",
    )
    parser.add_argument(
        "--type",
        dest="pkg_type",
        default="pkg_ps4_patch",
        choices=("pkg_ps4_patch", "pkg_ps4_app"),
        help="GP4 package type",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> tuple[Path, str]:
    staged_dir = Path(args.staged_dir).expanduser().resolve()
    if not staged_dir.is_dir():
        raise ValueError(f"--staged-dir is not a directory: {staged_dir}")

    content_id = args.content_id.strip()
    if not content_id:
        raise ValueError("--content-id cannot be empty")

    title_match = TITLE_ID_RE.search(content_id)
    if not title_match:
        raise ValueError("--content-id must include a valid title id like CUSA00000")

    passcode = args.passcode.strip()
    if not PASSCODE_RE.fullmatch(passcode):
        raise ValueError("--passcode must be exactly 32 hexadecimal characters")
    args.passcode = passcode.lower()
    args.content_id = content_id

    return staged_dir, title_match.group(0)


def include_file(path: Path, staged_dir: Path) -> bool:
    rel = path.relative_to(staged_dir)
    if any(part.lower() in EXCLUDED_DIRS for part in rel.parts[:-1]):
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return True


def file_entries(staged_dir: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    files = sorted((p for p in staged_dir.rglob("*") if p.is_file()), key=lambda p: p.as_posix())
    for path in files:
        if not include_file(path, staged_dir):
            continue
        rel = path.relative_to(staged_dir).as_posix()
        entries.append((rel, path.resolve().as_posix()))
    if not entries:
        raise ValueError("no package files found after exclusions")
    return entries


def build_gp4(
    volume_type: str,
    volume_id: str,
    content_id: str,
    passcode: str,
    entries: list[tuple[str, str]],
) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<psproject fmt="gp4" version="1000">',
        "  <volume>",
        f"    <volume_type>{escape(volume_type)}</volume_type>",
        f"    <volume_id>{escape(volume_id)}</volume_id>",
        f'    <package content_id="{escape(content_id)}" passcode="{escape(passcode)}"/>',
        "  </volume>",
        '  <files img_no="0">',
    ]
    for targ_path, orig_path in entries:
        lines.append(f'    <file targ_path="{escape(targ_path)}" orig_path="{escape(orig_path)}"/>')
    lines.extend(
        [
            "  </files>",
            "  <rootdir>",
            '    <dir targ_name=""/>',
            "  </rootdir>",
            "</psproject>",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        staged_dir, title_id = validate_args(args)
        entries = file_entries(staged_dir)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    gp4 = build_gp4(args.pkg_type, title_id, args.content_id, args.passcode, entries)
    output_path = Path(args.output_gp4).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(gp4, encoding="utf-8")
    print(f"Wrote {output_path} with {len(entries)} file entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
