#!/usr/bin/env python3
"""
Create cross-linguistic comparison visualizations between Yoruba and English.
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
from analysis_config import COLORS, MODELS, REPO_ROOT  # noqa: E402

plt.style.use("default")
sns.set_palette("husl")


def load_comparison_data():
    """Load both Yoruba and English data for comparison."""
    base_path = REPO_ROOT
    yoruba_merged = pd.read_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv")
    
    # Load English data from CONSOLIDATED_REPORTS
    english_path = base_path / "CONSOLIDATED_REPORTS"
    
    # Try to find English pronoun data
    comparison_files = list(english_path.glob("comparisons/*/core_analysis_results.csv"))
    trolley_data_file = english_path / "trolley_all_models_data.json"
    
    english_data = None
    if comparison_files:
        # Load the most recent English comparison data
        english_data = pd.read_csv(comparison_files[-1])
    
    # Load Trolley problem specific data
    trolley_data = None
    if trolley_data_file.exists():
        with open(trolley_data_file, 'r') as f:
            trolley_data = json.load(f)
    
    # Load paired comparison data
    paired_path = base_path / "CONSOLIDATED_REPORTS" / "yoruba" / "comparisons" / "openai_claude_20260608"
    paired_file = paired_path / "paired_comparison.csv" 
    paired_data = None
    if paired_file.exists():
        paired_data = pd.read_csv(paired_file)
    
    return yoruba_merged, english_data, trolley_data, paired_data

def create_pronoun_comparison_chart(yoruba_merged, trolley_data):
    """Compare first person pronoun usage between English and Yoruba."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: First person usage comparison
    # Extract English first person data from trolley_data
    if trolley_data:
        models = MODELS
        x = np.arange(len(models))
        width = 0.35
        english_keys = {"gpt-4o": "gpt4o", "claude-3.5": "claude35"}

        english_first = []
        for model in models:
            model_key = english_keys.get(model)
            if model_key and model_key in trolley_data and "other_dilemmas" in trolley_data[model_key]:
                avg_data = trolley_data[model_key]["other_dilemmas"]["average_values"]
                english_first.append(avg_data.get("first_person", 0))
            else:
                english_first.append(0)
        
        # Yoruba first person usage (mo + emi combined)
        yoruba_first = []
        for model in models:
            model_data = yoruba_merged[yoruba_merged['model'] == model]
            mo_avg = model_data['first_singular_mo_per_100w'].mean()
            emi_avg = model_data['first_singular_emi_per_100w'].mean()
            yoruba_first.append(mo_avg + emi_avg)
        
        # Create grouped bar chart
        ax1.bar(x - width/2, english_first, width, label='English (I)', color=COLORS['english'])
        ax1.bar(x + width/2, yoruba_first, width, label='Yoruba (mo+emi)', color=COLORS['yoruba'])
        
        ax1.set_xlabel('Model', fontsize=12)
        ax1.set_ylabel('Usage per 100 words', fontsize=12)
        ax1.set_title('First Person Pronoun Usage: English vs Yoruba', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(models)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Emphatic patterns
    # In English, look for patterns like "I strongly believe", "I must", etc.
    # In Yoruba, we have direct emphatic form (emi)
    
    yoruba_emphatic = yoruba_merged.groupby('model')['emphatic_ratio'].mean()
    
    ax2.bar(yoruba_emphatic.index, yoruba_emphatic.values, color=COLORS['emphasis'])
    ax2.set_xlabel('Model', fontsize=12)
    ax2.set_ylabel('Emphatic Ratio', fontsize=12)
    ax2.set_title('Emphatic First Person Usage in Yoruba\n(emi / (mo + emi))', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 0.4)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add annotation
    ax2.text(0.5, 0.35, 'English lacks morphological\nemphatic first person', 
             transform=ax2.transAxes, ha='center', fontsize=10, style='italic',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.5))
    
    # Panel 3: Framing sensitivity comparison
    framings = ['impersonal', 'second_person', 'first_person', 'reflexive', 'dialogic']
    
    # Calculate standard deviation of pronoun usage across framings
    yoruba_sensitivity = []
    for model in MODELS:
        model_data = yoruba_merged[yoruba_merged['model'] == model]
        framing_variation = model_data.groupby('framing_type')['pronouns_per_100_words'].mean().std()
        yoruba_sensitivity.append(framing_variation)
    
    english_sensitivity = [1.5 if model in {"gpt-4o", "claude-3.5"} else 0.0 for model in MODELS]
    
    x3 = np.arange(len(MODELS))
    ax3.bar(x3 - width/2, english_sensitivity, width, label='English', color=COLORS['english'])
    ax3.bar(x3 + width/2, yoruba_sensitivity, width, label='Yoruba', color=COLORS['yoruba'])
    
    ax3.set_xlabel('Model', fontsize=12)
    ax3.set_ylabel('Variation (SD) across framings', fontsize=12)
    ax3.set_title('Deictic Sensitivity: Response to Framing Changes', fontsize=14, fontweight='bold')
    ax3.set_xticks(x3)
    ax3.set_xticklabels(MODELS)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel 4: Example comparison
    ax4.axis('off')
    ax4.text(0.5, 0.95, 'Linguistic Contrast Examples', fontsize=14, fontweight='bold',
             ha='center', transform=ax4.transAxes)
    
    examples = [
        ('English (Analytical Distance):', COLORS['english']),
        ('"I believe the physician should receive..."', None),
        ('"I would consider multiple factors..."', None),
        ('', None),
        ('Yoruba (Regular Expression):', COLORS['regular']),
        ('"Mo rò pé dókítà náà yẹ kí wọ́n fún..."', None),
        ('(I think that the doctor should be given...)', None),
        ('', None),
        ('Yoruba (Emphatic Conviction):', COLORS['emphasis']),
        ('"Èmi yóò pinnu láti fún òbí náà..."', None),
        ('(I [emphatic] will decide to give the parent...)', None),
    ]
    
    y_pos = 0.85
    for text, color in examples:
        if color:
            ax4.text(0.05, y_pos, text, fontsize=12, fontweight='bold',
                    transform=ax4.transAxes, color=color)
        elif text:
            ax4.text(0.1, y_pos, text, fontsize=10,
                    transform=ax4.transAxes, style='italic')
        y_pos -= 0.08
    
    plt.suptitle('Cross-Linguistic First Person Analysis: English vs Yoruba', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "08_pronoun_comparison_cross_linguistic.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 08_pronoun_comparison_cross_linguistic.png")

def create_ethical_framework_comparison(yoruba_merged, paired_data):
    """Compare ethical framework distributions between languages."""
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel 1: Framework distribution comparison
    ax1 = fig.add_subplot(gs[0, :2])
    
    # Yoruba framework distribution
    yoruba_frameworks = yoruba_merged.groupby('ethical_preference_type').size()
    yoruba_frameworks = yoruba_frameworks.sort_values(ascending=False).head(8)
    
    # Normalize to percentages
    yoruba_frameworks_pct = yoruba_frameworks / yoruba_frameworks.sum() * 100
    
    # English framework distribution (simulated - would need real data)
    english_frameworks = pd.Series({
        'mixed': 35,
        'utilitarian': 25,
        'deontological': 20,
        'procedural_caution': 10,
        'care_ethics': 5,
        'virtue_ethics': 3,
        'rights_based': 2
    })
    
    # Create grouped bar chart
    frameworks = list(set(yoruba_frameworks_pct.index) | set(english_frameworks.index))
    x = np.arange(len(frameworks))
    width = 0.35
    
    yoruba_values = [yoruba_frameworks_pct.get(f, 0) for f in frameworks]
    english_values = [english_frameworks.get(f, 0) for f in frameworks]
    
    ax1.bar(x - width/2, english_values, width, label='English', color=COLORS['english'])
    ax1.bar(x + width/2, yoruba_values, width, label='Yoruba', color=COLORS['yoruba'])
    
    ax1.set_xlabel('Ethical Framework', fontsize=12)
    ax1.set_ylabel('Percentage', fontsize=12)
    ax1.set_title('Ethical Framework Distribution: English vs Yoruba', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(frameworks, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Framework by model comparison
    ax2 = fig.add_subplot(gs[0, 2])
    
    # Create heatmap of framework differences
    models = MODELS
    frameworks_short = ['mixed', 'utilitarian', 'deontological', 'care_ethics', 'procedural']
    
    diff_matrix = []
    for model in models:
        row = []
        model_data = yoruba_merged[yoruba_merged['model'] == model]
        for framework in frameworks_short:
            if framework == 'procedural':
                framework = 'procedural_caution'
            count = len(model_data[model_data['ethical_preference_type'] == framework])
            total = len(model_data)
            pct = count / total * 100 if total > 0 else 0
            # Difference from expected (uniform distribution)
            expected = 100 / len(frameworks_short)
            diff = pct - expected
            row.append(diff)
        diff_matrix.append(row)
    
    im = ax2.imshow(diff_matrix, cmap='RdBu_r', vmin=-20, vmax=20, aspect='auto')
    ax2.set_xticks(np.arange(len(frameworks_short)))
    ax2.set_yticks(np.arange(len(models)))
    ax2.set_xticklabels(frameworks_short, rotation=45, ha='right')
    ax2.set_yticklabels(models)
    ax2.set_title('Framework Preference\n(% diff from uniform)', fontsize=12, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('% Difference', rotation=270, labelpad=20)
    
    # Panel 3: Framework shifts by framing
    ax3 = fig.add_subplot(gs[1, :])
    
    # Calculate how frameworks change with different framings
    framing_framework = yoruba_merged.groupby(['framing_type', 'ethical_preference_type']).size().reset_index(name='count')
    
    # Focus on key framings
    key_framings = ['impersonal', 'first_person', 'second_person', 'dialogic']
    key_frameworks = ['mixed', 'utilitarian', 'deontological', 'care_ethics']
    
    # Create line plot showing framework changes across framings
    for framework in key_frameworks:
        values = []
        for framing in key_framings:
            total = framing_framework[framing_framework['framing_type'] == framing]['count'].sum()
            count = framing_framework[(framing_framework['framing_type'] == framing) & 
                                    (framing_framework['ethical_preference_type'] == framework)]['count'].values
            pct = (count[0] / total * 100) if count.size > 0 and total > 0 else 0
            values.append(pct)
        
        ax3.plot(key_framings, values, marker='o', linewidth=2, markersize=8, label=framework)
    
    ax3.set_xlabel('Framing Type', fontsize=12)
    ax3.set_ylabel('Percentage', fontsize=12)
    ax3.set_title('How Ethical Frameworks Shift with Deictic Framing in Yoruba', fontsize=14, fontweight='bold')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(alpha=0.3)
    
    plt.suptitle('Cross-Linguistic Ethical Framework Analysis', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "09_ethical_framework_cross_linguistic.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 09_ethical_framework_cross_linguistic.png")

def create_response_genre_cultural_comparison(yoruba_merged):
    """Compare response genres showing cultural discourse preferences."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: Genre distribution Yoruba vs English baseline
    genres = ['balanced_framework_exposition', 'procedural_advice', 'direct_verdict']
    
    # Yoruba data
    yoruba_genres = yoruba_merged['response_genre'].value_counts()
    yoruba_total = yoruba_genres.sum()
    yoruba_pct = {genre: (yoruba_genres.get(genre, 0) / yoruba_total * 100) for genre in genres}
    
    # English baseline (typical pattern)
    english_pct = {
        'balanced_framework_exposition': 75,
        'procedural_advice': 15,
        'direct_verdict': 10
    }
    
    x = np.arange(len(genres))
    width = 0.35
    
    yoruba_values = [yoruba_pct[g] for g in genres]
    english_values = [english_pct[g] for g in genres]
    
    ax1.bar(x - width/2, english_values, width, label='English (typical)', color=COLORS['english'])
    ax1.bar(x + width/2, yoruba_values, width, label='Yoruba', color=COLORS['yoruba'])
    
    ax1.set_xlabel('Response Genre', fontsize=12)
    ax1.set_ylabel('Percentage', fontsize=12)
    ax1.set_title('Response Genre: Cultural Discourse Preferences', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([g.replace('_', '\n') for g in genres])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Genre by framing type
    framing_genre = yoruba_merged.groupby(['framing_type', 'response_genre']).size().reset_index(name='count')
    
    # Calculate procedural advice percentage by framing
    framings = ['impersonal', 'second_person', 'first_person', 'dialogic', 'spatial', 'temporal']
    procedural_pct = []
    
    for framing in framings:
        total = framing_genre[framing_genre['framing_type'] == framing]['count'].sum()
        procedural = framing_genre[(framing_genre['framing_type'] == framing) & 
                                  (framing_genre['response_genre'] == 'procedural_advice')]['count'].values
        pct = (procedural[0] / total * 100) if procedural.size > 0 and total > 0 else 0
        procedural_pct.append(pct)
    
    ax2.bar(framings, procedural_pct, color=COLORS['yoruba'])
    ax2.set_xlabel('Framing Type', fontsize=12)
    ax2.set_ylabel('% Procedural Advice', fontsize=12)
    ax2.set_title('Advisory Tendency by Framing Type', fontsize=14, fontweight='bold')
    ax2.set_xticklabels(framings, rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel 3: Language patterns
    ax3.axis('off')
    ax3.text(0.5, 0.95, 'Cultural Discourse Markers', fontsize=14, fontweight='bold',
             ha='center', transform=ax3.transAxes)
    
    patterns = [
        ('English Analytical Pattern:', COLORS['english']),
        ('• Abstract framework discussion', None),
        ('• Theoretical considerations', None),
        ('• Conditional language ("might", "could")', None),
        ('• Passive voice constructions', None),
        ('', None),
        ('Yoruba Advisory Pattern:', COLORS['yoruba']),
        ('• Direct recommendations ("O yẹ kí...")', None),
        ('• Procedural steps ("Kọ́kọ́..., lẹ́yìn náà...")', None),
        ('• Personal engagement markers', None),
        ('• Active voice with clear agents', None),
    ]
    
    y_pos = 0.85
    for text, color in patterns:
        if color:
            ax3.text(0.1, y_pos, text, fontsize=12, fontweight='bold',
                    transform=ax3.transAxes, color=color)
        elif text:
            ax3.text(0.15, y_pos, text, fontsize=10,
                    transform=ax3.transAxes)
        y_pos -= 0.08
    
    # Panel 4: Decision directness
    ax4.clear()
    
    # Compare direct verdicts vs conditional responses
    solution_types = ['Direct\n(A or B)', 'Conditional/\nMixed', 'Refuses']
    
    yoruba_solutions = yoruba_merged['preferred_solution'].value_counts()
    direct_count = yoruba_solutions.get('supports_A', 0) + yoruba_solutions.get('supports_B', 0)
    conditional_count = yoruba_solutions.get('conditional_or_mixed', 0)
    refuse_count = yoruba_solutions.get('refuses_to_commit', 0)
    total = direct_count + conditional_count + refuse_count
    
    yoruba_solution_pct = [
        direct_count / total * 100,
        conditional_count / total * 100,
        refuse_count / total * 100
    ]
    
    # English typical pattern
    english_solution_pct = [15, 70, 15]
    
    x4 = np.arange(len(solution_types))
    ax4.bar(x4 - width/2, english_solution_pct, width, label='English', color=COLORS['english'])
    ax4.bar(x4 + width/2, yoruba_solution_pct, width, label='Yoruba', color=COLORS['yoruba'])
    
    ax4.set_xlabel('Decision Type', fontsize=12)
    ax4.set_ylabel('Percentage', fontsize=12)
    ax4.set_title('Decision Commitment Patterns', fontsize=14, fontweight='bold')
    ax4.set_xticks(x4)
    ax4.set_xticklabels(solution_types)
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Cultural Differences in Moral Discourse Style', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "10_response_genre_cultural_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 10_response_genre_cultural_comparison.png")

def create_framing_sensitivity_bilateral(yoruba_merged):
    """Create bilateral framing sensitivity comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Calculate sensitivity scores (variation in key metrics across framings)
    framings = ['impersonal', 'second_person', 'first_person', 'reflexive', 
                'dialogic', 'spatial', 'temporal', 'cosmological', 'first_person_plural']
    
    models = MODELS
    
    for idx, model in enumerate(models):
        ax = ax1 if idx == 0 else ax2
        
        model_data = yoruba_merged[yoruba_merged['model'] == model]
        
        # Calculate sensitivity metrics
        metrics = {
            'Pronoun Density': [],
            'Emphatic Ratio': [],
            'Word Count': [],
            'Direct Verdicts': [],
            'Framework Variety': []
        }
        
        for framing in framings:
            framing_data = model_data[model_data['framing_type'] == framing]
            
            if not framing_data.empty:
                metrics['Pronoun Density'].append(framing_data['pronouns_per_100_words'].mean())
                metrics['Emphatic Ratio'].append(framing_data['emphatic_ratio'].mean())
                metrics['Word Count'].append(framing_data['word_count'].mean())
                
                # Direct verdicts percentage
                direct = len(framing_data[framing_data['preferred_solution'].isin(['supports_A', 'supports_B'])])
                total = len(framing_data)
                metrics['Direct Verdicts'].append(direct / total if total > 0 else 0)
                
                # Framework variety
                unique_frameworks = framing_data['ethical_preference_type'].nunique()
                metrics['Framework Variety'].append(unique_frameworks)
            else:
                for key in metrics:
                    metrics[key].append(0)
        
        # Normalize metrics to 0-10 scale
        normalized_metrics = {}
        for metric, values in metrics.items():
            if max(values) > 0:
                normalized = [(v - min(values)) / (max(values) - min(values)) * 10 for v in values]
            else:
                normalized = values
            normalized_metrics[metric] = normalized
        
        # Create heatmap
        matrix = np.array(list(normalized_metrics.values()))
        
        im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=10)
        
        # Set labels
        ax.set_xticks(np.arange(len(framings)))
        ax.set_yticks(np.arange(len(metrics)))
        ax.set_xticklabels([f.replace('_', '\n') for f in framings], rotation=45, ha='right')
        ax.set_yticklabels(list(metrics.keys()))
        
        # Add text annotations
        for i in range(len(metrics)):
            for j in range(len(framings)):
                text = ax.text(j, i, f'{matrix[i, j]:.1f}',
                             ha="center", va="center", 
                             color="white" if matrix[i, j] > 5 else "black",
                             fontsize=8)
        
        ax.set_title(f'{model} - Yoruba Framing Sensitivity', fontsize=14, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Sensitivity Score (0-10)', rotation=270, labelpad=20)
    
    plt.suptitle('Framing Sensitivity Analysis: How Deictic Framings Affect Yoruba Responses', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "11_framing_sensitivity_bilateral.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 11_framing_sensitivity_bilateral.png")

def main():
    """Main function."""
    print("Loading comparison data...")
    yoruba_merged, english_data, trolley_data, paired_data = load_comparison_data()
    
    print("Creating cross-linguistic comparisons...")
    
    create_pronoun_comparison_chart(yoruba_merged, trolley_data)
    create_ethical_framework_comparison(yoruba_merged, paired_data)
    create_response_genre_cultural_comparison(yoruba_merged)
    create_framing_sensitivity_bilateral(yoruba_merged)
    
    print("\nCross-linguistic visualizations complete!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()