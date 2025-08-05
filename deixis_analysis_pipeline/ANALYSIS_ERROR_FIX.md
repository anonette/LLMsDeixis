# Analysis Pipeline Error Fix

## Issue Summary

The analysis pipeline is encountering several errors:

1. **Async/Await Mismatch**: The script tries to await non-async methods
2. **JSON Parsing Errors**: Expert analysis responses aren't being parsed correctly
3. **Type Errors**: "unhashable type: 'dict'" errors in critical and evidence experts

## Root Causes

### 1. Async Method Issue
The analysis script uses `await` on these methods:
- `await critical_expert.generate_critical_insights(core_results)`
- `await evidence_expert.generate_evidence_based_insights(core_results)`

But these methods are **not async** in the expert modules.

### 2. The Actual Method Signatures

**Critical Expert** (`critical_expert_analysis.py`):
```python
def generate_critical_insights(self, research_question_id: str) -> List[CriticalInsight]:
    # Not async!
```

**Evidence Expert** (`evidence_based_expert_analysis.py`):
```python
def generate_evidence_based_insights(self, research_question_id: str) -> List[EvidenceBasedInsight]:
    # Not async!
```

### 3. Method Mismatch
The analysis script is calling these methods with `core_results` (the full data), but the methods expect a `research_question_id` (a string).

## Quick Fix Options

### Option 1: Remove await and fix method calls
In `run_complete_deixis_analysis.py`, change:
```python
# FROM:
expert_results["critical_expert"] = await critical_expert.generate_critical_insights(core_results)

# TO:
expert_results["critical_expert"] = critical_expert.extract_critical_evidence(core_results)
```

### Option 2: Create wrapper methods
Add async wrapper methods that handle the data correctly:
```python
async def analyze_with_critical_expert(critical_expert, core_results):
    # Extract evidence first
    evidence = critical_expert.extract_critical_evidence(core_results)
    # Then generate insights for each research question
    insights = {}
    for rq in ["RQ1.1", "RQ2.1", "RQ3.1", "RQ4.1", "RQ5.1"]:
        insights[rq] = critical_expert.generate_critical_insights(rq)
    return {"evidence": evidence, "insights": insights}
```

### Option 3: Modify the expert modules
Make the methods async and fix the parameter mismatch.

## Recommended Solution

The quickest fix is to modify the analysis script to:
1. Call the correct methods synchronously (no await)
2. Extract evidence first, then generate insights
3. Handle the proper data flow

## Expert Analysis Parsing Errors

The expert_analysis_agent is failing to parse JSON responses because:
- The LLM responses might not be valid JSON
- The expected format doesn't match the actual response

This needs better error handling and response validation.