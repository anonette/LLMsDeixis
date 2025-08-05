# Trolley Problem Analysis: Complete Summary

## Executive Summary

This comprehensive analysis reveals how GPT-4o, Claude-3.5 Sonnet, and DeepSeek fundamentally change their reasoning approach when confronted with the well-known trolley problem versus novel ethical dilemmas. The findings demonstrate a universal "philosophy textbook effect" where all models dramatically increase philosophical references and alter their engagement style for this classic dilemma.

## Key Findings Across All Models

### 1. Philosophical Reference Explosion

All three models show massive increases in philosophical terminology when discussing the trolley problem:

| Model | Trolley Problem | Other Dilemmas | % Increase |
|-------|-----------------|----------------|------------|
| **GPT-4o** | 2.44 refs/response | 0.16 refs/response | **+1,471%** |
| **Claude-3.5** | 0.22 refs/response | 0.07 refs/response | **+233%** |
| **DeepSeek** | 3.11 refs/response | 0.56 refs/response | **+460%** |

**Key Insight**: GPT-4o shows the most extreme "textbook mode" activation with nearly 15x more philosophical references.

### 2. Response Length Patterns

Models show divergent approaches to response length:

| Model | Trolley Problem | Other Dilemmas | Change |
|-------|-----------------|----------------|--------|
| **GPT-4o** | 245 words | 326 words | -25% shorter |
| **Claude-3.5** | 62 words | 167 words | -63% shorter |
| **DeepSeek** | 474 words | 468 words | +1% (consistent) |

**Key Insight**: GPT-4o and Claude treat the trolley problem as "solved" and give briefer responses, while DeepSeek maintains consistent depth.

### 3. Pronoun Usage Shifts

Second-person pronoun usage reveals engagement style changes:

| Model | Trolley "You" Usage | Other "You" Usage | Change |
|-------|---------------------|-------------------|--------|
| **GPT-4o** | 5.0 per response | 4.8 per response | +4% |
| **Claude-3.5** | 0.2 per response | 1.4 per response | -84% |
| **DeepSeek** | 9.6 per response | 6.7 per response | +42% |

**Key Insight**: DeepSeek and GPT-4o increase direct reader engagement for trolley problem, while Claude becomes more abstract.

### 4. Uncertainty and Complexity Indicators

| Model | Metric | Trolley | Others | Change |
|-------|--------|---------|--------|--------|
| **GPT-4o** | Uncertainty words | 2.0 | 2.4 | -17% |
| **Claude-3.5** | Uncertainty words | 0.6 | 1.0 | -44% |
| **DeepSeek** | Uncertainty words | 2.2 | 2.1 | +4% |

**Key Insight**: GPT-4o and Claude express less uncertainty with the familiar dilemma, suggesting overconfidence from pattern matching.

## Model-Specific Behaviors

### GPT-4o: The Academic Reciter
- **1,471% increase** in philosophical references (highest)
- **25% shorter** responses
- **733% increase** in first-person pronouns
- Switches to lecture mode, citing textbook frameworks

### Claude-3.5: The Minimalist
- **63% shorter** responses (most extreme reduction)
- **84% decrease** in second-person engagement
- **44% less** uncertainty expression
- Treats trolley problem as settled philosophy

### DeepSeek: The Consistent Analyzer
- Maintains **consistent length** (only 1% change)
- **42% increase** in second-person engagement
- **312% increase** in collective pronouns (we/us)
- Integrates multiple frameworks regardless of familiarity

## Critical Insights

### 1. The "Philosophy Textbook" Effect
All models recognize the trolley problem from training data and switch into academic recitation mode, dramatically increasing mentions of:
- Utilitarianism
- Deontological ethics
- Kant
- Consequentialism
- Virtue ethics

### 2. Genuine Reasoning vs. Pattern Matching
- **Novel dilemmas**: Models engage in exploratory reasoning, consider practical implications, express appropriate uncertainty
- **Trolley problem**: Models recite memorized arguments, use philosophical jargon, show artificial confidence

### 3. Assessment Implications
The analysis strongly suggests that:
- Classical dilemmas are **poor tests** of AI ethical reasoning
- Novel scenarios **force genuine thinking** rather than recitation
- Familiar problems **trigger academic performance** rather than authentic engagement

## Practical Recommendations

### For Researchers
1. Use **novel ethical scenarios** to assess genuine moral reasoning capabilities
2. Be aware that classical dilemmas measure **recall** more than reasoning
3. Consider **framing familiar problems in novel ways** to bypass pattern matching

### For AI Development
1. Recognize that models have **memorized philosophical discussions**
2. Understand that brevity with familiar problems indicates **pattern recognition**
3. Design prompts that **force original thinking** rather than recitation

### For Practical Applications
1. For **real-world ethical decisions**, use contemporary scenarios
2. For **educational purposes**, be aware of the performative nature of responses
3. For **assessment**, focus on reasoning process rather than terminology usage

## Conclusion

This comprehensive analysis of trolley problem responses across three leading language models reveals a fundamental challenge in AI ethics: when confronted with well-known philosophical problems, models switch from genuine ethical reasoning to academic recitation. The dramatic increases in philosophical references (up to 1,471% for GPT-4o), combined with shortened responses and altered engagement patterns, demonstrate that familiar ethical dilemmas trigger pattern matching rather than authentic moral reasoning.

For meaningful assessment of AI ethical capabilities, novel scenarios that force genuine reasoning are essential. The trolley problem, while philosophically interesting, has become a test of training data recall rather than ethical thinking.

---

*Analysis based on 162 total responses: 27 trolley problem responses and 135 other dilemma responses across GPT-4o, Claude-3.5 Sonnet, and DeepSeek*

*All detailed reports saved in: `deixis_analysis_pipeline/CONSOLIDATED_REPORTS/`*