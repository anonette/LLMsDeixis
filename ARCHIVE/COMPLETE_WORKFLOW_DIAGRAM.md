# Complete Workflow: From Data Generation to Final Reports

## Visual Workflow Diagram

```mermaid
graph TD
    A[Start] --> B[Load Ethical Dilemmas]
    B --> C{For Each Dilemma}
    
    C --> D[Interrogative Transformation]
    D --> E[Generate 8 Deictic Framings]
    
    E --> F1[First-person: "What do I do?"]
    E --> F2[Second-person: "What do you do?"]
    E --> F3[Dialogic: "What do we do?"]
    E --> F4[Impersonal: "What does one do?"]
    E --> F5[Cosmological: "What do the ancestors say?"]
    E --> F6[Spatial: "What happens here?"]
    E --> F7[Temporal-past: "What did you do?"]
    E --> F8[Temporal-future: "What will you do?"]
    
    F1 --> G[LLM Response Generation]
    F2 --> G
    F3 --> G
    F4 --> G
    F5 --> G
    F6 --> G
    F7 --> G
    F8 --> G
    
    G --> H[Response Analysis]
    
    H --> I1[Deixis Analysis]
    H --> I2[Pronoun Agency Analysis]
    
    I1 --> J1[Deictic Markers]
    I1 --> J2[Spatial/Temporal Patterns]
    
    I2 --> K1[Pronoun Ratios]
    I2 --> K2[Agency Concentration]
    I2 --> K3[Agency Type Classification]
    
    J1 --> L[Expert Analysis Layer]
    J2 --> L
    K1 --> L
    K2 --> L
    K3 --> L
    
    L --> M1[Critical Expert]
    L --> M2[Evidence Expert]
    L --> M3[Pronoun Agency Expert]
    
    M1 --> N[Report Generation]
    M2 --> N
    M3 --> N
    
    N --> O1[Research Report]
    N --> O2[Pronoun Agency Report]
    N --> O3[Critical Analysis]
    N --> O4[Evidence Findings]
    N --> O5[Visualizations]
    
    O1 --> P[Session Output Directory]
    O2 --> P
    O3 --> P
    O4 --> P
    O5 --> P
    
    C --> |More Dilemmas| C
    C --> |All Complete| P
    
    P --> Q[End]
```

## Step-by-Step Process

### 1. **Data Preparation** (5 minutes)
```bash
# Create or verify ethical_dilemmas.json exists
cat ethical_dilemmas.json
```

### 2. **Environment Setup** (One-time, 5 minutes)
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Verify dependencies
pip list | grep -E "openai|pandas|matplotlib"
```

### 3. **Run Complete Analysis** (10-30 minutes depending on dilemmas)
```bash
python run_analysis_with_pronoun_agency.py
```

### 4. **Monitor Progress**
The script will show real-time progress:
```
================================================================================
ENHANCED DEICTIC ETHICAL ANALYSIS WITH PRONOUN AGENCY
================================================================================
Starting at: 2025-08-03 11:30:00

Initializing analyzers...
Loading ethical dilemmas...
Loaded 3 dilemmas

============================================================
Analyzing Dilemma 1/3: Tech Company Whistleblowing
============================================================

FIRST_PERSON - Response generated
  Length: 245 chars
  Deictic markers: 12 found

SECOND_PERSON - Response generated
  Length: 238 chars
  Deictic markers: 10 found

[... continues for all framings ...]

Running pronoun agency analysis...
✓ Pronoun agency analysis complete

Running critical expert analysis...
✓ Critical analysis complete

Running evidence-based expert analysis...
✓ Evidence-based analysis complete
```

### 5. **Output Structure**
```
automated_analysis_results/
└── session_20250803_113000/
    ├── all_results.json                    # Raw LLM responses and analysis
    ├── session_data_with_pronouns.json     # Complete session data
    ├── research_report.md                  # Main findings report
    ├── pronoun_agency_analysis.md          # Detailed agency analysis
    ├── critical_analysis_report.md         # Methodological critique
    ├── evidence_based_findings.md          # Empirical patterns
    ├── pronoun_agency_analysis_*.png       # 4-panel visualization
    └── analysis_summary.json               # Quick reference summary
```

## Data Flow Details

### Input: Ethical Dilemmas
```json
{
  "id": "whistleblowing_tech",
  "title": "Tech Company Whistleblowing",
  "description": "You discover...",
  "ethical_dimensions": ["privacy", "loyalty"]
}
```

### Processing: Interrogative Transformation
```
Original: "You discover your company is collecting user data..."
↓
First-person: "I discover my company is collecting user data. What do I do?"
Second-person: "You discover your company is collecting user data. What do you do?"
Dialogic: "We discover our company is collecting user data. What do we do?"
```

### Analysis: Pronoun Metrics
```
Response: "I must report this immediately. I cannot allow..."
↓
Pronouns found: {I: 5, me: 2, my: 1}
Agency concentration: 0.85
Agency type: individual
```

### Output: Research-Ready Data
```json
{
  "framing": "first_person",
  "pronoun_agency": {
    "agency_type": "individual",
    "concentration": 0.85,
    "ratios": {
      "first_singular": 0.89,
      "second_person": 0.0,
      "first_plural": 0.11
    }
  }
}
```

## Time Estimates

- **Setup**: 5-10 minutes (one-time)
- **Per dilemma**: ~2-3 minutes
- **10 dilemmas**: ~20-30 minutes
- **50 dilemmas**: ~2-3 hours
- **Report generation**: 1-2 minutes

## Verification Checklist

After running, verify:

- [ ] Session directory created with timestamp
- [ ] All JSON files contain data
- [ ] Markdown reports are readable
- [ ] PNG visualization exists
- [ ] No error messages in console

## Quick Troubleshooting

### If analysis fails:
1. Check API key: `echo %OPENROUTER_API_KEY%`
2. Check internet connection
3. Verify JSON format of dilemmas
4. Check console for specific error messages

### If reports are incomplete:
1. Check session_data_with_pronouns.json has data
2. Verify all expert agents completed
3. Look for partial results in JSON files

## Next Steps After Analysis

1. **Review Reports**: Start with research_report.md for overview
2. **Check Visualizations**: Open PNG files for visual patterns
3. **Statistical Analysis**: Import JSON data into R/Python/SPSS
4. **Publication**: Use markdown reports as basis for papers

The entire workflow is designed to be run with a single command while providing comprehensive, research-ready output.