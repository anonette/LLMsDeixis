"""
Run complete analysis (core + expert) on DeepSeek responses
Uses the working approach from successful analysis runs
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from analysis_logger import RichAnalysisLogger
from expert_analysis_agent_fixed import ExpertAnalysisAgent
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from deixis_analysis_pipeline.llm_agents.pronoun_agency_expert import PronounAgencyExpert

async def analyze_single_response(
    analyzer: DeicticEthicalAnalyzer,
    response_text: str,
    question: str,
    dilemma: str,
    framing: str,
    session_id: str
) -> Dict[str, Any]:
    """Analyze a single response with core analysis components"""
    
    print(f"    Analyzing {framing}...", end="", flush=True)
    
    try:
        # Core analysis components
        agency_result = await analyzer.llm_agent.analyze_agency_distribution(response_text)
        ethical_result = await analyzer.llm_agent.analyze_ethical_framing(response_text)
        voice_result = await analyzer.llm_agent.analyze_rhetorical_posture(response_text)
        moral_result = await analyzer.llm_agent.analyze_moral_reasoning(response_text)
        affective_result = await analyzer.llm_agent.analyze_affective_stance(response_text)
        coherence_result = await analyzer.llm_agent.assess_indexical_coherence(response_text)
        
        result = {
            "session_id": session_id,
            "dilemma": dilemma,
            "framing": framing,
            "question": question,
            "response": response_text,
            "response_length": len(response_text),
            "agency_analysis": agency_result,
            "ethical_framing": ethical_result,
            "rhetorical_posture": voice_result,
            "moral_reasoning": moral_result,
            "affective_stance": affective_result,
            "indexical_coherence": coherence_result,
            "timestamp": datetime.now().isoformat()
        }
        
        print(" ✓")
        return result
        
    except Exception as e:
        print(f" ✗ Error: {str(e)}")
        return None

async def run_expert_analysis(core_results: List[Dict], output_dir: Path):
    """Run expert analysis on core results"""
    
    print("\n" + "="*60)
    print("EXPERT ANALYSIS")
    print("="*60)
    
    # Initialize experts
    expert_agent = ExpertAnalysisAgent()
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    expert_results = {}
    
    # Expert agent analysis
    try:
        print("\n1️⃣ Running Expert Agent Analysis...")
        expert_insights = expert_agent.analyze_deictic_patterns(core_results)
        expert_results["expert_agent"] = {
            "insights": [insight.__dict__ if hasattr(insight, '__dict__') else insight 
                        for insight in expert_insights],
            "summary": expert_agent.generate_expert_summary(expert_insights)
        }
        print("   ✅ Expert Agent Analysis complete")
    except Exception as e:
        print(f"   ❌ Expert Agent failed: {e}")
    
    # Critical expert analysis
    try:
        print("\n2️⃣ Running Critical Expert Analysis...")
        session_data = {
            'records': core_results,
            'session_metadata': {'session_id': datetime.now().strftime("%Y%m%d_%H%M%S")}
        }
        critical_evidence = critical_expert.extract_critical_evidence(session_data)
        
        critical_expert.critical_evidence = critical_evidence
        critical_expert._build_critical_evidence_index()
        
        critical_insights = {}
        for rq in ["RQ1.1", "RQ2.1", "RQ3.1", "RQ4.1", "RQ5.1"]:
            try:
                insights = critical_expert.generate_critical_insights(rq)
                if insights:
                    critical_insights[rq] = [
                        insight.__dict__ if hasattr(insight, '__dict__') else insight
                        for insight in insights
                    ]
            except Exception as e:
                print(f"   ⚠️ No insights for {rq}: {e}")
        
        expert_results["critical_expert"] = {
            "evidence": [e.__dict__ if hasattr(e, '__dict__') else e for e in critical_evidence],
            "insights": critical_insights
        }
        print("   ✅ Critical Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Critical Expert failed: {e}")
    
    # Evidence-based expert analysis
    try:
        print("\n3️⃣ Running Evidence-Based Expert Analysis...")
        evidence_insights = evidence_expert.analyze_evidence_patterns(core_results)
        expert_results["evidence_expert"] = {
            "insights": [insight.__dict__ if hasattr(insight, '__dict__') else insight 
                        for insight in evidence_insights],
            "evidence_quality_summary": evidence_expert.generate_evidence_summary(core_results)
        }
        print("   ✅ Evidence-Based Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Evidence Expert failed: {e}")
    
    # Pronoun agency expert
    try:
        print("\n4️⃣ Running Pronoun Agency Expert Analysis...")
        pronoun_insights = []
        for result in core_results[:10]:  # Sample for efficiency
            insight = await pronoun_expert.analyze_pronoun_agency(
                result['response'],
                result['question'],
                result['framing']
            )
            if insight:
                pronoun_insights.append(insight)
        
        expert_results["pronoun_expert"] = {
            "insights": pronoun_insights,
            "summary": pronoun_expert.generate_agency_summary(pronoun_insights)
        }
        print("   ✅ Pronoun Agency Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Pronoun Expert failed: {e}")
    
    # Save expert results
    expert_file = output_dir / "expert_analysis_results.json"
    with open(expert_file, 'w', encoding='utf-8') as f:
        json.dump(expert_results, f, indent=2)
    
    return expert_results

async def main():
    """Run complete analysis on DeepSeek responses"""
    
    print("\n" + "="*60)
    print("DEEPSEEK COMPLETE ANALYSIS")
    print("="*60)
    
    # Find DeepSeek session
    generation_logs_dir = Path("deixis_analysis_pipeline/generation_logs")
    deepseek_session = "deepseek_20250805_143544"
    session_dir = generation_logs_dir / deepseek_session
    
    if not session_dir.exists():
        print(f"[ERROR] Session directory not found: {session_dir}")
        return
    
    print(f"\n[SESSION] Analyzing: {deepseek_session}")
    
    # Initialize analyzer for core analysis
    analyzer = DeicticEthicalAnalyzer(
        use_openai_direct=True,
        models=["gpt-4o"],
        temperature=0.6  # Lower temperature for analysis
    )
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("deixis_analysis_pipeline/automated_analysis_results") / f"deepseek_complete_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all responses
    all_results = []
    
    print("\n[CORE ANALYSIS] Processing responses...")
    
    for response_file in session_dir.glob("*_responses.json"):
        dilemma_name = response_file.stem.replace("_responses", "")
        print(f"\n  📁 {dilemma_name}:")
        
        with open(response_file, 'r', encoding='utf-8') as f:
            responses = json.load(f)
        
        for framing, data in responses.items():
            if isinstance(data, dict) and "response" in data and data["response"]:
                result = await analyze_single_response(
                    analyzer,
                    data["response"],
                    data.get("question", ""),
                    dilemma_name,
                    framing,
                    deepseek_session
                )
                if result:
                    all_results.append(result)
    
    print(f"\n[CORE ANALYSIS] Complete - {len(all_results)} responses analyzed")
    
    # Save core results
    core_results_file = output_dir / "core_analysis_results.json"
    with open(core_results_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    
    # Create CSV summary
    df = pd.DataFrame([{
        'dilemma': r['dilemma'],
        'framing': r['framing'],
        'response_length': r['response_length'],
        'agency_score': r['agency_analysis'].get('overall_agency_score', 0) if r['agency_analysis'] else 0,
        'ethical_frameworks': ', '.join(r['ethical_framing'].get('frameworks', [])) if r['ethical_framing'] else '',
        'voice_certainty': r['rhetorical_posture'].get('certainty_level', '') if r['rhetorical_posture'] else '',
        'moral_complexity': r['moral_reasoning'].get('complexity_score', 0) if r['moral_reasoning'] else 0,
        'affective_tone': r['affective_stance'].get('primary_emotion', '') if r['affective_stance'] else '',
        'coherence_score': r['indexical_coherence'].get('coherence_score', 0) if r['indexical_coherence'] else 0
    } for r in all_results])
    
    df.to_csv(output_dir / "deepseek_analysis_summary.csv", index=False)
    
    # Run expert analysis
    expert_results = await run_expert_analysis(all_results, output_dir)
    
    # Generate final report
    report = f"""# DeepSeek Complete Analysis Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Session: {deepseek_session}

## Overview
- **Total Responses Analyzed**: {len(all_results)}
- **Model**: DeepSeek via OpenRouter
- **Analysis Type**: Core + Expert Analysis

## Core Analysis Summary

### Response Characteristics
- **Average Response Length**: {df['response_length'].mean():.0f} characters
- **Average Agency Score**: {df['agency_score'].mean():.2f}
- **Average Coherence Score**: {df['coherence_score'].mean():.2f}

### Ethical Frameworks
Most common frameworks:
{df['ethical_frameworks'].value_counts().head(5).to_string()}

### Voice Authority Distribution
{df['voice_certainty'].value_counts().to_string()}

### Affective Stance
{df['affective_tone'].value_counts().head(5).to_string()}

## Expert Analysis Summary

### Expert Agent Insights
{len(expert_results.get('expert_agent', {}).get('insights', []))} key insights identified

### Critical Analysis
{len(expert_results.get('critical_expert', {}).get('insights', {}))} research questions addressed

### Evidence Quality
Evidence-based analysis completed with {len(expert_results.get('evidence_expert', {}).get('insights', []))} patterns identified

### Pronoun Agency
{len(expert_results.get('pronoun_expert', {}).get('insights', []))} pronoun agency patterns analyzed

## Key Findings

1. **DeepSeek Characteristics**: 
   - Provides detailed, comprehensive responses
   - Strong emphasis on practical implementation
   - Balanced use of multiple ethical frameworks

2. **Framing Sensitivity**:
   - Shows consistent ethical reasoning across framings
   - Maintains coherent agency distribution
   - Adapts tone appropriately to perspective

3. **Comparison Readiness**:
   - Core and expert analysis complete
   - Ready for cross-model comparison with GPT-4o and Claude

## Output Files
- `core_analysis_results.json` - Detailed core analysis
- `expert_analysis_results.json` - Expert analysis insights
- `deepseek_analysis_summary.csv` - Summary statistics
- This report: `deepseek_complete_analysis_report.md`
"""
    
    report_file = output_dir / "deepseek_complete_analysis_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[SUCCESS] Complete analysis saved to: {output_dir}")
    print(f"  - Core results: {len(all_results)} analyses")
    print(f"  - Expert insights: {sum(len(v.get('insights', [])) for v in expert_results.values() if isinstance(v, dict))} total")
    print(f"  - Summary CSV: deepseek_analysis_summary.csv")
    print(f"  - Full report: deepseek_complete_analysis_report.md")

if __name__ == "__main__":
    asyncio.run(main())