"""BaseProcessor contract shared by every pipeline stage."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ugc_pipeline.job.spec import JobSpec


@dataclass(slots=True)
class JobContext:
    spec: JobSpec
    config: dict[str, Any]
    artifacts: dict[str, "JobResult"] = field(default_factory=dict)

    def stage_dir(self, stage: str) -> Path:
        d = self.spec.work_dir / stage
        d.mkdir(parents=True, exist_ok=True)
        return d


@dataclass(slots=True)
class JobResult:
    ok: bool
    output_path: Path | None = None
    error: str | None = None
    metrics: dict[str, float] = field(default_factory=dict)


class BaseProcessor:
    name: str = "base"

    def process(self, ctx: JobContext) -> JobResult:
        raise NotImplementedError

    def _ok(self, path: Path | None = None, **metrics: float) -> JobResult:
        return JobResult(ok=True, output_path=path, metrics=metrics)

    def _fail(self, err: str) -> JobResult:
        return JobResult(ok=False, error=err)