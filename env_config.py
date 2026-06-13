"""Shared environment loading helpers for the repository."""

from __future__ import annotations

from pathlib import Path
from dotenv import load_dotenv


_LOADED = False


def load_project_env() -> None:
    """Load .env files from the repository root and common subdirectories once."""
    global _LOADED
    if _LOADED:
        return

    repo_root = Path(__file__).resolve().parent
    candidate_paths = [
        repo_root / ".env",
        repo_root / "deixis_analysis_pipeline" / ".env",
    ]

    for env_path in candidate_paths:
        if env_path.exists():
            load_dotenv(env_path, override=False)

    _LOADED = True
