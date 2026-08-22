<p align="center">
  <img src="https://raw.githubusercontent.com/vgreg/iolaus/main/docs/assets/iolaus.webp"
       alt="Iolaus, the companion who helped Heracles defeat the Hydra" width="200">
</p>

# Iolaus

> **Warning:** This project is under active development and is not yet stable. APIs may change without notice.

A lightweight Python framework for research data analysis projects. Iolaus wires together [Dynaconf](https://www.dynaconf.com/), [Typer](https://typer.tiangolo.com/), and a custom run-logging system into a single decorator-based API that adds automatic configuration management and reproducible run artifacts on every invocation.

**Documentation:** [www.vincentgregoire.com/iolaus](https://www.vincentgregoire.com/iolaus/)

## Features

- **Decorator-based API** — feels like FastAPI/Typer, with zero boilerplate
- **Automatic config management** — merge base settings, extra config files, and CLI overrides
- **Reproducible run artifacts** — every command run produces a timestamped output directory with a config snapshot and log file
- **Opt-in injection** — `settings` and `run_dir` are only injected if your function declares them

## Quick example

```python
from pathlib import Path
from dynaconf import Dynaconf
import typer
from iolaus import command

app = typer.Typer()
settings = Dynaconf(settings_files=["settings.toml"], envvar_prefix="MYAPP")
cmd = command(app, settings)

@cmd
def analyze(
    input: Path,
    verbose: bool = False,
    settings=None,   # injected by Iolaus
    run_dir: Path = None,  # injected by Iolaus
):
    """Run the analysis pipeline."""
    ...

@cmd
def report(settings=None):
    """Summarize the latest run."""
    ...

if __name__ == "__main__":
    app()
```

```bash
# Base invocation
python cli.py analyze data.csv

# Merge an extra config file
python cli.py analyze data.csv --config prod.yaml

# Override individual keys
python cli.py analyze data.csv --set model__lr=0.01 --set db__host=remote
```

> **Note:** Typer treats an application with exactly one registered command as a single-command CLI, and the command name is then left off the command line. These examples register two commands, so every invocation names the one to run.

Every run produces:

```
outputs/
└── analyze/
    └── 2025-03-29/
        └── 14-32-05/
            ├── run.log
            └── config.json
```

## Installation

```bash
pip install iolaus
```

Or with uv:

```bash
uv add iolaus
```

## Development

```bash
git clone https://github.com/vgreg/iolaus.git
cd iolaus
uv sync --all-extras
uv run pytest
```

## Relationship to Hydra

Iolaus is inspired by [Hydra](https://hydra.cc/), which established the pattern of composable configuration files combined with timestamped output directories for research code. Iolaus is deliberately a lightweight alternative implementing only the subset of Hydra's features that I actually use in my own projects, built on Dynaconf and Typer rather than on OmegaConf.

If Iolaus is not flexible enough, or if you need something it does not provide (config groups, multirun parameter sweeps, structured configs, object instantiation, or launcher plugins for clusters), you should use Hydra instead. It is a mature and well-documented project, and Iolaus makes no attempt to match its scope.

## License

MIT
