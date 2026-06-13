#!/usr/bin/env python3
"""Run Yoruba-only generation for all three article models."""

import subprocess
import sys
import os
import json
from pathlib import Path


def load_instruction_config(module_dir: Path):
    config_path = module_dir / "model_response_instructions.json"
    with open(config_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


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
    # Sanity check that the instruction config file exists and is readable.
    load_instruction_config(module_dir)

    # Use --response-instruction-key to avoid any chance of shell-level encoding
    # corruption of the Yoruba instruction text. The generator scripts read the
    # instruction directly from model_response_instructions.json using UTF-8.
    commands = [
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_multi_dilemma.py"),
                "--json-path",
                str(json_path),
                "--output-prefix",
                "yoruba_gpt4o",
                "--response-instruction-key",
                "gpt-4o"
            ],
            "Yoruba generation: GPT-4o"
        ),
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_anthropic.py"),
                "--json-path",
                str(json_path),
                "--output-prefix",
                "yoruba_claude",
                "--response-instruction-key",
                "claude-3.5-sonnet"
            ],
            "Yoruba generation: Claude 3.5 Sonnet"
        ),
        (
            [
                sys.executable,
                str(pipeline_dir / "generation_scripts" / "generate_responses_deepseek.py"),
                "--json-path",
                str(json_path),
                "--output-prefix",
                "yoruba_deepseek",
                "--response-instruction-key",
                "deepseek-chat"
            ],
            "Yoruba generation: DeepSeek"
        )
    ]

    for command, description in commands:
        run_command(command, description, str(repo_root))

    print("\n[DONE] Yoruba-only generation finished for all three models.")


if __name__ == "__main__":
    main()
