"""Stage 3 — drive a talking-head avatar from the VO track."""
from __future__ import annotations

from ugc_pipeline.processors.base import BaseProcessor, JobContext, JobResult
from ugc_pipeline.services.avatar import TalkingHeadLite


class AvatarAnimProcessor(BaseProcessor):
    name = "avatar_anim"

    def process(self, ctx: JobContext) -> JobResult:
        cfg = ctx.config.get("avatar_anim", {})
        if ctx.spec.avatar_path is None:
            return self._fail("no avatar reference provided")
        vo = ctx.artifacts["voice_synth"].output_path
        if vo is None:
            return self._fail("missing voice track")
        engine = TalkingHeadLite(fps=int(cfg.get("fps", 30)))
        out = ctx.stage_dir(self.name) / "avatar.mp4"
        engine.render(reference=ctx.spec.avatar_path, audio=vo, out=out)
        return self._ok(out, frames=float(engine.last_frame_count))