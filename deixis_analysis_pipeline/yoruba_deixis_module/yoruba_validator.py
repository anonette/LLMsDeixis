"""Validator for Yoruba LLM responses.

Detects English contamination, meta-commentary about translation,
prompt restatement, and other failure modes that the strict
generation instruction is supposed to prevent.

Usage:
    from yoruba_validator import score_response, score_session

    score, issues = score_response(text)
    # score is 0.0 (worst) to 1.0 (clean)
    # issues is a list of detected problems
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Iterable

# Common Yoruba words that look like English when stripped of tone marks
# and underdots. These should NOT trigger the English-word detector.
YORUBA_NO_DIACRITICS = {
    w.lower()
    for w in [
        # decisions / reasoning
        "pinnu", "gbogbo", "irin", "rere", "dinku", "ohun", "kankan",
        "gbangba", "buburu", "eniyan", "ipinnu", "asiri", "aabo", "ajo",
        "ojo", "isin", "ija", "ifeso", "oro", "ori", "sile", "ekun",
        "peniyan", "iku", "kuro", "idi", "tabi", "sugbon", "lori", "nipa",
        "niwon", "ninu", "laarin", "enia", "awon", "oye", "itoju", "wipe",
        "dada", "riro", "gan", "okan", "nikan", "dipo", "aiye", "agbara",
        "jeyo", "meji", "dudu", "ipo", "meta", "pipa", "ami", "iyato",
        "mejeji", "siwaju", "larin", "ipari", "tooto", "idanwo", "fikun",
        "julo", "iwa", "iye", "tito", "seyin", "sinu", "keji", "gbon",
        "wonyi", "peye", "pataki", "ojuse", "alaye", "loni", "iwon",
        "ibukun", "rara", "die", "lasiko", "leeyan", "lehin",
        "wahala", "yoo", "yio", "yatto", "kale", "ase", "lana",
        "ile", "ise", "tite", "owo", "fero", "isan", "lere", "lebi",
        "ifise", "akoko", "agbo", "ikeji", "ikini",
        "bawo", "eyin", "eyi", "esin", "inu",
        # additions from claude false positives
        "apaniyan", "nira", "farapa", "gidi", "gbogbogbo",
        "nita", "ninu", "olori", "olu", "olukoni", "alaba",
        "isise", "ojise", "ologun", "olukoni",
        # common Yoruba verbs / connectives (no-diacritic forms)
        "lati", "lai", "loju", "lojo", "loko", "para", "fara", "yoo",
        "alaisan", "alala", "alagba", "aladun", "alaye", "ailera",
        "ailagbara", "agbofinro", "aifo", "aimo", "ahere", "ailera",
        "akole", "aladun", "alaisi", "alagbara", "alaye", "ailoye",
        "asese", "asayan", "asayin", "asiri", "aworan", "awari",
        "awon", "awujo", "awo", "ayipada", "ayika",
        "agbara", "agbofinro", "agbalagba", "agba", "agbede",
        "aifoya", "afe", "afikun", "afi", "afojusun",
        "didara", "didahun", "didoju", "didubule", "didoju",
        "dipo", "dake", "danu", "darapo", "dawole", "die",
        "duro", "duroja", "dahun", "dake", "darapo",
        "eda", "edi", "eko", "ekoo", "ekoo", "epa", "esin",
        "esi", "ewu", "ewe", "edidi", "edidi", "eko", "edidi",
        "fikun", "fife", "fifi", "fihan", "fa", "fagun", "fete",
        "gbadun", "gbado", "gbe", "gbede", "gbero", "gboju", "gbon",
        "gbera", "gbo", "gbiyanju", "gba", "gbangba", "gboju",
        "iba", "ibikan", "ibukun", "ibinu", "ibere", "ifa", "ifesi",
        "ife", "ifesi", "ifi", "ifowo", "ifowosi", "iga", "igba",
        "igbagbo", "igbe", "igbera", "igbeyawo", "ija", "ijoba",
        "ikan", "ike", "ila", "ile", "imo", "imusepo", "inu",
        "ipa", "ipade", "ipe", "ipinya", "ipo", "irin", "iro",
        "iroyin", "iru", "isalẹ", "isale", "ise", "iseju", "iso",
        "isokan", "isokuso", "itan", "iwa", "iwo", "iya",
        "iyale", "iye", "iyebiye", "iyemeji", "iyokuro",
        "ja", "jade", "jagun", "jeje", "ji", "jiro", "jo", "joko",
        "ka", "kalẹ", "kale", "kankan", "kanna", "kekere", "ki",
        "koja", "kole", "kookan", "korira", "kuru", "kuna",
        "la", "lai", "lailai", "lalo", "lehin", "lekan", "lese",
        "lewu", "lo", "loke", "lopo", "lori",
        "ma", "majemu", "mejeji", "mejeeji", "mejila", "merin",
        "mimo", "mo", "moye", "mura",
        "ni", "nibi", "nigba", "nigbati", "nigboro", "nile",
        "nipa", "nise", "ninu", "nisinsinyi", "niwaju", "nje",
        "njọ", "njo",
        "obi", "obirin", "oga", "ogbon", "oja", "ojo", "ojoojumo",
        "oju", "okan", "oko", "okun", "okunkun", "ola", "olokiki",
        "olola", "olu", "omo", "omode", "ono", "onibara", "onise",
        "opo", "opolopo", "ore", "oriki", "orisi", "oro", "oruko",
        "osan", "osun", "ota", "otito", "owo", "oya",
        "pada", "padana", "paju", "papa", "paju", "papo", "para",
        "patapata", "pataki", "pelu", "pelu", "pe", "pin", "pinya",
        "pipa", "pipaarẹ́", "pipade", "po", "pupo",
        "re", "ri", "ro", "roju", "ronu", "ruru",
        "sa", "sai", "salaye", "sayin", "se", "sehin", "sese",
        "si", "sile", "siwaju", "so", "soko", "sokun", "sora",
        "sotito", "sua", "sun", "sunmo",
        "ta", "tabi", "tako", "tan", "tani", "te", "tele", "tete",
        "ti", "tii", "tobi", "tooto", "tooto", "tutu", "tan",
        "ulu", "un", "uwa",
        "wa", "wahala", "wale", "waye", "we", "win", "wo",
        "yan", "yara", "yi", "yio", "yoo",
        # forms with Yoruba o, ọ, ẹ ASCII-normalized
        "ojowojo", "alaaye", "ojulowo", "olufun", "olufunni",
        "iseyo", "iseyokan", "papasepo", "tooto",
        # additions from gpt-4o false positives
        "abajade", "ilera", "miiran", "baibai", "dukia", "agbede",
        "ajose", "kaakiri", "aapon", "asoju", "alaapon", "alasiri",
        "alaibikita", "alailera", "afoyemora", "alaadun", "alaapon",
        "alabowo", "aladudu", "alagada", "aaye", "afi", "afojusun",
        "afojuri", "ajalu", "akiyesi", "akoba", "akorita", "alakikanju",
        "aniyan", "anu", "asayan", "asese", "asopo", "ayanmo",
        "ayidayida", "ayipada", "ayipada", "ayipo", "ayodele",
        "baisi", "balogun", "bawọn", "bere", "biotilejepe", "boya",
        "didara", "didoju", "dudu", "duro", "duroja",
        "ebi", "ebu", "edidi", "edun", "egbe", "eka", "elese",
        "eniyan", "eranko", "eroja", "esi", "eto", "etutu",
        "fagunle", "fahan", "fapamo", "fipa", "fokun", "fokutoye",
        "gegebi", "gigan", "gboranko", "gboroye",
        "ifapamo", "ifiyesi", "ifoya", "igbagbo", "igbaradi",
        "igbero", "igbeyawo", "ijiya", "ijo", "ijoko", "ijọba",
        "ikilo", "ikorira", "ilana", "imularada", "imura", "inure",
        "ipade", "ipalemo", "ipoluse", "iponni", "ipongbe",
        "iranlowo", "iranti", "iribi", "iroyin", "irufe", "iseju",
        "isokuso", "isokan", "iso", "isowo", "iwadi", "iwaju",
        "iwapele", "iwo", "iwoye", "iya", "iyale", "iyebiye",
        "jagunjagun", "jeyo", "joba",
        "kankan", "kasiri", "kekere", "ketala", "korira",
        "lailai", "lainireti", "lasiko", "lasiri", "latari",
        "lehin", "lenu", "lo", "lojo", "lori",
        "mejila", "merin", "mimu", "moya", "mura",
        "nibitomilọsí", "nikan", "nilo", "nipa", "niraye", "nireti",
        "obi", "ode", "ogbon", "okiki", "olokiki", "olola",
        "olori", "olu", "ominira", "omo", "omode",
        "onibara", "onisegun", "onise", "opin", "ori",
        "padana", "pataki", "patapata", "pelu", "pipa", "pitan",
        "padaa", "padasi", "papo", "para", "patapata",
        "ranlowo", "rorun", "roro",
        "sapejuwe", "sayo", "se", "sehin", "sile", "sinu",
        "sipo", "sisọ", "siwaju", "siwon", "siyensi", "sodá",
        "sokun", "sokuso", "sopo", "sora", "sori", "sose",
        "tani", "tasekato", "taye", "te", "ti", "tii", "titi",
        "tobi", "tooto", "tote", "tubo", "tutu",
        "ujon", "umol", "urara",
        "wahala", "wale", "wari", "we", "win", "wo", "woke",
        "yan", "yara", "yatosi", "yoo",
        # additional doublings spotted in GPT-4o
        "wonyii", "ojuse", "iseyo", "ifese", "ifeso",
        "tiwa", "agbara", "aabo",
    ]
}

# Acronyms and proper nouns that are acceptable
ACCEPTABLE_TOKENS = {"PTSD", "ICU", "AI", "DeepSeek"}

# Strong indicators of English-mode meta-commentary or translation drift.
ENGLISH_HINT_PHRASES = [
    "Trolley", "Problem", "utilitarian", "utilitarianism", "deontolog",
    "translation", "Note that", "breakdown", "interpret", "Ethical",
    "accident", "translate", "English translation", "Your dilemma",
    "Decision:", "Reasoning:", "My Decision", "Reasons:",
    "Do you want", "Do you agree", "Yorùbá Response", "Yoruba Response",
    "I have decided", "I will translate", "in English",
]

# Meta-phrases in Yoruba that indicate the model is talking about itself
# instead of answering the question.
YORUBA_META_PHRASES = [
    "ti a fún mi ní àṣẹ",  # "that I was instructed"
    "gẹ́gẹ́ bí àṣẹ",  # "as per the instruction"
    "tí a beere",  # "that was asked"
    "Ìdáhùn yìí kò ní Gẹ̀ẹ́sì",  # "this response has no English"
    "tí ó bá àṣẹ mu",  # "that follows the instruction"
]

# Decision-template anchor words that suggest the model followed the format
TEMPLATE_ANCHORS = ["Ìpinnu mi", "Ìpinnu rẹ", "Ìdí:", "Ìdí rẹ̀", "Ìdí nìyí"]


def find_english_words(text: str) -> List[str]:
    """Return ASCII-only words >= 4 chars that aren't on the Yoruba allowlist."""
    raw_words = re.findall(r"\b[A-Za-z]{4,}\b", text)
    leaks: List[str] = []
    for w in raw_words:
        if w in ACCEPTABLE_TOKENS:
            continue
        if w.lower() in YORUBA_NO_DIACRITICS:
            continue
        # heuristic: a word with no Yoruba-style diacritics in surrounding
        # context is most likely English
        leaks.append(w)
    return leaks


def find_phrase_hits(text: str, phrases: Iterable[str]) -> List[str]:
    return [p for p in phrases if p in text]


def score_response(text: str) -> Tuple[float, Dict[str, List[str]]]:
    """Return (cleanliness_score, issues_dict).

    Score is 1.0 if no issues detected, decreases as issues accumulate.
    """
    issues: Dict[str, List[str]] = {}

    english_words = find_english_words(text)
    if english_words:
        issues["english_words"] = english_words

    english_phrases = find_phrase_hits(text, ENGLISH_HINT_PHRASES)
    if english_phrases:
        issues["english_phrases"] = english_phrases

    meta_phrases = find_phrase_hits(text, YORUBA_META_PHRASES)
    if meta_phrases:
        issues["meta_commentary"] = meta_phrases

    # bonus signal: does the response use the decision template?
    has_template = any(anchor in text for anchor in TEMPLATE_ANCHORS)

    # very short responses (< 100 chars) are suspicious
    if len(text.strip()) < 80:
        issues["too_short"] = [f"{len(text)} chars"]

    # very long responses are also suspicious (DeepSeek rambling)
    if len(text) > 3500:
        issues["too_long"] = [f"{len(text)} chars"]

    # compute score
    penalty = 0.0
    penalty += 0.5 * (len(english_words) > 0)
    penalty += 0.3 * (len(english_phrases) > 0)
    penalty += 0.2 * (len(meta_phrases) > 0)
    penalty += 0.1 * ("too_short" in issues)
    penalty += 0.1 * ("too_long" in issues)
    # template-following gives a small bonus when no major issues
    if has_template and penalty <= 0.2:
        penalty *= 0.5

    score = max(0.0, 1.0 - penalty)
    return score, issues


def is_clean(text: str, threshold: float = 0.9) -> bool:
    score, _ = score_response(text)
    return score >= threshold


def score_session(session_dir: Path) -> Dict[str, Dict[str, Dict]]:
    """Score every framing/dilemma in a session directory.

    Returns a nested dict: {dilemma_id: {framing: {score, issues, response_preview}}}.
    Handles both the GPT-4o/Claude schema (nested under 'responses') and the
    DeepSeek schema (flat top level).
    """
    results: Dict[str, Dict[str, Dict]] = {}

    for response_file in sorted(session_dir.glob("*_responses.json")):
        dilemma_id = response_file.stem.replace("_responses", "")
        with open(response_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # detect schema
        if "responses" in data and isinstance(data["responses"], dict):
            responses = data["responses"]
        else:
            responses = data

        per_framing: Dict[str, Dict] = {}
        for framing, payload in responses.items():
            if not isinstance(payload, dict):
                continue
            text = payload.get("response") or ""
            if not text or "error" in payload:
                per_framing[framing] = {
                    "score": 0.0,
                    "issues": {"missing": ["no response text"]},
                    "preview": "",
                }
                continue
            score, issues = score_response(text)
            per_framing[framing] = {
                "score": score,
                "issues": issues,
                "preview": text[:160],
            }
        results[dilemma_id] = per_framing
    return results


def summarize(results: Dict[str, Dict[str, Dict]], threshold: float = 0.9) -> Dict:
    """Produce a compact summary of validation results."""
    total = 0
    clean = 0
    dirty_cells: List[Tuple[str, str, float, Dict]] = []
    for dilemma_id, per_framing in results.items():
        for framing, info in per_framing.items():
            total += 1
            if info["score"] >= threshold:
                clean += 1
            else:
                dirty_cells.append((dilemma_id, framing, info["score"], info["issues"]))
    return {
        "total": total,
        "clean": clean,
        "dirty": total - clean,
        "clean_pct": (100.0 * clean / total) if total else 0.0,
        "dirty_cells": dirty_cells,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Score Yoruba LLM responses for language purity")
    parser.add_argument("session_dir", help="Path to generation session directory")
    parser.add_argument("--threshold", type=float, default=0.9,
                        help="Cleanliness threshold (default 0.9)")
    parser.add_argument("--verbose", action="store_true",
                        help="Show issue detail for dirty cells")
    args = parser.parse_args()

    results = score_session(Path(args.session_dir))
    summary = summarize(results, threshold=args.threshold)

    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    print(f"Session: {args.session_dir}")
    print(f"Clean: {summary['clean']}/{summary['total']} ({summary['clean_pct']:.0f}%)")
    print(f"Dirty: {summary['dirty']}")
    print()
    if args.verbose and summary["dirty_cells"]:
        print("Dirty cells:")
        for dilemma, framing, score, issues in summary["dirty_cells"]:
            print(f"  {dilemma} / {framing} : score={score:.2f}")
            for kind, items in issues.items():
                print(f"    {kind}: {items[:6]}")


if __name__ == "__main__":
    main()
