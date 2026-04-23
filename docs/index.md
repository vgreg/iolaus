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

## Next steps

- [Getting Started](getting-started.md) — installation and first project
- [Configuration](configuration.md) — config files, merging, and overrides
- [CLI](cli.md) — command-line options added by Iolaus
- [API Reference](api-reference.md) — full API documentation
