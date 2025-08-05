# Fix for Analysis File Saving Issue

## Problem Identified
The analysis pipeline was not saving all expected files because `run_complete_pipeline.py` was calling the wrong analysis script.

## Root Cause
- `run_complete_pipeline.py` was calling `run_complete_deixis_analysis.py` instead of `run_complete_deixis_analysis_fixed.py`
- The non-fixed version saves only 3 files
- The fixed version should save 10 files

## Fix Applied
Changed line 62 in `run_complete_pipeline.py`:
```python
# OLD:
analysis_script = pipeline_dir / "analysis_scripts" / "run_complete_deixis_analysis.py"

# NEW:
analysis_script = pipeline_dir / "analysis_scripts" / "run_complete_deixis_analysis_fixed.py"
```

## Expected Files After Fix

When running the fixed analysis script, the following files should be created in the output directory:

1. **core_analysis_results.csv** - Core analysis data in CSV format
2. **core_analysis_results.json** - Core analysis data in JSON format
3. **expert_analysis_results.json** - Results from all expert analyzers
4. **comparative_analysis.json** - Cross-framing comparative analysis
5. **research_framework_analysis.json** - Research framework roadmap
6. **detailed_analysis_report.md** - Comprehensive markdown report
7. **complete_session_log.json** - Full session logging data
8. **comprehensive_research_data.csv** - Research-formatted CSV (from non-fixed version)
9. **complete_analysis_results.json** - Complete results (from non-fixed version)
10. **FINAL_DEIXIS_RESEARCH_REPORT.md** - Final research report (if generator available)

## Current Status
- Only 3 files were being saved: `complete_analysis_results.json`, `comprehensive_research_data.csv`, and an empty `detailed_analysis_report.md`
- After the fix, all 10 files should be properly saved

## To Verify the Fix

Run the analysis again:
```bash
cd deixis_analysis_pipeline
python analysis_scripts/run_complete_deixis_analysis_fixed.py
```

Or run the complete pipeline:
```bash
python run_complete_pipeline.py
```

## Additional Fixes Applied

### Method Compatibility Issues
The fixed script had several method compatibility issues:

1. **Wrong method calls**: Changed from `analyzer.identify_primary_agent()` to `analyzer.llm_agent.analyze_agency_distribution()`
2. **Import issues**: Changed `InterrogativeDeicticTransformer` to `DeicticTransformer`
3. **Data structure handling**: Fixed to handle nested JSON response structure
4. **Logger initialization**: Fixed from `session_id` to `output_dir` parameter

### Current Status After Fixes
- ✅ Script reads all response files correctly
- ✅ Properly handles nested JSON structure
- ✅ Creates output directory
- ✅ Calls correct methods on llm_agent
- ✅ Implemented missing analysis methods:
  - `analyze_moral_reasoning` - Analyzes moral reasoning structure (consequentialist, deontological, etc.)
  - `analyze_affective_stance` - Analyzes emotional tone (detached, empathetic, urgent, etc.)
  - `assess_indexical_coherence` - Assesses consistency of deictic references
- 🔄 Running analysis on all 54 responses with full functionality

## Implementation Details

### New Methods Added to LLMAnalysisAgent
1. **analyze_moral_reasoning**: Classifies responses into moral reasoning categories
2. **analyze_affective_stance**: Identifies emotional stance and intensity
3. **assess_indexical_coherence**: Evaluates consistency of pronouns, temporal, and spatial references

These methods use the same LLM-based analysis pattern as existing methods, ensuring consistency.

## Note on Documentation
Many documentation files still reference `run_complete_deixis_analysis.py`. These should be updated to reference `run_complete_deixis_analysis_fixed.py` for consistency.