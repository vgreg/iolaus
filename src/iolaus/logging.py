"""Run directory setup, logging configuration, and config snapshots."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from dynaconf import Dynaconf


def setup_logging(command_name: str, base_dir: Path) -> Path:
    """Create a timestamped run directory and configure logging.

    Args:
        command_name: Name of the command (used as a subdirectory).
        base_dir: Root output directory.

    Returns:
        Path to the created run directory.
    """
    run_dir = base_dir / command_name / datetime.now().strftime("%Y-%m-%d/%H-%M-%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(run_dir / "run.log"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    return run_dir


def save_config_snapshot(settings: Dynaconf, run_dir: Path) -> None:
    """Write the full merged config as a JSON snapshot.

    Args:
        settings: The merged Dynaconf settings instance.
        run_dir: Directory to write ``config.json`` into.
    """
    snapshot = settings.as_dict()
    (run_dir / "config.json").write_text(json.dumps(snapshot, indent=2, default=str))
