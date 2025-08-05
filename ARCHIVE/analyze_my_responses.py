"""
Analyze Academic Integrity Responses - All 9 Deictic Framings
Process the specific responses file with comprehensive LLM-based and code-based analysis.
"""

import json
import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from pronoun_agency_analyzer import PronounAgencyAnalyzer

async def analyze_academic_integrity_responses():
    """Analyze the specific academic integrity responses file."""
    
    # Load your responses file
    responses_file = Path("generation_logs/academic_integrity_20250803_205333/academic_integrity_responses.json")
    
    if not responses_file.exists():
        print(f"❌ File not found: {responses_file}")
        return
    
    print("🔬 ANALYZING ACADEMIC INTEGRITY RESPONSES")
    print("=" * 60)
    print(f"📁 Source: {responses_file}")
    
    # Load the data
    with open(responses_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    responses = data["responses"]["responses"]
    print(f"✅ Found {len(responses)} deictic framings")
    
    # Initialize analyzers
    analyzer = DeicticEthicalAnalyzer(use_openai_direct=True, temperature=0.6)  # Lower temp for analysis
    pronoun_analyzer = PronounAgencyAnalyzer()
    
    analysis_results = {}
    
    for framing, response_data in responses.items():
        if "error" in response_data:
            print(f"  ❌ Skipping {framing} due to error")
            continue
        
        print(f"\n🔍 Analyzing {framing.upper()}...")
        
        response_text = response_data["response"]
        deictic_question = response_data["deictic_question"]
        
        # === 1. DEICTIC MARKER ANALYSIS (Code-based) ===
        deictic_markers = analyzer.transformer.analyze_deictic_markers(response_text)
        print(f"  📊 Deictic markers: {sum(deictic_markers.values())} total")
        
        # === 2. PRONOUN AGENCY ANALYSIS (Code-based) ===
        pronoun_analysis = pronoun_analyzer.analyze_text(
            response_text, 
            text_id=f"academic_integrity_{framing}",
            framing=framing
        )
        print(f"  🗣️ Pronouns: {pronoun_analysis.total_pronouns} total, agency={pronoun_analysis.agency_type}")
        
        # === 3. LLM-BASED ANALYSIS ===
        
        # Agency Distribution Analysis
        agency_analysis = await analyzer.llm_agent.analyze_agency_distribution(response_text)
        print(f"  👤 Primary agent: {agency_analysis.primary_agent}")
        
        # Ethical Framing Analysis  
        ethical_analysis = await analyzer.llm_agent.analyze_ethical_framing(response_text)
        print(f"  ⚖️ Ethical framework: {ethical_analysis.primary_framework}")
        
        # Rhetorical Posture Analysis
        rhetorical_analysis = await analyzer.llm_agent.analyze_rhetorical_posture(response_text)
        print(f"  🎭 Voice authority: {rhetorical_analysis.get('voice_authority_type', 'unknown')}")
        
        # Store comprehensive results
        analysis_results[framing] = {
            "framing_type": framing,
            "question_focus": response_data.get("framing_focus", ""),
            "response_length": len(response_text),
            "generation_time": response_data.get("generation_time_seconds", 0),
            
            # Deictic markers (code-based)
            "deictic_markers": deictic_markers,
            "total_deictic_markers": sum(deictic_markers.values()),
            
            # Pronoun analysis (code-based)
            "pronoun_analysis": {
                "total_pronouns": pronoun_analysis.total_pronouns,
                "agency_type": pronoun_analysis.agency_type,
                "agency_concentration": pronoun_analysis.agency_concentration,
                "first_singular_ratio": pronoun_analysis.first_singular_ratio,
                "second_person_ratio": pronoun_analysis.second_person_ratio,
                "first_plural_ratio": pronoun_analysis.first_plural_ratio,
                "third_person_ratio": pronoun_analysis.third_person_ratio,
                "impersonal_ratio": pronoun_analysis.impersonal_ratio
            },
            
            # LLM-based analysis
            "agency_analysis": {
                "primary_agent": agency_analysis.primary_agent,
                "agency_distribution": agency_analysis.agency_distribution,
                "decision_locus": agency_analysis.decision_locus,
                "collective_vs_individual": agency_analysis.collective_vs_individual
            },
            "ethical_analysis": {
                "primary_framework": ethical_analysis.primary_framework,
                "reasoning_type": ethical_analysis.ethical_reasoning_type,
                "consequence_vs_duty": ethical_analysis.consequence_vs_duty,
                "moral_considerations": ethical_analysis.moral_considerations
            },
            "rhetorical_analysis": rhetorical_analysis
        }
        
        # Brief delay between analyses
        await asyncio.sleep(1.0)
    
    # === COMPARATIVE ANALYSIS ===
    print(f"\n📈 GENERATING COMPARATIVE ANALYSIS...")
    
    comparative_insights = generate_comparative_analysis(analysis_results)
    
    # === SAVE RESULTS ===
    output_dir = responses_file.parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed analysis
    analysis_file = output_dir / f"comprehensive_analysis_{timestamp}.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump({
            "analysis_metadata": {
                "timestamp": datetime.now().isoformat(),
                "source_file": str(responses_file),
                "framings_analyzed": list(analysis_results.keys()),
                "total_framings": len(analysis_results)
            },
            "individual_analyses": analysis_results,
            "comparative_insights": comparative_insights
        }, f, indent=2, ensure_ascii=False, default=str)
    
    # Generate CSV for statistical analysis
    csv_file = output_dir / f"deictic_metrics_{timestamp}.csv"
    generate_csv_analysis(analysis_results, csv_file)
    
    # Generate readable report
    report_file = output_dir / f"analysis_report_{timestamp}.md"
    generate_markdown_report(analysis_results, comparative_insights, report_file)
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"📊 Detailed JSON: {analysis_file}")
    print(f"📈 CSV data: {csv_file}")  
    print(f"📝 Report: {report_file}")
    
    return analysis_results

def generate_comparative_analysis(results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate cross-framing comparative insights."""
    
    # Agency patterns
    agency_patterns = {framing: data["agency_analysis"]["primary_agent"] for framing, data in results.items()}
    
    # Ethical framework patterns  
    ethical_patterns = {framing: data["ethical_analysis"]["primary_framework"] for framing, data in results.items()}
    
    # Pronoun concentration
    pronoun_patterns = {framing: data["pronoun_analysis"]["agency_type"] for framing, data in results.items()}
    
    # Response lengths
    length_patterns = {framing: data["response_length"] for framing, data in results.items()}
    
    # Deictic intensity (markers per 1000 chars)
    intensity_patterns = {
        framing: (data["total_deictic_markers"] / data["response_length"]) * 1000 
        for framing, data in results.items()
    }
    
    return {
        "agency_distribution_by_framing": agency_patterns,
        "ethical_frameworks_by_framing": ethical_patterns,
        "pronoun_agency_by_framing": pronoun_patterns,
        "response_lengths": length_patterns,
        "deictic_intensity": intensity_patterns,
        "key_findings": {
            "longest_response": max(length_patterns.items(), key=lambda x: x[1]),
            "shortest_response": min(length_patterns.items(), key=lambda x: x[1]),
            "highest_deictic_intensity": max(intensity_patterns.items(), key=lambda x: x[1]),
            "most_individual_agency": [f for f, a in agency_patterns.items() if "individual" in a.lower()],
            "most_collective_agency": [f for f, a in agency_patterns.items() if "collective" in a.lower()]
        }
    }

def generate_csv_analysis(results: Dict[str, Any], output_file: Path):
    """Generate CSV for statistical analysis."""
    
    rows = []
    for framing, data in results.items():
        row = {
            'framing': framing,
            'response_length': data['response_length'],
            'generation_time': data['generation_time'],
            'total_deictic_markers': data['total_deictic_markers'],
            'deictic_intensity': (data['total_deictic_markers'] / data['response_length']) * 1000,
            
            # Pronoun ratios
            'first_singular_ratio': data['pronoun_analysis']['first_singular_ratio'],
            'second_person_ratio': data['pronoun_analysis']['second_person_ratio'], 
            'first_plural_ratio': data['pronoun_analysis']['first_plural_ratio'],
            'third_person_ratio': data['pronoun_analysis']['third_person_ratio'],
            'agency_concentration': data['pronoun_analysis']['agency_concentration'],
            'agency_type': data['pronoun_analysis']['agency_type'],
            
            # Agency analysis
            'primary_agent': data['agency_analysis']['primary_agent'],
            'decision_locus': data['agency_analysis']['decision_locus'],
            'collective_vs_individual': data['agency_analysis']['collective_vs_individual'],
            
            # Ethical analysis
            'primary_framework': data['ethical_analysis']['primary_framework'],
            'reasoning_type': data['ethical_analysis']['reasoning_type'],
            'consequence_vs_duty': data['ethical_analysis']['consequence_vs_duty']
        }
        
        # Add individual deictic markers
        for marker, count in data['deictic_markers'].items():
            row[f'deictic_{marker}'] = count
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)

def generate_markdown_report(results: Dict[str, Any], comparative: Dict[str, Any], output_file: Path):
    """Generate human-readable markdown report."""
    
    report = f"""# Academic Integrity Deictic Analysis Report

## Overview
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Framings Analyzed**: {len(results)}
- **Total Response Text**: {sum(r['response_length'] for r in results.values())} characters

## Key Findings

### Agency Distribution Patterns
"""
    
    for framing, agent in comparative["agency_distribution_by_framing"].items():
        report += f"- **{framing}**: {agent}\n"
    
    report += "\n### Ethical Framework Patterns\n"
    for framing, framework in comparative["ethical_frameworks_by_framing"].items():
        report += f"- **{framing}**: {framework}\n"
    
    report += "\n### Response Length Analysis\n"
    for framing, length in comparative["response_lengths"].items():
        report += f"- **{framing}**: {length} characters\n"
    
    report += f"\n## Notable Insights\n"
    findings = comparative["key_findings"]
    report += f"- **Longest response**: {findings['longest_response'][0]} ({findings['longest_response'][1]} chars)\n"
    report += f"- **Highest deictic intensity**: {findings['highest_deictic_intensity'][0]} ({findings['highest_deictic_intensity'][1]:.1f} markers/1000 chars)\n"
    
    if findings['most_individual_agency']:
        report += f"- **Individual agency framings**: {', '.join(findings['most_individual_agency'])}\n"
    if findings['most_collective_agency']:
        report += f"- **Collective agency framings**: {', '.join(findings['most_collective_agency'])}\n"
    
    report += "\n## Research Implications\n"
    report += "This analysis reveals how different deictic framings systematically influence:\n"
    report += "1. **Agency attribution** - Who GPT-4o assigns moral responsibility to\n"
    report += "2. **Ethical reasoning** - Which moral frameworks the model employs\n"
    report += "3. **Linguistic patterns** - How pronoun use reflects moral positioning\n"
    report += "4. **Response complexity** - How framing affects depth of reasoning\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    asyncio.run(analyze_academic_integrity_responses()) 