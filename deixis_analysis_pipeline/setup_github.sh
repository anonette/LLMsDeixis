#!/bin/bash

# Setup script for GitHub repository
# Run this script to initialize git and prepare for GitHub push

echo "Setting up Deixis Analysis Pipeline for GitHub..."

# Initialize git repository
cd deixis_analysis_pipeline
git init

# Rename README files
mv README_GITHUB.md README.md

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Deixis Analysis Pipeline - Multi-Model Ethical Reasoning Study

This comprehensive analysis pipeline studies how GPT-4o, Claude 3.5 Sonnet, and DeepSeek
respond to ethical dilemmas across various deictic framings.

Key features:
- Analysis of 6 ethical dilemmas across 9 deictic framings
- Comparison of 3 leading language models
- Discovery of the 'Philosophy Textbook Effect'
- Complete documentation and reproducible pipeline"

# Add remote repository (user needs to replace with their GitHub URL)
echo ""
echo "Now you need to:"
echo "1. Create a new repository on GitHub named 'deixis-analysis-pipeline'"
echo "2. Run the following commands (replace YOUR_USERNAME with your GitHub username):"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/deixis-analysis-pipeline.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "Repository is ready for GitHub!"