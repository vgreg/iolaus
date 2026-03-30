# Getting Started

## Installation

Install from PyPI:

```bash
pip install iolaus
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add iolaus
```

## Requirements

- Python 3.11 or later
- [Dynaconf](https://www.dynaconf.com/) and [Typer](https://typer.tiangolo.com/) (installed automatically)

## Your first project

### 1. Create a config file

```toml
# settings.toml
[model]
lr = 0.001
epochs = 10

[db]
host = "localhost"
port = 5432
```

### 2. Write your CLI

```python
# cli.py
from pathlib import Path
from dynaconf import Dynaconf
import typer
from iolaus import command

app = typer.Typer()
settings = Dynaconf(settings_files=["settings.toml"], envvar_prefix="MYAPP")
cmd = command(app, settings)

@cmd
def train(settings=None, run_dir=None):
    """Train the model."""
    print(f"Learning rate: {settings.model.lr}")
    print(f"Run artifacts in: {run_dir}")

if __name__ == "__main__":
    app()
```

### 3. Run it

```bash
python cli.py train
```

This creates a timestamped directory under `outputs/train/` containing:

- `run.log` — log output from the run
- `config.json` — full snapshot of the merged configuration

### 4. Override settings

```bash
# Merge an extra config file
python cli.py train --config prod.toml

# Override individual values
python cli.py train --set model__lr=0.01

# Combine both
python cli.py train --config prod.toml --set db__host=remote
```
