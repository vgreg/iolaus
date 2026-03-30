# Configuration

Iolaus uses [Dynaconf](https://www.dynaconf.com/) for configuration management. You define a base settings file, and Iolaus lets you layer additional config files and CLI overrides on top.

## Config file format

Iolaus supports any format Dynaconf supports: TOML, YAML, JSON, and `.env` files. TOML is recommended:

```toml
# settings.toml
[model]
lr = 0.001
epochs = 10

[db]
host = "localhost"
port = 5432
```

## Config merging

When you use the `--config` flag, Iolaus merges the extra config file on top of the base settings. Later values override earlier ones:

```bash
python cli.py train --config prod.toml
```

```toml
# prod.toml
[db]
host = "prod-db.example.com"
port = 5433
```

In this example, `db.host` and `db.port` are overridden, while `model.lr` and `model.epochs` retain their base values.

## CLI overrides with `--set`

Use `--set` (or `-s`) to override individual config values from the command line. Use `__` (double underscore) as a separator for nested keys:

```bash
python cli.py train --set model__lr=0.01 --set db__host=remote
```

This sets `model.lr` to `0.01` and `db.host` to `"remote"`.

Overrides applied via `--set` take precedence over both the base settings and any extra config file.

## Precedence order

From lowest to highest priority:

1. Base settings file(s) passed to `Dynaconf()`
2. Extra config file via `--config`
3. CLI overrides via `--set`

## Config snapshots

Every command run saves a `config.json` file in the run directory containing the full merged configuration. This makes runs reproducible — you can see exactly what settings were used.

## Accessing settings in your command

Declare a `settings` parameter in your function signature to receive the merged Dynaconf object:

```python
@cmd
def train(settings=None):
    lr = settings.model.lr
    host = settings.db.host
```

If you don't declare `settings`, it won't be injected — your command still runs, but without access to the config object.
