#!/usr/bin/env python3
"""Figures 23–25: èmi vs ẹ̀mí disambiguation audit and corrected emphatic ratios."""

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
from analysis_config import COLORS, MODELS  # noqa: E402

DILEMMA_LABELS = {
    "ai_consciousness": "AI consciousness",
    "icu_bed_allocation": "ICU beds",
    "memory_modification": "Memory mod.",
    "scholarship_fraud": "Scholarship",
    "trolley_problem": "Trolley",
    "whistleblower_risk": "Whistleblower",
}


def load_merged() -> pd.DataFrame:
    path = ac.DATA_DIR / "yoruba_merged_analysis.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run merge first: {path}")
    return pd.read_csv(path)


def _dilemma_order(df: pd.DataFrame) -> list[str]:
    return sorted(df["dilemma_id"].unique(), key=lambda d: DILEMMA_LABELS.get(d, d))


def create_fig23_emi_life_stacked(df: pd.DataFrame) -> None:
    """Stacked bars: emphatic èmi vs ẹ̀mí (life) by dilemma × model."""
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    dilemmas = _dilemma_order(df)
    n_models = len(MODELS)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharey=True)
    axes = axes.flatten()

    for ax, model in zip(axes, MODELS):
        sub = df[df["model"] == model]
        emph = []
        life = []
        for d in dilemmas:
            block = sub[sub["dilemma_id"] == d]
            emph.append(block["first_singular_emi_emphatic"].sum() if "first_singular_emi_emphatic" in block else 0)
            life.append(block["first_singular_emi_life"].sum() if "first_singular_emi_life" in block else 0)
        x = np.arange(len(dilemmas))
        ax.bar(x, emph, label="èmi (emphatic I)", color=COLORS.get(model, "#333"))
        ax.bar(x, life, bottom=emph, label="ẹ̀mí (life/spirit)", color="#94a3b8", hatch="//")
        ax.set_xticks(x)
        ax.set_xticklabels([DILEMMA_LABELS.get(d, d) for d in dilemmas], rotation=35, ha="right")
        ax.set_title(model, fontweight="bold")
        ax.set_ylabel("Token count (9 framings summed)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle(
        "What the pipeline tracks: emphatic èmi vs ẹ̀mí (life) — by dilemma",
        fontweight="bold",
        y=1.05,
    )
    plt.tight_layout()
    out = ac.VIZ_DIR / "23_emi_emphatic_vs_emi_life_by_dilemma.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Created: {out}")


def create_fig24_life_contamination_heatmap(df: pd.DataFrame) -> None:
    """Heatmap: share of all emi-pattern tokens that are ẹ̀mí (life), not èmi."""
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    dilemmas = _dilemma_order(df)
    rows = []
    for model in MODELS:
        for d in dilemmas:
            block = df[(df["model"] == model) & (df["dilemma_id"] == d)]
            life = block["first_singular_emi_life"].sum() if "first_singular_emi_life" in block else 0
            combined = block["first_singular_emi"].sum() if "first_singular_emi" in block else 0
            pct = (life / combined * 100) if combined else 0
            rows.append({"model": model, "dilemma": DILEMMA_LABELS.get(d, d), "life_share_pct": pct})

    mat_df = pd.DataFrame(rows).pivot(index="model", columns="dilemma", values="life_share_pct")
    fig, ax = plt.subplots(figsize=(14, 5))
    sns.heatmap(
        mat_df.reindex(MODELS),
        annot=True,
        fmt=".0f",
        cmap="OrRd",
        vmin=0,
        vmax=100,
        ax=ax,
        cbar_kws={"label": "% of emi-pattern tokens that are ẹ̀mí (life)"},
    )
    ax.set_title(
        "ẹ̀mí contamination: where 'life/spirit' inflated the old emi counts",
        fontweight="bold",
    )
    plt.tight_layout()
    out = ac.VIZ_DIR / "24_emi_life_contamination_heatmap.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Created: {out}")


def create_fig25_raw_vs_corrected_ratio(df: pd.DataFrame) -> None:
    """Grouped bars: emphatic ratio before vs after ẹ̀mí removal."""
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    raw_col = "emphatic_ratio_raw" if "emphatic_ratio_raw" in df.columns else "emphatic_ratio"
    corrected_col = "emphatic_ratio"

    summary = df.groupby("model").agg(
        raw=(raw_col, "mean"),
        corrected=(corrected_col, "mean"),
    ).reindex(MODELS)

    x = np.arange(len(MODELS))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width / 2, summary["raw"], width, label="Raw (èmi + ẹ̀mí combined)", color="#cbd5e1")
    bars = ax.bar(
        x + width / 2,
        summary["corrected"],
        width,
        label="Corrected (èmi only, ẹ̀mí excluded)",
        color=[COLORS[m] for m in MODELS],
    )
    ax.set_xticks(x)
    ax.set_xticklabels(MODELS)
    ax.set_ylabel("Mean emphatic ratio emi ÷ (mo + emi)")
    ax.set_title("Emphatic ratio: raw pipeline vs corrected disambiguation", fontweight="bold")
    ax.legend()
    for bar, val in zip(bars, summary["corrected"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005, f"{val:.3f}", ha="center", fontsize=9)
    plt.tight_layout()
    out = ac.VIZ_DIR / "25_emphatic_ratio_raw_vs_corrected.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Created: {out}")


def export_audit_csv(df: pd.DataFrame) -> None:
    """Summary table for the master report."""
    rows = []
    for model in MODELS:
        for d in _dilemma_order(df):
            block = df[(df["model"] == model) & (df["dilemma_id"] == d)]
            mo = block["first_singular_mo"].sum()
            emph = block["first_singular_emi_emphatic"].sum() if "first_singular_emi_emphatic" in block else 0
            life = block["first_singular_emi_life"].sum() if "first_singular_emi_life" in block else 0
            combined = block["first_singular_emi"].sum() if "first_singular_emi" in block else emph + life
            ratio_corr = emph / (mo + emph) if (mo + emph) else 0
            ratio_raw = combined / (mo + combined) if (mo + combined) else 0
            rows.append(
                {
                    "model": model,
                    "dilemma_id": d,
                    "mo_total": int(mo),
                    "emi_emphatic_total": int(emph),
                    "emi_life_total": int(life),
                    "emi_combined_total": int(combined),
                    "emphatic_ratio_raw": round(ratio_raw, 3),
                    "emphatic_ratio_corrected": round(ratio_corr, 3),
                    "life_share_of_emi_pattern": round(life / combined * 100, 1) if combined else 0,
                }
            )
    out = ac.DATA_DIR / "emi_disambiguation_audit.csv"
    pd.DataFrame(rows).to_csv(out, index=False, encoding="utf-8")
    print(f"Created: {out}")


def main() -> None:
    df = load_merged()
    create_fig23_emi_life_stacked(df)
    create_fig24_life_contamination_heatmap(df)
    create_fig25_raw_vs_corrected_ratio(df)
    export_audit_csv(df)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()
