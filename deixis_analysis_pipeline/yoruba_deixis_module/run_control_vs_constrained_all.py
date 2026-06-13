#!/usr/bin/env python3
"""Compare the latest unrestricted Yoruba bilingual sessions to the latest constrained ones."""

import subprocess
import sys
from pathlib import Path


SESSION_PREFIX_PAIRS = [
    ("yoruba_control_gpt4o_", ["yoruba_gpt4o_calibration_", "yoruba_gpt4o_"]),
    ("yoruba_control_claude_", ["yoruba_claude_calibration_", "yoruba_claude_"]),
    ("yoruba_control_deepseek_", ["yoruba_deepseek_calibration_", "yoruba_deepseek_"]),
]


def latest_session_for_prefix(root: Path, prefix: str) -> Path:
    matches = sorted(
        [path for path in root.iterdir() if path.is_dir() and path.name.startswith(prefix)],
        key=lambda path: path.name,
    )
    if not matches:
        raise FileNotFoundError(f"No sessions found for prefix {prefix}")
    return matches[-1]


def latest_session_for_any_prefix(root: Path, prefixes: list[str]) -> Path:
    for prefix in prefixes:
        matches = sorted(
            [path for path in root.iterdir() if path.is_dir() and path.name.startswith(prefix)],
            key=lambda path: path.name,
        )
        if matches:
            return matches[-1]
    raise FileNotFoundError(f"No sessions found for any prefix: {prefixes}")


def latest_bilingual_dir(root: Path, session_name: str) -> Path:
    matches = sorted(
        [path for path in root.iterdir() if path.is_dir() and path.name.startswith(f"{session_name}_bilingual_")],
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

    for control_prefix, constrained_prefixes in SESSION_PREFIX_PAIRS:
        control_session = latest_session_for_prefix(generation_logs_dir, control_prefix)
        constrained_session = latest_session_for_any_prefix(generation_logs_dir, constrained_prefixes)
        control_bilingual = latest_bilingual_dir(bilingual_root, control_session.name)
        constrained_bilingual = latest_bilingual_dir(bilingual_root, constrained_session.name)

        run_command(
            [
                sys.executable,
                str(module_dir / "compare_control_to_constrained.py"),
                str(control_bilingual),
                str(constrained_bilingual),
            ],
            f"Compare {control_bilingual.name} to {constrained_bilingual.name}",
            str(repo_root),
        )

    print("\n[DONE] Latest unrestricted-vs-constrained Yoruba comparisons completed for all three models.")


if __name__ == "__main__":
    main()
