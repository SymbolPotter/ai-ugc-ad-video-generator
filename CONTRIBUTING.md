# Contributing to ai-ugc-ad-video-generator

Thanks for wanting to push the UGC ad pipeline forward. This repo is a
pipeline/worker style codebase: **ingest handlers** pull raw material in,
**processors** transform it, **output drivers** emit finished ad videos,
and **job utils** keep the whole thing scheduled and observable.

## Ground rules

1. One job, one worker. Every processor must be idempotent — a re-run of
   the same `JobSpec` must produce byte-identical output or fail loudly.
2. No blocking calls in handlers. Handlers enqueue; workers execute.
3. Every new processor ships with a fixture in `tests/fixtures/` and a
   unit test in `tests/`.
4. Model weights are never committed. Pull them via `scripts/fetch_models.py`.

## Dev setup

```bash
python -m venv .venv
. .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
pytest -q
```

## Adding a processor

1. Create `src/ugc_pipeline/processors/your_stage.py`.
2. Subclass `BaseProcessor`, implement `process(job) -> JobResult`.
3. Register it in `src/ugc_pipeline/processors/registry.py`.
4. Add it to the default chain in `config/pipeline.toml`.
5. Write the test. If it has no test, it does not merge.

## Branch + commit style

- `feat/`, `fix/`, `chore/`, `docs/` prefixes.
- Conventional commits. Squash on merge.
- PRs need one reviewer from `CODEOWNERS`.

## Style

- `ruff` + `black` + `mypy --strict` on `src/`.
- Type hints mandatory on public functions.
- No `print()` in library code — use the `ugc_pipeline.logging` logger.

## Code of conduct

Be decent. This is a hobbyist-friendly OSS project. Harassment gets you
removed without a debate.