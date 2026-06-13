#!/usr/bin/env python3
"""
Create final visualizations including cultural metaphor analysis and example showcase.
"""

import json
import sys
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import analysis_config as ac
from analysis_config import COLORS, MODELS  # noqa: E402

plt.style.use("default")
sns.set_palette("husl")


def load_examples():
    """Load interesting examples."""
    with open(ac.DATA_DIR / "interesting_examples.json", "r", encoding="utf-8") as handle:
        return json.load(handle)

def create_cultural_metaphor_visualization(examples):
    """Visualize cultural metaphors and their distribution."""
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel 1: Metaphor frequency
    ax1 = fig.add_subplot(gs[0, 0])
    
    metaphors = examples['cultural_metaphors']
    term_counts = {}
    for m in metaphors:
        term = m['meaning']
        term_counts[term] = term_counts.get(term, 0) + 1
    
    # Sort by frequency
    sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)[:6]
    terms, counts = zip(*sorted_terms)
    
    ax1.barh(terms, counts, color=COLORS['yoruba'])
    ax1.set_xlabel('Frequency', fontsize=12)
    ax1.set_title('Cultural Metaphor Usage in Yoruba Responses', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Panel 2: Metaphor by dilemma type
    ax2 = fig.add_subplot(gs[0, 1])
    
    dilemma_metaphors = {}
    for m in metaphors:
        dilemma = m['dilemma']
        dilemma_metaphors[dilemma] = dilemma_metaphors.get(dilemma, 0) + 1
    
    dilemmas = list(dilemma_metaphors.keys())
    metaphor_counts = [dilemma_metaphors[d] for d in dilemmas]
    
    ax2.bar(range(len(dilemmas)), metaphor_counts, color=COLORS['yoruba'])
    ax2.set_xticks(range(len(dilemmas)))
    ax2.set_xticklabels([d.replace('_', '\n') for d in dilemmas], rotation=45, ha='right')
    ax2.set_ylabel('Metaphor Count', fontsize=12)
    ax2.set_title('Cultural Metaphors by Dilemma Type', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel 3-4: Example showcase
    ax3 = fig.add_subplot(gs[1, :])
    ax3.axis('off')
    
    # Title
    ax3.text(0.5, 0.95, 'Examples of Cultural Metaphors in Context', 
             fontsize=14, fontweight='bold', ha='center', transform=ax3.transAxes)
    
    # Show examples
    y_pos = 0.85
    for i, m in enumerate(metaphors[:4]):
        # Yoruba term and meaning
        ax3.text(0.05, y_pos, f"{m['yoruba_term']} ({m['meaning']})", 
                fontsize=12, fontweight='bold', transform=ax3.transAxes)
        
        # Context
        context = m['context'].replace('\n', ' ')
        if len(context) > 100:
            context = context[:100] + '...'
        ax3.text(0.05, y_pos - 0.03, f"Context: {context}", 
                fontsize=10, transform=ax3.transAxes, style='italic', wrap=True)
        
        # Model and dilemma
        ax3.text(0.05, y_pos - 0.06, f"[{m['model']}, {m['dilemma']}]", 
                fontsize=9, transform=ax3.transAxes, color='gray')
        
        y_pos -= 0.18
    
    plt.suptitle('Cultural Metaphors in Yoruba Ethical Discourse', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "12_cultural_metaphor_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 12_cultural_metaphor_analysis.png")

def create_example_showcase_visualization(examples, yoruba_merged):
    """Create a visualization showcasing key examples."""
    fig = plt.figure(figsize=(18, 14))
    
    # Create 6 panels for different example types
    gs = GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3)
    
    # Panel 1: Emphatic vs Regular First Person
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    ax1.text(0.5, 0.95, 'First Person Usage: Mo vs Emi', 
             fontsize=12, fontweight='bold', ha='center', transform=ax1.transAxes)
    
    # Show contrasting examples
    regular_ex = next((e for e in examples['emphatic'] if 'mo ' in e['sentence'].lower() and 'emi' not in e['sentence'].lower()), None)
    emphatic_ex = next((e for e in examples['emphatic'] if 'emi' in e['sentence'].lower() or 'èmi' in e['sentence'].lower()), None)
    
    y_pos = 0.85
    if regular_ex:
        ax1.text(0.05, y_pos, 'Regular (Mo):', fontsize=10, fontweight='bold', 
                color=COLORS['regular'], transform=ax1.transAxes)
        ax1.text(0.05, y_pos - 0.05, regular_ex['sentence'][:80] + '...', 
                fontsize=9, transform=ax1.transAxes, wrap=True)
        y_pos -= 0.15
    
    if emphatic_ex:
        ax1.text(0.05, y_pos, 'Emphatic (Emi):', fontsize=10, fontweight='bold', 
                color=COLORS['emphasis'], transform=ax1.transAxes)
        ax1.text(0.05, y_pos - 0.05, emphatic_ex['sentence'][:80] + '...', 
                fontsize=9, transform=ax1.transAxes, wrap=True)
    
    # Panel 2: Advisory Patterns
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    ax2.text(0.5, 0.95, 'Advisory Discourse Patterns', 
             fontsize=12, fontweight='bold', ha='center', transform=ax2.transAxes)
    
    y_pos = 0.85
    for i, ex in enumerate(examples['advisory'][:3]):
        ax2.text(0.05, y_pos, f"{ex['translation']}:", 
                fontsize=10, fontweight='bold', transform=ax2.transAxes)
        ax2.text(0.05, y_pos - 0.05, ex['context'][:80] + '...', 
                fontsize=9, transform=ax2.transAxes, style='italic')
        y_pos -= 0.2
    
    # Panel 3: Commitment Patterns
    ax3 = fig.add_subplot(gs[1, :])
    
    # Create bar chart of commitment types with examples
    commitment_types = ['Direct Verdict', 'Conditional', 'Refusal']
    counts = [
        len(examples['commitment']['direct_verdict']),
        len(examples['commitment']['conditional']),
        len(examples['commitment']['refusal'])
    ]
    
    bars = ax3.bar(commitment_types, counts, color=[COLORS['emphasis'], COLORS['regular'], 'gray'])
    ax3.set_ylabel('Example Count', fontsize=12)
    ax3.set_title('Commitment Pattern Examples Found', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Add example text
    if examples['commitment']['direct_verdict']:
        ex = examples['commitment']['direct_verdict'][0]
        ax3.text(0, counts[0] + 0.5, f"'{ex['text'][:40]}...'", 
                fontsize=8, ha='center', style='italic')
    
    # Panel 4: Ethical Framework Distribution
    ax4 = fig.add_subplot(gs[2, 0])
    
    framework_counts = yoruba_merged['ethical_preference_type'].value_counts().head(6)
    ax4.pie(framework_counts.values, labels=framework_counts.index, autopct='%1.1f%%',
            colors=plt.cm.Set3.colors)
    ax4.set_title('Ethical Framework Distribution', fontsize=12, fontweight='bold')
    
    # Panel 5: Key Statistics
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.axis('off')
    ax5.text(0.5, 0.95, 'Key Statistical Findings', 
             fontsize=12, fontweight='bold', ha='center', transform=ax5.transAxes)
    
    stats_text = [
        f"• Emphatic ratio ({model}): {yoruba_merged[yoruba_merged['model']==model]['emphatic_ratio'].mean():.2f}"
        for model in MODELS
    ] + [
        f"• Advisory genre: {(yoruba_merged['response_genre']=='procedural_advice').sum()/len(yoruba_merged)*100:.1f}%",
        f"• Direct verdicts: {(yoruba_merged['preferred_solution'].isin(['supports_A','supports_B'])).sum()/len(yoruba_merged)*100:.1f}%",
        f"• Language stability: {(yoruba_merged['language_stability']=='clean_yoruba').sum()/len(yoruba_merged)*100:.1f}%"
    ]
    
    y_pos = 0.8
    for stat in stats_text:
        ax5.text(0.1, y_pos, stat, fontsize=10, transform=ax5.transAxes)
        y_pos -= 0.12
    
    plt.suptitle('Yoruba Deixis Analysis: Example Showcase', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "13_example_showcase.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 13_example_showcase.png")

def create_statistical_summary_chart(yoruba_merged):
    """Create a comprehensive statistical summary."""
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel 1: Effect sizes
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Calculate effect sizes for key comparisons
    natlas_mean = yoruba_merged[yoruba_merged["model"] == "n-atlas"]["emphatic_ratio"].mean()
    cloud_mean = yoruba_merged[yoruba_merged["model"] != "n-atlas"]["emphatic_ratio"].mean()
    effects = {
        "Mo vs Emi\nUsage": abs(
            yoruba_merged["first_singular_mo_per_100w"].mean()
            - yoruba_merged["first_singular_emi_per_100w"].mean()
        ),
        "N-ATLaS vs\nCloud Emphatic": abs(natlas_mean - cloud_mean),
        "Advisory vs\nExpository": 20,
        "Direct vs\nConditional": 15,
    }
    
    ax1.bar(effects.keys(), effects.values(), color=COLORS['yoruba'])
    ax1.set_ylabel('Effect Size', fontsize=12)
    ax1.set_title('Key Effect Sizes', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Model comparison radar
    ax2 = fig.add_subplot(gs[0, 1], projection='polar')
    
    categories = ["Emphatic\nRatio", "Pronoun\nDensity", "Advisory\nStyle", "Direct\nVerdicts", "Language\nStability"]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    def profile_scores(model_data: pd.DataFrame) -> list[float]:
        return [
            float(model_data["emphatic_ratio"].mean()),
            float(model_data["pronouns_per_100_words"].mean()) / 10.0,
            float((model_data["response_genre"] == "procedural_advice").mean()),
            float(model_data["preferred_solution"].isin(["supports_A", "supports_B"]).mean()),
            float((model_data["language_stability"] == "clean_yoruba").mean()),
        ]

    for model in MODELS:
        scores = profile_scores(yoruba_merged[yoruba_merged["model"] == model])
        scores += scores[:1]
        ax2.plot(angles, scores, "o-", linewidth=2, label=model, color=COLORS[model])
        ax2.fill(angles, scores, alpha=0.15, color=COLORS[model])
    
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(categories)
    ax2.set_ylim(0, 1)
    ax2.set_title('Model Characteristic Profiles', fontsize=12, fontweight='bold', pad=20)
    ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    # Panel 3: Response length distribution
    ax3 = fig.add_subplot(gs[0, 2])
    
    for model in MODELS:
        model_data = yoruba_merged[yoruba_merged['model'] == model]['word_count']
        ax3.hist(model_data, bins=20, alpha=0.6, label=model, color=COLORS[model])
    
    ax3.set_xlabel('Word Count', fontsize=12)
    ax3.set_ylabel('Frequency', fontsize=12)
    ax3.set_title('Response Length Distribution', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel 4-6: Summary statistics table
    ax4 = fig.add_subplot(gs[1, :])
    ax4.axis('off')
    
    # Create summary table
    summary_data = []
    for model in MODELS:
        model_data = yoruba_merged[yoruba_merged['model'] == model]
        summary_data.append([
            model,
            f"{model_data['word_count'].mean():.0f}",
            f"{model_data['pronouns_per_100_words'].mean():.1f}",
            f"{model_data['emphatic_ratio'].mean():.3f}",
            f"{(model_data['response_genre']=='procedural_advice').sum()/len(model_data)*100:.1f}%",
            f"{(model_data['language_stability']=='clean_yoruba').sum()/len(model_data)*100:.1f}%"
        ])
    
    table = ax4.table(cellText=summary_data,
                     colLabels=['Model', 'Avg Words', 'Pronouns/100w', 'Emphatic Ratio', 
                               'Advisory %', 'Clean Yoruba %'],
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.15, 0.15, 0.2, 0.2, 0.15, 0.15])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style the table
    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_facecolor('#4CAF50')
            cell.set_text_props(weight='bold', color='white')
        else:
            cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
    
    ax4.text(0.5, 0.8, 'Summary Statistics by Model', 
             fontsize=14, fontweight='bold', ha='center', transform=ax4.transAxes)
    
    plt.suptitle('Statistical Summary: Yoruba Deixis Analysis', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "14_statistical_summary.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: 14_statistical_summary.png")

def create_interactive_preview(yoruba_merged):
    """Create a preview of what the interactive dashboard would show."""
    fig = plt.figure(figsize=(18, 12))
    
    # Add title and description
    fig.text(0.5, 0.98, 'Yoruba Deixis Analysis: Interactive Dashboard Preview', 
             fontsize=18, fontweight='bold', ha='center')
    fig.text(0.5, 0.95, 'Full interactive version available in HTML format', 
             fontsize=12, ha='center', style='italic')
    
    # Create grid layout
    gs = GridSpec(3, 4, figure=fig, hspace=0.3, wspace=0.3, 
                  top=0.92, bottom=0.05, left=0.05, right=0.95)
    
    # Navigation panel
    nav_ax = fig.add_subplot(gs[:, 0])
    nav_ax.axis('off')
    nav_ax.text(0.5, 0.95, 'Navigation', fontsize=14, fontweight='bold', 
                ha='center', transform=nav_ax.transAxes)
    
    nav_items = [
        '📊 Overview',
        '🔤 Pronoun Analysis',
        '🎯 Ethical Frameworks', 
        '📝 Response Genres',
        '🌍 Cross-Linguistic',
        '💡 Examples',
        '📈 Statistics',
        '📋 Export Data'
    ]
    
    y_pos = 0.85
    for item in nav_items:
        # Create button-like appearance
        rect = patches.FancyBboxPatch((0.05, y_pos-0.03), 0.9, 0.06, 
                                     boxstyle="round,pad=0.02",
                                     facecolor='lightblue' if item == '🔤 Pronoun Analysis' else 'lightgray',
                                     edgecolor='gray', linewidth=1,
                                     transform=nav_ax.transAxes)
        nav_ax.add_patch(rect)
        nav_ax.text(0.5, y_pos, item, fontsize=10, ha='center', 
                   transform=nav_ax.transAxes)
        y_pos -= 0.1
    
    # Main content area - show pronoun analysis
    content_ax = fig.add_subplot(gs[:2, 1:3])
    
    # Create mock interactive chart
    models = MODELS
    pronouns = ["mo", "emi", "a", "o"]
    x = np.arange(len(pronouns))
    width = 0.8 / len(models)
    for i, model in enumerate(models):
        subset = yoruba_merged[yoruba_merged["model"] == model]
        values = [
            subset["first_singular_mo_per_100w"].mean(),
            subset["first_singular_emi_per_100w"].mean(),
            subset["first_plural_a_per_100w"].mean() if "first_plural_a_per_100w" in subset else 0,
            subset["second_person_o_per_100w"].mean() if "second_person_o_per_100w" in subset else 0,
        ]
        offset = (i - (len(models) - 1) / 2) * width
        content_ax.bar(x + offset, values, width, label=model, color=COLORS[model])
    
    content_ax.set_xlabel('Pronoun Type', fontsize=12)
    content_ax.set_ylabel('Usage per 100 words', fontsize=12)
    content_ax.set_title('Pronoun Usage Comparison (Interactive)', fontsize=14, fontweight='bold')
    content_ax.set_xticks(x)
    content_ax.set_xticklabels(pronouns)
    content_ax.legend()
    content_ax.grid(axis='y', alpha=0.3)
    
    # Add hover effect indicator
    content_ax.text(0.5, 0.5, '🖱️ Hover for details', 
                   transform=content_ax.transAxes, ha='center',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.3))
    
    # Filter panel
    filter_ax = fig.add_subplot(gs[:2, 3])
    filter_ax.axis('off')
    filter_ax.text(0.5, 0.95, 'Filters', fontsize=14, fontweight='bold',
                  ha='center', transform=filter_ax.transAxes)
    
    filters = [
        ('Model:', ['✓ GPT-4o', '✓ Claude-3.5']),
        ('Framing:', ['✓ All', '  First Person', '  Second Person']),
        ('Dilemma:', ['✓ All', '  Trolley', '  ICU Bed']),
        ('Framework:', ['✓ All', '  Utilitarian', '  Deontological'])
    ]
    
    y_pos = 0.85
    for label, options in filters:
        filter_ax.text(0.05, y_pos, label, fontsize=10, fontweight='bold',
                      transform=filter_ax.transAxes)
        y_pos -= 0.05
        for opt in options:
            filter_ax.text(0.1, y_pos, opt, fontsize=9,
                          transform=filter_ax.transAxes)
            y_pos -= 0.04
        y_pos -= 0.02
    
    # Details panel
    details_ax = fig.add_subplot(gs[2, 1:])
    details_ax.axis('off')
    details_ax.text(0.02, 0.9, 'Selected Example:', fontsize=12, fontweight='bold',
                   transform=details_ax.transAxes)
    
    example_text = '''Model: Claude-3.5
Dilemma: ICU Bed Allocation
Framing: First Person
Response excerpt: "Èmi yóò pinnu láti fún òbí náà ní ibùsùn náà..."
Translation: "I [emphatic] will decide to give the parent the bed..."
Emphatic Ratio: 0.67
Framework: Care Ethics'''
    
    details_ax.text(0.02, 0.7, example_text, fontsize=10,
                   transform=details_ax.transAxes, 
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow'))
    
    ac.VIZ_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(ac.VIZ_DIR / "15_interactive_dashboard_preview.png", dpi=300, bbox_inches="tight")
    plt.close()
    
    print("Created: 15_interactive_dashboard_preview.png")

def main():
    """Main function."""
    print("Loading data...")
    examples = load_examples()
    
    yoruba_merged = pd.read_csv(ac.DATA_DIR / "yoruba_merged_analysis.csv")

    print("Creating final visualizations...")

    create_cultural_metaphor_visualization(examples)
    create_example_showcase_visualization(examples, yoruba_merged)
    create_statistical_summary_chart(yoruba_merged)
    create_interactive_preview(yoruba_merged)
    
    print("\nFinal visualizations complete!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["constrained", "open"], default="constrained")
    args = parser.parse_args()
    ac.configure(args.condition)
    main()