#!/usr/bin/env python3
"""
INTEGRATED COMPLETE DEIXIS ANALYSIS RUNNER
Combines core analysis with properly integrated expert analysis
"""

import asyncio
import json
import csv
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging
from collections import defaultdict, Counter
import re

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Core imports
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from transformer import DeicticFraming
from analysis_logger import RichAnalysisLogger

# Expert imports
from expert_analysis_agent_fixed import ExpertAnalysisAgent
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from deixis_analysis_pipeline.llm_agents.pronoun_agency_expert import PronounAgencyExpert
from deixis_analysis_pipeline.llm_agents.expert_analysis_agent import ExpertAnalysisAgent as StandardExpertAgent
from research_framework_system import DeicticResearchFramework
from detailed_report_generator import DetailedReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
OUTPUT_DIR = Path("deixis_analysis_pipeline/automated_analysis_results")
GENERATION_LOGS_DIR = Path("deixis_analysis_pipeline/generation_logs")

def count_deictic_markers(text: str) -> Dict[str, int]:
    """Count deictic markers in text."""
    markers = {
        'first_person': len(re.findall(r'\b(I|me|my|mine|myself)\b', text, re.IGNORECASE)),
        'second_person': len(re.findall(r'\b(you|your|yours|yourself)\b', text, re.IGNORECASE)),
        'third_person': len(re.findall(r'\b(he|she|it|they|him|her|them|his|hers|its|their)\b', text, re.IGNORECASE)),
        'spatial': len(re.findall(r'\b(here|there|where|near|far|above|below)\b', text, re.IGNORECASE)),
        'temporal': len(re.findall(r'\b(now|then|when|today|tomorrow|yesterday|soon|later)\b', text, re.IGNORECASE)),
        'demonstrative': len(re.findall(r'\b(this|that|these|those)\b', text, re.IGNORECASE))
    }
    return markers

async def analyze_single_response(
    analyzer: DeicticEthicalAnalyzer,
    dilemma_id: str,
    framing: str,
    llm_response: str,
    deictic_question: str,
    response_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze a single response with core analysis."""
    
    print(f"\n🔍 Analyzing {framing.upper()} response...")
    print(f"  📝 Response length: {len(llm_response)} characters")
    
    # Agency analysis
    agency_result = await analyzer.llm_agent.analyze_agency_distribution(llm_response)
    print(f"  👤 Primary agent: {agency_result.primary_agent}")
    
    # Ethical framing analysis
    framing_result = await analyzer.llm_agent.analyze_ethical_framing(llm_response)
    print(f"  [ETHICS] Ethical framework: {framing_result.primary_framework}")
    
    # Rhetorical posture analysis
    voice_result = await analyzer.llm_agent.analyze_rhetorical_posture(llm_response)
    print(f"  🎭 Voice authority: {voice_result.get('voice_authority_type', 'unknown')}")
    
    # Moral reasoning analysis
    reasoning_result = await analyzer.llm_agent.analyze_moral_reasoning(llm_response)
    print(f"  🧠 Moral reasoning: {reasoning_result.get('reasoning_type', 'unknown')}")
    
    # Affective stance analysis
    stance_result = await analyzer.llm_agent.analyze_affective_stance(llm_response)
    print(f"  💭 Affective stance: {stance_result.get('stance_type', 'unknown')}")
    
    # Indexical coherence
    coherence_result = await analyzer.llm_agent.assess_indexical_coherence(llm_response)
    print(f"  📝 Indexical coherence: {coherence_result.get('coherence_level', 0.0)}")
    
    # Count deictic markers
    deictic_markers = count_deictic_markers(llm_response)
    
    # Compile results
    return {
        'dilemma_id': dilemma_id,
        'framing': framing,
        'response_length': len(llm_response),
        'primary_agent': agency_result.primary_agent,
        'agency_distribution': agency_result.agency_distribution,
        'decision_locus': agency_result.decision_locus,
        'collective_vs_individual': agency_result.collective_vs_individual,
        'primary_framework': framing_result.primary_framework,
        'ethical_reasoning_type': framing_result.ethical_reasoning_type,
        'moral_considerations': framing_result.moral_considerations,
        'consequence_vs_duty': framing_result.consequence_vs_duty,
        'voice_authority_type': voice_result.get('voice_authority_type', 'unknown'),
        'temporal_orientation': voice_result.get('temporal_orientation', 'unknown'),
        'imagination_scope': voice_result.get('imagination_scope', 'unknown'),
        'moral_reasoning': reasoning_result.get('reasoning_type', 'unknown'),
        'reasoning_confidence': reasoning_result.get('confidence_score', 0.0),
        'affective_stance': stance_result.get('stance_type', 'unknown'),
        'stance_confidence': stance_result.get('confidence_score', 0.0),
        'indexical_coherence': coherence_result.get('coherence_level', 0.0),
        'coherence_score': coherence_result.get('confidence_score', 0.0),
        'deictic_markers': deictic_markers,
        'total_markers': sum(deictic_markers.values()),
        'llm_response': llm_response,
        'deictic_question': deictic_question,
        'model': response_metadata.get('model', 'unknown'),
        'temperature': response_metadata.get('temperature', 0.0),
        'generation_time': response_metadata.get('generation_time', 0.0)
    }

async def run_expert_analysis(core_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run expert analysis on core results using the working approach."""
    
    print("\n" + "="*80)
    print("EXPERT ANALYSIS - Advanced interpretation")
    print("="*80)
    
    # Initialize expert analyzers
    expert_agent = ExpertAnalysisAgent()
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    expert_results = {}
    
    # Expert agent analysis
    try:
        print("\n1️⃣ Running Expert Agent Analysis...")
        expert_results["expert_agent"] = await expert_agent.analyze_session_data(core_results)
        print("   ✅ Expert Agent Analysis complete")
    except Exception as e:
        print(f"   ❌ Expert Agent failed: {e}")
        logger.error(f"Expert agent error: {e}")
        expert_results["expert_agent"] = {"error": str(e)}
    
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
                print(f"   ✅ Generated insights for {rq}")
            except Exception as e:
                logger.warning(f"Failed to generate critical insights for {rq}: {e}")
        
        expert_results["critical_expert"] = {
            "evidence": [e.__dict__ if hasattr(e, '__dict__') else e for e in critical_evidence],
            "insights": critical_insights
        }
        print("   ✅ Critical Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Critical Expert failed: {e}")
        logger.error(f"Critical expert error: {e}")
        expert_results["critical_expert"] = {"error": str(e)}
    
    # Evidence-based expert analysis
    try:
        print("\n3️⃣ Running Evidence-Based Expert Analysis...")
        evidence_data = evidence_expert.extract_evidence(session_data)
        evidence_expert.evidence_base = evidence_data
        evidence_expert._build_evidence_index()
        
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
        
        expert_results["evidence_expert"] = {
            "evidence": [e.__dict__ if hasattr(e, '__dict__') else e for e in evidence_data],
            "insights": evidence_insights
        }
        print("   ✅ Evidence-Based Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Evidence Expert failed: {e}")
        logger.error(f"Evidence expert error: {e}")
        expert_results["evidence_expert"] = {"error": str(e)}
    
    # Pronoun agency expert
    try:
        print("\n4️⃣ Running Pronoun Agency Expert Analysis...")
        pronoun_results = await pronoun_expert.analyze_session_data(core_results)
        expert_results["pronoun_expert"] = pronoun_results
        print("   ✅ Pronoun Agency Expert Analysis complete")
    except Exception as e:
        print(f"   ❌ Pronoun Expert failed: {e}")
        logger.error(f"Pronoun expert error: {e}")
        expert_results["pronoun_expert"] = {"error": str(e)}
    
    return expert_results

async def run_comprehensive_analysis_on_responses(all_responses: List[Dict], output_dir: Path) -> Dict[str, Any]:
    """Run comprehensive analysis on all responses."""
    
    # Initialize analyzer
    analyzer = DeicticEthicalAnalyzer(
        use_openai_direct=True,
        temperature=0.6,
        enable_rich_logging=True
    )
    
    print(f"\n[ANALYSIS] RUNNING COMPREHENSIVE ANALYSIS")
    print(f"[OUTPUT] Output directory: {output_dir}")
    print(f"[DATA] Processing {len(all_responses)} responses")
    
    # Core analysis
    print("\n" + "="*80)
    print(f"CORE ANALYSIS - Processing {len(all_responses)} responses")
    print("="*80)
    
    core_results = []
    for response_data in all_responses:
        try:
            result = await analyze_single_response(
                analyzer,
                response_data['dilemma_id'],
                response_data['framing'],
                response_data['response'],
                response_data['deictic_question'],
                response_data
            )
            core_results.append(result)
        except Exception as e:
            logger.error(f"Failed to analyze response: {e}")
            continue
    
    print(f"\n🎉 Core analysis complete! Processed {len(core_results)} responses")
    
    # Expert analysis
    expert_results = await run_expert_analysis(core_results)
    
    # Generate comparative analysis
    print("\n🔗 Generating comparative analysis...")
    comparative_analysis = generate_comparative_analysis(core_results)
    
    # Research framework analysis
    print("\n[RESEARCH] Research framework analysis...")
    try:
        research_framework = DeicticResearchFramework()
        research_analysis = research_framework.analyze_session_data({
            'core_results': core_results,
            'expert_results': expert_results
        })
        print("  [OK] Research framework analysis complete")
    except Exception as e:
        logger.error(f"Research framework analysis failed: {e}")
        research_analysis = {"error": str(e)}
    
    # Save all results
    print("\n💾 Saving analysis results...")
    
    # Save core results CSV
    csv_path = output_dir / "core_analysis_results.csv"
    save_to_csv(core_results, csv_path)
    print(f"  [OK] Core results CSV: {csv_path}")
    
    # Save core results JSON
    json_path = output_dir / "core_analysis_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(core_results, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Core results JSON: {json_path}")
    
    # Save expert analysis
    expert_path = output_dir / "expert_analysis_results.json"
    with open(expert_path, 'w', encoding='utf-8') as f:
        json.dump(expert_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"  [OK] Expert analysis: {expert_path}")
    
    # Save comparative analysis
    comparative_path = output_dir / "comparative_analysis.json"
    with open(comparative_path, 'w', encoding='utf-8') as f:
        json.dump(comparative_analysis, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Comparative analysis: {comparative_path}")
    
    # Save research framework
    research_path = output_dir / "research_framework_analysis.json"
    with open(research_path, 'w', encoding='utf-8') as f:
        json.dump(research_analysis, f, indent=2, ensure_ascii=False, default=str)
    print(f"  [OK] Research framework: {research_path}")
    
    # Generate final report
    try:
        print("\n📄 Generating final report...")
        report_generator = DetailedReportGenerator()
        report_path = output_dir / "FINAL_DEIXIS_RESEARCH_REPORT.md"
        
        # Create report data
        report_data = {
            'core_results': core_results,
            'expert_results': expert_results,
            'comparative_analysis': comparative_analysis,
            'research_analysis': research_analysis,
            'metadata': {
                'total_responses': len(core_results),
                'timestamp': datetime.now().isoformat(),
                'models_used': list(set(r.get('model', 'unknown') for r in core_results))
            }
        }
        
        # Generate markdown report
        report_content = generate_markdown_report(report_data)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"  [OK] Final report: {report_path}")
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        print(f"  [WARNING] Report generation failed: {e}")
    
    return {
        'core_results': core_results,
        'expert_results': expert_results,
        'comparative_analysis': comparative_analysis,
        'research_analysis': research_analysis
    }

def generate_comparative_analysis(core_results: List[Dict]) -> Dict[str, Any]:
    """Generate comparative analysis across framings."""
    
    # Group by framing
    by_framing = defaultdict(list)
    for result in core_results:
        by_framing[result['framing']].append(result)
    
    comparative = {}
    for framing, results in by_framing.items():
        comparative[framing] = {
            'count': len(results),
            'avg_length': sum(r['response_length'] for r in results) / len(results),
            'primary_agents': Counter(r['primary_agent'] for r in results).most_common(3),
            'ethical_frameworks': Counter(r['primary_framework'] for r in results).most_common(3),
            'voice_types': Counter(r['voice_authority_type'] for r in results).most_common(3),
            'avg_markers': sum(r['total_markers'] for r in results) / len(results)
        }
    
    return comparative

def save_to_csv(results: List[Dict], filepath: Path):
    """Save results to CSV."""
    if not results:
        return
    
    # Flatten nested dictionaries
    flattened = []
    for result in results:
        flat = {}
        for key, value in result.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flat[f"{key}_{sub_key}"] = sub_value
            elif isinstance(value, list):
                flat[key] = str(value)
            else:
                flat[key] = value
        flattened.append(flat)
    
    # Write CSV
    keys = flattened[0].keys()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(flattened)

def generate_markdown_report(report_data: Dict) -> str:
    """Generate a markdown report from analysis data."""
    
    report = f"""# Deixis Analysis Research Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report presents the comprehensive analysis of ethical responses across different deictic framings.

### Key Statistics
- **Total Responses Analyzed**: {report_data['metadata']['total_responses']}
- **Models Used**: {', '.join(report_data['metadata']['models_used'])}
- **Analysis Timestamp**: {report_data['metadata']['timestamp']}

## Core Analysis Results

### Response Characteristics by Framing

"""
    
    # Add comparative analysis
    if 'comparative_analysis' in report_data:
        for framing, stats in report_data['comparative_analysis'].items():
            report += f"\n#### {framing.upper()}\n"
            report += f"- Average Response Length: {stats['avg_length']:.0f} characters\n"
            report += f"- Average Deictic Markers: {stats['avg_markers']:.1f}\n"
            report += f"- Top Agents: {', '.join([f'{agent[0]} ({agent[1]})' for agent in stats['primary_agents']])}\n"
            report += f"- Top Frameworks: {', '.join([f'{fw[0]} ({fw[1]})' for fw in stats['ethical_frameworks']])}\n"
    
    # Add expert insights
    report += "\n## Expert Analysis Insights\n"
    
    if 'expert_results' in report_data:
        for expert_type, results in report_data['expert_results'].items():
            if isinstance(results, dict) and 'error' not in results:
                report += f"\n### {expert_type.replace('_', ' ').title()}\n"
                if 'insights' in results:
                    for rq, insights in results.get('insights', {}).items():
                        if insights:
                            report += f"\n**{rq}**:\n"
                            for insight in insights[:2]:  # Limit to first 2 insights
                                if isinstance(insight, dict):
                                    report += f"- {insight.get('insight_text', 'No text available')}\n"
    
    report += "\n## Conclusions\n\n"
    report += "The analysis reveals systematic patterns in how deictic framing influences ethical reasoning and discourse structure.\n"
    
    return report

def load_response_files(session_dir: Path) -> List[Dict[str, Any]]:
    """Load all response files from a session directory."""
    all_responses = []
    
    response_files = list(session_dir.glob("*_responses.json"))
    print(f"[FILES] Found {len(response_files)} response files:")
    for f in response_files:
        print(f"  - {f.name}")
    
    for file_path in response_files:
        print(f"\n📖 Processing: {file_path.name}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract responses
            dilemma_id = data['dilemma_id']
            dilemma_title = data['dilemma_title']
            
            responses = data.get('responses', {})
            print(f"[OK] Extracted {len(responses)} response framings:")
            
            for framing, response_data in responses.items():
                print(f"  - {framing}")
                if 'error' not in response_data and 'response' in response_data:
                    all_responses.append({
                        'dilemma_id': dilemma_id,
                        'dilemma_title': dilemma_title,
                        'framing': framing,
                        'response': response_data['response'],
                        'deictic_question': response_data.get('deictic_question', ''),
                        'model': data.get('model', 'unknown'),
                        'temperature': data.get('temperature', 0.0),
                        'generation_time': response_data.get('generation_time', 0.0)
                    })
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            continue
    
    return all_responses

async def main():
    """Main function."""
    print("[ANALYSIS] INTEGRATED COMPLETE DEIXIS ANALYSIS RUNNER")
    print("="*80)
    print("[AUTO] Automated analysis of generation logs with integrated expert analysis")
    print("[TOOLS] Core analysis + Working expert analysis approach")
    print("[OUTPUT] Generates: CSV, JSON, Reports, Research Framework")
    print("="*80)
    
    # Find latest session
    print(f"\n[SCAN] Scanning: {GENERATION_LOGS_DIR}")
    if not GENERATION_LOGS_DIR.exists():
        print("[ERROR] Generation logs directory not found!")
        return
    
    session_dirs = [d for d in GENERATION_LOGS_DIR.iterdir() if d.is_dir()]
    if not session_dirs:
        print("[ERROR] No session directories found!")
        return
    
    # Sort by modification time
    session_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    print(f"[DIRS] Found {len(session_dirs)} session directories:")
    for i, d in enumerate(session_dirs[:5]):
        print(f"  {i+1}. {d.name}")
    
    # Use latest session
    latest_session = session_dirs[0]
    print(f"\n[OK] Using latest session: {latest_session.name}")
    
    # Load all response files
    all_responses = load_response_files(latest_session)
    
    if not all_responses:
        print("[ERROR] No valid responses found!")
        return
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUT_DIR / f"integrated_analysis_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run comprehensive analysis
    results = await run_comprehensive_analysis_on_responses(all_responses, output_dir)
    
    print("\n" + "="*80)
    print("🎉 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"📁 Results saved to: {output_dir}")
    print("📊 Files generated:")
    print("  - core_analysis_results.csv")
    print("  - core_analysis_results.json")
    print("  - expert_analysis_results.json")
    print("  - comparative_analysis.json")
    print("  - research_framework_analysis.json")
    print("  - FINAL_DEIXIS_RESEARCH_REPORT.md")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())