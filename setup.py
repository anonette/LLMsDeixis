#!/usr/bin/env python
"""
Setup script for Deixis Analysis Pipeline
Handles initial setup and module copying
"""

import os
import shutil
import sys
from pathlib import Path


def setup_project():
    """Set up the project by copying required modules from ARCHIVE."""
    
    print("🚀 Setting up Deixis Analysis Pipeline...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ is required")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Get project root
    project_root = Path(__file__).parent
    archive_dir = project_root / "ARCHIVE"
    
    if not archive_dir.exists():
        print("❌ Error: ARCHIVE directory not found")
        sys.exit(1)
    
    # List of required modules to copy
    required_modules = [
        "deixis_ethical_analyzer.py",
        "transformer.py",
        "pronoun_agency_analyzer.py",
        "llm_client.py",
        "expert_analysis_agent.py",
        "critical_expert_analysis.py",
        "evidence_based_expert_analysis.py",
        "pronoun_agency_expert.py",
        "detailed_report_generator.py",
        "final_report_generator.py",
        "research_framework_system.py",
        "analysis_logger.py"
    ]
    
    # Copy modules
    print("\n📁 Copying core modules from ARCHIVE...")
    copied = 0
    for module in required_modules:
        src = archive_dir / module
        dst = project_root / module
        
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Copied {module}")
            copied += 1
        else:
            print(f"  ⚠️  Skipped {module} (not found)")
    
    print(f"\n✅ Copied {copied} modules")
    
    # Create .env from example if it doesn't exist
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        shutil.copy2(env_example, env_file)
        print("\n📄 Created .env file from .env.example")
        print("⚠️  Remember to add your OpenAI API key to .env")
    
    # Create output directories
    directories = [
        "generation_logs",
        "automated_analysis_results",
        "analysis_logs",
        "detailed_reports"
    ]
    
    print("\n📁 Creating output directories...")
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
        print(f"  ✅ Created {directory}/")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add your OpenAI API key to .env")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the pipeline: python deixis_analysis_pipeline/run_complete_pipeline.py")


if __name__ == "__main__":
    setup_project()