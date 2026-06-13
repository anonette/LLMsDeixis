#!/usr/bin/env python3
"""Heatmap: ethical_preference_type by model x dilemma (constrained)."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
df = pd.read_csv(BASE / "data" / "yoruba_merged_analysis.csv")
models = ["gpt-4o", "claude-3.5", "deepseek", "n-atlas"]
dilemmas = sorted(df.dilemma_id.unique())
ethics_order = [
    "utilitarian",
    "deontological",
    "care_ethics",
    "procedural_caution",
    "mixed",
    "virtue_ethics",
    "rights_based",
    "unclear",
]

rows, labels = [], []
for model in models:
    for dilemma in dilemmas:
        sub = df[(df.model == model) & (df.dilemma_id == dilemma)]
        counts = sub.ethical_preference_type.value_counts()
        total = len(sub)
        rows.append([counts.get(e, 0) / total * 100 if total else 0 for e in ethics_order])
        short = dilemma.replace("_", " ")[:14]
        labels.append(f"{model}\n{short}")

mat = np.array(rows)
fig, ax = plt.subplots(figsize=(14, 12))
im = ax.imshow(mat, aspect="auto", cmap="YlOrRd", vmin=0, vmax=100)
ax.set_xticks(range(len(ethics_order)))
ax.set_xticklabels([e.replace("_", "\n") for e in ethics_order], rotation=45, ha="right")
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontsize=7)
plt.colorbar(im, ax=ax, label="% of 9 framings")
ax.set_title("Ethical Framework by Model and Dilemma (Constrained Yoruba)", fontweight="bold")
plt.tight_layout()
out = BASE / "visualizations" / "22_ethics_heatmap_model_dilemma.png"
out.parent.mkdir(exist_ok=True)
plt.savefig(out, dpi=300, bbox_inches="tight")
print(f"Created: {out}")
