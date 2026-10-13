"""JobSpec — the immutable description of one UGC ad generation run."""
from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class JobSpec:
    job_id: str
    brief_path: Path
    product_path: Path
    avatar_path: Path | None
    output_dir: Path
    config_path: Path
    stage_chain: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_paths(
        cls,
        *,
        brief_path: Path,
        product_path: Path,
        avatar_path: Path | None,
        output_dir: Path,
        config_path: Path,
    ) -> "JobSpec":
        brief_path = brief_path.resolve()
        product_path = product_path.resolve()
        avatar = avatar_path.resolve() if avatar_path else None
        seed = f"{brief_path}:{product_path}:{avatar}:{uuid.uuid4().hex}"
        job_id = hashlib.sha1(seed.encode()).hexdigest()[:12]
        return cls(
            job_id=job_id,
            brief_path=brief_path,
            product_path=product_path,
            avatar_path=avatar,
            output_dir=output_dir.resolve(),
            config_path=config_path.resolve(),
        )

    @property
    def work_dir(self) -> Path:
        return Path("cache/jobs") / self.job_id

    def fingerprint(self) -> str:
        parts = [self.job_id, self.brief_path.name, self.product_path.name]
        return hashlib.sha256("|".join(parts).encode()).hexdigest()