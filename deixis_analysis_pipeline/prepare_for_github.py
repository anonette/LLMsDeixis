"""
Prepare the Deixis Analysis Pipeline for GitHub
This script handles all the necessary steps to prepare the repository
"""

import os
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def prepare_repository():
    """Prepare the repository for GitHub"""
    
    print("🚀 Preparing Deixis Analysis Pipeline for GitHub...")
    
    # Get the current directory
    repo_dir = Path.cwd()
    print(f"📁 Working in: {repo_dir}")
    
    # Step 1: Rename README files
    print("\n📝 Step 1: Preparing README files...")
    
    # Check if README_IMPROVED.md exists and rename it
    if (repo_dir / "README_IMPROVED.md").exists():
        # Backup old README if it exists
        if (repo_dir / "README.md").exists():
            shutil.move(str(repo_dir / "README.md"), str(repo_dir / "README_OLD.md"))
            print("  ✓ Backed up old README.md to README_OLD.md")
        
        # Use improved README
        shutil.move(str(repo_dir / "README_IMPROVED.md"), str(repo_dir / "README.md"))
        print("  ✓ Renamed README_IMPROVED.md to README.md")
    
    # Remove other README variants if they exist
    for readme in ["README_GITHUB.md"]:
        if (repo_dir / readme).exists():
            os.remove(repo_dir / readme)
            print(f"  ✓ Removed {readme}")
    
    # Step 2: Initialize git if needed
    print("\n🔧 Step 2: Initializing Git repository...")
    success, stdout, stderr = run_command("git status", cwd=repo_dir)
    
    if not success:
        # Initialize git
        success, stdout, stderr = run_command("git init", cwd=repo_dir)
        if success:
            print("  ✓ Git repository initialized")
        else:
            print(f"  ❌ Failed to initialize git: {stderr}")
            return
    else:
        print("  ✓ Git repository already initialized")
    
    # Step 3: Add all files
    print("\n📦 Step 3: Adding files to git...")
    success, stdout, stderr = run_command("git add .", cwd=repo_dir)
    if success:
        print("  ✓ All files added to git")
    else:
        print(f"  ❌ Failed to add files: {stderr}")
    
    # Step 4: Show git status
    print("\n📊 Step 4: Git status...")
    success, stdout, stderr = run_command("git status --short", cwd=repo_dir)
    if success and stdout:
        print("  Files to be committed:")
        for line in stdout.strip().split('\n')[:10]:  # Show first 10 files
            print(f"    {line}")
        if len(stdout.strip().split('\n')) > 10:
            print(f"    ... and {len(stdout.strip().split('\n')) - 10} more files")
    
    # Step 5: Create commit command
    print("\n💾 Step 5: Ready to commit!")
    print("\nRun the following command to commit:")
    print('git commit -m "Initial commit: Deixis Analysis Pipeline - Multi-Model Ethical Reasoning Study"')
    
    print("\n🌐 Step 6: Push to GitHub")
    print("1. Create a new repository on GitHub: https://github.com/new")
    print("2. Name it: deixis-analysis-pipeline")
    print("3. Run these commands (replace YOUR_USERNAME):")
    print("\n   git remote add origin https://github.com/YOUR_USERNAME/deixis-analysis-pipeline.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n✅ Repository preparation complete!")
    
    # Create a summary file
    with open(repo_dir / "GITHUB_READY.txt", "w") as f:
        f.write("Repository is ready for GitHub!\n\n")
        f.write("Next steps:\n")
        f.write('1. Run: git commit -m "Initial commit: Deixis Analysis Pipeline"\n')
        f.write("2. Create repository on GitHub\n")
        f.write("3. Add remote and push\n")
    
    print("\n📄 Created GITHUB_READY.txt with instructions")

if __name__ == "__main__":
    prepare_repository()