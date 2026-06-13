#!/usr/bin/env python3
"""Compare constrained vs open deixis patterns across four models."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from analysis_config import ANALYSIS_ROOT, COLORS, FRAMING_ORDER, MODELS  # noqa: E402

OUT_DIR = ANALYSIS_ROOT / "visualizations_constrained_vs_open"
CONSTRAINED_CSV = ANALYSIS_ROOT / "data" / "yoruba_merged_analysis.csv"
OPEN_CSV = ANALYSIS_ROOT / "data" / "open" / "yoruba_merged_analysis.csv"

METRICS = [
    ("first_singular_mo_per_100w", "Mo"),
    ("first_singular_emi_per_100w", "Emi"),
    ("first_singular_mi_per_100w", "Mi"),
    ("emphatic_ratio", "Emphatic ratio"),
]


def load_both() -> tuple[pd.DataFrame, pd.DataFrame]:
    constrained = pd.read_csv(CONSTRAINED_CSV)
    open_df = pd.read_csv(OPEN_CSV)
    constrained["arm"] = "constrained"
    open_df["arm"] = "open"
    return constrained, open_df


def model_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("model").agg(
        {
            "first_singular_mo_per_100w": "mean",
            "first_singular_emi_per_100w": "mean",
            "first_singular_mi_per_100w": "mean",
            "emphatic_ratio": "mean",
            "word_count": "mean",
        }
    )


def plot_model_arm_bars(constrained: pd.DataFrame, open_df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    x = np.arange(len(MODELS))
    width = 0.35

    for ax, (col, title) in zip(axes, METRICS):
        c_vals = [constrained[constrained["model"] == m][col].mean() for m in MODELS]
        o_vals = [open_df[open_df["model"] == m][col].mean() for m in MODELS]
        ax.bar(x - width / 2, c_vals, width, label="Constrained", color="#457B9D", alpha=0.85)
        ax.bar(x + width / 2, o_vals, width, label="Open", color="#E63946", alpha=0.85)
        ax.set_title(title, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, rotation=20, ha="right")
        ax.grid(axis="y", alpha=0.3)
        if ax is axes[0]:
            ax.legend()

    fig.suptitle("Constrained vs Open: First-Person Deixis by Model", fontsize=16, fontweight="bold")
    plt.tight_layout()
    fig.savefig(OUT_DIR / "18_constrained_vs_open_model_summary.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Created: 18_constrained_vs_open_model_summary.png")


def plot_open_minus_constrained_delta(constrained: pd.DataFrame, open_df: pd.DataFrame) -> None:
    rows = []
    for model in MODELS:
        for col, label in METRICS:
            c_mean = constrained[constrained["model"] == model][col].mean()
            o_mean = open_df[open_df["model"] == model][col].mean()
            rows.append({"model": model, "metric": label, "delta": o_mean - c_mean})
    delta = pd.DataFrame(rows)
    pivot = delta.pivot(index="model", columns="metric", values="delta").reindex(MODELS)

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(pivot.values, cmap="RdBu_r", aspect="auto", vmin=-3, vmax=3)
    ax.set_xticks(np.arange(len(pivot.columns)))
    ax.set_yticks(np.arange(len(pivot.index)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticklabels(pivot.index)
    plt.colorbar(im, ax=ax, label="Open minus constrained")
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            ax.text(j, i, f"{pivot.values[i, j]:+.2f}", ha="center", va="center", fontsize=9)
    ax.set_title("Open − Constrained Deixis Delta (positive = more in open arm)", fontweight="bold")
    plt.tight_layout()
    fig.savefig(OUT_DIR / "19_open_minus_constrained_delta.png", dpi=300, bbox_inches="tight")
    plt.close()
    pivot.to_csv(OUT_DIR.parent / "data" / "constrained_vs_open_delta.csv")
    print("Created: 19_open_minus_constrained_delta.png")


def plot_framing_by_arm(constrained: pd.DataFrame, open_df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)
    for ax, arm_df, title in [
        (axes[0], constrained, "Constrained"),
        (axes[1], open_df, "Open"),
    ]:
        grouped = arm_df.groupby(["framing_type", "model"])["first_singular_mi_per_100w"].mean().unstack("model")
        grouped = grouped.reindex(FRAMING_ORDER)[MODELS]
        x = np.arange(len(FRAMING_ORDER))
        width = 0.18
        for i, model in enumerate(MODELS):
            offset = (i - (len(MODELS) - 1) / 2) * width
            ax.bar(x + offset, grouped[model].values, width, label=model, color=COLORS[model])
        ax.set_title(f"{title}: Mi usage by framing", fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([f.replace("_", "\n") for f in FRAMING_ORDER], rotation=45, ha="right")
        ax.set_ylabel("Mi per 100 words")
        ax.grid(axis="y", alpha=0.3)
    axes[0].legend(loc="upper left", fontsize=8)
    fig.suptitle("Mi (me/my) Across Framings: Constrained vs Open", fontsize=15, fontweight="bold")
    plt.tight_layout()
    fig.savefig(OUT_DIR / "20_mi_framing_constrained_vs_open.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Created: 20_mi_framing_constrained_vs_open.png")


def plot_natlas_instruction_effect(constrained: pd.DataFrame, open_df: pd.DataFrame) -> None:
    """Highlight N-ATLaS shift when instruction layer is removed."""
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics = ["word_count", "first_singular_mi_per_100w", "emphatic_ratio"]
    labels = ["Avg words", "Mi/100w", "Emphatic ratio"]
    x = np.arange(len(metrics))
    width = 0.35
    natlas_c = constrained[constrained["model"] == "n-atlas"]
    natlas_o = open_df[open_df["model"] == "n-atlas"]
    c_vals = [natlas_c[m].mean() for m in metrics]
    o_vals = [natlas_o[m].mean() for m in metrics]
    ax.bar(x - width / 2, c_vals, width, label="N-ATLaS constrained", color=COLORS["n-atlas"], alpha=0.5)
    ax.bar(x + width / 2, o_vals, width, label="N-ATLaS open", color=COLORS["n-atlas"])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("N-ATLaS: Instruction Layer vs Unrestricted", fontweight="bold")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    for i, (c, o) in enumerate(zip(c_vals, o_vals)):
        ax.text(i - width / 2, c, f"{c:.2f}", ha="center", va="bottom", fontsize=8)
        ax.text(i + width / 2, o, f"{o:.2f}", ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    fig.savefig(OUT_DIR / "21_natlas_constrained_vs_open.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("Created: 21_natlas_constrained_vs_open.png")


def write_summary_md(constrained: pd.DataFrame, open_df: pd.DataFrame) -> None:
    c_sum = model_summary(constrained)
    o_sum = model_summary(open_df)
    lines = ["# Constrained vs Open Four-Model Deixis Summary\n"]
    for model in MODELS:
        lines.append(f"## {model}\n")
        lines.append("| Metric | Constrained | Open | Δ (open−constrained) |")
        lines.append("|--------|-------------|------|------------------------|")
        for col, label in METRICS:
            c = c_sum.loc[model, col]
            o = o_sum.loc[model, col]
            lines.append(f"| {label} | {c:.3f} | {o:.3f} | {o - c:+.3f} |")
        cw = c_sum.loc[model, "word_count"]
        ow = o_sum.loc[model, "word_count"]
        lines.append(f"| Avg words | {cw:.1f} | {ow:.1f} | {ow - cw:+.1f} |\n")
    path = OUT_DIR.parent / "data" / "constrained_vs_open_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {path}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    constrained, open_df = load_both()
    plot_model_arm_bars(constrained, open_df)
    plot_open_minus_constrained_delta(constrained, open_df)
    plot_framing_by_arm(constrained, open_df)
    plot_natlas_instruction_effect(constrained, open_df)
    write_summary_md(constrained, open_df)


if __name__ == "__main__":
    main()
