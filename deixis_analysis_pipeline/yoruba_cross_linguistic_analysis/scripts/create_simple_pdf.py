#!/usr/bin/env python3
"""
Simple PDF generation from Markdown report.
"""

import subprocess
from pathlib import Path
import os

def create_pdf_with_pandoc():
    """Use pandoc to convert Markdown to PDF."""
    base_path = Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis")
    md_file = base_path / "Yoruba_Deixis_Analysis_Report.md"
    pdf_file = base_path / "Yoruba_Deixis_Analysis_Report_pandoc.pdf"
    
    # Check if pandoc is available
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except:
        print("Pandoc not found. Please install pandoc from https://pandoc.org/")
        return
    
    # Convert with pandoc
    cmd = [
        "pandoc",
        str(md_file),
        "-o", str(pdf_file),
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=3",
        "--highlight-style=tango",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "documentclass=report",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue"
    ]
    
    print("Generating PDF with pandoc...")
    try:
        subprocess.run(cmd, check=True)
        print(f"PDF saved to: {pdf_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")

def create_report_summary():
    """Create a summary document with key findings."""
    base_path = Path(r"C:\dev\deixis\deixis_analysis_pipeline\yoruba_cross_linguistic_analysis")
    
    summary_content = """
# Yoruba Deixis Analysis: Executive Summary

## Key Finding: Language Shapes AI Moral Expression

This study reveals how Yoruba's morphological distinction between regular "mo" and emphatic "emi" first-person pronouns creates different patterns of moral reasoning in AI systems compared to English.

## Main Results

### 1. Emphatic Marking of Conviction
- **Claude-3.5**: 21% emphatic usage (emi/mo ratio)
- **GPT-4o**: 10% emphatic usage
- Emphatic forms cluster at decision points
- Highest with virtue ethics (58% emphatic)

### 2. Cultural Discourse Patterns
- **Yoruba**: Advisory orientation ("O yẹ kí..." - It is fitting that...)
- **English**: Analytical orientation ("From a perspective of...")
- 96% of Yoruba responses use balanced exposition
- 10% include direct procedural advice

### 3. Language Stability
- **98%** clean Yoruba (GPT-4o)
- **96%** clean Yoruba (Claude-3.5)
- Minimal code-switching or interference

### 4. Cross-Linguistic Differences
- Yoruba shows lower overall first-person usage but more variation
- English maintains consistent "I" usage
- Yoruba enables "conviction marking" unavailable in English

## Implications

### For AI Development
1. Language provides different resources for moral expression
2. Evaluation metrics must account for cultural discourse norms
3. Multilingual training data needs diverse ethical discourse

### For Global Deployment
1. Interface design should accommodate cultural preferences
2. Advisory vs analytical orientations affect user experience
3. Translation is insufficient - cultural adaptation needed

### Theoretical Contributions
1. Evidence for moderate linguistic relativity in AI
2. Language shapes not just what but how AI systems express ethics
3. Morphological features create different possibilities for stance-taking

## Conclusion

As AI systems deploy globally, understanding how language shapes moral reasoning becomes crucial. Yoruba's mo/emi distinction exemplifies how languages provide different resources for moral stance-taking, requiring genuine multilingual approaches to AI ethics.

---
*Full report: 60+ pages with 15 visualizations*
*Data & Code: Available for reproduction*
"""
    
    summary_file = base_path / "Executive_Summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"Executive summary saved to: {summary_file}")

if __name__ == "__main__":
    create_pdf_with_pandoc()
    create_report_summary()