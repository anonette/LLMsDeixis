"""
Generate Responses Only - Academic Integrity Dilemma
Generate responses using the high-quality deictic questions from academic_integrity_deictic_questions.json
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from transformer import DeicticFraming

def load_academic_integrity_questions():
    """Load the academic integrity deictic questions from JSON."""
    json_file = Path("academic_integrity_deictic_questions.json")
    if not json_file.exists():
        raise FileNotFoundError("academic_integrity_deictic_questions.json not found!")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

async def generate_responses_only():
    """Generate responses for academic integrity dilemma only using JSON questions."""
    
    print("🚀 ACADEMIC INTEGRITY DILEMMA - GPT-4o")
    print("=" * 60)
    print("Configuration:")
    print("  - Model: GPT-4o (OpenAI direct)")
    print("  - Generation Temperature: 0.9")
    print("  - Source: academic_integrity_deictic_questions.json")
    print("  - 1 dilemma × 9 framings = 9 responses")
    print("=" * 60)
    
    # Load the academic integrity questions
    try:
        academic_data = load_academic_integrity_questions()
        deictic_questions = academic_data["deictic_questions"]
        print(f"\n✓ Loaded questions for: {academic_data['dilemma_title']}")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return
    
    # Initialize analyzer for generation only
    analyzer = DeicticEthicalAnalyzer(
        use_openai_direct=True,
        temperature=0.9,  # High temperature for generation
        enable_rich_logging=False  # Disable complex logging
    )
    
    # All 9 deictic framings (including the new first_person_plural)
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
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"generation_logs/academic_integrity_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nStarting generation...")
    print(f"Output directory: {output_dir}")
    print()
    
    dilemma_responses = {
        "dilemma_id": academic_data["dilemma_id"],
        "dilemma_title": academic_data["dilemma_title"],
        "dilemma_description": academic_data["dilemma_description"],
        "timestamp": datetime.now().isoformat(),
        "model": "gpt-4o",
        "temperature": 0.9,
        "question_source": "academic_integrity_deictic_questions.json",
        "responses": {}
    }
    
    total_responses = len(framings) + len(custom_framings)
    current = 0
    
    print(f"{'='*80}")
    print(f"DILEMMA: {academic_data['dilemma_title']}")
    print(f"ID: {academic_data['dilemma_id']}")
    print('='*80)
    
    # Process standard framings
    for framing in framings:
        current += 1
        framing_key = framing.value
        
        print(f"\n[{current}/{total_responses}] {framing_key.upper()} framing...")
        
        if framing_key not in deictic_questions:
            print(f"  ❌ No question found for {framing_key}")
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
            
            print(f"  ✓ Generated ({len(response)} chars, {generation_time:.2f}s)")
            
            # Brief delay to avoid rate limiting
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            dilemma_responses["responses"][framing_key] = {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # Process custom framings
    for framing_key in custom_framings:
        current += 1
        
        print(f"\n[{current}/{total_responses}] {framing_key.upper()} framing...")
        
        if framing_key not in deictic_questions:
            print(f"  ❌ No question found for {framing_key}")
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
            
            print(f"  ✓ Generated ({len(response)} chars, {generation_time:.2f}s)")
            
            # Brief delay to avoid rate limiting
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            dilemma_responses["responses"][framing_key] = {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # Save complete responses
    complete_file = output_dir / "academic_integrity_responses.json"
    with open(complete_file, 'w', encoding='utf-8') as f:
        json.dump({
            "generation_session": {
                "timestamp": timestamp,
                "model": "gpt-4o",
                "temperature": 0.9,
                "dilemma": "academic_integrity_only",
                "source_file": "academic_integrity_deictic_questions.json"
            },
            "original_questions": academic_data,
            "responses": dilemma_responses
        }, f, indent=2, ensure_ascii=False)
    
    # Generate summary
    successful = sum(1 for framing in dilemma_responses["responses"] if "error" not in dilemma_responses["responses"][framing])
    failed = sum(1 for framing in dilemma_responses["responses"] if "error" in dilemma_responses["responses"][framing])
    
    summary = {
        "session_info": {
            "timestamp": timestamp,
            "model": "gpt-4o", 
            "temperature": 0.9,
            "dilemma_focus": "academic_integrity_only",
            "output_directory": str(output_dir)
        },
        "statistics": {
            "total_framings": len(framings) + len(custom_framings),
            "successful_generations": successful,
            "failed_generations": failed
        },
        "research_design": {
            "deictic_framings": [f.value for f in framings] + custom_framings,
            "question_source": "JSON file with expert-crafted questions",
            "hypothesis": "Different deictic markers will elicit different reasoning patterns for academic integrity dilemma"
        }
    }
    
    summary_file = output_dir / "generation_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Final report
    print(f"\n\n🎉 GENERATION COMPLETE!")
    print("=" * 60)
    print(f"Dilemma: {academic_data['dilemma_title']}")
    print(f"Successful responses: {successful}/{len(framings) + len(custom_framings)}")
    print(f"Output directory: {output_dir}")
    print(f"Complete file: {complete_file}")
    print(f"Summary file: {summary_file}")
    print("\n✅ Academic integrity deictic analysis ready!")

if __name__ == "__main__":
    asyncio.run(generate_responses_only()) 