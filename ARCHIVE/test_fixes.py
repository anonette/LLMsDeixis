#!/usr/bin/env python3
"""
Quick test script to verify the fixes for the deixis ethical analyzer
"""

import asyncio
import os
from deixis_ethical_analyzer import DeicticEthicalAnalyzer

async def test_analyzer():
    """Test the analyzer with a simple dilemma to verify fixes."""
    print("🧪 Testing Deixis Ethical Analyzer fixes...")
    
    # Check if API key is available
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ No OPENROUTER_API_KEY found in environment")
        return False
    
    try:
        # Initialize analyzer
        analyzer = DeicticEthicalAnalyzer(
            api_key=api_key,
            models=["openai/gpt-4o-mini"],  # Use a single, fast model for testing
            enable_rich_logging=True,
            output_dir="test_results"
        )
        print("✅ Analyzer initialized successfully")
        
        # Test with a single dilemma and framework
        print("🔍 Testing single analysis...")
        results = await analyzer.analyze_dilemma_across_frameworks("workplace_whistleblowing")
        
        if results:
            print(f"✅ Analysis completed successfully! Generated {len(results)} results")
            
            # Check if the results have the expected structure
            first_result = results[0]
            print(f"✅ Result structure: {type(first_result).__name__}")
            print(f"✅ Dilemma ID: {first_result.dilemma_id}")
            print(f"✅ Framing: {first_result.framing}")
            print(f"✅ Response length: {first_result.response_length}")
            
            # Finalize analysis to test logging
            summary = analyzer.finalize_and_save_analysis()
            if summary:
                print("✅ Analysis finalized and saved successfully")
            else:
                print("⚠️ Analysis finalization returned None")
            
            return True
        else:
            print("❌ No results generated")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test."""
    print("Starting test of deixis ethical analyzer fixes...")
    success = asyncio.run(test_analyzer())
    
    if success:
        print("\n🎉 All tests passed! The fixes appear to be working.")
    else:
        print("\n💥 Tests failed. There may still be issues to resolve.")

if __name__ == "__main__":
    main()