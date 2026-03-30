"""Shared test fixtures."""

from pathlib import Path

import pytest
import typer
from dynaconf import Dynaconf


@pytest.fixture
def base_settings(tmp_path: Path) -> Dynaconf:
    """Create a Dynaconf instance backed by a temporary TOML file."""
    cfg = tmp_path / "settings.toml"
    cfg.write_text('[model]\nlr = 0.001\n\n[db]\nhost = "localhost"\n')
    return Dynaconf(settings_files=[str(cfg)], envvar_prefix="TEST")


@pytest.fixture
def app() -> typer.Typer:
    """Create a fresh Typer application."""
    return typer.Typer()
