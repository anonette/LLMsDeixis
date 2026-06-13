#!/usr/bin/env python3
"""Translate a Yoruba generation session into a bilingual dataset."""

from __future__ import annotations

import argparse
import asyncio
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, Any, List

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from llm_client import UnifiedLLMClient

from session_utils import (
    infer_model_from_session_data,
    iterate_response_records,
    load_json,
    load_prompt_lookup,
    write_json,
)


TRANSLATION_PROMPT_TEMPLATE = """Translate the following Yoruba ethical response into smooth academic English.

Requirements:
1. Preserve the original ethical reasoning and argument structure.
2. Preserve deictic stance, including first-person, second-person, collective, spatial, temporal, reflexive, or cosmological orientation.
3. Preserve the level of certainty, hedging, and advisory tone.
4. Do not add new arguments or remove important nuances.
5. Write in readable academic English, not literal gloss English.

Yoruba prompt context:
{prompt_yo}

Yoruba response:
{response_yo}
"""


async def translate_text(client: UnifiedLLMClient, prompt_yo: str, response_yo: str, temperature: float) -> str:
    prompt = TRANSLATION_PROMPT_TEMPLATE.format(prompt_yo=prompt_yo, response_yo=response_yo)
    return await client.generate_completion(prompt, temperature=temperature, max_tokens=2500)


async def process_session(
    session_dir: Path,
    prompt_inventory_path: Path,
    output_dir: Path,
    translation_model: str,
    translation_temperature: float,
) -> Path:
    prompt_lookup = load_prompt_lookup(prompt_inventory_path)
    client = UnifiedLLMClient(translation_model)

    session_meta_path = session_dir / "complete_session_data.json"
    session_meta = load_json(session_meta_path) if session_meta_path.exists() else {}

    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    inferred_model = None
    translated_count = 0

    for record in iterate_response_records(session_dir):
        inferred_model = inferred_model or record["model"]
        details = prompt_lookup[(record["dilemma_id"], record["framing_type"])]
        response_en = await translate_text(
            client,
            details["question"],
            record["response"],
            translation_temperature,
        )
        grouped[record["dilemma_id"]].append(
            {
                "framing_type": record["framing_type"],
                "prompt_yo": details["question"],
                "prompt_en_reference": details.get("question_en_reference", ""),
                "response_yo": record["response"],
                "response_en_academic": response_en,
                "analysis_text": response_en,
                "model": record["model"],
                "audit_notes": details.get("audit_notes", ""),
                "normalization_notes": details.get("normalization_notes", ""),
                "raw_generation_payload": record["raw_payload"],
            }
        )
        translated_count += 1

    final_model = inferred_model or infer_model_from_session_data(session_dir, session_meta.get("generation_session", {}))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = output_dir / f"{session_dir.name}_bilingual_{timestamp}"
    target_dir.mkdir(parents=True, exist_ok=True)

    for dilemma_id, records in grouped.items():
        payload = {
            "dilemma_id": dilemma_id,
            "model": final_model,
            "source_session": session_dir.name,
            "translation_model": translation_model,
            "translation_temperature": translation_temperature,
            "responses": {entry["framing_type"]: entry for entry in records},
        }
        write_json(target_dir / f"{dilemma_id}_bilingual.json", payload)

    summary = {
        "source_session": session_dir.name,
        "source_model": final_model,
        "translation_model": translation_model,
        "translation_temperature": translation_temperature,
        "translated_responses": translated_count,
        "prompt_inventory": str(prompt_inventory_path),
        "generated_at": datetime.now().isoformat(),
    }
    write_json(target_dir / "bilingual_summary.json", summary)
    return target_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate a Yoruba generation session into a bilingual dataset")
    parser.add_argument("session_dir", help="Path to a Yoruba generation session directory")
    parser.add_argument(
        "--prompt-inventory",
        default=str(Path(__file__).resolve().parent.parent / "input_questions" / "all_dilemmas_deictic_questions_yoruba.json"),
        help="Path to the canonical Yoruba prompt inventory",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "outputs" / "bilingual_sessions"),
        help="Directory where bilingual session outputs should be written",
    )
    parser.add_argument(
        "--translation-model",
        default="gpt-4o",
        help="Model to use for academic English translation",
    )
    parser.add_argument(
        "--translation-temperature",
        type=float,
        default=0.2,
        help="Temperature for translation generation",
    )
    args = parser.parse_args()

    target_dir = asyncio.run(
        process_session(
            Path(args.session_dir),
            Path(args.prompt_inventory),
            Path(args.output_dir),
            args.translation_model,
            args.translation_temperature,
        )
    )
    print(f"[DONE] Bilingual session written to {target_dir}")


if __name__ == "__main__":
    main()
