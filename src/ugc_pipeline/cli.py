"""Typer entrypoint for the ai-ugc-ad-video-generator CLI."""
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ugc_pipeline.job.runner import JobRunner
from ugc_pipeline.job.spec import JobSpec
from ugc_pipeline.logging import configure_logging

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


@app.command()
def generate(
    brief: Annotated[Path, typer.Option("--brief", "-b", exists=True, dir_okay=False)],
    product: Annotated[Path, typer.Option("--product", "-p", exists=True)],
    avatar: Annotated[Path | None, typer.Option("--avatar", "-a", exists=True)] = None,
    out: Annotated[Path, typer.Option("--out", "-o")] = Path("renders"),
    config: Annotated[Path, typer.Option("--config", "-c")] = Path("config/pipeline.toml"),
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Run a full UGC ad pipeline for one brief."""
    configure_logging(verbose=verbose)
    spec = JobSpec.from_paths(
        brief_path=brief,
        product_path=product,
        avatar_path=avatar,
        output_dir=out,
        config_path=config,
    )
    runner = JobRunner.from_config(config)
    result = runner.run(spec)
    console.print(f"[bold green]done[/] -> {result.output_path}")


@app.command()
def serve(
    host: Annotated[str, typer.Option()] = "127.0.0.1",
    port: Annotated[int, typer.Option()] = 8765,
) -> None:
    """Start the local HTTP API for job submission."""
    from ugc_pipeline.api.server import run_server

    run_server(host=host, port=port)


if __name__ == "__main__":
    app()