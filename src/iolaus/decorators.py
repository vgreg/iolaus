"""The ``command`` decorator factory — the central public API of Iolaus."""

from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any

import typer
from dynaconf import Dynaconf

from iolaus.logging import save_config_snapshot, setup_logging
from iolaus.settings import build_settings

_EXTRA_PARAMS = [
    inspect.Parameter(
        "extra_config",
        inspect.Parameter.KEYWORD_ONLY,
        default=None,
        annotation=Annotated[
            Path | None,
            typer.Option(
                "--config",
                "-c",
                help="Extra config file to merge on top of base settings.",
            ),
        ],
    ),
    inspect.Parameter(
        "override",
        inspect.Parameter.KEYWORD_ONLY,
        default=[],
        annotation=Annotated[
            list[str],
            typer.Option(
                "--set",
                "-s",
                help=(
                    "Override a config value. Use __ for nesting: --set model__lr=0.01"
                ),
            ),
        ],
    ),
]


def command(
    app: typer.Typer,
    base_settings: Dynaconf,
    output_dir: Path = Path("outputs"),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator factory. Bind once, reuse as a decorator on every command.

    Args:
        app: The Typer application to register commands on.
        base_settings: Base Dynaconf settings instance.
        output_dir: Root directory for run artifacts.

    Returns:
        A decorator that registers the function as a Typer command with
        automatic config merging and run logging.

    Example::

        cmd = command(app, settings)

        @cmd
        def my_command(settings=None, run_dir=None):
            ...
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        sig = inspect.signature(func)
        existing = list(sig.parameters.values())
        existing_names = {p.name for p in existing}
        extra = [p for p in _EXTRA_PARAMS if p.name not in existing_names]
        new_sig = sig.replace(parameters=existing + extra)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            extra_config: Path | None = kwargs.pop("extra_config", None)
            overrides: list[str] = kwargs.pop("override", [])

            merged_settings = build_settings(base_settings, extra_config, overrides)
            run_dir = setup_logging(func.__name__, output_dir)
            save_config_snapshot(merged_settings, run_dir)

            if "settings" in sig.parameters:
                kwargs["settings"] = merged_settings
            if "run_dir" in sig.parameters:
                kwargs["run_dir"] = run_dir

            return func(*args, **kwargs)

        wrapper.__signature__ = new_sig  # type: ignore[attr-defined]
        app.command()(wrapper)
        return func  # return unwrapped original so it is unit-testable without Typer

    return decorator
