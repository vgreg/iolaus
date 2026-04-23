# CLI Options

Iolaus automatically adds two CLI options to every decorated command.

## `--config`, `-c`

Merge an extra config file on top of the base settings.

```bash
python cli.py train --config prod.toml
python cli.py train -c prod.toml
```

The extra file is loaded and merged using Dynaconf. Keys in the extra file override matching keys in the base settings.

## `--set`, `-s`

Override individual config values directly from the command line.

```bash
python cli.py train --set model__lr=0.01
python cli.py train -s model__lr=0.01 -s db__host=remote
```

Use `__` (double underscore) as a separator for nested keys. For example, `model__lr=0.01` sets the `lr` key inside the `model` section.

Multiple `--set` flags can be used in a single invocation.

## Combining options

Both options can be used together. `--set` overrides take the highest precedence:

```bash
python cli.py train --config prod.toml --set model__lr=0.01
```

## Run artifacts

Every invocation creates a timestamped run directory:

```
outputs/
└── <command_name>/
    └── YYYY-MM-DD/
        └── HH-MM-SS/
            ├── run.log       # log output
            └── config.json   # merged config snapshot
```

The output base directory defaults to `outputs/` but can be configured via the `output_dir` parameter on the `command()` factory.

## Injected parameters

Your command function can optionally declare these parameters to receive them:

| Parameter | Type | Description |
|-----------|------|-------------|
| `settings` | `Dynaconf` | The fully merged configuration object |
| `run_dir` | `Path` | Path to the current run's output directory |

Both are opt-in: only injected if declared in your function signature.
