"""Tests for iolaus.logging."""

import json
from pathlib import Path

from dynaconf import Dynaconf

from iolaus.logging import save_config_snapshot, setup_logging


def test_setup_logging_creates_run_dir(tmp_path: Path) -> None:
    """setup_logging creates the timestamped run directory."""
    run_dir = setup_logging("mycommand", tmp_path)
    assert run_dir.exists()
    assert run_dir.is_dir()
    # Should be nested under command name
    assert "mycommand" in str(run_dir)


def test_setup_logging_creates_log_file(tmp_path: Path) -> None:
    """A run.log file is created in the run directory."""
    run_dir = setup_logging("mycommand", tmp_path)
    assert (run_dir / "run.log").exists()


def test_setup_logging_directory_structure(tmp_path: Path) -> None:
    """Run dir follows the pattern base/command/YYYY-MM-DD/HH-MM-SS."""
    run_dir = setup_logging("analyze", tmp_path)
    # The relative path from tmp_path should have 4 parts:
    # analyze / YYYY-MM-DD / HH-MM-SS
    rel = run_dir.relative_to(tmp_path)
    parts = rel.parts
    assert len(parts) == 3
    assert parts[0] == "analyze"


def test_save_config_snapshot(tmp_path: Path) -> None:
    """save_config_snapshot writes a valid JSON config file."""
    settings = Dynaconf()
    settings.set("model.lr", 0.001)
    settings.set("db.host", "localhost")

    save_config_snapshot(settings, tmp_path)

    config_path = tmp_path / "config.json"
    assert config_path.exists()

    snapshot = json.loads(config_path.read_text())
    assert snapshot["MODEL"]["lr"] == 0.001
    assert snapshot["DB"]["host"] == "localhost"
