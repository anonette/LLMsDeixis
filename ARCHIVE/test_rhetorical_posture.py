"""Test script to verify rhetorical posture analysis JSON parsing."""

import asyncio
import json
from deixis_ethical_analyzer import DeicticEthicalAnalyzer

async def test_rhetorical_posture():
    """Test the rhetorical posture analysis function."""
    print("🧪 Testing rhetorical posture analysis...")
    
    # Initialize analyzer
    analyzer = DeicticEthicalAnalyzer()
    
    # Test response
    test_response = """
    You face a difficult moral choice here. You must weigh the immediate needs 
    of your family against the broader implications for society. Consider how 
    you would feel looking back on this decision years from now. What kind of 
    person do you want to be? The path forward requires careful deliberation 
    about your values and the legacy you wish to leave.
    """
    
    test_dilemma = "Should you report your brother's crime to the authorities?"
    
    try:
        # Test the analysis
        result = await analyzer.llm_agent.analyze_rhetorical_posture(
            test_response, 
            test_dilemma
        )
        
        print("\n✅ Analysis completed successfully!")
        print(f"📊 Result type: {type(result)}")
        print(f"🔍 Keys found: {list(result.keys())}")
        
        # Pretty print the result
        print("\n📝 Analysis Result:")
        print(json.dumps(result, indent=2))
        
        # Validate required fields
        required_fields = [
            "voice_authority_type",
            "voice_authority_score",
            "voice_authority_markers",
            "temporal_orientation",
            "temporal_orientation_score",
            "temporal_markers",
            "imagination_scope",
            "imagination_scope_score",
            "imagination_markers",
            "moral_subject_vision",
            "rhetorical_sophistication"
        ]
        
        missing_fields = [field for field in required_fields if field not in result]
        if missing_fields:
            print(f"\n⚠️ Missing fields: {missing_fields}")
        else:
            print("\n✅ All required fields present!")
            
        # Check data types
        print("\n🔍 Data type validation:")
        print(f"  - voice_authority_type: {type(result.get('voice_authority_type'))}")
        print(f"  - voice_authority_score: {type(result.get('voice_authority_score'))}")
        print(f"  - voice_authority_markers: {type(result.get('voice_authority_markers'))}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_rhetorical_posture())
    if success:
        print("\n🎉 Rhetorical posture analysis is working correctly!")
    else:
        print("\n❌ Rhetorical posture analysis needs further fixes.")