#!/usr/bin/env python3
"""Sync local modded files to GoldHEN AFSP over FTP."""

from __future__ import annotations

import argparse
import ftplib
import os
import posixpath
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

TITLE_ID_RE = re.compile(r"^[A-Z]{4}[0-9]{5}$")
AFSP_ROOT = "/data/GoldHEN/AFSP"


@dataclass
class SyncStats:
    uploaded: int = 0
    skipped: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ip", required=True, help="PS4 IP address")
    parser.add_argument("--port", type=int, default=2121, help="GoldHEN FTP port (default: 2121)")
    parser.add_argument("--title-id", required=True, help="Game title id (example: CUSA00123)")
    parser.add_argument("--local-dir", required=True, help="Local directory with modified files")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> tuple[Path, str]:
    title_id = args.title_id.strip().upper()
    if not TITLE_ID_RE.fullmatch(title_id):
        raise ValueError("--title-id must match format like CUSA00123")

    local_dir = Path(args.local_dir).expanduser().resolve()
    if not local_dir.is_dir():
        raise ValueError(f"--local-dir is not a directory: {local_dir}")
    if not any(p.is_file() for p in local_dir.rglob("*")):
        raise ValueError("--local-dir has no files to sync")
    return local_dir, title_id


def connect_ftp(ip: str, port: int) -> ftplib.FTP:
    ports = [port]
    if port == 2121:
        ports.append(1337)

    errors: list[str] = []
    for current_port in ports:
        ftp = ftplib.FTP()
        try:
            ftp.connect(ip, current_port, timeout=10)
            ftp.login()
            print(f"Connected to {ip}:{current_port}")
            return ftp
        except Exception as exc:  # pragma: no cover - network path
            errors.append(f"{current_port}: {exc}")
            try:
                ftp.close()
            except Exception:
                pass
    raise ConnectionError("unable to connect to FTP server (" + "; ".join(errors) + ")")


def ensure_remote_dir(ftp: ftplib.FTP, path: str) -> None:
    current = ""
    for part in path.split("/"):
        if not part:
            continue
        current = f"{current}/{part}"
        try:
            ftp.mkd(current)
        except ftplib.error_perm as exc:
            if not str(exc).startswith("550"):
                raise


def remote_mdtm(ftp: ftplib.FTP, remote_file: str) -> datetime | None:
    try:
        reply = ftp.sendcmd(f"MDTM {remote_file}")
    except ftplib.all_errors:
        return None
    if not reply.startswith("213 "):
        return None
    value = reply[4:].strip()
    try:
        return datetime.strptime(value, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def needs_upload(ftp: ftplib.FTP, local_file: Path, remote_file: str) -> bool:
    local_size = local_file.stat().st_size
    try:
        remote_size = ftp.size(remote_file)
    except ftplib.all_errors:
        return True
    if remote_size != local_size:
        return True

    remote_time = remote_mdtm(ftp, remote_file)
    if remote_time is None:
        return False

    local_time = datetime.fromtimestamp(local_file.stat().st_mtime, tz=timezone.utc)
    return local_time > remote_time


def sync_tree(ftp: ftplib.FTP, local_dir: Path, remote_root: str) -> SyncStats:
    stats = SyncStats()
    ensure_remote_dir(ftp, remote_root)
    files = sorted((p for p in local_dir.rglob("*") if p.is_file()), key=lambda p: p.as_posix())
    for local_file in files:
        rel = local_file.relative_to(local_dir).as_posix()
        remote_file = posixpath.join(remote_root, rel)
        ensure_remote_dir(ftp, posixpath.dirname(remote_file))

        if not needs_upload(ftp, local_file, remote_file):
            stats.skipped += 1
            continue

        with local_file.open("rb") as handle:
            ftp.storbinary(f"STOR {remote_file}", handle)
        try:
            os.utime(local_file, None)
        except OSError:
            pass
        print(f"Uploaded {rel}")
        stats.uploaded += 1
    return stats


def main() -> int:
    args = parse_args()
    try:
        local_dir, title_id = validate_args(args)
        ftp = connect_ftp(args.ip.strip(), args.port)
    except (ValueError, ConnectionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    remote_root = posixpath.join(AFSP_ROOT, title_id)
    try:
        stats = sync_tree(ftp, local_dir, remote_root)
    except Exception as exc:  # pragma: no cover - network path
        print(f"error: sync failed: {exc}", file=sys.stderr)
        return 1
    finally:
        try:
            ftp.quit()
        except Exception:
            pass

    print(f"Sync complete: uploaded={stats.uploaded}, skipped={stats.skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
