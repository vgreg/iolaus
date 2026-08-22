<p align="center">
  <img src="assets/iolaus.webp" alt="Iolaus, the companion who helped Heracles defeat the Hydra" width="220">
</p>

# Iolaus

**Iolaus** is a lightweight Python framework for research data analysis projects. It wires together [Dynaconf](https://www.dynaconf.com/), [Typer](https://typer.tiangolo.com/), and a custom run-logging system into a single decorator-based API.

## Core value proposition

Every command run produces a timestamped output directory containing a merged config snapshot and a log file, with zero boilerplate in your code.

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

Every run produces:

```
outputs/
└── analyze/
    └── 2025-03-29/
        └── 14-32-05/
            ├── run.log
            └── config.json
```

## Relationship to Hydra

Iolaus is inspired by [Hydra](https://hydra.cc/), which established the pattern of composable configuration files combined with timestamped output directories for research code. Iolaus is deliberately a lightweight alternative implementing only the subset of Hydra's features that I actually use in my own projects, built on [Dynaconf](https://www.dynaconf.com/) and [Typer](https://typer.tiangolo.com/) rather than on OmegaConf.

The trade-off is scope. Iolaus gives you a decorator, config merging, and a run directory, and nothing else. Hydra gives you a much larger system:

| | Iolaus | Hydra |
| --- | --- | --- |
| Config merging from files | Yes | Yes |
| CLI key overrides | Yes | Yes |
| Timestamped run directories | Yes | Yes |
| Config groups and defaults lists | No | Yes |
| Multirun and parameter sweeps | No | Yes |
| Structured (typed) configs | No | Yes |
| Object instantiation from config | No | Yes |
| Launcher plugins (Slurm, Ray, etc.) | No | Yes |

If Iolaus is not flexible enough, or if you need any of the features in the right-hand column, you should use Hydra instead. It is a mature and well-documented project, and Iolaus makes no attempt to match its scope.

## Next steps

- [Getting Started](getting-started.md) — installation and first project
- [Configuration](configuration.md) — config files, merging, and overrides
- [CLI](cli.md) — command-line options added by Iolaus
- [API Reference](api-reference.md) — full API documentation
