"""Stage 1 — generate the UGC ad script from the brief."""
from __future__ import annotations

from ugc_pipeline.models.copywriter import CopywriterModel
from ugc_pipeline.processors.base import BaseProcessor, JobContext, JobResult
from ugc_pipeline.services.brief_parser import parse_brief


class ScriptGenProcessor(BaseProcessor):
    name = "script_gen"

    def process(self, ctx: JobContext) -> JobResult:
        cfg = ctx.config.get("script_gen", {})
        brief = parse_brief(ctx.spec.brief_path)
        model = CopywriterModel.load(cfg["model"])
        script = model.write(
            brief=brief,
            max_tokens=int(cfg.get("max_tokens", 512)),
            temperature=float(cfg.get("temperature", 0.8)),
        )
        out = ctx.stage_dir(self.name) / "script.json"
        out.write_text(script.to_json(), encoding="utf-8")
        return self._ok(out, tokens=float(script.token_count))