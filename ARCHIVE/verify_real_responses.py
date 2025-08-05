"""
Quick verification that LLM responses are real answers to reframed questions
"""

import asyncio
import os
from dotenv import load_dotenv
from deixis_ethical_analyzer import DeicticEthicalAnalyzer, EthicalDilemma
from transformer import DeicticFraming

# Load environment variables
load_dotenv()

async def verify_responses():
    # Create analyzer
    analyzer = DeicticEthicalAnalyzer(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        enable_rich_logging=False  # Disable logging for quick test
    )
    
    # Use the whistleblowing dilemma
    dilemma = analyzer.dilemma_db.get_dilemma("workplace_whistleblowing")
    
    print("=== VERIFYING REAL RESPONSES ===\n")
    
    # Test a few framings
    test_framings = [
        DeicticFraming.IMPERSONAL,
        DeicticFraming.FIRST_PERSON,
        DeicticFraming.DIALOGIC
    ]
    
    for framing in test_framings:
        print(f"\n--- {framing.value.upper()} FRAMING ---")
        
        # Get the direct question
        direct_question = analyzer.transformer.transform_dilemma_direct(dilemma, framing)
        print(f"Question: {direct_question}")
        
        # Get LLM response
        llm_response = await analyzer.llm_agent.generate_ethical_response(direct_question)
        
        # Show first 400 characters
        print(f"\nLLM Response (first 400 chars):")
        print(llm_response[:400] + "..." if len(llm_response) > 400 else llm_response)
        
        # Check if it's answering the question or reframing
        reframing_indicators = [
            "security vulnerability",
            "social media application", 
            "user data",
            "unauthorized entities",
            "financial implications"
        ]
        
        is_reframing = sum(1 for indicator in reframing_indicators if indicator.lower() in llm_response.lower()) >= 3
        
        print(f"\nVerification: {'❌ REFRAMING DETECTED' if is_reframing else '✅ REAL RESPONSE TO QUESTION'}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(verify_responses())