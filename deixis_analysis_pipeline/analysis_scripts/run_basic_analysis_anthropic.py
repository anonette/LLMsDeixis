"""
Basic Analysis Script for Anthropic Claude Generated Responses
Processes the generated responses and creates a summary report
"""

import json
import csv
from pathlib import Path
from datetime import datetime
import pandas as pd

def load_response_files(session_dir):
    """Load all response files from a session directory."""
    responses = []
    response_files = list(session_dir.glob("*_responses.json"))
    
    for file_path in response_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            responses.append(data)
    
    return responses

def analyze_responses(responses):
    """Basic analysis of responses."""
    analysis_results = []
    
    for response_data in responses:
        dilemma_id = response_data['dilemma_id']
        dilemma_title = response_data['dilemma_title']
        model = response_data['model']
        
        for framing, response_info in response_data['responses'].items():
            if 'error' in response_info:
                continue
                
            result = {
                'dilemma_id': dilemma_id,
                'dilemma_title': dilemma_title,
                'model': model,
                'framing': framing,
                'response_length': len(response_info.get('response', '')),
                'generation_time': response_info.get('generation_time', 0),
                'deictic_markers': ', '.join(response_info.get('deictic_markers', [])),
                'framing_focus': response_info.get('framing_focus', ''),
                'response_preview': response_info.get('response', '')[:200] + '...'
            }
            analysis_results.append(result)
    
    return analysis_results

def save_results(analysis_results, output_dir):
    """Save analysis results to CSV and JSON."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    csv_path = output_dir / "anthropic_analysis_results.csv"
    df = pd.DataFrame(analysis_results)
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] CSV results: {csv_path}")
    
    # Save to JSON
    json_path = output_dir / "anthropic_analysis_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] JSON results: {json_path}")
    
    # Generate summary report
    summary = {
        'analysis_timestamp': datetime.now().isoformat(),
        'total_responses_analyzed': len(analysis_results),
        'dilemmas_analyzed': len(df['dilemma_id'].unique()),
        'framings_per_dilemma': len(df['framing'].unique()),
        'model_used': 'anthropic/claude-3.5-sonnet',
        'average_response_length': df['response_length'].mean(),
        'average_generation_time': df['generation_time'].mean(),
        'dilemma_summary': df.groupby('dilemma_title')['response_length'].agg(['count', 'mean']).to_dict()
    }
    
    summary_path = output_dir / "analysis_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Summary report: {summary_path}")
    
    # Generate markdown report
    md_report = f"""# Anthropic Claude 3.5 Sonnet Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics

- **Total Responses Analyzed**: {len(analysis_results)}
- **Number of Dilemmas**: {len(df['dilemma_id'].unique())}
- **Framings per Dilemma**: {len(df['framing'].unique())}
- **Model Used**: anthropic/claude-3.5-sonnet
- **Average Response Length**: {df['response_length'].mean():.0f} characters
- **Average Generation Time**: {df['generation_time'].mean():.2f} seconds

## Dilemma Breakdown

| Dilemma | Responses | Avg Length |
|---------|-----------|------------|
"""
    
    for dilemma in df['dilemma_title'].unique():
        dilemma_data = df[df['dilemma_title'] == dilemma]
        count = len(dilemma_data)
        avg_length = dilemma_data['response_length'].mean()
        md_report += f"| {dilemma} | {count} | {avg_length:.0f} |\n"
    
    md_report += f"\n## Framing Distribution\n\n"
    framing_counts = df['framing'].value_counts()
    for framing, count in framing_counts.items():
        md_report += f"- **{framing}**: {count} responses\n"
    
    md_path = output_dir / "anthropic_analysis_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_report)
    print(f"[SAVED] Markdown report: {md_path}")

def main():
    """Main analysis function."""
    print("="*80)
    print("BASIC ANALYSIS OF ANTHROPIC CLAUDE RESPONSES")
    print("="*80)
    
    # Find the latest Anthropic session
    generation_logs_dir = Path("deixis_analysis_pipeline/generation_logs")
    anthropic_sessions = [d for d in generation_logs_dir.iterdir() if d.is_dir() and 'anthropic' in d.name]
    
    if not anthropic_sessions:
        print("[ERROR] No Anthropic session found!")
        return
    
    latest_session = max(anthropic_sessions, key=lambda x: x.stat().st_mtime)
    print(f"[OK] Using session: {latest_session.name}")
    
    # Load responses
    responses = load_response_files(latest_session)
    print(f"[OK] Loaded {len(responses)} dilemma response files")
    
    # Analyze responses
    analysis_results = analyze_responses(responses)
    print(f"[OK] Analyzed {len(analysis_results)} individual responses")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("deixis_analysis_pipeline/automated_analysis_results") / f"anthropic_basic_{timestamp}"
    save_results(analysis_results, output_dir)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print(f"Results saved to: {output_dir}")
    print("="*80)

if __name__ == "__main__":
    main()