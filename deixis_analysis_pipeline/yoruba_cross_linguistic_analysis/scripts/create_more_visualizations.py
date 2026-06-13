#!/usr/bin/env python3
"""
Create additional visualizations focusing on Yoruba-specific features and cross-linguistic comparisons.
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac
from analysis_config import COLORS, FRAMING_ORDER, MODELS  # noqa: E402

plt.style.use("default")
sns.set_palette("husl")


def load_data():
    """Load necessary data."""
    return pd.read_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv")

def create_deictic_uptake_divergence(yoruba_merged):
    """Visualize deictic uptake quality patterns."""
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel 1: Uptake quality by framing
    ax1 = fig.add_subplot(gs[0, :])
    
    uptake_data = yoruba_merged.groupby(['framing_type', 'deictic_uptake_quality', 'model']).size().reset_index(name='count')
    
    framings = ['impersonal', 'second_person', 'first_person', 'reflexive', 'dialogic', 
                'spatial', 'temporal', 'cosmological', 'first_person_plural']
    uptake_levels = ['strong_uptake', 'partial_uptake', 'weak_uptake']
    
    x = np.arange(len(framings))
    width = 0.35
    
    for i, model in enumerate(MODELS):
        bottom = np.zeros(len(framings))
        
        for uptake in uptake_levels:
            values = []
            for framing in framings:
                total = uptake_data[(uptake_data['model'] == model) & 
                                  (uptake_data['framing_type'] == framing)]['count'].sum()
                count = uptake_data[(uptake_data['model'] == model) & 
                                  (uptake_data['framing_type'] == framing) & 
                                  (uptake_data['deictic_uptake_quality'] == uptake)]['count'].values
                percentage = (count[0] / total * 100) if count.size > 0 and total > 0 else 0
                values.append(percentage)
            
            color = COLORS[uptake.split('_')[0]]
            ax1.bar(x + i*width, values, width, bottom=bottom, 
                   label=f'{model} - {uptake}' if i == 0 else '', 
                   color=color, alpha=0.8 if i == 0 else 0.6)
            bottom += np.array(values)
    
    ax1.set_xlabel('Framing Type', fontsize=12)
    ax1.set_ylabel('Percentage', fontsize=12)
    ax1.set_title('Deictic Uptake Quality by Framing Type', fontsize=14, fontweight='bold')
    ax1.set_xticks(x + width/2)
    ax1.set_xticklabels([f.replace('_', '\n') for f in framings], rotation=45, ha='right')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Uptake quality vs emphatic ratio
    ax2 = fig.add_subplot(gs[1, 0])
    
    uptake_emphatic = yoruba_merged.groupby(['deictic_uptake_quality', 'model']).agg({
        'emphatic_ratio': ['mean', 'std'],
        'pronouns_per_100_words': 'mean'
    }).reset_index()
    
    x2 = np.arange(len(uptake_levels))
    
    for i, model in enumerate(MODELS):
        values = []
        errors = []
        for uptake in uptake_levels:
            row = uptake_emphatic[(uptake_emphatic['model'] == model) & 
                                 (uptake_emphatic['deictic_uptake_quality'] == uptake)]
            if not row.empty:
                values.append(row[('emphatic_ratio', 'mean')].values[0])
                errors.append(row[('emphatic_ratio', 'std')].values[0])
            else:
                values.append(0)
                errors.append(0)
        
        ax2.bar(x2 + i*width, values, width, yerr=errors, 
               label=model, color=COLORS[model], capsize=5)
    
    ax2.set_xlabel('Deictic Uptake Quality', fontsize=12)
    ax2.set_ylabel('Emphatic Ratio', fontsize=12)
    ax2.set_title('Emphatic Usage by Uptake Quality', fontsize=14, fontweight='bold')
    ax2.set_xticks(x2 + width/2)
    ax2.set_xticklabels(['Strong', 'Partial', 'Weak'])
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel 3: Uptake quality by solution preference
    ax3 = fig.add_subplot(gs[1, 1])
    
    solution_uptake = yoruba_merged.groupby(['preferred_solution', 'deictic_uptake_quality']).size().reset_index(name='count')
    solution_pivot = solution_uptake.pivot(index='preferred_solution', 
                                          columns='deictic_uptake_quality', 
                                          values='count').fillna(0)
    
    # Normalize to percentages
    solution_norm = solution_pivot.div(solution_pivot.sum(axis=1), axis=0) * 100
    
    solution_norm.plot(kind='barh', stacked=True, ax=ax3, 
                      color=[COLORS['strong'], COLORS['partial'], COLORS['weak']])
    ax3.set_xlabel('Percentage', fontsize=12)
    ax3.set_ylabel('Solution Preference', fontsize=12)
    ax3.set_title('Uptake Quality by Decision Type', fontsize=14, fontweight='bold')
    ax3.legend(title='Uptake Quality', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Deictic Uptake Patterns: How Well Models Maintain Framing in Yoruba', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "04_deictic_uptake_divergence.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 04_deictic_uptake_divergence.png")

def create_language_stability_matrix(yoruba_merged):
    """Visualize language stability patterns unique to Yoruba."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: Language stability by model and framing
    stability_data = yoruba_merged.groupby(['framing_type', 'language_stability', 'model']).size().reset_index(name='count')
    
    # Create heatmap data
    models = MODELS
    framings = ['impersonal', 'second_person', 'first_person', 'reflexive', 'dialogic', 
                'spatial', 'temporal', 'cosmological', 'first_person_plural']
    stability_levels = ['clean_yoruba', 'minor_interference', 'significant_interference']
    
    for idx, model in enumerate(models):
        ax = ax1 if idx == 0 else ax2
        
        # Create matrix
        matrix = np.zeros((len(framings), len(stability_levels)))
        
        for i, framing in enumerate(framings):
            for j, stability in enumerate(stability_levels):
                total = stability_data[(stability_data['model'] == model) & 
                                     (stability_data['framing_type'] == framing)]['count'].sum()
                count = stability_data[(stability_data['model'] == model) & 
                                     (stability_data['framing_type'] == framing) & 
                                     (stability_data['language_stability'] == stability)]['count'].values
                if count.size > 0 and total > 0:
                    matrix[i, j] = count[0] / total * 100
        
        im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=100)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(stability_levels)))
        ax.set_yticks(np.arange(len(framings)))
        ax.set_xticklabels(['Clean', 'Minor\nInterference', 'Significant\nInterference'])
        ax.set_yticklabels([f.replace('_', ' ') for f in framings])
        
        # Add text annotations
        for i in range(len(framings)):
            for j in range(len(stability_levels)):
                text = ax.text(j, i, f'{matrix[i, j]:.0f}%',
                             ha="center", va="center", 
                             color="white" if matrix[i, j] > 50 else "black")
        
        ax.set_title(f'{model} - Language Stability', fontsize=14, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Percentage', rotation=270, labelpad=20)
    
    # Panel 3: Language stability vs pronoun usage
    ax3.clear()
    
    stability_pronouns = yoruba_merged.groupby(['language_stability', 'model']).agg({
        'pronouns_per_100_words': ['mean', 'std'],
        'emphatic_ratio': 'mean'
    }).reset_index()
    
    x3 = np.arange(len(stability_levels))
    width = 0.35
    
    for i, model in enumerate(models):
        values = []
        errors = []
        for stability in stability_levels:
            row = stability_pronouns[(stability_pronouns['model'] == model) & 
                                   (stability_pronouns['language_stability'] == stability)]
            if not row.empty:
                values.append(row[('pronouns_per_100_words', 'mean')].values[0])
                errors.append(row[('pronouns_per_100_words', 'std')].values[0])
            else:
                values.append(0)
                errors.append(0)
        
        ax3.bar(x3 + i*width, values, width, yerr=errors, 
               label=model, color=COLORS[model], capsize=5)
    
    ax3.set_xlabel('Language Stability', fontsize=12)
    ax3.set_ylabel('Pronouns per 100 words', fontsize=12)
    ax3.set_title('Pronoun Usage by Language Stability', fontsize=14, fontweight='bold')
    ax3.set_xticks(x3 + width/2)
    ax3.set_xticklabels(['Clean', 'Minor', 'Significant'])
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel 4: Translation behavior patterns
    ax4.clear()
    
    translation_data = yoruba_merged.groupby(['model', 'contains_translation_behavior']).size().reset_index(name='count')
    
    # Calculate percentages
    for model in models:
        total = translation_data[translation_data['model'] == model]['count'].sum()
        has_translation = translation_data[(translation_data['model'] == model) & 
                                         (translation_data['contains_translation_behavior'] == True)]['count'].values
        percentage = (has_translation[0] / total * 100) if has_translation.size > 0 else 0
        
        ax4.bar(model, percentage, color=COLORS[model], width=0.6)
        ax4.text(model, percentage + 1, f'{percentage:.1f}%', ha='center', fontsize=12)
    
    ax4.set_ylabel('Percentage of Responses', fontsize=12)
    ax4.set_title('Translation Behavior Frequency', fontsize=14, fontweight='bold')
    ax4.set_ylim(0, max(20, ax4.get_ylim()[1]))
    ax4.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Language Stability Analysis: Yoruba-Specific Phenomena', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "05_language_stability_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 05_language_stability_matrix.png")

def create_commitment_patterns_cultural(yoruba_merged):
    """Compare commitment patterns showing cultural differences."""
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel 1: Solution preference distribution
    ax1 = fig.add_subplot(gs[0, :2])
    
    solution_data = yoruba_merged.groupby(['model', 'preferred_solution']).size().reset_index(name='count')
    
    solutions = ['supports_A', 'supports_B', 'conditional_or_mixed', 'refuses_to_commit']
    models = MODELS
    
    x = np.arange(len(solutions))
    width = 0.35
    
    for i, model in enumerate(models):
        values = []
        total = solution_data[solution_data['model'] == model]['count'].sum()
        for solution in solutions:
            count = solution_data[(solution_data['model'] == model) & 
                                (solution_data['preferred_solution'] == solution)]['count'].values
            percentage = (count[0] / total * 100) if count.size > 0 else 0
            values.append(percentage)
        
        ax1.bar(x + i*width, values, width, label=model, color=COLORS[model])
    
    ax1.set_xlabel('Solution Type', fontsize=12)
    ax1.set_ylabel('Percentage', fontsize=12)
    ax1.set_title('Decision Commitment Patterns in Yoruba', fontsize=14, fontweight='bold')
    ax1.set_xticks(x + width/2)
    ax1.set_xticklabels(['Supports A', 'Supports B', 'Conditional/\nMixed', 'Refuses to\nCommit'])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Emphatic usage at decision points
    ax2 = fig.add_subplot(gs[0, 2])
    
    decision_emphatic = yoruba_merged.groupby(['preferred_solution']).agg({
        'emphatic_ratio': 'mean',
        'first_singular_emi_per_100w': 'mean'
    }).reset_index()
    
    # Sort by emphatic ratio
    decision_emphatic = decision_emphatic.sort_values('emphatic_ratio', ascending=True)
    
    ax2.barh(decision_emphatic['preferred_solution'], 
             decision_emphatic['emphatic_ratio'],
             color=['#264653', '#2a9d8f', '#e9c46a', '#e76f51'])
    
    ax2.set_xlabel('Emphatic Ratio', fontsize=12)
    ax2.set_ylabel('Solution Type', fontsize=12)
    ax2.set_title('Emphatic Usage by\nDecision Type', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Panel 3: Framework usage by commitment type
    ax3 = fig.add_subplot(gs[1, :])
    
    framework_solution = yoruba_merged.groupby(['preferred_solution', 'ethical_preference_type']).size().reset_index(name='count')
    
    # Get top frameworks
    top_frameworks = yoruba_merged['ethical_preference_type'].value_counts().head(6).index
    
    # Create grouped bar chart
    solutions_short = ['A', 'B', 'Mixed', 'Refuse']
    x3 = np.arange(len(solutions_short))
    width3 = 0.15
    
    for i, framework in enumerate(top_frameworks):
        values = []
        for j, solution in enumerate(solutions):
            total = framework_solution[framework_solution['preferred_solution'] == solution]['count'].sum()
            count = framework_solution[(framework_solution['preferred_solution'] == solution) & 
                                     (framework_solution['ethical_preference_type'] == framework)]['count'].values
            percentage = (count[0] / total * 100) if count.size > 0 and total > 0 else 0
            values.append(percentage)
        
        ax3.bar(x3 + i*width3, values, width3, label=framework)
    
    ax3.set_xlabel('Solution Type', fontsize=12)
    ax3.set_ylabel('Percentage within Solution Type', fontsize=12)
    ax3.set_title('Ethical Framework Distribution by Commitment Type', fontsize=14, fontweight='bold')
    ax3.set_xticks(x3 + width3*2.5)
    ax3.set_xticklabels(solutions_short)
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Commitment Patterns: Cultural Differences in Moral Certainty', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "06_commitment_patterns_cultural.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 06_commitment_patterns_cultural.png")

def create_comprehensive_summary_dashboard(yoruba_merged):
    """Create a comprehensive dashboard summarizing key findings."""
    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel 1: Key metrics overview
    ax1 = fig.add_subplot(gs[0, 0])
    
    metrics = yoruba_merged.groupby('model').agg({
        'word_count': 'mean',
        'pronouns_per_100_words': 'mean',
        'emphatic_ratio': 'mean'
    }).reset_index()
    
    models = MODELS
    x = np.arange(3)
    width = 0.35
    
    for i, model in enumerate(models):
        model_data = metrics[metrics['model'] == model]
        if not model_data.empty:
            values = [
                model_data['word_count'].values[0] / 10,  # Scale down for visualization
                model_data['pronouns_per_100_words'].values[0] * 10,
                model_data['emphatic_ratio'].values[0] * 100
            ]
            ax1.bar(x + i*width, values, width, label=model, color=COLORS[model])
    
    ax1.set_xticks(x + width/2)
    ax1.set_xticklabels(['Avg Words\n(÷10)', 'Pronouns/100w\n(×10)', 'Emphatic %\n(×100)'])
    ax1.set_ylabel('Value', fontsize=12)
    ax1.set_title('Key Metrics Overview', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Mo vs Emi distribution
    ax2 = fig.add_subplot(gs[0, 1])
    
    pronoun_dist = yoruba_merged.groupby('model').agg({
        'first_singular_mo_per_100w': 'sum',
        'first_singular_emi_per_100w': 'sum'
    }).reset_index()
    
    for model in models:
        model_data = pronoun_dist[pronoun_dist['model'] == model]
        if not model_data.empty:
            sizes = [model_data['first_singular_mo_per_100w'].values[0],
                    model_data['first_singular_emi_per_100w'].values[0]]
            if sum(sizes) > 0:
                ax2.pie(sizes, labels=['Mo', 'Emi'], autopct='%1.1f%%',
                       colors=[COLORS['regular'], COLORS['emphasis']],
                       startangle=90)
                ax2.set_title(f'{model}\nMo vs Emi Distribution', fontsize=12)
                break
    
    # Panel 3: Language stability overview
    ax3 = fig.add_subplot(gs[0, 2])
    
    stability_summary = yoruba_merged.groupby(['model', 'language_stability']).size().reset_index(name='count')
    
    # Create stacked bar
    stability_levels = ['clean_yoruba', 'minor_interference', 'significant_interference']
    bottom = np.zeros(len(models))
    
    for stability in stability_levels:
        values = []
        for model in models:
            total = stability_summary[stability_summary['model'] == model]['count'].sum()
            count = stability_summary[(stability_summary['model'] == model) & 
                                    (stability_summary['language_stability'] == stability)]['count'].values
            percentage = (count[0] / total * 100) if count.size > 0 else 0
            values.append(percentage)
        
        color = COLORS[stability.split('_')[0]]
        ax3.bar(models, values, bottom=bottom, label=stability.replace('_', ' ').title(), color=color)
        bottom += np.array(values)
    
    ax3.set_ylabel('Percentage', fontsize=12)
    ax3.set_title('Language Stability', fontsize=14, fontweight='bold')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel 4-6: Framework distribution
    ax4 = fig.add_subplot(gs[1, :])
    
    framework_data = yoruba_merged.groupby(['model', 'ethical_preference_type']).size().reset_index(name='count')
    top_frameworks = yoruba_merged['ethical_preference_type'].value_counts().head(8).index
    
    framework_matrix = []
    for model in models:
        row = []
        total = framework_data[framework_data['model'] == model]['count'].sum()
        for framework in top_frameworks:
            count = framework_data[(framework_data['model'] == model) & 
                                 (framework_data['ethical_preference_type'] == framework)]['count'].values
            percentage = (count[0] / total * 100) if count.size > 0 else 0
            row.append(percentage)
        framework_matrix.append(row)
    
    im = ax4.imshow(framework_matrix, cmap='YlOrRd', aspect='auto')
    ax4.set_xticks(np.arange(len(top_frameworks)))
    ax4.set_yticks(np.arange(len(models)))
    ax4.set_xticklabels(top_frameworks, rotation=45, ha='right')
    ax4.set_yticklabels(models)
    ax4.set_title('Ethical Framework Distribution (%)', fontsize=14, fontweight='bold')
    
    # Add text annotations
    for i in range(len(models)):
        for j in range(len(top_frameworks)):
            text = ax4.text(j, i, f'{framework_matrix[i][j]:.1f}',
                          ha="center", va="center", color="black" if framework_matrix[i][j] < 20 else "white")
    
    plt.colorbar(im, ax=ax4, orientation='horizontal', pad=0.1)
    
    # Panel 7-9: Solution preferences and uptake quality
    ax7 = fig.add_subplot(gs[2, 0])
    
    solution_summary = yoruba_merged['preferred_solution'].value_counts()
    ax7.pie(solution_summary.values, labels=solution_summary.index, autopct='%1.1f%%',
            colors=['#264653', '#2a9d8f', '#e9c46a', '#e76f51'])
    ax7.set_title('Overall Solution Distribution', fontsize=14, fontweight='bold')
    
    # Panel 8: Uptake quality summary
    ax8 = fig.add_subplot(gs[2, 1])
    
    uptake_summary = yoruba_merged['deictic_uptake_quality'].value_counts()
    ax8.pie(uptake_summary.values, labels=['Strong', 'Partial', 'Weak'], autopct='%1.1f%%',
            colors=[COLORS['strong'], COLORS['partial'], COLORS['weak']])
    ax8.set_title('Deictic Uptake Quality', fontsize=14, fontweight='bold')
    
    # Panel 9: Response genre summary
    ax9 = fig.add_subplot(gs[2, 2])
    
    genre_summary = yoruba_merged['response_genre'].value_counts()
    ax9.barh(genre_summary.index[:5], genre_summary.values[:5], 
             color=['#264653', '#e76f51', '#e9c46a', '#f4a261', '#2a9d8f'])
    ax9.set_xlabel('Count', fontsize=12)
    ax9.set_title('Top Response Genres', fontsize=14, fontweight='bold')
    ax9.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Yoruba Deixis Analysis: Comprehensive Summary Dashboard', 
                fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "07_comprehensive_summary_dashboard.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 07_comprehensive_summary_dashboard.png")

def main():
    """Main function."""
    print("Loading data...")
    yoruba_merged = load_data()
    
    print("Creating additional visualizations...")
    
    create_deictic_uptake_divergence(yoruba_merged)
    create_language_stability_matrix(yoruba_merged)
    create_commitment_patterns_cultural(yoruba_merged)
    create_comprehensive_summary_dashboard(yoruba_merged)
    
    print("\nAdditional visualizations complete!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()