"""
Test the new generative deictic transformer approach.
Shows how it minimizes hardcoding and maximizes LLM generation for studying deixis.
"""

from models.schemas import EthicalDilemma, DeicticFraming
from transformer import DeicticTransformer

def create_test_dilemma():
    """Create a test dilemma for comparison."""
    return EthicalDilemma(
        id="workplace_whistleblowing",
        title="The Corporate Cover-Up",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="contemporary_workplace",
        tags=["whistleblowing", "corporate_responsibility", "privacy", "career"]
    )

def test_generative_prompts():
    """Test the new generative prompting approach."""
    print("="*80)
    print("GENERATIVE DEICTIC TRANSFORMER TEST")
    print("="*80)
    
    transformer = DeicticTransformer()
    dilemma = create_test_dilemma()
    
    print(f"Original Dilemma: {dilemma.description[:100]}...\n")
    
    # Test each framing type
    for framing in transformer.get_available_framings():
        print(f"--- {framing.value.upper()} FRAMING ---")
        
        # Show the generative prompt (what gets sent to LLM)
        generative_prompt = transformer.transform_dilemma(dilemma, framing)
        print(f"Generative Prompt:\n{generative_prompt}\n")
        
        # Show the direct question version (for immediate use)
        direct_question = transformer.transform_dilemma_direct(dilemma, framing)
        print(f"Direct Question: {direct_question}\n")
        
        print("-" * 40)

def test_dynamic_tension_extraction():
    """Test the dynamic tension extraction (no hardcoded patterns)."""
    print("\n" + "="*80)
    print("DYNAMIC TENSION EXTRACTION TEST")
    print("="*80)
    
    transformer = DeicticTransformer()
    
    # Test various dilemma descriptions
    test_descriptions = [
        "A doctor must choose between saving one patient or two patients.",
        "A journalist wants to publish a story but it could harm innocent people.",  
        "A teacher should report cheating but the student is struggling financially.",
        "An employee discovers fraud that could help expose corruption but might cost jobs.",
        "A parent faces pressure to lie to protect their child from consequences."
    ]
    
    for i, description in enumerate(test_descriptions, 1):
        print(f"\nTest {i}: {description}")
        
        # Create temporary dilemma
        temp_dilemma = EthicalDilemma(
            id=f"test_{i}",
            title=f"Test Dilemma {i}",
            description=description,
            domain="test",
            complexity_score=5.0,
            source="test",
            tags=["test"]
        )
        
        # Extract tension dynamically
        tension = transformer._extract_dynamic_tension(description)
        print(f"Extracted Tension: {tension}")
        
        # Show how it generates different framings
        spatial_q = transformer.transform_dilemma_direct(temp_dilemma, DeicticFraming.SPATIAL)
        cosmic_q = transformer.transform_dilemma_direct(temp_dilemma, DeicticFraming.COSMOLOGICAL)
        
        print(f"Spatial: {spatial_q}")
        print(f"Cosmic: {cosmic_q}")

def test_comprehensive_marker_analysis():
    """Test the enhanced 20+ category deictic marker analysis."""
    print("\n" + "="*80)
    print("COMPREHENSIVE DEICTIC MARKER ANALYSIS")
    print("="*80)
    
    transformer = DeicticTransformer()
    
    # Test responses with different deictic patterns
    test_responses = [
        "I believe we should carefully consider what the universe demands of us here and now, standing at this crossroads where ancestors guide our sacred duty.",
        "You must decide whether to act immediately, as the situation requires urgent attention from your position.",
        "The appropriate response involves analyzing their perspective through ethical principles that transcend individual choice.",
        "We collectively face this moment when our cosmic responsibilities collide with earthly obligations."
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n--- Test Response {i} ---")
        print(f"Text: {response}")
        
        # Analyze with comprehensive system
        markers = transformer.analyze_deictic_markers(response)
        
        # Show all non-zero markers
        print("Detected Markers:")
        for marker_type, count in markers.items():
            if count > 0:
                print(f"  {marker_type}: {count}")
        
        # Suggest frame type
        suggested_frame, confidence = transformer.suggest_frame_type(response)
        print(f"Suggested Frame: {suggested_frame.value} (confidence: {confidence:.2f})")

def test_preview_functionality():
    """Test the preview functionality that shows both approaches."""
    print("\n" + "="*80)
    print("PREVIEW FUNCTIONALITY TEST")
    print("="*80)
    
    transformer = DeicticTransformer()
    dilemma = create_test_dilemma()
    
    # Preview different framings
    for framing in [DeicticFraming.SPATIAL, DeicticFraming.COSMOLOGICAL, DeicticFraming.DIALOGIC]:
        print(f"\n--- {framing.value.upper()} PREVIEW ---")
        
        preview = transformer.preview_transformation(dilemma, framing)
        
        for key, value in preview.items():
            if len(str(value)) > 100:
                value = str(value)[:100] + "..."
            print(f"{key}: {value}")

def main():
    """Run all tests to demonstrate the generative approach."""
    print("GENERATIVE DEICTIC TRANSFORMER - MINIMAL HARDCODING, MAXIMUM LLM GENERATION")
    print("Designed to study how LLMs naturally handle deictic transformations")
    print("\nKey Features:")
    print("- Minimal prescriptive prompts instead of hardcoded templates")
    print("- Dynamic tension extraction without predefined patterns") 
    print("- 20+ category comprehensive deictic marker analysis")
    print("- Both generative prompts and direct questions available")
    print("- Focus on studying emergent LLM deictic behavior")
    
    try:
        test_generative_prompts()
        test_dynamic_tension_extraction()
        test_comprehensive_marker_analysis()
        test_preview_functionality()
        
        print("\n" + "="*80)
        print("SUCCESS: GENERATIVE APPROACH READY FOR DEIXIS RESEARCH")
        print("="*80)
        
        print("\nThis approach will help you study:")
        print("- How LLMs naturally interpret deictic framing instructions")
        print("- What deictic markers emerge in ethical reasoning")
        print("- How different framings affect moral decision-making")
        print("- Emergent patterns in LLM deictic behavior")
        print("- Natural language deixis vs prescribed patterns")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
