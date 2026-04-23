# Iolaus — Claude Code Guide

## Project overview

Iolaus is a lightweight Python framework for research data analysis projects. It wires together Dynaconf (config), Typer (CLI), and a custom run-logging system into a single decorator-based API. Every command run produces a timestamped output directory with a merged config snapshot and log file.

## Tech stack

- **Python >= 3.11** (targets 3.11–3.14)
- **Dynaconf** — configuration management
- **Typer** — CLI framework
- **uv** — package/dependency management
- **Hatchling** — build backend
- **pytest** — testing
- **ruff** — linting and formatting
- **mypy** (strict mode) — type checking
- **MkDocs Material** — documentation
- **bump-my-version** — version bumping

## Repository layout

```
src/iolaus/          # Library source (src layout)
  __init__.py        # Public API exports
  decorators.py      # command() decorator factory
  settings.py        # Dynaconf helpers / config merging
  logging.py         # Run directory setup, logging, config snapshots
  py.typed           # PEP 561 marker
tests/               # pytest test suite
docs/                # MkDocs documentation pages
.github/workflows/   # CI and publish workflows
```

## Common commands

```bash
uv sync --all-extras          # Install all dependencies
uv run pytest                 # Run tests
uv run pytest --cov=iolaus    # Run tests with coverage
uv run ruff check src/ tests/ # Lint
uv run ruff format src/ tests/ # Format
uv run mypy src/              # Type check
uv run mkdocs serve           # Local docs server
uv run pre-commit run --all-files  # Run all pre-commit hooks
```

## Key design decisions

- **src/ layout** — prevents accidental local imports during testing
- **`__` separator** for nested config keys (Dynaconf native convention)
- **`settings`/`run_dir` injection** is opt-in: only injected if the function signature declares them
- **Decorator returns the unwrapped original function** so it can be unit-tested without Typer
- **`basicConfig(force=True)`** ensures each command invocation gets its own log handlers
- **Config snapshots** are JSON (human-readable, diff-friendly, no extra dependency)

## Coding conventions

- Follow ruff's selected rules: E, F, I, UP
- Use Google-style docstrings (for mkdocstrings compatibility)
- Type annotations on all public APIs (mypy strict mode)
- Tests use `tmp_path` fixtures for isolation — no leftover artifacts
