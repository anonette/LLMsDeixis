# Session-Based Output Organization

## ✅ Current Structure: All Reports ARE Already in Session Folders

The Deixis Ethical Analyzer **already organizes all outputs by session**. Each analysis run creates a timestamped session folder containing ALL reports and data files together.

## 📁 Actual Session Folder Example

Here's the real structure from an actual analysis session:

```
automated_analysis_results/
└── session_20250730_224025/              # ← All files for this session
    ├── FINAL_RESEARCH_REPORT.md          # Complete academic report
    ├── research_report.md                # Main findings
    ├── critical_analysis_report.md       # Methodological critique
    ├── evidence_based_findings.md        # Concrete examples
    ├── README.md                         # Session overview
    ├── raw_analysis_results.json         # Complete raw data
    ├── comparative_reports.json          # Cross-framework analysis
    ├── session_data.json                 # Session logs
    ├── analysis_report_20250730_224025.json
    ├── deictic_analysis_20250730_224025.csv
    ├── deictic_analysis_20250730_224025.json
    ├── for_python_analysis_20250730_224025.pkl
    ├── for_R_analysis_20250730_224025.csv
    ├── session_summary_20250730_224025.json
    └── README_RESULTS.json               # File descriptions
```

## 🎯 Key Points

1. **Everything is ALREADY session-based** - Each run creates one folder with ALL outputs
2. **No files are scattered** - All 15+ files from a session stay together
3. **Timestamped folders** - Format: `session_YYYYMMDD_HHMMSS`
4. **Self-contained** - Each session folder has everything needed

## 📊 Multiple Sessions Example

When you run the analysis multiple times:

```
automated_analysis_results/
├── session_20250730_223332/    # First run
│   ├── FINAL_RESEARCH_REPORT.md
│   ├── research_report.md
│   └── ... (all other files)
│
├── session_20250730_223704/    # Second run
│   ├── FINAL_RESEARCH_REPORT.md
│   ├── research_report.md
│   └── ... (all other files)
│
└── session_20250730_224025/    # Third run (most complete)
    ├── FINAL_RESEARCH_REPORT.md
    ├── research_report.md
    ├── critical_analysis_report.md
    ├── evidence_based_findings.md
    └── ... (all other files)
```

## 🔍 How the System Works

1. **Start analysis**: `python run_analysis.py`
2. **System creates**: New session folder with timestamp
3. **All outputs go there**: Reports, data, logs - everything
4. **Result**: Clean, organized, session-based structure

## 💡 Benefits of This Structure

- **Easy to find**: All files from one run are together
- **No confusion**: Clear which files belong to which analysis
- **Version control**: Multiple runs don't overwrite each other
- **Complete package**: Share entire session folder with colleagues

## 📂 Other Output Directories

The system uses different base directories for different entry points:

```
deixisAugust2025/
├── automated_analysis_results/    # From run_analysis.py
│   └── session_YYYYMMDD_HHMMSS/
│
├── complete_analysis_results/     # From run_complete_analysis.py
│   └── (session folders)
│
├── test_analysis_results/         # From test scripts
│   └── (test outputs)
│
└── demo_results/                  # From demo scripts
    └── (demo outputs)
```

But within each directory, **everything is organized by session**.

## ✅ Summary

**The system ALREADY puts all reports in session-based folders.** Each analysis run creates one timestamped folder containing:
- All 5 markdown reports
- All 7+ JSON data files  
- All CSV export files
- All metadata and logs

No manual organization needed - it's automatic!