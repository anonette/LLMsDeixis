"""
Run expert analysis on Claude and DeepSeek responses
Uses the working expert analysis approach that was successful
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from deixis_analysis_pipeline.llm_agents.expert_analysis_agent import ExpertAnalysisAgent
from deixis_analysis_pipeline.llm_agents.critical_expert_analysis import CriticalExpertAnalyzer
from deixis_analysis_pipeline.llm_agents.evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from deixis_analysis_pipeline.llm_agents.pronoun_agency_expert import PronounAgencyExpert

async def run_expert_analysis_for_model(model_name: str, session_dir: Path):
    """Run expert analysis for a specific model's responses"""
    
    print(f"\n{'='*60}")
    print(f"EXPERT ANALYSIS FOR {model_name.upper()}")
    print(f"{'='*60}")
    print(f"Session: {session_dir.name}")
    
    # Initialize experts
    expert_agent = ExpertAnalysisAgent()
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("deixis_analysis_pipeline/automated_analysis_results") / f"{model_name}_expert_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_expert_analyses = []
    
    # Process each response file
    for response_file in session_dir.glob("*_responses.json"):
        dilemma_name = response_file.stem.replace("_responses", "")
        print(f"\n[PROCESSING] {dilemma_name}")
        
        with open(response_file, 'r', encoding='utf-8') as f:
            responses = json.load(f)
        
        # Analyze each framing
        for framing, data in responses.items():
            if isinstance(data, dict) and "response" in data and data["response"]:
                response_text = data["response"]
                question = data.get("question", "")
                
                print(f"  - {framing}: ", end="", flush=True)
                
                try:
                    # Run all expert analyses
                    expert_analysis = await expert_agent.analyze_response(
                        response_text, 
                        question, 
                        framing
                    )
                    
                    critical_analysis = await critical_expert.analyze_response(
                        response_text,
                        question,
                        framing
                    )
                    
                    evidence_analysis = await evidence_expert.analyze_response(
                        response_text,
                        question,
                        framing
                    )
                    
                    pronoun_analysis = await pronoun_expert.analyze_response(
                        response_text,
                        question,
                        framing
                    )
                    
                    # Combine all analyses
                    combined_analysis = {
                        "model": model_name,
                        "dilemma": dilemma_name,
                        "framing": framing,
                        "response_length": len(response_text),
                        "expert_analysis": expert_analysis,
                        "critical_analysis": critical_analysis,
                        "evidence_analysis": evidence_analysis,
                        "pronoun_agency_analysis": pronoun_analysis,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    all_expert_analyses.append(combined_analysis)
                    print("✓")
                    
                except Exception as e:
                    print(f"✗ Error: {str(e)}")
                    continue
    
    # Save results
    results_file = output_dir / "expert_analysis_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(all_expert_analyses, f, indent=2)
    
    # Generate summary report
    report = f"""# Expert Analysis Report - {model_name}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Session: {session_dir.name}

## Overview
- Total Responses Analyzed: {len(all_expert_analyses)}
- Model: {model_name}

## Key Findings

### Expert Agent Analysis
"""
    
    # Summarize key patterns
    ethical_frameworks = {}
    critical_issues = []
    evidence_patterns = []
    pronoun_patterns = {}
    
    for analysis in all_expert_analyses:
        # Count ethical frameworks
        if "expert_analysis" in analysis and "ethical_frameworks" in analysis["expert_analysis"]:
            for framework in analysis["expert_analysis"]["ethical_frameworks"]:
                ethical_frameworks[framework] = ethical_frameworks.get(framework, 0) + 1
        
        # Collect critical issues
        if "critical_analysis" in analysis and "critical_issues" in analysis["critical_analysis"]:
            critical_issues.extend(analysis["critical_analysis"]["critical_issues"])
        
        # Collect evidence patterns
        if "evidence_analysis" in analysis and "evidence_quality" in analysis["evidence_analysis"]:
            evidence_patterns.append(analysis["evidence_analysis"]["evidence_quality"])
        
        # Count pronoun patterns
        if "pronoun_agency_analysis" in analysis and "agency_distribution" in analysis["pronoun_agency_analysis"]:
            for agent, score in analysis["pronoun_agency_analysis"]["agency_distribution"].items():
                if agent not in pronoun_patterns:
                    pronoun_patterns[agent] = []
                pronoun_patterns[agent].append(score)
    
    # Add to report
    report += "\n#### Ethical Frameworks Used:\n"
    for framework, count in sorted(ethical_frameworks.items(), key=lambda x: x[1], reverse=True):
        report += f"- {framework}: {count} occurrences\n"
    
    report += "\n### Critical Analysis Highlights\n"
    unique_issues = list(set(critical_issues))[:5]
    for issue in unique_issues:
        report += f"- {issue}\n"
    
    report += "\n### Evidence-Based Analysis\n"
    if evidence_patterns:
        avg_evidence_quality = sum(evidence_patterns) / len(evidence_patterns)
        report += f"- Average Evidence Quality Score: {avg_evidence_quality:.2f}/10\n"
    
    report += "\n### Pronoun Agency Distribution\n"
    for agent, scores in pronoun_patterns.items():
        if scores:
            avg_score = sum(scores) / len(scores)
            report += f"- {agent}: {avg_score:.1f}% average agency\n"
    
    report += f"\n## Conclusion\n"
    report += f"The expert analysis reveals {model_name}'s distinctive approach to ethical reasoning, "
    report += f"with particular strengths in {list(ethical_frameworks.keys())[0] if ethical_frameworks else 'balanced frameworks'}.\n"
    
    # Save report
    report_file = output_dir / "expert_analysis_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[SUCCESS] Expert analysis complete for {model_name}")
    print(f"[OUTPUT] Results saved to: {output_dir}")
    
    return output_dir

async def main():
    """Run expert analysis for Claude and DeepSeek"""
    
    print("\n" + "="*60)
    print("EXPERT ANALYSIS FOR CLAUDE AND DEEPSEEK")
    print("="*60)
    
    # Define model sessions
    generation_logs_dir = Path("deixis_analysis_pipeline/generation_logs")
    
    models_to_analyze = {
        "claude": generation_logs_dir / "anthropic_claude_20250805_125046",
        "deepseek": generation_logs_dir / "deepseek_20250805_143544"
    }
    
    # Run analysis for each model
    for model_name, session_dir in models_to_analyze.items():
        if session_dir.exists():
            await run_expert_analysis_for_model(model_name, session_dir)
        else:
            print(f"\n[ERROR] Session directory not found for {model_name}: {session_dir}")
    
    print("\n" + "="*60)
    print("ALL EXPERT ANALYSES COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())