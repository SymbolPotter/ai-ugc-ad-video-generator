"""Stage 2 — synthesize voiceover from the generated script."""
from __future__ import annotations

import json

from ugc_pipeline.processors.base import BaseProcessor, JobContext, JobResult
from ugc_pipeline.services.tts import PiperEngine


class VoiceSynthProcessor(BaseProcessor):
    name = "voice_synth"

    def process(self, ctx: JobContext) -> JobResult:
        cfg = ctx.config.get("voice_synth", {})
        script_path = ctx.artifacts["script_gen"].output_path
        if script_path is None:
            return self._fail("script_gen produced no output")
        script = json.loads(script_path.read_text(encoding="utf-8"))
        engine = PiperEngine(voice_pack=cfg["voice_pack"], speed=float(cfg.get("speed", 1.0)))
        wav = ctx.stage_dir(self.name) / "vo.wav"
        engine.synthesize(script["lines"], wav)
        return self._ok(wav, duration_s=engine.last_duration_s)