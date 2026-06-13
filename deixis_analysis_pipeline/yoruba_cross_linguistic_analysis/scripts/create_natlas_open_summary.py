#!/usr/bin/env python3
"""Dedicated open-condition summary: N-ATLaS (native) vs cloud models.

Single 2x3 dashboard contrasting the open/unrestricted Yoruba arm across all
four models, highlighting N-ATLaS. Writes 26_natlas_open_vs_cloud_summary.png
into visualizations_open/.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac  # noqa: E402
from analysis_config import COLORS, MODELS  # noqa: E402

ac.configure("open")

HIGHLIGHT = "n-atlas"


def _bar_colors(models: list[str]) -> list[str]:
    return [COLORS.get(m, "#888888") for m in models]


def _annotate(ax, bars, fmt="{:.0f}"):
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h, fmt.format(h),
                ha="center", va="bottom", fontsize=9)


def _stacked(ax, df, field, order, title, palette):
    ct = pd.crosstab(df["model"], df[field]).reindex(MODELS)
    cats = [c for c in order if c in ct.columns] + [c for c in ct.columns if c not in order]
    bottom = np.zeros(len(MODELS))
    x = np.arange(len(MODELS))
    for cat in cats:
        vals = ct[cat].fillna(0).values
        ax.bar(x, vals, bottom=bottom, label=cat.replace("_", " "),
               color=palette.get(cat, "#cccccc"), edgecolor="black", linewidth=0.4)
        bottom += vals
    ax.set_xticks(x)
    ax.set_xticklabels(MODELS, rotation=20, ha="right")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(fontsize=7, loc="upper right")
    ax.set_ylim(0, 60)


def main() -> None:
    df = pd.read_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv")
    g = df.groupby("model")
    x = np.arange(len(MODELS))

    fig, axes = plt.subplots(2, 3, figsize=(19, 11))
    fig.suptitle(
        "Open (unconstrained) Yoruba: N-ATLaS (native) vs cloud models",
        fontsize=17, fontweight="bold",
    )

    # A: response length
    ax = axes[0, 0]
    vals = [g["response_length"].mean().get(m, 0) for m in MODELS]
    bars = ax.bar(x, vals, color=_bar_colors(MODELS), edgecolor="black")
    _annotate(ax, bars)
    ax.set_xticks(x); ax.set_xticklabels(MODELS, rotation=20, ha="right")
    ax.set_title("Mean response length (chars)", fontsize=12, fontweight="bold")

    # B: mo vs true emphatic emi
    ax = axes[0, 1]
    mo = [g["first_singular_mo"].sum().get(m, 0) for m in MODELS]
    emi = [g["first_singular_emi_emphatic"].sum().get(m, 0) for m in MODELS]
    w = 0.38
    b1 = ax.bar(x - w / 2, mo, w, label="mo (ordinary I)", color="#2A9D8F", edgecolor="black")
    b2 = ax.bar(x + w / 2, emi, w, label="èmi (emphatic I)", color="#F1C453", edgecolor="black")
    _annotate(ax, b1); _annotate(ax, b2)
    ax.set_xticks(x); ax.set_xticklabels(MODELS, rotation=20, ha="right")
    ax.set_title("mo vs true èmi (totals)", fontsize=12, fontweight="bold")
    ax.legend(fontsize=8)

    # C: corrected emphatic ratio
    ax = axes[0, 2]
    vals = [g["emphatic_ratio"].mean().get(m, 0) for m in MODELS]
    bars = ax.bar(x, vals, color=_bar_colors(MODELS), edgecolor="black")
    _annotate(ax, bars, fmt="{:.3f}")
    ax.set_xticks(x); ax.set_xticklabels(MODELS, rotation=20, ha="right")
    ax.set_title("Corrected emphatic ratio  èmi / (mo+èmi)", fontsize=12, fontweight="bold")

    # D: language stability
    _stacked(axes[1, 0], df, "language_stability",
             ["clean_yoruba", "yoruba_with_english_markers", "translation_mode", "corrupted_or_unusable"],
             "Language stability", {
                 "clean_yoruba": "#52b788",
                 "yoruba_with_english_markers": "#f4a261",
                 "translation_mode": "#457B9D",
                 "corrupted_or_unusable": "#e63946",
             })

    # E: deictic uptake
    _stacked(axes[1, 1], df, "deictic_uptake_quality",
             ["strong_uptake", "partial_uptake", "weak_uptake"],
             "Deictic uptake quality", {
                 "strong_uptake": "#264653",
                 "partial_uptake": "#2a9d8f",
                 "weak_uptake": "#e76f51",
             })

    # F: response genre
    _stacked(axes[1, 2], df, "response_genre",
             ["balanced_framework_exposition", "procedural_advice", "direct_verdict", "mixed",
              "meta_commentary", "translation_or_gloss"],
             "Response genre spread", {
                 "balanced_framework_exposition": "#2E86AB",
                 "procedural_advice": "#F18F01",
                 "direct_verdict": "#A23B72",
                 "mixed": "#06A77D",
                 "meta_commentary": "#999999",
                 "translation_or_gloss": "#cccccc",
             })

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = ac.VIZ_DIR / "26_natlas_open_vs_cloud_summary.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Created: {out}")


if __name__ == "__main__":
    main()
