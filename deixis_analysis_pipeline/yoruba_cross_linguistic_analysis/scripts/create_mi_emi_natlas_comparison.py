#!/usr/bin/env python3
"""Focused mi / emi / mo comparison highlighting N-ATLaS vs cloud models."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac
from analysis_config import COLORS, FRAMING_ORDER, MODELS  # noqa: E402

plt.style.use("default")
sns.set_palette("husl")


def load_merged() -> pd.DataFrame:
    return pd.read_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv")


def create_mi_emi_mo_panel(df: pd.DataFrame) -> None:
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    metrics = [
        ("first_singular_mo_per_100w", "Mo (regular I)"),
        ("first_singular_emi_per_100w", "Emi (emphatic I)"),
        ("first_singular_mi_per_100w", "Mi (me/my)"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(20, 7), sharey=False)
    x = np.arange(len(FRAMING_ORDER))
    width = 0.18

    for ax, (col, title) in zip(axes, metrics):
        for i, model in enumerate(MODELS):
            subset = df[df["model"] == model]
            values = []
            for framing in FRAMING_ORDER:
                row = subset[subset["framing_type"] == framing]
                values.append(row[col].mean() if not row.empty and col in row else 0.0)
            offset = (i - (len(MODELS) - 1) / 2) * width
            ax.bar(
                x + offset,
                values,
                width,
                label=model,
                color=COLORS.get(model, "#888888"),
                edgecolor="black",
                linewidth=0.4,
            )
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([f.replace("_", "\n") for f in FRAMING_ORDER], rotation=45, ha="right")
        ax.set_ylabel("Per 100 words")
        ax.grid(axis="y", alpha=0.3)

    axes[0].legend(loc="upper left", fontsize=9)
    fig.suptitle(
        f"First-Person Deixis: Mo vs Emi vs Mi by Framing "
        f"({ac.active_condition().capitalize()}, 4 Models)",
        fontsize=16,
        fontweight="bold",
    )
    plt.tight_layout()
    out = ac.VIZ_DIR / "16_mi_emi_mo_four_model_framing.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Created: {out.name}")


def create_natlas_vs_cloud_heatmap(df: pd.DataFrame) -> None:
    cloud = df[df["model"] != "n-atlas"].groupby("framing_type").agg(
        {
            "first_singular_mo_per_100w": "mean",
            "first_singular_emi_per_100w": "mean",
            "first_singular_mi_per_100w": "mean",
            "emphatic_ratio": "mean",
        }
    )
    natlas = df[df["model"] == "n-atlas"].groupby("framing_type").agg(
        {
            "first_singular_mo_per_100w": "mean",
            "first_singular_emi_per_100w": "mean",
            "first_singular_mi_per_100w": "mean",
            "emphatic_ratio": "mean",
        }
    )

    delta = natlas.reindex(FRAMING_ORDER) - cloud.reindex(FRAMING_ORDER)
    delta = delta.fillna(0)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(delta.values, cmap="RdBu_r", aspect="auto", vmin=-5, vmax=5)
    ax.set_xticks(np.arange(len(delta.columns)))
    ax.set_yticks(np.arange(len(delta.index)))
    ax.set_xticklabels(["Mo", "Emi", "Mi", "Emi/(Mo+Emi)"])
    ax.set_yticklabels([f.replace("_", " ") for f in delta.index])
    plt.colorbar(im, ax=ax, label="N-ATLaS minus cloud mean")
    for i in range(len(delta.index)):
        for j in range(len(delta.columns)):
            ax.text(j, i, f"{delta.values[i, j]:+.2f}", ha="center", va="center", fontsize=9)
    ax.set_title("N-ATLaS vs Cloud Mean: First-Person Deixis Delta by Framing", fontweight="bold")
    plt.tight_layout()
    out = ac.VIZ_DIR / "17_natlas_vs_cloud_deixis_delta.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Created: {out.name}")


def create_model_summary_table(df: pd.DataFrame) -> None:
    summary = df.groupby("model").agg(
        {
            "first_singular_mo_per_100w": "mean",
            "first_singular_emi_per_100w": "mean",
            "first_singular_mi_per_100w": "mean",
            "emphatic_ratio": "mean",
            "word_count": "mean",
        }
    )
    summary = summary.reindex(MODELS)
    summary.to_csv(ac.DATA_DIR / "four_model_deixis_summary.csv")
    print("Saved: four_model_deixis_summary.csv")
    print(summary.round(3))


def main() -> None:
    df = load_merged()
    create_mi_emi_mo_panel(df)
    create_natlas_vs_cloud_heatmap(df)
    create_model_summary_table(df)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()
