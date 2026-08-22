# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-22

Initial release.

### Added

- `command()` decorator factory that registers a function as a Typer command and wires in configuration and run logging.
- Configuration merging via Dynaconf: base settings, extra config files passed with `--config`, and individual key overrides passed with `--set` (using `__` for nested keys).
- Timestamped run directories under `outputs/<command>/<date>/<time>/`, each containing a `run.log` and a `config.json` snapshot of the merged configuration.
- Opt-in injection of `settings` and `run_dir`, only for functions that declare them in their signature.
- Type annotations throughout, with a `py.typed` marker for downstream type checkers.

[Unreleased]: https://github.com/vgreg/iolaus/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vgreg/iolaus/releases/tag/v0.1.0
