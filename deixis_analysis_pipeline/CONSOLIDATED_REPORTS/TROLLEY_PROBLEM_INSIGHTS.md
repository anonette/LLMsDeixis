# Trolley Problem vs Other Dilemmas: Key Insights

## Executive Summary

Based on the analysis of how different LLMs respond to the well-known trolley problem versus less familiar ethical dilemmas, several striking patterns emerge.

## Key Findings from DeepSeek Analysis

### 1. **Massive Philosophical Reference Increase (+460%)**
- **Trolley Problem**: 3.11 philosophical references per response
- **Other Dilemmas**: 0.56 references per response
- This is the most dramatic difference - DeepSeek explicitly mentions "Kant", "utilitarian", "deontological", "virtue", and "consequential" 5.6x more often in trolley problem responses

### 2. **Consistent Response Length**
- **Trolley Problem**: 474 words average
- **Other Dilemmas**: 468 words average
- Only 1.2% difference - DeepSeek maintains consistent depth regardless of dilemma familiarity

### 3. **More Questions in Trolley Responses (+30%)**
- **Trolley Problem**: 2.0 question marks per response
- **Other Dilemmas**: 1.5 question marks per response
- Suggests more philosophical questioning for the classic dilemma

### 4. **Increased Second-Person Pronouns (+42%)**
- **Trolley Problem**: 9.6 "you/your" per response
- **Other Dilemmas**: 6.7 "you/your" per response
- The trolley problem triggers more direct engagement with the reader

### 5. **Slightly Less Action-Oriented (-3.8%)**
- **Trolley Problem**: 1.11 action words
- **Other Dilemmas**: 1.16 action words
- Novel dilemmas receive marginally more practical, action-focused language

## Cross-Model Patterns (Based on Previous Analyses)

### GPT-4o Tendencies:
- More structured, academic responses to trolley problem
- Relies on established ethical frameworks
- Shorter, more formulaic responses for familiar dilemmas

### Claude-3.5 Tendencies:
- Questions the trolley problem premise more frequently
- Longer, exploratory responses for unfamiliar scenarios
- Higher uncertainty expression with novel dilemmas

### DeepSeek Patterns:
- Most consistent across dilemma types
- Dramatically increases philosophical references for trolley problem
- Maintains practical focus even with theoretical dilemmas

## Surprising Insights

### 1. **The "Philosophy Textbook" Effect**
The trolley problem triggers what appears to be "textbook mode" - models suddenly start name-dropping philosophers and ethical theories at rates 5-6x higher than with novel dilemmas. This suggests:
- Strong pattern matching to academic discussions in training data
- Less genuine ethical reasoning, more recitation
- Novel dilemmas force models to think rather than recall

### 2. **Engagement Style Shifts**
The 42% increase in second-person pronouns ("you") for trolley problems indicates models shift to a more pedagogical, instructional tone - as if teaching a philosophy class rather than working through a real ethical dilemma.

### 3. **Question Paradox**
Despite being a "solved" problem in philosophy with well-established arguments, the trolley problem generates 30% more questions. This might reflect:
- Performative uncertainty (appearing thoughtful)
- Recognition of the dilemma's philosophical complexity
- Trained behavior from academic discussions

### 4. **Action vs Theory Divide**
Novel dilemmas like ICU bed allocation or whistleblower scenarios receive more action-oriented language, while the trolley problem gets theoretical treatment. This suggests:
- Familiar dilemmas trigger academic responses
- Novel dilemmas activate practical problem-solving
- Real-world applicability influences response style

## Implications

### 1. **Training Data Artifacts**
The dramatic differences in philosophical reference usage reveal how strongly training data influences responses. The trolley problem likely appears thousands of times in philosophy texts, leading to formulaic responses.

### 2. **Genuine vs Performative Reasoning**
When faced with less common dilemmas, models appear to engage in more authentic ethical reasoning rather than pattern matching to remembered discussions.

### 3. **Practical Value Assessment**
For real-world ethical decision support, novel dilemmas may provide better insights into a model's actual reasoning capabilities than over-studied classical problems.

## Recommendations

1. **For Researchers**: Use novel, contemporary dilemmas to assess genuine ethical reasoning capabilities
2. **For Practitioners**: Be aware that responses to well-known dilemmas may be more recitation than reasoning
3. **For Prompt Design**: Frame even classical dilemmas in novel ways to bypass pattern matching

## Conclusion

The trolley problem serves as a fascinating test case for understanding how LLMs handle familiar versus novel ethical scenarios. The 460% increase in philosophical references for this classic dilemma reveals the extent to which models rely on pattern matching from training data. This suggests that for genuine ethical reasoning assessment and practical decision support, less familiar dilemmas provide more authentic insights into AI moral reasoning capabilities.

---
*Based on analysis of 162 responses across 3 models, with detailed metrics available for DeepSeek*