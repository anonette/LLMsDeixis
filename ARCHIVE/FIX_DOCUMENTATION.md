# Fix Documentation: LLM Response Generation

## Issue Description

The system was generating LLM responses that were reframing the ethical dilemma instead of answering the reframed ethical question. This happened because the wrong prompt was being sent to the LLM.

## Root Cause

In the `_analyze_single_framework` method of `deixis_ethical_analyzer.py`, the system was using:
- `transformed_prompt` - which asks the LLM to "Reframe this ethical dilemma using [framing type] language..."
- Instead of `direct_question` - which contains the actual ethical question like "What is the appropriate response when one faces..."

## The Fix

Changed line 498 in `deixis_ethical_analyzer.py`:
```python
# OLD (incorrect):
llm_response = await self.llm_agent.generate_ethical_response(transformed_prompt)

# NEW (correct):
llm_response = await self.llm_agent.generate_ethical_response(direct_question)
```

## How It Works Now

1. **Original Dilemma**: "A software engineer discovers that their company's popular social media app contains a security flaw..."

2. **Reframed Question (IMPERSONAL)**: "What is the appropriate response when one faces competing demands involving hurt and company?"

3. **LLM Response**: Now provides an actual answer to the ethical question, discussing how to handle competing demands, rather than just reframing the dilemma again.

## Example Output

Before the fix, the LLM would respond with:
> "A security vulnerability is identified within a widely-used social media application, resulting in the potential exposure of user data..."

After the fix, the LLM responds with:
> "When facing competing demands involving hurt and company, it's important to address both the emotional and practical aspects..."

## Testing

Run `test_fix_verification.py` to verify the fix is working correctly. The test will:
1. Generate a reframed question
2. Send it to the LLM
3. Check if the response is answering the question (✅) or just reframing (❌)

## Important Notes

- The system still generates both `transformed_prompt` (for logging/analysis) and `direct_question` (for LLM response)
- All analysis functions (agency, ethical framing, rhetorical posture) continue to work on the LLM's response
- The fix ensures the LLM provides substantive ethical guidance rather than just rephrasing the dilemma