"""
Test script to verify model-specific analysis setup and run a quick test
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_setup():
    """Check if environment is properly configured."""
    print("Checking setup...")
    print("-" * 50)
    
    # Check for .env file
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("   Please create a .env file with your API keys")
        return False
    else:
        print("✓ .env file found")
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in .env")
        return False
    else:
        print("✓ OPENAI_API_KEY found")
    
    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY not found in .env")
        return False
    else:
        print("✓ OPENROUTER_API_KEY found")
    
    # Check if required files exist
    required_files = [
        "llm_client.py",
        "deixis_ethical_analyzer_single_model.py",
        "run_model_specific_analysis.py",
        "dilemma_generator.py",
        "pronoun_agency_analyzer.py",
        "ethical_consistency_analyzer.py",
        "final_report_generator.py",
        "transformer.py",
        "analysis_logger.py"
    ]
    
    print("\nChecking required files...")
    all_files_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"❌ {file} not found")
            all_files_exist = False
    
    return all_files_exist


async def run_quick_test():
    """Run a quick test with one dilemma and one model."""
    print("\nRunning quick test with GPT-4o and 1 dilemma...")
    print("-" * 50)
    
    try:
        from run_model_specific_analysis import ModelSpecificAnalysisRunner
        
        runner = ModelSpecificAnalysisRunner()
        
        # Generate one test dilemma
        test_dilemma = [{
            "id": "test_001",
            "title": "Whistleblower's Dilemma",
            "description": "You discover your company is dumping toxic waste. Reporting it would save the environment but cost hundreds of jobs including yours.",
            "domain": "professional_ethics",
            "complexity_score": 7.5,
            "source": "test",
            "tags": ["environment", "whistleblowing", "employment"]
        }]
        
        # Run analysis with just GPT-4o
        print("\nStarting analysis...")
        results = await runner.run_single_model_analysis(
            model_name="gpt-4o",
            dilemmas=test_dilemma,
            num_dilemmas=1
        )
        
        print("\n✓ Test completed successfully!")
        print(f"\nResults saved in: automated_analysis_results/gpt-4o/")
        
        # Show what was created
        output_dir = Path("automated_analysis_results/gpt-4o")
        if output_dir.exists():
            sessions = list(output_dir.glob("session_*"))
            if sessions:
                latest_session = sorted(sessions)[-1]
                print(f"\nSession directory: {latest_session}")
                print("\nFiles created:")
                for file in sorted(latest_session.iterdir()):
                    print(f"  - {file.name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_instructions():
    """Show instructions for running the full analysis."""
    print("\n" + "="*60)
    print("INSTRUCTIONS FOR RUNNING FULL ANALYSIS")
    print("="*60)
    
    print("\n1. To run analysis with ALL models (5 dilemmas each):")
    print("   python run_model_specific_analysis.py")
    
    print("\n2. To run with specific models:")
    print("   python run_model_specific_analysis.py --models gpt-4o claude-3.5-sonnet")
    
    print("\n3. To run with custom number of dilemmas:")
    print("   python run_model_specific_analysis.py --num-dilemmas 10")
    
    print("\n4. To run a single model with 3 dilemmas:")
    print("   python run_model_specific_analysis.py --models gpt-4o --num-dilemmas 3")
    
    print("\nThe analysis will:")
    print("  • Generate ethical dilemmas")
    print("  • Run each model through all deictic framings")
    print("  • Analyze pronoun usage and agency distribution")
    print("  • Check ethical consistency")
    print("  • Generate individual and comparison reports")
    
    print("\nOutput will be saved in:")
    print("  automated_analysis_results/")
    print("    ├── MODEL_COMPARISON_[timestamp].md")
    print("    ├── gpt-4o/session_[timestamp]/")
    print("    ├── claude-3.5-sonnet/session_[timestamp]/")
    print("    └── deepseek-chat/session_[timestamp]/")
    
    print("\nLogs will show:")
    print("  • Progress for each dilemma")
    print("  • Which model is being used")
    print("  • Analysis steps being performed")
    print("  • File paths for generated reports")


async def main():
    """Main entry point."""
    print("Model-Specific Deixis Analysis Setup Checker")
    print("=" * 60)
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup incomplete. Please fix the issues above.")
        return
    
    print("\n✓ Setup looks good!")
    
    # Ask if user wants to run a test
    print("\nWould you like to run a quick test? (y/n): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        success = await run_quick_test()
        if success:
            show_instructions()
    else:
        show_instructions()


if __name__ == "__main__":
    asyncio.run(main())