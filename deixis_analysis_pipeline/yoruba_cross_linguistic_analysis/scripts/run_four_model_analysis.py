#!/usr/bin/env python3
"""Run the full four-model Yoruba deixis analysis pipeline."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

STEPS = [
    ("build_constrained_four_model_coding_merge.py", "Merge constrained coding (4 models)"),
    ("extract_yoruba_pronouns_v2.py", "Extract pronoun counts"),
    ("merge_and_prepare_data.py", "Merge pronouns + coding"),
    ("extract_interesting_examples.py", "Extract interesting examples"),
    ("create_visualizations.py", "Create visualizations 01-03"),
    ("create_more_visualizations.py", "Create visualizations 04-07"),
    ("create_cross_linguistic_comparisons.py", "Create visualizations 08-11"),
    ("create_final_visualizations.py", "Create visualizations 12-15"),
    ("create_mi_emi_natlas_comparison.py", "Create mi/emi/n-atlas focus chart"),
    ("create_ethics_dilemma_heatmap.py", "Create ethics heatmap (22)"),
    ("create_emi_disambiguation_visualizations.py", "Create emi/ẹ̀mí audit charts (23-25)"),
]


def main() -> None:
    for script, label in STEPS:
        path = SCRIPT_DIR / script
        print(f"\n{'=' * 60}\n{label}\n{'=' * 60}")
        subprocess.run([sys.executable, str(path)], check=True)
    print("\n[DONE] Four-model analysis complete.")


if __name__ == "__main__":
    main()
