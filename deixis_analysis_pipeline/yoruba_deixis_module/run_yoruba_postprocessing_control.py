#!/usr/bin/env python3
"""Translate and compare the latest unrestricted Yoruba control sessions."""

import subprocess
import sys
from pathlib import Path


SESSION_PREFIXES = [
    "yoruba_control_gpt4o_",
    "yoruba_control_claude_",
    "yoruba_control_deepseek_",
]


def latest_session_for_prefix(generation_logs_dir: Path, prefix: str) -> Path:
    matches = sorted(
        [path for path in generation_logs_dir.iterdir() if path.is_dir() and path.name.startswith(prefix)],
        key=lambda path: path.name,
    )
    if not matches:
        raise FileNotFoundError(f"No sessions found for prefix {prefix}")
    return matches[-1]


def latest_bilingual_dir(bilingual_root: Path, session_name: str) -> Path:
    matches = sorted(
        [path for path in bilingual_root.iterdir() if path.is_dir() and path.name.startswith(f"{session_name}_bilingual_")],
        key=lambda path: path.name,
    )
    if not matches:
        raise FileNotFoundError(f"No bilingual session found for source session {session_name}")
    return matches[-1]


def run_command(command, description, workdir):
    print(f"\n[RUN] {description}")
    print("=" * 72)
    result = subprocess.run(command, cwd=workdir, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        raise RuntimeError(f"{description} failed with exit code {result.returncode}")
    if result.stdout:
        print(result.stdout)


def main():
    module_dir = Path(__file__).resolve().parent
    pipeline_dir = module_dir.parent
    repo_root = pipeline_dir.parent
    generation_logs_dir = pipeline_dir / "generation_logs"
    bilingual_root = module_dir / "outputs" / "bilingual_sessions"

    for prefix in SESSION_PREFIXES:
        session_dir = latest_session_for_prefix(generation_logs_dir, prefix)

        run_command(
            [
                sys.executable,
                str(module_dir / "translate_yoruba_session.py"),
                str(session_dir),
            ],
            f"Translate unrestricted Yoruba session {session_dir.name}",
            str(repo_root),
        )

        bilingual_dir = latest_bilingual_dir(bilingual_root, session_dir.name)

        run_command(
            [
                sys.executable,
                str(module_dir / "compare_yoruba_to_published_english.py"),
                str(bilingual_dir),
            ],
            f"Compare unrestricted session {bilingual_dir.name} to published English baseline",
            str(repo_root),
        )

    print("\n[DONE] Latest unrestricted Yoruba control sessions translated and paired with the published English baseline.")


if __name__ == "__main__":
    main()
