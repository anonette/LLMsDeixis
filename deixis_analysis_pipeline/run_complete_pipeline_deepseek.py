"""
Run complete pipeline with DeepSeek model via OpenRouter
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from deixis_analysis_pipeline.generation_scripts.generate_responses_deepseek import main as generate_deepseek
from deixis_analysis_pipeline.analysis_scripts.run_complete_deixis_analysis_integrated import main as run_analysis

async def run_complete_pipeline():
    """Run generation and analysis pipeline with DeepSeek"""
    
    print("\n" + "="*80)
    print("DEIXIS ANALYSIS PIPELINE - DEEPSEEK VIA OPENROUTER")
    print("="*80)
    
    # Step 1: Generate responses with DeepSeek
    print("\n[STEP 1] GENERATING RESPONSES WITH DEEPSEEK")
    print("-"*80)
    
    try:
        output_dir = await generate_deepseek()
        print(f"\n[SUCCESS] Generation completed. Output directory: {output_dir}")
    except Exception as e:
        print(f"\n[ERROR] Generation failed: {e}")
        return
    
    # Step 2: Run integrated analysis
    print("\n[STEP 2] RUNNING INTEGRATED ANALYSIS")
    print("-"*80)
    
    try:
        await run_analysis()
        print("\n[SUCCESS] Analysis completed successfully")
    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {e}")
        return
    
    print("\n" + "="*80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(run_complete_pipeline())