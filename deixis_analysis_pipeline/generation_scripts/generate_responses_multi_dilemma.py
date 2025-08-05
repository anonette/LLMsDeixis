"""
Generate Responses for Multiple Dilemmas
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
        return data

async def generate_responses_for_dilemma(analyzer, dilemma_data, output_dir):
    """Generate responses for a single dilemma across all framings."""
    
    # All 9 deictic framings
    framings = [
        DeicticFraming.IMPERSONAL,
        DeicticFraming.SECOND_PERSON,
        DeicticFraming.FIRST_PERSON,
        DeicticFraming.REFLEXIVE,
        DeicticFraming.DIALOGIC,
        DeicticFraming.SPATIAL,
        DeicticFraming.TEMPORAL,
        DeicticFraming.COSMOLOGICAL
    ]
    
    # Add the custom first_person_plural framing
    custom_framings = ["first_person_plural"]
    
    deictic_questions = dilemma_data["deictic_questions"]
    
    dilemma_responses = {
        "dilemma_id": dilemma_data["dilemma_id"],
        "dilemma_title": dilemma_data["dilemma_title"],
        "dilemma_description": dilemma_data["dilemma_description"],
        "timestamp": datetime.now().isoformat(),
        "model": "gpt-4o",
        "temperature": 0.9,
        "responses": {}
    }
    
    if "ethical_dimensions" in dilemma_data:
        dilemma_responses["ethical_dimensions"] = dilemma_data["ethical_dimensions"]
    
    total_responses = len(framings) + len(custom_framings)
    current = 0
    
    print(f"\n{'='*80}")
    print(f"DILEMMA: {dilemma_data['dilemma_title']}")
    print(f"ID: {dilemma_data['dilemma_id']}")
    print('='*80)
    
    # Process standard framings
    for framing in framings:
        current += 1
        framing_key = framing.value
        
        print(f"\n[{current}/{total_responses}] {framing_key.upper()} framing...")
        
        if framing_key not in deictic_questions:
            print(f"  [X] No question found for {framing_key}")
            continue
            
        try:
            # Get the question from JSON
            question_data = deictic_questions[framing_key]
            deictic_question = question_data["question"]
            
            print(f"  Question: {deictic_question[:100]}...")
            
            # Generate response using GPT-4o
            start_time = datetime.now()
            response = await analyzer.llm_agent.generate_ethical_response(deictic_question)
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Store the response with metadata from JSON
            dilemma_responses["responses"][framing_key] = {
                "deictic_question": deictic_question,
                "deictic_markers": question_data.get("deictic_markers", []),
                "framing_focus": question_data.get("focus", ""),
                "response": response,
                "generation_time_seconds": generation_time,
                "response_length": len(response),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"  [OK] Generated ({len(response)} chars, {generation_time:.2f}s)")
            
            # Brief delay to avoid rate limiting
            await asyncio.sleep(1.0)
            
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            dilemma_responses["responses"][framing_key] = {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # Process custom framings
    for framing_key in custom_framings:
        current += 1
        
        print(f"\n[{current}/{total_responses}] {framing_key.upper()} framing...")
        
        if framing_key not in deictic_questions:
            print(f"  [X] No question found for {framing_key}")
            continue
            
        try:
            # Get the question from JSON
            question_data = deictic_questions[framing_key]
            deictic_question = question_data["question"]
            
            print(f"  Question: {deictic_question[:100]}...")
            
            # Generate response using GPT-4o
            start_time = datetime.now()
            response = await analyzer.llm_agent.generate_ethical_response(deictic_question)
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Store the response with metadata from JSON
            dilemma_responses["responses"][framing_key] = {
                "deictic_question": deictic_question,
                "deictic_markers": question_data.get("deictic_markers", []),
                "framing_focus": question_data.get("focus", ""),
                "response": response,
                "generation_time_seconds": generation_time,
                "response_length": len(response),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"  [OK] Generated ({len(response)} chars, {generation_time:.2f}s)")
            
            # Brief delay to avoid rate limiting
            await asyncio.sleep(1.0)
            
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            dilemma_responses["responses"][framing_key] = {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # Save dilemma responses
    dilemma_file = output_dir / f"{dilemma_data['dilemma_id']}_responses.json"
    with open(dilemma_file, 'w', encoding='utf-8') as f:
        json.dump(dilemma_responses, f, indent=2, ensure_ascii=False)
    
    # Calculate statistics
    successful = sum(1 for framing in dilemma_responses["responses"] if "error" not in dilemma_responses["responses"][framing])
    failed = sum(1 for framing in dilemma_responses["responses"] if "error" in dilemma_responses["responses"][framing])
    
    print(f"\n[DONE] Completed {dilemma_data['dilemma_title']}")
    print(f"  Successful: {successful}/{total_responses}")
    print(f"  Failed: {failed}/{total_responses}")
    print(f"  Saved to: {dilemma_file}")
    
    return dilemma_responses, successful, failed

async def generate_responses_multi_dilemma(dilemma_ids=None, json_path="all_dilemmas_deictic_questions.json"):
    """Generate responses for multiple dilemmas using JSON questions."""
    
    print("MULTI-DILEMMA DEICTIC ANALYSIS - GPT-4o")
    print("=" * 60)
    print("Configuration:")
    print("  - Model: GPT-4o (OpenAI direct)")
    print("  - Generation Temperature: 0.9")
    print(f"  - Source: {json_path}")
    print("=" * 60)
    
    # Load all dilemmas
    try:
        all_data = load_all_dilemmas_questions(json_path)
        dilemmas = all_data["dilemmas"]
        print(f"\n[OK] Loaded {len(dilemmas)} dilemmas from JSON")
        
        # Filter dilemmas if specific IDs provided
        if dilemma_ids:
            dilemmas = [d for d in dilemmas if d["dilemma_id"] in dilemma_ids]
            print(f"[OK] Filtered to {len(dilemmas)} specified dilemmas")
            
    except Exception as e:
        print(f"[ERROR] Error loading JSON: {e}")
        return
    
    # Initialize analyzer for generation only
    analyzer = DeicticEthicalAnalyzer(
        use_openai_direct=True,
        temperature=0.9,  # High temperature for generation
        enable_rich_logging=False  # Disable complex logging
    )
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Use absolute path relative to the script location
    output_dir = Path(__file__).parent.parent / "generation_logs" / f"multi_dilemma_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nStarting generation...")
    print(f"Output directory: {output_dir}")
    print(f"Processing {len(dilemmas)} dilemmas × 9 framings = {len(dilemmas) * 9} responses")
    
    # Process each dilemma
    all_responses = []
    total_successful = 0
    total_failed = 0
    
    for idx, dilemma in enumerate(dilemmas, 1):
        print(f"\n\n{'='*80}")
        print(f"PROCESSING DILEMMA {idx}/{len(dilemmas)}")
        print('='*80)
        
        try:
            responses, successful, failed = await generate_responses_for_dilemma(
                analyzer, dilemma, output_dir
            )
            all_responses.append(responses)
            total_successful += successful
            total_failed += failed
            
            # Longer delay between dilemmas to avoid rate limiting
            if idx < len(dilemmas):
                print(f"\n[WAIT] Waiting 2 seconds before next dilemma...")
                await asyncio.sleep(2.0)
                
        except Exception as e:
            print(f"[FAILED] Failed to process dilemma {dilemma['dilemma_id']}: {e}")
            total_failed += 9  # Count all framings as failed
    
    # Save complete session data
    session_data = {
        "generation_session": {
            "timestamp": timestamp,
            "model": "gpt-4o",
            "temperature": 0.9,
            "total_dilemmas": len(dilemmas),
            "source_file": json_path
        },
        "dilemmas_processed": [d["dilemma_id"] for d in dilemmas],
        "all_responses": all_responses,
        "statistics": {
            "total_responses_attempted": len(dilemmas) * 9,
            "total_successful": total_successful,
            "total_failed": total_failed,
            "success_rate": total_successful / (len(dilemmas) * 9) if len(dilemmas) > 0 else 0
        }
    }
    
    session_file = output_dir / "complete_session_data.json"
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    # Generate summary report
    summary = {
        "session_info": {
            "timestamp": timestamp,
            "model": "gpt-4o",
            "temperature": 0.9,
            "output_directory": str(output_dir)
        },
        "dilemmas_summary": [
            {
                "id": d["dilemma_id"],
                "title": d["dilemma_title"],
                "responses_generated": len([r for r in all_responses if r["dilemma_id"] == d["dilemma_id"]][0]["responses"]) if any(r["dilemma_id"] == d["dilemma_id"] for r in all_responses) else 0
            }
            for d in dilemmas
        ],
        "statistics": {
            "total_dilemmas": len(dilemmas),
            "total_framings_per_dilemma": 9,
            "total_responses_attempted": len(dilemmas) * 9,
            "successful_generations": total_successful,
            "failed_generations": total_failed,
            "success_rate_percentage": (total_successful / (len(dilemmas) * 9) * 100) if len(dilemmas) > 0 else 0
        },
        "research_design": {
            "deictic_framings": ["impersonal", "second_person", "first_person", "first_person_plural",
                               "reflexive", "dialogic", "spatial", "temporal", "cosmological"],
            "question_source": "JSON file with expert-crafted questions",
            "hypothesis": "Different deictic markers will elicit different reasoning patterns across diverse ethical dilemmas"
        }
    }
    
    summary_file = output_dir / "generation_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Final report
    print(f"\n\n🎉 MULTI-DILEMMA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"Dilemmas processed: {len(dilemmas)}")
    print(f"Total responses attempted: {len(dilemmas) * 9}")
    print(f"Successful responses: {total_successful}")
    print(f"Failed responses: {total_failed}")
    print(f"Success rate: {(total_successful / (len(dilemmas) * 9) * 100):.1f}%" if len(dilemmas) > 0 else "N/A")
    print(f"\nOutput directory: {output_dir}")
    print(f"Session data: {session_file}")
    print(f"Summary file: {summary_file}")
    print("\n[SUCCESS] Multi-dilemma deictic analysis ready!")

def main():
    """Main entry point with command line argument support."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate responses for multiple ethical dilemmas with deictic framings')
    parser.add_argument('--dilemmas', nargs='+', help='Specific dilemma IDs to process (default: all)')
    parser.add_argument('--json-path', default='all_dilemmas_deictic_questions.json',
                       help='Path to JSON file with dilemma questions')
    
    args = parser.parse_args()
    
    # Run the async function
    asyncio.run(generate_responses_multi_dilemma(
        dilemma_ids=args.dilemmas,
        json_path=args.json_path
    ))

if __name__ == "__main__":
    main()