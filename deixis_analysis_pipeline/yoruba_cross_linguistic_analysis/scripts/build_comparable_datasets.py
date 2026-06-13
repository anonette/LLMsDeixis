#!/usr/bin/env python3
"""Build comparable English/Yoruba datasets for OpenAI and Anthropic runs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


BASE = Path(r"C:\dev\deixis\deixis_analysis_pipeline")
OUT_DIR = BASE / "yoruba_cross_linguistic_analysis" / "data"


ENGLISH_CODED = BASE / "yoruba_deixis_module" / "outputs" / "english_coded_content" / "english_open_comparison_coded_20260608_175242" / "coded_content.csv"
YORUBA_MERGED = BASE / "yoruba_cross_linguistic_analysis" / "data" / "yoruba_merged_analysis.csv"

SESSIONS = {
    "english": {
        "gpt-4o": BASE / "generation_logs" / "multi_dilemma_20250804_170010",
        "claude": BASE / "generation_logs" / "anthropic_claude_20250805_125046",
    },
    "yoruba": {
        "gpt-4o": BASE / "generation_logs" / "yoruba_gpt4o_20260608_105712",
        "claude": BASE / "generation_logs" / "yoruba_claude_20260608_110809",
    },
}


ENGLISH_PRONOUN_PATTERNS = {
    "first_person": r"\b(i|me|my|mine|myself)\b",
    "first_person_plural": r"\b(we|us|our|ours|ourselves)\b",
    "second_person": r"\b(you|your|yours|yourself|yourselves)\b",
    "third_person": r"\b(he|she|they|them|their|theirs|him|her|his|hers|himself|herself|themselves)\b",
}

ENGLISH_TEMPORAL = r"\b(now|today|later|soon|immediately|recently|moment|future|long-term|short-term|at this moment|going forward)\b"
ENGLISH_SPATIAL = r"\b(here|there|out there|from this position|where i stand|nearby|beyond)\b"
ENGLISH_DEMONSTRATIVES = r"\b(this|that|these|those)\b"
ENGLISH_OBLIGATION = r"\b(must|should|need to|have to|ought to|cannot|can't)\b"
ENGLISH_ADVISORY = r"\b(consider|i would recommend|it may be prudent|i encourage|here are some|you could|you should)\b"
ENGLISH_HEDGES = r"\b(might|may|could|perhaps|seems|appears|likely|arguably|maybe|reasonable|uncertain|uncertainty)\b"
ENGLISH_UNIVERSALIST = r"\b(humanity|dignity|universal|all beings|everyone|society|cosmos|stewardship|all existence)\b"

YORUBA_PRONOUN_PATTERNS = {
    "first_person_regular": r"\bmo\b",
    "first_person_emphatic": r"\b(emi|èmi|émí|èmí)\b",
    "first_person_object": r"\bmi\b",
    "first_person_plural": r"\b(a|awa|àwa)\b",
    "second_person": r"\b(ìwọ|iwo|iwọ|o|ọ|ẹ)\b",
    "third_person": r"\b(ó|won|wọn|wọ́n|oun|òun)\b",
}

YORUBA_TEMPORAL = r"(ní báyìí|lónìí|lẹ́sẹ̀kẹsẹ̀|ní àkókò yìí|lọ́la|ní kíákíá|ṣẹ̀ṣẹ̀|níwájú|ọjọ́ iwájú)"
YORUBA_SPATIAL = r"(níbí|níbẹ̀|níbẹ|láti ipò yìí|ní ita|kárí ayé|ní ojú)"
YORUBA_DEMONSTRATIVES = r"\b(yìí|yẹn|wọ̀nyí|èyí|àwọn wọ̀nyí|náà)\b"
YORUBA_OBLIGATION = r"(gbọ́dọ̀|yẹ kí|kò yẹ|nílò láti|gbodo|ye ki|must|mọ̀ gbọdọ̀|ọdọ̀)"
YORUBA_ADVISORY = r"(ó yẹ kí|o yẹ kí|ìwọ ó yẹ kí|dára láti|gbìyànjú láti|ẹ jẹ́ ká|jẹ́ kí)"
YORUBA_HEDGES = r"(bóyá|ó lè|lè jẹ́|ó ṣeé ṣe|ṣeé ṣe|ṣùgbọ́n)"
YORUBA_UNIVERSALIST = r"(gbogbo àwọn tó kan|gbogbo ènìyàn|àwùjọ|ayé|ẹ̀tọ́ ènìyàn|ìwà rere|ọkàn rere|kárí ayé)"


def read_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_response_lookup(session_dir: Path) -> Tuple[Dict[Tuple[str, str], dict], Optional[str], Optional[str]]:
    lookup: Dict[Tuple[str, str], dict] = {}
    wrapper = None
    session_model = None

    complete = session_dir / "complete_session_data.json"
    if complete.exists():
        complete_data = read_json(complete)
        session_model = complete_data.get("generation_session", {}).get("model")
        wrapper = complete_data.get("generation_session", {}).get("response_instruction")

    for file in session_dir.glob("*_responses.json"):
        data = read_json(file)
        dilemma_id = data["dilemma_id"]
        for framing_type, payload in data.get("responses", {}).items():
            lookup[(dilemma_id, framing_type)] = {
                "response_text": payload.get("response", ""),
                "deictic_question": payload.get("deictic_question", ""),
                "prompt_sent": payload.get("prompt_sent"),
                "source_model": data.get("model") or session_model,
            }
    return lookup, wrapper, session_model


def count_regex(pattern: str, text: str) -> int:
    if not text:
        return 0
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def normalize_per_100(count: int, word_count: int) -> float:
    if not word_count:
        return 0.0
    return count / word_count * 100.0


def safe_int(value) -> int:
    if pd.isna(value):
        return 0
    try:
        return int(value)
    except Exception:
        return 0


def estimate_framework_count(text: str, language: str) -> int:
    if not text:
        return 0
    text_l = text.lower()
    if language == "english":
        patterns = [
            r"utilitarian|consequential",
            r"deontolog|duty|rights",
            r"virtue",
            r"care ethics|care",
            r"justice|fairness",
            r"autonomy|consent",
        ]
    else:
        patterns = [
            r"utilitarian|ànfààní|àbájáde",
            r"deontolog|ẹ̀tọ́|ojúṣe|òtítọ́",
            r"virtue|ìwà rere|ìwà",
            r"care|àánú|ìtọ́jú",
            r"justice|òdodo|ìdájọ́",
            r"autonomy|òmìnira|ìfọkànsìn|ìmúra sí",
        ]
    return sum(1 for p in patterns if re.search(p, text_l, flags=re.IGNORECASE))


def infer_primary_agent(framing_type: str, response_text: str) -> str:
    text_l = response_text.lower()
    if framing_type == "first_person":
        return "speaker_self"
    if framing_type == "first_person_plural":
        return "collective_self"
    if framing_type == "second_person":
        return "addressee_as_decider"
    if framing_type == "reflexive":
        return "reflective_self"
    if framing_type == "dialogic":
        return "consultative_interlocutor"
    if framing_type == "impersonal":
        if any(x in text_l for x in ["organization", "institution", "ilé iṣẹ", "àjọ", "aláṣẹ"]):
            return "institutional_actor"
        return "third_person_actor"
    if framing_type == "spatial":
        return "situated_self"
    if framing_type == "temporal":
        return "urgent_self"
    if framing_type == "cosmological":
        return "distributed_collective"
    return "unspecified"


def infer_moral_reasoning_type(ethical_type: str, framing_type: str, preferred_solution: str) -> str:
    if framing_type == "reflexive" and preferred_solution in {"conditional_or_mixed", "refuses_to_commit"}:
        return "reflective_deliberation"
    mapping = {
        "utilitarian": "consequentialist_calculation",
        "deontological": "duty_based_reasoning",
        "rights_based": "rights_based_reasoning",
        "virtue_ethics": "character_based_reasoning",
        "care_ethics": "relational_care_reasoning",
        "procedural_caution": "procedural_governance",
        "mixed": "mixed_balancing",
        "unclear": "indeterminate",
    }
    return mapping.get(ethical_type, "indeterminate")


def infer_voice_authority(response_genre: str, contains_followup_question: bool, contains_direct_imperative: bool, preferred_solution: str, framing_type: str) -> str:
    if response_genre == "direct_verdict":
        return "verdict_giver"
    if contains_followup_question:
        return "consultative_guide"
    if response_genre == "procedural_advice" and contains_direct_imperative:
        return "practical_advisor"
    if response_genre == "procedural_advice":
        return "process_guide"
    if framing_type in {"impersonal", "cosmological"}:
        return "moral_analyst"
    if preferred_solution == "refuses_to_commit":
        return "analytical_guide"
    return "moral_analyst"


def infer_affective_stance(ethical_type: str, response_genre: str, framing_type: str, contains_followup_question: bool, preferred_solution: str) -> str:
    if framing_type == "reflexive" and preferred_solution in {"conditional_or_mixed", "refuses_to_commit"}:
        return "reflective_hesitant"
    if ethical_type == "care_ethics":
        return "compassionate"
    if ethical_type == "procedural_caution":
        return "cautious"
    if response_genre == "direct_verdict":
        return "directive"
    if contains_followup_question:
        return "consultative"
    if response_genre == "balanced_framework_exposition":
        return "analytical"
    return "mixed"


def coherence_from_uptake(uptake: str, language_stability: Optional[str], framing_type: str, metrics: Dict[str, int]) -> Tuple[float, str]:
    base = {
        "strong_uptake": 0.95,
        "partial_uptake": 0.8,
        "weak_uptake": 0.6,
    }.get(uptake, 0.75)

    note_parts: List[str] = []
    if framing_type == "first_person" and metrics["first_person_count"] > 0:
        base += 0.02
        note_parts.append("first-person maintained")
    if framing_type == "second_person" and metrics["second_person_count"] > 0:
        base += 0.02
        note_parts.append("second-person maintained")
    if framing_type == "first_person_plural" and metrics["first_person_plural_count"] > 0:
        base += 0.02
        note_parts.append("collective voice maintained")
    if framing_type == "temporal" and metrics["temporal_marker_count"] > 0:
        base += 0.02
        note_parts.append("temporal marking visible")
    if framing_type == "spatial" and metrics["spatial_marker_count"] > 0:
        base += 0.02
        note_parts.append("spatial marking visible")
    if framing_type == "cosmological" and metrics["universalist_marker_count"] > 0:
        base += 0.02
        note_parts.append("expanded perspective visible")
    if framing_type == "impersonal" and metrics["first_person_count"] > 2:
        base -= 0.08
        note_parts.append("first-person bleed into impersonal frame")

    if language_stability and language_stability not in {"clean_yoruba", "english_clean", "clean_english", "not_applicable"}:
        base -= 0.1
        note_parts.append(f"stability reduced: {language_stability}")

    base = max(0.0, min(1.0, base))
    if not note_parts:
        note_parts.append("no major deictic disruption detected")
    return round(base, 3), "; ".join(note_parts)


def english_metrics(text: str) -> Dict[str, int]:
    counts = {k: count_regex(v, text) for k, v in ENGLISH_PRONOUN_PATTERNS.items()}
    return {
        "first_person_count": counts["first_person"],
        "first_person_emphatic_count": 0,
        "first_person_plural_count": counts["first_person_plural"],
        "second_person_count": counts["second_person"],
        "third_person_count": counts["third_person"],
        "temporal_marker_count": count_regex(ENGLISH_TEMPORAL, text),
        "spatial_marker_count": count_regex(ENGLISH_SPATIAL, text),
        "demonstrative_count": count_regex(ENGLISH_DEMONSTRATIVES, text),
        "obligation_marker_count": count_regex(ENGLISH_OBLIGATION, text),
        "advisory_formula_count": count_regex(ENGLISH_ADVISORY, text),
        "hedge_marker_count": count_regex(ENGLISH_HEDGES, text),
        "universalist_marker_count": count_regex(ENGLISH_UNIVERSALIST, text),
    }


def yoruba_metrics(text: str, row: pd.Series) -> Dict[str, int]:
    # Reuse existing Yoruba counts when available.
    first_regular = safe_int(row.get("first_singular_mo", 0))
    first_emph = safe_int(row.get("first_singular_emi", 0))
    first_obj = safe_int(row.get("first_singular_mi", 0))
    first_pl = safe_int(row.get("first_plural_a", 0)) + safe_int(row.get("first_plural_awa", 0))
    second = safe_int(row.get("second_person_o", 0)) + safe_int(row.get("second_person_e", 0)) + safe_int(row.get("second_person_iwo", 0))
    third = safe_int(row.get("third_person_o_3rd", 0)) + safe_int(row.get("third_person_won", 0)) + safe_int(row.get("third_person_oun", 0))
    return {
        "first_person_count": first_regular + first_emph + first_obj,
        "first_person_emphatic_count": first_emph,
        "first_person_plural_count": first_pl,
        "second_person_count": second,
        "third_person_count": third,
        "temporal_marker_count": count_regex(YORUBA_TEMPORAL, text),
        "spatial_marker_count": count_regex(YORUBA_SPATIAL, text),
        "demonstrative_count": count_regex(YORUBA_DEMONSTRATIVES, text),
        "obligation_marker_count": count_regex(YORUBA_OBLIGATION, text),
        "advisory_formula_count": count_regex(YORUBA_ADVISORY, text),
        "hedge_marker_count": count_regex(YORUBA_HEDGES, text),
        "universalist_marker_count": count_regex(YORUBA_UNIVERSALIST, text),
    }


def build_english_dataset() -> pd.DataFrame:
    df = pd.read_csv(ENGLISH_CODED)
    df = df[df["model"].isin(["gpt-4o", "anthropic/claude-3.5-sonnet"])].copy()

    lookups = {}
    wrappers = {}
    actual_models = {}
    for key, session in SESSIONS["english"].items():
        lookup, wrapper, actual_model = load_response_lookup(session)
        lookups[key] = lookup
        wrappers[key] = wrapper
        actual_models[key] = actual_model

    rows = []
    for _, r in df.iterrows():
        family = "gpt-4o" if r["model"] == "gpt-4o" else "claude"
        lookup = lookups[family]
        raw = lookup[(r["dilemma_id"], r["framing_type"])]
        response_text = raw["response_text"]
        prompt_text = raw["deictic_question"]
        word_count = len(response_text.split())
        metrics = english_metrics(response_text)
        indexical_score, indexical_notes = coherence_from_uptake(
            r["deictic_uptake_quality"],
            "not_applicable",
            r["framing_type"],
            metrics,
        )
        framework_count = estimate_framework_count(response_text, "english")
        row = {
            "language": "english",
            "provider_family": "openai" if family == "gpt-4o" else "anthropic",
            "model_label": "gpt-4o" if family == "gpt-4o" else "claude",
            "raw_model_name": actual_models[family] or r["model"],
            "dilemma_id": r["dilemma_id"],
            "framing_type": r["framing_type"],
            "prompt_wrapper": wrappers[family],
            "prompt_text": prompt_text,
            "prompt_full": prompt_text,
            "response_text": response_text,
            "word_count": word_count,
            "preferred_solution": r["preferred_solution"],
            "ethical_preference_type": r["ethical_preference_type"],
            "response_genre": r["response_genre"],
            "deictic_uptake_quality": r["deictic_uptake_quality"],
            "language_stability": "not_applicable",
            "primary_agent": infer_primary_agent(r["framing_type"], response_text),
            "moral_reasoning_type": infer_moral_reasoning_type(r["ethical_preference_type"], r["framing_type"], r["preferred_solution"]),
            "voice_authority": infer_voice_authority(r["response_genre"], bool(r["contains_followup_question"]), bool(r["contains_direct_imperative"]), r["preferred_solution"], r["framing_type"]),
            "affective_stance": infer_affective_stance(r["ethical_preference_type"], r["response_genre"], r["framing_type"], bool(r["contains_followup_question"]), r["preferred_solution"]),
            "indexical_coherence_score": indexical_score,
            "indexical_coherence_notes": indexical_notes,
            "contains_framework_labels": bool(r["contains_framework_labels"]),
            "contains_followup_question": bool(r["contains_followup_question"]),
            "contains_direct_imperative": bool(r["contains_direct_imperative"]),
            "contains_role_exit": bool(r["contains_role_exit"]),
            "contains_translation_behavior": False,
            "framework_count_estimate": framework_count,
            "pluralism_two_plus": framework_count >= 2,
        }
        row.update(metrics)
        row["pronouns_per_100_words"] = normalize_per_100(
            row["first_person_count"] + row["first_person_plural_count"] + row["second_person_count"] + row["third_person_count"],
            word_count,
        )
        row["obligation_density_per_100_words"] = normalize_per_100(row["obligation_marker_count"], word_count)
        row["advisory_density_per_100_words"] = normalize_per_100(row["advisory_formula_count"], word_count)
        row["hedge_density_per_100_words"] = normalize_per_100(row["hedge_marker_count"], word_count)
        row["emphatic_ratio"] = 0.0
        rows.append(row)
    return pd.DataFrame(rows)


def build_yoruba_dataset() -> pd.DataFrame:
    df = pd.read_csv(YORUBA_MERGED)
    df = df[df["model"].isin(["gpt-4o", "claude-3.5"])].copy()

    lookups = {}
    wrappers = {}
    actual_models = {}
    for key, session in SESSIONS["yoruba"].items():
        lookup, wrapper, actual_model = load_response_lookup(session)
        lookups[key] = lookup
        wrappers[key] = wrapper
        actual_models[key] = actual_model

    rows = []
    for _, r in df.iterrows():
        family = "gpt-4o" if r["model"] == "gpt-4o" else "claude"
        raw = lookups[family][(r["dilemma_id"], r["framing_type"])]
        response_text = raw["response_text"]
        prompt_text = raw["deictic_question"]
        prompt_full = raw.get("prompt_sent") or raw["deictic_question"]
        word_count = int(r.get("word_count", 0) or len(response_text.split()))
        metrics = yoruba_metrics(response_text, r)
        indexical_score, indexical_notes = coherence_from_uptake(
            r["deictic_uptake_quality"],
            str(r["language_stability"]),
            r["framing_type"],
            metrics,
        )
        framework_count = estimate_framework_count(response_text, "yoruba")
        row = {
            "language": "yoruba",
            "provider_family": "openai" if family == "gpt-4o" else "anthropic",
            "model_label": "gpt-4o" if family == "gpt-4o" else "claude",
            "raw_model_name": actual_models[family] or r["model"],
            "dilemma_id": r["dilemma_id"],
            "framing_type": r["framing_type"],
            "prompt_wrapper": wrappers[family],
            "prompt_text": prompt_text,
            "prompt_full": prompt_full,
            "response_text": response_text,
            "word_count": word_count,
            "preferred_solution": r["preferred_solution"],
            "ethical_preference_type": r["ethical_preference_type"],
            "response_genre": r["response_genre"],
            "deictic_uptake_quality": r["deictic_uptake_quality"],
            "language_stability": r["language_stability"],
            "primary_agent": infer_primary_agent(r["framing_type"], response_text),
            "moral_reasoning_type": infer_moral_reasoning_type(r["ethical_preference_type"], r["framing_type"], r["preferred_solution"]),
            "voice_authority": infer_voice_authority(r["response_genre"], bool(r["contains_followup_question"]), False, r["preferred_solution"], r["framing_type"]),
            "affective_stance": infer_affective_stance(r["ethical_preference_type"], r["response_genre"], r["framing_type"], bool(r["contains_followup_question"]), r["preferred_solution"]),
            "indexical_coherence_score": indexical_score,
            "indexical_coherence_notes": indexical_notes,
            "contains_framework_labels": bool(r["contains_framework_labels"]),
            "contains_followup_question": bool(r["contains_followup_question"]),
            "contains_direct_imperative": count_regex(YORUBA_OBLIGATION, response_text) > 0,
            "contains_role_exit": False,
            "contains_translation_behavior": bool(r.get("contains_translation_behavior", False)),
            "framework_count_estimate": framework_count,
            "pluralism_two_plus": framework_count >= 2,
        }
        row.update(metrics)
        row["pronouns_per_100_words"] = normalize_per_100(
            row["first_person_count"] + row["first_person_plural_count"] + row["second_person_count"] + row["third_person_count"],
            word_count,
        )
        row["obligation_density_per_100_words"] = normalize_per_100(row["obligation_marker_count"], word_count)
        row["advisory_density_per_100_words"] = normalize_per_100(row["advisory_formula_count"], word_count)
        row["hedge_density_per_100_words"] = normalize_per_100(row["hedge_marker_count"], word_count)
        row["emphatic_ratio"] = float(r.get("emphatic_ratio", 0.0) or 0.0)
        rows.append(row)
    return pd.DataFrame(rows)


def write_outputs(english_df: pd.DataFrame, yoruba_df: pd.DataFrame) -> None:
    combined = pd.concat([english_df, yoruba_df], ignore_index=True)
    english_path = OUT_DIR / "english_openai_anthropic_comparable.csv"
    yoruba_path = OUT_DIR / "yoruba_openai_anthropic_comparable.csv"
    combined_path = OUT_DIR / "english_yoruba_openai_anthropic_comparable.csv"
    english_df.to_csv(english_path, index=False, encoding="utf-8")
    yoruba_df.to_csv(yoruba_path, index=False, encoding="utf-8")
    combined.to_csv(combined_path, index=False, encoding="utf-8")

    combined_json_path = OUT_DIR / "english_yoruba_openai_anthropic_comparable.json"
    with open(combined_json_path, "w", encoding="utf-8") as f:
        json.dump(combined.to_dict(orient="records"), f, ensure_ascii=False, indent=2)


def write_schema_note() -> None:
    note = OUT_DIR / "comparable_dataset_schema.md"
    content = """# Comparable Dataset Schema

This file documents the second-stage comparable datasets created for English and Yoruba OpenAI/Anthropic analysis.

## Files

- `english_openai_anthropic_comparable.csv`
- `yoruba_openai_anthropic_comparable.csv`
- `english_yoruba_openai_anthropic_comparable.csv`
- `english_yoruba_openai_anthropic_comparable.json`

## Core comparison fields

- `language`
- `provider_family`
- `model_label`
- `raw_model_name`
- `dilemma_id`
- `framing_type`
- `prompt_text`
- `prompt_full`
- `preferred_solution`
- `ethical_preference_type`
- `response_genre`
- `deictic_uptake_quality`
- `language_stability`

## Added discourse-comparison fields

- `primary_agent`
- `moral_reasoning_type`
- `voice_authority`
- `affective_stance`
- `indexical_coherence_score`
- `indexical_coherence_notes`

## Marker-count fields

- `first_person_count`
- `first_person_emphatic_count`
- `first_person_plural_count`
- `second_person_count`
- `third_person_count`
- `temporal_marker_count`
- `spatial_marker_count`
- `demonstrative_count`
- `obligation_marker_count`
- `advisory_formula_count`
- `hedge_marker_count`
- `universalist_marker_count`

## Density fields

- `pronouns_per_100_words`
- `obligation_density_per_100_words`
- `advisory_density_per_100_words`
- `hedge_density_per_100_words`

## Notes

- English `first_person_emphatic_count` is set to `0` because English lacks a direct morphological equivalent to Yoruba `emi`.
- Yoruba `language_stability` is meaningful; English uses `not_applicable`.
- `voice_authority`, `affective_stance`, and `primary_agent` are second-stage heuristic fields intended for comparability, not as replacements for close reading.
"""
    with open(note, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    english_df = build_english_dataset()
    yoruba_df = build_yoruba_dataset()
    write_outputs(english_df, yoruba_df)
    write_schema_note()
    print("Wrote comparable English and Yoruba datasets to", OUT_DIR)
    print("English rows:", len(english_df))
    print("Yoruba rows:", len(yoruba_df))


if __name__ == "__main__":
    main()
