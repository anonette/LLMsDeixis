"""Inspect whether the 9 deictic framings actually produce deictic-uptake variation
in model responses, using the cleaned GPT-4o session.

This is an empirical check on the central manipulation:
- does the impersonal framing yield third-person responses?
- does the first_person framing yield 'mo'/'mi' responses?
- does the reflexive yield 'ara mi' / introspective constructions?
- does the dialogic yield direct address back to the asker?
- does the cosmological reach for àgbáyé / supra-personal vantage?
"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Pronoun/marker buckets in Yoruba
MARKERS = {
    "1st_sg_subj": [r"\bMo\b", r"\bmo\b", r"\bÈmi\b", r"\bèmi\b"],
    "1st_sg_obj":  [r"\bmi\b", r"\bmí\b"],
    "1st_pl_subj": [r"\bA\b", r"\bAwa\b", r"\bÀwa\b"],
    "1st_pl_obj":  [r"\bwa\b", r"\bwá\b"],
    "2nd_subj":    [r"\bÌwọ\b", r"\bIwo\b"],
    "2nd_obj":     [r"\brẹ\b", r"\bọ\b\s"],
    "3rd_subj":    [r"\bÒun\b", r"\bòun\b", r"\bẸni\b", r"\bẹni\b", r"\bòṣìṣẹ́\b"],
    "reflexive":   [r"ara mi", r"ara rẹ", r"ara wa", r"fúnra rẹ̀", r"fúnra mi"],
    "spatial_here":[r"\bníbí\b", r"\bipò yìí\b", r"\bibi yìí\b", r"láti ibí"],
    "spatial_there":[r"\bníbẹ̀\b", r"\bibẹ̀\b", r"níta"],
    "temporal_now":[r"\bbáyìí\b", r"\bnísinsin\b", r"\bní àkókò\b", r"\blónìí\b"],
    "cosmological":[r"\bàgbáyé\b", r"\bgbogbo\b.{0,30}\bìgbésí\b", r"ẹ̀mí gbogbo"],
    "ipinnu":      [r"\bÌpinnu\b", r"\bìpinnu\b"],
    "idi":         [r"\bÌdí\b", r"\bìdí\b"],
}


def count_markers(text: str) -> dict:
    out = {}
    for k, patterns in MARKERS.items():
        total = 0
        for p in patterns:
            total += len(re.findall(p, text))
        out[k] = total
    return out


def summarize_framing(session_dir: Path, framing: str) -> dict:
    """Pool marker counts across all 6 dilemmas for this framing."""
    pooled = {k: 0 for k in MARKERS}
    chars = 0
    for response_file in sorted(session_dir.glob("*_responses.json")):
        data = json.loads(response_file.read_text(encoding="utf-8"))
        responses = data.get("responses", data)
        if framing in responses:
            text = responses[framing].get("response") or ""
            counts = count_markers(text)
            for k, v in counts.items():
                pooled[k] += v
            chars += len(text)
    # normalize per 1000 chars for fair cross-framing comparison
    if chars > 0:
        return {k: round(v * 1000 / chars, 2) for k, v in pooled.items()}, chars
    return pooled, 0


def main():
    session = Path(__file__).resolve().parent.parent / "generation_logs" / "yoruba_gpt4o_20260528_194240_cleaned_20260529_102820"
    if not session.exists():
        print(f"Session not found: {session}")
        return 1

    framings = ["impersonal", "second_person", "first_person", "first_person_plural",
                "reflexive", "dialogic", "spatial", "temporal", "cosmological"]

    print(f"Session: {session.name}")
    print("Per-framing marker rate (occurrences per 1000 chars across 6 dilemmas)")
    print()
    print(f"{'framing':<22}", end="")
    cols = ["1st_sg_subj", "1st_pl_subj", "2nd_subj", "reflexive",
            "spatial_here", "temporal_now", "cosmological", "ipinnu", "idi"]
    for c in cols:
        print(f"{c:>14}", end="")
    print()

    for framing in framings:
        rates, chars = summarize_framing(session, framing)
        print(f"{framing:<22}", end="")
        for c in cols:
            print(f"{rates.get(c, 0):>14}", end="")
        print(f"  [{chars} chars]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
