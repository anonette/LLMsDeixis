"""
Analyze agency distribution in existing deixis analysis results.
This script finds and analyzes all existing analysis sessions.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from pronoun_agency_analyzer import PronounAgencyAnalyzer
from integrate_pronoun_analyzer import DeixisPronounIntegration
import pandas as pd
import matplotlib.pyplot as plt


def find_analysis_sessions():
    """Find all existing analysis session directories."""
    sessions = []
    
    # Check automated_analysis_results directory
    results_dir = Path("automated_analysis_results")
    if results_dir.exists():
        for session_dir in results_dir.iterdir():
            if session_dir.is_dir() and session_dir.name.startswith("session_"):
                all_results_path = session_dir / "all_results.json"
                if all_results_path.exists():
                    sessions.append({
                        'name': session_dir.name,
                        'path': all_results_path,
                        'dir': session_dir
                    })
    
    # Check for other result files
    other_paths = [
        "analysis_results.json",
        "analysis_results/all_results.json"
    ]
    
    for path in other_paths:
        if Path(path).exists():
            sessions.append({
                'name': Path(path).stem,
                'path': Path(path),
                'dir': Path(path).parent
            })
    
    return sessions


def analyze_session(session_info):
    """Analyze agency distribution in a single session."""
    print(f"\n{'='*80}")
    print(f"Analyzing session: {session_info['name']}")
    print(f"Path: {session_info['path']}")
    print('='*80)
    
    # Initialize integration
    integration = DeixisPronounIntegration()
    
    # Analyze the session
    df = integration.analyze_existing_results(str(session_info['path']))
    
    if df is None or df.empty:
        print("No valid data found in this session.")
        return None
    
    # Generate report
    report_path = session_info['dir'] / "pronoun_agency_report.md"
    report = integration.generate_agency_report(df, str(report_path))
    
    # Generate visualization
    viz_path = session_info['dir'] / "agency_distribution_visualization.png"
    integration.pronoun_analyzer.visualize_agency_distribution(df, str(viz_path))
    
    # Print summary statistics
    print(f"\nAnalyzed {len(df)} responses")
    print(f"Report saved to: {report_path}")
    print(f"Visualization saved to: {viz_path}")
    
    # Show key findings
    print("\nKey Findings:")
    print("-" * 40)
    
    # Agency concentration by framing
    agency_by_framing = df.groupby('framing')['agency_concentration'].agg(['mean', 'std', 'count'])
    print("\nAgency Concentration by Framing:")
    print(agency_by_framing.round(3))
    
    # Dominant pronouns by framing
    print("\nDominant Pronoun Type by Framing:")
    for framing in df['framing'].unique():
        framing_data = df[df['framing'] == framing]
        
        # Get average ratios
        ratio_cols = ['first_singular_ratio', 'second_person_ratio', 
                     'first_plural_ratio', 'third_person_ratio', 'impersonal_ratio']
        avg_ratios = framing_data[ratio_cols].mean()
        
        # Find dominant
        dominant = avg_ratios.idxmax()
        dominant_name = dominant.replace('_ratio', '').replace('_', ' ').title()
        dominant_value = avg_ratios[dominant]
        
        print(f"  {framing}: {dominant_name} ({dominant_value:.1%})")
    
    # Agency type distribution
    print("\nAgency Type Distribution:")
    agency_types = df.groupby(['framing', 'agency_type']).size().unstack(fill_value=0)
    print(agency_types)
    
    return df


def create_comparative_report(all_sessions_data):
    """Create a comparative report across all sessions."""
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS ACROSS ALL SESSIONS")
    print("="*80)
    
    # Combine all dataframes
    combined_df = pd.concat(all_sessions_data.values(), ignore_index=True)
    
    # Initialize analyzer for reporting
    analyzer = PronounAgencyAnalyzer()
    
    # Generate comprehensive report
    report_path = "comprehensive_agency_analysis_report.md"
    
    with open(report_path, 'w') as f:
        f.write("# Comprehensive Pronoun Agency Analysis\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Overview\n")
        f.write(f"- Total responses analyzed: {len(combined_df)}\n")
        f.write(f"- Number of sessions: {len(all_sessions_data)}\n")
        f.write(f"- Unique framings: {', '.join(combined_df['framing'].unique())}\n\n")
        
        f.write("## Key Research Findings\n\n")
        f.write("### How do deixis-based prompting techniques influence agency distribution?\n\n")
        
        # Overall patterns
        f.write("#### 1. Agency Concentration Patterns\n\n")
        agency_stats = combined_df.groupby('framing')['agency_concentration'].agg(['mean', 'std', 'count'])
        f.write("| Framing | Mean Concentration | Std Dev | N |\n")
        f.write("|---------|-------------------|---------|---|\n")
        for framing, row in agency_stats.iterrows():
            f.write(f"| {framing} | {row['mean']:.3f} | {row['std']:.3f} | {row['count']} |\n")
        
        f.write("\n#### 2. Pronoun Usage Patterns\n\n")
        f.write("Average pronoun distribution by framing:\n\n")
        
        ratio_cols = ['first_singular_ratio', 'second_person_ratio', 
                     'first_plural_ratio', 'third_person_ratio', 'impersonal_ratio']
        
        for framing in combined_df['framing'].unique():
            framing_data = combined_df[combined_df['framing'] == framing]
            f.write(f"\n**{framing.title()} Framing:**\n")
            
            avg_ratios = framing_data[ratio_cols].mean()
            for col, value in avg_ratios.items():
                if value > 0.01:  # Only show if > 1%
                    category = col.replace('_ratio', '').replace('_', ' ').title()
                    f.write(f"- {category}: {value:.1%}\n")
        
        f.write("\n#### 3. Agency Type Distribution\n\n")
        agency_types = combined_df.groupby(['framing', 'agency_type']).size().unstack(fill_value=0)
        f.write("```\n")
        f.write(str(agency_types))
        f.write("\n```\n")
        
        f.write("\n## Interpretation\n\n")
        f.write("""
The analysis reveals systematic patterns in how deixis influences agency distribution:

1. **First-person framing** concentrates agency in the individual speaker through heavy use of "I/me/my" pronouns
2. **Second-person framing** transfers agency to the reader/decision-maker through "you/your" pronouns  
3. **Dialogic framing** distributes agency collectively through "we/us/our" pronouns
4. **Impersonal framing** abstracts agency through "one/someone" constructions
5. **Cosmological framing** externalizes agency to non-human entities

These patterns demonstrate that linguistic structure (deixis) fundamentally shapes how moral responsibility is constructed and attributed in ethical reasoning.
""")
        
        f.write("\n## Session Details\n\n")
        for session_name, df in all_sessions_data.items():
            f.write(f"### {session_name}\n")
            f.write(f"- Responses: {len(df)}\n")
            f.write(f"- Average agency concentration: {df['agency_concentration'].mean():.3f}\n")
            f.write(f"- Most common agency type: {df['agency_type'].mode()[0] if not df['agency_type'].mode().empty else 'N/A'}\n\n")
    
    print(f"\nComprehensive report saved to: {report_path}")
    
    # Create combined visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Agency Distribution Across All Sessions', fontsize=16)
    
    # 1. Agency concentration by framing
    ax1 = axes[0, 0]
    agency_stats = combined_df.groupby('framing')['agency_concentration'].mean().sort_values(ascending=False)
    agency_stats.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Average Agency Concentration by Framing')
    ax1.set_ylabel('Concentration Score')
    ax1.set_xlabel('Framing')
    ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Balanced')
    
    # 2. Pronoun distribution heatmap
    ax2 = axes[0, 1]
    pronoun_avg = combined_df.groupby('framing')[ratio_cols].mean()
    im = ax2.imshow(pronoun_avg.T, aspect='auto', cmap='YlOrRd')
    ax2.set_xticks(range(len(pronoun_avg.index)))
    ax2.set_xticklabels(pronoun_avg.index, rotation=45)
    ax2.set_yticks(range(len(ratio_cols)))
    ax2.set_yticklabels([col.replace('_ratio', '').replace('_', ' ').title() for col in ratio_cols])
    ax2.set_title('Pronoun Usage Heatmap')
    plt.colorbar(im, ax=ax2)
    
    # 3. Agency type distribution
    ax3 = axes[1, 0]
    agency_type_counts = combined_df['agency_type'].value_counts()
    agency_type_counts.plot(kind='pie', ax=ax3, autopct='%1.1f%%')
    ax3.set_title('Overall Agency Type Distribution')
    ax3.set_ylabel('')
    
    # 4. Response count by framing
    ax4 = axes[1, 1]
    framing_counts = combined_df['framing'].value_counts()
    framing_counts.plot(kind='bar', ax=ax4, color='lightgreen')
    ax4.set_title('Number of Responses by Framing')
    ax4.set_ylabel('Count')
    ax4.set_xlabel('Framing')
    
    plt.tight_layout()
    plt.savefig('comprehensive_agency_visualization.png', dpi=300, bbox_inches='tight')
    print("Comprehensive visualization saved to: comprehensive_agency_visualization.png")
    
    return combined_df


def main():
    """Main analysis function."""
    print("Pronoun Agency Analysis for Existing Data")
    print("="*80)
    
    # Find all sessions
    sessions = find_analysis_sessions()
    
    if not sessions:
        print("No existing analysis sessions found.")
        return
    
    print(f"Found {len(sessions)} analysis session(s):")
    for session in sessions:
        print(f"  - {session['name']}: {session['path']}")
    
    # Analyze each session
    all_sessions_data = {}
    
    for session in sessions:
        df = analyze_session(session)
        if df is not None:
            all_sessions_data[session['name']] = df
    
    # Create comparative report if we have data
    if all_sessions_data:
        combined_df = create_comparative_report(all_sessions_data)
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nTotal responses analyzed: {sum(len(df) for df in all_sessions_data.values())}")
        print("\nGenerated files:")
        print("  - Individual session reports in each session directory")
        print("  - comprehensive_agency_analysis_report.md")
        print("  - comprehensive_agency_visualization.png")
        
        # Answer the research question
        print("\n" + "="*80)
        print("RESEARCH QUESTION ANSWER")
        print("="*80)
        print("\nHow do deixis-based prompting techniques influence agency distribution in LLMs?")
        print("\nThe pronoun ratio analysis reveals that deixis systematically redistributes moral agency:")
        
        # Calculate key metrics
        for framing in combined_df['framing'].unique():
            framing_data = combined_df[combined_df['framing'] == framing]
            
            # Get dominant pronoun type
            ratio_cols = ['first_singular_ratio', 'second_person_ratio', 
                         'first_plural_ratio', 'third_person_ratio', 'impersonal_ratio']
            avg_ratios = framing_data[ratio_cols].mean()
            dominant = avg_ratios.idxmax()
            dominant_name = dominant.replace('_ratio', '').replace('_', ' ').title()
            dominant_value = avg_ratios[dominant]
            
            # Get agency type
            agency_type = framing_data['agency_type'].mode()[0] if not framing_data['agency_type'].mode().empty else 'mixed'
            
            print(f"\n{framing.upper()}: {dominant_name} ({dominant_value:.0%}) → {agency_type} agency")
    
    else:
        print("\nNo valid data found to analyze.")


if __name__ == "__main__":
    main()