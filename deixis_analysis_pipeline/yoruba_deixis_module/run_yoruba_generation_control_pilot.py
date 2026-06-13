#!/usr/bin/env python3
"""Run an unrestricted Yoruba control pilot on one dilemma for all models."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description, workdir):
    print(f"\n[RUN] {description}")
    print("=" * 72)
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(command, cwd=workdir, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        raise RuntimeError(f"{description} failed with exit code {result.returncode}")
    if result.stdout:
        print(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Run an unrestricted Yoruba control pilot on one dilemma")
    parser.add_argument("--dilemma-id", default="trolley_problem", help="Single dilemma id to run")
    parser.add_argument("--output-suffix", default="pilot", help="Suffix added to output prefixes")
    args = parser.parse_args()

    module_dir = Path(__file__).resolve().parent
    pipeline_dir = module_dir.parent
    repo_root = pipeline_dir.parent
    json_path = pipeline_dir / "input_questions" / "all_dilemmas_deictic_questions_yoruba.json"

    commands = [
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_multi_dilemma.py"),
                "--json-path",
                str(json_path),
                "--dilemmas",
                args.dilemma_id,
                "--output-prefix",
                f"yoruba_control_gpt4o_{args.output_suffix}",
            ],
            f"Unrestricted Yoruba control pilot: GPT-4o ({args.dilemma_id})",
        ),
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_anthropic.py"),
                "--json-path",
                str(json_path),
                "--dilemma-ids",
                args.dilemma_id,
                "--output-prefix",
                f"yoruba_control_claude_{args.output_suffix}",
            ],
            f"Unrestricted Yoruba control pilot: Claude ({args.dilemma_id})",
        ),
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_deepseek.py"),
                "--json-path",
                str(json_path),
                "--dilemma-ids",
                args.dilemma_id,
                "--output-prefix",
                f"yoruba_control_deepseek_{args.output_suffix}",
            ],
            f"Unrestricted Yoruba control pilot: DeepSeek ({args.dilemma_id})",
        ),
    ]

    for command, description in commands:
        run_command(command, description, str(repo_root))

    print("\n[DONE] Unrestricted Yoruba control pilot finished for all three models.")


if __name__ == "__main__":
    main()
