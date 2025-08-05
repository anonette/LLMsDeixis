# Analysis Methodology

## Overview
The system uses a hybrid approach to analyze LLM responses to ethical dilemmas:

## 1. Question Generation (Interrogative Transformer)
- Generates direct questions without meta-instructions
- Example: "You discover your company's app has a security flaw... What do you do?"

## 2. LLM Response Generation
- Temperature: **0.9** (high variability for diverse ethical responses)
- Models rotate between: GPT-4, Claude 3.5, DeepSeek
- Each model responds to the direct question

## 3. Response Analysis (Hybrid Approach)

### A. LLM-Based Analysis (Temperature: 0.7)
Three types of analysis are performed using LLM agents:

1. **Agency Distribution Analysis**
   - Identifies primary decision-makers
   - Maps how agency is distributed
   - Determines individual vs collective responsibility
   - Output: JSON with primary_agent, agency_distribution, etc.

2. **Ethical Framing Analysis**
   - Detects ethical frameworks (utilitarian, deontological, etc.)
   - Identifies moral reasoning patterns
   - Analyzes consequence vs duty orientation
   - Output: JSON with primary_framework, reasoning_type, etc.

3. **Rhetorical Posture Analysis**
   - Examines mode of moral address
   - Analyzes rhetorical strategies
   - Identifies persuasion techniques
   - Output: JSON with moral_address, rhetorical_mode, etc.

### B. Direct Code Analysis (No LLM)
Programmatic counting of linguistic markers:

1. **Deictic Marker Analysis**
   - Counts pronouns (I/me, you/your, we/us, etc.)
   - Counts temporal markers (now, then, urgent, etc.)
   - Counts spatial markers (here, there, toward, etc.)
   - Counts obligation language (should, must, ought, etc.)
   - No LLM involved - pure pattern matching

## Temperature Settings
- **Response Generation**: 0.9 (high creativity)
- **Analysis Tasks**: 0.7 (balanced creativity/consistency)
- **Direct Code Analysis**: N/A (no LLM used)

## Data Flow
1. Interrogative question → LLM
2. LLM response → Analysis pipeline
3. Analysis results → Structured data storage
4. All analyses focus on the LLM's response text, not the questions