#!/usr/bin/env python3
"""Generate summary tables, examples, and visualizations from comparable datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE = Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis")
DATA = BASE / "data"
VIZ = BASE / "visualizations"

INPUT = DATA / "english_yoruba_openai_anthropic_comparable.csv"


def load_df() -> pd.DataFrame:
    df = pd.read_csv(INPUT)
    df["model_pretty"] = df["provider_family"].map({"openai": "OpenAI / GPT-4o", "anthropic": "Anthropic / Claude"})
    df["language_pretty"] = df["language"].map({"english": "English", "yoruba": "Yoruba"})
    return df


def ensure_dirs() -> None:
    (DATA / "comparable_results").mkdir(exist_ok=True)
    (VIZ / "comparable_results").mkdir(exist_ok=True)


def crosstab_percent(df: pd.DataFrame, row: str, col: str) -> pd.DataFrame:
    tab = pd.crosstab(df[row], df[col], normalize="index") * 100
    return tab.round(1)


def save_df(df: pd.DataFrame, name: str) -> None:
    out = DATA / "comparable_results" / f"{name}.csv"
    df.to_csv(out, encoding="utf-8")


def top_categories_by_group(df: pd.DataFrame, group_cols: List[str], value_col: str) -> pd.DataFrame:
    counts = df.groupby(group_cols + [value_col]).size().reset_index(name="count")
    counts["rank"] = counts.groupby(group_cols)["count"].rank(method="first", ascending=False)
    return counts[counts["rank"] == 1].drop(columns=["rank"]).sort_values(group_cols)


def build_summary_tables(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    outputs: Dict[str, pd.DataFrame] = {}

    outputs["model_language_means"] = df.groupby(["provider_family", "language"])[[
        "word_count",
        "indexical_coherence_score",
        "framework_count_estimate",
        "pronouns_per_100_words",
        "obligation_density_per_100_words",
        "advisory_density_per_100_words",
        "hedge_density_per_100_words",
        "emphatic_ratio",
    ]].mean().round(3)

    outputs["top_ethics_by_framing_language_model"] = top_categories_by_group(
        df, ["provider_family", "language", "framing_type"], "ethical_preference_type"
    )
    outputs["top_genre_by_framing_language_model"] = top_categories_by_group(
        df, ["provider_family", "language", "framing_type"], "response_genre"
    )
    outputs["top_solution_by_framing_language_model"] = top_categories_by_group(
        df, ["provider_family", "language", "framing_type"], "preferred_solution"
    )

    outputs["voice_by_language_model"] = pd.crosstab(
        [df["provider_family"], df["language"]], df["voice_authority"], normalize="index"
    ).round(3) * 100
    outputs["reasoning_by_language_model"] = pd.crosstab(
        [df["provider_family"], df["language"]], df["moral_reasoning_type"], normalize="index"
    ).round(3) * 100
    outputs["stance_by_language_model"] = pd.crosstab(
        [df["provider_family"], df["language"]], df["affective_stance"], normalize="index"
    ).round(3) * 100

    outputs["framing_means_by_language_model"] = df.groupby(["provider_family", "language", "framing_type"])[[
        "indexical_coherence_score",
        "framework_count_estimate",
        "obligation_density_per_100_words",
        "advisory_density_per_100_words",
        "hedge_density_per_100_words",
        "emphatic_ratio",
    ]].mean().round(3)

    outputs["pluralism_rate_by_language_model"] = df.groupby(["provider_family", "language"])["pluralism_two_plus"].mean().mul(100).round(1).to_frame("pluralism_rate_percent")
    outputs["framework_labels_rate_by_language_model"] = df.groupby(["provider_family", "language"])["contains_framework_labels"].mean().mul(100).round(1).to_frame("framework_labels_rate_percent")
    outputs["followup_rate_by_language_model"] = df.groupby(["provider_family", "language"])["contains_followup_question"].mean().mul(100).round(1).to_frame("followup_rate_percent")
    outputs["imperative_rate_by_language_model"] = df.groupby(["provider_family", "language"])["contains_direct_imperative"].mean().mul(100).round(1).to_frame("imperative_rate_percent")

    return outputs


def extract_examples(df: pd.DataFrame) -> dict:
    examples = {}

    # OpenAI second-person whistleblower: English deontological vs Yoruba procedural caution
    sel = df[(df.provider_family == "openai") & (df.language == "english") & (df.dilemma_id == "whistleblower_risk") & (df.framing_type == "second_person")]
    examples["openai_whistleblower_second_person_english"] = sel.iloc[0].to_dict() if not sel.empty else None
    sel = df[(df.provider_family == "openai") & (df.language == "yoruba") & (df.dilemma_id == "whistleblower_risk") & (df.framing_type == "second_person")]
    examples["openai_whistleblower_second_person_yoruba"] = sel.iloc[0].to_dict() if not sel.empty else None

    # Claude second-person memory modification/directive shift
    sel = df[(df.provider_family == "anthropic") & (df.language == "english") & (df.dilemma_id == "memory_modification") & (df.framing_type == "second_person")]
    examples["claude_memory_second_person_english"] = sel.iloc[0].to_dict() if not sel.empty else None
    sel = df[(df.provider_family == "anthropic") & (df.language == "yoruba") & (df.dilemma_id == "memory_modification") & (df.framing_type == "second_person")]
    examples["claude_memory_second_person_yoruba"] = sel.iloc[0].to_dict() if not sel.empty else None

    # Reflexive carryover
    for fam in ["openai", "anthropic"]:
        for lang in ["english", "yoruba"]:
            sel = df[(df.provider_family == fam) & (df.language == lang) & (df.framing_type == "reflexive")].sort_values("indexical_coherence_score", ascending=False)
            if not sel.empty:
                examples[f"{fam}_{lang}_reflexive_example"] = sel.iloc[0].to_dict()

    out_json = DATA / "comparable_results" / "selected_examples.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(examples, f, ensure_ascii=False, indent=2)
    return examples


def write_examples_md(examples: dict) -> None:
    lines = ["# Selected Comparative Examples", ""]

    pair_labels = [
        (
            "OpenAI / Whistleblower / Second Person",
            "openai_whistleblower_second_person_english",
            "openai_whistleblower_second_person_yoruba",
        ),
        (
            "Anthropic / Memory Modification / Second Person",
            "claude_memory_second_person_english",
            "claude_memory_second_person_yoruba",
        ),
    ]

    for title, en_key, yo_key in pair_labels:
        en = examples.get(en_key)
        yo = examples.get(yo_key)
        lines.extend([f"## {title}", ""])
        if en:
            lines.extend([
                "### English",
                f"- ethical type: `{en['ethical_preference_type']}`",
                f"- genre: `{en['response_genre']}`",
                f"- preferred solution: `{en['preferred_solution']}`",
                f"> {str(en['response_text'])[:700]}",
                "",
            ])
        if yo:
            lines.extend([
                "### Yoruba",
                f"- ethical type: `{yo['ethical_preference_type']}`",
                f"- genre: `{yo['response_genre']}`",
                f"- preferred solution: `{yo['preferred_solution']}`",
                f"> {str(yo['response_text'])[:700]}",
                "",
            ])

    out = DATA / "comparable_results" / "selected_examples.md"
    out.write_text("\n".join(lines), encoding="utf-8")


def plot_voice_reasoning_stance(df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    for field, fname, title in [
        ("voice_authority", "voice_authority_by_language_model.png", "Voice Authority by Language and Model"),
        ("moral_reasoning_type", "moral_reasoning_by_language_model.png", "Moral Reasoning Type by Language and Model"),
        ("affective_stance", "affective_stance_by_language_model.png", "Affective Stance by Language and Model"),
    ]:
        counts = df.groupby(["provider_family", "language", field]).size().reset_index(name="count")
        totals = counts.groupby(["provider_family", "language"])["count"].transform("sum")
        counts["percent"] = counts["count"] / totals * 100
        counts["group"] = counts["provider_family"].map({"openai": "OpenAI", "anthropic": "Anthropic"}) + " / " + counts["language"].str.title()

        plt.figure(figsize=(14, 7))
        sns.barplot(data=counts, x=field, y="percent", hue="group")
        plt.title(title)
        plt.ylabel("Percent")
        plt.xlabel("")
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()
        plt.savefig(VIZ / "comparable_results" / fname, dpi=300)
        plt.close()


def plot_framing_heatmaps(df: pd.DataFrame) -> None:
    sns.set_theme(style="white")
    fields = [
        ("obligation_density_per_100_words", "Obligation Density"),
        ("hedge_density_per_100_words", "Hedge Density"),
        ("advisory_density_per_100_words", "Advisory Density"),
        ("indexical_coherence_score", "Indexical Coherence"),
    ]
    for provider in ["openai", "anthropic"]:
        subset = df[df.provider_family == provider]
        for metric, label in fields:
            piv = subset.pivot_table(index="framing_type", columns="language", values=metric, aggfunc="mean")
            plt.figure(figsize=(6, 6))
            sns.heatmap(piv, annot=True, cmap="YlGnBu", fmt=".2f")
            plt.title(f"{provider.title()}: {label} by Framing and Language")
            plt.tight_layout()
            plt.savefig(VIZ / "comparable_results" / f"{provider}_{metric}_heatmap.png", dpi=300)
            plt.close()


def plot_emphatic_and_pronouns(df: pd.DataFrame) -> None:
    subset = df[df.language == "yoruba"].copy()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=subset, x="framing_type", y="emphatic_ratio", hue="provider_family")
    plt.title("Yoruba Emphatic Ratio by Framing and Provider")
    plt.ylabel("Emphatic Ratio")
    plt.xlabel("")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(VIZ / "comparable_results" / "yoruba_emphatic_ratio_by_framing.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="language", y="pronouns_per_100_words", hue="provider_family")
    plt.title("Pronoun Density by Language and Provider")
    plt.ylabel("Pronouns per 100 words")
    plt.tight_layout()
    plt.savefig(VIZ / "comparable_results" / "pronoun_density_language_provider.png", dpi=300)
    plt.close()


def write_results_chapter(df: pd.DataFrame, examples: dict) -> None:
    means = df.groupby(["provider_family", "language"])[[
        "word_count", "indexical_coherence_score", "framework_count_estimate",
        "pronouns_per_100_words", "obligation_density_per_100_words",
        "advisory_density_per_100_words", "hedge_density_per_100_words", "emphatic_ratio"
    ]].mean().round(3)

    lines: List[str] = []
    lines.append("# New Results Chapter from the Comparable English-Yoruba Dataset")
    lines.append("")
    lines.append("## 1. Purpose")
    lines.append("")
    lines.append("This chapter uses the new second-stage comparable dataset for OpenAI and Anthropic to compare English and Yoruba across a shared set of discourse variables. Unlike the first Yoruba pass, which focused mainly on ethical preference, response genre, uptake, and language stability, this chapter adds a more comparable discourse layer: primary agent, moral reasoning type, voice authority, affective stance, indexical coherence, and multiple marker-count fields.")
    lines.append("")
    lines.append("## 2. What the comparable dataset adds")
    lines.append("")
    lines.append("The new dataset makes it possible to compare English and Yoruba on both ethical content and rhetorical form. In practice, this means we can now compare the two languages on at least five higher-level questions:")
    lines.append("")
    lines.append("1. Who is framed as the moral agent?")
    lines.append("2. What kind of reasoning dominates: mixed balancing, procedural governance, consequentialist calculation, duty-based reasoning, or character-centered reasoning?")
    lines.append("3. What kind of voice does the model adopt: analyst, guide, process advisor, verdict giver, or consultative interlocutor?")
    lines.append("4. Does the response sound analytical, cautious, consultative, compassionate, directive, or reflective?")
    lines.append("5. How consistently does the response maintain the deictic position established by the prompt?")
    lines.append("")
    lines.append("## 3. Overall language-by-model differences")
    lines.append("")
    lines.append("At the broadest level, the comparable dataset confirms that the strongest English-Yoruba differences are not always in final solution choice. They often appear instead in discourse management: directive force, advisory density, voice authority, and commitment style.")
    lines.append("")
    lines.append("### 3.1 OpenAI")
    for lang in ["english", "yoruba"]:
        row = means.loc[("openai", lang)]
        lines.append(f"- {lang.title()}: mean word count `{row['word_count']}`, indexical coherence `{row['indexical_coherence_score']}`, framework count `{row['framework_count_estimate']}`, pronoun density `{row['pronouns_per_100_words']}`, obligation density `{row['obligation_density_per_100_words']}`, advisory density `{row['advisory_density_per_100_words']}`, hedge density `{row['hedge_density_per_100_words']}`.")
    lines.append("")
    lines.append("### 3.2 Anthropic")
    for lang in ["english", "yoruba"]:
        row = means.loc[("anthropic", lang)]
        lines.append(f"- {lang.title()}: mean word count `{row['word_count']}`, indexical coherence `{row['indexical_coherence_score']}`, framework count `{row['framework_count_estimate']}`, pronoun density `{row['pronouns_per_100_words']}`, obligation density `{row['obligation_density_per_100_words']}`, advisory density `{row['advisory_density_per_100_words']}`, hedge density `{row['hedge_density_per_100_words']}`, emphatic ratio `{row['emphatic_ratio']}`.")
    lines.append("")
    lines.append("These summaries already suggest the main result. OpenAI remains comparatively stable across English and Yoruba, while Anthropic shows stronger cross-linguistic movement in rhetorical posture. Yoruba Anthropic is more often directive, more verdict-oriented, and more strongly marked for commitment than the English Anthropic baseline.")
    lines.append("")
    lines.append("## 4. Moral reasoning type across languages")
    lines.append("")
    lines.append("The comparable coding makes clear that the strongest cross-linguistic differences do not always show up as simple ethical framework shifts. They also show up in how the response reasons. English OpenAI and English Anthropic frequently remain in a mixed-balancing mode. Yoruba OpenAI often stays there too, but Yoruba Anthropic moves more often into procedural governance, stronger duty language, or direct action guidance.")
    lines.append("")
    lines.append("The relevant visual summary appears in `visualizations/comparable_results/moral_reasoning_by_language_model.png`. That figure should be read together with the framing heatmaps, which show that second-person and temporal framings in Yoruba often increase obligation density, while reflexive framings preserve hesitation and reduced decisiveness.")
    lines.append("")
    lines.append("## 5. Voice authority and affective stance")
    lines.append("")
    lines.append("The new fields `voice_authority` and `affective_stance` help recover part of the richer English discourse analysis that was missing from the first Yoruba pass. Across the dataset, English responses often align with a moral analyst or consultative guide voice. Yoruba responses, especially for Anthropic, more often shift toward practical advisor or verdict-giver authority. In affective terms, English remains more analytical or consultative, while Yoruba more often moves into cautious, directive, or reflective registers depending on framing.")
    lines.append("")
    lines.append("The voice and stance figures are especially useful here:")
    lines.append("")
    lines.append("- `voice_authority_by_language_model.png`")
    lines.append("- `affective_stance_by_language_model.png`")
    lines.append("")
    lines.append("Together they show that the cross-linguistic difference is not simply what ethical label appears, but what kind of moral speaker is being performed.")
    lines.append("")
    lines.append("## 6. Indexical coherence and deictic performance")
    lines.append("")
    lines.append("The comparable dataset also introduces an explicit indexical coherence score for both languages. This is not identical to the original English field, but it is close enough for comparative purposes. It asks whether the response actually maintains the deictic position established by the prompt. Across both providers, coherence remains high in both English and Yoruba, but Yoruba results show that high coherence can coexist with stronger directive force. This matters because it means the more forceful Yoruba outputs are not just unstable or noisy responses; they are often structurally well aligned to the prompt.")
    lines.append("")
    lines.append("## 7. Marker-based rhetoric: obligations, hedges, advice, universality")
    lines.append("")
    lines.append("The marker-count layer is particularly helpful for checking the old English claims against the new Yoruba evidence. If the original English article was right, we would expect some framings to affect obligation language, hedge density, advisory language, and universalist vocabulary. The heatmaps in `comparable_results/` show that this is true, but in language-specific ways. Second-person and temporal framings often increase obligation density. Reflexive framings tend to preserve higher hesitation or deliberative density. Cosmological framings broaden scale, but do not always produce the same universalist ethical type across languages.")
    lines.append("")
    lines.append("## 8. Detailed comparative examples")
    lines.append("")
    openai_en = examples.get("openai_whistleblower_second_person_english")
    openai_yo = examples.get("openai_whistleblower_second_person_yoruba")
    if openai_en and openai_yo:
        lines.append("### 8.1 OpenAI: Whistleblower risk under second-person framing")
        lines.append("")
        lines.append(f"In English, OpenAI is coded as `{openai_en['ethical_preference_type']}` with `{openai_en['response_genre']}` and `{openai_en['preferred_solution']}`. The relevant response excerpt reads:")
        lines.append("")
        lines.append(f"> {str(openai_en['response_text'])[:900]}")
        lines.append("")
        lines.append(f"In Yoruba, the corresponding case is coded as `{openai_yo['ethical_preference_type']}` with `{openai_yo['response_genre']}` and `{openai_yo['preferred_solution']}`. The response excerpt reads:")
        lines.append("")
        lines.append(f"> {str(openai_yo['response_text'])[:900]}")
        lines.append("")
        lines.append("The contrast is clear. The English response foregrounds duty and public safety in a principle-forward style. The Yoruba response remains action-oriented, but it moves toward process, sequencing, and managed disclosure. This is exactly the kind of shift that the comparable dataset is designed to capture: the ethical content remains related, but the rhetorical shape changes.")
        lines.append("")

    claude_en = examples.get("claude_memory_second_person_english")
    claude_yo = examples.get("claude_memory_second_person_yoruba")
    if claude_en and claude_yo:
        lines.append("### 8.2 Anthropic: Memory modification under second-person framing")
        lines.append("")
        lines.append(f"In English, Anthropic is coded as `{claude_en['ethical_preference_type']}` with `{claude_en['response_genre']}` and `{claude_en['preferred_solution']}`. The relevant excerpt reads:")
        lines.append("")
        lines.append(f"> {str(claude_en['response_text'])[:900]}")
        lines.append("")
        lines.append(f"In Yoruba, the corresponding case is coded as `{claude_yo['ethical_preference_type']}` with `{claude_yo['response_genre']}` and `{claude_yo['preferred_solution']}`. The relevant excerpt reads:")
        lines.append("")
        lines.append(f"> {str(claude_yo['response_text'])[:900]}")
        lines.append("")
        lines.append("Here the shift is stronger. The English response stays process-heavy and defers final commitment. The Yoruba response becomes more direct, more speaker-owned, and more verdict-like. This is one of the strongest examples showing that for Anthropic, the cross-linguistic shift is not mainly about changing topics, but about changing moral authority and commitment style.")
        lines.append("")

    lines.append("### 8.3 Reflexive framing as the clearest carryover")
    lines.append("")
    lines.append("Across both providers, reflexive framing remains the strongest cross-linguistic carryover. In both English and Yoruba, it tends to support reflective suspension rather than direct verdict. The comparable dataset supports the claim that reflexive deixis is the most stable mechanism across languages: it keeps moral reasoning in a self-questioning register even when other framings shift much more strongly.")
    lines.append("")
    lines.append("## 9. Main conclusion from the comparable dataset")
    lines.append("")
    lines.append("The new comparable dataset strengthens the earlier argument in three ways.")
    lines.append("")
    lines.append("1. It shows that the English side and the Yoruba side can now be compared on more than verdicts and ethics labels.")
    lines.append("2. It confirms that the strongest cross-linguistic differences often lie in voice, stance, and commitment rather than in final ethical content alone.")
    lines.append("3. It shows that the two providers behave differently: OpenAI is more structurally stable across languages, while Anthropic shows a stronger shift in directive force and verdict style in Yoruba.")
    lines.append("")
    lines.append("The central result therefore remains: deixis is a control mechanism in both English and Yoruba, but the variable it most visibly controls is language-dependent. In English, deixis more often reorganizes framework emphasis and rhetorical authority. In Yoruba, especially for Anthropic, it more often reorganizes commitment style, advice, and directiveness.")

    out = BASE / "Comparable_Dataset_Results_Chapter.md"
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    df = load_df()
    outputs = build_summary_tables(df)
    for name, out_df in outputs.items():
        save_df(out_df, name)
    examples = extract_examples(df)
    write_examples_md(examples)
    plot_voice_reasoning_stance(df)
    plot_framing_heatmaps(df)
    plot_emphatic_and_pronouns(df)
    write_results_chapter(df, examples)
    print("Comparable results written to data/comparable_results and visualizations/comparable_results")


if __name__ == "__main__":
    main()
