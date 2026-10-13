"""FFmpegDriver — subprocess-safe compositor for the final render."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from ugc_pipeline.logging import get_logger

log = get_logger("services.ffmpeg")

_ALLOWED_CODECS = {"libx264", "h264_nvenc", "hevc_nvenc", "libvpx-vp9"}


class FFmpegDriver:
    def __init__(
        self,
        *,
        codec: str,
        fallback_codec: str,
        crf: int,
        resolution: str,
        fps: int,
    ) -> None:
        if codec not in _ALLOWED_CODECS:
            raise ValueError(f"codec not allowlisted: {codec}")
        self.codec = codec
        self.fallback_codec = fallback_codec
        self.crf = crf
        self.resolution = resolution
        self.fps = fps

    def composite(
        self,
        *,
        avatar: Path,
        broll: Path,
        captions: Path,
        audio: Path,
        out: Path,
    ) -> Path:
        if shutil.which("ffmpeg") is None:
            raise RuntimeError("ffmpeg binary not found on PATH")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(avatar),
            "-i", str(broll),
            "-i", str(audio),
            "-vf", f"subtitles={captions},scale={self.resolution.replace('x', ':')}",
            "-c:v", self.codec,
            "-crf", str(self.crf),
            "-r", str(self.fps),
            "-c:a", "aac",
            "-b:a", "192k",
            str(out),
        ]
        log.debug("ffmpeg cmd: %s", " ".join(cmd))
        proc = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        if proc.returncode != 0:
            log.error("ffmpeg failed: %s", proc.stderr[-2000:])
            raise RuntimeError(f"ffmpeg exited {proc.returncode}")
        return out
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>