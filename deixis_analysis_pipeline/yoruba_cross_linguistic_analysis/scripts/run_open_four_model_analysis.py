#!/usr/bin/env python3
"""Run the full four-model open/unrestricted Yoruba deixis analysis pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

STEPS = [
    ("build_open_four_model_coding_merge.py", []),
    ("extract_yoruba_pronouns_v2.py", ["--condition", "open"]),
    ("merge_and_prepare_data.py", ["--condition", "open"]),
    ("extract_interesting_examples.py", ["--condition", "open"]),
    ("create_visualizations.py", ["--condition", "open"]),
    ("create_more_visualizations.py", ["--condition", "open"]),
    ("create_cross_linguistic_comparisons.py", ["--condition", "open"]),
    ("create_final_visualizations.py", ["--condition", "open"]),
    ("create_mi_emi_natlas_comparison.py", ["--condition", "open"]),
    ("create_ethics_dilemma_heatmap.py", []),
    ("create_emi_disambiguation_visualizations.py", ["--condition", "open"]),
    ("create_constrained_vs_open_comparison.py", []),
]


def main() -> None:
    for script, extra in STEPS:
        path = SCRIPT_DIR / script
        print(f"\n{'=' * 60}\n{script}\n{'=' * 60}")
        subprocess.run([sys.executable, str(path), *extra], check=True)
    print("\n[DONE] Open four-model analysis + constrained vs open comparison complete.")


if __name__ == "__main__":
    main()
