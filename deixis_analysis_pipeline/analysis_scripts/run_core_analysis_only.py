#!/usr/bin/env python3
"""
Simplified analysis script that runs ONLY the core analysis.
This bypasses the problematic expert analysis modules.

Usage:
    python analysis_scripts/run_core_analysis_only.py
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import core modules
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from transformer import InterrogativeDeicticTransformer
from analysis_logger import RichAnalysisLogger

# Constants
GENERATION_LOGS_DIR = Path(__file__).parent.parent / "generation_logs"
OUTPUT_DIR = Path(__file__).parent.parent / "automated_analysis_results"

async def analyze_single_response(
    analyzer: DeicticEthicalAnalyzer,
    transformer: InterrogativeDeicticTransformer,
    response_data: Dict[str, Any],
    dilemma_id: str
) -> Dict[str, Any]:
    """Analyze a single response with core analysis only."""
    
    framing_type = response_data['framing_type']
    llm_response = response_data['response']
    
    print(f"\n🔍 Analyzing {framing_type.upper()} response...")
    print(f"  📝 Response length: {len(llm_response)} characters")
    
    # Core analysis
    agent_result = await analyzer.identify_primary_agent(llm_response)
    print(f"  👤 Primary agent: {agent_result['primary_agent']}")
    
    framework_result = await analyzer.detect_ethical_framework(llm_response)
    print(f"  [ETHICS] Ethical framework: {framework_result['framework']}")
    
    voice_result = await analyzer.analyze_voice_authority(llm_response)
    print(f"  🎭 Voice authority: {voice_result['voice_type']}")
    
    reasoning_result = await analyzer.analyze_moral_reasoning(llm_response)
    print(f"  🧠 Moral reasoning: {reasoning_result['reasoning_type']}")
    
    stance_result = await analyzer.analyze_affective_stance(llm_response)
    print(f"  💭 Affective stance: {stance_result['stance_type']}")
    
    coherence_result = await analyzer.assess_indexical_coherence(llm_response)
    print(f"  📝 Indexical coherence: {coherence_result['coherence_level']}")
    
    # Deictic marker analysis
    deictic_markers = transformer.extract_deictic_markers(llm_response)
    
    return {
        'dilemma_id': dilemma_id,
        'framing_type': framing_type,
        'response_length': len(llm_response),
        'primary_agent': agent_result['primary_agent'],
        'ethical_framework': framework_result['framework'],
        'voice_authority': voice_result['voice_type'],
        'moral_reasoning': reasoning_result['reasoning_type'],
        'affective_stance': stance_result['stance_type'],
        'indexical_coherence': coherence_result['coherence_level'],
        'deictic_markers': deictic_markers,
        'total_markers': sum(deictic_markers.values()),
        'llm_response': llm_response[:500] + '...' if len(llm_response) > 500 else llm_response
    }

async def main():
    """Run core analysis only on the latest generation logs."""
    
    print("[CORE ANALYSIS] SIMPLIFIED DEIXIS ANALYSIS")
    print("=" * 60)
    print("[INFO] Running core analysis only (no expert modules)")
    print("[INFO] This avoids the parsing errors in expert analysis")
    print("=" * 60)
    
    # Find latest session
    if not GENERATION_LOGS_DIR.exists():
        print(f"[ERROR] Generation logs directory not found: {GENERATION_LOGS_DIR}")
        return
    
    session_dirs = [d for d in GENERATION_LOGS_DIR.iterdir() if d.is_dir()]
    if not session_dirs:
        print("[ERROR] No session directories found")
        return
    
    latest_session = max(session_dirs, key=lambda d: d.stat().st_mtime)
    print(f"\n[OK] Using session: {latest_session.name}")
    
    # Find response files
    response_files = list(latest_session.glob("*_responses.json"))
    response_files = [f for f in response_files if f.name != "complete_session_data.json"]
    
    if not response_files:
        print("[ERROR] No response files found")
        return
    
    print(f"📄 Found {len(response_files)} response files")
    
    # Initialize analyzers
    analyzer = DeicticEthicalAnalyzer()
    transformer = InterrogativeDeicticTransformer()
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUT_DIR / f"core_analysis_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all responses
    all_results = []
    
    for response_file in response_files:
        dilemma_id = response_file.stem.replace("_responses", "")
        print(f"\n📖 Processing: {response_file.name}")
        
        with open(response_file, 'r', encoding='utf-8') as f:
            responses_data = json.load(f)
        
        print(f"[OK] Loaded {len(responses_data)} responses")
        
        # Analyze each response
        for response_data in responses_data:
            result = await analyze_single_response(
                analyzer, transformer, response_data, dilemma_id
            )
            all_results.append(result)
    
    print(f"\n🎉 Core analysis complete! Processed {len(all_results)} responses")
    
    # Save results
    # CSV format
    df = pd.DataFrame(all_results)
    csv_path = output_dir / "core_analysis_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n📊 Saved CSV: {csv_path}")
    
    # JSON format
    json_path = output_dir / "core_analysis_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    print(f"📄 Saved JSON: {json_path}")
    
    # Summary statistics
    print("\n📈 SUMMARY STATISTICS")
    print("=" * 40)
    print(f"Total responses analyzed: {len(all_results)}")
    print(f"Dilemmas processed: {len(response_files)}")
    print(f"Output directory: {output_dir}")
    
    # Framework distribution
    frameworks = df['ethical_framework'].value_counts()
    print("\n🎯 Ethical Framework Distribution:")
    for framework, count in frameworks.items():
        print(f"  - {framework}: {count} ({count/len(df)*100:.1f}%)")
    
    # Framing type distribution
    framings = df['framing_type'].value_counts()
    print("\n📐 Framing Type Distribution:")
    for framing, count in framings.items():
        print(f"  - {framing}: {count}")
    
    print("\n✅ CORE ANALYSIS COMPLETE!")
    print(f"Results saved to: {output_dir}")

if __name__ == "__main__":
    asyncio.run(main())