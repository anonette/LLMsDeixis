"""
Simple test script to verify the Deixis Ethical Analysis System
Tests core functionality without requiring API keys
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from transformer import DeicticTransformer, DeicticFraming
from models.schemas import EthicalDilemma
from deixis_ethical_analyzer import EthicalDilemmaDatabase
import json

def test_transformer():
    """Test the deictic transformer functionality."""
    print("=== Testing Deictic Transformer ===")
    
    transformer = DeicticTransformer()
    
    # Create test dilemma
    test_dilemma = EthicalDilemma(
        id="test_1",
        title="Test Dilemma",
        description="A person must choose between helping a friend who needs support and fulfilling a professional obligation that affects many people.",
        domain="test",
        complexity_score=5.0,
        source="test",
        tags=["test"]
    )
    
    print(f"Original dilemma: {test_dilemma.description}\n")
    
    # Test all framings
    framings = transformer.get_available_framings()
    print(f"Available framings: {len(framings)}")
    
    for framing in framings:
        transformed = transformer.transform_dilemma(test_dilemma, framing)
        print(f"\n{framing.value.upper()}:")
        print(f"Transformed: {transformed[:100]}...")
        
        # Test preview functionality
        preview = transformer.preview_transformation(test_dilemma, framing)
        print(f"Template: {preview['template_used'][:50]}...")
    
    print("\n✅ Transformer tests passed!")
    return True

def test_database():
    """Test the ethical dilemma database."""
    print("\n=== Testing Dilemma Database ===")
    
    db = EthicalDilemmaDatabase()
    dilemmas = db.get_all_dilemmas()
    
    print(f"Total dilemmas in database: {len(dilemmas)}")
    
    for dilemma in dilemmas:
        print(f"- {dilemma.title} (Domain: {dilemma.domain}, Complexity: {dilemma.complexity_score})")
        
        # Test retrieval
        retrieved = db.get_dilemma(dilemma.id)
        assert retrieved is not None, f"Failed to retrieve dilemma {dilemma.id}"
        assert retrieved.title == dilemma.title, "Retrieved dilemma doesn't match"
    
    # Test adding custom dilemma
    custom_dilemma = EthicalDilemma(
        id="custom_test",
        title="Custom Test Dilemma",
        description="A test dilemma for validation purposes.",
        domain="testing",
        complexity_score=1.0,
        source="test_suite",
        tags=["test", "validation"]
    )
    
    db.add_dilemma(custom_dilemma)
    retrieved_custom = db.get_dilemma("custom_test")
    assert retrieved_custom is not None, "Failed to add/retrieve custom dilemma"
    
    print("✅ Database tests passed!")
    return True

def test_deictic_analysis():
    """Test deictic marker analysis."""
    print("\n=== Testing Deictic Analysis ===")
    
    transformer = DeicticTransformer()
    
    # Test response with known markers
    test_response = """
    I believe that you should consider what we might do in this situation.
    Here and now, they must choose between different paths.
    This decision will affect those who come after us.
    """
    
    markers = transformer.analyze_deictic_markers(test_response)
    
    print("Deictic markers found:")
    for marker_type, count in markers.items():
        print(f"  {marker_type}: {count}")
    
    # Verify some expected results
    assert markers['first_person'] > 0, "Should detect first person markers"
    assert markers['second_person'] > 0, "Should detect second person markers"
    assert markers['third_person'] > 0, "Should detect third person markers"
    assert markers['spatial'] > 0, "Should detect spatial markers"
    assert markers['temporal'] > 0, "Should detect temporal markers"
    assert markers['total_markers'] > 0, "Should have total markers"
    
    print("✅ Deictic analysis tests passed!")
    return True

def test_export_functionality():
    """Test JSON export/import functionality."""
    print("\n=== Testing Export Functionality ===")
    
    db = EthicalDilemmaDatabase()
    dilemmas = db.get_all_dilemmas()
    
    # Test serialization
    serialized = [
        {
            'id': d.id,
            'title': d.title,
            'description': d.description,
            'domain': d.domain,
            'complexity_score': d.complexity_score,
            'source': d.source,
            'tags': d.tags
        }
        for d in dilemmas
    ]
    
    # Test JSON export
    test_filename = "test_export.json"
    with open(test_filename, 'w') as f:
        json.dump(serialized, f, indent=2)
    
    # Test JSON import
    with open(test_filename, 'r') as f:
        imported = json.load(f)
    
    assert len(imported) == len(dilemmas), "Import/export mismatch"
    
    # Cleanup
    Path(test_filename).unlink()
    
    print("✅ Export functionality tests passed!")
    return True

def run_all_tests():
    """Run all system tests."""
    print("🧪 Running Deixis Ethical Analysis System Tests\n")
    
    tests = [
        test_transformer,
        test_database,
        test_deictic_analysis,
        test_export_functionality
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} failed with error: {e}")
    
    print(f"\n🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Run: python demo_analysis.py")
        print("3. Explore the full functionality!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    run_all_tests()
