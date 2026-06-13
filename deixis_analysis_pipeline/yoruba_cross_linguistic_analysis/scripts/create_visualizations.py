#!/usr/bin/env python3
"""
Create visualizations for Yoruba deixis analysis focusing on interesting linguistic contrasts.
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac
from analysis_config import COLORS, FRAMING_ORDER, MODELS  # noqa: E402

plt.style.use("default")
sns.set_palette("husl")


def load_analysis_data():
    """Load all necessary data for visualization."""
    data_path = ac.DATA_DIR
    
    # Load merged Yoruba data
    yoruba_merged = pd.read_csv(data_path / "yoruba_merged_analysis.csv")
    
    # Load pronoun detailed data
    with open(data_path / "yoruba_pronoun_detailed.json", 'r', encoding='utf-8') as f:
        pronoun_details = json.load(f)
    
    # Load statistics
    stats = {}
    for stat_file in data_path.glob("stats_*.csv"):
        key = stat_file.stem.replace("stats_", "")
        stats[key] = pd.read_csv(stat_file, index_col=0)
    
    return yoruba_merged, pronoun_details, stats

def create_emphatic_first_person_analysis(yoruba_merged, pronoun_details):
    """Create the most revealing visualization showing mo vs emi usage patterns."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: Mo vs Emi usage across framings
    framing_data = yoruba_merged.groupby(['framing_type', 'model']).agg({
        'first_singular_mo_per_100w': 'mean',
        'first_singular_emi_per_100w': 'mean',
        'emphatic_ratio': 'mean'
    }).reset_index()
    
    framings = FRAMING_ORDER

    x = np.arange(len(framings))
    group_width = 0.8
    width = group_width / len(MODELS)

    for i, model in enumerate(MODELS):
        model_data = framing_data[framing_data['model'] == model]
        mo_values = []
        emi_values = []
        
        for framing in framings:
            row = model_data[model_data['framing_type'] == framing]
            if not row.empty:
                mo_values.append(row['first_singular_mo_per_100w'].values[0])
                emi_values.append(row['first_singular_emi_per_100w'].values[0])
            else:
                mo_values.append(0)
                emi_values.append(0)
        
        offset = (i - (len(MODELS) - 1) / 2) * width
        ax1.bar(x + offset, mo_values, width / 2, label=f"{model} mo", color=COLORS[model], alpha=0.6)
        ax1.bar(
            x + offset + width / 2,
            emi_values,
            width / 2,
            label=f"{model} emi",
            color=COLORS[model],
            alpha=1.0,
            edgecolor="black",
            linewidth=1,
        )
    
    ax1.set_xlabel('Framing Type', fontsize=12)
    ax1.set_ylabel('Usage per 100 words', fontsize=12)
    ax1.set_title('Mo (regular I) vs Emi (emphatic I) Usage Patterns', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f.replace('_', '\n') for f in framings], rotation=45, ha='right')
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Emphatic ratio by ethical framework
    ethics_data = yoruba_merged.groupby(['ethical_preference_type', 'model']).agg({
        'emphatic_ratio': ['mean', 'count']
    }).reset_index()
    
    # Filter for frameworks with enough data
    ethics_data = ethics_data[ethics_data[('emphatic_ratio', 'count')] > 2]
    
    # Create grouped bar chart
    frameworks = ethics_data['ethical_preference_type'].unique()
    x2 = np.arange(len(frameworks))
    
    bar_width = group_width / len(MODELS)
    for i, model in enumerate(MODELS):
        model_data = ethics_data[ethics_data['model'] == model]
        values = []
        for framework in frameworks:
            row = model_data[model_data['ethical_preference_type'] == framework]
            if not row.empty:
                values.append(row[('emphatic_ratio', 'mean')].values[0])
            else:
                values.append(0)

        ax2.bar(x2 + (i - (len(MODELS) - 1) / 2) * bar_width, values, bar_width, label=model, color=COLORS[model])

    ax2.set_xlabel('Ethical Framework', fontsize=12)
    ax2.set_ylabel('Emphatic Ratio (emi/(mo+emi))', fontsize=12)
    ax2.set_title('Emphatic First Person by Ethical Framework', fontsize=14, fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(frameworks, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(0, 1)
    
    # Panel 3: Context examples
    # Extract examples of mo vs emi usage
    examples = []
    natlas_sessions = [s for s in pronoun_details if s.get("model") == "n-atlas"]
    other_sessions = [s for s in pronoun_details if s.get("model") != "n-atlas"]
    for session in (natlas_sessions[:1] + other_sessions[:1]):
        if isinstance(session, dict) and 'responses' in session:
            for framing, data in session['responses'].items():
                if isinstance(data, dict):
                    if data.get('mo_contexts'):
                        examples.append(('mo', data['mo_contexts'][0] if data['mo_contexts'] else ''))
                    if data.get('emi_contexts'):
                        examples.append(('emi', data['emi_contexts'][0] if data['emi_contexts'] else ''))
    
    # Plot example contexts
    ax3.text(0.05, 0.95, "Example Contexts:", fontsize=12, fontweight='bold', 
             transform=ax3.transAxes, va='top')
    
    y_pos = 0.85
    for pronoun_type, context in examples[:6]:  # Show 6 examples
        if context:
            color = COLORS['emphasis'] if pronoun_type == 'emi' else COLORS['regular']
            # Highlight the pronoun in the context
            display_text = context[:100] + '...' if len(context) > 100 else context
            ax3.text(0.05, y_pos, f"{pronoun_type.upper()}: {display_text}", 
                    fontsize=10, transform=ax3.transAxes, va='top', 
                    color=color, wrap=True)
            y_pos -= 0.15
    
    ax3.axis('off')
    
    # Panel 4: Correlation with commitment patterns
    commitment_data = yoruba_merged.groupby(['preferred_solution', 'model']).agg({
        'emphatic_ratio': 'mean',
        'first_singular_mo_per_100w': 'mean',
        'first_singular_emi_per_100w': 'mean'
    }).reset_index()
    
    solutions = ['supports_A', 'supports_B', 'conditional_or_mixed', 'refuses_to_commit']
    
    # Create scatter plot
    markers = ["o", "s", "^", "D"]
    for mi, model in enumerate(MODELS):
        model_data = commitment_data[commitment_data["model"] == model]
        for solution in solutions:
            row = model_data[model_data["preferred_solution"] == solution]
            if not row.empty:
                x_val = row["first_singular_mo_per_100w"].values[0]
                y_val = row["first_singular_emi_per_100w"].values[0]
                ax4.scatter(
                    x_val,
                    y_val,
                    s=120,
                    color=COLORS[model],
                    marker=markers[mi % len(markers)],
                    alpha=0.8,
                )
                ax4.annotate(
                    f"{model[:3]}:{solution.split('_')[0]}",
                    (x_val, y_val),
                    fontsize=7,
                    ha="center",
                    va="bottom",
                )
    
    ax4.set_xlabel('Mo usage (per 100 words)', fontsize=12)
    ax4.set_ylabel('Emi usage (per 100 words)', fontsize=12)
    ax4.set_title('Pronoun Usage by Decision Commitment', fontsize=14, fontweight='bold')
    ax4.grid(alpha=0.3)
    
    # Add diagonal line for equal usage
    max_val = max(ax4.get_xlim()[1], ax4.get_ylim()[1])
    ax4.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='Equal usage')
    
    # Legend with custom markers
    direct_marker = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10)
    conditional_marker = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markersize=10)
    ax4.legend([direct_marker, conditional_marker], ['Direct verdict', 'Conditional'], 
              loc='upper right')
    
    plt.suptitle('Emphatic First Person Analysis: Mo vs Emi in Yoruba Ethical Discourse', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "01_emphatic_first_person_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()
    
    print("Created: 01_emphatic_first_person_analysis.png")

def create_moral_subjectivity_heatmap(yoruba_merged):
    """Create heatmap showing how pronouns correlate with ethical frameworks."""
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    axes = axes.flatten()
    
    # Prepare data for heatmap
    pronoun_types = ['first_singular_mo_per_100w', 'first_singular_emi_per_100w', 
                     'first_plural_a_per_100w', 'second_person_o_per_100w']
    frameworks = ['utilitarian', 'deontological', 'virtue_ethics', 'care_ethics', 
                  'mixed', 'procedural_caution']
    
    for idx, model in enumerate(MODELS):
        model_data = yoruba_merged[yoruba_merged["model"] == model]

        matrix = []
        for framework in frameworks:
            row = []
            framework_data = model_data[model_data["ethical_preference_type"] == framework]
            for pronoun in pronoun_types:
                if not framework_data.empty and pronoun in framework_data.columns:
                    value = framework_data[pronoun].mean()
                    row.append(value if not pd.isna(value) else 0)
                else:
                    row.append(0)
            matrix.append(row)

        matrix = np.array(matrix)
        ax = axes[idx]
        im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(pronoun_types)))
        ax.set_yticks(np.arange(len(frameworks)))
        ax.set_xticklabels(['Mo\n(regular I)', 'Emi\n(emphatic I)', 
                           'A\n(we)', 'O\n(you)'], rotation=0)
        ax.set_yticklabels(frameworks)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Usage per 100 words', rotation=270, labelpad=20)
        
        # Add text annotations
        for i in range(len(frameworks)):
            for j in range(len(pronoun_types)):
                text = ax.text(j, i, f'{matrix[i, j]:.1f}',
                             ha="center", va="center", color="black" if matrix[i, j] < matrix.max()/2 else "white")
        
        ax.set_title(f'{model} - Pronoun-Framework Correlation', fontsize=14, fontweight='bold')
        ax.set_xlabel('Pronoun Type', fontsize=12)
        ax.set_ylabel('Ethical Framework', fontsize=12)
    
    plt.suptitle('Moral Subjectivity: How Pronoun Choice Correlates with Ethical Frameworks', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "02_moral_subjectivity_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()
    
    print("Created: 02_moral_subjectivity_heatmap.png")

def create_advisory_vs_analytical_genre(yoruba_merged):
    """Compare response genres between Yoruba and show cultural differences."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: Genre distribution by model
    genre_data = yoruba_merged.groupby(['model', 'response_genre']).size().reset_index(name='count')
    
    models = MODELS
    genres = ["balanced_framework_exposition", "procedural_advice", "direct_verdict"]

    x = np.arange(len(models))
    width = 0.8 / len(genres)
    
    for i, genre in enumerate(genres):
        values = []
        for model in models:
            model_total = genre_data[genre_data['model'] == model]['count'].sum()
            genre_count = genre_data[(genre_data['model'] == model) & 
                                   (genre_data['response_genre'] == genre)]['count'].values
            percentage = (genre_count[0] / model_total * 100) if genre_count.size > 0 else 0
            values.append(percentage)
        
        color = ['#264653', '#e76f51', '#e9c46a'][i]
        ax1.bar(x + i*width, values, width, label=genre.replace('_', ' ').title(), color=color)
    
    ax1.set_xlabel('Model', fontsize=12)
    ax1.set_ylabel('Percentage of Responses', fontsize=12)
    ax1.set_title('Response Genre Distribution in Yoruba', fontsize=14, fontweight='bold')
    ax1.set_xticks(x + width)
    ax1.set_xticklabels(models)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Genre by deictic framing
    framing_genre = yoruba_merged.groupby(['framing_type', 'response_genre']).size().reset_index(name='count')
    framing_genre_pivot = framing_genre.pivot(index='framing_type', columns='response_genre', values='count').fillna(0)
    
    # Normalize to percentages
    framing_genre_norm = framing_genre_pivot.div(framing_genre_pivot.sum(axis=1), axis=0) * 100
    
    # Create stacked bar chart
    framing_genre_norm.plot(kind='bar', stacked=True, ax=ax2, 
                            color=['#264653', '#e76f51', '#e9c46a'])
    ax2.set_xlabel('Framing Type', fontsize=12)
    ax2.set_ylabel('Percentage', fontsize=12)
    ax2.set_title('Genre Distribution by Deictic Framing', fontsize=14, fontweight='bold')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel 3: Pronoun usage by genre
    genre_pronoun = yoruba_merged.groupby(['response_genre', 'model']).agg({
        'pronouns_per_100_words': 'mean',
        'emphatic_ratio': 'mean'
    }).reset_index()
    
    genres_ordered = ['procedural_advice', 'direct_verdict', 'balanced_framework_exposition']
    x3 = np.arange(len(genres_ordered))
    
    for i, model in enumerate(models):
        values = []
        for genre in genres_ordered:
            row = genre_pronoun[(genre_pronoun['model'] == model) & 
                               (genre_pronoun['response_genre'] == genre)]
            if not row.empty:
                values.append(row['pronouns_per_100_words'].values[0])
            else:
                values.append(0)
        
        ax3.bar(x3 + i*width*2, values, width*2, label=model, color=COLORS[model])
    
    ax3.set_xlabel('Response Genre', fontsize=12)
    ax3.set_ylabel('Total Pronouns per 100 words', fontsize=12)
    ax3.set_title('Pronoun Density by Response Genre', fontsize=14, fontweight='bold')
    ax3.set_xticks(x3 + width)
    ax3.set_xticklabels([g.replace('_', '\n') for g in genres_ordered])
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel 4: Cultural discourse markers
    ax4.text(0.05, 0.95, "Cultural Discourse Patterns:", fontsize=14, fontweight='bold', 
             transform=ax4.transAxes, va='top')
    
    patterns = [
        ("Advisory Pattern (Yoruba):", "#e76f51"),
        ("'O yẹ kí...' (It is fitting that...)", None),
        ("'Ó dára láti...' (It is good to...)", None),
        ("'Kí o má...' (So that you may...)", None),
        ("", None),
        ("Analytical Pattern (English baseline):", "#264653"),
        ("'One might consider...'", None),
        ("'The ethical implications...'", None),
        ("'From a utilitarian perspective...'", None)
    ]
    
    y_pos = 0.85
    for text, color in patterns:
        if color:
            ax4.text(0.05, y_pos, text, fontsize=12, fontweight='bold',
                    transform=ax4.transAxes, va='top', color=color)
        else:
            ax4.text(0.1, y_pos, text, fontsize=11, 
                    transform=ax4.transAxes, va='top', style='italic')
        y_pos -= 0.08
    
    ax4.axis('off')
    
    plt.suptitle('Advisory vs Analytical: Cultural Differences in Moral Discourse', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "03_advisory_vs_analytical_genre.png", dpi=300, bbox_inches="tight")
    plt.close()
    
    print("Created: 03_advisory_vs_analytical_genre.png")

def main():
    """Main visualization creation function."""
    print("Loading analysis data...")
    yoruba_merged, pronoun_details, stats = load_analysis_data()
    
    print("Creating visualizations...")
    
    # Create output directory if it doesn't exist
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create visualizations
    create_emphatic_first_person_analysis(yoruba_merged, pronoun_details)
    create_moral_subjectivity_heatmap(yoruba_merged)
    create_advisory_vs_analytical_genre(yoruba_merged)
    
    print("\nVisualization creation complete!")
    print(f"Files saved to: {ac.VIZ_DIR}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()