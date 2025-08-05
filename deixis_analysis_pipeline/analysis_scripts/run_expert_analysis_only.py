#!/usr/bin/env python3
"""
Run only the Expert Analysis on existing core analysis results.
This script loads previously generated core analysis results and runs expert analysis on them.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import expert modules
from expert_analysis_agent_fixed import ExpertAnalysisAgent
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from deixis_analysis_pipeline.llm_agents.pronoun_agency_expert import PronounAgencyExpert

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_expert_analysis_only(core_results_path: Path, output_dir: Path):
    """Run expert analysis on existing core results."""
    
    # Load core results
    print(f"\n📂 Loading core results from: {core_results_path}")
    with open(core_results_path, 'r', encoding='utf-8') as f:
        core_results = json.load(f)
    
    print(f"✅ Loaded {len(core_results)} analysis records")
    
    # Initialize expert analyzers
    print("\n🔧 Initializing expert analyzers...")
    expert_agent = ExpertAnalysisAgent()
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    print("\n" + "="*80)
    print("EXPERT ANALYSIS - Advanced interpretation")
    print("="*80)
    
    expert_results = {}
    
    # Expert agent analysis
    try:
        print("\n1️⃣ Running Expert Agent Analysis...")
        expert_results["expert_agent"] = await expert_agent.analyze_session_data(core_results)
        print("   ✅ Expert Agent Analysis complete")
    except Exception as e:
        print(f"   ❌ Expert Agent failed: {e}")
        logger.error(f"Expert agent error: {e}")
    
    # Critical expert analysis
    try:
        print("\n2️⃣ Running Critical Expert Analysis...")
        # Extract evidence first
        session_data = {
            'records': core_results,
            'session_metadata': {'session_id': datetime.now().strftime("%Y%m%d_%H%M%S")}
        }
        critical_evidence = critical_expert.extract_critical_evidence(session_data)
        
        # Build evidence index
        critical_expert.critical_evidence = critical_evidence
        critical_expert._build_critical_evidence_index()
        
        # Generate insights
        critical_insights = {}
        for rq in ["RQ1.1", "RQ2.1", "RQ3.1", "RQ4.1", "RQ5.1"]:
            try:
                insights = critical_expert.generate_critical_insights(rq)
                if insights:
                    critical_insights[rq] = [
                        insight.__dict__ if hasattr(insight, '__dict__') else insight
                        for insight in insights
                    ]
                print(f"   ✅ Generated insights for {rq}")
            except Exception as e:
                logger.warning(f"Failed to generate critical insights for {rq}: {e}")
                print(f"   ⚠️ No insights for {rq}")
        
        expert_results["critical_expert"] = {
            "evidence": [e.__dict__ if hasattr(e, '__dict__') else e for e in critical_evidence],
            "insights": critical_insights
        }
        print("   ✅ Critical Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Critical Expert failed: {e}")
        logger.error(f"Critical expert error: {e}")
    
    # Evidence-based expert analysis
    try:
        print("\n3️⃣ Running Evidence-Based Expert Analysis...")
        # Extract evidence
        evidence_based_evidence = evidence_expert.extract_evidence_from_logs(session_data)
        
        # Build evidence index
        evidence_expert.logged_evidence = evidence_based_evidence
        evidence_expert._build_evidence_index()
        
        # Generate insights
        evidence_insights = {}
        for rq in ["RQ1.1", "RQ2.1", "RQ3.1", "RQ4.1", "RQ5.1"]:
            try:
                insights = evidence_expert.generate_evidence_based_insights(rq)
                if insights:
                    evidence_insights[rq] = [
                        insight.__dict__ if hasattr(insight, '__dict__') else insight
                        for insight in insights
                    ]
                print(f"   ✅ Generated insights for {rq}")
            except Exception as e:
                logger.warning(f"Failed to generate evidence insights for {rq}: {e}")
                print(f"   ⚠️ No insights for {rq}")
        
        expert_results["evidence_expert"] = {
            "evidence": [e.__dict__ if hasattr(e, '__dict__') else e for e in evidence_based_evidence],
            "insights": evidence_insights
        }
        print("   ✅ Evidence-Based Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Evidence Expert failed: {e}")
        logger.error(f"Evidence expert error: {e}")
    
    # Pronoun expert analysis
    try:
        print("\n4️⃣ Running Pronoun Agency Expert Analysis...")
        # Group responses by framing type
        responses_by_framing = {}
        for result in core_results:
            framing = result.get('framing_type', 'unknown')
            if framing not in responses_by_framing:
                responses_by_framing[framing] = []
            responses_by_framing[framing].append(result)
        
        # Call with proper session data structure
        pronoun_analysis = await pronoun_expert.analyze_pronoun_agency({
            'records': core_results,
            'responses_by_framing': responses_by_framing,
            'session_metadata': {'session_id': datetime.now().strftime("%Y%m%d_%H%M%S")}
        })
        
        # Convert to serializable format
        if hasattr(pronoun_analysis, '__dict__'):
            expert_results["pronoun_expert"] = pronoun_analysis.__dict__
        else:
            expert_results["pronoun_expert"] = pronoun_analysis
            
        print("   ✅ Pronoun Agency Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Pronoun Expert failed: {e}")
        logger.error(f"Pronoun expert error: {e}")
    
    # Save expert analysis results
    print(f"\n💾 Saving expert analysis results...")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    expert_path = output_dir / "expert_analysis_results.json"
    with open(expert_path, 'w', encoding='utf-8') as f:
        json.dump(expert_results, f, indent=2, default=str)
    print(f"✅ Saved to: {expert_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("EXPERT ANALYSIS SUMMARY")
    print("="*80)
    for expert_name, results in expert_results.items():
        if isinstance(results, dict) and 'insights' in results:
            total_insights = sum(len(insights) for insights in results['insights'].values())
            print(f"✅ {expert_name}: {total_insights} insights generated")
        else:
            print(f"✅ {expert_name}: Analysis completed")
    
    return expert_results

async def main():
    """Main entry point for expert analysis runner."""
    
    print("🔬 EXPERT ANALYSIS ONLY RUNNER")
    print("="*60)
    print("Runs expert analysis on existing core analysis results")
    print("="*60)
    
    # Find existing core results
    results_dir = Path(__file__).parent.parent / "automated_analysis_results"
    
    # List available analysis sessions
    sessions = sorted([d for d in results_dir.iterdir() if d.is_dir()], 
                     key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not sessions:
        print("❌ No analysis sessions found!")
        return
    
    print(f"\n📁 Available analysis sessions:")
    for i, session in enumerate(sessions[:10], 1):  # Show last 10
        core_file = session / "core_analysis_results.json"
        if core_file.exists():
            print(f"  {i}. {session.name} {'✅' if core_file.exists() else '❌'}")
    
    # Use the most recent session with core results
    selected_session = None
    for session in sessions:
        core_file = session / "core_analysis_results.json"
        if core_file.exists():
            selected_session = session
            break
    
    if not selected_session:
        print("❌ No session with core_analysis_results.json found!")
        return
    
    print(f"\n✅ Using session: {selected_session.name}")
    core_results_path = selected_session / "core_analysis_results.json"
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = results_dir / f"expert_analysis_only_{timestamp}"
    
    # Run expert analysis
    await run_expert_analysis_only(core_results_path, output_dir)
    
    print(f"\n🎉 Expert analysis complete!")
    print(f"📁 Results saved to: {output_dir}")

if __name__ == "__main__":
    asyncio.run(main())
