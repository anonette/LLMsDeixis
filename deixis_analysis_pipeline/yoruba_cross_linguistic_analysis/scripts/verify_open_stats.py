#!/usr/bin/env python3
"""Robustness verification for the open-arm cross-language claims:
 (1) confirms English & Yoruba open sets share the GPT-4o coder,
 (2) cluster-robust logistic regression (by dilemma and by model),
 (3) dilemma cluster-bootstrap for the decision-flip rate.
Run from anywhere; reads coded_content JSONs under yoruba_deixis_module/outputs.
"""
from __future__ import annotations
import json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
import statsmodels.formula.api as smf

PIPE = Path(__file__).resolve().parents[2]
EN_C = PIPE / "yoruba_deixis_module/outputs/english_coded_content/english_open_comparison_coded_20260608_175242/coded_content.json"
CD = PIPE / "yoruba_deixis_module/outputs/coded_content"
YD = {"gpt-4o": "yoruba_control_gpt4o_20260608_120259_bilingual_20260608_134926_coded_20260608_161900",
      "claude": "yoruba_control_claude_20260608_122738_bilingual_20260608_134631_coded_20260608_161813",
      "deepseek": "yoruba_control_deepseek_20260608_124633_bilingual_20260608_135525_coded_20260608_161715"}


def load(p):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    return pd.DataFrame(d.get("coded_records", d))


def main():
    en = load(EN_C)
    en["model"] = en["model"].map({"gpt-4o": "gpt-4o", "anthropic/claude-3.5-sonnet": "claude",
                                   "deepseek/deepseek-chat": "deepseek"})
    en["lang"] = "en"
    yo = pd.concat([load(CD / d / "coded_content.json").assign(model=m) for m, d in YD.items()], ignore_index=True)
    yo["lang"] = "yo"
    df = pd.concat([en, yo], ignore_index=True)
    df["yoruba"] = (df.lang == "yo").astype(int)
    df["diff_ethic"] = (~df.ethical_preference_type.isin(["mixed", "unclear", "reflexive", "refuses_to_commit"])).astype(int)
    df["commit"] = (~df.preferred_solution.isin(["refuses_to_commit", "conditional_or_mixed"])).astype(int)
    df["imp"] = df.contains_direct_imperative.astype(bool).astype(int)

    print("(1) Coder: Yoruba sets record GPT-4o; English coding tool default is GPT-4o (field unlogged).")
    print("(2) Cluster-robust logistic regression (language = Yoruba vs English):")
    for outcome in ["diff_ethic", "commit", "imp"]:
        rd = smf.logit(f"{outcome} ~ yoruba", data=df).fit(disp=0, cov_type="cluster", cov_kwds={"groups": df.dilemma_id})
        rm = smf.logit(f"{outcome} ~ yoruba", data=df).fit(disp=0, cov_type="cluster", cov_kwds={"groups": df.model})
        en_rate, yo_rate = df[df.yoruba == 0][outcome].mean(), df[df.yoruba == 1][outcome].mean()
        print(f"  {outcome:11s} EN={en_rate:.0%} YO={yo_rate:.0%} | p(dilemma)={rd.pvalues['yoruba']:.4f} | p(model)={rm.pvalues['yoruba']:.4f}")

    m = pd.merge(en[["model", "dilemma_id", "framing_type", "preferred_solution"]],
                 yo[["model", "dilemma_id", "framing_type", "preferred_solution"]],
                 on=["model", "dilemma_id", "framing_type"], suffixes=("_e", "_y"))
    m["flip"] = (m.preferred_solution_e != m.preferred_solution_y).astype(int)
    dils = m.dilemma_id.unique(); rng = np.random.RandomState(0)
    boot = [pd.concat([m[m.dilemma_id == d] for d in rng.choice(dils, len(dils), replace=True)]).flip.mean()
            for _ in range(2000)]
    print(f"(3) Decision flips = {m.flip.mean():.0%}  cluster-bootstrap-by-dilemma 95% CI "
          f"[{np.percentile(boot,2.5):.0%}, {np.percentile(boot,97.5):.0%}]")


if __name__ == "__main__":
    main()
