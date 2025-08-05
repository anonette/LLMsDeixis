"""
Test to demonstrate the reframing issue and show the fix
"""

import asyncio
from deixis_ethical_analyzer import DeicticEthicalAnalyzer, EthicalDilemma
from transformer import DeicticTransformer, DeicticFraming

async def test_reframing_issue():
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
    
    print("=== CURRENT BEHAVIOR ===")
    print("\n1. transform_dilemma() output (what gets sent to LLM):")
    transformed_prompt = transformer.transform_dilemma(dilemma, DeicticFraming.IMPERSONAL)
    print(transformed_prompt)
    
    print("\n2. transform_dilemma_direct() output (the actual question):")
    direct_question = transformer.transform_dilemma_direct(dilemma, DeicticFraming.IMPERSONAL)
    print(direct_question)
    
    print("\n3. Extracted tension:")
    tension = transformer._extract_dynamic_tension(dilemma.description)
    print(tension)
    
    print("\n=== THE ISSUE ===")
    print("The LLM receives the transform_dilemma() output which asks it to REFRAME the dilemma,")
    print("not to ANSWER the ethical question. So it provides a reframed description instead of")
    print("answering 'What is the appropriate response when one faces competing demands involving hurt and company?'")
    
    print("\n=== THE FIX ===")
    print("To get the LLM to answer the reframed question, we should send:")
    print(f"\n{direct_question}")
    print("\nThis way the LLM will provide an answer to the ethical question, not just reframe it.")

if __name__ == "__main__":
    asyncio.run(test_reframing_issue())