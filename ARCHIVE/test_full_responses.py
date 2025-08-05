"""Test showing full LLM responses to interrogative questions"""

import asyncio
import os
from dotenv import load_dotenv
from transformer_interrogative import InterrogativeTransformer
from models.schemas import EthicalDilemma, DeicticFraming
from deixis_ethical_analyzer import LLMAnalysisAgent

# Load environment variables
load_dotenv()

async def test_full_responses():
    """Test showing complete LLM responses to the interrogative questions."""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env file")
        return
    
    # Create components
    transformer = InterrogativeTransformer()
    llm_agent = LLMAnalysisAgent(api_key)
    
    # Test dilemma
    dilemma = EthicalDilemma(
        id="whistleblowing",
        title="Security Whistleblowing",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="workplace",
        tags=["whistleblowing", "security", "ethics"]
    )
    
    print("=== FULL LLM RESPONSES TO INTERROGATIVE QUESTIONS ===\n")
    print("Note: These are complete, untruncated responses to direct questions.")
    print("No meta-instructions or reframing prompts were used.\n")
    
    # Test three different framings
    test_framings = [
        DeicticFraming.SECOND_PERSON,
        DeicticFraming.FIRST_PERSON,
        DeicticFraming.DIALOGIC,
        DeicticFraming.SPATIAL,
        DeicticFraming.TEMPORAL,
        DeicticFraming.COSMOLOGICAL
    ]
    
    for framing in test_framings:
        print(f"\n{'='*80}")
        print(f"{framing.value.upper()} FRAMING")
        print('='*80)
        
        # Generate question
        question = transformer.transform_to_question(dilemma, framing)
        print(f"\nQUESTION SENT TO LLM:\n{question}")
        
        # Get LLM response
        print(f"\nFULL LLM RESPONSE:")
        print("-" * 80)
        response = await llm_agent.generate_ethical_response(question)
        print(response)
        print("-" * 80)
        print(f"Response length: {len(response)} characters")
        print(f"Deictic perspective: {framing.value}")
        print("Type of response: Direct ethical reasoning (not a reframing)")

if __name__ == "__main__":
    asyncio.run(test_full_responses())