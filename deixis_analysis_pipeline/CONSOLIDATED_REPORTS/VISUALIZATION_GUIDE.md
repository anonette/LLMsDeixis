# Deixis Analysis Visualization Guide

## Overview

This guide explains all the visualizations generated for the deixis analysis project. These visualizations help understand how different LLM models (GPT-4o, Claude 3.5, and DeepSeek) respond to ethical dilemmas with varying deictic framings, with special attention to the Trolley Problem.

## Location

All visualizations are stored in: `CONSOLIDATED_REPORTS/visualizations/`

---

## Visualization Catalog

### 1. **comprehensive_summary.png**
**Purpose**: Provides a comprehensive overview of all key metrics across models and dilemma types.

**What it shows**:
- Top row: Three bar charts comparing Trolley Problem vs Other Dilemmas
  - Response Length (word count)
  - Philosophical References
  - Second Person Pronoun Usage
- Middle row: Three pie charts showing the distribution of words between Trolley and Other dilemmas for each model
- Bottom: Heatmap showing percentage differences in key metrics

**Key Insights**:
- Quickly compare all models at a glance
- Identify which model shows the most dramatic differences between Trolley and other dilemmas
- See relative response lengths and philosophical engagement

---

### 2. **trolley_detailed_comparison.png**
**Purpose**: Deep dive into how models respond differently to the Trolley Problem vs other ethical dilemmas.

**What it shows**: Six subplots comparing:
1. Average Word Count
2. Average Sentence Count
3. Philosophical References
4. First Person Pronoun Usage
5. Second Person Pronoun Usage
6. Uncertainty Expression

**Key Insights**:
- **GPT-4o**: Shorter responses for Trolley, but MORE philosophical references
- **Claude 3.5**: Dramatically shorter Trolley responses across all metrics
- **DeepSeek**: Similar response lengths, but higher philosophical content in Trolley

---

### 3. **trolley_difference_heatmap.png**
**Purpose**: Shows percentage changes between Trolley Problem and other dilemmas using color coding.

**What it shows**: 
- Rows represent different metrics
- Columns represent the three models
- Colors indicate: Green (higher in Trolley), Red (lower in Trolley)
- Numbers show exact percentage differences

**Key Insights**:
- **GPT-4o**: +1025% utilitarian references in Trolley, +733% first-person usage
- **Claude 3.5**: -64% length, -83% second-person, but +900% utilitarian references
- **DeepSeek**: Very consistent except +311% first-person plural, +459% philosophical total

---

### 4. **pronoun_usage_analysis.png**
**Purpose**: Detailed breakdown of pronoun usage patterns across models.

**What it shows**: Two side-by-side charts
- Left: Trolley Problem pronoun usage
- Right: Other Dilemmas pronoun usage
- Four pronoun categories: First Person, Second Person, Third Person, First Plural

**Key Insights**:
- **DeepSeek** uses significantly more "you" (second person) in Trolley Problem
- **GPT-4o** shows balanced pronoun usage
- **Claude 3.5** uses minimal pronouns in Trolley responses
- First-person plural ("we") usage is low across all models

---

### 5. **philosophical_frameworks_detailed.png**
**Purpose**: Shows how each model references different philosophical frameworks.

**What it shows**: Three panels (one per model) comparing:
- Kantian references
- Utilitarian references  
- Deontological references
- Virtue Ethics references
- Consequentialist references

**Key Insights**:
- **GPT-4o & DeepSeek**: Strong utilitarian and deontological focus in Trolley
- **Claude 3.5**: Minimal philosophical framework usage overall
- All models show increased philosophical engagement in Trolley vs other dilemmas

---

### 6. **ethical_framework_comparison.png** (from original script)
**Purpose**: Bar chart showing ethical framework usage percentages by model.

**What it shows**:
- Five frameworks compared across three models
- Direct percentage comparison

**Key Insights**:
- **DeepSeek**: Highest framework integration (>80% in most categories)
- **GPT-4o**: Utilitarian dominant (45%)
- **Claude 3.5**: More balanced but lower overall usage

---

### 7. **framing_sensitivity_heatmap.png** (from original script)
**Purpose**: Shows how sensitive each model is to different deictic framings.

**What it shows**:
- Rows: Nine different deictic framings (Temporal, Reflexive, Dialogic, etc.)
- Columns: Three models
- Scale: 0-10 sensitivity score

**Key Insights**:
- **DeepSeek**: Most sensitive to Dialogic framing (10/10)
- **Claude 3.5**: Most sensitive to Reflexive framing (9/10)
- **GPT-4o**: Most sensitive to Temporal framing (9/10)
- All models show varying sensitivity to different framings

---

### 8. **model_summary_dashboard.png** (from original script)
**Purpose**: Four-panel dashboard summarizing model characteristics.

**What it shows**:
1. Ethical Framework Distribution (pie chart for GPT-4o)
2. Recommendation Rates (DeepSeek highest at 96.3%)
3. Generation Efficiency (words per minute scatter plot)
4. Sensitivity vs Consistency (quality metrics scatter)

**Key Insights**:
- **DeepSeek**: Most action-oriented (96.3% recommendation rate)
- **Claude 3.5**: Most efficient (slower but longer responses)
- **DeepSeek**: Best balance of sensitivity and consistency

---

### 9. **response_characteristics_comparison.png** (from original script)
**Purpose**: Compares response characteristics and creates a radar chart for normalized comparison.

**What it shows**:
- Left: Raw values bar chart (word count, recommendation rate, generation time, framework integration)
- Right: Radar chart showing normalized characteristics

**Key Insights**:
- **DeepSeek**: Highest framework integration (4.1 frameworks per response)
- **Claude 3.5**: Longest responses (750 words average)
- **GPT-4o**: Balanced across metrics

---

### 10. **response_length_by_framing.png** (from original script)
**Purpose**: Shows how response length varies by deictic framing type.

**What it shows**:
- Nine deictic framings on x-axis
- Average character count on y-axis
- Three bars per framing (one per model)

**Key Insights**:
- **Dialogic framing**: Produces longest responses (especially from DeepSeek)
- **Second Person framing**: Produces shortest responses (especially from Claude)
- **DeepSeek**: Most variable response length across framings
- **Claude 3.5**: Most consistent response length

---

## Interpreting the Results

### Color Schemes
- **Red (#E63946)**: Trolley Problem data
- **Blue (#457B9D)**: Other Dilemmas data
- **GPT-4o**: Blue (#2E86AB)
- **Claude 3.5**: Purple (#A23B72)
- **DeepSeek**: Orange (#F18F01)

### Key Findings Summary

1. **The Trolley Problem Effect**: All models respond differently to the Trolley Problem compared to other dilemmas, but in different ways:
   - GPT-4o: Shorter but more philosophically dense
   - Claude 3.5: Much shorter and less detailed
   - DeepSeek: Similar length but more philosophical

2. **Deictic Framing Matters**: All models show sensitivity to how questions are framed (temporal, dialogic, reflexive, etc.)

3. **Model Personalities**:
   - **GPT-4o**: Balanced, utilitarian-leaning
   - **Claude 3.5**: Concise, balanced across frameworks
   - **DeepSeek**: Comprehensive, action-oriented, high philosophical integration

## Using These Visualizations

### For Academic Writing
- Reference specific visualizations by filename
- Use the comprehensive_summary.png for overview sections
- Use detailed charts for in-depth analysis of specific phenomena

### For Presentations
- Start with comprehensive_summary.png for overview
- Use model_summary_dashboard.png for executive summary
- Use specific charts (trolley, pronoun, framework) for detailed findings
