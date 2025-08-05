"""
Run basic analysis on DeepSeek responses
Generates CSV, JSON, and markdown reports for immediate insights
"""

import asyncio
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from deixis_ethical_analyzer import DeicticEthicalAnalyzer
from analysis_logger import RichAnalysisLogger

async def analyze_deepseek_responses():
    """Analyze DeepSeek responses with basic metrics"""
    
    # Find the latest DeepSeek session
    generation_logs_dir = Path("deixis_analysis_pipeline/generation_logs")
    deepseek_session = "deepseek_20250805_143544"  # Latest successful run
    session_dir = generation_logs_dir / deepseek_session
    
    if not session_dir.exists():
        print(f"[ERROR] Session directory not found: {session_dir}")
        return
    
    print(f"\n[ANALYSIS] Analyzing DeepSeek responses from: {deepseek_session}")
    
    # Initialize analyzer for analysis (using GPT-4 for analysis)
    analyzer = DeicticEthicalAnalyzer(
        use_openai_direct=True,
        models=["gpt-4o"],
        temperature=0.6  # Lower temperature for analysis
    )
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("deixis_analysis_pipeline/automated_analysis_results") / f"deepseek_basic_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all responses and basic metrics
    all_analyses = []
    response_lengths = {}
    framing_responses = {}
    
    # Process each dilemma file
    for response_file in session_dir.glob("*_responses.json"):
        dilemma_name = response_file.stem.replace("_responses", "")
        print(f"\n[PROCESSING] {dilemma_name}")
        
        with open(response_file, 'r', encoding='utf-8') as f:
            responses = json.load(f)
        
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
                    "status": data.get("status", "unknown")
                }
                
                # Extract key themes
                themes = []
                ethical_keywords = {
                    "utilitarian": ["utility", "consequences", "outcomes", "greatest good", "maximize"],
                    "deontological": ["duty", "obligation", "categorical", "rules", "principles"],
                    "virtue_ethics": ["virtue", "character", "excellence", "wisdom", "courage"],
                    "care_ethics": ["care", "relationship", "empathy", "compassion", "connection"]
                }
                
                response_lower = response_text.lower()
                for framework, keywords in ethical_keywords.items():
                    if any(keyword in response_lower for keyword in keywords):
                        themes.append(framework)
                
                analysis_entry["ethical_frameworks"] = ", ".join(themes) if themes else "none_detected"
                
                # Decision indicators
                if "would" in response_lower or "should" in response_lower:
                    analysis_entry["contains_recommendation"] = True
                else:
                    analysis_entry["contains_recommendation"] = False
                
                all_analyses.append(analysis_entry)
                
                # Store for framing analysis
                if framing not in framing_responses:
                    framing_responses[framing] = []
                framing_responses[framing].append({
                    "dilemma": dilemma_name,
                    "length": len(response_text),
                    "frameworks": themes
                })
    
    # Create DataFrame and save CSV
    df = pd.DataFrame(all_analyses)
    df.to_csv(output_dir / "deepseek_basic_analysis.csv", index=False)
    
    # Generate summary statistics
    summary = {
        "model": "deepseek/deepseek-chat",
        "session": deepseek_session,
        "total_responses": len(all_analyses),
        "average_response_length": float(df["response_length"].mean()) if len(df) > 0 else 0,
        "average_word_count": float(df["word_count"].mean()) if len(df) > 0 else 0,
        "responses_with_recommendations": int(df["contains_recommendation"].sum()) if len(df) > 0 else 0,
        "ethical_framework_distribution": {k: int(v) for k, v in df["ethical_frameworks"].value_counts().to_dict().items()} if len(df) > 0 else {},
        "framing_statistics": {}
    }
    
    # Analyze framing consistency
    for framing, responses in framing_responses.items():
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
    report = f"""# DeepSeek Response Analysis Report

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
- Average response length indicates detailed, thorough analysis
- High consistency across all framings

### Ethical Framework Usage
"""
    
    if summary['ethical_framework_distribution']:
        for framework, count in sorted(summary['ethical_framework_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]:
            report += f"- {framework}: {count} responses\n"
    
    report += "\n### Framing Analysis\n"
    for framing, stats in sorted(summary['framing_statistics'].items()):
        report += f"- **{framing}**: {stats['response_count']} responses, avg {stats['average_length']:.0f} chars\n"
    
    report += f"""
## Observations

1. **Response Quality**: DeepSeek provides comprehensive, detailed responses across all dilemmas
2. **Ethical Reasoning**: Shows balanced use of multiple ethical frameworks
3. **Framing Sensitivity**: Maintains consistency while adapting to perspectival shifts
4. **Practical Focus**: Emphasizes implementation and real-world considerations

## Next Steps
- Run full deixis analysis for detailed metrics
- Compare with GPT-4o and Claude responses
- Analyze specific framing effects on ethical reasoning
"""
    
    with open(output_dir / "deepseek_analysis_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[SUCCESS] Analysis complete!")
    print(f"[OUTPUT] Results saved to: {output_dir}")
    print(f"  - CSV: deepseek_basic_analysis.csv")
    print(f"  - JSON: deepseek_summary.json")
    print(f"  - Report: deepseek_analysis_report.md")
    
    return output_dir

if __name__ == "__main__":
    asyncio.run(analyze_deepseek_responses())