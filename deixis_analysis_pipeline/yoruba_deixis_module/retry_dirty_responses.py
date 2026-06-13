"""Retry dirty Yoruba responses until they pass the validator.

Reads a generation session (DeepSeek flat schema or GPT-4o/Claude
nested schema), identifies responses that fail the language-purity
validator, and regenerates them via the configured LLM provider
until either they pass or max_attempts is exhausted.

The cleaned session is saved as a new directory next to the original
with a `_cleaned` suffix.

Usage:
    python retry_dirty_responses.py <session_dir> \
        --provider deepseek \
        --model deepseek/deepseek-chat \
        --instruction-key deepseek-chat \
        --max-attempts 4 \
        --threshold 0.9
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

# add repo root for env_config + analyzer imports
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from env_config import load_project_env  # noqa: E402

load_project_env()

from deixis_ethical_analyzer import DeicticEthicalAnalyzer  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from yoruba_validator import score_response  # noqa: E402


def load_instruction(key: str | None, raw: str | None) -> str:
    if raw:
        return raw
    if key:
        cfg_path = Path(__file__).parent / "model_response_instructions.json"
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg["model_response_instructions"][key]
    return ""


def build_prompt(question: str, instruction: str) -> str:
    if not instruction:
        return question
    return f"{instruction.strip()}\n\nÌbéèrè / Question:\n{question}"


def build_stricter_prompt(question: str, instruction: str, prior_response: str) -> str:
    """For retry attempts, add a remediation header that points out the prior failure."""
    addendum = (
        "Ìdáhùn rẹ àkọ́kọ́ ní àwọn ọ̀rọ̀ Gẹ̀ẹ́sì tàbí àlàyé tí kò yẹ. "
        "Tún dáhùn ní Yorùbá mímọ́ péré, lo àkọsílẹ̀ 'Ìpinnu mi: ... Ìdí: ...' nìkan, "
        "kò sí Gẹ̀ẹ́sì, kò sí ìtumọ̀, kò sí ìbéèrè, dúró lẹ́yìn 'Ìdí'."
    )
    return f"{addendum}\n\n{instruction.strip()}\n\nÌbéèrè / Question:\n{question}"


def detect_schema(data: dict) -> Tuple[str, dict]:
    """Return (schema_type, responses_dict)."""
    if "responses" in data and isinstance(data["responses"], dict):
        return "nested", data["responses"]
    return "flat", data


def get_question(payload: dict) -> str:
    return payload.get("deictic_question") or payload.get("question") or ""


def make_analyzer(provider: str, model: str) -> DeicticEthicalAnalyzer:
    if provider == "openai":
        return DeicticEthicalAnalyzer(
            use_openai_direct=True,
            temperature=0.9,
            enable_rich_logging=False,
            models=[model],
        )
    elif provider == "anthropic":
        return DeicticEthicalAnalyzer(
            use_openai_direct=False,
            use_anthropic_direct=True,
            temperature=0.9,
            enable_rich_logging=False,
            models=[model],
        )
    elif provider == "deepseek" or provider == "openrouter":
        return DeicticEthicalAnalyzer(
            use_openai_direct=False,
            temperature=0.9,
            enable_rich_logging=False,
            models=[model],
        )
    raise ValueError(f"unknown provider: {provider}")


def _is_api_error_string(text: str) -> bool:
    if not text:
        return True
    head = text.strip()[:80]
    if head.startswith("Error:") and ("code" in head.lower() or "error code" in head.lower()):
        return True
    return False


async def retry_cell(
    analyzer: DeicticEthicalAnalyzer,
    question: str,
    instruction: str,
    prior_response: str,
    max_attempts: int,
    threshold: float,
) -> Tuple[str, float, int]:
    """Return (best_response, best_score, attempts_used)."""
    best_response = prior_response
    if _is_api_error_string(prior_response):
        # The prior 'response' is an API error string saved by an older bug.
        # Treat it as score 0 so any real response replaces it.
        best_score = 0.0
        best_response = ""
    else:
        best_score, _ = score_response(prior_response)

    for attempt in range(1, max_attempts + 1):
        if attempt == 1:
            prompt = build_prompt(question, instruction)
        else:
            prompt = build_stricter_prompt(question, instruction, best_response or prior_response)

        try:
            new_response = await analyzer.llm_agent.generate_ethical_response(prompt)
        except Exception as exc:  # noqa: BLE001
            print(f"    attempt {attempt} failed: {exc}")
            continue

        new_score, _ = score_response(new_response)
        print(f"    attempt {attempt}: score={new_score:.2f} ({len(new_response)} chars)")
        if new_score > best_score:
            best_response = new_response
            best_score = new_score
        if best_score >= threshold:
            return best_response, best_score, attempt
    return best_response, best_score, max_attempts


async def process_session(
    session_dir: Path,
    provider: str,
    model: str,
    instruction: str,
    max_attempts: int,
    threshold: float,
) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cleaned_dir = session_dir.parent / f"{session_dir.name}_cleaned_{timestamp}"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    analyzer = make_analyzer(provider, model)

    summary = {
        "source_session": session_dir.name,
        "provider": provider,
        "model": model,
        "max_attempts": max_attempts,
        "threshold": threshold,
        "instruction": instruction,
        "retried": [],
    }

    # Patterns that indicate the saved "response" is actually an API error
    # string (e.g. quota exhaustion, auth failure) rather than a real model output.
    API_ERROR_PREFIXES = (
        "Error: Error code:",
        "Error: 4",
        "Error: 5",
        "Error: ",
    )

    def looks_like_api_error(text: str) -> bool:
        if not text:
            return True
        head = text.strip()
        # any text that opens with our error-shim wrapper
        for p in API_ERROR_PREFIXES:
            if head.startswith(p):
                # Don't false-trigger on actual Yoruba content
                # The shim string is English and contains 'code' or 'error'.
                if "code" in head[:60].lower() or "error" in head[:60].lower():
                    return True
        return False

    for response_file in sorted(session_dir.glob("*_responses.json")):
        dilemma_id = response_file.stem.replace("_responses", "")
        with open(response_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        schema, responses = detect_schema(data)

        print(f"[{dilemma_id}] checking {len(responses)} framings...")
        for framing, payload in responses.items():
            if not isinstance(payload, dict):
                continue
            text = payload.get("response") or ""
            # Treat saved API error strings and empty responses as score 0.0
            if looks_like_api_error(text):
                score = 0.0
                print(f"  ✗ {framing} (API error string detected), regenerating...")
            else:
                score, _ = score_response(text)
                if score >= threshold:
                    continue
                print(f"  ✗ {framing} (score {score:.2f}), retrying...")
            question = get_question(payload)
            if not question:
                print("    no question text, skipping")
                continue
            new_text, new_score, attempts_used = await retry_cell(
                analyzer, question, instruction, text, max_attempts, threshold
            )
            payload["response"] = new_text
            payload["response_length"] = len(new_text)
            payload["retry_score"] = new_score
            payload["retry_attempts_used"] = attempts_used
            payload["retry_timestamp"] = datetime.now().isoformat()
            # If the original payload had an explicit "error" key, clear it now
            # that we have a real response.
            if "error" in payload and new_score > 0:
                payload["original_error"] = payload.pop("error")
            summary["retried"].append({
                "dilemma_id": dilemma_id,
                "framing": framing,
                "old_score": score,
                "new_score": new_score,
                "attempts": attempts_used,
                "improved": new_score > score,
                "now_clean": new_score >= threshold,
            })
            print(f"    -> final score {new_score:.2f}")

        # write back into the right schema
        out_path = cleaned_dir / response_file.name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    summary_path = cleaned_dir / "retry_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return cleaned_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Retry dirty Yoruba responses")
    parser.add_argument("session_dir", help="Path to source session directory")
    parser.add_argument("--provider", required=True, choices=["openai", "anthropic", "deepseek", "openrouter"],
                        help="LLM provider to use for retries")
    parser.add_argument("--model", required=True, help="Model id (e.g. gpt-4o, deepseek/deepseek-chat, claude-sonnet-4-20250514)")
    parser.add_argument("--instruction-key", default=None,
                        help="Key in model_response_instructions.json")
    parser.add_argument("--instruction", default=None,
                        help="Inline instruction (not recommended; prefer --instruction-key)")
    parser.add_argument("--max-attempts", type=int, default=4)
    parser.add_argument("--threshold", type=float, default=0.9)
    args = parser.parse_args()

    instruction = load_instruction(args.instruction_key, args.instruction)
    if not instruction:
        print("WARNING: no instruction supplied; retries will use bare prompts")

    out = asyncio.run(process_session(
        Path(args.session_dir),
        args.provider,
        args.model,
        instruction,
        args.max_attempts,
        args.threshold,
    ))
    print(f"\nCleaned session written to: {out}")


if __name__ == "__main__":
    main()
