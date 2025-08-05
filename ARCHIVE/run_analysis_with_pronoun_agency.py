"""
Enhanced Automated Deictic Research Analysis Runner
Includes pronoun agency analysis alongside existing expert analyses
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from pronoun_agency_expert import PronounAgencyExpert, add_pronoun_agency_analysis

def extract_detailed_examples_from_logs(session_data):
    """Extract detailed examples from session logs for use in reports."""
    if not session_data or 'records' not in session_data:
        return {}
    
    examples = {
        'sample_responses': {},
        'processing_metrics': {},
        'deictic_patterns': {},
        'response_variations': []
    }
    
    # Group records by framework
    framework_responses = {}
    for record in session_data['records']:
        if isinstance(record, dict):
            framework = record.get('deictic_framing', 'unknown')
            if framework not in framework_responses:
                framework_responses[framework] = []
            framework_responses[framework].append(record)
    
    # Extract sample responses for each framework
    for framework, responses in framework_responses.items():
        if responses:
            # Get the first complete response as a sample
            sample = responses[0]
            llm_response = sample.get('llm_response', '')
            
            # Extract excerpt (first 200 characters)
            response_excerpt = llm_response[:200] + "..." if len(llm_response) > 200 else llm_response
            
            # Extract deictic markers
            deictic_markers = sample.get('deictic_markers', [])
            if isinstance(deictic_markers, dict):
                deictic_markers = list(deictic_markers.keys())
            
            examples['sample_responses'][framework] = {
                'excerpt': response_excerpt,
                'full_response': llm_response,
                'deictic_markers': deictic_markers,
                'processing_time': sample.get('processing_time', 0),
                'dilemma_id': sample.get('dilemma_id', 'unknown')
            }
            
            # Collect processing metrics
            if framework not in examples['processing_metrics']:
                examples['processing_metrics'][framework] = {
                    'avg_time': 0,
                    'total_responses': 0,
                    'avg_length': 0
                }
            
            for response in responses:
                metrics = examples['processing_metrics'][framework]
                metrics['total_responses'] += 1
                metrics['avg_time'] += response.get('processing_time', 0)
                metrics['avg_length'] += len(response.get('llm_response', ''))
            
            # Calculate averages
            if metrics['total_responses'] > 0:
                metrics['avg_time'] /= metrics['total_responses']
                metrics['avg_length'] /= metrics['total_responses']
    
    # Extract deictic patterns
    for framework, responses in framework_responses.items():
        pattern_counts = {}
        for response in responses:
            markers = response.get('deictic_markers', [])
            if isinstance(markers, dict):
                for marker in markers:
                    pattern_counts[marker] = pattern_counts.get(marker, 0) + 1
            elif isinstance(markers, list):
                for marker in markers:
                    pattern_counts[marker] = pattern_counts.get(marker, 0) + 1
        
        examples['deictic_patterns'][framework] = pattern_counts
    
    # Extract response variations
    for framework, responses in framework_responses.items():
        if len(responses) > 1:
            # Compare first two responses for the same dilemma
            dilemma_groups = {}
            for response in responses:
                dilemma_id = response.get('dilemma_id', 'unknown')
                if dilemma_id not in dilemma_groups:
                    dilemma_groups[dilemma_id] = []
                dilemma_groups[dilemma_id].append(response)
            
            for dilemma_id, dilemma_responses in dilemma_groups.items():
                if len(dilemma_responses) >= 2:
                    examples['response_variations'].append({
                        'framework': framework,
                        'dilemma_id': dilemma_id,
                        'response_1_excerpt': dilemma_responses[0].get('llm_response', '')[:150] + "...",
                        'response_2_excerpt': dilemma_responses[1].get('llm_response', '')[:150] + "...",
                        'variation_note': 'Different responses to same dilemma show framework influence'
                    })
    
    return examples

async def run_complete_analysis():
    """Run complete analysis with all expert agents including pronoun agency."""
    
    print("=" * 80)
    print("ENHANCED DEICTIC ETHICAL ANALYSIS WITH PRONOUN AGENCY")
    print("=" * 80)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize analyzers
    print("\nInitializing analyzers...")
    print("  - Using GPT-4o directly through OpenAI API")
    print("  - Temperature: 0.6 (balanced analysis)")
    print("  - No model rotation: consistent single model")
    analyzer = DeicticEthicalAnalyzer(
        enable_rich_logging=True, 
        use_openai_direct=True, 
        temperature=0.6
    )
    critical_expert = CriticalExpertAnalyzer()
    evidence_expert = EvidenceBasedExpertAnalyzer()
    pronoun_expert = PronounAgencyExpert()
    
    # Load dilemmas
    print("\nLoading ethical dilemmas...")
    dilemmas = [
        {
            "id": "whistleblowing_tech",
            "title": "Tech Company Whistleblowing",
            "description": "You discover your company is secretly collecting user data beyond what users consented to. Reporting this would likely end your career but protect millions of users.",
            "ethical_dimensions": ["privacy", "loyalty", "transparency", "personal_cost"]
        },
        {
            "id": "ai_bias_hiring",
            "title": "AI Bias in Hiring System",
            "description": "You're developing an AI hiring system and discover it has a subtle bias against certain demographic groups. Your manager wants to launch on schedule.",
            "ethical_dimensions": ["fairness", "discrimination", "business_pressure", "social_impact"]
        },
        {
            "id": "medical_resource_allocation",
            "title": "Medical Resource Allocation",
            "description": "During a medical crisis, you must decide how to allocate limited ventilators between young and elderly patients.",
            "ethical_dimensions": ["fairness", "utility", "age_discrimination", "triage"]
        }
    ]
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = Path(f"automated_analysis_results/session_{timestamp}")
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # Run analysis
    print(f"\nAnalyzing {len(dilemmas)} dilemmas across all deictic framings...")
    all_results = []
    
    for i, dilemma in enumerate(dilemmas, 1):
        print(f"\n{'='*60}")
        print(f"Analyzing Dilemma {i}/{len(dilemmas)}: {dilemma['title']}")
        print("="*60)
        
        try:
            results = await analyzer.analyze_dilemma_async(dilemma)
            all_results.append(results)
            
            # Show progress
            if 'responses' in results:
                for framing, response_data in results['responses'].items():
                    if 'response' in response_data:
                        print(f"\n{framing.upper()} - Response generated")
                        print(f"  Length: {len(response_data['response'])} chars")
                        if 'deictic_markers' in response_data:
                            markers = response_data['deictic_markers']
                            if isinstance(markers, dict):
                                print(f"  Deictic markers: {len(markers)} found")
                            
        except Exception as e:
            print(f"Error analyzing dilemma {dilemma['id']}: {e}")
            continue
    
    # Get session data from logger
    print("\n\nExtracting session data...")
    session_data = analyzer.logger.get_session_data() if hasattr(analyzer, 'logger') else {}
    
    # Add pronoun agency analysis
    print("\nRunning pronoun agency analysis...")
    try:
        session_data = await add_pronoun_agency_analysis(session_data, str(session_dir))
        print("✓ Pronoun agency analysis complete")
    except Exception as e:
        print(f"Error in pronoun agency analysis: {e}")
    
    # Run critical expert analysis
    print("\nRunning critical expert analysis...")
    try:
        critical_report = await critical_expert.analyze_session_data(session_data)
        critical_insights = critical_expert.generate_critical_insights(critical_report)
        print("✓ Critical analysis complete")
    except Exception as e:
        print(f"Error in critical analysis: {e}")
        critical_insights = {}
    
    # Run evidence-based expert analysis
    print("\nRunning evidence-based expert analysis...")
    try:
        evidence_report = await evidence_expert.analyze_session_data(session_data)
        evidence_findings = evidence_expert.generate_evidence_based_findings(evidence_report)
        print("✓ Evidence-based analysis complete")
    except Exception as e:
        print(f"Error in evidence-based analysis: {e}")
        evidence_findings = {}
    
    # Extract examples from logs
    examples = extract_detailed_examples_from_logs(session_data)
    
    # Generate comprehensive reports
    print("\n\nGenerating comprehensive reports...")
    
    # Save raw results
    with open(session_dir / "all_results.json", 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Save session data with pronoun analysis
    with open(session_dir / "session_data_with_pronouns.json", 'w') as f:
        json.dump(session_data, f, indent=2)
    
    # Generate main research report
    main_report = generate_main_report(all_results, session_data, examples)
    with open(session_dir / "research_report.md", 'w', encoding='utf-8') as f:
        f.write(main_report)
    
    # Generate critical analysis report
    if critical_insights:
        critical_report_md = generate_critical_report(critical_insights, session_data)
        with open(session_dir / "critical_analysis_report.md", 'w', encoding='utf-8') as f:
            f.write(critical_report_md)
    
    # Generate evidence-based report
    if evidence_findings:
        evidence_report_md = generate_evidence_report(evidence_findings, examples)
        with open(session_dir / "evidence_based_findings.md", 'w', encoding='utf-8') as f:
            f.write(evidence_report_md)
    
    # Generate final summary
    print("\nGenerating final summary...")
    summary = {
        "session_id": timestamp,
        "analysis_date": datetime.now().isoformat(),
        "dilemmas_analyzed": len(dilemmas),
        "framings_tested": len(analyzer.deictic_framings),
        "total_responses": len(all_results) * len(analyzer.deictic_framings),
        "reports_generated": [
            "research_report.md",
            "critical_analysis_report.md",
            "evidence_based_findings.md",
            "pronoun_agency_analysis.md",
            "session_data_with_pronouns.json"
        ],
        "key_findings": {
            "pronoun_agency": session_data.get('pronoun_agency_analysis', {}).get('key_findings', []),
            "critical_insights": list(critical_insights.keys()) if critical_insights else [],
            "evidence_based": list(evidence_findings.keys()) if evidence_findings else []
        }
    }
    
    with open(session_dir / "analysis_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"\nAll results saved to: {session_dir}/")
    print("\nGenerated reports:")
    for report in summary['reports_generated']:
        print(f"  - {report}")
    
    # Show key pronoun agency findings
    if 'pronoun_agency_analysis' in session_data:
        agency_data = session_data['pronoun_agency_analysis']
        print("\n" + "="*80)
        print("KEY PRONOUN AGENCY FINDINGS")
        print("="*80)
        
        if 'executive_summary' in agency_data:
            print(f"\n{agency_data['executive_summary']}")
        
        if 'agency_patterns_by_framing' in agency_data:
            print("\nAgency Distribution by Framing:")
            for framing, pattern in agency_data['agency_patterns_by_framing'].items():
                print(f"\n{framing.upper()}:")
                print(f"  - Dominant agency: {pattern.get('dominant_agency_type', 'unknown')}")
                print(f"  - Concentration: {pattern.get('agency_concentration', 0):.3f}")
                print(f"  - Mechanism: {pattern.get('linguistic_mechanism', 'N/A')}")
    
    return session_dir

def generate_main_report(all_results, session_data, examples):
    """Generate the main research report."""
    report = f"""# Deictic Ethical Analysis Research Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report presents the results of an automated analysis examining how different deictic framings influence ethical reasoning in AI language models. The analysis includes traditional deixis metrics alongside new pronoun-based agency distribution analysis.

## Key Findings

### Pronoun Agency Analysis

"""
    
    if 'pronoun_agency_analysis' in session_data:
        agency_data = session_data['pronoun_agency_analysis']
        if 'key_findings' in agency_data:
            for finding in agency_data['key_findings']:
                report += f"- {finding}\n"
    
    report += "\n### Deictic Patterns\n\n"
    
    # Add deictic pattern analysis
    for framework, patterns in examples.get('deictic_patterns', {}).items():
        if patterns:
            top_markers = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:3]
            report += f"**{framework.title()}**: "
            report += ", ".join([f"{marker} ({count})" for marker, count in top_markers])
            report += "\n"
    
    report += "\n## Detailed Analysis by Dilemma\n\n"
    
    # Add detailed results
    for result in all_results:
        if 'dilemma_id' in result:
            report += f"### {result['dilemma_id']}\n\n"
            
            if 'responses' in result:
                for framing, response_data in result['responses'].items():
                    report += f"#### {framing.title()} Framing\n\n"
                    
                    if 'response' in response_data:
                        excerpt = response_data['response'][:200] + "..."
                        report += f"**Response excerpt:** {excerpt}\n\n"
                    
                    if 'deictic_markers' in response_data:
                        markers = response_data['deictic_markers']
                        if isinstance(markers, dict) and markers:
                            report += f"**Deictic markers found:** {len(markers)}\n\n"
    
    return report

def generate_critical_report(critical_insights, session_data):
    """Generate critical analysis report."""
    report = """# Critical Analysis Report

## Methodological Assessment

This report provides a critical evaluation of the deictic analysis methodology and findings.

"""
    
    for insight_id, insights in critical_insights.items():
        report += f"\n### {insight_id}\n\n"
        
        for insight in insights:
            report += f"**Finding:** {insight.get('insight_statement', 'N/A')}\n"
            report += f"**Confidence:** {insight.get('confidence_level', 0):.2f}\n\n"
            
            if 'what_works' in insight:
                report += "**Strengths:**\n"
                for item in insight['what_works']:
                    report += f"- {item}\n"
                report += "\n"
            
            if 'what_doesnt_work' in insight:
                report += "**Limitations:**\n"
                for item in insight['what_doesnt_work']:
                    report += f"- {item}\n"
                report += "\n"
    
    return report

def generate_evidence_report(evidence_findings, examples):
    """Generate evidence-based findings report."""
    report = """# Evidence-Based Findings Report

## Empirical Analysis Results

This report presents findings based on direct evidence from the analysis.

"""
    
    for finding_id, findings in evidence_findings.items():
        report += f"\n### {finding_id}\n\n"
        
        for finding in findings:
            report += f"**Pattern:** {finding.get('pattern_description', 'N/A')}\n"
            report += f"**Statistical Significance:** {finding.get('statistical_significance', 'N/A')}\n\n"
            
            if 'supporting_evidence' in finding:
                report += "**Evidence:**\n"
                for evidence in finding['supporting_evidence']:
                    report += f"- {evidence}\n"
                report += "\n"
    
    # Add examples
    if examples.get('sample_responses'):
        report += "\n## Sample Responses\n\n"
        for framework, sample in examples['sample_responses'].items():
            report += f"### {framework.title()}\n"
            report += f"**Excerpt:** {sample.get('excerpt', 'N/A')}\n\n"
    
    return report

if __name__ == "__main__":
    # Run the complete analysis
    asyncio.run(run_complete_analysis())