#!/usr/bin/env python3
"""Dilemma x framing x model account figures + data tables, for one condition.

Usage: python create_dilemma_framing_account.py --condition open|constrained

Writes figures 30-36 into the condition's VIZ_DIR and a data dump
(account_tables_<condition>.txt) into DATA_DIR for write-up.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac  # noqa: E402
from analysis_config import COLORS, FRAMING_ORDER, MODELS  # noqa: E402

DILEMMA_ORDER = [
    "trolley_problem",
    "icu_bed_allocation",
    "whistleblower_risk",
    "scholarship_fraud",
    "ai_consciousness",
    "memory_modification",
]
DIL_SHORT = {
    "trolley_problem": "trolley",
    "icu_bed_allocation": "ICU bed",
    "whistleblower_risk": "whistleblower",
    "scholarship_fraud": "scholarship",
    "ai_consciousness": "AI mind",
    "memory_modification": "memory mod",
}

SOLUTION_COLORS = {
    "supports_A": "#2E86AB", "supports_B": "#A23B72",
    "conditional_or_mixed": "#F18F01", "refuses_to_commit": "#6c757d",
    "uncodable": "#e63946",
}
GENRE_COLORS = {
    "direct_verdict": "#A23B72", "procedural_advice": "#F18F01",
    "balanced_framework_exposition": "#2E86AB", "mixed": "#06A77D",
    "meta_commentary": "#999999", "translation_or_gloss": "#cccccc",
}
ETHIC_COLORS = {
    "utilitarian": "#2E86AB", "deontological": "#A23B72", "care_ethics": "#06A77D",
    "virtue_ethics": "#F1C453", "procedural_caution": "#F18F01", "rights_based": "#8338ec",
    "mixed": "#52b788", "unclear": "#adb5bd",
}
STAB_COLORS = {
    "clean_yoruba": "#52b788", "yoruba_with_english_markers": "#f4a261",
    "translation_mode": "#457B9D", "corrupted_or_unusable": "#e63946",
}


def stacked_by_model(ax, df, field, palette, title, order=None):
    ct = pd.crosstab(df["model"], df[field]).reindex(MODELS)
    cols = (order or []) + [c for c in ct.columns if c not in (order or [])]
    cols = [c for c in cols if c in ct.columns]
    bottom = np.zeros(len(MODELS))
    x = np.arange(len(MODELS))
    for cat in cols:
        vals = ct[cat].fillna(0).values
        ax.bar(x, vals, bottom=bottom, label=cat.replace("_", " "),
               color=palette.get(cat, "#cccccc"), edgecolor="black", linewidth=0.4)
        bottom += vals
    ax.set_xticks(x); ax.set_xticklabels(MODELS, rotation=20, ha="right")
    ax.set_ylabel("responses (of 54)"); ax.set_title(title, fontweight="bold")
    ax.legend(fontsize=7, loc="upper right", framealpha=0.9)
    ax.set_ylim(0, 58)


def heatmap(ax, mat, rows, cols, title, fmt="{:.2f}", cmap="RdYlGn_r", vmin=None, vmax=None):
    im = ax.imshow(mat, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=20, ha="right")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows)
    for i in range(len(rows)):
        for j in range(len(cols)):
            v = mat[i, j]
            if not np.isnan(v):
                ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=8,
                        color="black")
    ax.set_title(title, fontweight="bold")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--condition", choices=["open", "constrained"], default="open")
    args = p.parse_args()
    ac.configure(args.condition)
    cond = args.condition
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv")
    df = df[df["model"].isin(MODELS)]
    tag = f"({cond.capitalize()} arm)"

    # 30 preferred solution
    fig, ax = plt.subplots(figsize=(9, 6))
    stacked_by_model(ax, df, "preferred_solution", SOLUTION_COLORS,
                     f"Preferred solution by model {tag}",
                     order=list(SOLUTION_COLORS))
    fig.tight_layout(); fig.savefig(ac.VIZ_DIR / "30_preferred_solution_by_model.png", dpi=150); plt.close(fig)

    # 31 genre
    fig, ax = plt.subplots(figsize=(9, 6))
    stacked_by_model(ax, df, "response_genre", GENRE_COLORS,
                     f"Response genre by model {tag}", order=list(GENRE_COLORS))
    fig.tight_layout(); fig.savefig(ac.VIZ_DIR / "31_genre_by_model.png", dpi=150); plt.close(fig)

    # 32 ethic
    fig, ax = plt.subplots(figsize=(9, 6))
    stacked_by_model(ax, df, "ethical_preference_type", ETHIC_COLORS,
                     f"Ethical reasoning type by model {tag}", order=list(ETHIC_COLORS))
    fig.tight_layout(); fig.savefig(ac.VIZ_DIR / "32_ethic_by_model.png", dpi=150); plt.close(fig)

    # 35 stability
    fig, ax = plt.subplots(figsize=(9, 6))
    stacked_by_model(ax, df, "language_stability", STAB_COLORS,
                     f"Language stability by model {tag}", order=list(STAB_COLORS))
    fig.tight_layout(); fig.savefig(ac.VIZ_DIR / "35_stability_by_model.png", dpi=150); plt.close(fig)

    # 33 emphatic ratio: dilemma x model heatmap
    dils = [d for d in DILEMMA_ORDER if d in df["dilemma_id"].unique()]
    mat = np.full((len(dils), len(MODELS)), np.nan)
    for i, d in enumerate(dils):
        for j, m in enumerate(MODELS):
            sub = df[(df.dilemma_id == d) & (df.model == m)]
            if len(sub):
                mat[i, j] = sub["emphatic_ratio"].mean()
    fig, ax = plt.subplots(figsize=(8, 6))
    heatmap(ax, mat, [DIL_SHORT[d] for d in dils], MODELS,
            f"Corrected emphatic ratio  emi/(mo+emi)  by dilemma {tag}",
            fmt="{:.2f}", cmap="Purples", vmin=0, vmax=max(0.5, np.nanmax(mat)))
    ax.set_xlabel("model"); ax.set_ylabel("dilemma")
    fig.tight_layout(); fig.savefig(ac.VIZ_DIR / "33_emphatic_ratio_dilemma_model.png", dpi=150); plt.close(fig)

    # 34 strong uptake fraction: framing x model
    frs = [f for f in FRAMING_ORDER if f in df["framing_type"].unique()]
    mat = np.full((len(frs), len(MODELS)), np.nan)
    for i, f in enumerate(frs):
        for j, m in enumerate(MODELS):
            sub = df[(df.framing_type == f) & (df.model == m)]
            if len(sub):
                mat[i, j] = (sub["deictic_uptake_quality"] == "strong_uptake").mean()
    fig, ax = plt.subplots(figsize=(8, 7))
    heatmap(ax, mat, [f.replace("_", " ") for f in frs], MODELS,
            f"Strong deictic-uptake rate by framing {tag}",
            fmt="{:.0%}", cmap="Greens", vmin=0, vmax=1)
    ax.set_xlabel("model"); ax.set_ylabel("framing")
    fig.tight_layout(); fig.savefig(ac.VIZ_DIR / "34_strong_uptake_framing_model.png", dpi=150); plt.close(fig)

    # 36 genre by dilemma, small multiples per model
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    for ax, m in zip(axes.flat, MODELS):
        sub = df[df.model == m]
        ct = pd.crosstab(sub["dilemma_id"], sub["response_genre"]).reindex(dils)
        bottom = np.zeros(len(dils)); x = np.arange(len(dils))
        for cat in [c for c in GENRE_COLORS if c in ct.columns]:
            vals = ct[cat].fillna(0).values
            ax.bar(x, vals, bottom=bottom, label=cat.replace("_", " "),
                   color=GENRE_COLORS.get(cat, "#ccc"), edgecolor="black", linewidth=0.3)
            bottom += vals
        ax.set_xticks(x); ax.set_xticklabels([DIL_SHORT[d] for d in dils], rotation=30, ha="right")
        ax.set_title(m, fontweight="bold"); ax.set_ylabel("responses (of 9 framings)")
        ax.set_ylim(0, 9.5); ax.legend(fontsize=6, loc="upper right")
    fig.suptitle(f"Response genre by dilemma, per model {tag}", fontsize=15, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(ac.VIZ_DIR / "36_genre_by_dilemma_per_model.png", dpi=150); plt.close(fig)

    # ---- data dump for write-up ----
    out = [f"# Account tables — {cond} arm\n"]
    g = df.groupby("model")
    out.append("## Model-level summary")
    summ = pd.DataFrame({
        "words": g["word_count"].mean().round(0),
        "chars": g["response_length"].mean().round(0),
        "mo_total": g["first_singular_mo"].sum().astype(int),
        "emi_emph_total": g["first_singular_emi_emphatic"].sum().astype(int),
        "emi_life_total": g["first_singular_emi_life"].sum().astype(int),
        "emph_ratio": g["emphatic_ratio"].mean().round(3),
        "clean_yo": g.apply(lambda s: (s["language_stability"] == "clean_yoruba").sum()),
        "strong_uptake": g.apply(lambda s: (s["deictic_uptake_quality"] == "strong_uptake").sum()),
    }).reindex(MODELS)
    out.append(summ.to_string()); out.append("")
    for fld in ["preferred_solution", "response_genre", "ethical_preference_type", "language_stability"]:
        out.append(f"## {fld} (rows=model)")
        out.append(pd.crosstab(df["model"], df[fld]).reindex(MODELS).to_string()); out.append("")
    out.append("## emphatic_ratio by dilemma x model")
    out.append(df.pivot_table("emphatic_ratio", "dilemma_id", "model", aggfunc="mean").reindex(dils).round(3).to_string())
    out.append("")
    out.append("## strong-uptake rate by framing x model")
    up = df.assign(strong=(df.deictic_uptake_quality == "strong_uptake").astype(int))
    out.append(up.pivot_table("strong", "framing_type", "model", aggfunc="mean").reindex(frs).round(2).to_string())
    (ac.DATA_DIR / f"account_tables_{cond}.txt").write_text("\n".join(out), encoding="utf-8")

    print(f"[{cond}] figures 30-36 -> {ac.VIZ_DIR}")
    print(f"[{cond}] tables -> {ac.DATA_DIR / f'account_tables_{cond}.txt'}")


if __name__ == "__main__":
    main()
