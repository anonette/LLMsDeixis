"""
Show real LLM responses to verify they are answering the reframed questions
"""

import asyncio
import os
from dotenv import load_dotenv
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from transformer import DeicticFraming

# Load environment variables
load_dotenv()

async def show_real_responses():
    print("=== SHOWING REAL LLM RESPONSES TO REFRAMED QUESTIONS ===\n")
    
    # Create analyzer
    analyzer = DeicticEthicalAnalyzer(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        enable_rich_logging=False
    )
    
    # Get the whistleblowing dilemma
    dilemma = analyzer.dilemma_db.get_dilemma("workplace_whistleblowing")
    
    # Test 3 different framings
    test_framings = [
        DeicticFraming.IMPERSONAL,
        DeicticFraming.FIRST_PERSON,
        DeicticFraming.DIALOGIC
    ]
    
    for framing in test_framings:
        print(f"\n{'='*80}")
        print(f"{framing.value.upper()} FRAMING")
        print('='*80)
        
        # Get the direct question
        direct_question = analyzer.transformer.transform_dilemma_direct(dilemma, framing)
        print(f"\nReframed Question: {direct_question}")
        
        # Get LLM response
        print("\nGenerating LLM response...")
        llm_response = await analyzer.llm_agent.generate_ethical_response(direct_question)
        
        # Show the response
        print(f"\nLLM Response:")
        print("-" * 40)
        print(llm_response[:800] + "..." if len(llm_response) > 800 else llm_response)
        print("-" * 40)
        
        # Quick check
        reframing_words = ["security vulnerability", "social media application", "user data", "unauthorized entities"]
        is_reframing = sum(1 for word in reframing_words if word.lower() in llm_response.lower()) >= 2
        
        print(f"\nVerification: {'❌ This looks like a reframing!' if is_reframing else '✅ This is a real response to the question!'}")

if __name__ == "__main__":
    asyncio.run(show_real_responses())