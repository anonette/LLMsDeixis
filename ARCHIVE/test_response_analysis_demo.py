"""Demonstrate that the analyzer analyzes LLM responses, not the questions."""

import asyncio
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from models.schemas import DeicticFraming

async def demonstrate_response_analysis():
    """Show what the analyzer actually analyzes."""
    
    # Create analyzer
    analyzer = DeicticEthicalAnalyzer()
    
    # Get a dilemma
    dilemma_id = "workplace_whistleblowing"
    dilemma = analyzer.dilemma_db.get_dilemma(dilemma_id)
    
    # Generate a question using the interrogative transformer
    question = analyzer.transformer.transform_dilemma(dilemma, DeicticFraming.SECOND_PERSON)
    print("STEP 1 - Interrogative Question Generated:")
    print("-" * 60)
    print(question)
    print()
    
    # Get LLM response to the question
    print("STEP 2 - Getting LLM Response to the Question...")
    print("-" * 60)
    llm_response = await analyzer.llm_agent.generate_ethical_response(question)
    print(f"LLM Response (first 200 chars): {llm_response[:200]}...")
    print()
    
    # Analyze the LLM's response
    print("STEP 3 - Analyzing the LLM's Response (NOT the question):")
    print("-" * 60)
    
    # Analyze deictic markers in the response
    deictic_markers = analyzer.transformer.analyze_deictic_markers(llm_response)
    print(f"Deictic markers in LLM response:")
    print(f"  - Second person pronouns (you/your): {deictic_markers['second_person']}")
    print(f"  - First person pronouns (I/me/my): {deictic_markers['first_person_singular']}")
    print(f"  - Obligation language (should/must): {deictic_markers['obligation_language']}")
    print()
    
    # Analyze agency in the response
    agency_analysis = await analyzer.llm_agent.analyze_agency_distribution(
        llm_response, dilemma.description
    )
    print(f"Agency analysis of LLM response:")
    print(f"  - Primary agent: {agency_analysis.primary_agent}")
    print(f"  - Agency distribution: {agency_analysis.agency_distribution}")
    print()
    
    # Analyze ethical framing in the response
    ethical_analysis = await analyzer.llm_agent.analyze_ethical_framing(
        llm_response, dilemma.description
    )
    print(f"Ethical framing in LLM response:")
    print(f"  - Primary framework: {ethical_analysis.primary_framework}")
    print(f"  - Reasoning type: {ethical_analysis.ethical_reasoning_type}")
    print()
    
    print("SUMMARY:")
    print("-" * 60)
    print("1. The interrogative transformer generates a QUESTION")
    print("2. The LLM responds to that QUESTION")
    print("3. The analyzer analyzes the LLM's RESPONSE (not the question)")
    print("4. All metrics (deictic markers, agency, ethics) come from the RESPONSE")

if __name__ == "__main__":
    asyncio.run(demonstrate_response_analysis())