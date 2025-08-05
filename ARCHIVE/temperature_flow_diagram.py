"""
Visual representation of temperature flow in the Deixis Ethical Analyzer
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_temperature_flow_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Define colors
    high_temp_color = '#FF6B6B'  # Red for high temperature
    low_temp_color = '#4ECDC4'   # Teal for low temperature
    model_colors = {
        'GPT-4': '#FFE66D',
        'Claude': '#95E1D3',
        'DeepSeek': '#C7CEEA'
    }
    
    # Title
    plt.title('Temperature Flow in Deixis Ethical Analyzer', fontsize=16, fontweight='bold', pad=20)
    
    # Main workflow boxes
    workflow_y = 7
    box_height = 1.2
    box_width = 2.5
    
    # Step 1: Generate Response
    step1_box = FancyBboxPatch((0.5, workflow_y), box_width, box_height,
                               boxstyle="round,pad=0.1",
                               facecolor=high_temp_color,
                               edgecolor='black',
                               linewidth=2)
    ax.add_patch(step1_box)
    ax.text(0.5 + box_width/2, workflow_y + box_height/2, 
            'Generate\nEthical Response\nTemp: 0.9',
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Step 2-4: Analysis tasks
    analysis_tasks = [
        'Analyze\nAgency\nTemp: 0.5',
        'Analyze\nEthics\nTemp: 0.5',
        'Analyze\nRhetoric\nTemp: 0.5'
    ]
    
    for i, task in enumerate(analysis_tasks):
        x_pos = 4 + i * 3
        box = FancyBboxPatch((x_pos, workflow_y), box_width, box_height,
                            boxstyle="round,pad=0.1",
                            facecolor=low_temp_color,
                            edgecolor='black',
                            linewidth=2)
        ax.add_patch(box)
        ax.text(x_pos + box_width/2, workflow_y + box_height/2, task,
                ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw arrows
        if i == 0:
            ax.arrow(0.5 + box_width, workflow_y + box_height/2,
                    x_pos - (0.5 + box_width) - 0.2, 0,
                    head_width=0.2, head_length=0.1, fc='black', ec='black')
        else:
            prev_x = 4 + (i-1) * 3
            ax.arrow(prev_x + box_width, workflow_y + box_height/2,
                    x_pos - (prev_x + box_width) - 0.2, 0,
                    head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Model rotation visualization
    model_y = 4
    ax.text(6, model_y + 1.5, 'Model Rotation (Cycles through all tasks)', 
            ha='center', fontsize=12, fontweight='bold')
    
    models = ['GPT-4', 'Claude', 'DeepSeek']
    for i, model in enumerate(models):
        x_pos = 2 + i * 4
        circle = plt.Circle((x_pos, model_y), 0.8, 
                          facecolor=model_colors[model],
                          edgecolor='black',
                          linewidth=2)
        ax.add_patch(circle)
        ax.text(x_pos, model_y, model, ha='center', va='center', fontsize=10)
        
        # Draw rotation arrows
        if i < len(models) - 1:
            ax.arrow(x_pos + 0.8, model_y, 
                    4 - 1.6 - 0.2, 0,
                    head_width=0.15, head_length=0.1, fc='gray', ec='gray')
    
    # Draw curved arrow back to first model
    from matplotlib.patches import FancyArrowPatch
    arrow = FancyArrowPatch((10, model_y - 0.8), (2, model_y - 0.8),
                           connectionstyle="arc3,rad=-.3",
                           arrowstyle='->', 
                           mutation_scale=20,
                           color='gray')
    ax.add_patch(arrow)
    
    # Temperature scale legend
    legend_y = 1
    ax.text(6, legend_y + 1, 'Temperature Scale', ha='center', fontsize=12, fontweight='bold')
    
    # Create gradient
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    gradient = np.vstack((gradient, gradient))
    
    im = ax.imshow(gradient, aspect='auto', cmap='coolwarm', 
                   extent=[2, 10, legend_y - 0.3, legend_y + 0.3])
    ax.text(2, legend_y - 0.5, '0.0', ha='center', fontsize=10)
    ax.text(6, legend_y - 0.5, '0.5', ha='center', fontsize=10)
    ax.text(10, legend_y - 0.5, '1.0', ha='center', fontsize=10)
    ax.text(2, legend_y + 0.5, 'Deterministic', ha='center', fontsize=9)
    ax.text(10, legend_y + 0.5, 'Creative', ha='center', fontsize=9)
    
    # Add annotations
    ax.text(0.5, 9, 'For each dilemma × framing combination:', 
            fontsize=12, style='italic')
    
    # Pattern explanation
    pattern_text = """Pattern: Generate (0.9) → Analyze (0.5) → Analyze (0.5) → Analyze (0.5)
    
This creates optimal balance between:
• Creative ethical reasoning in responses
• Reliable structured analysis of those responses"""
    
    ax.text(6, -0.5, pattern_text, ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.5))
    
    # Set axis limits and remove axes
    ax.set_xlim(-1, 13)
    ax.set_ylim(-2, 10)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('temperature_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.savefig('temperature_flow_diagram.pdf', bbox_inches='tight')
    print("Temperature flow diagram saved as temperature_flow_diagram.png and .pdf")

if __name__ == "__main__":
    create_temperature_flow_diagram()