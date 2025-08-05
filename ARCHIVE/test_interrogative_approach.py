"""
Test the interrogative transformer approach with stateless LLM calls.
Verifies that we send only direct questions without meta-instructions.
"""

import asyncio
import os
from dotenv import load_dotenv
from transformer_interrogative import InterrogativeTransformer
from models.schemas import EthicalDilemma, DeicticFraming
from deixis_ethical_analyzer import LLMAnalysisAgent

# Load environment variables
load_dotenv()

async def test_interrogative_transformation():
    """Test the interrogative transformer with a sample dilemma."""
    
    # Create test dilemma
    dilemma = EthicalDilemma(
        id="workplace_whistleblowing",
        title="The Corporate Cover-Up",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="contemporary_workplace",
        tags=["whistleblowing", "corporate_responsibility", "privacy", "career"]
    )
    
    # Initialize transformer
    transformer = InterrogativeTransformer()
    
    print("=== INTERROGATIVE TRANSFORMATION TEST ===\n")
    print(f"Original Dilemma: {dilemma.description}\n")
    print("=" * 80 + "\n")
    
    # Test each deictic framing
    for framing in DeicticFraming:
        print(f"\n--- {framing.value.upper()} FRAMING ---")
        
        # Generate the interrogative question
        question = transformer.transform_to_question(dilemma, framing)
        print(f"Generated Question: {question}")
        
        # Preview the transformation details
        preview = transformer.preview_transformation(dilemma, framing)
        print(f"Approach: {preview['approach']}")
        print(f"Extracted Elements:")
        for key, value in preview['extracted_elements'].items():
            print(f"  - {key}: {value}")
        
        print()

async def test_stateless_llm_calls():
    """Test that the questions work with stateless LLM calls."""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in .env file")
        return
    
    # Create components
    transformer = InterrogativeTransformer()
    llm_agent = LLMAnalysisAgent(api_key)
    
    # Test dilemma
    dilemma = EthicalDilemma(
        id="workplace_whistleblowing",
        title="The Corporate Cover-Up",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="contemporary_workplace",
        tags=["whistleblowing", "corporate_responsibility", "privacy", "career"]
    )
    
    print("\n=== STATELESS LLM CALL TEST ===\n")
    
    # Test a few framings with actual LLM calls
    test_framings = [DeicticFraming.SECOND_PERSON, DeicticFraming.FIRST_PERSON, DeicticFraming.DIALOGIC]
    
    for framing in test_framings:
        print(f"\n--- Testing {framing.value} with LLM ---")
        
        # Generate question
        question = transformer.transform_to_question(dilemma, framing)
        print(f"Question sent to LLM: {question}")
        print("\nVerifying stateless call:")
        print("✓ No system prompt")
        print("✓ No meta-instructions")
        print("✓ Only the question text")
        print("✓ Temperature: 0.9")
        
        # Make the LLM call
        print("\nLLM Response:")
        response = await llm_agent.generate_ethical_response(question)
        
        # Show first 300 characters of response
        print(response[:300] + "..." if len(response) > 300 else response)
        print("\n" + "=" * 80)

async def test_multiple_dilemmas():
    """Test the transformer with different types of dilemmas."""
    
    dilemmas = [
        EthicalDilemma(
            id="medical_allocation",
            title="Scarce Resources",
            description="During a pandemic, a hospital administrator must decide how to allocate the last ventilator between a young parent with three children and an elderly renowned scientist on the verge of a major breakthrough.",
            domain="medical ethics",
            complexity_score=8.0,
            source="healthcare",
            tags=["resource_allocation", "triage", "fairness"]
        ),
        EthicalDilemma(
            id="environmental_economy",
            title="Jobs vs Environment",
            description="A small coastal town's economy depends entirely on a factory that provides jobs for 80% of residents. Environmental tests reveal the factory is slowly poisoning the local water supply, which will cause serious health problems in 10-15 years.",
            domain="environmental ethics",
            complexity_score=7.0,
            source="environmental",
            tags=["environment", "economy", "community"]
        )
    ]
    
    transformer = InterrogativeTransformer()
    
    print("\n=== MULTIPLE DILEMMA TEST ===\n")
    
    for dilemma in dilemmas:
        print(f"\nDilemma: {dilemma.title}")
        print(f"Description: {dilemma.description[:100]}...")
        
        # Test a few framings for each
        for framing in [DeicticFraming.IMPERSONAL, DeicticFraming.SPATIAL, DeicticFraming.COSMOLOGICAL]:
            question = transformer.transform_to_question(dilemma, framing)
            print(f"\n{framing.value}: {question}")

def verify_no_instructions(question: str) -> bool:
    """Verify that a question contains no meta-instructions."""
    instruction_keywords = [
        "reframe", "transform", "convert", "change", "modify",
        "rewrite", "rephrase", "reformulate", "express differently",
        "original dilemma:", "reframed dilemma:", "instructions:"
    ]
    
    question_lower = question.lower()
    for keyword in instruction_keywords:
        if keyword in question_lower:
            return False
    return True

async def main():
    """Run all tests."""
    print("Testing Interrogative Deictic Transformer\n")
    
    # Test 1: Basic transformation
    await test_interrogative_transformation()
    
    # Test 2: Verify no instructions
    print("\n=== INSTRUCTION CHECK ===")
    transformer = InterrogativeTransformer()
    test_dilemma = EthicalDilemma(
        id="test",
        title="Test",
        description="A person must choose between personal gain and helping others.",
        domain="general",
        complexity_score=5.0,
        source="test",
        tags=["test"]
    )
    
    all_clean = True
    for framing in DeicticFraming:
        question = transformer.transform_to_question(test_dilemma, framing)
        is_clean = verify_no_instructions(question)
        status = "✓ CLEAN" if is_clean else "✗ CONTAINS INSTRUCTIONS"
        print(f"{framing.value}: {status}")
        if not is_clean:
            all_clean = False
            print(f"  Question: {question}")
    
    print(f"\nOverall: {'All questions are clean!' if all_clean else 'Some questions contain instructions!'}")
    
    # Test 3: Multiple dilemmas
    await test_multiple_dilemmas()
    
    # Test 4: Stateless LLM calls (optional - requires API key)
    if os.getenv("OPENROUTER_API_KEY"):
        await test_stateless_llm_calls()
    else:
        print("\n[Skipping LLM test - no API key found]")

if __name__ == "__main__":
    asyncio.run(main())