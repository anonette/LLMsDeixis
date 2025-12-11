# Deixis Analysis Visualizations

## Quick Start

To generate or regenerate all visualizations:

```bash
python deixis_analysis_pipeline/create_enhanced_visualizations.py
```

Or from within the pipeline directory:

```bash
cd deixis_analysis_pipeline
python create_enhanced_visualizations.py
```

## What Was Created

### Visualization Scripts

1. **create_enhanced_visualizations.py** (NEW)
   - Enhanced visualization suite with trolley-specific analysis
   - Creates 5 new detailed visualizations
   - Focuses on Trolley Problem vs Other Dilemmas comparison

2. **create_model_comparison_visualizations.py** (EXISTING)
   - Original model comparison visualizations
   - Creates 5 visualizations focused on general model characteristics
   - Ethical frameworks, framing sensitivity, response characteristics

### Output Location

All visualizations are saved to:
```
deixis_analysis_pipeline/CONSOLIDATED_REPORTS/visualizations/
```

### Generated Visualizations (10 total)

#### New Enhanced Visualizations (5):
1. **comprehensive_summary.png** - Complete overview dashboard
2. **trolley_detailed_comparison.png** - Trolley vs Others detailed metrics
3. **trolley_difference_heatmap.png** - Percentage differences heatmap
4. **pronoun_usage_analysis.png** - Detailed pronoun patterns
5. **philosophical_frameworks_detailed.png** - Framework usage by model

#### Existing Model Comparison Visualizations (5):
6. **ethical_framework_comparison.png** - Framework usage bar chart
7. **framing_sensitivity_heatmap.png** - Deictic framing sensitivity
8. **model_summary_dashboard.png** - Four-panel model summary
9. **response_characteristics_comparison.png** - Response metrics with radar
10. **response_length_by_framing.png** - Length variation by framing

## Documentation

📖 **Full Guide**: See [VISUALIZATION_GUIDE.md](CONSOLIDATED_REPORTS/VISUALIZATION_GUIDE.md) for detailed explanations of each visualization including:
- What each visualization shows
- Key insights from each chart
- How to interpret the results
- Color schemes and conventions
- Usage recommendations for academic writing and presentations

## Key Features

### Enhanced Analysis
- **Trolley Problem Focus**: Special attention to how models handle the classic trolley dilemma
- **Comparative Analysis**: Direct comparison between Trolley Problem and other ethical dilemmas
- **Statistical Depth**: Percentage differences, heatmaps, and multi-dimensional comparisons

### Professional Quality
- High resolution (300 DPI) for publications
- Clear labeling and legends
- Consistent color schemes across visualizations
- Publication-ready formatting

### Data Sources
All visualizations are generated from:
- `CONSOLIDATED_REPORTS/trolley_all_models_data.json` - Trolley comparison data
- Analysis results from the main pipeline

## Customization

To modify visualizations:

1. Edit `create_enhanced_visualizations.py`
2. Adjust colors in `MODEL_COLORS` dictionary
3. Modify figure sizes for different aspect ratios
4. Add new visualization functions as needed

Example color scheme:
```python
MODEL_COLORS = {
    'GPT-4o': '#2E86AB',      # Blue
    'Claude-3.5': '#A23B72',  # Purple
    'DeepSeek': '#F18F01'     # Orange
}
```

## Requirements

### Python Packages
- matplotlib
- seaborn
- pandas
- numpy
- pathlib (built-in)

Install with:
```bash
pip install matplotlib seaborn pandas numpy
```

### Optional
- plotly (for interactive visualizations - not yet implemented)
```bash
pip install plotly kaleido
```

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: CONSOLIDATED_REPORTS not found`
- **Solution**: Run from the correct directory or check paths in script

**Issue**: Missing data file
- **Solution**: Ensure `trolley_all_models_data.json` exists in CONSOLIDATED_REPORTS/

**Issue**: Font warnings
- **Solution**: These are harmless matplotlib warnings and don't affect output

## Research Applications

### For Papers
- Use high-resolution PNG files directly in LaTeX/Word
- Reference specific visualizations by filename
- Comprehensive_summary.png works well for overview sections

### For Presentations
- All visualizations are presentation-ready
- Clear, high-contrast color schemes
- Large, readable fonts and labels

### For Analysis
- Heatmaps show patterns at a glance
- Bar charts enable precise comparisons
- Pie charts illustrate distributions

## Updates and Maintenance

Last updated: 2025-11-01

To update visualizations with new data:
1. Ensure latest analysis results are in CONSOLIDATED_REPORTS/
2. Run the visualization scripts
3. Check output in visualizations/ directory

## Additional Resources

- **Main Pipeline**: See `README.md` in parent directory
- **Analysis Results**: See files in `CONSOLIDATED_REPORTS/`
- **Model Findings**: See `MODEL_COMPARISON_FINDINGS.md`
- **Technical Guide**: See `TECHNICAL_IMPLEMENTATION_GUIDE.md`

## Summary

This visualization suite provides comprehensive graphical analysis of how three leading LLM models (GPT-4o, Claude 3.5, and DeepSeek) respond to ethical dilemmas with various deictic framings. The visualizations reveal significant differences in:

- Response length and complexity
- Philosophical framework usage
- Pronoun patterns and agency attribution
- Sensitivity to question framing
- Special handling of the Trolley Problem

Use these visualizations to support empirical findings about LLM ethical reasoning and the impact of deictic framing on AI-generated moral guidance.
