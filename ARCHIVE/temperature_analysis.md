# Temperature Usage Analysis in Deixis Ethical Analyzer

## Overview
The Deixis Ethical Analyzer uses a dual-temperature strategy to balance creativity in ethical response generation with reliability in structured analysis tasks.

## Temperature Settings

### 1. High Temperature (0.9) - Creative Generation
**Used for:** Generating ethical responses to dilemmas
**Method:** `generate_ethical_response()`
**Purpose:** Maximizes creativity and variability in ethical reasoning

**Additional parameters for high variability:**
- `top_p`: 0.95 (nucleus sampling for additional randomness)
- `frequency_penalty`: 0.3 (reduces repetition)
- `presence_penalty`: 0.3 (encourages novel content)

### 2. Moderate Temperature (0.5) - Structured Analysis
**Used for:** JSON-based analysis tasks
**Methods:**
- `analyze_agency_distribution()` - Extracts agency patterns
- `analyze_ethical_framing()` - Identifies ethical frameworks
- `analyze_rhetorical_posture()` - Analyzes rhetorical characteristics

**Purpose:** Ensures consistent, parseable JSON outputs

## Workflow Analysis

For each dilemma-framing combination, the system follows this sequence:

1. **Transform dilemma** using deictic framing (no LLM call)
2. **Generate response** at temp 0.9 (creative)
3. **Analyze agency** at temp 0.5 (structured)
4. **Analyze ethics** at temp 0.5 (structured)
5. **Analyze rhetoric** at temp 0.5 (structured)

This creates a pattern of: 0.9 → 0.5 → 0.5 → 0.5 for each analysis cycle.

## Temperature Switching Mechanism

```python
# Pattern used in all analysis methods:
original_temp = self.temperature  # Save current (0.9)
self.temperature = 0.5           # Switch for analysis
response = await self._make_llm_request(prompt)
self.temperature = original_temp  # Restore to 0.9
```

## Model Rotation Impact

The system also rotates between three models:
- OpenAI GPT-4
- Anthropic Claude 3.5 Sonnet  
- DeepSeek Chat

Combined with temperature variation, this creates:
- **12 unique generation configurations** (3 models × 2 temps × various prompts)
- **High diversity** in responses across analyses

## Implications

### For Response Generation (0.9):
- **Pros:** Rich, varied ethical perspectives; avoids formulaic responses
- **Cons:** Less predictable; may occasionally produce tangential content

### For Analysis Tasks (0.5):
- **Pros:** Reliable JSON parsing; consistent categorization
- **Cons:** May miss nuanced interpretations in edge cases

### Overall Design Philosophy:
The dual-temperature approach reflects a key insight: **creative ethical reasoning** and **structured analysis** have different optimal temperature requirements. By dynamically adjusting temperature based on task type, the system achieves both creative diversity and analytical reliability.

## Log Pattern Explanation

The alternating temperature logs you observe:
```
INFO: Generated response using openai/gpt-4o at temp 0.9
INFO: Generated response using anthropic/claude-3.5-sonnet at temp 0.5
INFO: Generated response using deepseek/deepseek-chat at temp 0.5
INFO: Generated response using openai/gpt-4o at temp 0.5
```

This pattern emerges because:
1. First call generates the ethical response (0.9)
2. Next three calls analyze that response (0.5 each)
3. Pattern repeats for next dilemma/framing combination

The model rotation ensures no single model dominates the analysis, while temperature variation ensures appropriate creativity or consistency for each task type.