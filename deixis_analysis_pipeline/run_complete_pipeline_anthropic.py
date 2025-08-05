#!/usr/bin/env python3
"""
MASTER DEIXIS ANALYSIS PIPELINE RUNNER - ANTHROPIC CLAUDE VERSION
One-command execution of the complete analysis pipeline using Claude 3.5 Sonnet
"""

import subprocess
import sys
import asyncio
from pathlib import Path

def run_command(command, description):
    """Run a command and handle output."""
    print(f"\n🔄 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completed successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"[FAILED] {description} failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] {description} failed with exception: {e}")
        return False
        
    return True

def main():
    """Run the complete deixis analysis pipeline with Anthropic Claude."""
    
    print("🚀 COMPLETE DEIXIS ANALYSIS PIPELINE - ANTHROPIC CLAUDE 3.5 SONNET")
    print("=" * 60)
    print("🎯 One-command execution from questions to research insights")
    print("🤖 Using Anthropic Claude 3.5 Sonnet via OpenRouter")
    print("🔬 Generates: CSV data, JSON results, detailed reports")
    print("=" * 60)
    
    # Check if we're in the right directory
    pipeline_dir = Path(__file__).parent
    print(f"📁 Pipeline directory: {pipeline_dir}")
    
    # Step 1: Generate LLM Responses using Anthropic
    generation_script = pipeline_dir / "generation_scripts" / "generate_responses_anthropic.py"
    if not generation_script.exists():
        print(f"[ERROR] Generation script not found: {generation_script}")
        return False
    
    print(f"\n🤖 STEP 1: GENERATING LLM RESPONSES WITH CLAUDE 3.5 SONNET")
    json_path = pipeline_dir / "input_questions" / "all_dilemmas_deictic_questions.json"
    cmd1 = f"cd {pipeline_dir.parent} && python {generation_script} --json-path {json_path}"
    if not run_command(cmd1, "LLM Response Generation (Claude 3.5 Sonnet)"):
        return False
    
    # Step 2: Run Complete Analysis
    analysis_script = pipeline_dir / "analysis_scripts" / "run_complete_deixis_analysis_fixed.py"
    if not analysis_script.exists():
        print(f"[ERROR] Analysis script not found: {analysis_script}")
        return False
    
    print(f"\n🔍 STEP 2: RUNNING COMPREHENSIVE ANALYSIS")
    cmd2 = f"cd {pipeline_dir.parent} && python {analysis_script}"
    if not run_command(cmd2, "Comprehensive Analysis"):
        return False
    
    # Step 3: Generate Additional Reports (optional, continues on failure)
    reports_script = pipeline_dir / "utilities" / "generate_missing_reports.py"
    if reports_script.exists():
        print(f"\n📄 STEP 3: GENERATING ADDITIONAL REPORTS")
        cmd3 = f"cd {pipeline_dir.parent} && python {reports_script}"
        run_command(cmd3, "Additional Report Generation")  # Don't fail pipeline if this fails
    
    print(f"\n🎉 PIPELINE COMPLETE!")
    print("=" * 60)
    print("📁 Check these directories for results:")
    print("   📊 generation_logs/ - LLM responses (Claude 3.5 Sonnet)")
    print("   📊 automated_analysis_results/ - Complete analysis data")
    print("=" * 60)
    print("📋 Key output files:")
    print("   🔢 comprehensive_research_data.csv - Research dataset")
    print("   💾 complete_analysis_results.json - Raw analysis data")
    print("   📄 detailed_analysis_report.md - Human-readable analysis")
    print("   🎯 FINAL_DEIXIS_RESEARCH_REPORT.md - Executive summary")
    print("=" * 60)
    print("🤖 Model: Anthropic Claude 3.5 Sonnet (via OpenRouter)")
    print("🌡️ Temperature: 0.9 (high variability for generation)")
    print("=" * 60)
    print("[READY] Ready for statistical analysis and publication!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)