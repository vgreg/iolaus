"""Dynaconf helpers for config merging and overrides."""

from __future__ import annotations

from pathlib import Path

from dynaconf import Dynaconf


def build_settings(
    base: Dynaconf,
    extra_config: Path | None,
    overrides: list[str],
) -> Dynaconf:
    """Merge base settings, an optional extra config file, and CLI overrides.

    Args:
        base: The base Dynaconf settings instance.
        extra_config: Optional path to an additional config file to layer on top.
        overrides: List of ``key=value`` strings. Use ``__`` for nesting
            (e.g. ``model__lr=0.01``).

    Returns:
        A new Dynaconf instance with all sources merged.
    """
    files = list(base.settings_file or [])
    if extra_config:
        files.append(str(extra_config))

    merged = Dynaconf(
        settings_files=files,
        envvar_prefix=base.envvar_prefix_for_dynaconf or "APP",
    )

    for item in overrides:
        key, _, value = item.partition("=")
        merged.set(key.replace("__", "."), value)

    return merged
