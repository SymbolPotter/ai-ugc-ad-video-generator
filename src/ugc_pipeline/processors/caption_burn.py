"""Stage 5 — burn UGC-style captions onto the timeline."""
from __future__ import annotations

from ugc_pipeline.processors.base import BaseProcessor, JobContext, JobResult
from ugc_pipeline.services.captions import CaptionRenderer


class CaptionBurnProcessor(BaseProcessor):
    name = "caption_burn"

    def process(self, ctx: JobContext) -> JobResult:
        cfg = ctx.config.get("caption_burn", {})
        renderer = CaptionRenderer(
            style=cfg.get("style", "ugc-bold"),
            font=cfg.get("font"),
            position=cfg.get("position", "bottom-center"),
        )
        out = ctx.stage_dir(self.name) / "captions.ass"
        renderer.write_ass(
            script_path=ctx.artifacts["script_gen"].output_path,  # type: ignore[arg-type]
            audio_path=ctx.artifacts["voice_synth"].output_path,  # type: ignore[arg-type]
            out_path=out,
        )
        return self._ok(out)