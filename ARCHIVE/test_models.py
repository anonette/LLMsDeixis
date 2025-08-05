"""
Test Model Access Script
Quick test to verify GPT-4o, Claude 3.5 Sonnet, and DeepSeek are accessible
"""

import asyncio
import os
from deixis_ethical_analyzer import LLMAnalysisAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_model_access():
    """Test access to the three target models."""
    
    print("🧪 TESTING MODEL ACCESS")
    print("=" * 50)
    print()
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found in .env file")
        return False
    
    print(f"✅ OpenRouter API key found: {api_key[:10]}...")
    print()
    
    # Define target models
    target_models = [
        "openai/gpt-4o",
        "anthropic/claude-3.5-sonnet", 
        "deepseek/deepseek-chat"
    ]
    
    # Initialize LLM agent with target models
    try:
        llm_agent = LLMAnalysisAgent(api_key=api_key, models=target_models)
        print("✅ LLM agent initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize LLM agent: {e}")
        return False
    
    # Test each model with a simple prompt
    test_prompt = "Respond with just 'Hello from [model name]' to confirm you're working."
    
    print("🔄 Testing each model...")
    print()
    
    success_count = 0
    
    for i, model in enumerate(target_models, 1):
        try:
            print(f"   {i}. Testing {model}...")
            
            # Force the agent to use this specific model
            llm_agent.current_model_index = target_models.index(model)
            
            response = await llm_agent._make_llm_request(test_prompt)
            
            if response and not response.startswith("Error:"):
                print(f"      ✅ SUCCESS: {response.strip()[:50]}...")
                success_count += 1
            else:
                print(f"      ❌ FAILED: {response}")
                
        except Exception as e:
            print(f"      ❌ ERROR: {e}")
    
    print()
    print("📊 RESULTS:")
    print(f"   • Models tested: {len(target_models)}")
    print(f"   • Successful: {success_count}")
    print(f"   • Failed: {len(target_models) - success_count}")
    print()
    
    if success_count == len(target_models):
        print("🎉 ALL MODELS ACCESSIBLE! Ready to generate data.")
        print()
        print("Next step: Run the full analysis with:")
        print("   python generate_multi_model_data.py")
        return True
    else:
        print("⚠️  SOME MODELS FAILED. Check your OpenRouter account and model access.")
        print()
        print("Common issues:")
        print("   • Insufficient credits in OpenRouter account")
        print("   • Model not available in your region")
        print("   • API rate limits")
        return False

def main():
    """Run the model access test."""
    print("Testing access to GPT-4o, Claude 3.5 Sonnet, and DeepSeek...")
    print()
    
    success = asyncio.run(test_model_access())
    
    if success:
        print("✅ All systems ready for multi-model analysis!")
    else:
        print("❌ Fix the issues above before proceeding.")

if __name__ == "__main__":
    main()