# Deixis Analysis Pipeline - Quick Start Guide

## Prerequisites

### 1. Python Environment
```bash
# Ensure Python 3.8+ is installed
python --version

# Activate virtual environment (if not already active)
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install required packages
pip install -r ARCHIVE/requirements.txt
```

### 3. Set Up API Keys
Create or verify `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here  # Optional
```

### 4. Copy Core Modules (One-time setup)
```bash
# Windows PowerShell:
copy ARCHIVE\deixis_ethical_analyzer.py .
copy ARCHIVE\transformer.py .
copy ARCHIVE\pronoun_agency_analyzer.py .
copy ARCHIVE\llm_client.py .
copy ARCHIVE\expert_analysis_agent.py .
copy ARCHIVE\critical_expert_analysis.py .
copy ARCHIVE\evidence_based_expert_analysis.py .
copy ARCHIVE\pronoun_agency_expert.py .
copy ARCHIVE\detailed_report_generator.py .
copy ARCHIVE\final_report_generator.py .
copy ARCHIVE\research_framework_system.py .

# Mac/Linux:
cp ARCHIVE/*.py .
```

## Running the Pipeline

### Option 1: Complete Pipeline (Recommended)
Run both generation and analysis in sequence:
```bash
python deixis_analysis_pipeline/run_complete_pipeline.py
```

### Option 2: Step-by-Step Execution

#### Step 1: Generate Responses
```bash
# Generate responses for all dilemmas
python deixis_analysis_pipeline/generation_scripts/generate_responses_multi_dilemma.py

# Or specify custom JSON path
python deixis_analysis_pipeline/generation_scripts/generate_responses_multi_dilemma.py --json-path deixis_analysis_pipeline/input_questions/all_dilemmas_deictic_questions.json

# Or process specific dilemmas only
python deixis_analysis_pipeline/generation_scripts/generate_responses_multi_dilemma.py --dilemmas trolley_problem ai_consciousness
```

**Expected output:**
- 54 responses (6 dilemmas × 9 framings)
- Location: `generation_logs/multi_dilemma_YYYYMMDD_HHMMSS/`
- Time: ~10-15 minutes
- Cost: ~$0.15-0.30

#### Step 2: Analyze Responses
```bash
# Analyze the latest generation session
python deixis_analysis_pipeline/analysis_scripts/run_complete_deixis_analysis.py
```

**Expected output:**
- CSV data: `automated_analysis_results/complete_analysis_YYYYMMDD_HHMMSS/comprehensive_research_data.csv`
- JSON results: `automated_analysis_results/complete_analysis_YYYYMMDD_HHMMSS/complete_analysis_results.json`
- Time: ~5-10 minutes per dilemma
- Cost: ~$0.10-0.20

## Quick Commands Reference

### Check Generated Responses
```bash
# List all generation sessions
dir generation_logs  # Windows
ls generation_logs   # Mac/Linux

# View a specific response file
type generation_logs\multi_dilemma_20250804_131927\ai_consciousness_responses.json  # Windows
cat generation_logs/multi_dilemma_20250804_131927/ai_consciousness_responses.json   # Mac/Linux
```

### Check Analysis Results
```bash
# List all analysis sessions
dir automated_analysis_results  # Windows
ls automated_analysis_results   # Mac/Linux

# Open CSV in Excel/Numbers
start automated_analysis_results\complete_analysis_20250804_133550\comprehensive_research_data.csv  # Windows
open automated_analysis_results/complete_analysis_20250804_133550/comprehensive_research_data.csv   # Mac
```

## Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'deixis_ethical_analyzer'**
   - Solution: Copy the required modules from ARCHIVE (see step 4 above)

2. **OpenAI API Error**
   - Check your API key in .env file
   - Verify you have credits in your OpenAI account
   - Check rate limits

3. **Analysis only processes one dilemma**
   - Current limitation: Modify the analysis script to process all files
   - Workaround: Run analysis multiple times with different input files

4. **Permission denied errors**
   - Close any files that might be open in Excel/other programs
   - Run terminal as administrator (Windows)

### Verify Installation:
```python
# Test imports
python -c "import deixis_ethical_analyzer; print('✓ Core modules loaded')"
python -c "import openai; print('✓ OpenAI installed')"
python -c "import pandas; print('✓ Pandas installed')"
```

## Understanding the Output

### Generation Output Structure:
```
generation_logs/
└── multi_dilemma_YYYYMMDD_HHMMSS/
    ├── whistleblower_risk_responses.json
    ├── scholarship_fraud_responses.json
    ├── icu_bed_allocation_responses.json
    ├── trolley_problem_responses.json
    ├── ai_consciousness_responses.json
    ├── memory_modification_responses.json
    ├── complete_session_data.json
    └── generation_summary.json
```

### Analysis Output Structure:
```
automated_analysis_results/
└── complete_analysis_YYYYMMDD_HHMMSS/
    ├── comprehensive_research_data.csv  # For statistical analysis
    └── complete_analysis_results.json   # Detailed analysis data
```

## Next Steps

1. **View Results**: Open the CSV file in Excel/Numbers for data exploration
2. **Statistical Analysis**: Import CSV into R/Python for statistical tests
3. **Generate Reports**: Fix and run report generators for markdown summaries
4. **Extend Analysis**: Modify scripts to analyze all 6 dilemmas
5. **Custom Dilemmas**: Create new dilemma JSON files and run pipeline

## Cost Estimates

- **Generation**: ~$0.05 per dilemma (9 responses)
- **Analysis**: ~$0.02-0.03 per dilemma
- **Total for full run**: ~$0.50-0.60

## Support

For detailed documentation, see:
- `LOG_AND_OUTPUT_LOCATIONS.md` - File locations guide
- `LLM_EXPERT_ANALYSIS_GUIDE.md` - Analysis components explained
- `TECHNICAL_IMPLEMENTATION_GUIDE.md` - Technical details
- `README.md` - Project overview