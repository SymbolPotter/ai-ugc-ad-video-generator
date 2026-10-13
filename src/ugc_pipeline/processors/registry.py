"""Stage name -> processor instance registry."""
from __future__ import annotations

from typing import Any

from ugc_pipeline.processors.avatar_anim import AvatarAnimProcessor
from ugc_pipeline.processors.base import BaseProcessor
from ugc_pipeline.processors.broll_match import BrollMatchProcessor
from ugc_pipeline.processors.caption_burn import CaptionBurnProcessor
from ugc_pipeline.processors.render import RenderProcessor
from ugc_pipeline.processors.script_gen import ScriptGenProcessor
from ugc_pipeline.processors.voice_synth import VoiceSynthProcessor

_BUILDERS: dict[str, type[BaseProcessor]] = {
    "script_gen": ScriptGenProcessor,
    "voice_synth": VoiceSynthProcessor,
    "avatar_anim": AvatarAnimProcessor,
    "broll_match": BrollMatchProcessor,
    "caption_burn": CaptionBurnProcessor,
    "render": RenderProcessor,
}


def build_chain(stages: list[str], config: dict[str, Any]) -> list[BaseProcessor]:
    chain: list[BaseProcessor] = []
    for stage in stages:
        builder = _BUILDERS.get(stage)
        if builder is None:
            raise KeyError(f"unknown stage: {stage!r}")
        chain.append(builder())  # type: ignore[call-arg]
    return chain