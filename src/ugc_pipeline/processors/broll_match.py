"""Stage 4 — retrieve matching b-roll clips for the script beats."""
from __future__ import annotations

import json

from ugc_pipeline.processors.base import BaseProcessor, JobContext, JobResult
from ugc_pipeline.services.broll_index import BrollIndex


class BrollMatchProcessor(BaseProcessor):
    name = "broll_match"

    def process(self, ctx: JobContext) -> JobResult:
        cfg = ctx.config.get("broll_match", {})
        script = json.loads(ctx.artifacts["script_gen"].output_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
        index = BrollIndex.load(cfg["index"])
        picks = index.match(
            beats=script["beats"],
            top_k=int(cfg.get("top_k", 6)),
            min_score=float(cfg.get("min_score", 0.42)),
        )
        out = ctx.stage_dir(self.name) / "broll.json"
        out.write_text(json.dumps(picks, indent=2), encoding="utf-8")
        return self._ok(out, clips=float(len(picks)))