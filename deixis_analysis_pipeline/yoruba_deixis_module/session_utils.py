"""Utilities for Yoruba module session loading and normalization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Iterable, List, Tuple


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_prompt_lookup(prompt_inventory_path: Path) -> Dict[Tuple[str, str], Dict[str, Any]]:
    data = load_json(prompt_inventory_path)
    lookup: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for dilemma in data["dilemmas"]:
        dilemma_id = dilemma["dilemma_id"]
        for framing, details in dilemma["deictic_questions"].items():
            lookup[(dilemma_id, framing)] = details
    return lookup


def list_response_files(session_dir: Path) -> List[Path]:
    return sorted(session_dir.glob("*_responses.json"))


def infer_model_from_session_data(session_dir: Path, session_data: Dict[str, Any]) -> str:
    if session_data.get("model"):
        return session_data["model"]
    session_name = session_dir.name.lower()
    if "deepseek" in session_name:
        return "deepseek/deepseek-chat"
    if "claude" in session_name:
        return "anthropic/claude-3.5-sonnet"
    return "gpt-4o"


def normalize_response_file(file_path: Path) -> Dict[str, Any]:
    data = load_json(file_path)
    if "responses" in data:
        responses = data["responses"]
        return {
            "dilemma_id": data.get("dilemma_id", file_path.stem.replace("_responses", "")),
            "dilemma_title": data.get("dilemma_title", file_path.stem.replace("_responses", "")),
            "dilemma_description": data.get("dilemma_description", ""),
            "model": data.get("model"),
            "responses": responses,
        }

    return {
        "dilemma_id": file_path.stem.replace("_responses", ""),
        "dilemma_title": file_path.stem.replace("_responses", ""),
        "dilemma_description": "",
        "model": None,
        "responses": data,
    }


def iterate_response_records(session_dir: Path) -> Iterable[Dict[str, Any]]:
    for file_path in list_response_files(session_dir):
        normalized = normalize_response_file(file_path)
        dilemma_id = normalized["dilemma_id"]
        dilemma_title = normalized["dilemma_title"]
        dilemma_description = normalized["dilemma_description"]
        model = normalized["model"]
        for framing, payload in normalized["responses"].items():
            response_text = payload.get("response")
            if not response_text:
                continue
            yield {
                "source_file": str(file_path),
                "dilemma_id": dilemma_id,
                "dilemma_title": dilemma_title,
                "dilemma_description": dilemma_description,
                "framing_type": framing,
                "model": model,
                "question": payload.get("deictic_question", payload.get("question", "")),
                "response": response_text,
                "raw_payload": payload,
            }


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
