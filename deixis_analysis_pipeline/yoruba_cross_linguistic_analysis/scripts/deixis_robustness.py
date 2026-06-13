#!/usr/bin/env python3
"""Robustness / uncertainty for the deixis -> decision/ethics claims.

Wilson 95% CIs for headline proportions, two-proportion tests for the language
contrasts, and a chi-square for framing x ethic within each language. Prints a
table to paste into Deixis_Decision_Effects_Summary.md.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import norm, chi2_contingency, fisher_exact

CSV = Path(__file__).resolve().parents[1] / "data" / "english_yoruba_openai_anthropic_comparable.csv"


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return ((c - h) / d, (c + h) / d)


def two_prop(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = (p * (1 - p) * (1 / n1 + 1 / n2)) ** 0.5
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    return z, 2 * (1 - norm.cdf(abs(z)))


def line(label, k, n):
    lo, hi = wilson(k, n)
    return f"| {label} | {k}/{n} = {k/n:.0%} | [{lo:.0%}, {hi:.0%}] |"


def main():
    df = pd.read_csv(CSV)
    df["commit"] = ~df["preferred_solution"].isin(["refuses_to_commit", "conditional_or_mixed"])
    df["refuse"] = df["preferred_solution"] == "refuses_to_commit"

    print("### Headline proportions with Wilson 95% CIs\n")
    print("| Quantity | Estimate | 95% CI |")
    print("|---|---|---|")
    # decision flip
    piv = df.pivot_table(index=["model_label", "dilemma_id", "framing_type"],
                         columns="language", values="preferred_solution", aggfunc="first").dropna()
    diff = (piv["english"] != piv["yoruba"]).sum()
    print(line("Decision flips EN-YO (all)", diff, len(piv)))
    wb = piv[piv.index.get_level_values("dilemma_id") == "whistleblower_risk"]
    print(line("Decision flips EN-YO (whistleblower)", (wb["english"] != wb["yoruba"]).sum(), len(wb)))
    # refuse by language
    for lang in ["english", "yoruba"]:
        s = df[df.language == lang]
        print(line(f"Refuse-to-commit ({lang})", s["refuse"].sum(), len(s)))
    print()

    print("### Language contrasts (two-proportion z-test)\n")
    print("| Contrast | EN | YO | z | p |")
    print("|---|---|---|---|---|")
    en, yo = df[df.language == "english"], df[df.language == "yoruba"]
    for name, col in [("refuse-to-commit", "refuse"), ("commit", "commit")]:
        z, p = two_prop(yo[col].sum(), len(yo), en[col].sum(), len(en))
        print(f"| {name} | {en[col].mean():.0%} | {yo[col].mean():.0%} | {z:+.2f} | {p:.3f} |")
    # ethical register: procedural+duty+care+util ("differentiated") vs mixed/unclear
    def diff_ethic(s):
        return (~s["ethical_preference_type"].isin(["mixed", "unclear", "reflexive", "refuses_to_commit"])).sum()
    z, p = two_prop(diff_ethic(yo), len(yo), diff_ethic(en), len(en))
    print(f"| differentiated ethic (non-mixed) | {diff_ethic(en)/len(en):.0%} | {diff_ethic(yo)/len(yo):.0%} | {z:+.2f} | {p:.3f} |")
    print()

    print("### Framing × ethic association (chi-square), within each language\n")
    print("| Language | chi2 | dof | p | note |")
    print("|---|---|---|---|---|")
    df["eb"] = df["ethical_preference_type"].apply(
        lambda e: "differentiated" if e not in ("mixed", "unclear", "reflexive", "refuses_to_commit") else "mixed")
    for lang in ["english", "yoruba"]:
        s = df[df.language == lang]
        ct = pd.crosstab(s["framing_type"], s["eb"])
        try:
            chi2, p, dof, _ = chi2_contingency(ct)
            note = "sparse (expected<5)"
            print(f"| {lang} | {chi2:.1f} | {dof} | {p:.3f} | {note} |")
        except Exception as e:
            print(f"| {lang} | - | - | - | {e} |")
    print()

    print("### #5 decisiveness: reflexive vs second_person commit (per language, N=12 each)\n")
    print("| Language | reflexive commit | 2nd-person commit | Fisher p |")
    print("|---|---|---|---|")
    for lang in ["english", "yoruba"]:
        s = df[df.language == lang]
        rf = s[s.framing_type == "reflexive"]["commit"]
        sp = s[s.framing_type == "second_person"]["commit"]
        table = [[sp.sum(), len(sp) - sp.sum()], [rf.sum(), len(rf) - rf.sum()]]
        _, p = fisher_exact(table)
        print(f"| {lang} | {rf.sum()}/{len(rf)} | {sp.sum()}/{len(sp)} | {p:.3f} |")


if __name__ == "__main__":
    main()
