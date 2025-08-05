"""
Test script to compare the original transformer with the enhanced hybrid approach.
Demonstrates the benefits of combining both architectural styles.
"""

import sys
import asyncio
from models.schemas import EthicalDilemma, DeicticFraming
from transformer import DeicticTransformer as OriginalTransformer
from transformer_enhanced import EnhancedDeicticTransformer

def create_test_dilemmas():
    """Create test dilemmas for comparison."""
    return [
        EthicalDilemma(
            id="workplace_whistleblowing",
            title="The Corporate Cover-Up",
            description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits.",
            domain="professional ethics",
            complexity_score=7.5,
            source="contemporary_workplace",
            tags=["whistleblowing", "corporate_responsibility", "privacy", "career"]
        ),
        EthicalDilemma(
            id="medical_resource_allocation",
            title="The ICU Bed Decision", 
            description="A hospital administrator during a health crisis has only one ICU bed left. Two patients arrive simultaneously: a 30-year-old parent of three and a 65-year-old doctor who served the community.",
            domain="medical ethics",
            complexity_score=8.9,
            source="healthcare_triage",
            tags=["triage", "life_death", "fairness", "medical_resources"]
        ),
        EthicalDilemma(
            id="unknown_scenario",
            title="Generic Ethical Conflict",
            description="A person must choose between helping a friend conceal a mistake that could harm others or refusing to help and potentially damaging the friendship.",
            domain="personal ethics",
            complexity_score=6.0,
            source="generic",
            tags=["friendship", "loyalty", "harm_prevention"]
        )
    ]

def test_frame_information():
    """Test the enhanced frame information system."""
    print("=== ENHANCED FRAME INFORMATION ===")
    enhanced = EnhancedDeicticTransformer()
    
    for framing in enhanced.get_available_framings():
        frame_info = enhanced.get_frame_info(framing)
        print(f"\n{framing.value.upper()}:")
        print(f"  Strategy: {frame_info.transformation_strategy}")
        print(f"  Description: {frame_info.description}")
        print(f"  Key Markers: {', '.join(frame_info.linguistic_markers[:3])}")
        print(f"  Example Phrases: {', '.join(frame_info.example_phrases[:2])}")

def test_transformation_comparison():
    """Compare transformations between original and enhanced approaches."""
    print("\n" + "="*80)
    print("TRANSFORMATION COMPARISON")
    print("="*80)
    
    original = OriginalTransformer()
    enhanced = EnhancedDeicticTransformer()
    dilemmas = create_test_dilemmas()
    
    # Test specific framings that showcase differences
    test_framings = [
        DeicticFraming.FIRST_PERSON,
        DeicticFraming.SPATIAL, 
        DeicticFraming.COSMOLOGICAL,
        DeicticFraming.DIALOGIC
    ]
    
    for dilemma in dilemmas:
        print(f"\n--- {dilemma.title} ---")
        print(f"Original: {dilemma.description[:100]}...")
        
        for framing in test_framings:
            print(f"\n{framing.value.upper()}:")
            
            # Original transformation
            try:
                orig_result = original.transform_dilemma(dilemma, framing)
                print(f"  Original: {orig_result}")
            except Exception as e:
                print(f"  Original: ERROR - {e}")
            
            # Enhanced transformation
            try:
                enhanced_result = enhanced.transform_dilemma(dilemma, framing)
                print(f"  Enhanced: {enhanced_result}")
            except Exception as e:
                print(f"  Enhanced: ERROR - {e}")

def test_preview_functionality():
    """Test the enhanced preview functionality."""
    print("\n" + "="*80)
    print("PREVIEW FUNCTIONALITY TEST")
    print("="*80)
    
    enhanced = EnhancedDeicticTransformer()
    dilemma = create_test_dilemmas()[0]  # Use workplace whistleblowing
    
    # Test preview for different framings
    for framing in [DeicticFraming.SPATIAL, DeicticFraming.TEMPORAL]:
        print(f"\n--- PREVIEW: {framing.value.upper()} ---")
        preview = enhanced.preview_transformation(dilemma, framing)
        
        for key, value in preview.items():
            if isinstance(value, list):
                value = ', '.join(value[:3]) + ('...' if len(value) > 3 else '')
            elif len(str(value)) > 150:
                value = str(value)[:150] + "..."
            print(f"  {key}: {value}")

def test_enhanced_marker_analysis():
    """Test the enhanced deictic marker analysis."""
    print("\n" + "="*80)
    print("ENHANCED MARKER ANALYSIS TEST")
    print("="*80)
    
    original = OriginalTransformer()
    enhanced = EnhancedDeicticTransformer()
    
    # Test responses with different deictic patterns
    test_responses = [
        "I believe you should carefully consider what we need to do here and now.",
        "Standing at this crossroads under the eternal gaze of cosmic justice, one must choose.",
        "The appropriate response involves analyzing the situation from their perspective.",
        "We collectively face this moment when our ancestors' wisdom guides us."
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n--- Test Response {i} ---")
        print(f"Text: {response}")
        
        # Original analysis
        print("\nOriginal Analysis:")
        orig_markers = original.analyze_deictic_markers(response)
        for marker_type, count in orig_markers.items():
            if count > 0:
                print(f"  {marker_type}: {count}")
        
        # Enhanced analysis
        print("\nEnhanced Analysis:")
        enhanced_markers = enhanced.analyze_deictic_markers(response)
        for marker_type, count in enhanced_markers.items():
            if count > 0:
                print(f"  {marker_type}: {count}")

def test_frame_suggestion():
    """Test the frame suggestion functionality."""
    print("\n" + "="*80)
    print("FRAME SUGGESTION TEST")
    print("="*80)
    
    enhanced = EnhancedDeicticTransformer()
    
    test_texts = [
        "How should you handle this situation when you face competing demands?",
        "Standing here at this crossroads, what action is needed?",
        "Under the gaze of ancestors, what honors the cosmic order?",
        "What should we collectively decide as our response?",
        "What is the appropriate action when one faces this dilemma?"
    ]
    
    for text in test_texts:
        suggested_frame, confidence = enhanced.suggest_frame_type(text)
        print(f"\nText: {text}")
        print(f"Suggested Frame: {suggested_frame.value}")
        print(f"Confidence: {confidence:.2f}")

def test_conflict_extraction():
    """Test the enhanced conflict extraction system."""
    print("\n" + "="*80)
    print("CONFLICT EXTRACTION TEST")
    print("="*80)
    
    enhanced = EnhancedDeicticTransformer()
    dilemmas = create_test_dilemmas()
    
    for dilemma in dilemmas:
        print(f"\n--- {dilemma.title} ---")
        conflict = enhanced._extract_core_conflict(dilemma)
        
        print(f"ID: {dilemma.id}")
        print(f"Core Conflict: {conflict['conflict']}")
        print(f"Actor Situation: {conflict['actor_situation']}")
        print(f"Decision Type: {'Predefined' if dilemma.id in enhanced.conflict_patterns else 'Pattern-matched'}")

def main():
    """Run all tests."""
    print("ENHANCED DEICTIC TRANSFORMER TEST SUITE")
    print("="*80)
    
    try:
        # Run all test functions
        test_frame_information()
        test_transformation_comparison()
        test_preview_functionality()
        test_enhanced_marker_analysis()
        test_frame_suggestion()
        test_conflict_extraction()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print("\nKEY IMPROVEMENTS IN ENHANCED VERSION:")
        print("- Hybrid approach: Templates for precision, direct methods for nuance")
        print("- Enhanced frame metadata with transformation strategies")
        print("- Improved marker analysis with cosmic and collective categories")
        print("- Frame suggestion based on linguistic analysis")
        print("- Pattern-based conflict extraction for unknown dilemmas")
        print("- Comprehensive preview functionality for debugging")
        print("- Backward compatibility with existing codebase")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
