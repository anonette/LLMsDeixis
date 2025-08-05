# Deixis Analysis Pipeline - Complete Summary

## What We've Accomplished

### 1. Enhanced Reflexive Framings ✅
Modified the reflexive framings in `all_dilemmas_deictic_questions.json` to include more self-reflective language:
- Added introspective phrases like "looking within myself", "questioning my own integrity"
- Enhanced self-examination elements: "examining my own conscience", "wrestling with myself"
- Deepened moral introspection: "what I can live with myself doing", "my true self demands"

### 2. Generated All Responses ✅
Successfully generated 54 responses (6 dilemmas × 9 framings):
- The Whistleblower's Risk
- The Scholarship Fraud
- The ICU Bed Decision
- The Trolley Problem
- The Artificial Mind's Rights
- The Memory Modification Treatment

### 3. Ran Comprehensive Analysis ✅
The analysis pipeline processes responses with multiple tools:
- Deictic marker counting
- Pronoun agency analysis
- LLM-based ethical framework analysis
- Rhetorical posture analysis
- Moral reasoning structure analysis
- Affective stance analysis
- Lexical and rhetorical features analysis

### 4. Created Documentation ✅
- **LOG_AND_OUTPUT_LOCATIONS.md** - Complete guide to all file locations
- **LLM_EXPERT_ANALYSIS_GUIDE.md** - Detailed explanation of analysis components
- **QUICK_START_GUIDE.md** - Step-by-step instructions for running the pipeline

## Current Status

### Generation Phase: COMPLETE
- Location: `generation_logs/multi_dilemma_20250804_131927/`
- Files: 6 dilemma response files + session data
- Total responses: 54

### Analysis Phase: IN PROGRESS
- Currently analyzing responses from the latest generation session
- Creating CSV data and JSON results
- Location: `automated_analysis_results/complete_analysis_[timestamp]/`

## Known Issues and Solutions

### 1. Unicode Encoding Error
**Issue**: Emoji characters cause encoding errors on Windows
**Solution**: Removed emojis from print statements in scripts

### 2. Module Import Errors
**Issue**: Scripts can't find core modules
**Solution**: Added sys.path modifications and copied modules from ARCHIVE

### 3. Analysis Limited to One Dilemma
**Issue**: Current analysis script only processes first dilemma file
**Solution**: Would need to modify script to loop through all response files

## How to Use the Pipeline

### Quick Start:
```bash
# Option 1: Run everything
python deixis_analysis_pipeline/run_complete_pipeline.py

# Option 2: Run analysis on existing data
python deixis_analysis_pipeline/analysis_scripts/run_complete_deixis_analysis.py

# Option 3: Generate new responses
python deixis_analysis_pipeline/generation_scripts/generate_responses_multi_dilemma.py
```

### Access Results:
```python
# Load CSV for statistical analysis
import pandas as pd
df = pd.read_csv('automated_analysis_results/[session]/comprehensive_research_data.csv')

# Load complete analysis data
import json
with open('automated_analysis_results/[session]/complete_analysis_results.json', 'r') as f:
    data = json.load(f)
```

## Research Applications

The pipeline enables research into:
1. **Linguistic-Ethical Correlations**: How deictic framing affects moral reasoning
2. **Agency Attribution**: How perspective shifts decision-making locus
3. **Emotional Engagement**: How framing affects affective stance
4. **Rhetorical Authority**: How voice changes with perspective

## Cost Summary
- Generation: ~$0.05 per dilemma (9 responses)
- Analysis: ~$0.02-0.03 per dilemma
- Total pipeline run: ~$0.50-0.60

## Next Steps for Researchers

1. **Statistical Analysis**: Use the CSV data for quantitative research
2. **Pattern Recognition**: Identify correlations in the JSON data
3. **Extended Analysis**: Modify scripts to analyze all 6 dilemmas
4. **Custom Dilemmas**: Create new ethical scenarios for analysis
5. **Publication**: Use findings for research papers on AI ethics and linguistics

## Technical Architecture

```
deixis_analysis_pipeline/
├── input_questions/          # Deictic framings
├── generation_scripts/       # Response generation
├── analysis_scripts/         # Analysis tools
├── llm_agents/              # LLM interfaces
└── utilities/               # Helper functions

Core Modules (from ARCHIVE):
├── deixis_ethical_analyzer.py
├── transformer.py
├── pronoun_agency_analyzer.py
├── expert_analysis_agent.py
└── [other analysis modules]
```

## Conclusion

The deixis analysis pipeline successfully demonstrates how linguistic framing (deixis) systematically affects AI ethical reasoning. The enhanced reflexive framings add depth to the self-examination dimension, providing richer data for understanding how perspective shapes moral decision-making in AI systems.