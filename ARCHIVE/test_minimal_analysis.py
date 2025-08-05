"""Minimal test to verify the system works"""
import asyncio
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from models.schemas import DeicticFraming

async def test_single_analysis():
    """Test analyzing one dilemma with one framework"""
    print("🧪 Testing minimal analysis...")
    
    # Initialize analyzer
    analyzer = DeicticEthicalAnalyzer()
    
    # Get first dilemma
    dilemmas = analyzer.get_dilemma_list()
    first_dilemma_id = dilemmas[0]['id']
    
    print(f"📋 Testing with dilemma: {first_dilemma_id}")
    print(f"🔄 Using framework: {DeicticFraming.IMPERSONAL.value}")
    
    # Test single framework analysis
    try:
        dilemma = analyzer.dilemma_db.get_dilemma(first_dilemma_id)
        result = await analyzer._analyze_single_framework(dilemma, DeicticFraming.IMPERSONAL)
        
        print("\n✅ Analysis completed successfully!")
        print(f"📊 Agency Analysis: {result.agency_analysis.primary_agent}")
        print(f"🧭 Ethical Framework: {result.ethical_framing_analysis.primary_framework}")
        print(f"📝 Response length: {result.response_length} chars")
        print(f"⏱️ Processing time: {result.processing_time:.2f}s")
        
        # Check if we got real values (not "unknown")
        if result.agency_analysis.primary_agent != "unknown":
            print("\n🎉 SUCCESS: Agency analysis returned real values!")
        else:
            print("\n⚠️ WARNING: Agency analysis still returning 'unknown'")
            
        if result.ethical_framing_analysis.primary_framework != "unknown":
            print("🎉 SUCCESS: Ethical framework analysis returned real values!")
        else:
            print("⚠️ WARNING: Ethical framework analysis still returning 'unknown'")
            
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_single_analysis())