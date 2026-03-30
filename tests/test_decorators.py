"""Tests for iolaus.decorators."""

from pathlib import Path

import typer
from dynaconf import Dynaconf
from typer.testing import CliRunner

from iolaus.decorators import command

runner = CliRunner()


def _make_multi_command(app: typer.Typer) -> None:
    """Register a dummy command so Typer uses subcommand mode."""

    @app.command()
    def _noop() -> None:
        pass


def test_command_runs(
    app: typer.Typer, base_settings: Dynaconf, tmp_path: Path
) -> None:
    """A decorated command executes successfully via Typer."""
    cmd = command(app, base_settings, output_dir=tmp_path)
    captured: dict[str, object] = {}

    @cmd
    def train(
        epochs: int = 10,
        settings=None,
        run_dir=None,
    ) -> None:
        captured["settings"] = settings
        captured["run_dir"] = run_dir

    _make_multi_command(app)
    result = runner.invoke(app, ["train", "--epochs", "5"])
    assert result.exit_code == 0
    assert captured["settings"] is not None
    assert isinstance(captured["run_dir"], Path)
    assert captured["run_dir"].exists()  # type: ignore[union-attr]


def test_set_override_applies(
    app: typer.Typer, base_settings: Dynaconf, tmp_path: Path
) -> None:
    """--set overrides are applied to injected settings."""
    cmd = command(app, base_settings, output_dir=tmp_path)
    captured: dict[str, object] = {}

    @cmd
    def train(settings=None) -> None:
        captured["settings"] = settings

    _make_multi_command(app)
    result = runner.invoke(app, ["train", "--set", "model__lr=0.1"])
    assert result.exit_code == 0
    import pytest

    assert float(captured["settings"].model.lr) == pytest.approx(0.1)  # type: ignore[union-attr]


def test_extra_config_merges(
    app: typer.Typer, base_settings: Dynaconf, tmp_path: Path
) -> None:
    """--config merges an extra config file on top of base settings."""
    extra = tmp_path / "extra.toml"
    extra.write_text('[db]\nhost = "remote"\n')
    cmd = command(app, base_settings, output_dir=tmp_path)
    captured: dict[str, object] = {}

    @cmd
    def run_cmd(settings=None) -> None:
        captured["settings"] = settings

    _make_multi_command(app)
    result = runner.invoke(
        app, ["run-cmd", "--config", str(extra)]
    )
    assert result.exit_code == 0
    assert captured["settings"].db.host == "remote"  # type: ignore[union-attr]


def test_original_function_is_callable_directly(
    app: typer.Typer, base_settings: Dynaconf, tmp_path: Path
) -> None:
    """The unwrapped function is importable and callable without Typer."""
    cmd = command(app, base_settings, output_dir=tmp_path)

    @cmd
    def process(x: int = 1) -> int:
        return x * 2

    assert process(x=3) == 6


def test_run_artifacts_created(
    app: typer.Typer, base_settings: Dynaconf, tmp_path: Path
) -> None:
    """Each run creates run.log and config.json in the run directory."""
    cmd = command(app, base_settings, output_dir=tmp_path)
    captured: dict[str, object] = {}

    @cmd
    def analyze(run_dir=None) -> None:
        captured["run_dir"] = run_dir

    _make_multi_command(app)
    result = runner.invoke(app, ["analyze"])
    assert result.exit_code == 0
    run_dir = captured["run_dir"]
    assert isinstance(run_dir, Path)
    assert (run_dir / "run.log").exists()
    assert (run_dir / "config.json").exists()


def test_no_injection_when_not_declared(
    app: typer.Typer, base_settings: Dynaconf, tmp_path: Path
) -> None:
    """settings/run_dir are not injected if not in the function signature."""
    cmd = command(app, base_settings, output_dir=tmp_path)
    captured: dict[str, object] = {}

    @cmd
    def simple(x: int = 1) -> None:
        captured["x"] = x

    _make_multi_command(app)
    result = runner.invoke(app, ["simple"])
    assert result.exit_code == 0
    assert captured["x"] == 1
