# Complete Workflow Guide: Generate → Analyze → Reports

## Overview
This guide shows you exactly how to use `generate_responses_multi_dilemma.py` to generate LLM responses for all 6 ethical dilemmas, where the logs are saved, how they're analyzed, and where the final reports are stored.

## Step 1: Generate LLM Responses

### Command to Run:
```bash
cd deixis_analysis_pipeline
python generation_scripts/generate_responses_multi_dilemma.py --json-path input_questions/all_dilemmas_deictic_questions.json
```

### What Happens:
- The script reads `all_dilemmas_deictic_questions.json` containing 6 ethical dilemmas
- For each dilemma, it generates 9 responses (one for each deictic framing)
- Total: 54 LLM responses using GPT-4o
- Time required: 15-30 minutes
- Cost: ~$0.50-$1.00 in OpenAI API credits

### Where Logs Are Saved:
```
deixis_analysis_pipeline/generation_logs/multi_dilemma_[timestamp]/
├── whistleblower_risk_responses.json      # 9 responses
├── scholarship_fraud_responses.json        # 9 responses  
├── icu_bed_allocation_responses.json       # 9 responses
├── trolley_problem_responses.json          # 9 responses
├── ai_consciousness_responses.json         # 9 responses
├── memory_modification_responses.json      # 9 responses
└── generation_summary.json                 # Session metadata
```

Example timestamp: `multi_dilemma_20250804_163350`

## Step 2: Analyze the Responses

### Command to Run:
```bash
cd deixis_analysis_pipeline
python analysis_scripts/run_complete_deixis_analysis.py
```

### What Happens:
1. **Finds Latest Generation**: Automatically locates the most recent session in `generation_logs/`
2. **Loads All Responses**: Reads all 54 responses from the JSON files
3. **Runs Multiple Analyses**:
   - Core deixis analysis (pronoun patterns, framing effects)
   - Expert agent analysis (ethical frameworks, reasoning patterns)
   - Critical expert analysis (deeper insights)
   - Evidence-based analysis (supporting patterns)
   - Pronoun agency analysis (subject/object positioning)
   - Research framework analysis

### Where Analysis Results Are Saved:
```
automated_analysis_results/complete_analysis_[timestamp]/
├── complete_analysis_results.json          # All analysis data
├── comprehensive_research_data.csv         # Spreadsheet format
├── detailed_analysis_report.md             # Human-readable report
├── FINAL_DEIXIS_RESEARCH_REPORT.md        # Executive summary
└── research_framework_analysis.json        # Research insights
```

## Step 3: Access Your Reports

### Main Reports:
1. **CSV Data** (`comprehensive_research_data.csv`):
   - Import into Excel/Google Sheets
   - Contains all responses and analysis metrics
   - Ready for statistical analysis

2. **Detailed Report** (`detailed_analysis_report.md`):
   - Comprehensive markdown report
   - Includes all expert analyses
   - Formatted for reading/sharing

3. **Final Research Report** (`FINAL_DEIXIS_RESEARCH_REPORT.md`):
   - Executive summary
   - Key findings and insights
   - Research implications

## Complete Example Workflow:

```bash
# 1. Navigate to the pipeline directory
cd deixis_analysis_pipeline

# 2. Generate all responses (takes 15-30 minutes)
python generation_scripts/generate_responses_multi_dilemma.py --json-path input_questions/all_dilemmas_deictic_questions.json

# Output: Generation complete! Check generation_logs/multi_dilemma_20250804_163350/

# 3. Run the analysis
python analysis_scripts/run_complete_deixis_analysis.py

# Output: Analysis complete! Results in automated_analysis_results/complete_analysis_20250804_170000/

# 4. View your reports
# Open the markdown files in VS Code or any text editor
# Import the CSV into Excel for data analysis
```

## File Flow Diagram:

```
input_questions/all_dilemmas_deictic_questions.json
    ↓
[generate_responses_multi_dilemma.py]
    ↓
generation_logs/multi_dilemma_[timestamp]/
    ├── whistleblower_risk_responses.json
    ├── scholarship_fraud_responses.json
    ├── (4 more dilemma files...)
    └── generation_summary.json
    ↓
[run_complete_deixis_analysis.py]
    ↓
automated_analysis_results/complete_analysis_[timestamp]/
    ├── complete_analysis_results.json
    ├── comprehensive_research_data.csv
    ├── detailed_analysis_report.md
    ├── FINAL_DEIXIS_RESEARCH_REPORT.md
    └── research_framework_analysis.json
```

## Important Notes:

1. **Ensure .env file exists** with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

2. **The analysis script automatically finds** the latest generation session

3. **All paths are now fixed** - generation and analysis scripts use consistent paths

4. **Each dilemma gets its own file** for easier processing and debugging

5. **The system analyzes real LLM responses** - not templates or placeholders

## Troubleshooting:

- **"No response files found"**: Make sure generation completed successfully
- **Unicode errors**: Already fixed in the latest version
- **Path errors**: Already fixed - scripts now use absolute paths
- **API errors**: Check your OpenAI API key and credits

## Summary:
1. Generate: Creates 54 LLM responses in `generation_logs/`
2. Analyze: Processes all responses and creates comprehensive analysis
3. Reports: Saves all results in `automated_analysis_results/`

The entire pipeline is now ready to use for your deixis research!