#!/usr/bin/env python3
"""How deixis (framing) and language shape DECISIONS and ETHICAL APPROACH.

Cross-language comparable set (English + Yoruba x GPT-4o + Claude, 6 dilemmas x
9 framings). Writes visualizations_open/40_deixis_decision_summary.png.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ANALYSIS_ROOT = SCRIPT_DIR.parent
CSV = ANALYSIS_ROOT / "data" / "english_yoruba_openai_anthropic_comparable.csv"
OUT = ANALYSIS_ROOT / "visualizations_open" / "40_deixis_decision_summary.png"

FRAMING_ORDER = ["impersonal", "second_person", "first_person", "reflexive", "dialogic",
                 "spatial", "temporal", "cosmological", "first_person_plural"]
DIL_SHORT = {"trolley_problem": "trolley", "icu_bed_allocation": "ICU bed",
             "whistleblower_risk": "whistleblower", "scholarship_fraud": "scholarship",
             "ai_consciousness": "AI mind", "memory_modification": "memory mod"}
ETHIC_ORDER = ["utilitarian", "deontological/rights", "care/virtue", "procedural", "mixed/unclear"]
LANG_COLOR = {"english": "#457B9D", "yoruba": "#E63946"}


def bucket(e):
    if e == "utilitarian":
        return "utilitarian"
    if e in ("deontological", "rights_based"):
        return "deontological/rights"
    if e in ("care_ethics", "virtue_ethics"):
        return "care/virtue"
    if e == "procedural_caution":
        return "procedural"
    return "mixed/unclear"


def main():
    df = pd.read_csv(CSV)
    df["ethic"] = df["ethical_preference_type"].map(bucket)
    df["commit"] = ~df["preferred_solution"].isin(["refuses_to_commit", "conditional_or_mixed"])

    fig, axes = plt.subplots(2, 2, figsize=(17, 12))
    fig.suptitle("How deixis & language shape the DECISION and the ETHICAL APPROACH\n"
                 "(English vs Yoruba; GPT-4o + Claude; 6 dilemmas x 9 framings)",
                 fontsize=15, fontweight="bold")

    # A: ethical approach by language
    ax = axes[0, 0]
    ct = pd.crosstab(df["language"], df["ethic"], normalize="index").reindex(columns=ETHIC_ORDER)
    x = np.arange(len(ETHIC_ORDER)); w = 0.38
    for i, lang in enumerate(["english", "yoruba"]):
        ax.bar(x + (i - 0.5) * w, ct.loc[lang].values, w, label=lang,
               color=LANG_COLOR[lang], edgecolor="black", linewidth=0.4)
    ax.set_xticks(x); ax.set_xticklabels(ETHIC_ORDER, rotation=25, ha="right")
    ax.set_ylabel("share of responses"); ax.legend()
    ax.set_title("A. Ethical approach by language\nYoruba commits to differentiated ethics; English collapses to 'mixed'",
                 fontweight="bold", fontsize=11)

    # B: commit rate by framing x language
    ax = axes[0, 1]
    cm = df.pivot_table("commit", "framing_type", "language", aggfunc="mean").reindex(FRAMING_ORDER)
    x = np.arange(len(FRAMING_ORDER))
    for i, lang in enumerate(["english", "yoruba"]):
        ax.bar(x + (i - 0.5) * w, cm[lang].values, w, label=lang,
               color=LANG_COLOR[lang], edgecolor="black", linewidth=0.4)
    ax.set_xticks(x); ax.set_xticklabels([f.replace("_", "\n") for f in FRAMING_ORDER], fontsize=8)
    ax.set_ylabel("commit rate (1 - hedge/refuse)"); ax.legend()
    ax.set_title("B. Decisiveness by framing\n'you' (second person) most decisive; reflexive least; Yoruba > English",
                 fontweight="bold", fontsize=11)

    # C: decision divergence English vs Yoruba by dilemma
    ax = axes[1, 0]
    piv = df.pivot_table(index=["model_label", "dilemma_id", "framing_type"],
                         columns="language", values="preferred_solution", aggfunc="first").dropna()
    piv["diff"] = piv["english"] != piv["yoruba"]
    dv = piv.groupby("dilemma_id")["diff"].mean().reindex(DIL_SHORT.keys()).sort_values()
    ax.barh([DIL_SHORT[d] for d in dv.index], dv.values, color="#6a4c93", edgecolor="black")
    for i, v in enumerate(dv.values):
        ax.text(v + 0.01, i, f"{v:.0%}", va="center", fontsize=9)
    ax.set_xlim(0, 0.75); ax.set_xlabel("share of cells where the DECISION flips English -> Yoruba")
    overall = piv["diff"].mean()
    ax.set_title(f"C. Same model + dilemma + framing, different language ->\ndifferent decision in {overall:.0%} of cells",
                 fontweight="bold", fontsize=11)

    # D: ethic by framing heatmap
    ax = axes[1, 1]
    hm = pd.crosstab(df["framing_type"], df["ethic"], normalize="index").reindex(
        index=FRAMING_ORDER, columns=ETHIC_ORDER)
    im = ax.imshow(hm.values, cmap="YlOrRd", aspect="auto", vmin=0, vmax=hm.values.max())
    ax.set_xticks(range(len(ETHIC_ORDER))); ax.set_xticklabels(ETHIC_ORDER, rotation=25, ha="right", fontsize=8)
    ax.set_yticks(range(len(FRAMING_ORDER))); ax.set_yticklabels([f.replace("_", " ") for f in FRAMING_ORDER], fontsize=8)
    for i in range(len(FRAMING_ORDER)):
        for j in range(len(ETHIC_ORDER)):
            ax.text(j, i, f"{hm.values[i, j]:.0%}", ha="center", va="center", fontsize=7)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("D. Which framing evokes which ethic\nimpersonal->duty, 'you'->utilitarian, cosmological->procedural",
                 fontweight="bold", fontsize=11)

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUT, dpi=150, bbox_inches="tight")
    print(f"Created: {OUT}")


if __name__ == "__main__":
    main()
