"""Test that the new interrogative transformer is compatible with the analyzer."""

from transformer import DeicticTransformer, DeicticFraming
from models.schemas import EthicalDilemma

def test_transformer_compatibility():
    """Test that all methods work as expected."""
    
    # Create transformer
    transformer = DeicticTransformer()
    
    # Create test dilemma
    dilemma = EthicalDilemma(
        id="test",
        title="Test Dilemma",
        description="A software engineer discovers that their company's popular social media app contains a security flaw that exposes user data to hackers. The company knows about it but refuses to fix it because it would cost millions and hurt quarterly profits. The engineer faces losing their job and being blacklisted from the industry if they report it, but staying silent puts millions of users at risk.",
        domain="professional ethics",
        complexity_score=7.5,
        source="test",
        tags=["whistleblowing", "security"]
    )
    
    print("Testing transformer compatibility...\n")
    
    # Test all framings
    for framing in DeicticFraming:
        print(f"\n{framing.value.upper()} FRAMING:")
        print("-" * 50)
        
        # Test transform_dilemma (main method)
        question1 = transformer.transform_dilemma(dilemma, framing)
        print(f"transform_dilemma: {question1}")
        
        # Test get_transformation_prompt (backward compatibility)
        question2 = transformer.get_transformation_prompt(dilemma, framing)
        print(f"get_transformation_prompt: {question2}")
        
        # Test transform_dilemma_direct (backward compatibility)
        question3 = transformer.transform_dilemma_direct(dilemma, framing)
        print(f"transform_dilemma_direct: {question3}")
        
        # Verify all return the same direct question
        assert question1 == question2 == question3, "Methods should return the same question"
        
        # Verify it's a question (ends with ?)
        assert question1.endswith("?"), "Should be a question"
        
        # Verify no meta-instructions
        meta_words = ["reframe", "transform", "using", "language", "perspective"]
        assert not any(word in question1.lower() for word in meta_words), "Should not contain meta-instructions"
    
    # Test other methods
    print("\n\nTesting other methods:")
    print("-" * 50)
    
    # Test analyze_deictic_markers
    sample_response = "I think we should report this issue because it affects millions of users."
    markers = transformer.analyze_deictic_markers(sample_response)
    print(f"Deictic markers found: {sum(v for k, v in markers.items() if k != 'total_markers')} markers")
    
    # Test suggest_frame_type
    frame, confidence = transformer.suggest_frame_type(sample_response)
    print(f"Suggested frame: {frame.value} (confidence: {confidence:.2f})")
    
    # Test get_available_framings
    framings = transformer.get_available_framings()
    print(f"Available framings: {len(framings)}")
    
    # Test get_framing_description
    desc = transformer.get_framing_description(DeicticFraming.COSMOLOGICAL)
    print(f"Cosmological description: {desc}")
    
    # Test preview_transformation
    preview = transformer.preview_transformation(dilemma, DeicticFraming.SECOND_PERSON)
    print(f"\nPreview keys: {list(preview.keys())}")
    
    print("\n✅ All compatibility tests passed!")

if __name__ == "__main__":
    test_transformer_compatibility()