# Correct Commands to Run the Pipeline

## The Issue
You were in the `generation_scripts` directory and using the wrong path. Here are the correct commands:

## Option 1: Run from the deixis_analysis_pipeline directory (RECOMMENDED)

```bash
# Make sure you're in the right directory
cd C:\dev\deixisAugust2025\deixis_analysis_pipeline

# Run the generation script
python generation_scripts/generate_responses_multi_dilemma.py --json-path input_questions/all_dilemmas_deictic_questions.json

# Run the analysis script
python analysis_scripts/run_complete_deixis_analysis.py
```

## Option 2: Run from the generation_scripts directory

```bash
# If you're already in generation_scripts
cd C:\dev\deixisAugust2025\deixis_analysis_pipeline\generation_scripts

# Run without the path prefix
python generate_responses_multi_dilemma.py --json-path ../input_questions/all_dilemmas_deictic_questions.json

# Go back to run analysis
cd ..
python analysis_scripts/run_complete_deixis_analysis.py
```

## Complete Step-by-Step:

1. **Start fresh from any directory:**
   ```bash
   cd C:\dev\deixisAugust2025\deixis_analysis_pipeline
   ```

2. **Verify you're in the right place:**
   ```bash
   pwd
   # Should show: C:\dev\deixisAugust2025\deixis_analysis_pipeline
   ```

3. **Run generation (this will take 15-30 minutes):**
   ```bash
   python generation_scripts/generate_responses_multi_dilemma.py --json-path input_questions/all_dilemmas_deictic_questions.json
   ```

4. **After generation completes, run analysis:**
   ```bash
   python analysis_scripts/run_complete_deixis_analysis.py
   ```

## Where Files Are Saved:

### Generation Output:
```
C:\dev\deixisAugust2025\deixis_analysis_pipeline\generation_logs\multi_dilemma_[timestamp]\
├── whistleblower_risk_responses.json
├── scholarship_fraud_responses.json
├── icu_bed_allocation_responses.json
├── trolley_problem_responses.json
├── ai_consciousness_responses.json
├── memory_modification_responses.json
└── generation_summary.json
```

### Analysis Output:
```
C:\dev\deixisAugust2025\automated_analysis_results\complete_analysis_[timestamp]\
├── complete_analysis_results.json
├── comprehensive_research_data.csv
├── detailed_analysis_report.md
├── FINAL_DEIXIS_RESEARCH_REPORT.md
└── research_framework_analysis.json
```

## Common Mistakes to Avoid:

1. ❌ Don't run from inside `generation_scripts` with a path:
   ```bash
   # WRONG - you're already in generation_scripts
   python generation_scripts/generate_responses_multi_dilemma.py
   ```

2. ❌ Don't forget the --json-path argument:
   ```bash
   # WRONG - missing the input file
   python generation_scripts/generate_responses_multi_dilemma.py
   ```

3. ✅ Always run from `deixis_analysis_pipeline` directory:
   ```bash
   # CORRECT
   cd C:\dev\deixisAugust2025\deixis_analysis_pipeline
   python generation_scripts/generate_responses_multi_dilemma.py --json-path input_questions/all_dilemmas_deictic_questions.json
   ```

## Quick Test:

To verify everything is set up correctly without running the full generation:
```bash
cd C:\dev\deixisAugust2025\deixis_analysis_pipeline
python generation_scripts/generate_responses_multi_dilemma.py --help
```

This should show the help message if the script is accessible.