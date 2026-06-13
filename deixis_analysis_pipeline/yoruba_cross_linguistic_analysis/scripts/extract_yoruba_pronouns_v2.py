#!/usr/bin/env python3
"""
Extract and count Yoruba pronouns from raw response data.
Focus on first person distinctions (mo vs emi vs mi) and their contexts.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac

YORUBA_PRONOUNS = {
    "first_singular": {
        "mo": r"\bmo\b",
        # Legacy combined bucket (emphatic + life); prefer emi_emphatic / emi_life below.
        "emi": r"\bemi\b|\bèmi\b|\bémí\b|\bèmí\b",
        "emi_life": r"\b[ẹẸ][̀\u0300]?m[íi]\b|\bẹ̀mí\b|\bẹ̀mi\b|\bẹ́mí\b",
        "emi_emphatic": r"\b(?:èmi|èmí|emi|émí)\b",
        "mi": r"\bmi\b",
        "ti_emi": r"\bti emi\b|\bti èmi\b",
    },
    "first_plural": {
        "a": r"\ba\b",
        "awa": r"\bawa\b|\bàwa\b",
    },
    "second_person": {
        "o": r"\bo\b|\bọ\b",
        "iwo": r"\biwo\b|\bìwọ\b|\bíwọ\b",
        "e": r"\be\b|\bẹ\b",
    },
    "third_person": {
        "o_3rd": r"\bó\b",
        "won": r"\bwọn\b|\bwọ́n\b",
        "oun": r"\boun\b|\bòun\b",
    },
}


def extract_pronoun_contexts(text: str, pronoun_pattern: str, window: int = 50) -> List[str]:
    contexts = []
    for match in re.finditer(pronoun_pattern, text, re.IGNORECASE):
        start = max(0, match.start() - window)
        end = min(len(text), match.end() + window)
        contexts.append(text[start:end].strip())
    return contexts


def classify_emi_token(token: str) -> str:
    """Return 'life' (ẹ̀mí = life/spirit) or 'emphatic' (èmi = I myself)."""
    if any(ch in token for ch in "ẹẸ"):
        return "life"
    return "emphatic"


def count_emi_disambiguated(text: str) -> Dict[str, int]:
    """Count èmi (emphatic I) separately from ẹ̀mí (life/spirit)."""
    combined = re.compile(
        r"\b(?:ẹ̀mí|ẹ̀mi|ẹ́mí|[ẹẸ][̀\u0300]?m[íi]|èmi|èmí|emi|émí)\b",
        re.IGNORECASE | re.UNICODE,
    )
    counts = {"emi_life": 0, "emi_emphatic": 0, "emi_combined": 0}
    for match in combined.finditer(text):
        counts["emi_combined"] += 1
        kind = classify_emi_token(match.group(0))
        counts[f"emi_{kind}"] += 1
    return counts


def count_pronouns(text: str) -> Dict[str, Dict[str, int]]:
    counts = defaultdict(lambda: defaultdict(int))
    emi_split = count_emi_disambiguated(text)
    if emi_split["emi_life"]:
        counts["first_singular"]["emi_life"] = emi_split["emi_life"]
    if emi_split["emi_emphatic"]:
        counts["first_singular"]["emi_emphatic"] = emi_split["emi_emphatic"]
    if emi_split["emi_combined"]:
        counts["first_singular"]["emi"] = emi_split["emi_combined"]

    for category, patterns in YORUBA_PRONOUNS.items():
        for pronoun_name, pattern in patterns.items():
            if pronoun_name in {"emi", "emi_life", "emi_emphatic"}:
                continue
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                counts[category][pronoun_name] = matches
    return dict(counts)


def calculate_emphatic_ratio(counts: Dict[str, Dict[str, int]], corrected: bool = True) -> float:
    regular = counts.get("first_singular", {}).get("mo", 0)
    if corrected:
        emphatic = counts.get("first_singular", {}).get("emi_emphatic", 0)
        if emphatic == 0 and "emi" in counts.get("first_singular", {}):
            emphatic = counts.get("first_singular", {}).get("emi", 0)
    else:
        emphatic = counts.get("first_singular", {}).get("emi", 0)
    if regular + emphatic == 0:
        return 0.0
    return emphatic / (regular + emphatic)


def calculate_emphatic_ratio_raw(counts: Dict[str, Dict[str, int]]) -> float:
    return calculate_emphatic_ratio(counts, corrected=False)


def analyze_response_file(file_path: Path) -> Dict:
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        print(f"Error loading {file_path}: {exc}")
        return None

    dilemma_id, responses = ac.iter_response_entries(data, file_path)
    results = {"dilemma_id": dilemma_id, "responses": {}}

    for framing, response_data in responses.items():
        response_text = response_data.get("response", "")
        if not response_text:
            continue

        pronoun_counts = count_pronouns(response_text)
        mo_contexts = extract_pronoun_contexts(response_text, YORUBA_PRONOUNS["first_singular"]["mo"])
        emi_contexts = extract_pronoun_contexts(response_text, YORUBA_PRONOUNS["first_singular"]["emi"])
        mi_contexts = extract_pronoun_contexts(response_text, YORUBA_PRONOUNS["first_singular"]["mi"])
        word_count = len(response_text.split())
        emphatic_ratio = calculate_emphatic_ratio(pronoun_counts)
        emphatic_ratio_raw = calculate_emphatic_ratio_raw(pronoun_counts)

        results["responses"][framing] = {
            "pronoun_counts": pronoun_counts,
            "word_count": word_count,
            "emphatic_ratio": emphatic_ratio,
            "emphatic_ratio_raw": emphatic_ratio_raw,
            "total_pronouns": sum(sum(cat.values()) for cat in pronoun_counts.values()),
            "mo_contexts": mo_contexts[:3],
            "emi_contexts": emi_contexts[:3],
            "mi_contexts": mi_contexts[:3],
            "response_length": len(response_text),
            "response_text": response_text[:500],
        }

    return results


def process_session_directory(session_dir: Path, model: str) -> List[Dict]:
    results = []
    response_files = [
        f
        for f in session_dir.glob("*_responses.json")
        if not f.name.startswith(("session", "summary"))
    ]
    print(f"  Found {len(response_files)} response files")

    for file_path in response_files:
        analysis = analyze_response_file(file_path)
        if analysis:
            analysis["model"] = model
            analysis["session"] = session_dir.name
            results.append(analysis)
    return results


def main():
    ac.DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_results = []

    for model in ac.MODELS:
        session_path = ac.PRONOUN_SESSIONS[model]
        if not session_path.exists():
            print(f"Missing session for {model}: {session_path}")
            continue
        print(f"Processing session: {session_path.name} ({model})")
        results = process_session_directory(session_path, model)
        all_results.extend(results)
        print(f"  Processed {len(results)} dilemmas")

    if not all_results:
        print("No results found!")
        return None

    structured_data = []
    for result in all_results:
        model = result["model"]
        dilemma = result["dilemma_id"]
        for framing, data in result["responses"].items():
            row = {
                "model": model,
                "dilemma_id": dilemma,
                "framing_type": framing,
                "word_count": data["word_count"],
                "response_length": data["response_length"],
                "total_pronouns": data["total_pronouns"],
                "emphatic_ratio": data["emphatic_ratio"],
                "emphatic_ratio_raw": data.get("emphatic_ratio_raw", data["emphatic_ratio"]),
                "pronouns_per_100_words": (
                    data["total_pronouns"] / data["word_count"] * 100 if data["word_count"] > 0 else 0
                ),
            }
            for category, counts in data["pronoun_counts"].items():
                for pronoun, count in counts.items():
                    row[f"{category}_{pronoun}"] = count
                    row[f"{category}_{pronoun}_per_100w"] = (
                        count / data["word_count"] * 100 if data["word_count"] > 0 else 0
                    )
            structured_data.append(row)

    df = pd.DataFrame(structured_data)
    df.to_csv(ac.DATA_DIR / "yoruba_pronoun_analysis.csv", index=False, encoding="utf-8")

    with open(ac.DATA_DIR / "yoruba_pronoun_detailed.json", "w", encoding="utf-8") as handle:
        json.dump(all_results, handle, ensure_ascii=False, indent=2)

    print(f"\nTotal responses analyzed: {len(structured_data)}")
    if len(structured_data) > 0:
        print("\nEmphatic ratio summary:")
        print(df.groupby("model")["emphatic_ratio"].agg(["mean", "std", "min", "max"]))

        print("\nMi usage per 100 words (object/reflexive 'me/my'):")
        if "first_singular_mi_per_100w" in df.columns:
            print(df.groupby("model")["first_singular_mi_per_100w"].agg(["mean", "std", "sum"]))

        print("\nMo vs Emi per 100 words:")
        for col in ["first_singular_mo_per_100w", "first_singular_emi_per_100w"]:
            if col in df.columns:
                print(f"\n{col}:")
                print(df.groupby("model")[col].agg(["mean", "std", "sum"]))

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()
