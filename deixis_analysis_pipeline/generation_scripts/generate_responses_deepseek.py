"""
Generate Responses for Multiple Dilemmas using DeepSeek via OpenRouter
Generate responses using the comprehensive deictic questions from all_dilemmas_deictic_questions.json
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from transformer import DeicticFraming


def build_generation_prompt(question: str, response_instruction: str = "") -> str:
    """Compose the final prompt sent to the model."""
    if not response_instruction:
        return question
    return f"{response_instruction.strip()}\n\nÌbéèrè / Question:\n{question}"

def load_all_dilemmas_questions(json_path="all_dilemmas_deictic_questions.json"):
    """Load all dilemmas with deictic questions from JSON."""
    json_file = Path(json_path)
    if not json_file.exists():
        # Try looking in the input_questions directory
        json_file = Path("../input_questions") / json_path
        if not json_file.exists():
            raise FileNotFoundError(f"{json_path} not found!")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        # Convert the structure to match expected format
        dilemmas_dict = {}
        for dilemma in data['dilemmas']:
            dilemma_id = dilemma['dilemma_id']
            # Extract just the questions from deictic_questions
            questions = {}
            for framing, details in dilemma['deictic_questions'].items():
                questions[framing] = details['question']
            dilemmas_dict[dilemma_id] = questions
        
        return dilemmas_dict

async def generate_responses_for_dilemma(analyzer, dilemma_name, deictic_questions, response_instruction=""):
    """Generate responses for a single dilemma across all deictic framings."""
    responses = {}
    success_count = 0
    
    for framing_name, question in deictic_questions.items():
        print(f"\n[{framing_name.upper()}] Generating response...")
        print(f"Question: {question[:100]}...")
        
        try:
            # Generate response using DeepSeek
            prompt_to_send = build_generation_prompt(question, response_instruction)
            response = await analyzer.llm_agent.generate_ethical_response(prompt_to_send)
            
            # Store response
            responses[framing_name] = {
                "question": question,
                "prompt_sent": prompt_to_send,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
            success_count += 1
            print(f"✓ Response generated successfully ({len(response)} chars)")
            
        except Exception as e:
            print(f"✗ Error generating response: {str(e)}")
            responses[framing_name] = {
                "question": question,
                "response": None,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    
    return responses, success_count

def save_responses(responses, output_file):
    """Save responses to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(responses, f, indent=2, ensure_ascii=False)

async def main(json_path=None, output_prefix="deepseek", response_instruction="", dilemma_ids=None):
    """Main function to generate responses using DeepSeek via OpenRouter."""
    # Initialize analyzer with DeepSeek configuration
    analyzer = DeicticEthicalAnalyzer(
        use_openai_direct=False,  # Use OpenRouter
        models=["deepseek/deepseek-chat"],  # DeepSeek model
        temperature=0.9  # Same temperature as original
    )
    
    # Load all dilemmas questions
    script_dir = Path(__file__).parent
    questions_path = Path(json_path) if json_path else script_dir.parent / "input_questions" / "all_dilemmas_deictic_questions.json"
    all_dilemmas = load_all_dilemmas_questions(str(questions_path))
    
    if dilemma_ids:
        all_dilemmas = {k: v for k, v in all_dilemmas.items() if k in dilemma_ids}
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = script_dir.parent / "generation_logs" / f"{output_prefix}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"DEEPSEEK RESPONSE GENERATION via OpenRouter")
    print(f"{'='*60}")
    print(f"Model: deepseek/deepseek-chat")
    print(f"Temperature: 0.9")
    print(f"Output directory: {output_dir}")
    print(f"Dilemmas to process: {len(all_dilemmas)}")
    
    # Process each dilemma
    all_results = {}
    total_success = 0
    total_attempts = 0
    
    for dilemma_name, deictic_questions in all_dilemmas.items():
        print(f"\n{'='*60}")
        print(f"Processing: {dilemma_name}")
        print(f"{'='*60}")
        
        # Generate responses
        responses, success_count = await generate_responses_for_dilemma(
            analyzer, dilemma_name, deictic_questions
            , response_instruction=response_instruction
        )
        
        # Save responses
        output_file = output_dir / f"{dilemma_name}_responses.json"
        save_responses(responses, output_file)
        
        # Update statistics
        all_results[dilemma_name] = responses
        total_success += success_count
        total_attempts += len(deictic_questions)
        
        print(f"\nSaved to: {output_file}")
        print(f"Success rate: {success_count}/{len(deictic_questions)}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total responses generated: {total_success}/{total_attempts}")
    print(f"Success rate: {(total_success/total_attempts)*100:.1f}%")
    print(f"Output directory: {output_dir}")
    
    return output_dir

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate ethical responses for multiple dilemmas using DeepSeek")
    parser.add_argument("--json-path", default=None,
                       help="Path to JSON file with dilemmas and questions")
    parser.add_argument("--output-prefix", default="deepseek",
                       help="Prefix for the output session directory")
    parser.add_argument("--response-instruction", default="",
                       help="Additional instruction prepended to every generation prompt")
    parser.add_argument("--response-instruction-file", default=None,
                       help="Path to a UTF-8 text file containing the response instruction (preferred for non-ASCII).")
    parser.add_argument("--response-instruction-key", default=None,
                       help="Key in yoruba_deixis_module/model_response_instructions.json to load the instruction from")
    parser.add_argument("--dilemma-ids", nargs="+", default=None,
                       help="Specific dilemma IDs to process (default: all)")

    args = parser.parse_args()

    instruction = args.response_instruction
    if args.response_instruction_file:
        with open(args.response_instruction_file, "r", encoding="utf-8") as f:
            instruction = f.read().strip()
    elif args.response_instruction_key:
        cfg_path = Path(__file__).parent.parent / "yoruba_deixis_module" / "model_response_instructions.json"
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        instruction = cfg["model_response_instructions"][args.response_instruction_key]

    asyncio.run(main(args.json_path, args.output_prefix, instruction, args.dilemma_ids))
