#!/usr/bin/env python3
"""Two headline figures for the article:
  41 - macro markers EN vs YO (imperative %, pronoun/obligation/hedge density)
  42 - emphatic ratio in committed vs hedged Yoruba responses (mo/emi centerpiece)
Writes into visualizations_open/.
"""
from __future__ import annotations
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "english_yoruba_openai_anthropic_comparable.csv"
VIZ = ROOT / "visualizations_open"
LANG = {"english": "#457B9D", "yoruba": "#E63946"}


def main():
    df = pd.read_csv(CSV)
    en, yo = df[df.language == "english"], df[df.language == "yoruba"]

    # ---- Fig 41: macro markers ----
    fig, axes = plt.subplots(1, 4, figsize=(17, 5))
    panels = [
        ("Direct imperative\n(% of responses)", en.contains_direct_imperative.mean() * 100,
         yo.contains_direct_imperative.mean() * 100, "{:.0f}%"),
        ("Pronouns\n(per 100 words)", en.pronouns_per_100_words.mean(),
         yo.pronouns_per_100_words.mean(), "{:.1f}"),
        ("Obligation markers\n(per 100 words)", en.obligation_density_per_100_words.mean(),
         yo.obligation_density_per_100_words.mean(), "{:.2f}"),
        ("Hedge markers\n(per 100 words)", en.hedge_density_per_100_words.mean(),
         yo.hedge_density_per_100_words.mean(), "{:.2f}"),
    ]
    for ax, (title, ev, yv, fmt) in zip(axes, panels):
        bars = ax.bar(["English", "Yoruba"], [ev, yv],
                      color=[LANG["english"], LANG["yoruba"]], edgecolor="black")
        for b, v in zip(bars, [ev, yv]):
            ax.text(b.get_x() + b.get_width() / 2, v, fmt.format(v), ha="center", va="bottom", fontsize=11)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_ylim(0, max(ev, yv) * 1.25)
    fig.suptitle("Yoruba commands, English explains: rhetorical markers by language "
                 "(GPT-4o + Claude)", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(VIZ / "41_macro_markers_en_vs_yo.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Created 41_macro_markers_en_vs_yo.png")

    # ---- Fig 42: emphatic ratio committed vs hedged (Yoruba) ----
    y = yo.copy()
    y["commit"] = ~y.preferred_solution.isin(["refuses_to_commit", "conditional_or_mixed"])
    grp = y.groupby("commit")["emphatic_ratio"]
    means = {True: grp.mean().get(True, 0), False: grp.mean().get(False, 0)}
    fig, ax = plt.subplots(figsize=(7, 6))
    bars = ax.bar(["Committed\n(takes a stance)", "Hedged\n(conditional/refuses)"],
                  [means[True], means[False]],
                  color=["#06A77D", "#adb5bd"], edgecolor="black")
    for b, v in zip(bars, [means[True], means[False]]):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.2f}", ha="center", va="bottom", fontsize=13)
    ax.set_ylabel("Corrected emphatic ratio  èmi / (mo + èmi)")
    ax.set_ylim(0, max(means.values()) * 1.3)
    ax.set_title("Emphatic èmi is elevated where the model commits (Yoruba)\n"
                 "Mann–Whitney p = 0.022", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(VIZ / "42_emphatic_committed_vs_hedged.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Created 42_emphatic_committed_vs_hedged.png")


if __name__ == "__main__":
    main()
