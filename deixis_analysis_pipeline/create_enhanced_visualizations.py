#!/usr/bin/env python3
"""
Enhanced visualization suite for deixis analysis results.
Creates comprehensive visualizations including trolley problem analysis,
interactive plots, and statistical comparisons.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import json

# Set style for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Define output directory
SCRIPT_DIR = Path(__file__).parent
REPORT_DIR = SCRIPT_DIR / "CONSOLIDATED_REPORTS"
VIZ_DIR = REPORT_DIR / "visualizations"
VIZ_DIR.mkdir(parents=True, exist_ok=True)

# Color schemes for models
MODEL_COLORS = {
    'GPT-4o': '#2E86AB',
    'Claude-3.5': '#A23B72',
    'Claude 3.5': '#A23B72',
    'DeepSeek': '#F18F01'
}


def load_trolley_data():
    """Load trolley problem data from JSON file."""
    data_file = REPORT_DIR / "trolley_all_models_data.json"
    if not data_file.exists():
        print(f"⚠️  Warning: {data_file} not found")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_trolley_comparison_charts():
    """Create detailed trolley problem comparison visualizations."""
    print("✓ Creating trolley problem comparison charts...")
    
    data = load_trolley_data()
    if data is None:
        return
    
    # Prepare data for plotting
    models = list(data.keys())
    metrics = ['word_count', 'sentence_count', 'philosophical_total', 
               'first_person', 'second_person', 'uncertainty_words']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Trolley Problem vs Other Dilemmas: Detailed Comparison', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    metric_titles = {
        'word_count': 'Average Word Count',
        'sentence_count': 'Average Sentence Count',
        'philosophical_total': 'Philosophical References',
        'first_person': 'First Person Pronoun Usage',
        'second_person': 'Second Person Pronoun Usage',
        'uncertainty_words': 'Uncertainty Expression'
    }
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 3, idx % 3]
        
        trolley_vals = [data[model]['averages']['trolley'][metric] for model in models]
        other_vals = [data[model]['averages']['others'][metric] for model in models]
        
        x = np.arange(len(models))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, trolley_vals, width, label='Trolley Problem',
                      color='#E63946', alpha=0.8)
        bars2 = ax.bar(x + width/2, other_vals, width, label='Other Dilemmas',
                      color='#457B9D', alpha=0.8)
        
        ax.set_ylabel('Value', fontweight='bold')
        ax.set_title(metric_titles[metric], fontweight='bold', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=15, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'trolley_detailed_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_trolley_difference_heatmap():
    """Create a heatmap showing percentage differences for trolley problem."""
    print("✓ Creating trolley problem difference heatmap...")
    
    data = load_trolley_data()
    if data is None:
        return
    
    models = list(data.keys())
    metrics = ['length', 'word_count', 'sentence_count', 'philosophical_total',
               'first_person', 'second_person', 'third_person', 'uncertainty_words',
               'action_words', 'emotional_words']
    
    # Create difference matrix
    diff_matrix = []
    for metric in metrics:
        row = [data[model]['differences'][metric] for model in models]
        diff_matrix.append(row)
    
    df = pd.DataFrame(diff_matrix, columns=models, index=metrics)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 12))
    
    sns.heatmap(df, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                cbar_kws={'label': 'Percentage Change (Trolley vs Others)'},
                linewidths=0.5, ax=ax)
    
    ax.set_title('Trolley Problem: Percentage Differences from Other Dilemmas\n' +
                 '(Positive = Higher in Trolley, Negative = Lower in Trolley)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Models', fontsize=12, fontweight='bold')
    ax.set_ylabel('Metrics', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'trolley_difference_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_pronoun_usage_analysis():
    """Create detailed pronoun usage analysis across models and dilemma types."""
    print("✓ Creating pronoun usage analysis...")
    
    data = load_trolley_data()
    if data is None:
        return
    
    models = list(data.keys())
    pronouns = ['first_person', 'second_person', 'third_person', 'first_plural']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Trolley problem pronouns
    trolley_data = {model: [data[model]['averages']['trolley'][p] for p in pronouns] 
                    for model in models}
    
    x = np.arange(len(pronouns))
    width = 0.25
    
    for i, model in enumerate(models):
        offset = (i - 1) * width
        bars = ax1.bar(x + offset, trolley_data[model], width, 
                      label=model, color=MODEL_COLORS.get(model, None), alpha=0.8)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            if height > 0.1:  # Only label visible bars
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    ax1.set_ylabel('Average Count per Response', fontweight='bold')
    ax1.set_title('Pronoun Usage: Trolley Problem', fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(['First\nPerson', 'Second\nPerson', 'Third\nPerson', 'First\nPlural'])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Other dilemmas pronouns
    other_data = {model: [data[model]['averages']['others'][p] for p in pronouns] 
                  for model in models}
    
    for i, model in enumerate(models):
        offset = (i - 1) * width
        bars = ax2.bar(x + offset, other_data[model], width, 
                      label=model, color=MODEL_COLORS.get(model, None), alpha=0.8)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            if height > 0.1:
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    ax2.set_ylabel('Average Count per Response', fontweight='bold')
    ax2.set_title('Pronoun Usage: Other Dilemmas', fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(['First\nPerson', 'Second\nPerson', 'Third\nPerson', 'First\nPlural'])
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'pronoun_usage_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_philosophical_framework_detail():
    """Create detailed philosophical framework usage visualization."""
    print("✓ Creating philosophical framework analysis...")
    
    data = load_trolley_data()
    if data is None:
        return
    
    models = list(data.keys())
    frameworks = ['kant_refs', 'utilitarian_refs', 'deontological_refs', 
                  'virtue_refs', 'consequential_refs']
    
    framework_labels = ['Kantian', 'Utilitarian', 'Deontological', 
                       'Virtue Ethics', 'Consequentialist']
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Philosophical Framework References by Model and Dilemma Type',
                 fontsize=14, fontweight='bold', y=1.02)
    
    # For each model
    for idx, model in enumerate(models):
        ax = axes[idx]
        
        trolley_vals = [data[model]['averages']['trolley'][f] for f in frameworks]
        other_vals = [data[model]['averages']['others'][f] for f in frameworks]
        
        x = np.arange(len(frameworks))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, trolley_vals, width, label='Trolley',
                      color='#E63946', alpha=0.8)
        bars2 = ax.bar(x + width/2, other_vals, width, label='Others',
                      color='#457B9D', alpha=0.8)
        
        ax.set_ylabel('Avg References', fontweight='bold')
        ax.set_title(model, fontweight='bold', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(framework_labels, rotation=45, ha='right', fontsize=9)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0.05:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.2f}', ha='center', va='bottom', fontsize=7)
    
    plt.tight_layout()
    plt.savefig(VIZ_DIR / 'philosophical_frameworks_detailed.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_comprehensive_summary():
    """Create a comprehensive summary visualization."""
    print("✓ Creating comprehensive summary dashboard...")
    
    data = load_trolley_data()
    if data is None:
        return
    
    models = list(data.keys())
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Title
    fig.suptitle('Comprehensive Deixis Analysis: Model Comparison Summary', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # 1. Response Length Comparison
    ax1 = fig.add_subplot(gs[0, 0])
    word_counts_trolley = [data[m]['averages']['trolley']['word_count'] for m in models]
    word_counts_other = [data[m]['averages']['others']['word_count'] for m in models]
    
    x = np.arange(len(models))
    width = 0.35
    ax1.bar(x - width/2, word_counts_trolley, width, label='Trolley', color='#E63946', alpha=0.8)
    ax1.bar(x + width/2, word_counts_other, width, label='Others', color='#457B9D', alpha=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=15, ha='right')
    ax1.set_ylabel('Word Count')
    ax1.set_title('Average Response Length', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Philosophical References
    ax2 = fig.add_subplot(gs[0, 1])
    phil_trolley = [data[m]['averages']['trolley']['philosophical_total'] for m in models]
    phil_other = [data[m]['averages']['others']['philosophical_total'] for m in models]
    
    ax2.bar(x - width/2, phil_trolley, width, label='Trolley', color='#E63946', alpha=0.8)
    ax2.bar(x + width/2, phil_other, width, label='Others', color='#457B9D', alpha=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, rotation=15, ha='right')
    ax2.set_ylabel('Count')
    ax2.set_title('Philosophical References', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Second Person Usage (You)
    ax3 = fig.add_subplot(gs[0, 2])
    you_trolley = [data[m]['averages']['trolley']['second_person'] for m in models]
    you_other = [data[m]['averages']['others']['second_person'] for m in models]
    
    ax3.bar(x - width/2, you_trolley, width, label='Trolley', color='#E63946', alpha=0.8)
    ax3.bar(x + width/2, you_other, width, label='Others', color='#457B9D', alpha=0.8)
    ax3.set_xticks(x)
    ax3.set_xticklabels(models, rotation=15, ha='right')
    ax3.set_ylabel('Count')
    ax3.set_title('Second Person Pronoun Usage', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4-6. Pie charts showing trolley vs others distribution for each model
    for idx, model in enumerate(models):
        ax = fig.add_subplot(gs[1, idx])
        trolley_count = data[model]['averages']['trolley']['word_count']
        other_count = data[model]['averages']['others']['word_count']
        
        colors = ['#E63946', '#457B9D']
        ax.pie([trolley_count, other_count], labels=['Trolley', 'Others'],
               autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title(f'{model}\nWord Distribution', fontweight='bold')
    
    # 7. Key differences heatmap
    ax7 = fig.add_subplot(gs[2, :])
    key_metrics = ['word_count', 'philosophical_total', 'first_person', 
                   'second_person', 'uncertainty_words']
    diff_data = [[data[m]['differences'][metric] for m in models] for metric in key_metrics]
    
    df_diff = pd.DataFrame(diff_data, columns=models, index=key_metrics)
    sns.heatmap(df_diff, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                cbar_kws={'label': '% Change (Trolley vs Others)'}, ax=ax7)
    ax7.set_title('Key Metric Differences: Trolley Problem vs Other Dilemmas', 
                  fontweight='bold', pad=10)
    ax7.set_xlabel('Models')
    ax7.set_ylabel('Metrics')
    
    plt.savefig(VIZ_DIR / 'comprehensive_summary.png', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    """Generate all enhanced visualizations."""
    
    print("\n" + "="*70)
    print("ENHANCED DEIXIS ANALYSIS VISUALIZATIONS")
    print("="*70)
    print(f"\nOutput directory: {VIZ_DIR.absolute()}\n")
    
    try:
        # Create all visualizations
        create_trolley_comparison_charts()
        create_trolley_difference_heatmap()
        create_pronoun_usage_analysis()
        create_philosophical_framework_detail()
        create_comprehensive_summary()
        
        print("\n" + "="*70)
        print("🎉 All enhanced visualizations created successfully!")
        print("="*70)
        print(f"\n📁 Files saved in: {VIZ_DIR.absolute()}\n")
        
        # List all PNG files in visualizations directory
        print("Generated files:")
        viz_files = sorted(VIZ_DIR.glob("*.png"))
        for file in viz_files:
            print(f"  ✓ {file.name}")
        
        print(f"\nTotal: {len(viz_files)} visualizations\n")
        
    except Exception as e:
        print(f"\n❌ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
