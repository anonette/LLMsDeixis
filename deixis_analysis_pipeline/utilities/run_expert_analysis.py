"""
EXPERT LLM AGENT ANALYSIS RUNNER
Runs the complete suite of expert LLM analyzers using the correct method names
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Import expert analyzers
from expert_analysis_agent import ExpertAnalysisAgent
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from pronoun_agency_expert import PronounAgencyExpert

async def run_complete_expert_analysis():
    """Run all expert LLM analyzers on the saved analysis results."""
    
    print("🔬 EXPERT LLM AGENT ANALYSIS SUITE")
    print("=" * 60)
    print("🤖 Advanced interpretation using multiple expert LLM agents")
    print("🎯 Deep qualitative analysis beyond core metrics")
    print("=" * 60)
    
    # Load the saved analysis results
    results_dir = Path("automated_analysis_results/complete_analysis_20250803_220710")
    results_file = results_dir / "complete_analysis_results.json"
    
    if not results_file.exists():
        print(f"❌ Analysis results file not found: {results_file}")
        return
    
    print(f"📖 Loading core analysis data from: {results_file}")
    
    with open(results_file, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    print(f"✅ Loaded analysis for {len(analysis_data.get('core_analysis', {}))} responses")
    
    # Initialize expert analyzers
    print(f"\n🤖 Initializing Expert LLM Agents...")
    
    expert_agent = ExpertAnalysisAgent()
    print("  ✅ Expert Analysis Agent (Claude-3.5-Sonnet)")
    
    critical_expert = CriticalExpertAnalyzer()
    print("  ✅ Critical Expert Analyzer (Rigorous evaluation)")
    
    evidence_expert = EvidenceBasedExpertAnalyzer()
    print("  ✅ Evidence-Based Expert Analyzer (Research-focused)")
    
    pronoun_expert = PronounAgencyExpert()
    print("  ✅ Pronoun Agency Expert (Linguistic specialist)")
    
    # Prepare session data format expected by experts
    session_data = {
        "session_id": "academic_integrity_analysis",
        "timestamp": datetime.now().isoformat(),
        "core_analysis": analysis_data.get("core_analysis", {}),
        "comparative_analysis": analysis_data.get("comparative_analysis", {}),
        "analysis_metadata": analysis_data.get("analysis_metadata", {})
    }
    
    expert_results = {}
    
    print(f"\n{'='*80}")
    print(f"RUNNING EXPERT LLM AGENT ANALYSIS")
    print(f"{'='*80}")
    
    # 1. Expert Analysis Agent
    print(f"\n🎓 Running Expert Analysis Agent...")
    try:
        expert_report = await expert_agent.analyze_session_data(session_data)
        expert_results["expert_agent"] = {
            "report": expert_report,
            "success": True,
            "method": "analyze_session_data"
        }
        print("  ✅ Expert Analysis Agent complete")
        
        # Save individual report
        expert_file = results_dir / "expert_analysis_report.json"
        with open(expert_file, 'w', encoding='utf-8') as f:
            json.dump(expert_report.__dict__ if hasattr(expert_report, '__dict__') else expert_report, 
                     f, indent=2, ensure_ascii=False, default=str)
        print(f"  📄 Saved: {expert_file}")
        
    except Exception as e:
        print(f"  ❌ Expert Analysis Agent failed: {e}")
        expert_results["expert_agent"] = {"error": str(e), "success": False}
    
    # 2. Critical Expert Analyzer
    print(f"\n🔍 Running Critical Expert Analyzer...")
    try:
        critical_evidence = critical_expert.extract_critical_evidence(session_data)
        print(f"  📊 Extracted {len(critical_evidence)} pieces of critical evidence")
        
        # Generate insights for key research questions
        research_questions = ["rq1_1", "rq2_1", "rq3_1"]  # Core deictic research questions
        critical_insights = {}
        
        for rq_id in research_questions:
            try:
                insights = critical_expert.generate_critical_insights(rq_id)
                critical_insights[rq_id] = insights
                print(f"  🧠 Generated {len(insights)} insights for {rq_id}")
            except Exception as e:
                print(f"  ⚠️ Failed to generate insights for {rq_id}: {e}")
        
        expert_results["critical_expert"] = {
            "evidence": critical_evidence,
            "insights": critical_insights,
            "success": True,
            "method": "extract_critical_evidence + generate_critical_insights"
        }
        print("  ✅ Critical Expert Analysis complete")
        
        # Save individual report
        critical_file = results_dir / "critical_expert_analysis.json"
        with open(critical_file, 'w', encoding='utf-8') as f:
            json.dump({
                "evidence": [ev.__dict__ if hasattr(ev, '__dict__') else ev for ev in critical_evidence],
                "insights": {k: [ins.__dict__ if hasattr(ins, '__dict__') else ins for ins in v] 
                           for k, v in critical_insights.items()},
                "evidence_count": len(critical_evidence),
                "insights_count": sum(len(v) for v in critical_insights.values())
            }, f, indent=2, ensure_ascii=False, default=str)
        print(f"  📄 Saved: {critical_file}")
        
    except Exception as e:
        print(f"  ❌ Critical Expert Analysis failed: {e}")
        expert_results["critical_expert"] = {"error": str(e), "success": False}
    
    # 3. Evidence-Based Expert Analyzer  
    print(f"\n📊 Running Evidence-Based Expert Analyzer...")
    try:
        logged_evidence = evidence_expert.extract_evidence_from_logs(session_data)
        print(f"  📋 Extracted {len(logged_evidence)} pieces of logged evidence")
        
        # Generate evidence-based insights
        research_questions = ["rq1_1", "rq2_1", "rq3_1", "rq4_1", "rq5_1"]
        evidence_insights = {}
        
        for rq_id in research_questions:
            try:
                insights = evidence_expert.generate_evidence_based_insights(rq_id)
                evidence_insights[rq_id] = insights
                print(f"  🔬 Generated {len(insights)} evidence-based insights for {rq_id}")
            except Exception as e:
                print(f"  ⚠️ Failed to generate evidence insights for {rq_id}: {e}")
        
        expert_results["evidence_expert"] = {
            "evidence": logged_evidence,
            "insights": evidence_insights,
            "success": True,
            "method": "extract_evidence_from_logs + generate_evidence_based_insights"
        }
        print("  ✅ Evidence-Based Expert Analysis complete")
        
        # Save individual report
        evidence_file = results_dir / "evidence_based_expert_analysis.json"
        with open(evidence_file, 'w', encoding='utf-8') as f:
            json.dump({
                "evidence": [ev.__dict__ if hasattr(ev, '__dict__') else ev for ev in logged_evidence],
                "insights": {k: [ins.__dict__ if hasattr(ins, '__dict__') else ins for ins in v] 
                           for k, v in evidence_insights.items()},
                "evidence_count": len(logged_evidence),
                "insights_count": sum(len(v) for v in evidence_insights.values())
            }, f, indent=2, ensure_ascii=False, default=str)
        print(f"  📄 Saved: {evidence_file}")
        
    except Exception as e:
        print(f"  ❌ Evidence-Based Expert Analysis failed: {e}")
        expert_results["evidence_expert"] = {"error": str(e), "success": False}
    
    # 4. Pronoun Agency Expert
    print(f"\n👤 Running Pronoun Agency Expert...")
    try:
        pronoun_report = await pronoun_expert.analyze_pronoun_agency(session_data)
        expert_results["pronoun_expert"] = {
            "report": pronoun_report,
            "success": True,
            "method": "analyze_pronoun_agency"
        }
        print("  ✅ Pronoun Agency Expert Analysis complete")
        
        # Save individual report
        pronoun_file = results_dir / "pronoun_agency_expert_analysis.json"
        with open(pronoun_file, 'w', encoding='utf-8') as f:
            json.dump(pronoun_report.__dict__ if hasattr(pronoun_report, '__dict__') else pronoun_report,
                     f, indent=2, ensure_ascii=False, default=str)
        print(f"  📄 Saved: {pronoun_file}")
        
        # Generate markdown report if available
        try:
            markdown_file = results_dir / "pronoun_agency_expert_report.md"
            pronoun_expert.generate_markdown_report(pronoun_report, str(markdown_file))
            print(f"  📄 Markdown report: {markdown_file}")
        except Exception as e:
            print(f"  ⚠️ Markdown report generation failed: {e}")
        
    except Exception as e:
        print(f"  ❌ Pronoun Agency Expert failed: {e}")
        expert_results["pronoun_expert"] = {"error": str(e), "success": False}
    
    # Save complete expert analysis results
    print(f"\n💾 Saving complete expert analysis results...")
    
    complete_expert_file = results_dir / "complete_expert_analysis_results.json"
    with open(complete_expert_file, 'w', encoding='utf-8') as f:
        json.dump({
            "expert_analysis_metadata": {
                "timestamp": datetime.now().isoformat(),
                "expert_agents_used": 4,
                "successful_analyses": sum(1 for result in expert_results.values() if result.get("success", False)),
                "failed_analyses": sum(1 for result in expert_results.values() if not result.get("success", False))
            },
            "expert_results": expert_results
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ Complete expert results: {complete_expert_file}")
    
    # Generate summary
    successful = sum(1 for result in expert_results.values() if result.get("success", False))
    failed = len(expert_results) - successful
    
    print(f"\n🎉 EXPERT ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"Expert Agents Run: {len(expert_results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Results Directory: {results_dir}")
    print("=" * 60)
    
    if successful > 0:
        print("📋 Generated Reports:")
        if expert_results.get("expert_agent", {}).get("success"):
            print("  🎓 expert_analysis_report.json")
        if expert_results.get("critical_expert", {}).get("success"):
            print("  🔍 critical_expert_analysis.json")
        if expert_results.get("evidence_expert", {}).get("success"):
            print("  📊 evidence_based_expert_analysis.json")
        if expert_results.get("pronoun_expert", {}).get("success"):
            print("  👤 pronoun_agency_expert_analysis.json")
            print("  👤 pronoun_agency_expert_report.md")
        print("  💾 complete_expert_analysis_results.json")
    
    print(f"\n✨ Expert LLM Agent Analysis provides deep qualitative insights")
    print(f"beyond the core quantitative analysis!")
    
    return expert_results

if __name__ == "__main__":
    asyncio.run(run_complete_expert_analysis()) 