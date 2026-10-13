"""Ingest handlers for brief, product media, and avatar reference."""
from __future__ import annotations

import mimetypes
import shutil
from pathlib import Path

from ugc_pipeline.logging import get_logger

log = get_logger("ingest.handlers")

_ALLOWED_MIME = {
    "video/mp4",
    "video/quicktime",
    "image/png",
    "image/jpeg",
    "text/plain",
    "application/json",
}
_MAX_UPLOAD_MB = 512


def _guard(path: Path, dest_root: Path) -> Path:
    dest_root = dest_root.resolve()
    dest = (dest_root / path.name).resolve()
    if dest_root not in dest.parents and dest != dest_root:
        raise ValueError(f"path traversal blocked: {path}")
    return dest


def _check_size(path: Path) -> None:
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > _MAX_UPLOAD_MB:
        raise ValueError(f"upload too large: {size_mb:.1f} MB > {_MAX_UPLOAD_MB} MB")


def _check_mime(path: Path) -> None:
    mime, _ = mimetypes.guess_type(path.name)
    if mime not in _ALLOWED_MIME:
        raise ValueError(f"unsupported mime type: {mime!r}")


def ingest_brief(src: Path, dest_root: Path) -> Path:
    _check_size(src)
    _check_mime(src)
    dest = _guard(src, dest_root / "brief")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    log.info("ingested brief %s -> %s", src.name, dest)
    return dest


def ingest_product_media(src: Path, dest_root: Path) -> Path:
    _check_size(src)
    _check_mime(src)
    dest = _guard(src, dest_root / "product")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    log.info("ingested product media %s -> %s", src.name, dest)
    return dest


def ingest_avatar_ref(src: Path, dest_root: Path) -> Path:
    _check_size(src)
    _check_mime(src)
    dest = _guard(src, dest_root / "avatar")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    log.info("ingested avatar ref %s -> %s", src.name, dest)
    return dest