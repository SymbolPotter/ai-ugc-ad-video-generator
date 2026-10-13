# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | ✅        |
| 0.3.x   | ⚠️ security fixes only |
| < 0.3   | ❌        |

## Reporting a vulnerability

Do **not** open a public issue for security bugs. Email
`security@ugc-ad-pipeline.dev` with:

- Affected component (`ingest`, `processors`, `output`, `api`).
- Reproduction steps.
- Impact assessment (RCE, path traversal, prompt injection into the
  copy generator, model weight tampering, etc.).

We acknowledge within 72 hours and aim to patch critical issues within
14 days.

## Threat model

This tool ingests untrusted media and untrusted ad briefs. The primary
attack surfaces are:

- **Path traversal** in ingest handlers writing to `cache/` or `renders/`.
- **Prompt injection** via ad brief text reaching the LLM copy stage.
- **Weight poisoning** — only load models from the pinned hashes in
  `models/manifest.lock.json`.
- **Arbitrary code execution** via `eval` in template rendering. We do
  not use `eval`. If you find one, it's a bug.

## Hardening defaults

- FFmpeg subprocess calls run with `shell=False` and an allowlisted
  codec set.
- The API binds to `127.0.0.1` by default.
- Uploaded files are size-capped and MIME-sniffed before ingest.

## Out of scope

- Denial of service from absurdly large input videos.
- Issues requiring local admin on the host.
- Anything in `examples/` — that's demo code.