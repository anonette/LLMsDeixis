"""
Generate ethical dilemma responses via remote Ollama (N-ATLaS / n-atlas).

Calls the Ollama HTTP API with tuned generation options (longer outputs, Yoruba
instruction layer) and writes session JSON matching generate_responses_multi_dilemma.py.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
PIPELINE_DIR = SCRIPT_DIR.parent
REPO_ROOT = PIPELINE_DIR.parent
DEFAULT_OLLAMA_HOST = "http://100.111.129.69:12434"
DEFAULT_MODEL = "n-atlas"

FRAMINGS = [
    "impersonal",
    "second_person",
    "first_person",
    "reflexive",
    "dialogic",
    "spatial",
    "temporal",
    "cosmological",
    "first_person_plural",
]


def build_generation_prompt(question: str, response_instruction: str = "") -> str:
    if not response_instruction:
        return question
    return f"{response_instruction.strip()}\n\nÌbéèrè / Question:\n{question}"


def load_all_dilemmas_questions(json_path: str) -> Dict[str, Any]:
    json_file = Path(json_path)
    if not json_file.exists():
        json_file = PIPELINE_DIR / "input_questions" / json_path
    if not json_file.exists():
        raise FileNotFoundError(f"{json_path} not found")
    with open(json_file, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_response_instruction(args: argparse.Namespace) -> str:
    if args.open_control:
        return ""
    if args.response_instruction_file:
        with open(args.response_instruction_file, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    if args.response_instruction_key:
        cfg_path = PIPELINE_DIR / "yoruba_deixis_module" / "model_response_instructions.json"
        with open(cfg_path, "r", encoding="utf-8") as handle:
            cfg = json.load(handle)
        return cfg["model_response_instructions"][args.response_instruction_key]
    return args.response_instruction


class OllamaClient:
    def __init__(
        self,
        host: str,
        model: str,
        temperature: float = 0.9,
        repeat_penalty: float = 1.12,
        num_ctx: int = 8192,
        num_predict: int = 1024,
        keep_alive: str = "30m",
        timeout: int = 600,
    ) -> None:
        self.base_url = host.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.repeat_penalty = repeat_penalty
        self.num_ctx = num_ctx
        self.num_predict = num_predict
        self.keep_alive = keep_alive
        self.timeout = timeout

    def generate(self, prompt: str) -> Tuple[str, Dict[str, Any]]:
        payload = {
            "model": self.model,
            "stream": False,
            "keep_alive": self.keep_alive,
            "messages": [{"role": "user", "content": prompt}],
            "options": {
                "temperature": self.temperature,
                "repeat_penalty": self.repeat_penalty,
                "num_ctx": self.num_ctx,
                "num_predict": self.num_predict,
            },
        }
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("message", {}).get("content", "")
        meta = {
            "eval_count": data.get("eval_count"),
            "prompt_eval_count": data.get("prompt_eval_count"),
            "total_duration_ms": round((data.get("total_duration") or 0) / 1e6, 1),
            "load_duration_ms": round((data.get("load_duration") or 0) / 1e6, 1),
            "num_predict": self.num_predict,
        }
        return text, meta


def generate_responses_for_dilemma(
    client: OllamaClient,
    dilemma_data: Dict[str, Any],
    output_dir: Path,
    response_instruction: str,
) -> Tuple[Dict[str, Any], int, int]:
    deictic_questions = dilemma_data["deictic_questions"]
    dilemma_responses: Dict[str, Any] = {
        "dilemma_id": dilemma_data["dilemma_id"],
        "dilemma_title": dilemma_data["dilemma_title"],
        "dilemma_description": dilemma_data["dilemma_description"],
        "timestamp": datetime.now().isoformat(),
        "model": client.model,
        "temperature": client.temperature,
        "responses": {},
    }
    if "ethical_dimensions" in dilemma_data:
        dilemma_responses["ethical_dimensions"] = dilemma_data["ethical_dimensions"]

    successful = 0
    failed = 0

    print(f"\n{'=' * 80}")
    print(f"DILEMMA: {dilemma_data['dilemma_title']}")
    print(f"ID: {dilemma_data['dilemma_id']}")
    print("=" * 80)

    for idx, framing_key in enumerate(FRAMINGS, 1):
        print(f"\n[{idx}/{len(FRAMINGS)}] {framing_key.upper()} framing...")
        if framing_key not in deictic_questions:
            print(f"  [X] No question found for {framing_key}")
            failed += 1
            continue

        question_data = deictic_questions[framing_key]
        deictic_question = question_data["question"]
        prompt_to_send = build_generation_prompt(deictic_question, response_instruction)
        print(f"  Question: {deictic_question[:100]}...")

        start_time = time.time()
        try:
            response, meta = client.generate(prompt_to_send)
            generation_time = time.time() - start_time
            dilemma_responses["responses"][framing_key] = {
                "deictic_question": deictic_question,
                "prompt_sent": prompt_to_send,
                "deictic_markers": question_data.get("deictic_markers", []),
                "framing_focus": question_data.get("focus", ""),
                "response": response,
                "generation_time_seconds": generation_time,
                "response_length": len(response),
                "generation_meta": meta,
                "timestamp": datetime.now().isoformat(),
            }
            successful += 1
            print(
                f"  [OK] Generated ({len(response)} chars, {generation_time:.2f}s, "
                f"{meta.get('eval_count', '?')} tokens)"
            )
        except Exception as exc:
            failed += 1
            print(f"  [ERROR] {exc}")
            dilemma_responses["responses"][framing_key] = {
                "deictic_question": deictic_question,
                "prompt_sent": prompt_to_send,
                "error": str(exc),
                "timestamp": datetime.now().isoformat(),
            }

    dilemma_file = output_dir / f"{dilemma_data['dilemma_id']}_responses.json"
    with open(dilemma_file, "w", encoding="utf-8") as handle:
        json.dump(dilemma_responses, handle, indent=2, ensure_ascii=False)

    print(f"\n[DONE] {dilemma_data['dilemma_title']}: {successful}/{len(FRAMINGS)} ok")
    print(f"  Saved to: {dilemma_file}")
    return dilemma_responses, successful, failed


def run_generation(
    json_path: str,
    output_prefix: str,
    response_instruction: str,
    dilemma_ids: Optional[List[str]],
    client: OllamaClient,
) -> Path:
    all_data = load_all_dilemmas_questions(json_path)
    dilemmas = all_data["dilemmas"]
    if dilemma_ids:
        dilemmas = [d for d in dilemmas if d["dilemma_id"] in dilemma_ids]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = PIPELINE_DIR / "generation_logs" / f"{output_prefix}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("N-ATLaS / OLLAMA RESPONSE GENERATION")
    print("=" * 60)
    print(f"  Ollama host: {client.base_url}")
    print(f"  Model: {client.model}")
    print(f"  Temperature: {client.temperature}")
    print(f"  num_predict: {client.num_predict}")
    print(f"  num_ctx: {client.num_ctx}")
    print(f"  Source: {json_path}")
    print(f"  Dilemmas: {len(dilemmas)}")
    print(f"  Output: {output_dir}")
    print("=" * 60)

    all_responses: List[Dict[str, Any]] = []
    total_successful = 0
    total_failed = 0

    for idx, dilemma in enumerate(dilemmas, 1):
        print(f"\n\n{'=' * 80}")
        print(f"PROCESSING DILEMMA {idx}/{len(dilemmas)}")
        print("=" * 80)
        responses, successful, failed = generate_responses_for_dilemma(
            client, dilemma, output_dir, response_instruction
        )
        all_responses.append(responses)
        total_successful += successful
        total_failed += failed

    attempted = len(dilemmas) * len(FRAMINGS)
    session_data = {
        "generation_session": {
            "timestamp": timestamp,
            "model": client.model,
            "backend": "ollama",
            "ollama_host": client.base_url,
            "temperature": client.temperature,
            "num_predict": client.num_predict,
            "num_ctx": client.num_ctx,
            "repeat_penalty": client.repeat_penalty,
            "total_dilemmas": len(dilemmas),
            "source_file": json_path,
            "response_instruction": response_instruction,
        },
        "dilemmas_processed": [d["dilemma_id"] for d in dilemmas],
        "all_responses": all_responses,
        "statistics": {
            "total_responses_attempted": attempted,
            "total_successful": total_successful,
            "total_failed": total_failed,
            "success_rate": total_successful / attempted if attempted else 0,
        },
    }
    session_file = output_dir / "complete_session_data.json"
    with open(session_file, "w", encoding="utf-8") as handle:
        json.dump(session_data, handle, indent=2, ensure_ascii=False)

    summary = {
        "session_info": {
            "timestamp": timestamp,
            "model": client.model,
            "backend": "ollama",
            "ollama_host": client.base_url,
            "temperature": client.temperature,
            "num_predict": client.num_predict,
            "output_directory": str(output_dir),
        },
        "statistics": {
            "total_dilemmas": len(dilemmas),
            "total_framings_per_dilemma": len(FRAMINGS),
            "total_responses_attempted": attempted,
            "successful_generations": total_successful,
            "failed_generations": total_failed,
            "success_rate_percentage": (total_successful / attempted * 100) if attempted else 0,
        },
        "research_design": {
            "deictic_framings": FRAMINGS,
            "response_instruction": response_instruction,
        },
    }
    summary_file = output_dir / "generation_summary.json"
    with open(summary_file, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(f"\n\nGENERATION COMPLETE")
    print("=" * 60)
    print(f"Successful: {total_successful}/{attempted}")
    print(f"Output directory: {output_dir}")
    return output_dir


def smoke_test(client: OllamaClient, json_path: str, response_instruction: str) -> None:
    data = load_all_dilemmas_questions(json_path)
    dilemma = next(d for d in data["dilemmas"] if d["dilemma_id"] == "trolley_problem")
    question = dilemma["deictic_questions"]["second_person"]["question"]
    prompt = build_generation_prompt(question, response_instruction)
    print("SMOKE TEST — trolley_problem / second_person")
    print(f"Host: {client.base_url}  Model: {client.model}")
    print(f"num_predict: {client.num_predict}")
    print("-" * 60)
    text, meta = client.generate(prompt)
    print("RESPONSE:\n")
    print(text)
    print("-" * 60)
    print(f"Length: {len(text)} chars | tokens: {meta.get('eval_count')} | time: {meta.get('total_duration_ms')} ms")


def main() -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Generate Yoruba dilemma responses via Ollama N-ATLaS")
    parser.add_argument("--json-path", default=str(PIPELINE_DIR / "input_questions" / "all_dilemmas_deictic_questions_yoruba.json"))
    parser.add_argument("--output-prefix", default="yoruba_natlas")
    parser.add_argument("--ollama-host", default=DEFAULT_OLLAMA_HOST)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--repeat-penalty", type=float, default=1.12)
    parser.add_argument("--num-ctx", type=int, default=8192)
    parser.add_argument("--num-predict", type=int, default=1024, help="Max new tokens (raise if answers truncate)")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--response-instruction", default="")
    parser.add_argument("--response-instruction-file", default=None)
    parser.add_argument("--response-instruction-key", default="n-atlas")
    parser.add_argument(
        "--open-control",
        action="store_true",
        help="Unrestricted Yoruba control: dilemma prompt only, no instruction layer",
    )
    parser.add_argument("--dilemmas", nargs="+", default=None, help="Specific dilemma IDs")
    parser.add_argument("--smoke-test", action="store_true", help="Run one full trolley second_person cell and exit")
    args = parser.parse_args()

    instruction = load_response_instruction(args)
    client = OllamaClient(
        host=args.ollama_host,
        model=args.model,
        temperature=args.temperature,
        repeat_penalty=args.repeat_penalty,
        num_ctx=args.num_ctx,
        num_predict=args.num_predict,
        timeout=args.timeout,
    )

    if args.smoke_test:
        smoke_test(client, args.json_path, instruction)
        return

    run_generation(
        json_path=args.json_path,
        output_prefix=args.output_prefix,
        response_instruction=instruction,
        dilemma_ids=args.dilemmas,
        client=client,
    )


if __name__ == "__main__":
    main()
