"""Stage 6 — final composite render of the UGC ad video."""
from __future__ import annotations

from ugc_pipeline.processors.base import BaseProcessor, JobContext, JobResult
from ugc_pipeline.services.ffmpeg import FFmpegDriver


class RenderProcessor(BaseProcessor):
    name = "render"

    def process(self, ctx: JobContext) -> JobResult:
        cfg = ctx.config.get("render", {})
        driver = FFmpegDriver(
            codec=cfg.get("codec", "libx264"),
            fallback_codec=cfg.get("fallback_codec", "libx264"),
            crf=int(cfg.get("crf", 20)),
            resolution=cfg.get("resolution", "1080x1920"),
            fps=int(cfg.get("fps", 30)),
        )
        out = ctx.spec.output_dir / f"{ctx.spec.job_id}_ugc_ad.mp4"
        driver.composite(
            avatar=ctx.artifacts["avatar_anim"].output_path,  # type: ignore[arg-type]
            broll=ctx.artifacts["broll_match"].output_path,  # type: ignore[arg-type]
            captions=ctx.artifacts["caption_burn"].output_path,  # type: ignore[arg-type]
            audio=ctx.artifacts["voice_synth"].output_path,  # type: ignore[arg-type]
            out=out,
        )
        return self._ok(out)