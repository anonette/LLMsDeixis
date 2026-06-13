#!/usr/bin/env python3
"""Code published English baseline responses into a schema aligned with the open Yoruba coding."""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from llm_client import UnifiedLLMClient
from session_utils import write_json


PROMPT = """You are a research coding assistant.

Code ONE English ethical response using a schema aligned to the open Yoruba coding layer.

Return ONLY a valid JSON object with these exact fields:
{{
  "preferred_solution": "supports_A" or "supports_B" or "conditional_or_mixed" or "refuses_to_commit" or "uncodable",
  "preferred_solution_description": "short plain-English description of the action preferred, or none",
  "ethical_preference_type": "utilitarian" or "deontological" or "virtue_ethics" or "care_ethics" or "rights_based" or "procedural_caution" or "mixed" or "unclear",
  "response_genre": "direct_verdict" or "balanced_framework_exposition" or "procedural_advice" or "translation_or_gloss" or "meta_commentary" or "mixed",
  "deictic_uptake_quality": "strong_uptake" or "partial_uptake" or "weak_uptake",
  "contains_framework_labels": true or false,
  "contains_followup_question": true or false,
  "contains_direct_imperative": true or false,
  "contains_role_exit": true or false,
  "evidence_span_en": "1-3 sentences from the English response supporting your coding",
  "coding_rationale": "2-4 sentence explanation of why you assigned the labels",
  "confidence": 0.0
}}

Rules:
1. If the response clearly recommends a concrete action, do not label it refuses_to_commit.
2. If it lays out multiple frameworks and lightly leans, use conditional_or_mixed.
3. If it stays analytical and avoids endorsement, use refuses_to_commit.
4. For trolley-like dilemmas, supports_A means divert/intervene; supports_B means do not divert/do not intervene.

Context:
- model: {model}
- dilemma_id: {dilemma_id}
- framing_type: {framing_type}
- prompt: {prompt_en}

English response:
{response_en}
"""


@dataclass
class EnglishCodingRecord:
    record_id: int
    model: str
    model_label: str
    dilemma_id: str
    framing_type: str
    preferred_solution: str
    preferred_solution_description: str
    ethical_preference_type: str
    response_genre: str
    deictic_uptake_quality: str
    contains_framework_labels: bool
    contains_followup_question: bool
    contains_direct_imperative: bool
    contains_role_exit: bool
    evidence_span_en: str
    coding_rationale: str
    confidence: float


def model_label(model: str) -> str:
    lowered = model.lower()
    if "deepseek" in lowered:
        return "DeepSeek"
    if "claude" in lowered:
        return "Claude"
    return "GPT-4o"


def parse_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    return json.loads(text)


def iter_paired_records(comparison_dirs: List[Path]) -> Iterable[Dict[str, Any]]:
    seen: set[Tuple[str, str, str]] = set()
    for directory in comparison_dirs:
        payload = json.load(open(directory / "paired_comparison.json", encoding="utf-8"))
        for row in payload["paired_records"]:
            key = (row["model"], row["dilemma_id"], row["framing_type"])
            if key in seen:
                continue
            seen.add(key)
            yield {
                "model": row["model"],
                "dilemma_id": row["dilemma_id"],
                "framing_type": row["framing_type"],
                "prompt_en": row.get("prompt_en_reference", ""),
                "response_en": row["baseline_response_en"],
            }


async def code_record(client: UnifiedLLMClient, rec: Dict[str, Any], record_id: int) -> EnglishCodingRecord:
    prompt = PROMPT.format(
        model=rec["model"],
        dilemma_id=rec["dilemma_id"],
        framing_type=rec["framing_type"],
        prompt_en=rec["prompt_en"],
        response_en=rec["response_en"],
    )
    raw = await client.generate_completion(prompt, temperature=0.1, max_tokens=1600)
    data = parse_json(raw)
    return EnglishCodingRecord(
        record_id=record_id,
        model=rec["model"],
        model_label=model_label(rec["model"]),
        dilemma_id=rec["dilemma_id"],
        framing_type=rec["framing_type"],
        preferred_solution=data["preferred_solution"],
        preferred_solution_description=data["preferred_solution_description"],
        ethical_preference_type=data["ethical_preference_type"],
        response_genre=data["response_genre"],
        deictic_uptake_quality=data["deictic_uptake_quality"],
        contains_framework_labels=bool(data["contains_framework_labels"]),
        contains_followup_question=bool(data["contains_followup_question"]),
        contains_direct_imperative=bool(data["contains_direct_imperative"]),
        contains_role_exit=bool(data["contains_role_exit"]),
        evidence_span_en=data["evidence_span_en"],
        coding_rationale=data["coding_rationale"],
        confidence=float(data["confidence"]),
    )


async def process(output_dir: Path, coding_model: str) -> Path:
    comparison_dirs = [
        Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\comparisons\yoruba_control_gpt4o_20260608_120259_bilingual_20260608_134926_vs_published_english_20260608_135541"),
        Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\comparisons\yoruba_control_claude_20260608_122738_bilingual_20260608_134631_vs_published_english_20260608_135541"),
        Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_deixis_module\outputs\comparisons\yoruba_control_deepseek_20260608_124633_bilingual_20260608_135525_vs_published_english_20260608_135541"),
    ]
    client = UnifiedLLMClient(coding_model)
    records = list(iter_paired_records(comparison_dirs))
    coded: List[EnglishCodingRecord] = []
    for idx, rec in enumerate(records, start=1):
        coded.append(await code_record(client, rec, idx))

    target = output_dir / f"english_open_comparison_coded_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    target.mkdir(parents=True, exist_ok=True)
    write_json(target / "coded_content.json", {"coded_records": [asdict(r) for r in coded], "generated_at": datetime.now().isoformat()})
    with open(target / "coded_content.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(coded[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(r) for r in coded)
    summary = {
        "records_coded": len(coded),
        "preferred_solution_distribution": dict(Counter(r.preferred_solution for r in coded)),
        "ethical_preference_distribution": dict(Counter(r.ethical_preference_type for r in coded)),
        "response_genre_distribution": dict(Counter(r.response_genre for r in coded)),
        "generated_at": datetime.now().isoformat(),
    }
    write_json(target / "coding_summary.json", summary)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Code published English baseline into a schema aligned with Yoruba coding")
    parser.add_argument("--coding-model", default="gpt-4o", choices=["gpt-4o", "claude-3.5-sonnet", "deepseek-chat"])
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parent / "outputs" / "english_coded_content"))
    args = parser.parse_args()
    target = asyncio.run(process(Path(args.output_dir), args.coding_model))
    print(f"[DONE] English aligned coding written to {target}")


if __name__ == "__main__":
    main()
