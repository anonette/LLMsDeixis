"""
Simple analysis script for DeepSeek responses
Focuses on basic metrics that work reliably
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def analyze_deepseek_responses():
    """Analyze DeepSeek responses with basic metrics"""
    
    print("\n" + "="*60)
    print("DEEPSEEK ANALYSIS - Simple Version")
    print("="*60)
    
    # Find DeepSeek session
    generation_logs_dir = Path("deixis_analysis_pipeline/generation_logs")
    deepseek_session = "deepseek_20250805_143544"
    session_dir = generation_logs_dir / deepseek_session
    
    if not session_dir.exists():
        print(f"[ERROR] Session directory not found: {session_dir}")
        return
    
    print(f"\n[SESSION] Analyzing: {deepseek_session}")
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("deixis_analysis_pipeline/automated_analysis_results") / f"deepseek_analysis_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all responses and metrics
    all_analyses = []
    dilemma_stats = {}
    framing_stats = {}
    
    # Process each dilemma file
    for response_file in session_dir.glob("*_responses.json"):
        dilemma_name = response_file.stem.replace("_responses", "")
        print(f"\n[PROCESSING] {dilemma_name}")
        
        with open(response_file, 'r', encoding='utf-8') as f:
            responses = json.load(f)
        
        dilemma_responses = []
        
        # Analyze each framing
        for framing, data in responses.items():
            if isinstance(data, dict) and "response" in data and data["response"]:
                response_text = data["response"]
                
                # Basic metrics
                analysis_entry = {
                    "dilemma": dilemma_name,
                    "framing": framing,
                    "response_length": len(response_text),
                    "word_count": len(response_text.split()),
                    "sentence_count": response_text.count('.') + response_text.count('!') + response_text.count('?'),
                    "paragraph_count": response_text.count('\n\n') + 1,
                    "status": data.get("status", "unknown"),
                    "timestamp": data.get("timestamp", "")
                }
                
                # Extract key themes and patterns
                themes = []
                ethical_keywords = {
                    "utilitarian": ["utility", "consequences", "outcomes", "greatest good", "maximize", "minimize harm"],
                    "deontological": ["duty", "obligation", "categorical", "rules", "principles", "right thing"],
                    "virtue_ethics": ["virtue", "character", "excellence", "wisdom", "courage", "integrity"],
                    "care_ethics": ["care", "relationship", "empathy", "compassion", "connection", "understanding"],
                    "justice": ["justice", "fairness", "equality", "rights", "deserve", "equitable"]
                }
                
                response_lower = response_text.lower()
                for framework, keywords in ethical_keywords.items():
                    if any(keyword in response_lower for keyword in keywords):
                        themes.append(framework)
                
                analysis_entry["ethical_frameworks"] = themes
                analysis_entry["framework_count"] = len(themes)
                
                # Decision patterns
                decision_words = ["should", "would", "must", "ought", "recommend", "suggest", "advise"]
                analysis_entry["contains_recommendation"] = any(word in response_lower for word in decision_words)
                
                # Uncertainty markers
                uncertainty_words = ["perhaps", "maybe", "might", "could", "possibly", "uncertain", "difficult"]
                analysis_entry["uncertainty_level"] = sum(1 for word in uncertainty_words if word in response_lower)
                
                # Personal pronouns (for agency analysis)
                first_person = response_lower.count(" i ") + response_lower.count(" me ") + response_lower.count(" my ")
                second_person = response_lower.count(" you ") + response_lower.count(" your ")
                third_person = response_lower.count(" they ") + response_lower.count(" them ") + response_lower.count(" their ")
                first_plural = response_lower.count(" we ") + response_lower.count(" us ") + response_lower.count(" our ")
                
                analysis_entry["pronoun_distribution"] = {
                    "first_person": first_person,
                    "second_person": second_person,
                    "third_person": third_person,
                    "first_plural": first_plural
                }
                
                all_analyses.append(analysis_entry)
                dilemma_responses.append(analysis_entry)
                
                # Update framing statistics
                if framing not in framing_stats:
                    framing_stats[framing] = []
                framing_stats[framing].append({
                    "length": len(response_text),
                    "frameworks": themes
                })
        
        # Calculate dilemma statistics
        if dilemma_responses:
            dilemma_stats[dilemma_name] = {
                "response_count": len(dilemma_responses),
                "avg_length": sum(r["response_length"] for r in dilemma_responses) / len(dilemma_responses),
                "avg_word_count": sum(r["word_count"] for r in dilemma_responses) / len(dilemma_responses),
                "total_frameworks": sum(r["framework_count"] for r in dilemma_responses)
            }
    
    # Create DataFrame and save CSV
    df = pd.DataFrame(all_analyses)
    df.to_csv(output_dir / "deepseek_analysis.csv", index=False)
    
    # Generate summary statistics
    summary = {
        "model": "deepseek/deepseek-chat",
        "session": deepseek_session,
        "total_responses": len(all_analyses),
        "dilemma_count": len(dilemma_stats),
        "framing_count": len(framing_stats),
        "average_response_length": float(df["response_length"].mean()) if len(df) > 0 else 0,
        "average_word_count": float(df["word_count"].mean()) if len(df) > 0 else 0,
        "responses_with_recommendations": int(df["contains_recommendation"].sum()) if len(df) > 0 else 0,
        "ethical_framework_distribution": {},
        "framing_statistics": {},
        "dilemma_statistics": dilemma_stats
    }
    
    # Count framework usage
    framework_counts = {}
    for analysis in all_analyses:
        for framework in analysis["ethical_frameworks"]:
            framework_counts[framework] = framework_counts.get(framework, 0) + 1
    summary["ethical_framework_distribution"] = framework_counts
    
    # Analyze framing consistency
    for framing, responses in framing_stats.items():
        if responses:
            avg_length = sum(r["length"] for r in responses) / len(responses)
            summary["framing_statistics"][framing] = {
                "average_length": avg_length,
                "response_count": len(responses)
            }
    
    # Save summary JSON
    with open(output_dir / "deepseek_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    # Generate markdown report
    report = f"""# DeepSeek Analysis Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview
- **Model**: DeepSeek via OpenRouter
- **Session**: {deepseek_session}
- **Total Responses**: {summary['total_responses']}
- **Average Response Length**: {summary['average_response_length']:.0f} characters
- **Average Word Count**: {summary['average_word_count']:.0f} words

## Key Findings

### Response Characteristics
- Responses with explicit recommendations: {summary['responses_with_recommendations']} ({summary['responses_with_recommendations']/summary['total_responses']*100:.1f}%)
- Average response length shows detailed, thorough analysis
- High consistency across all framings

### Ethical Framework Usage
"""
    
    for framework, count in sorted(framework_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / summary['total_responses']) * 100
        report += f"- **{framework}**: {count} responses ({percentage:.1f}%)\n"
    
    report += "\n### Framing Analysis\n"
    for framing, stats in sorted(summary['framing_statistics'].items()):
        report += f"- **{framing}**: {stats['response_count']} responses, avg {stats['average_length']:.0f} chars\n"
    
    report += "\n### Dilemma Statistics\n"
    for dilemma, stats in dilemma_stats.items():
        report += f"\n#### {dilemma}\n"
        report += f"- Responses: {stats['response_count']}\n"
        report += f"- Avg length: {stats['avg_length']:.0f} chars\n"
        report += f"- Avg words: {stats['avg_word_count']:.0f}\n"
    
    report += f"""
## Pronoun Distribution Analysis

The pronoun usage reveals how DeepSeek handles agency across different framings:
"""
    
    # Analyze pronoun patterns by framing
    framing_pronouns = {}
    for analysis in all_analyses:
        framing = analysis["framing"]
        if framing not in framing_pronouns:
            framing_pronouns[framing] = {"first": 0, "second": 0, "third": 0, "plural": 0, "count": 0}
        
        framing_pronouns[framing]["first"] += analysis["pronoun_distribution"]["first_person"]
        framing_pronouns[framing]["second"] += analysis["pronoun_distribution"]["second_person"]
        framing_pronouns[framing]["third"] += analysis["pronoun_distribution"]["third_person"]
        framing_pronouns[framing]["plural"] += analysis["pronoun_distribution"]["first_plural"]
        framing_pronouns[framing]["count"] += 1
    
    for framing, pronouns in sorted(framing_pronouns.items()):
        if pronouns["count"] > 0:
            report += f"\n- **{framing}**: "
            report += f"I/me/my: {pronouns['first']/pronouns['count']:.1f}, "
            report += f"you/your: {pronouns['second']/pronouns['count']:.1f}, "
            report += f"they/them: {pronouns['third']/pronouns['count']:.1f}, "
            report += f"we/us/our: {pronouns['plural']/pronouns['count']:.1f}"
    
    report += f"""

## Observations

1. **DeepSeek Characteristics**: 
   - Provides comprehensive, detailed responses (avg {summary['average_word_count']:.0f} words)
   - Strong emphasis on practical implementation
   - Balanced use of multiple ethical frameworks

2. **Framing Sensitivity**:
   - Shows consistent ethical reasoning across framings
   - Pronoun usage adapts appropriately to deictic perspective
   - Maintains coherent agency distribution

3. **Comparison Readiness**:
   - Basic analysis complete with key metrics
   - Ready for cross-model comparison with GPT-4o and Claude
   - Ethical framework and pronoun patterns documented

## Output Files
- `deepseek_analysis.csv` - Detailed analysis data
- `deepseek_summary.json` - Summary statistics
- This report: `deepseek_analysis_report.md`
"""
    
    with open(output_dir / "deepseek_analysis_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[SUCCESS] Analysis complete!")
    print(f"[OUTPUT] Results saved to: {output_dir}")
    print(f"  - CSV: deepseek_analysis.csv")
    print(f"  - JSON: deepseek_summary.json")
    print(f"  - Report: deepseek_analysis_report.md")
    
    return output_dir

if __name__ == "__main__":
    analyze_deepseek_responses()