#!/usr/bin/env python3
"""Open-arm-only cross-language figure (English baseline vs OPEN Yoruba, no wrapper
on either side; GPT-4o + Claude + DeepSeek). Writes visualizations_open/43.
Built from the coded_content JSONs (the trustworthy open source)."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PIPE = ROOT.parent
VIZ = ROOT / "visualizations_open"
EN_C = PIPE / "yoruba_deixis_module/outputs/english_coded_content/english_open_comparison_coded_20260608_175242/coded_content.json"
YD = {"gpt-4o": "yoruba_control_gpt4o_20260608_120259_bilingual_20260608_134926_coded_20260608_161900",
      "claude": "yoruba_control_claude_20260608_122738_bilingual_20260608_134631_coded_20260608_161813",
      "deepseek": "yoruba_control_deepseek_20260608_124633_bilingual_20260608_135525_coded_20260608_161715"}
CD = PIPE / "yoruba_deixis_module/outputs/coded_content"
DIL = {"trolley_problem": "trolley", "icu_bed_allocation": "ICU bed", "whistleblower_risk": "whistleblower",
       "scholarship_fraud": "scholarship", "ai_consciousness": "AI mind", "memory_modification": "memory mod"}
EN, YO = "#457B9D", "#E63946"


def load(p):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    return pd.DataFrame(d.get("coded_records", d))


def main():
    en = load(EN_C)
    en["model"] = en["model"].map({"gpt-4o": "gpt-4o", "anthropic/claude-3.5-sonnet": "claude",
                                   "deepseek/deepseek-chat": "deepseek"})
    yo = pd.concat([load(CD / d / "coded_content.json").assign(model=m) for m, d in YD.items()],
                   ignore_index=True)

    def diff(s): return (~s.ethical_preference_type.isin(["mixed", "unclear", "reflexive", "refuses_to_commit"])).mean()
    def commit(s): return (~s.preferred_solution.isin(["refuses_to_commit", "conditional_or_mixed"])).mean()
    def imp(s): return s.contains_direct_imperative.astype(bool).mean()

    fig, axes = plt.subplots(1, 3, figsize=(17, 5.2))
    fig.suptitle("Open-arm cross-language effects (English baseline vs OPEN Yoruba; no wrapper either side; "
                 "GPT-4o + Claude + DeepSeek)", fontsize=13.5, fontweight="bold")

    # A: three rates EN vs YO
    ax = axes[0]
    labels = ["Differentiated\nethic", "Commits to\na side", "Direct\nimperative"]
    ev = [diff(en) * 100, commit(en) * 100, imp(en) * 100]
    yv = [diff(yo) * 100, commit(yo) * 100, imp(yo) * 100]
    x = np.arange(3); w = 0.38
    b1 = ax.bar(x - w / 2, ev, w, label="English", color=EN, edgecolor="black")
    b2 = ax.bar(x + w / 2, yv, w, label="Yoruba (open)", color=YO, edgecolor="black")
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{b.get_height():.0f}%", ha="center", va="bottom", fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel("% of responses"); ax.legend()
    ax.set_title("A. Yoruba is more differentiated, committed,\nand directive  (diff. ethic p<0.001)", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 60)

    # B: decision flips by dilemma
    ax = axes[1]
    m = pd.merge(en[["model", "dilemma_id", "framing_type", "preferred_solution"]],
                 yo[["model", "dilemma_id", "framing_type", "preferred_solution"]],
                 on=["model", "dilemma_id", "framing_type"], suffixes=("_en", "_yo"))
    m["flip"] = m.preferred_solution_en != m.preferred_solution_yo
    dv = m.groupby("dilemma_id").flip.mean().reindex(DIL.keys()).sort_values()
    ax.barh([DIL[d] for d in dv.index], dv.values * 100, color="#6a4c93", edgecolor="black")
    for i, v in enumerate(dv.values):
        ax.text(v * 100 + 1, i, f"{v*100:.0f}%", va="center", fontsize=10)
    ax.set_xlabel("% cells where the decision flips EN→YO"); ax.set_xlim(0, 80)
    ax.set_title(f"B. Switching language flips the decision\n(overall {m.flip.mean()*100:.0f}%)", fontsize=11, fontweight="bold")

    # C: emphatic ratio gradient (4 models, open) from merged
    ax = axes[2]
    o = pd.read_csv(ROOT / "data" / "open" / "yoruba_merged_analysis.csv")
    g = o.groupby("model")["emphatic_ratio"].mean().reindex(["claude-3.5", "gpt-4o", "deepseek", "n-atlas"])
    colors = ["#A23B72", "#2E86AB", "#F18F01", "#06A77D"]
    bars = ax.bar(["Claude", "GPT-4o", "DeepSeek", "N-ATLaS\n(native)"], g.values, color=colors, edgecolor="black")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{b.get_height():.2f}", ha="center", va="bottom", fontsize=11)
    ax.set_ylabel("corrected emphatic ratio  èmi/(mo+èmi)")
    ax.set_title("C. mo/èmi gradient — native N-ATLaS\nuses the LEAST èmi (inverts the cloud)", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 0.4)

    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(VIZ / "43_open_crosslang_summary.png", dpi=150, bbox_inches="tight")
    print("Created 43_open_crosslang_summary.png")


if __name__ == "__main__":
    main()
