"""JobRunner — drives a JobSpec through the processor chain."""
from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from ugc_pipeline.job.spec import JobSpec
from ugc_pipeline.logging import get_logger
from ugc_pipeline.processors.base import BaseProcessor, JobContext, JobResult
from ugc_pipeline.processors.registry import build_chain

log = get_logger("job.runner")


class JobRunner:
    def __init__(self, chain: list[BaseProcessor], raw_config: dict[str, Any]) -> None:
        self._chain = chain
        self._config = raw_config

    @classmethod
    def from_config(cls, config_path: Path) -> "JobRunner":
        with config_path.open("rb") as fh:
            raw = tomllib.load(fh)
        chain = build_chain(raw.get("chain", {}).get("stages", []), raw)
        return cls(chain=chain, raw_config=raw)

    def run(self, spec: JobSpec) -> JobResult:
        spec.work_dir.mkdir(parents=True, exist_ok=True)
        spec.output_dir.mkdir(parents=True, exist_ok=True)
        ctx = JobContext(spec=spec, config=self._config)
        result: JobResult | None = None
        for processor in self._chain:
            log.info("stage %s start job=%s", processor.name, spec.job_id)
            result = processor.process(ctx)
            if not result.ok:
                log.error("stage %s failed: %s", processor.name, result.error)
                if self._config.get("run", {}).get("fail_fast"):
                    return result
            ctx.artifacts[processor.name] = result
        if result is None:
            raise RuntimeError("empty processor chain")
        return result