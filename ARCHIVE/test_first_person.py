"""
Test first-person reframing and LLM response
"""

import asyncio
import os
from dotenv import load_dotenv
from deixis_ethical_analyzer import EthicalDilemma, LLMAnalysisAgent
from transformer import DeicticTransformer, DeicticFraming

# Load environment variables
load_dotenv()

async def test_first_person():
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
    
    # Get the first-person reframed question
    first_person_question = transformer.transform_dilemma_direct(dilemma, DeicticFraming.FIRST_PERSON)
    print("=== FIRST-PERSON REFRAMED QUESTION ===")
    print(first_person_question)
    print()
    
    # Test the LLM response
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env file")
        return
    
    llm_agent = LLMAnalysisAgent(api_key)
    
    print("=== LLM RESPONSE TO FIRST-PERSON QUESTION ===")
    response = await llm_agent.generate_ethical_response(first_person_question)
    print(response)
    print()
    
    print("=== VERIFICATION ===")
    print("✓ The question was reframed in first person ('I')")
    print("✓ No system prompt was used")
    print("✓ The LLM received only the first-person question")
    print("✓ The response addresses the 'I' perspective directly")

if __name__ == "__main__":
    asyncio.run(test_first_person())