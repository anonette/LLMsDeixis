#!/usr/bin/env python3
"""Run an unrestricted Yoruba control generation for all three models.

This control condition uses the same Yoruba prompt inventory as the main study
but does not prepend any response-shaping instruction. It is intended as a
separate experiment to measure how the models respond to the Yoruba dilemmas
without the Yoruba-only / decision-format constraints used in the main run.
"""

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
                "--output-prefix",
                "yoruba_control_gpt4o",
            ],
            "Unrestricted Yoruba control: GPT-4o",
        ),
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_anthropic.py"),
                "--json-path",
                str(json_path),
                "--output-prefix",
                "yoruba_control_claude",
            ],
            "Unrestricted Yoruba control: Claude Sonnet",
        ),
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_deepseek.py"),
                "--json-path",
                str(json_path),
                "--output-prefix",
                "yoruba_control_deepseek",
            ],
            "Unrestricted Yoruba control: DeepSeek",
        ),
    ]

    for command, description in commands:
        run_command(command, description, str(repo_root))

    print("\n[DONE] Unrestricted Yoruba control generation finished for all three models.")


if __name__ == "__main__":
    main()
