"""
Test to verify that the LLM now answers the reframed question instead of just reframing
"""

import asyncio
import os
from dotenv import load_dotenv
from deixis_ethical_analyzer import DeicticEthicalAnalyzer, EthicalDilemma, LLMAnalysisAgent
from transformer import DeicticTransformer, DeicticFraming

# Load environment variables
load_dotenv()

async def test_fix():
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
    
    # Get the direct question that should be sent to the LLM
    direct_question = transformer.transform_dilemma_direct(dilemma, DeicticFraming.IMPERSONAL)
    print("=== REFRAMED QUESTION (what LLM should answer) ===")
    print(direct_question)
    print()
    
    # Test the LLM response
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env file")
        return
    
    llm_agent = LLMAnalysisAgent(api_key)
    
    print("=== LLM RESPONSE (should answer the question, not reframe) ===")
    response = await llm_agent.generate_ethical_response(direct_question)
    print(response)
    print()
    
    # Check if the response is answering the question or just reframing
    reframing_indicators = [
        "security vulnerability",
        "social media application", 
        "user data",
        "unauthorized entities",
        "financial implications",
        "quarterly profits",
        "insider poses",
        "industry exclusion"
    ]
    
    is_reframing = sum(1 for indicator in reframing_indicators if indicator.lower() in response.lower()) >= 4
    
    if is_reframing:
        print("❌ ISSUE: The LLM is still reframing the dilemma instead of answering the question!")
    else:
        print("✅ SUCCESS: The LLM is now answering the ethical question!")
    
    print("\n=== ANALYSIS ===")
    print(f"Question asked: {direct_question}")
    print(f"Response type: {'Reframing' if is_reframing else 'Answer to question'}")

if __name__ == "__main__":
    asyncio.run(test_fix())