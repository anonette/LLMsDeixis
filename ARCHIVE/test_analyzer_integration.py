"""Test that the interrogative transformer works properly with the analyzer and logging."""

import asyncio
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from models.schemas import EthicalDilemma, DeicticFraming
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_analyzer_integration():
    """Test the analyzer with the new interrogative transformer."""
    
    # Create analyzer
    analyzer = DeicticEthicalAnalyzer()
    
    # Create test dilemma
    test_dilemma = EthicalDilemma(
        id="integration_test",
        title="Security Flaw Whistleblowing",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="test",
        tags=["whistleblowing", "security", "privacy"]
    )
    
    # The analyzer already has dilemmas from its database
    # We'll use the existing workplace_whistleblowing dilemma which is similar
    dilemma_id = "workplace_whistleblowing"
    
    print("Testing analyzer with interrogative transformer...")
    print("=" * 60)
    
    # Test with a few framings
    test_framings = [DeicticFraming.IMPERSONAL, DeicticFraming.SECOND_PERSON, DeicticFraming.COSMOLOGICAL]
    
    for framing in test_framings:
        print(f"\nTesting {framing.value} framing:")
        print("-" * 40)
        
        # Get the first dilemma from the database for testing
        test_dilemma_from_db = analyzer.dilemma_db.get_dilemma(dilemma_id)
        
        # Get the transformed question
        question = analyzer.transformer.transform_dilemma(test_dilemma_from_db, framing)
        print(f"Generated question: {question}")
        
        # Verify it's a question
        assert question.endswith("?"), f"Should end with '?': {question}"
        
        # Verify no meta-instructions
        meta_words = ["reframe", "transform", "using", "language", "perspective"]
        assert not any(word in question.lower() for word in meta_words), f"Contains meta-instructions: {question}"
        
        print("✓ Question format validated")
    
    print("\n" + "=" * 60)
    print("Running full analysis on one framing...")
    print("=" * 60)
    
    # Get the dilemma and run analysis on just one framing
    dilemma = analyzer.dilemma_db.get_dilemma(dilemma_id)
    result = await analyzer._analyze_single_framework(dilemma, DeicticFraming.SECOND_PERSON)
    
    if result:
        print(f"\nAnalysis completed for {result.framing.value}:")
        print(f"- Transformed prompt: {result.transformed_prompt[:100]}...")
        print(f"- LLM responded: {'Yes' if result.llm_response else 'No'}")
        print(f"- Response length: {result.response_length} chars")
        print(f"- Processing time: {result.processing_time:.2f}s")
        
        if result.agency_analysis:
            print(f"- Primary agent: {result.agency_analysis.primary_agent}")
            print(f"- Agency distribution: {result.agency_analysis.agency_distribution}")
        
        if result.ethical_framing_analysis:
            print(f"- Ethical framework: {result.ethical_framing_analysis.primary_framework}")
            print(f"- Reasoning type: {result.ethical_framing_analysis.ethical_reasoning_type}")
        
        print(f"- Deictic markers found: {result.deictic_markers.get('total_markers', 0)}")
        
        print("\n✓ Full analysis pipeline working correctly!")
    else:
        print("❌ No results returned from analysis")
    
    # Check that logging is working
    print("\n" + "=" * 60)
    print("Checking analysis logger...")
    print("=" * 60)
    
    # The analyzer should have created log entries
    if hasattr(analyzer, 'analysis_logger') and analyzer.analysis_logger:
        print("✓ Analysis logger is active")
        
        # Generate summary to test logging
        summary = analyzer.generate_summary()
        if summary:
            print(f"✓ Summary generated with {len(summary.get('dilemmas_analyzed', []))} dilemmas")
            print(f"✓ Total analyses: {summary.get('total_analyses', 0)}")
        else:
            print("❌ No summary generated")
    else:
        print("❌ Analysis logger not found")

if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_analyzer_integration())