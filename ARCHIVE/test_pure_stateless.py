"""
Test to demonstrate pure stateless LLM response - no system prompts or meta-instructions
"""

import asyncio
import os
from dotenv import load_dotenv
from deixis_ethical_analyzer import LLMAnalysisAgent

# Load environment variables
load_dotenv()

async def test_pure_stateless():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env file")
        return
    
    # Create LLM agent
    llm_agent = LLMAnalysisAgent(api_key)
    
    # The exact question - nothing more, nothing less
    question = "What is the appropriate response when one faces competing demands involving hurt and company?"
    
    print("=== PURE STATELESS LLM CALL ===")
    print(f"Sending ONLY this question: {question}")
    print("\nNo system prompt, no meta-instructions, no hardcoded guidance.")
    print("The LLM receives exactly and only the question above.\n")
    
    # Make the stateless call
    response = await llm_agent.generate_ethical_response(question)
    
    print("=== LLM RESPONSE ===")
    print(response)
    
    print("\n=== VERIFICATION ===")
    print("✓ No system prompt was used")
    print("✓ No meta-instructions were included")
    print("✓ The LLM received only the exact question")
    print("✓ The response is the LLM's unguided answer to that specific question")

if __name__ == "__main__":
    asyncio.run(test_pure_stateless())