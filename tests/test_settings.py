"""Tests for iolaus.settings."""

from pathlib import Path

import pytest
from dynaconf import Dynaconf

from iolaus.settings import build_settings


def test_build_settings_base_only(base_settings: Dynaconf) -> None:
    """Base settings are preserved when no extras are provided."""
    merged = build_settings(base_settings, extra_config=None, overrides=[])
    assert merged.model.lr == pytest.approx(0.001)
    assert merged.db.host == "localhost"


def test_build_settings_extra_config(base_settings: Dynaconf, tmp_path: Path) -> None:
    """An extra config file overrides matching keys."""
    extra = tmp_path / "extra.toml"
    extra.write_text('[db]\nhost = "remote"\n')
    merged = build_settings(base_settings, extra_config=extra, overrides=[])
    assert merged.db.host == "remote"
    # Non-overridden keys should still be present
    assert merged.model.lr == pytest.approx(0.001)


def test_build_settings_overrides(base_settings: Dynaconf) -> None:
    """CLI --set overrides apply on top of base settings."""
    merged = build_settings(
        base_settings, extra_config=None, overrides=["model__lr=0.1"]
    )
    assert merged.model.lr == pytest.approx(0.1)


def test_build_settings_nested_override(base_settings: Dynaconf) -> None:
    """Double-underscore separator is converted to dot notation."""
    merged = build_settings(
        base_settings,
        extra_config=None,
        overrides=["db__host=newhost", "model__lr=0.5"],
    )
    assert merged.db.host == "newhost"
    assert merged.model.lr == pytest.approx(0.5)


def test_build_settings_extra_and_overrides(
    base_settings: Dynaconf, tmp_path: Path
) -> None:
    """Overrides take precedence over extra config file values."""
    extra = tmp_path / "extra.toml"
    extra.write_text('[db]\nhost = "staging"\n')
    merged = build_settings(
        base_settings, extra_config=extra, overrides=["db__host=production"]
    )
    assert merged.db.host == "production"


def test_build_settings_override_preserves_types(base_settings: Dynaconf) -> None:
    """Overrides are parsed as TOML so they keep their types, not bare strings."""
    merged = build_settings(
        base_settings,
        extra_config=None,
        overrides=["model__lr=0.01", "model__epochs=50", "debug=true"],
    )
    assert isinstance(merged.model.lr, float)
    assert isinstance(merged.model.epochs, int)
    assert isinstance(merged.debug, bool)
    assert merged.model.lr == pytest.approx(0.01)
    assert merged.model.epochs == 50
    assert merged.debug is True


def test_build_settings_override_non_toml_stays_string(
    base_settings: Dynaconf,
) -> None:
    """Values that are not valid TOML fall back to plain strings."""
    merged = build_settings(
        base_settings,
        extra_config=None,
        overrides=["db__host=remote", "out__path=/tmp/data.csv", "note=a=b"],
    )
    assert merged.db.host == "remote"
    assert merged.out.path == "/tmp/data.csv"
    assert merged.note == "a=b"
