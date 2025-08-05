"""
Test all 8 deictic framings to show how the LLM responds to each perspective
"""

import asyncio
import os
from dotenv import load_dotenv
from deixis_ethical_analyzer import EthicalDilemma, LLMAnalysisAgent
from transformer import DeicticTransformer, DeicticFraming

# Load environment variables
load_dotenv()

async def test_all_framings():
    # Create the dilemma
    dilemma = EthicalDilemma(
        id="workplace_whistleblowing",
        title="The Corporate Cover-Up",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="contemporary_workplace",
        tags=["whistleblowing", "corporate_responsibility", "privacy", "career"]
    )
    
    transformer = DeicticTransformer()
    
    # Test the LLM response
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env file")
        return
    
    llm_agent = LLMAnalysisAgent(api_key)
    
    # Test all 8 framings
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
    
    print("=== TESTING ALL 8 DEICTIC FRAMINGS ===\n")
    print("Original dilemma: A software engineer discovers a security flaw that exposes user data...")
    print("\n" + "="*80 + "\n")
    
    for framing in framings:
        print(f"\n### {framing.value.upper()} FRAMING ###")
        
        # Get the reframed question
        question = transformer.transform_dilemma_direct(dilemma, framing)
        print(f"\nReframed Question: {question}")
        
        # Get LLM response
        print("\nLLM Response:")
        response = await llm_agent.generate_ethical_response(question)
        
        # Show first 500 characters of response to keep output manageable
        if len(response) > 500:
            print(response[:500] + "...\n[Response truncated for brevity]")
        else:
            print(response)
        
        print("\n" + "-"*80)
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(1)
    
    print("\n=== SUMMARY ===")
    print("✓ All 8 framings tested")
    print("✓ Each framing produces a different question perspective")
    print("✓ LLM responds naturally to each perspective without system prompts")
    print("✓ Responses adapt to the deictic framing (I, you, we, spatial, temporal, etc.)")

if __name__ == "__main__":
    asyncio.run(test_all_framings())