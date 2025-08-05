# Fix for Generation Logs Path Issue

## The Problem

There's a path mismatch between where the generation scripts save their output and where the analysis script looks for them:

1. **Generation Scripts Save To:**
   - `generate_responses_only.py`: `generation_logs/academic_integrity_[timestamp]/`
   - `generate_responses_multi_dilemma.py`: `generation_logs/multi_dilemma_[timestamp]/`
   
   These paths are relative to where the script is run from.

2. **Analysis Script Looks In:**
   - `deixis_analysis_pipeline/generation_logs/` (after our fix)
   
## Current Situation

- When we ran the generation script during testing, it was interrupted
- The directories `deixis_analysis_pipeline/generation_logs/multi_dilemma_20250804_163350/` were created but are empty
- The only existing response data is in `generation_logs/academic_integrity_20250803_205333/` (parent directory)

## The Fix

We need to ensure the generation scripts save to the correct location. Here are two options:

### Option 1: Update the Generation Scripts (Recommended)

Modify the output directory in both generation scripts to use an absolute path:

```python
# In generate_responses_multi_dilemma.py, line 215:
output_dir = Path(__file__).parent.parent / "generation_logs" / f"multi_dilemma_{timestamp}"

# In generate_responses_only.py, line 74:
output_dir = Path(__file__).parent.parent / "generation_logs" / f"academic_integrity_{timestamp}"
```

### Option 2: Run Scripts from Correct Directory

Always run the generation scripts from the `deixis_analysis_pipeline` directory:

```bash
cd deixis_analysis_pipeline
python generation_scripts/generate_responses_multi_dilemma.py --json-path input_questions/all_dilemmas_deictic_questions.json
```

## What Will Be Generated

When `generate_responses_multi_dilemma.py` runs with `all_dilemmas_deictic_questions.json`, it will create:

```
generation_logs/multi_dilemma_[timestamp]/
├── whistleblower_risk_responses.json      # 9 responses for dilemma 1
├── scholarship_fraud_responses.json        # 9 responses for dilemma 2  
├── icu_bed_allocation_responses.json       # 9 responses for dilemma 3
├── trolley_problem_responses.json          # 9 responses for dilemma 4
├── ai_consciousness_responses.json         # 9 responses for dilemma 5
├── memory_modification_responses.json      # 9 responses for dilemma 6
└── generation_summary.json                 # Session metadata
```

Total: 54 LLM responses (6 dilemmas × 9 framings)

## Verification

The existing `academic_integrity_20250803_205333` responses show that the system IS analyzing real LLM responses:
- Each framing gets a unique response from GPT-4o
- Responses vary in length (1700-2100 characters)
- Generation times are recorded (9-16 seconds per response)
- The responses show different reasoning patterns based on the deictic framing

## Next Steps

1. Apply the fix to the generation scripts
2. Run the complete generation (15-30 minutes for all 54 responses)
3. The analysis script will then find and analyze all responses
4. Complete analysis outputs will be generated in `automated_analysis_results/`