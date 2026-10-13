"""Tiny JSON-backed job state tracker."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Literal

from ugc_pipeline.job.spec import JobSpec

StageStatus = Literal["pending", "running", "done", "failed"]


class JobState:
    def __init__(self, spec: JobSpec) -> None:
        self.path = spec.work_dir / "state.json"
        self._data: dict[str, object] = {"job_id": spec.job_id, "stages": {}}

    def mark(self, stage: str, status: StageStatus, detail: str = "") -> None:
        stages = self._data.setdefault("stages", {})
        assert isinstance(stages, dict)
        stages[stage] = {"status": status, "detail": detail, "ts": time.time()}
        self._flush()

    def _flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def read(self) -> dict[str, object]:
        if not self.path.exists():
            return self._data
        return json.loads(self.path.read_text(encoding="utf-8"))